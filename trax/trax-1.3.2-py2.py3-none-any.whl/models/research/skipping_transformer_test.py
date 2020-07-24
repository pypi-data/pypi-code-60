# coding=utf-8
# Copyright 2020 The Trax Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Tests for Reformer models."""

from absl.testing import absltest
import numpy as np

from trax import shapes
from trax.models.research import skipping_transformer


class SkippingTransformerTest(absltest.TestCase):

  def test_skipping_transformer_forward_shape(self):
    """Tests that the forward pass runs and returns the expected shape."""
    vocab_size = 16
    model = skipping_transformer.SkippingTransformerLM(
        vocab_size, d_model=32, d_ff=64, n_layers=2, n_heads=2, max_len=16)
    xs = [np.ones((1, 8)).astype(np.int32),
          np.ones((1, 8)).astype(np.int32)]
    _, _ = model.init(shapes.signature(xs))
    ys = model(xs)
    self.assertEqual([y.shape for y in ys], [(1, 8, 16), (1, 8)])


if __name__ == '__main__':
  absltest.main()
