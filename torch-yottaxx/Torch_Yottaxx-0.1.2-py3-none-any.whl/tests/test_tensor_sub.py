import unittest
from autograd import Tensor


class TestTensorSub(unittest.TestCase):
    def test_simple_sub(self):
        t1 = Tensor([1, 2, 3], requires_grad=True)
        t2 = Tensor([4, 5, 6], requires_grad=True)
        t3 = t1 - t2
        assert t3.data.tolist()==[-3,-3,-3]

        t3.backward(Tensor([-1, -2, -3]))
        assert t1.grad.data.tolist() == [-1, -2, -3]
        assert t2.grad.data.tolist() == [1, 2, 3]

        t1 -= 0.1
        assert t1.grad is None
        assert t1.data.tolist() == [0.9, 1.9, 2.9]

    def test_broadcast_sub(self):
        """
        eg: t1.shape==(10,5)  t2.shape=(5,) => t1 + t2  ,viewed as(1,5)
            t2=[1,2,3,4,5] => viewed v2 as[[1,2,3,4,5]]

        eg:
            t1 as (10,5)
            t2 as (1,5) ias [[1,2,3,4,,5]]
        :return:
        """
        t1 = Tensor([[1, 2, 3], [4, 5, 6]], requires_grad=True)
        t2 = Tensor([7, 8, 9], requires_grad=True)

        t3 = t1-t2  # shape(2,3)
        assert t3.data.tolist()==[[-6,-6,-6],[-3,-3,-3]]
        t3.backward(Tensor([[1, 1, 1], [1, 1, 1]]))

        assert t1.grad.data.tolist() == [[1, 1, 1], [1, 1, 1]]
        assert t2.grad.data.tolist() == [-2, -2, -2]

    def test_broadcast_sub2(self):
        t1 = Tensor([[1, 2, 3], [4, 5, 6]], requires_grad=True)
        t2 = Tensor([[7, 8, 9]], requires_grad=True)

        t3 = t1-t2  # shape(2,3)
        assert t3.data.tolist()==[[-6,-6,-6],[-3,-3,-3]]
        t3.backward(Tensor([[1, 1, 1], [1, 1, 1]]))

        assert t1.grad.data.tolist() == [[1, 1, 1], [1, 1, 1]]
        assert t2.grad.data.tolist() == [[-2, -2, -2]]
