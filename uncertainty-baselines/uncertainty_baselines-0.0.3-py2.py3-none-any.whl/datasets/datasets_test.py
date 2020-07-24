# coding=utf-8
# Copyright 2020 The Uncertainty Baselines Authors.
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
"""Tests for get_dataset()."""
from absl.testing import parameterized

import tensorflow.compat.v2 as tf
import uncertainty_baselines as ub


class DatasetsTest(tf.test.TestCase, parameterized.TestCase):

  @parameterized.parameters('mnist', 'glue/cola')
  def testGetDataset(self, name):
    dataset = ub.datasets.get(name, batch_size=13, eval_batch_size=17)
    self.assertEqual(dataset.name, name)

if __name__ == '__main__':
  tf.test.main()
