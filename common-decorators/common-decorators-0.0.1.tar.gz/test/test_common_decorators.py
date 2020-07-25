from common_decorators import (
    lazy
)


def test_lazy():
    class A:
        def __init__(self):
            self._init = False

        @lazy
        def a(self):
            if self._init:
                raise RuntimeError('boooooom')

            self._init = True

            return 1

    A.b = A.a

    a = A()

    assert a.a == 1
    assert a.a == 1

    b = A()

    assert b.b == 1
    assert b.a == 1
