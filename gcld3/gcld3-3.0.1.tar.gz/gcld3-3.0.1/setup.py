"""Setup utility for gcld3."""

import os
import shutil
import subprocess
import setuptools
from setuptools.command import build_ext

__version__ = '3.0.1'
_NAME = 'gcld3'

REQUIREMENTS = ['pybind11 >= 2.5.0', 'wheel >= 0.34.2']

PROTO_FILES = [
    'src/feature_extractor.proto',
    'src/sentence.proto',
    'src/task_spec.proto',
]

SRCS = [
    'src/base.cc',
    'src/embedding_feature_extractor.cc',
    'src/embedding_network.cc',
    'src/feature_extractor.cc',
    'src/feature_types.cc',
    'src/fml_parser.cc',
    'src/lang_id_nn_params.cc',
    'src/language_identifier_features.cc',
    'src/language_identifier_main.cc',
    'src/nnet_language_identifier.cc',
    'src/registry.cc',
    'src/relevant_script_feature.cc',
    'src/sentence_features.cc',
    'src/task_context.cc',
    'src/task_context_params.cc',
    'src/unicodetext.cc',
    'src/utils.cc',
    'src/workspace.cc',
    'src/script_span/fixunicodevalue.cc',
    'src/script_span/generated_entities.cc',
    'src/script_span/generated_ulscript.cc',
    'src/script_span/getonescriptspan.cc',
    'src/script_span/offsetmap.cc',
    'src/script_span/text_processing.cc',
    'src/script_span/utf8statetable.cc',
    # These CC files have to be generated by the proto buffer compiler 'protoc'
    'src/cld_3/protos/feature_extractor.pb.cc',
    'src/cld_3/protos/sentence.pb.cc',
    'src/cld_3/protos/task_spec.pb.cc',
    # pybind11 bindings
    'src/python/gcld3.cc',
]


class CompileProtos(build_ext.build_ext):
  """Compile protocol buffers via `protoc` compiler."""

  def run(self):
    if shutil.which('protoc') is None:
      raise RuntimeError('Please install the proto buffer compiler.')

    # The C++ code expect the protos to be compiled under the following
    # directory, therefore, create it if necessary.
    compiled_protos_dir = 'src/cld_3/protos/'
    os.makedirs(compiled_protos_dir, exist_ok=True)
    command = ['protoc', f'--cpp_out={compiled_protos_dir}', '--proto_path=src']
    command.extend(PROTO_FILES)
    subprocess.run(command, check=True, cwd='./')
    build_ext.build_ext.run(self)


class PyBindIncludes(object):
  """Returns the include paths for pybind11 when needed.

    To delay the invocation of "pybind11.get_include()" until it is available
    in the environment. This lazy evaluation allows us to install it first, then
    import it later to determine the correct include paths.
  """

  def __str__(self):
    import pybind11  # pylint: disable=g-import-not-at-top
    return pybind11.get_include()


ext_modules = [
    setuptools.Extension(
        _NAME,
        sorted(SRCS),
        include_dirs=[
            PyBindIncludes(),
        ],
        libraries=['protobuf'],
        language='c++'),
]

DESCRIPTION = """CLD3 is a neural network model for language identification.
This package contains the inference code and a trained model. See
https://github.com/google/cld3 for more details.
"""

setuptools.setup(
    author='Rami Al-Rfou',
    author_email='rmyeid@google.com',
    cmdclass={
        'build_ext': CompileProtos,
    },
    ext_modules=ext_modules,
    description='CLD3 is a neural network model for language identification.',
    long_description=DESCRIPTION,
    name=_NAME,
    setup_requires=REQUIREMENTS,
    url='https://github.com/google/cld3',
    version=__version__,
    zip_safe=False,
)
