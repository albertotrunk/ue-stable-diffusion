# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""Shared utils among inference plugins that are platform-specific."""

import csv
from glob import glob
from grpc.beta import implementations
import os
import random
from six.moves.urllib.parse import urlparse
import tensorflow as tf

from tensorboard_plugin_wit._utils import common_utils
from tensorflow.core.framework import types_pb2
from tensorboard_plugin_wit._vendor.tensorflow_serving.apis import classification_pb2
from tensorboard_plugin_wit._vendor.tensorflow_serving.apis import predict_pb2
from tensorboard_plugin_wit._vendor.tensorflow_serving.apis import prediction_service_pb2
from tensorboard_plugin_wit._vendor.tensorflow_serving.apis import regression_pb2


def filepath_to_filepath_list(file_path):
  """Returns a list of files given by a filepath.

  Args:
    file_path: A path, possibly representing a single file, or containing a
        wildcard or sharded path.

  Returns:
    A list of files represented by the provided path.
  """
  file_path = file_path.strip()
  if '*' in file_path:
    return glob(file_path)
  else:
    return [file_path]


def path_is_parent(parent_path, child_path):
  """Returns if the provided parent path is a parent of the provided child path.

  Args:
    parent_path: File path to check as parent.
    child_path: File path to check as child.

  Returns:
    True if parent_path is a parent of the child_path.
  """
  # Smooth out relative path names.
  parent_path = os.path.normpath(parent_path)
  child_path = os.path.normpath(child_path)

  # Compare the common path of the parent and child path with the common path of
  # just the parent path. Using the commonpath method on just the parent path
  # will regularise the path name in the same way as the comparison that deals
  # with both paths, removing any trailing path separator.
  return os.path.commonpath([parent_path]) == os.path.commonpath(
      [parent_path, child_path])


def throw_if_file_access_not_allowed(file_path, logdir, allowed_dir=None):
  """Throws an error if a file cannot be loaded for inference.

  Args:
    file_path: A file path.
    logdir: The path to the logdir of the TensorBoard context.
    allowed_dir: An optional path to allow loading files from, outside of
    the logdir.

  Raises:
    InvalidUserInputError: If the file is not in the logdir and is not globally
        readable.
  """
  file_paths = filepath_to_filepath_list(file_path)
  if not file_paths:
    raise common_utils.InvalidUserInputError(file_path + ' contains no files')

  for path in file_paths:
    # Check if the file is inside the logdir or allowed dir.
    if not (path_is_parent(logdir, path) or
            (allowed_dir and path_is_parent(allowed_dir, path))):
      raise common_utils.InvalidUserInputError(
          path + ' is not inside the TensorBoard logdir or '
          '--whatif-data-dir argument directory.'
      )


def example_protos_from_path(path,
                             num_examples=10,
                             start_index=0,
                             parse_examples=True,
                             sampling_odds=1,
                             example_class=tf.train.Example):
  """Returns a number of examples from the provided path.

  Args:
    path: A string path to the examples.
    num_examples: The maximum number of examples to return from the path.
    parse_examples: If true then parses the serialized proto from the path into
        proto objects. Defaults to True.
    sampling_odds: Odds of loading an example, used for sampling. When >= 1
        (the default), then all examples are loaded.
    example_class: tf.train.Example or tf.train.SequenceExample class to load.
        Defaults to tf.train.Example.

  Returns:
    A list of Example protos or serialized proto strings at the path.

  Raises:
    InvalidUserInputError: If examples cannot be procured from the path.
  """

  def append_examples_from_iterable(iterable, examples):
    for value in iterable:
      if sampling_odds >= 1 or random.random() < sampling_odds:
        examples.append(
            example_class.FromString(value) if parse_examples else value)
        if len(examples) >= num_examples:
          return

  examples = []

  if path.endswith('.csv'):
    def are_floats(values):
      for value in values:
        try:
          float(value)
        except ValueError:
          return False
      return True
    csv.register_dialect('CsvDialect', skipinitialspace=True)
    rows = csv.DictReader(open(path), dialect='CsvDialect')
    for row in rows:
      if sampling_odds < 1 and random.random() > sampling_odds:
        continue
      example = tf.train.Example()
      for col in row.keys():
          # Parse out individual values from vertical-bar-delimited lists
          values = [val.strip() for val in row[col].split('|')]
          if are_floats(values):
            example.features.feature[col].float_list.value.extend(
              [float(val) for val in values])
          else:
            example.features.feature[col].bytes_list.value.extend(
              [val.encode('utf-8') for val in values])
      examples.append(
        example if parse_examples else example.SerializeToString())
      if len(examples) >= num_examples:
        break
    return examples

  filenames = filepath_to_filepath_list(path)
  compression_types = [
      '',  # no compression (distinct from `None`!)
      'GZIP',
      'ZLIB',
  ]
  current_compression_idx = 0
  current_file_index = 0
  while (current_file_index < len(filenames) and
         current_compression_idx < len(compression_types)):
    try:
      record_iterator = tf.compat.v1.python_io.tf_record_iterator(
          path=filenames[current_file_index],
          options=tf.io.TFRecordOptions(
              compression_types[current_compression_idx]))
      append_examples_from_iterable(record_iterator, examples)
      current_file_index += 1
      if len(examples) >= num_examples:
        break
    except tf.errors.DataLossError:
      current_compression_idx += 1
    except (IOError, tf.errors.NotFoundError) as e:
      raise common_utils.InvalidUserInputError(e)

  if examples:
    return examples
  else:
    raise common_utils.InvalidUserInputError(
        'No examples found at ' + path +
        '. Valid formats are TFRecord files.')

def call_servo(examples, serving_bundle):
  """Send an RPC request to the Servomatic prediction service.

  Args:
    examples: A list of examples that matches the model spec.
    serving_bundle: A `ServingBundle` object that contains the information to
      make the serving request.

  Returns:
    A ClassificationResponse or RegressionResponse proto.
  """
  # Batch size for number of examples to send to servo in a single RPC.
  batch_size = 100000

  parsed_url = urlparse('http://' + serving_bundle.inference_address)
  channel = implementations.insecure_channel(parsed_url.hostname,
                                             parsed_url.port)
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

  def batch_call(batch_examples):
    if serving_bundle.use_predict:
      request = predict_pb2.PredictRequest()
    elif serving_bundle.model_type == 'classification':
      request = classification_pb2.ClassificationRequest()
    else:
      request = regression_pb2.RegressionRequest()
    request.model_spec.name = serving_bundle.model_name
    if serving_bundle.model_version is not None:
      request.model_spec.version.value = serving_bundle.model_version
    if serving_bundle.signature is not None:
      request.model_spec.signature_name = serving_bundle.signature

    if serving_bundle.use_predict:
      # tf.compat.v1 API used here to convert tf.example into proto. This
      # utility file is bundled in the witwidget pip package which has a dep
      # on TensorFlow.
      request.inputs[serving_bundle.predict_input_tensor].CopyFrom(
        tf.compat.v1.make_tensor_proto(
          values=[ex.SerializeToString() for ex in batch_examples],
          dtype=types_pb2.DT_STRING))
    else:
      request.input.example_list.examples.extend(batch_examples)

    if serving_bundle.use_predict:
      return common_utils.convert_predict_response(
        stub.Predict(request, 30.0), serving_bundle) # 30 secs timeout
    elif serving_bundle.model_type == 'classification':
      return stub.Classify(request, 30.0)  # 30 secs timeout
    else:
      return stub.Regress(request, 30.0)  # 30 secs timeout

  start_example = 0
  results = []
  first_loop = True
  while start_example < len(examples) or first_loop:
    first_loop = False
    end_example = start_example + batch_size
    batch_examples = examples[start_example:end_example]
    results.append(batch_call(batch_examples))
    start_example = end_example
  return combine_results(results, serving_bundle.model_type == 'classification')

def combine_results(result_protos, is_classification):
  """Combine results protos from batches into single proto."""
  for i in range(1, len(result_protos)):
    if is_classification:
      for j in range(len(result_protos[i].result.classifications)):
        result_protos[0].result.classifications.add(classes=result_protos[i].result.classifications[j].classes)
    else:
      for j in range(len(result_protos[i].result.regressions)):
        result_protos[0].result.regressions.add(value=result_protos[i].result.regressions[j].value)
  return result_protos[0]
