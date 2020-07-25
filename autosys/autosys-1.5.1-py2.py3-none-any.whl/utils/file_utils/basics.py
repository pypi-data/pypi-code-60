#!/usr/bin/env false python3
# -*- coding: utf-8 -*-
""" AutoSys Package Metadata
    ---
    Part of the [AutoSys][1] package

    Copyright (c) 2018 [Michael Treanor][2]

    AutoSys is licensed under the [MIT License][3]

    [1]: https://www.github.com/skeptycal/autosys
    [2]: https://www.twitter.com/skeptycal
    [3]: https://opensource.org/licenses/MIT
    """


try:
    # FileNotFoundError might happen in py34, and is not available with py27.
    import_errors = (ImportError, FileNotFoundError)
except NameError:
    import_errors = (ImportError,)
