import contextlib
import functools
import os
import shutil
import tempfile

from pathlib import Path

from typing import AnyStr


@contextlib.contextmanager
def temp_dir(
    suffix: AnyStr = "",
    prefix: AnyStr = "tmp",
    parent_dir: AnyStr = None,
    make_cwd=False,
):
    """ Create a temporary directory and optionally change the current
        working directory to it. The directory is deleted when the context
        exits.

        The temporary directory is created when entering the context
        manager, and deleted when exiting it:
        >>> import temporary
        >>> with temporary.temp_dir() as temp_dir:
        ...     assert temp_dir.is_dir()
        >>> assert not temp_dir.exists()

        This time let's make the temporary directory our working directory:
        >>> import os
        >>> with temporary.temp_dir(make_cwd=True) as temp_dir:
        ...     assert str(temp_dir) == os.getcwd()
        >>> assert not str(temp_dir) == os.getcwd()

        The suffix, prefix, and parent_dir options are passed to the
        standard ``tempfile.mkdtemp()`` function:
        >>> with temporary.temp_dir() as p:
        ...     with temporary.temp_dir(suffix='suf', prefix='pre'
        parent_dir=p) as d:
        ...         assert d.parent == p
        ...         assert d.name.startswith('pre')
        ...         assert d.name.endswith('suf')

        This function can also be used as a decorator, with the in_temp_dir
        alias:
        >>> @temporary.in_temp_dir()
        ... def my_function():
        ...     assert old_cwd != os.getcwd()
        ...
        >>> old_cwd = os.getcwd()
        >>> my_function()
        >>> assert old_cwd == os.getcwd()
        """
    prev_cwd = Path().cwd()

    # if not parent directory is given, use cwd
    parent_dir = Path(parent_dir).resolve() if parent_dir else prev_cwd

    tmp_dir = tempfile.TemporaryDirectory(suffix=suffix, prefix=prefix, dir=parent_dir)

    abs_path = tempfile.mkdtemp(suffix, prefix, parent_dir)
    path = Path(abs_path)
    try:
        if make_cwd:
            os.chdir(str(abs_path))
        yield path.resolve()
    finally:
        if make_cwd:
            os.chdir(prev_cwd)
        with temporary.util.allow_missing_file():
            shutil.rmtree(str(abs_path))


in_temp_dir = functools.partial(temp_dir, make_cwd=True)  # pylint: disable=invalid-name
