# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
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
"""Wraps the base_plugin.TBContext to stores additional data shared across API
handlers for the HParams plugin backend."""


import collections
import os


from tensorboard.plugins.hparams import api_pb2
from tensorboard.plugins.hparams import metadata
from google.protobuf import json_format
from tensorboard.plugins.scalar import metadata as scalar_metadata


class Context:
    """Wraps the base_plugin.TBContext to stores additional data shared across
    API handlers for the HParams plugin backend.

    Before adding fields to this class, carefully consider whether the
    field truelly needs to be accessible to all API handlers or if it
    can be passed separately to the handler constructor. We want to
    avoid this class becoming a magic container of variables that have
    no better place. See http://wiki.c2.com/?MagicContainer
    """

    def __init__(self, tb_context, max_domain_discrete_len=10):
        """Instantiates a context.

        Args:
          tb_context: base_plugin.TBContext. The "base" context we extend.
          max_domain_discrete_len: int. Only used when computing the experiment
            from the session runs. The maximum number of disticnt values a string
            hyperparameter can have for us to populate its 'domain_discrete' field.
            Typically, only tests should specify a value for this parameter.
        """
        self._tb_context = tb_context
        self._max_domain_discrete_len = max_domain_discrete_len

    def experiment_from_metadata(
        self, ctx, experiment_id, hparams_run_to_tag_to_content
    ):
        """Returns the experiment protobuffer defining the experiment.

        Accepts a dict containing the plugin contents for all summary tags
        associated with the hparams plugin, as an optimization for callers
        who already have this information available, so that this function
        can minimize its calls to the underlying `DataProvider`.

        This method first attempts to find a metadata.EXPERIMENT_TAG tag and
        retrieve the associated protobuffer. If no such tag is found, the method
        will attempt to build a minimal experiment protobuffer by scanning for
        all metadata.SESSION_START_INFO_TAG tags (to compute the hparam_infos
        field of the experiment) and for all scalar tags (to compute the
        metric_infos field of the experiment).

        Returns:
          The experiment protobuffer. If no tags are found from which an experiment
          protobuffer can be built (possibly, because the event data has not been
          completely loaded yet), returns an entirely empty experiment.
        """
        experiment = self._find_experiment_tag(hparams_run_to_tag_to_content)
        if experiment:
            return experiment
        return self._compute_experiment_from_runs(
            ctx, experiment_id, hparams_run_to_tag_to_content
        )

    @property
    def tb_context(self):
        return self._tb_context

    def _convert_plugin_metadata(self, data_provider_output):
        return {
            run: {
                tag: time_series.plugin_content
                for (tag, time_series) in tag_to_time_series.items()
            }
            for (run, tag_to_time_series) in data_provider_output.items()
        }

    def hparams_metadata(self, ctx, experiment_id, run_tag_filter=None):
        """Reads summary metadata for all hparams time series.

        Args:
          experiment_id: String, from `plugin_util.experiment_id`.
          run_tag_filter: Optional `data.provider.RunTagFilter`, with
            the semantics as in `list_tensors`.

        Returns:
          A dict `d` such that `d[run][tag]` is a `bytes` value with the
          summary metadata content for the keyed time series.
        """
        return self._convert_plugin_metadata(
            self._tb_context.data_provider.list_tensors(
                ctx,
                experiment_id=experiment_id,
                plugin_name=metadata.PLUGIN_NAME,
                run_tag_filter=run_tag_filter,
            )
        )

    def scalars_metadata(self, ctx, experiment_id):
        """Reads summary metadata for all scalar time series.

        Args:
          experiment_id: String, from `plugin_util.experiment_id`.

        Returns:
          A dict `d` such that `d[run][tag]` is a `bytes` value with the
          summary metadata content for the keyed time series.
        """
        return self._convert_plugin_metadata(
            self._tb_context.data_provider.list_scalars(
                ctx,
                experiment_id=experiment_id,
                plugin_name=scalar_metadata.PLUGIN_NAME,
            )
        )

    def read_last_scalars(self, ctx, experiment_id, run_tag_filter):
        """Reads the most recent values from scalar time series.

        Args:
          experiment_id: String.
          run_tag_filter: Required `data.provider.RunTagFilter`, with
            the semantics as in `read_scalars`.

        Returns:
          A dict `d` such that `d[run][tag]` is a `provider.ScalarDatum`
          value, with keys only for runs and tags that actually had
          data, which may be a subset of what was requested.
        """
        data_provider_output = self._tb_context.data_provider.read_scalars(
            ctx,
            experiment_id=experiment_id,
            plugin_name=scalar_metadata.PLUGIN_NAME,
            run_tag_filter=run_tag_filter,
            # TODO(#3436): We assume that downsampling always includes
            # the most recent datum, which holds for all implementations
            # of interest but is not yet required by the interface.
            downsample=1,
        )
        return {
            run: {tag: data[-1] for (tag, data) in tag_to_data.items()}
            for (run, tag_to_data) in data_provider_output.items()
        }

    def _find_experiment_tag(self, hparams_run_to_tag_to_content):
        """Finds the experiment associcated with the metadata.EXPERIMENT_TAG
        tag.

        Returns:
          The experiment or None if no such experiment is found.
        """
        # We expect only one run to have an `EXPERIMENT_TAG`; look
        # through all of them and arbitrarily pick the first one.
        for tags in hparams_run_to_tag_to_content.values():
            maybe_content = tags.get(metadata.EXPERIMENT_TAG)
            if maybe_content is not None:
                return metadata.parse_experiment_plugin_data(maybe_content)
        return None

    def _compute_experiment_from_runs(
        self, ctx, experiment_id, hparams_run_to_tag_to_content
    ):
        """Computes a minimal Experiment protocol buffer by scanning the runs.

        Returns an empty Experiment if there are no hparam infos logged.
        """
        hparam_infos = self._compute_hparam_infos(hparams_run_to_tag_to_content)
        if hparam_infos:
            metric_infos = self._compute_metric_infos(
                ctx, experiment_id, hparams_run_to_tag_to_content
            )
        else:
            metric_infos = []
        return api_pb2.Experiment(
            hparam_infos=hparam_infos, metric_infos=metric_infos
        )

    def _compute_hparam_infos(self, hparams_run_to_tag_to_content):
        """Computes a list of api_pb2.HParamInfo from the current run, tag
        info.

        Finds all the SessionStartInfo messages and collects the hparams values
        appearing in each one. For each hparam attempts to deduce a type that fits
        all its values. Finally, sets the 'domain' of the resulting HParamInfo
        to be discrete if the type is string and the number of distinct values is
        small enough.

        Returns:
          A list of api_pb2.HParamInfo messages.
        """
        # Construct a dict mapping an hparam name to its list of values.
        hparams = collections.defaultdict(list)
        for tag_to_content in hparams_run_to_tag_to_content.values():
            if metadata.SESSION_START_INFO_TAG not in tag_to_content:
                continue
            start_info = metadata.parse_session_start_info_plugin_data(
                tag_to_content[metadata.SESSION_START_INFO_TAG]
            )
            for (name, value) in start_info.hparams.items():
                hparams[name].append(value)

        # Try to construct an HParamInfo for each hparam from its name and list
        # of values.
        result = []
        for (name, values) in hparams.items():
            hparam_info = self._compute_hparam_info_from_values(name, values)
            if hparam_info is not None:
                result.append(hparam_info)
        return result

    def _compute_hparam_info_from_values(self, name, values):
        """Builds an HParamInfo message from the hparam name and list of
        values.

        Args:
          name: string. The hparam name.
          values: list of google.protobuf.Value messages. The list of values for the
            hparam.

        Returns:
          An api_pb2.HParamInfo message.
        """
        # Figure out the type from the values.
        # Ignore values whose type is not listed in api_pb2.DataType
        # If all values have the same type, then that is the type used.
        # Otherwise, the returned type is DATA_TYPE_STRING.
        result = api_pb2.HParamInfo(name=name, type=api_pb2.DATA_TYPE_UNSET)
        distinct_values = set(
            _protobuf_value_to_string(v)
            for v in values
            if _protobuf_value_type(v)
        )
        for v in values:
            v_type = _protobuf_value_type(v)
            if not v_type:
                continue
            if result.type == api_pb2.DATA_TYPE_UNSET:
                result.type = v_type
            elif result.type != v_type:
                result.type = api_pb2.DATA_TYPE_STRING
            if result.type == api_pb2.DATA_TYPE_STRING:
                # A string result.type does not change, so we can exit the loop.
                break

        # If we couldn't figure out a type, then we can't compute the hparam_info.
        if result.type == api_pb2.DATA_TYPE_UNSET:
            return None

        # If the result is a string, set the domain to be the distinct values if
        # there aren't too many of them.
        if (
            result.type == api_pb2.DATA_TYPE_STRING
            and len(distinct_values) <= self._max_domain_discrete_len
        ):
            result.domain_discrete.extend(distinct_values)

        return result

    def _compute_metric_infos(
        self, ctx, experiment_id, hparams_run_to_tag_to_content
    ):
        return (
            api_pb2.MetricInfo(name=api_pb2.MetricName(group=group, tag=tag))
            for tag, group in self._compute_metric_names(
                ctx, experiment_id, hparams_run_to_tag_to_content
            )
        )

    def _compute_metric_names(
        self, ctx, experiment_id, hparams_run_to_tag_to_content
    ):
        """Computes the list of metric names from all the scalar (run, tag)
        pairs.

        The return value is a list of (tag, group) pairs representing the metric
        names. The list is sorted in Python tuple-order (lexicographical).

        For example, if the scalar (run, tag) pairs are:
        ("exp/session1", "loss")
        ("exp/session2", "loss")
        ("exp/session2/eval", "loss")
        ("exp/session2/validation", "accuracy")
        ("exp/no-session", "loss_2"),
        and the runs corresponding to sessions are "exp/session1", "exp/session2",
        this method will return [("loss", ""), ("loss", "/eval"), ("accuracy",
        "/validation")]

        More precisely, each scalar (run, tag) pair is converted to a (tag, group)
        metric name, where group is the suffix of run formed by removing the
        longest prefix which is a session run. If no session run is a prefix of
        'run', the pair is skipped.

        Returns:
          A python list containing pairs. Each pair is a (tag, group) pair
          representing a metric name used in some session.
        """
        session_runs = set(
            run
            for run, tags in hparams_run_to_tag_to_content.items()
            if metadata.SESSION_START_INFO_TAG in tags
        )
        metric_names_set = set()
        scalars_run_to_tag_to_content = self.scalars_metadata(
            ctx, experiment_id
        )
        for run, tags in scalars_run_to_tag_to_content.items():
            session = _find_longest_parent_path(session_runs, run)
            if not session:
                continue
            group = os.path.relpath(run, session)
            # relpath() returns "." for the 'session' directory, we use an empty
            # string.
            if group == ".":
                group = ""
            metric_names_set.update((tag, group) for tag in tags)
        metric_names_list = list(metric_names_set)
        # Sort metrics for determinism.
        metric_names_list.sort()
        return metric_names_list


def _find_longest_parent_path(path_set, path):
    """Finds the longest "parent-path" of 'path' in 'path_set'.

    This function takes and returns "path-like" strings which are strings
    made of strings separated by os.sep. No file access is performed here, so
    these strings need not correspond to actual files in some file-system..
    This function returns the longest ancestor path
    For example, for path_set=["/foo/bar", "/foo", "/bar/foo"] and
    path="/foo/bar/sub_dir", returns "/foo/bar".

    Args:
      path_set: set of path-like strings -- e.g. a list of strings separated by
        os.sep. No actual disk-access is performed here, so these need not
        correspond to actual files.
      path: a path-like string.

    Returns:
      The element in path_set which is the longest parent directory of 'path'.
    """
    # This could likely be more efficiently implemented with a trie
    # data-structure, but we don't want to add an extra dependency for that.
    while path not in path_set:
        if not path:
            return None
        path = os.path.dirname(path)
    return path


def _protobuf_value_type(value):
    """Returns the type of the google.protobuf.Value message as an
    api.DataType.

    Returns None if the type of 'value' is not one of the types supported in
    api_pb2.DataType.

    Args:
      value: google.protobuf.Value message.
    """
    if value.HasField("number_value"):
        return api_pb2.DATA_TYPE_FLOAT64
    if value.HasField("string_value"):
        return api_pb2.DATA_TYPE_STRING
    if value.HasField("bool_value"):
        return api_pb2.DATA_TYPE_BOOL
    return None


def _protobuf_value_to_string(value):
    """Returns a string representation of given google.protobuf.Value message.

    Args:
      value: google.protobuf.Value message. Assumed to be of type 'number',
        'string' or 'bool'.
    """
    value_in_json = json_format.MessageToJson(value)
    if value.HasField("string_value"):
        # Remove the quotations.
        return value_in_json[1:-1]
    return value_in_json
