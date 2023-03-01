from typing import Dict

import torch._C as _C

TensorProtoDataType = _C._onnx.TensorProtoDataType
OperatorExportTypes = _C._onnx.OperatorExportTypes
TrainingMode = _C._onnx.TrainingMode
_CAFFE2_ATEN_FALLBACK = _C._onnx._CAFFE2_ATEN_FALLBACK

ONNX_ARCHIVE_MODEL_PROTO_NAME = "__MODEL_PROTO"

producer_name = "pytorch"
producer_version = _C._onnx.PRODUCER_VERSION


class ExportTypes:
    r"""Specifies how the ONNX model is stored."""

    PROTOBUF_FILE = "Saves model in the specified protobuf file."
    ZIP_ARCHIVE = "Saves model in the specified ZIP file (uncompressed)."
    COMPRESSED_ZIP_ARCHIVE = "Saves model in the specified ZIP file (compressed)."
    DIRECTORY = "Saves model in the specified folder."


class CheckerError(Exception):
    r"""Raised when ONNX checker detects an invalid model."""

    pass


class SymbolicContext:
    r"""Provides extra context for symbolic functions.

    Args:
        params_dict (Dict[str, _C.IValue]): Mapping from graph initializer name to IValue.
        env (Dict[_C.Value, _C.Value]): Mapping from Torch domain graph Value to ONNX domain graph Value.
        cur_node (_C.Node): Current node being converted to ONNX domain.
        onnx_block (_C.Block): Current ONNX block that converted nodes are being appended to.
    """

    def __init__(self, params_dict, env, cur_node, onnx_block):
        self.params_dict: Dict[str, _C.IValue] = params_dict
        self.env: Dict[_C.Value, _C.Value] = env
        # Current node that is being converted.
        self.cur_node: _C.Node = cur_node
        # Current onnx block that converted nodes are being appended to.
        self.onnx_block: _C.Block = onnx_block


def _export(*args, **kwargs):
    from torch.onnx import utils

    result = utils._export(*args, **kwargs)
    return result


def export(
    model,
    args,
    f,
    export_params=True,
    verbose=False,
    training=TrainingMode.EVAL,
    input_names=None,
    output_names=None,
    operator_export_type=OperatorExportTypes.ONNX,
    opset_version=None,
    do_constant_folding=True,
    dynamic_axes=None,
    keep_initializers_as_inputs=None,
    custom_opsets=None,
    export_modules_as_functions=False,
):
    r"""
    Exports a model into ONNX format. If ``model`` is not a
    :class:`torch.jit.ScriptModule` nor a :class:`torch.jit.ScriptFunction`, this runs
    ``model`` once in order to convert it to a TorchScript graph to be exported
    (the equivalent of :func:`torch.jit.trace`). Thus this has the same limited support
    for dynamic control flow as :func:`torch.jit.trace`.

    Args:
        model (torch.nn.Module, torch.jit.ScriptModule or torch.jit.ScriptFunction):
            the model to be exported.
        args (tuple or torch.Tensor):

            args can be structured either as:

            1. ONLY A TUPLE OF ARGUMENTS::

                args = (x, y, z)

            The tuple should contain model inputs such that ``model(*args)`` is a valid
            invocation of the model. Any non-Tensor arguments will be hard-coded into the
            exported model; any Tensor arguments will become inputs of the exported model,
            in the order they occur in the tuple.

            2. A TENSOR::

                args = torch.Tensor([1])

            This is equivalent to a 1-ary tuple of that Tensor.

            3. A TUPLE OF ARGUMENTS ENDING WITH A DICTIONARY OF NAMED ARGUMENTS::

                args = (x,
                        {'y': input_y,
                         'z': input_z})

            All but the last element of the tuple will be passed as non-keyword arguments,
            and named arguments will be set from the last element. If a named argument is
            not present in the dictionary, it is assigned the default value, or None if a
            default value is not provided.

            .. note::
                If a dictionary is the last element of the args tuple, it will be
                interpreted as containing named arguments. In order to pass a dict as the
                last non-keyword arg, provide an empty dict as the last element of the args
                tuple. For example, instead of::

                    torch.onnx.export(
                        model,
                        (x,
                         # WRONG: will be interpreted as named arguments
                         {y: z}),
                        "test.onnx.pb")

                Write::

                    torch.onnx.export(
                        model,
                        (x,
                         {y: z},
                         {}),
                        "test.onnx.pb")

        f: a file-like object (such that ``f.fileno()`` returns a file descriptor)
            or a string containing a file name.  A binary protocol buffer will be written
            to this file.
        export_params (bool, default True): if True, all parameters will
            be exported. Set this to False if you want to export an untrained model.
            In this case, the exported model will first take all of its parameters
            as arguments, with the ordering as specified by ``model.state_dict().values()``
        verbose (bool, default False): if True, prints a description of the
            model being exported to stdout. In addition, the final ONNX graph will include the
            field ``doc_string``` from the exported model which mentions the source code locations
            for ``model``. If True, ONNX exporter logging will be turned on.
        training (enum, default TrainingMode.EVAL):
            * ``TrainingMode.EVAL``: export the model in inference mode.
            * ``TrainingMode.PRESERVE``: export the model in inference mode if model.training is
              False and in training mode if model.training is True.
            * ``TrainingMode.TRAINING``: export the model in training mode. Disables optimizations
              which might interfere with training.
        input_names (list of str, default empty list): names to assign to the
            input nodes of the graph, in order.
        output_names (list of str, default empty list): names to assign to the
            output nodes of the graph, in order.
        operator_export_type (enum, default OperatorExportTypes.ONNX):

            * ``OperatorExportTypes.ONNX``: Export all ops as regular ONNX ops
              (in the default opset domain).
            * ``OperatorExportTypes.ONNX_FALLTHROUGH``: Try to convert all ops
              to standard ONNX ops in the default opset domain. If unable to do so
              (e.g. because support has not been added to convert a particular torch op to ONNX),
              fall back to exporting the op into a custom opset domain without conversion. Applies
              to `custom ops <https://pytorch.org/tutorials/advanced/torch_script_custom_ops.html>`_
              as well as ATen ops. For the exported model to be usable, the runtime must support
              these non-standard ops.
            * ``OperatorExportTypes.ONNX_ATEN``: All ATen ops (in the TorchScript namespace "aten")
              are exported as ATen ops (in opset domain "org.pytorch.aten").
              `ATen <https://pytorch.org/cppdocs/#aten>`_ is PyTorch's built-in tensor library, so
              this instructs the runtime to use PyTorch's implementation of these ops.

              .. warning::

                Models exported this way are probably runnable only by Caffe2.

              This may be useful if the numeric differences in implementations of operators are
              causing large differences in behavior between PyTorch and Caffe2 (which is more
              common on untrained models).

            * ``OperatorExportTypes.ONNX_ATEN_FALLBACK``: Try to export each ATen op
              (in the TorchScript namespace "aten") as a regular ONNX op. If we are unable to do so
              (e.g. because support has not been added to convert a particular torch op to ONNX),
              fall back to exporting an ATen op. See documentation on OperatorExportTypes.ONNX_ATEN for
              context.
              For example::

                graph(%0 : Float):
                  %3 : int = prim::Constant[value=0]()
                  # conversion unsupported
                  %4 : Float = aten::triu(%0, %3)
                  # conversion supported
                  %5 : Float = aten::mul(%4, %0)
                  return (%5)

              Assuming ``aten::triu`` is not supported in ONNX, this will be exported as::

                graph(%0 : Float):
                  %1 : Long() = onnx::Constant[value={0}]()
                  # not converted
                  %2 : Float = aten::ATen[operator="triu"](%0, %1)
                  # converted
                  %3 : Float = onnx::Mul(%2, %0)
                  return (%3)

              If PyTorch was built with Caffe2 (i.e. with ``BUILD_CAFFE2=1``), then
              Caffe2-specific behavior will be enabled, including special support
              for ops are produced by the modules described in
              `Quantization <https://pytorch.org/docs/stable/quantization.html>`_.

              .. warning::

                Models exported this way are probably runnable only by Caffe2.

        opset_version (int, default 13): The version of the
            `default (ai.onnx) opset <https://github.com/onnx/onnx/blob/master/docs/Operators.md>`_
            to target. Must be >= 7 and <= 16.
        do_constant_folding (bool, default True): Apply the constant-folding optimization.
            Constant-folding will replace some of the ops that have all constant inputs
            with pre-computed constant nodes.
        dynamic_axes (dict<string, dict<int, string>> or dict<string, list(int)>, default empty dict):

            By default the exported model will have the shapes of all input and output tensors
            set to exactly match those given in ``args``. To specify axes of tensors as
            dynamic (i.e. known only at run-time), set ``dynamic_axes`` to a dict with schema:

            * KEY (str): an input or output name. Each name must also be provided in ``input_names`` or
              ``output_names``.
            * VALUE (dict or list): If a dict, keys are axis indices and values are axis names. If a
              list, each element is an axis index.

            For example::

                class SumModule(torch.nn.Module):
                    def forward(self, x):
                        return torch.sum(x, dim=1)

                torch.onnx.export(SumModule(), (torch.ones(2, 2),), "onnx.pb",
                                  input_names=["x"], output_names=["sum"])

            Produces::

                input {
                  name: "x"
                  ...
                      shape {
                        dim {
                          dim_value: 2  # axis 0
                        }
                        dim {
                          dim_value: 2  # axis 1
                ...
                output {
                  name: "sum"
                  ...
                      shape {
                        dim {
                          dim_value: 2  # axis 0
                ...

            While::

                torch.onnx.export(SumModule(), (torch.ones(2, 2),), "onnx.pb",
                                  input_names=["x"], output_names=["sum"],
                                  dynamic_axes={
                                      # dict value: manually named axes
                                      "x": {0: "my_custom_axis_name"},
                                      # list value: automatic names
                                      "sum": [0],
                                  })

            Produces::

                input {
                  name: "x"
                  ...
                      shape {
                        dim {
                          dim_param: "my_custom_axis_name"  # axis 0
                        }
                        dim {
                          dim_value: 2  # axis 1
                ...
                output {
                  name: "sum"
                  ...
                      shape {
                        dim {
                          dim_param: "sum_dynamic_axes_1"  # axis 0
                ...

        keep_initializers_as_inputs (bool, default None): If True, all the
            initializers (typically corresponding to parameters) in the
            exported graph will also be added as inputs to the graph. If False,
            then initializers are not added as inputs to the graph, and only
            the non-parameter inputs are added as inputs.
            This may allow for better optimizations (e.g. constant folding) by
            backends/runtimes.

            If ``opset_version < 9``, initializers MUST be part of graph
            inputs and this argument will be ignored and the behavior will be
            equivalent to setting this argument to True.

            If None, then the behavior is chosen automatically as follows:

            * If ``operator_export_type=OperatorExportTypes.ONNX``, the behavior is equivalent
              to setting this argument to False.
            * Else, the behavior is equivalent to setting this argument to True.

        custom_opsets (dict<str, int>, default empty dict): A dict with schema:

            * KEY (str): opset domain name
            * VALUE (int): opset version

            If a custom opset is referenced by ``model`` but not mentioned in this dictionary,
            the opset version is set to 1. Only custom opset domain name and version should be
            indicated through this argument.

        export_modules_as_functions (bool or set of type of nn.Module, default False): Flag to enable
            exporting all ``nn.Module`` forward calls as local functions in ONNX. Or a set to indicate the
            particular types of modules to export as local functions in ONNX.
            This feature requires ``opset_version`` >= 15, otherwise the export will fail. This is because
            ``opset_version`` < 15 implies IR version < 8, which means no local function support.
            Module variables will be exported as function attributes. There are two categories of function
            attributes.

            1. Annotated attributes: class variables that have type annotations via
            `PEP 526-style <https://www.python.org/dev/peps/pep-0526/#class-and-instance-variable-annotations>`_
            will be exported as attributes.
            Annotated attributes are not used inside the subgraph of ONNX local function because
            they are not created by PyTorch JIT tracing, but they may be used by consumers
            to determine whether or not to replace the function with a particular fused kernel.

            2. Inferred attributes: variables that are used by operators inside the module. Attribute names
            will have prefix "inferred::". This is to differentiate from predefined attributes retrieved from
            python module annotations. Inferred attributes are used inside the subgraph of ONNX local function.

            * ``False``(default): export ``nn.Module`` forward calls as fine grained nodes.
            * ``True``: export all ``nn.Module`` forward calls as local function nodes.
            * Set of type of nn.Module: export ``nn.Module`` forward calls as local function nodes,
              only if the type of the ``nn.Module`` is found in the set.

    Raises:
      CheckerError: If the ONNX checker detects an invalid ONNX graph. Will still export the
        model to the file ``f`` even if this is raised.
    """

    from torch.onnx import utils

    return utils.export(
        model,
        args,
        f,
        export_params,
        verbose,
        training,
        input_names,
        output_names,
        operator_export_type,
        opset_version,
        do_constant_folding,
        dynamic_axes,
        keep_initializers_as_inputs,
        custom_opsets,
        export_modules_as_functions,
    )


def export_to_pretty_string(*args, **kwargs) -> str:
    r"""
    Similar to :func:`export`, but returns a text representation of the ONNX
    model. Only differences in args listed below. All other args are the same
    as :func:`export`.

    Args:
      add_node_names (bool, default True): Whether or not to set
          NodeProto.name. This makes no difference unless
          ``google_printer=True``.
      google_printer (bool, default False): If False, will return a custom,
          compact representation of the model. If True will return the
          protobuf's `Message::DebugString()`, which is more verbose.

    Returns:
      A UTF-8 str containing a human-readable representation of the ONNX model.
    """
    from torch.onnx import utils

    return utils.export_to_pretty_string(*args, **kwargs)


def _optimize_trace(graph, operator_export_type):
    from torch.onnx import utils

    return utils._optimize_graph(graph, operator_export_type)


def select_model_mode_for_export(model, mode):
    r"""
    A context manager to temporarily set the training mode of ``model``
    to ``mode``, resetting it when we exit the with-block.  A no-op if
    mode is None.

    Args:
      model: Same type and meaning as ``model`` arg to :func:`export`.
      mode: Same type and meaning as ``training`` arg to :func:`export`.
    """

    from torch.onnx import utils

    return utils.select_model_mode_for_export(model, mode)


def _run_symbolic_function(*args, **kwargs):
    from torch.onnx import utils

    return utils._run_symbolic_function(*args, **kwargs)


def _run_symbolic_method(*args, **kwargs):
    from torch.onnx import utils

    return utils._run_symbolic_method(*args, **kwargs)


def is_in_onnx_export():
    r"""
    Returns True iff :func:`export` is running in the current thread
    """

    from torch.onnx import utils

    return utils.is_in_onnx_export()


def register_custom_op_symbolic(symbolic_name, symbolic_fn, opset_version):
    r"""
    Registers ``symbolic_fn`` to handle ``symbolic_name``. See
    "Custom Operators" in the module documentation for an example usage.

    Args:
      symbolic_name (str): The name of the custom operator in "<domain>::<op>"
        format.
      symbolic_fn (Callable): A function that takes in the ONNX graph and
        the input arguments to the current operator, and returns new
        operator nodes to add to the graph.
      opset_version (int): The ONNX opset version in which to register.
    """
    from torch.onnx import utils

    utils.register_custom_op_symbolic(symbolic_name, symbolic_fn, opset_version)


def unregister_custom_op_symbolic(symbolic_name, opset_version):
    r"""
    Unregisters ``symbolic_name``. See
    "Custom Operators" in the module documentation for an example usage.

    Args:
      symbolic_name (str): The name of the custom operator in "<domain>::<op>"
        format.
      opset_version (int): The ONNX opset version in which to unregister.
    """

    from torch.onnx import utils

    utils.unregister_custom_op_symbolic(symbolic_name, opset_version)


def is_onnx_log_enabled():
    r"""
    Returns True iff ONNX logging is turned on.
    """
    return _C._jit_is_onnx_log_enabled()


def enable_log():
    r"""
    Enables ONNX logging.
    """
    _C._jit_set_onnx_log_enabled(True)


def disable_log():
    r"""
    Disables ONNX logging.
    """
    _C._jit_set_onnx_log_enabled(False)


def set_log_stream(stream_name="stdout"):
    r"""
    Set output stream for ONNX logging.

    Args:
      stream_name (str, default "stdout"): Only ``stdout`` and ``stderr`` are supported
        as `stream_name`.
    """
    _C._jit_set_onnx_log_output_stream(stream_name)


def log(*args):
    r"""
    A simple logging facility for ONNX exporter.

    Args:
      args: Arguments are converted to string, concatenated together with a newline
        character appended to the end, and flushed to output stream.
    """
    _C._jit_onnx_log(*args)
