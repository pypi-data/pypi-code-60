import numpy as np
from typing import List, NamedTuple, Callable, Optional, Union


# NamedTuple 三种取值：index name getattr()

class Dependency(NamedTuple):
    tensor: 'Tensor'
    grad_fn: Callable[[np.ndarray], np.ndarray]  # 张量依赖关系


Arrayable = Union[float, list, np.ndarray]


def ensure_array(arrayable: Arrayable) -> np.ndarray:
    if isinstance(arrayable, np.ndarray):
        return arrayable
    elif isinstance(arrayable, Tensor):
        return arrayable.data
    else:
        return np.array(arrayable, dtype=np.float64)


Tensorable = Union['Tensor', float, np.ndarray]


def ensure_tensor(tensorable: Tensorable) -> 'Tensor':
    if isinstance(tensorable, Tensor):
        return tensorable
    else:
        return Tensor(tensorable)


class Tensor:
    def __init__(self, data: Arrayable, requires_grad: bool = False, depends_on: List[Dependency] = None) -> None:
        self._data = ensure_array(data)
        self.requires_grad = requires_grad
        self.depends_on = depends_on or []
        self.shape = self.data.shape
        self.grad: Optional['Tensor'] = None
        if self.requires_grad:
            self.zero_grad()

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, new_data: np.ndarray) -> None:
        self._data = new_data
        self.grad = None

    def zero_grad(self) -> None:
        self.grad = Tensor(np.zeros_like(self.data, dtype=np.float64))

    def __repr__(self) -> str:
        return f"Tensor({self.data},requires_grad={self.requires_grad})"

    def sum(self) -> 'Tensor':
        return tensor_sum(self)

    def __add__(self, other) -> 'Tensor':
        """
        get called if do t+ other
        :param other:
        :return:
        """
        return _add(self, ensure_tensor(other))

    def __radd__(self, other) -> 'Tensor':
        """
        get called if other + t
        :param other:
        :return:
        """
        return _add(ensure_tensor(other), self)

    def __iadd__(self, other) -> 'Tensor':
        """
        when we do t+=other
        :param other:
        :return:
        """
        self.data += ensure_tensor(other).data
        # invalidate the gradient
        return self

    def __isub__(self, other) -> 'Tensor':
        self.data -= ensure_tensor(other).data
        # invalidate the gradient
        return self

    def __imul__(self, other) -> 'Tensor':
        self.data *= ensure_tensor(other).data
        # invalidate the gradient
        return self

    def __mul__(self, other) -> 'Tensor':
        return _mul(self, ensure_tensor(other))

    def __rmul__(self, other) -> 'Tensor':
        return _mul(ensure_tensor(other), self)

    def __matmul__(self, other) -> 'Tensor':
        return _matmul(self, ensure_tensor(other))

    def __neg__(self) -> 'Tensor':
        return _neg(self)

    def __sub__(self, other) -> 'Tensor':
        return _sub(self, ensure_tensor(other))

    def __rsub__(self, other) -> 'Tensor':
        return _sub(ensure_tensor(other), self)

    def __getitem__(self, item) -> 'Tensor':
        return _slice(self, item)

    def backward(self, grad: 'Tensor' = None) -> None:
        assert self.requires_grad, "called backward on non-requires-grad tensor"

        if grad is None:
            if self.shape == ():
                grad = Tensor(1.0)
            else:
                raise RuntimeError("grad must be specified for non-0-Tensor")

        self.grad.data += grad.data
        for dependency in self.depends_on:
            backward_grad = dependency.grad_fn(grad.data)
            dependency.tensor.backward(Tensor(backward_grad))


def tensor_sum(t: Tensor) -> Tensor:
    """
    tankes a tensor and returns the 0-tensor
    that's the sum of all its elemetns;
    :param t:
    :return:
    """
    data = t.data.sum()
    requires_grad = t.requires_grad
    if requires_grad:
        def grad_fn(grad: np.ndarray) -> np.ndarray:
            """
            grad is necessarily a 0-tenosr, so each input element contributes that much
            :param grad:
            :return:
            """
            return grad * np.ones_like(t.data)

        depends_on = [Dependency(t, grad_fn)]

    else:
        depends_on = []

    return Tensor(data, requires_grad, depends_on)


def _add(t1: Tensor, t2: Tensor) -> Tensor:
    data = t1.data + t2.data
    requires_grad = t1.requires_grad or t2.requires_grad
    depends_on: List[Dependency] = []

    if t1.requires_grad:
        def grad_fn1(grad: np.ndarray) -> np.ndarray:
            # handel broadcasting properly

            # sum out added dims
            # (2,3)+(3,)
            ndims_added = grad.ndim - t1.data.ndim
            for _ in range(ndims_added):
                grad = grad.sum(axis=0)

            # sum across braodcasted(but non-added dims)
            # (2,3) + (1,3)
            for i, dim in enumerate(t1.shape):
                if dim == 1:
                    grad = grad.sum(axis=i, keepdims=True)
            return grad

        depends_on.append(Dependency(t1, grad_fn1))

    if t2.requires_grad:
        def grad_fn2(grad: np.ndarray) -> np.ndarray:
            ndims_added = grad.ndim - t2.data.ndim
            for _ in range(ndims_added):
                grad = grad.sum(axis=0)

            for i, dim in enumerate(t2.shape):
                if dim == 1:
                    grad = grad.sum(axis=i, keepdims=True)

            return grad

        depends_on.append(Dependency(t2, grad_fn2))

    return Tensor(data, requires_grad, depends_on)


def _mul(t1: Tensor, t2: Tensor) -> Tensor:
    """
    y = a * b
    have dL/dy
    dL/da = dL/dy * b
    :param t1:
    :param t2:
    :return:
    """
    data = t1.data * t2.data
    requires_grad = t1.requires_grad or t2.requires_grad
    depends_on: List[Dependency] = []

    if t1.requires_grad:
        def grad_fn1(grad: np.ndarray) -> np.ndarray:
            # handel broadcasting properly
            grad = grad * t2.data
            # sum out added dims
            # (2,3)+(3,)
            ndims_added = grad.ndim - t1.data.ndim
            for _ in range(ndims_added):
                grad = grad.sum(axis=0)

            # sum across braodcasted(but non-added dims)
            # (2,3) + (1,3)
            for i, dim in enumerate(t1.shape):
                if dim == 1:
                    grad = grad.sum(axis=i, keepdims=True)
            return grad

        depends_on.append(Dependency(t1, grad_fn1))

    if t2.requires_grad:
        def grad_fn2(grad: np.ndarray) -> np.ndarray:
            grad = grad * t1.data
            ndims_added = grad.ndim - t2.data.ndim
            for _ in range(ndims_added):
                grad = grad.sum(axis=0)

            for i, dim in enumerate(t2.shape):
                if dim == 1:
                    grad = grad.sum(axis=i, keepdims=True)

            return grad

        depends_on.append(Dependency(t2, grad_fn2))

    return Tensor(data, requires_grad, depends_on)


def _neg(t: Tensor) -> Tensor:
    data = -t.data
    requires_grad = t.requires_grad
    if requires_grad:
        depends_on = [Dependency(t, lambda x: -x)]

    else:
        depends_on = []

    return Tensor(data, requires_grad, depends_on)


def _sub(t1: Tensor, t2: Tensor) -> Tensor:
    return t1 + -t2


def _matmul(t1: Tensor, t2: Tensor) -> Tensor:
    """
        if t1 =(n1,m1) and t2 is (m1,m2) then t1 @ t2 = (n1,m2)
        so grad3  is (n1,m2)

        if t3 = t1 @ t2
        and grad3 if the gradient of some function wrt t3 ,
        then
        grad1 = grad3 @t2.T (n1,m2) * (m2,m1)
        grad2 = t1.T @ grad3 (m1,n1) * (n1.m2)


        """
    data = t1.data @ t2.data
    requires_grad = t1.requires_grad or t2.requires_grad
    depends_on: List[Dependency] = []

    if t1.requires_grad:
        def grad_fn1(grad: np.ndarray) -> np.ndarray:
            # handel broadcasting properly
            return grad @ t2.data.T

        depends_on.append(Dependency(t1, grad_fn1))

    if t2.requires_grad:
        def grad_fn2(grad: np.ndarray) -> np.ndarray:
            return t1.data.T @ grad

        depends_on.append(Dependency(t2, grad_fn2))

    return Tensor(data, requires_grad, depends_on)


def _slice(t: Tensor, idx) -> Tensor:
    """
    :param t:
    :param idx:
    :return:
    """
    data = t.data[idx]
    requires_grad = t.requires_grad

    if requires_grad:
        def grad_fn(grad: np.ndarray) -> np.ndarray:
            bigger_grad = np.zeros_like(data)
            bigger_grad[idx] = grad
            return bigger_grad

        depends_on = Dependency(t, grad_fn)

    else:
        depends_on = []

    return Tensor(data, requires_grad, depends_on)
