import errno
import contextlib


@contextlib.contextmanager
def allow_missing_file():
    try:
        yield
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise
