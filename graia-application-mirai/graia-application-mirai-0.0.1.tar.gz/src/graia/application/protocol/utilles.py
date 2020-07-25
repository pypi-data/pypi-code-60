from typing import Union
from graia.broadcast.entities.dispatcher import BaseDispatcher
from graia.broadcast.interfaces.dispatcher import DispatcherInterface
from .exceptions import (AccountMuted, AccountNotFound, InvaildArgument,
                         InvaildAuthkey, InvaildSession, NotSupportedVersion,
                         TooLongMessage, UnauthorizedSession, UnknownTarget)
from ..context import enter_context


def requireAuthenticated(func):
    def wrapper(self, *args, **kwargs):
        if not self.connect_info.sessionKey:
            raise InvaildSession("you must authenticate before this.")
        return func(self, *args, **kwargs)
    wrapper.__annotations__ = func.__annotations__
    return wrapper

def SinceVersion(*version: int):
    def wrapper(func):
        def inside_wrapper(self, *args, **kwargs):
            if self.connect_info.current_version and \
                self.connect_info.current_version < version:
                raise NotSupportedVersion(
                    "the current version does not support this feature: {0}".format(self.connect_info.current_version)
                )
            return func(*args, **kwargs)
        return inside_wrapper
    return wrapper

def DeprecatedSince(*version: int, action: str = "warn"):
    if action not in ["warn", "error", "ignore"]:
        raise TypeError("action must be in" + str(["warn", "error", "ignore"]))
    def wrapper(func):
        def inside_wrapper(self, *args, **kwargs):
            if self.connect_info.current_version and \
                self.connect_info.current_version > version:
                if action == "error":
                    raise NotSupportedVersion(
                        "the current version deprecated this feature: {0}".format(self.connect_info.current_version)
                    )
                elif action == "warn":
                    import warnings
                    warnings.warn(
                        "'{0}' has been deprecated since {1}, use other methods to realize your business as soon as possible!"\
                        .format(func.__qualname__, version))
            return func(*args, **kwargs)
        return inside_wrapper
    return wrapper

code_exceptions_mapping = {
    1: InvaildAuthkey,
    2: AccountNotFound,
    3: InvaildSession,
    4: UnauthorizedSession,
    5: UnknownTarget,
    6: FileNotFoundError,
    10: PermissionError,
    20: AccountMuted,
    30: TooLongMessage,
    400: InvaildArgument
}

def raise_for_return_code(code: Union[dict, int]):
    if isinstance(code, dict):
        code = code.get("code")
        exception_code = code_exceptions_mapping.get(code)
        if exception_code:
            raise exception_code
    elif isinstance(code, int):
        exception_code = code_exceptions_mapping.get(code)
        if exception_code:
            raise exception_code

class AppMiddlewareAsDispatcher(BaseDispatcher):
    def __init__(self, app) -> None:
        self.app = app

    def catch(self, interface: "DispatcherInterface"):
        with enter_context(self.app, interface.event):
            yield

def context_enter_auto(context):
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            with context:
                return func(*args, **kwargs)
        return wrapper2
    return wrapper1