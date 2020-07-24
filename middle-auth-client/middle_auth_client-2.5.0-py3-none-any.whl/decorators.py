from functools import wraps
import flask
import json
import os
from urllib.parse import quote
from furl import furl
import cachetools.func
import requests

AUTH_URI = os.environ.get('AUTH_URI', 'localhost:5000/auth')
AUTH_URL = os.environ.get('AUTH_URL', AUTH_URI)
STICKY_AUTH_URL = os.environ.get('STICKY_AUTH_URL', AUTH_URL)

USE_REDIS = os.environ.get('AUTH_USE_REDIS', "false") == "true"
TOKEN_NAME = os.environ.get('TOKEN_NAME', "middle_auth_token")
CACHE_MAXSIZE = int(os.environ.get('TOKEN_CACHE_MAXSIZE', "1024"))
CACHE_TTL = int(os.environ.get('TOKEN_CACHE_TTL', "300"))

r = None
if USE_REDIS:
    import redis
    r = redis.Redis(
        host=os.environ.get('REDISHOST', 'localhost'),
        port=int(os.environ.get('REDISPORT', 6379)))

@cachetools.func.ttl_cache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)
def user_cache_http(token):
    user_request = requests.get('https://' + AUTH_URL + '/api/v1/user/cache', headers={'authorization': 'Bearer ' + token})
    if user_request.status_code == 200:
        return user_request.json()

def get_user_cache(token):
    if USE_REDIS:
        cached_user_data = r.get("token_" + token)
        if cached_user_data:
            return json.loads(cached_user_data.decode('utf-8'))
    else:
        return user_cache_http(token)

@cachetools.func.ttl_cache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)
def is_root_public(table_id, root_id, token):
    if root_id is None:
        return False

    cip_url = 'https://{}/api/v1/table/{}/root/{}/is_public'.format(AUTH_URL, table_id, root_id)

    user_request = requests.get(cip_url, headers={'authorization': 'Bearer ' + token}, timeout=5)
    if user_request.status_code == 200:
        return user_request.json()

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if flask.request.method == 'OPTIONS':
            return f(*args, **kwargs)

        if hasattr(flask.g, 'auth_token'):
            # if authorization header has already been parsed, don't need to re-parse
            # this allows auth_required to be an optional decorator if auth_requires_role is also used
            return f(*args, **kwargs)

        token = None
        cookie_name = TOKEN_NAME

        auth_header = flask.request.headers.get('authorization')
        xrw_header = flask.request.headers.get('X-Requested-With')

        programmatic_access = xrw_header or auth_header or flask.request.environ.get('HTTP_ORIGIN')

        AUTHORIZE_URI = 'https://' + STICKY_AUTH_URL + '/api/v1/authorize'

        query_param_token = flask.request.args.get(TOKEN_NAME)

        if not query_param_token:
            # deprecated
            query_param_token = flask.request.args.get('token')

        if programmatic_access:
            if query_param_token:
                token = query_param_token
            else:
                if not auth_header:
                    resp = flask.Response("Unauthorized", 401)
                    resp.headers['WWW-Authenticate'] = 'Bearer realm="' + AUTHORIZE_URI + '"'
                    return resp
                elif not auth_header.startswith('Bearer '):
                    resp = flask.Response("Invalid Request", 400)
                    resp.headers['WWW-Authenticate'] = 'Bearer realm="' + AUTHORIZE_URI + '", error="invalid_request", error_description="Header must begin with \'Bearer\'"'
                    return resp

                token = auth_header.split(' ')[1] # remove schema
        else: # direct browser access, or a non-browser request missing auth header (user error) TODO: check user agent to deliver 401 in this case
            if query_param_token:
                resp = flask.make_response(flask.redirect(furl(flask.request.url).remove([TOKEN_NAME, 'token']).url, code=302))
                resp.set_cookie(cookie_name, query_param_token, secure=True, httponly=True)
                return resp

            token = flask.request.cookies.get(cookie_name)

        cached_user_data = get_user_cache(token) if token else None

        if cached_user_data:
            flask.g.auth_user = cached_user_data
            flask.g.auth_token = token
            return f(*args, **kwargs)
        elif not programmatic_access:
            return flask.redirect(AUTHORIZE_URI + '?redirect=' + quote(flask.request.url), code=302)
        else:
            resp = flask.Response("Invalid/Expired Token", 401)
            resp.headers['WWW-Authenticate'] = 'Bearer realm="' + AUTHORIZE_URI + '", error="invalid_token", error_description="Invalid/Expired Token"'
            return resp
    return decorated_function


def auth_requires_admin(f):
    @wraps(f)
    @auth_required
    def decorated_function(*args, **kwargs):
        if flask.request.method == 'OPTIONS':
            return f(*args, **kwargs)

        if not flask.g.auth_user['admin']:
            resp = flask.Response("Requires superadmin privilege.", 403)
            return resp
        else:
            return f(*args, **kwargs)

    return decorated_function


def auth_requires_permission(required_permission, node_key='node_id'):
    def decorator(f):
        @wraps(f)
        @auth_required
        def decorated_function(table_id, *args, **kwargs):
            if flask.request.method == 'OPTIONS':
                return f(*args, **{**kwargs, **{'table_id': table_id}})

            required_level = ['none', 'view', 'edit'].index(required_permission)

            table_id_to_dataset = {
                "pinky100_sv16": "pinky100",
                "pinky100_neo1": "pinky100",
                "akhilesh-pinky100-0": "pinky100",
                "anp0": "pinky100",
                "minnie3_v0": "minnie65",
                "anm0": "minnie65",
                "fly_v26": "fafb_sandbox",
                "fly_v31": "fafb",
                "fly_arv0": "fafb"
            }

            if table_id in table_id_to_dataset:
                dataset = table_id_to_dataset.get(table_id)
            elif table_id.startswith("pinky100_rv") or \
                    table_id.startswith("pinky100_arv") or \
                    table_id.startswith("pinky_nf"):
                dataset = "pinky100"
            elif table_id.startswith("minnie3_v"):
                dataset = "minnie65"
            else:
                raise Exception("Unknown dataset")

            if dataset is not None:
                level_for_dataset = flask.g.auth_user['permissions'].get(dataset, 0)
                has_permission = level_for_dataset >= required_level

                if has_permission or (required_level < 2 and is_root_public(table_id, kwargs.get(node_key), flask.g.auth_token)):
                    return f(*args, **{**kwargs, **{'table_id': table_id}})
                else:
                    resp = flask.Response("Missing permission: {0} for dataset {1}".format(required_permission, dataset), 403)
                    return resp
            else:
                resp = flask.Response("Invalid table_id", 400)
                return resp

        return decorated_function
    return decorator

def auth_requires_group(required_group):
    def decorator(f):
        @wraps(f)
        @auth_required
        def decorated_function(*args, **kwargs):
            if flask.request.method == 'OPTIONS':
                return f(*args, **kwargs)

            if required_group not in flask.g.auth_user['groups']:
                resp = flask.Response("Requires membership of group: {0}".format(required_group), 403)
                return resp

            return f(*args, **kwargs)

        return decorated_function
    return decorator
