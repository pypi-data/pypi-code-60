from collections import namedtuple

import pytest
import torch

from zero.metrics import Metric

Point = namedtuple('Point', ['x', 'y'])
Model = namedtuple('Model', ['model', 'weight', 'bias', 'loss_fn', 'optimizer', 'data'])


class ObjectCounter(Metric):
    def __init__(self, sign):
        self.sign = sign
        self.reset()

    def reset(self):
        self.count = 0
        return self

    def update(self, data):
        self.count += len(data[0])
        return self

    def compute(self):
        assert not self.empty
        return self.sign * self.count

    @property
    def empty(self):
        return not self.count


def make_model(data):
    model = torch.nn.Linear(data.shape[1], 1)
    return Model(
        model,
        model.weight.clone(),
        model.bias.clone(),
        lambda: model(data).sum(),
        torch.optim.SGD(model.parameters(), 0.0001),
        data,
    )


requires_gpu = pytest.mark.skipif(
    not torch.cuda.is_available(), reason="GPU is required for this test"
)
