"""Upon import, print the source of the main module."""

import inspect
import __main__

try:
    print(inspect.getsource(__main__), end='')
except TypeError:
    # In interactive mode, __main__ has no source. It's considered a builtin.
    pass
