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

"""Trax trainer."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import datetime
import os

from absl import app
from absl import flags
from absl import logging

import gin
import jax
import tensorflow.compat.v2 as tf
from trax import fastmath
from trax import trainer_flags  # pylint: disable=unused-import
from trax.supervised import trainer_lib
from trax.tf_numpy import numpy as tf_np

FLAGS = flags.FLAGS


# TODO(afrozm): Share between trainer.py and rl_trainer.py
def _tf_setup_from_flags():
  """Processes TensorFlow-relevant flags."""
  if FLAGS.enable_eager_execution:
    tf.compat.v1.enable_eager_execution()
  if FLAGS.tf_xla:
    tf.config.optimizer.set_jit(True)
    fastmath.tf_math.set_tf_xla_forced_compile(FLAGS.tf_xla_forced_compile)
  tf.config.optimizer.set_experimental_options({
      'pin_to_host_optimization': FLAGS.tf_opt_pin_to_host,
      'layout_optimizer': FLAGS.tf_opt_layout,
  })
  tf_np.set_allow_float64(FLAGS.tf_allow_float64)


# TODO(afrozm): Share between trainer.py and rl_trainer.py
def _gin_parse_configs():
  """Initializes gin-controlled bindings."""
  # Imports for configurables
  # pylint: disable=g-import-not-at-top,unused-import,g-bad-import-order,reimported,unused-variable
  from trax import models as _trax_models
  from trax import optimizers as _trax_opt
  # pylint: disable=g-import-not-at-top,unused-import,g-bad-import-order,reimported,unused-variable

  configs = FLAGS.config or []
  # Override with --dataset and --model
  if FLAGS.dataset:
    configs.append("data_streams.dataset_name='%s'" % FLAGS.dataset)
  if FLAGS.data_dir:
    configs.append("data_streams.data_dir='%s'" % FLAGS.data_dir)
  if FLAGS.model:
    configs.append('train.model=@trax.models.%s' % FLAGS.model)
  gin.parse_config_files_and_bindings(FLAGS.config_file, configs)


def _output_dir_or_default():
  """Returns a path to the output directory."""
  if FLAGS.output_dir:
    output_dir = FLAGS.output_dir
    trainer_lib.log('Using --output_dir {}'.format(output_dir))
    return os.path.expanduser(output_dir)

  # Else, generate a default output dir (under the user's home directory).
  try:
    dataset_name = gin.query_parameter('data_streams.dataset_name')
  except ValueError:
    dataset_name = 'random'
  output_name = '{model_name}_{dataset_name}_{timestamp}'.format(
      model_name=gin.query_parameter('train.model').configurable.name,
      dataset_name=dataset_name,
      timestamp=datetime.datetime.now().strftime('%Y%m%d_%H%M'),
  )
  output_dir = os.path.join('~', 'trax', output_name)
  output_dir = os.path.expanduser(output_dir)
  print()
  trainer_lib.log('No --output_dir specified')
  trainer_lib.log('Using default output_dir: {}'.format(output_dir))
  return output_dir


# TODO(afrozm): Share between trainer.py and rl_trainer.py
def _jax_and_tf_configure_for_devices():  # pylint: disable=missing-function-docstring
  if FLAGS.use_tpu:
    jax.config.update('jax_platform_name', 'tpu')
    jax.config.update('jax_xla_backend', FLAGS.jax_xla_backend)
    jax.config.update('jax_backend_target', FLAGS.jax_backend_target)
  if (FLAGS.enable_eager_execution and
      fastmath.backend_name() in ('numpy', 'jax')):
    # Numpy backend doesn't benefit from having the input pipeline run on GPU,
    # and jax backend has GPU memory contention if TF uses the GPU. Gin must be
    # set up first before determining the backend.
    tf.config.experimental.set_visible_devices([], 'GPU')


def _train_using_tf(output_dir):
  worker_cpu = tf_init_tpu()
  with tf.device(worker_cpu):
    if trainer_lib.num_devices() == 1:
      # TF's device priority is GPU > CPU > TPU, so we need to explicitly make
      # the TPU core the default device here.
      with tf.device('/device:TPU:0'):
        trainer_lib.train(output_dir=output_dir)
    else:
      trainer_lib.train(output_dir=output_dir)


@gin.configurable
def tf_init_tpu(worker='', protocol=None):
  """Initializes TPU for TensorFlow.

  Args:
    worker: The BNS address of the remote TPU worker. If it's empty (the default
      value), TF will assume the TPU devices are connected to the local host.
    protocol: The network protocol used to connect to the TPU worker.
  Returns:
    The device name of the TPU worker's CPU.
  """
  protocol = protocol or 'grpc'
  is_local = (worker in ('', 'local'))
  resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu=worker)
  if not is_local:
    tf.config.experimental_connect_to_cluster(resolver, protocol=protocol)
  tf.tpu.experimental.initialize_tpu_system(resolver)
  if is_local:
    return ''
  else:
    return '/job:worker'


def main(_):
  logging.set_verbosity(FLAGS.log_level)

  _tf_setup_from_flags()
  _gin_parse_configs()
  _jax_and_tf_configure_for_devices()

  output_dir = _output_dir_or_default()
  if FLAGS.use_tpu and fastmath.backend_name() == 'tf':
    _train_using_tf(output_dir)
  else:
    trainer_lib.train(output_dir=output_dir)

  trainer_lib.log('Finished training.')


if __name__ == '__main__':
  app.run(main)
