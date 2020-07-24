#!/usr/bin/env python3
import os
import pathlib
import json
import shutil
import datetime

from flask_cors import CORS
from flask import Flask, request, send_file, render_template, send_from_directory, Response
from typing import List, Callable
from time import sleep

import mmpm.utils
import mmpm.consts
import mmpm.core
import mmpm.models

MagicMirrorPackage = mmpm.models.MagicMirrorPackage
get_env: Callable = mmpm.utils.get_env

app = Flask(
    __name__,
    root_path=mmpm.consts.MMPM_WEB_ROOT_DIR,
    static_folder=mmpm.consts.MMPM_STATIC_DIR,
    template_folder=mmpm.consts.MMPM_TEMPLATES_DIR,
)

app.config['CORS_HEADERS'] = 'Content-Type'

resources: dict = {
    r'/*': {'origins': '*'},
    r'/api/*': {'origins': '*'},
    r'/socket.io/*': {'origins': '*'},
}

CORS(app)

api = lambda path: f'/api/{path}'

_packages_ = mmpm.core.load_packages()


def __deserialize_selected_packages__(rqst, key: str = 'selected-packages') -> List[MagicMirrorPackage]:
    '''
    Helper method to extract a list of MagicMirrorPackage objects from Flask
    request object

    Parameters:
       request (werkzeug.wrappers.Request): the Flask request object

    Returns:
        selected_packages (List[MagicMirrorPackage]): extracted list of MagicMirrorPackage objects
    '''

    pkgs: dict = rqst.get_json(force=True)[key]

    MAGICMIRROR_MODULES_DIR: str = os.path.join(get_env(mmpm.consts.MMPM_MAGICMIRROR_ROOT_ENV), 'modules')
    default_directory = lambda title: os.path.normpath(os.path.join(MAGICMIRROR_MODULES_DIR, title))

    for pkg in pkgs:
        print(pkg)

        if not pkg['directory']:
            pkg['directory'] = default_directory(pkg['title'])

    return [MagicMirrorPackage(**pkg) for pkg in pkgs]


@app.after_request
def after_request(response: Response) -> Response:
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response


@app.route('/<path:path>', methods=[mmpm.consts.GET])
def static_proxy(path):
    return send_from_directory('./', path)


@app.route('/', methods=[mmpm.consts.GET, mmpm.consts.POST, mmpm.consts.DELETE])
def root() -> str:
    return render_template('index.html')


@app.errorhandler(500)
def server_error(error) -> Response:
    return Response(f'An internal error occurred [{__name__}.py]: {error}', status=500)


#  -- START: PACKAGES --
@app.route(api('packages/marketplace'), methods=[mmpm.consts.GET])
def packages_marketplace() -> Response:
    mmpm.utils.log.info('Sending all marketplace packages')
    return Response(json.dumps(_packages_, default=lambda pkg: pkg.serialize_full()))


@app.route(api('packages/installed'), methods=[mmpm.consts.GET])
def packages_installed() -> Response:
    mmpm.utils.log.info('Sending all installed packages')
    return Response(json.dumps(mmpm.core.get_installed_packages(_packages_), default=lambda pkg: pkg.serialize_full()))


@app.route(api('packages/external'), methods=[mmpm.consts.GET])
def packages_external() -> Response:
    mmpm.utils.log.info('Sending all external packages')
    return Response(json.dumps(mmpm.core.load_external_packages(), default=lambda pkg: pkg.serialize_full()))


@app.route(api('packages/install'), methods=[mmpm.consts.POST])
def packages_install() -> Response:
    selected_packages: List[MagicMirrorPackage] = __deserialize_selected_packages__(request)
    failures: List[dict] = []

    for package in selected_packages:
        error = mmpm.core.install_package(package, assume_yes=True)

        if error:
            mmpm.utils.log.error(f'Failed to install {package.title} with error of: {error}')
            failures.append({'package': package.serialize(), 'error': error})
        else:
            mmpm.utils.log.info(f'Installed {package.title}')

    return Response(json.dumps(failures))


@app.route(api('packages/remove'), methods=[mmpm.consts.POST])
def packages_remove() -> Response:
    # not bothering with serialization since the directory is already included in the request
    selected_packages: List[dict] = request.get_json(force=True)['selected-packages']
    failures: List[dict] = []

    for package in selected_packages:
        directory = package['directory']
        mmpm.utils.log.info(f"Attempting to removing {package['title']} at {directory}")

        try:
            shutil.rmtree(directory)
        except PermissionError as error:
            failures.append({'package': package, 'error': f"Cannot remove {directory}: {str(error)}"})
        except Exception as error:
            failures.append({'package': package, 'error': f"Cannot remove {directory}: {str(error)}"})
        finally:
            sleep(0.05)

    return Response(json.dumps(failures))


@app.route(api('packages/upgrade'), methods=[mmpm.consts.POST])
def packages_upgrade() -> Response:
    selected_packages: List[MagicMirrorPackage] = __deserialize_selected_packages__(request)
    mmpm.utils.log.info(f'Request to upgrade {selected_packages}')

    failures: List[dict] = []

    for package in selected_packages:
        error = mmpm.core.upgrade_package(package)
        if error:
            mmpm.utils.log.error(f'Failed to upgrade {package.title} with error of: {error}')
            failures.append({'package': package.serialize(), 'error': error})

    mmpm.utils.log.info('Finished executing upgrades')
    return Response(json.dumps(failures))


@app.route(api('packages/update'), methods=[mmpm.consts.GET])
def packages_update() -> Response:
    try:
        mmpm.core.check_for_package_updates(_packages_)
        mmpm.core.check_for_mmpm_updates()
        mmpm.core.check_for_magicmirror_updates()
    except Exception as error:
        mmpm.utils.log.error(str(error))
        return Response(json.dumps(False))

    return Response(json.dumps(True))

@app.route(api('packages/upgradeable'), methods=[mmpm.consts.GET])
def packages_upgradeable() -> Response:
    mmpm.utils.log.info('Request to get upgradeable packages')
    available_upgrades: dict = mmpm.core.get_available_upgrades()

    MMPM_MAGICMIRROR_ROOT: str = os.path.normpath(os.path.join(get_env(mmpm.consts.MMPM_MAGICMIRROR_ROOT_ENV)))

    available_upgrades[MMPM_MAGICMIRROR_ROOT][mmpm.consts.PACKAGES] = [
        pkg.serialize_full() for pkg in available_upgrades[MMPM_MAGICMIRROR_ROOT][mmpm.consts.PACKAGES]
    ]

    available_upgrades[MMPM_MAGICMIRROR_ROOT][mmpm.consts.MMPM] = available_upgrades[mmpm.consts.MMPM]
    return Response(json.dumps(available_upgrades[MMPM_MAGICMIRROR_ROOT]))
#  -- END: PACKAGES --


#  -- START: EXTERNAL PACKAGES --
@app.route(api('external-packages/add'), methods=[mmpm.consts.POST])
def external_packages_add() -> Response:
    package: dict = request.get_json(force=True)['external-package']

    failures: List[dict] = []

    error: str = mmpm.core.add_external_package(
        title=package.get('title'),
        author=package.get('author'),
        description=package.get('description'),
        repo=package.get('repository')
    )

    failures.append({'package': package, 'error': error})
    return Response(json.dumps({'error': "no_error" if not error else error}))


@app.route(api('external-packages/remove'), methods=[mmpm.consts.DELETE])
def external_packages_remove() -> Response:
    selected_packages: List[MagicMirrorPackage] = __deserialize_selected_packages__(request, 'external-packages')
    mmpm.utils.log.info('Request to remove external sources')

    ext_packages: dict = {mmpm.consts.EXTERNAL_PACKAGES: []}
    marked_for_removal: list = []
    external_packages: List[MagicMirrorPackage] = mmpm.core.load_external_packages()[mmpm.consts.EXTERNAL_PACKAGES]

    for selected_package in selected_packages:
        for external_package in external_packages:
            if external_package == selected_package:
                marked_for_removal.append(external_package)
                mmpm.utils.log.info(f'Found matching external module ({external_package.title}) and marked for removal')

    for package in marked_for_removal:
        external_packages.remove(package)
        mmpm.utils.log.info(f'Removed {package.title}')

    try:
        with open(mmpm.consts.MMPM_EXTERNAL_PACKAGES_FILE, 'w') as mmpm_ext_srcs:
            json.dump(ext_packages, mmpm_ext_srcs)

        mmpm.utils.log.info(f'Wrote updated external modules to {mmpm.consts.MMPM_EXTERNAL_PACKAGES_FILE}')

    except IOError as error:
        mmpm.utils.log.error(error)
        return Response(json.dumps({'error': str(error)}))

    mmpm.utils.log.info(f'Wrote external modules to {mmpm.consts.MMPM_EXTERNAL_PACKAGES_FILE}')
    return Response(json.dumps({'error': "no_error"}))
#  -- END: EXTERNAL PACKAGES --


#  -- START: MAGICMIRROR --
@app.route(api('magicmirror/config'), methods=[mmpm.consts.GET, mmpm.consts.POST])
def magicmirror_config() -> Response:
    MAGICMIRROR_CONFIG_DIR: str = os.path.join(get_env(mmpm.consts.MMPM_MAGICMIRROR_ROOT_ENV), 'config')
    MAGICMIRROR_CONFIG_FILE: str = os.path.join(MAGICMIRROR_CONFIG_DIR, 'config.js')

    if request.method == mmpm.consts.GET:
        if not os.path.exists(MAGICMIRROR_CONFIG_FILE):
            does_not_exist: str = f'// {MAGICMIRROR_CONFIG_FILE} not found. An empty file was created for you in its place'
            try:
                pathlib.Path(MAGICMIRROR_CONFIG_DIR).mkdir(parents=True, exist_ok=True)
                pathlib.Path(MAGICMIRROR_CONFIG_FILE).touch(mode=0o664, exist_ok=True)
                return Response(does_not_exist)
            except OSError:
                return Response(does_not_exist)

        mmpm.utils.log.info('Retrieving MagicMirror config')
        return send_file(MAGICMIRROR_CONFIG_FILE, attachment_filename='config.js')

    data: dict = request.get_json(force=True)
    mmpm.utils.log.info('Saving MagicMirror config file')

    try:
        with open(MAGICMIRROR_CONFIG_FILE, 'w') as config:
            config.write(data.get('code'))
    except IOError:
        return Response(json.dumps(False))

    return Response(json.dumps(True))


@app.route(api('magicmirror/custom-css'), methods=[mmpm.consts.GET, mmpm.consts.POST])
def magicmirror_custom_css() -> Response:
    MAGICMIRROR_CUSTOM_DIR: str = os.path.join(get_env(mmpm.consts.MMPM_MAGICMIRROR_ROOT_ENV), 'custom')
    MAGICMIRROR_CUSTOM_CSS_FILE: str = os.path.join(MAGICMIRROR_CUSTOM_DIR, 'custom.css')

    if request.method == mmpm.consts.GET:
        if not os.path.exists(MAGICMIRROR_CUSTOM_CSS_FILE):
            try:
                pathlib.Path(MAGICMIRROR_CUSTOM_DIR).mkdir(parents=True, exist_ok=True)
                pathlib.Path(MAGICMIRROR_CUSTOM_CSS_FILE).touch(mode=0o664, exist_ok=True)
            except OSError:
                message: str = f'/* File not found. Unable to create {MAGICMIRROR_CUSTOM_CSS_FILE}. Is the MagicMirror directory owned by root? */'
                mmpm.utils.log.error(message)
                return Response(message)

        mmpm.utils.log.info(f'Retrieving MagicMirror {MAGICMIRROR_CUSTOM_CSS_FILE}')
        return send_file(MAGICMIRROR_CUSTOM_CSS_FILE, attachment_filename='custom.css')

    # POST
    data: dict = request.get_json(force=True)
    mmpm.utils.log.info(f'Saving MagicMirror {MAGICMIRROR_CUSTOM_CSS_FILE}')

    try:
        with open(MAGICMIRROR_CUSTOM_CSS_FILE, 'w') as custom_css:
            custom_css.write(data.get('code'))
    except IOError:
        return Response(json.dumps(False))

    return Response(json.dumps(True))


@app.route(api('magicmirror/start'), methods=[mmpm.consts.GET])
def magicmirror_start() -> Response:
    '''
    Restart the MagicMirror by killing all associated processes, the
    re-running the startup script for MagicMirror

    Parameters:
        None

    Returns:
        bool: True if the command was called, False it appears that MagicMirror is currently running
    '''
    # there really isn't an easy way to capture return codes for the background
    # process

    # if these processes are all running, we assume MagicMirror is running currently
    if mmpm.utils.is_magicmirror_running():
        mmpm.utils.log.info('MagicMirror appears to be running already. Returning False.')
        return Response(json.dumps({'error': 'MagicMirror appears to be running already'}))

    mmpm.utils.log.info('MagicMirror does not appear to be running currently. Returning True.')
    mmpm.core.start_magicmirror()
    return Response(json.dumps({'error': ''}))


@app.route(api('magicmirror/restart'), methods=[mmpm.consts.GET])
def magicmirror_restart() -> Response:
    '''
    Restart the MagicMirror by killing all associated processes, then
    re-running the startup script for MagicMirror

    Parameters:
        None

    Returns:
        bool: Always True only as a signal the process was called
    '''
    # same issue as the start-magicmirror api call
    mmpm.core.restart_magicmirror()
    return Response(json.dumps(True))


@app.route(api('magicmirror/stop'), methods=[mmpm.consts.GET])
def magicmirror_stop() -> Response:
    '''
    Stop the MagicMirror by killing all associated processes

    Parameters:
        None

    Returns:
        bool: Always True only as a signal the process was called
    '''
    # same sort of issue as the start-magicmirror call
    mmpm.core.stop_magicmirror()
    return Response(json.dumps(True))


@app.route(api('magicmirror/upgrade'), methods=[mmpm.consts.GET])
def magicmirror_upgrade() -> Response:
    mmpm.utils.log.info('Request to upgrade MagicMirror')
    mmpm.utils.log.info('Finished installing')

    error: str = mmpm.core.upgrade_magicmirror()

    if mmpm.utils.is_magicmirror_running():
        mmpm.core.restart_magicmirror()

    return Response(json.dumps({'error': error}))

@app.route(api('magicmirror/install-mmpm-module'))
def magicmirror_install_mmpm_module() -> Response:
    return Response(json.dumps({'error': mmpm.core.install_mmpm_as_magicmirror_module(assume_yes=True)}))
#  -- END: MAGICMIRROR --


#  -- START: RASPBERRYPI --
@app.route(api('raspberrypi/restart'), methods=[mmpm.consts.GET])
def raspberrypi_restart() -> Response:
    '''
    Reboot the RaspberryPi

    Parameters:
        None

    Returns:
        success (bool): If the command fails, False is returned. If success, the return will never reach the interface
    '''

    mmpm.utils.log.info('Restarting RaspberryPi')
    mmpm.core.stop_magicmirror()
    error_code, _, _ = mmpm.utils.run_cmd(['sudo', 'reboot'])
    # if success, it'll never get the response, but we'll know if it fails
    return Response(json.dumps(bool(not error_code)))


@app.route(api('raspberrypi/stop'), methods=[mmpm.consts.GET])
def raspberrypi_stop() -> Response:
    '''
    Shut down the RaspberryPi

    Parameters:
        None

    Returns:
        success (bool): If the command fails, False is returned. If success, the return will never reach the interface
    '''

    mmpm.utils.log.info('Shutting down RaspberryPi')
    # if success, we'll never get the response, but we'll know if it fails
    mmpm.core.stop_magicmirror()
    error_code, _, _ = mmpm.utils.run_cmd(['sudo', 'shutdown', '-P', 'now'])
    return Response(json.dumps(bool(not error_code)))


@app.route(api('raspberrypi/rotate-screen'), methods=[mmpm.consts.POST])
def raspberrypi_rotate_screent() -> Response:
    degrees: int = request.get_json(force=True)['degrees']
    return Response(json.dumps({'error': mmpm.core.rotate_raspberrypi_screen(degrees, assume_yes=True)}))
#  -- END: RASPBERRYPI --


#  -- START: MMPM --
@app.route(api('mmpm/download-logs'), methods=[mmpm.consts.GET])
def download_log_files() -> Response:
    os.chdir('/tmp')
    today = datetime.datetime.now()
    zip_file_name = f'mmpm-logs-{today.year}-{today.month}-{today.day}'
    shutil.make_archive(zip_file_name, 'zip', mmpm.consts.MMPM_LOG_DIR)
    return send_file(f'/tmp/{zip_file_name}.zip', attachment_filename='{}.zip'.format(zip_file_name), as_attachment=True)


@app.route(api('mmpm/environment-vars'), methods=[mmpm.consts.GET])
def mmpm_environment_vars() -> Response:
    env_vars: dict = {}

    with open(mmpm.consts.MMPM_ENV_FILE, 'r') as env:
        try:
            env_vars = json.load(env)
        except json.JSONDecodeError:
            pass

    return Response(json.dumps(env_vars))


@app.route(api('mmpm/environment-vars-file'), methods=[mmpm.consts.GET, mmpm.consts.POST])
def mmpm_environment_vars_file() -> Response:
    if request.method == mmpm.consts.GET:
        return send_file(mmpm.consts.MMPM_ENV_FILE, attachment_filename='mmpm-env.json')

    data: dict = request.get_json(force=True)
    mmpm.utils.log.info('Saving MMPM environment variables file')

    try:
        with open(mmpm.consts.MMPM_ENV_FILE, 'w') as config:
            config.write(data.get('code'))
    except IOError:
        return Response(json.dumps(False))

    return Response(json.dumps(True))
