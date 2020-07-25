"""
Ref: https://stackoverflow.com/a/6147060/9878098
There is a specific example of when you should use del (there may be others, but I know about this one off hand) when you are using sys.exc_info() to inspect an exception. This function returns a tuple, the type of exception that was raised, the message, and a traceback.

The first two values are usually sufficient to diagnose an error and act on it, but the third contains the entire call stack between where the exception was raised and where the the exception is caught. In particular, if you do something like

```
try:
    do_evil()
except:
    exc_type, exc_value, tb = sys.exc_info()
    if something(exc_value):
        raise
```

the traceback, tb ends up in the locals of the call stack, creating a circular reference that cannot be garbage collected. Thus, it is important to do:
"""

try:
    do_evil()
except:
    exc_type, exc_value, tb = sys.exc_info()
    del tb
    if something(exc_value):
        raise

"""
to break the circular reference. In many cases where you would want to call sys.exc_info(), like with metaclass magic, the traceback is useful, so you have to make sure that you clean it up before you can possibly leave the exception handler. If you don't need the traceback, you should delete it immediately, or just do:

```
exc_type, exc_value = sys.exc_info()[:2]
```

To avoid it all together.
"""

