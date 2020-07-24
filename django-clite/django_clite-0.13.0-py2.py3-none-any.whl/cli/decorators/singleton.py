import functools


def singleton(cls):
    """
    Make a class a Singleton class (only one instance)
    Source: https://realpython.com/primer-on-python-decorators/#stateful-decorators
    """

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance
    wrapper_singleton.instance = None
    return wrapper_singleton
