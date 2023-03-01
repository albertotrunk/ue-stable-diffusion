# Copyright The PyTorch Lightning team.
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
import functools
import inspect
from abc import ABC, abstractmethod
from contextlib import contextmanager
from copy import deepcopy
from typing import Any, Callable, Dict, Generator, List, Optional, Sequence, Tuple, Union

import torch
from torch import Tensor
from torch.nn import Module

from torchmetrics.utilities import apply_to_collection, rank_zero_warn
from torchmetrics.utilities.data import (
    _flatten,
    _squeeze_if_scalar,
    dim_zero_cat,
    dim_zero_max,
    dim_zero_mean,
    dim_zero_min,
    dim_zero_sum,
)
from torchmetrics.utilities.distributed import gather_all_tensors
from torchmetrics.utilities.exceptions import TorchMetricsUserError


def jit_distributed_available() -> bool:
    return torch.distributed.is_available() and torch.distributed.is_initialized()


class Metric(Module, ABC):
    """Base class for all metrics present in the Metrics API.

    Implements ``add_state()``, ``forward()``, ``reset()`` and a few other things to
    handle distributed synchronization and per-step metric computation.

    Override ``update()`` and ``compute()`` functions to implement your own metric. Use
    ``add_state()`` to register metric state variables which keep track of state on each
    call of ``update()`` and are synchronized across processes when ``compute()`` is called.

    Note:
        Metric state variables can either be :class:`~torch.Tensor` or an empty list which can we used
        to store :class:`~torch.Tensor`.

    Note:
        Different metrics only override ``update()`` and not ``forward()``. A call to ``update()``
        is valid, but it won't return the metric value at the current step. A call to ``forward()``
        automatically calls ``update()`` and also returns the metric value at the current step.

    Args:
        kwargs: additional keyword arguments, see :ref:`Metric kwargs` for more info.

            - compute_on_cpu: If metric state should be stored on CPU during computations. Only works
                for list states.
            - dist_sync_on_step: If metric state should synchronize on ``forward()``. Default is ``False``
            - process_group: The process group on which the synchronization is called. Default is the world.
            - dist_sync_fn: function that performs the allgather option on the metric state. Default is an
                custom implementation that calls ``torch.distributed.all_gather`` internally.
            - distributed_available_fn: function that checks if the distributed backend is available.
                Defaults to a check of ``torch.distributed.is_available()`` and ``torch.distributed.is_initialized()``.
            - sync_on_compute: If metric state should synchronize when ``compute`` is called. Default is ``True``-
    """

    __jit_ignored_attributes__ = ["device"]
    __jit_unused_properties__ = ["is_differentiable"]
    is_differentiable: Optional[bool] = None
    higher_is_better: Optional[bool] = None
    full_state_update: Optional[bool] = None

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__()

        # see (https://github.com/pytorch/pytorch/blob/3e6bb5233f9ca2c5aa55d9cda22a7ee85439aa6e/
        # torch/nn/modules/module.py#L227)
        torch._C._log_api_usage_once(f"torchmetrics.metric.{self.__class__.__name__}")

        self._device = torch.device("cpu")

        self.compute_on_cpu = kwargs.pop("compute_on_cpu", False)
        if not isinstance(self.compute_on_cpu, bool):
            raise ValueError(
                f"Expected keyword argument `compute_on_cpu` to be an `bool` but got {self.compute_on_cpu}"
            )

        self.dist_sync_on_step = kwargs.pop("dist_sync_on_step", False)
        if not isinstance(self.dist_sync_on_step, bool):
            raise ValueError(
                f"Expected keyword argument `dist_sync_on_step` to be an `bool` but got {self.dist_sync_on_step}"
            )

        self.process_group = kwargs.pop("process_group", None)

        self.dist_sync_fn = kwargs.pop("dist_sync_fn", None)
        if self.dist_sync_fn is not None and not callable(self.dist_sync_fn):
            raise ValueError(
                f"Expected keyword argument `dist_sync_fn` to be an callable function but got {self.dist_sync_fn}"
            )

        self.distributed_available_fn = kwargs.pop("distributed_available_fn", jit_distributed_available)

        self.sync_on_compute = kwargs.pop("sync_on_compute", True)
        if not isinstance(self.sync_on_compute, bool):
            raise ValueError(
                f"Expected keyword argument `sync_on_compute` to be a `bool` but got {self.sync_on_compute}"
            )

        # initialize
        self._update_signature = inspect.signature(self.update)
        self.update: Callable = self._wrap_update(self.update)  # type: ignore
        self.compute: Callable = self._wrap_compute(self.compute)  # type: ignore
        self._computed = None
        self._forward_cache = None
        self._update_count = 0
        self._to_sync = self.sync_on_compute
        self._should_unsync = True
        self._enable_grad = False

        # initialize state
        self._defaults: Dict[str, Union[List, Tensor]] = {}
        self._persistent: Dict[str, bool] = {}
        self._reductions: Dict[str, Union[str, Callable[..., Any], None]] = {}

        # state management
        self._is_synced = False
        self._cache: Optional[Dict[str, Union[List[Tensor], Tensor]]] = None

    @property
    def _update_called(self) -> bool:
        # Needed for lightning integration
        return self._update_count > 0

    def add_state(
        self,
        name: str,
        default: Union[list, Tensor],
        dist_reduce_fx: Optional[Union[str, Callable]] = None,
        persistent: bool = False,
    ) -> None:
        """Adds metric state variable. Only used by subclasses.

        Args:
            name: The name of the state variable. The variable will then be accessible at ``self.name``.
            default: Default value of the state; can either be a :class:`~torch.Tensor` or an empty list.
                The state will be reset to this value when ``self.reset()`` is called.
            dist_reduce_fx (Optional): Function to reduce state across multiple processes in distributed mode.
                If value is ``"sum"``, ``"mean"``, ``"cat"``, ``"min"`` or ``"max"`` we will use ``torch.sum``,
                ``torch.mean``, ``torch.cat``, ``torch.min`` and ``torch.max``` respectively, each with argument
                ``dim=0``. Note that the ``"cat"`` reduction only makes sense if the state is a list, and not
                a tensor. The user can also pass a custom function in this parameter.
            persistent (Optional): whether the state will be saved as part of the modules ``state_dict``.
                Default is ``False``.

        Note:
            Setting ``dist_reduce_fx`` to None will return the metric state synchronized across different processes.
            However, there won't be any reduction function applied to the synchronized metric state.

            The metric states would be synced as follows

            - If the metric state is :class:`~torch.Tensor`, the synced value will be a stacked :class:`~torch.Tensor`
              across the process dimension if the metric state was a :class:`~torch.Tensor`. The original
              :class:`~torch.Tensor` metric state retains dimension and hence the synchronized output will be of shape
              ``(num_process, ...)``.

            - If the metric state is a ``list``, the synced value will be a ``list`` containing the
              combined elements from all processes.

        Note:
            When passing a custom function to ``dist_reduce_fx``, expect the synchronized metric state to follow
            the format discussed in the above note.

        Raises:
            ValueError:
                If ``default`` is not a ``tensor`` or an ``empty list``.
            ValueError:
                If ``dist_reduce_fx`` is not callable or one of ``"mean"``, ``"sum"``, ``"cat"``, ``None``.
        """
        if not isinstance(default, (Tensor, list)) or (isinstance(default, list) and default):
            raise ValueError("state variable must be a tensor or any empty list (where you can append tensors)")

        if dist_reduce_fx == "sum":
            dist_reduce_fx = dim_zero_sum
        elif dist_reduce_fx == "mean":
            dist_reduce_fx = dim_zero_mean
        elif dist_reduce_fx == "max":
            dist_reduce_fx = dim_zero_max
        elif dist_reduce_fx == "min":
            dist_reduce_fx = dim_zero_min
        elif dist_reduce_fx == "cat":
            dist_reduce_fx = dim_zero_cat
        elif dist_reduce_fx is not None and not callable(dist_reduce_fx):
            raise ValueError("`dist_reduce_fx` must be callable or one of ['mean', 'sum', 'cat', None]")

        if isinstance(default, Tensor):
            default = default.contiguous()

        setattr(self, name, default)

        self._defaults[name] = deepcopy(default)
        self._persistent[name] = persistent
        self._reductions[name] = dist_reduce_fx

    @torch.jit.unused
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        """``forward`` serves the dual purpose of both computing the metric on the current batch of inputs but also
        add the batch statistics to the overall accumululating metric state.

        Input arguments are the exact same as corresponding ``update`` method. The returned output is the exact same as
        the output of ``compute``.
        """
        # check if states are already synced
        if self._is_synced:
            raise TorchMetricsUserError(
                "The Metric shouldn't be synced when performing ``forward``. "
                "HINT: Did you forget to call ``unsync`` ?."
            )

        if self.full_state_update or self.full_state_update is None or self.dist_sync_on_step:
            self._forward_cache = self._forward_full_state_update(*args, **kwargs)
        else:
            self._forward_cache = self._forward_reduce_state_update(*args, **kwargs)

        return self._forward_cache

    def _forward_full_state_update(self, *args: Any, **kwargs: Any) -> Any:
        """forward computation using two calls to `update` to calculate the metric value on the current batch and
        accumulate global state.

        Doing this secures that metrics that need access to the full metric state during `update` works as expected.
        """
        # global accumulation
        self.update(*args, **kwargs)
        _update_count = self._update_count

        self._to_sync = self.dist_sync_on_step
        # skip restore cache operation from compute as cache is stored below.
        self._should_unsync = False
        # skip computing on cpu for the batch
        _temp_compute_on_cpu = self.compute_on_cpu
        self.compute_on_cpu = False

        # save context before switch
        cache = {attr: getattr(self, attr) for attr in self._defaults}

        # call reset, update, compute, on single batch
        self._enable_grad = True  # allow grads for batch computation
        self.reset()
        self.update(*args, **kwargs)
        batch_val = self.compute()

        # restore context
        for attr, val in cache.items():
            setattr(self, attr, val)
        self._update_count = _update_count

        # restore context
        self._is_synced = False
        self._should_unsync = True
        self._to_sync = self.sync_on_compute
        self._computed = None
        self._enable_grad = False
        self.compute_on_cpu = _temp_compute_on_cpu
        if self.compute_on_cpu:
            self._move_list_states_to_cpu()

        return batch_val

    def _forward_reduce_state_update(self, *args: Any, **kwargs: Any) -> Any:
        """forward computation using single call to `update` to calculate the metric value on the current batch and
        accumulate global state.

        This can be done when the global metric state is a sinple reduction of batch states.
        """
        # store global state and reset to default
        global_state = {attr: getattr(self, attr) for attr in self._defaults.keys()}
        _update_count = self._update_count
        self.reset()

        # local syncronization settings
        self._to_sync = self.dist_sync_on_step
        self._should_unsync = False
        _temp_compute_on_cpu = self.compute_on_cpu
        self.compute_on_cpu = False
        self._enable_grad = True  # allow grads for batch computation

        # calculate batch state and compute batch value
        self.update(*args, **kwargs)
        batch_val = self.compute()

        # reduce batch and global state
        self._update_count = _update_count + 1
        with torch.no_grad():
            self._reduce_states(global_state)

        # restore context
        self._is_synced = False
        self._should_unsync = True
        self._to_sync = self.sync_on_compute
        self._computed = None
        self._enable_grad = False
        self.compute_on_cpu = _temp_compute_on_cpu
        if self.compute_on_cpu:
            self._move_list_states_to_cpu()

        return batch_val

    def _reduce_states(self, incoming_state: Dict[str, Any]) -> None:
        """Adds an incoming metric state to the current state of the metric.

        Args:
            incoming_state: a dict containing a metric state similar metric itself
        """
        for attr in self._defaults.keys():
            local_state = getattr(self, attr)
            global_state = incoming_state[attr]
            reduce_fn = self._reductions[attr]
            if reduce_fn == dim_zero_sum:
                reduced = global_state + local_state
            elif reduce_fn == dim_zero_mean:
                reduced = ((self._update_count - 1) * global_state + local_state).float() / self._update_count
            elif reduce_fn == dim_zero_max:
                reduced = torch.max(global_state, local_state)
            elif reduce_fn == dim_zero_min:
                reduced = torch.min(global_state, local_state)
            elif reduce_fn == dim_zero_cat:
                reduced = global_state + local_state
            elif reduce_fn is None and isinstance(global_state, Tensor):
                reduced = torch.stack([global_state, local_state])
            elif reduce_fn is None and isinstance(global_state, list):
                reduced = _flatten([global_state, local_state])
            else:
                reduced = reduce_fn(torch.stack([global_state, local_state]))  # type: ignore

            setattr(self, attr, reduced)

    def _sync_dist(self, dist_sync_fn: Callable = gather_all_tensors, process_group: Optional[Any] = None) -> None:
        input_dict = {attr: getattr(self, attr) for attr in self._reductions}

        for attr, reduction_fn in self._reductions.items():
            # pre-concatenate metric states that are lists to reduce number of all_gather operations
            if reduction_fn == dim_zero_cat and isinstance(input_dict[attr], list) and len(input_dict[attr]) > 1:
                input_dict[attr] = [dim_zero_cat(input_dict[attr])]

        output_dict = apply_to_collection(
            input_dict,
            Tensor,
            dist_sync_fn,
            group=process_group or self.process_group,
        )

        for attr, reduction_fn in self._reductions.items():
            # pre-processing ops (stack or flatten for inputs)

            if isinstance(output_dict[attr], list) and len(output_dict[attr]) == 0:
                setattr(self, attr, [])
                continue

            if isinstance(output_dict[attr][0], Tensor):
                output_dict[attr] = torch.stack(output_dict[attr])
            elif isinstance(output_dict[attr][0], list):
                output_dict[attr] = _flatten(output_dict[attr])

            if not (callable(reduction_fn) or reduction_fn is None):
                raise TypeError("reduction_fn must be callable or None")
            reduced = reduction_fn(output_dict[attr]) if reduction_fn is not None else output_dict[attr]
            setattr(self, attr, reduced)

    def _wrap_update(self, update: Callable) -> Callable:
        @functools.wraps(update)
        def wrapped_func(*args: Any, **kwargs: Any) -> None:
            self._computed = None
            self._update_count += 1
            with torch.set_grad_enabled(self._enable_grad):
                try:
                    update(*args, **kwargs)
                except RuntimeError as err:
                    if "Expected all tensors to be on" in str(err):
                        raise RuntimeError(
                            "Encountered different devices in metric calculation (see stacktrace for details)."
                            " This could be due to the metric class not being on the same device as input."
                            f" Instead of `metric={self.__class__.__name__}(...)` try to do"
                            f" `metric={self.__class__.__name__}(...).to(device)` where"
                            " device corresponds to the device of the input."
                        ) from err
                    raise err

            if self.compute_on_cpu:
                self._move_list_states_to_cpu()

        return wrapped_func

    def _move_list_states_to_cpu(self) -> None:
        """Move list states to cpu to save GPU memory."""
        for key in self._defaults.keys():
            current_val = getattr(self, key)
            if isinstance(current_val, Sequence):
                setattr(self, key, [cur_v.to("cpu") for cur_v in current_val])

    def sync(
        self,
        dist_sync_fn: Optional[Callable] = None,
        process_group: Optional[Any] = None,
        should_sync: bool = True,
        distributed_available: Optional[Callable] = None,
    ) -> None:
        """Sync function for manually controlling when metrics states should be synced across processes.

        Args:
            dist_sync_fn: Function to be used to perform states synchronization
            process_group:
                Specify the process group on which synchronization is called.
                default: `None` (which selects the entire world)
            should_sync: Whether to apply to state synchronization. This will have an impact
                only when running in a distributed setting.
            distributed_available: Function to determine if we are running inside a distributed setting
        """
        if self._is_synced and should_sync:
            raise TorchMetricsUserError("The Metric has already been synced.")

        if distributed_available is None and self.distributed_available_fn is not None:
            distributed_available = self.distributed_available_fn

        is_distributed = distributed_available() if callable(distributed_available) else None

        if not should_sync or not is_distributed:
            return

        if dist_sync_fn is None:
            dist_sync_fn = gather_all_tensors

        # cache prior to syncing
        self._cache = {attr: getattr(self, attr) for attr in self._defaults}

        # sync
        self._sync_dist(dist_sync_fn, process_group=process_group)
        self._is_synced = True

    def unsync(self, should_unsync: bool = True) -> None:
        """Unsync function for manually controlling when metrics states should be reverted back to their local
        states.

        Args:
            should_unsync: Whether to perform unsync
        """
        if not should_unsync:
            return

        if not self._is_synced:
            raise TorchMetricsUserError("The Metric has already been un-synced.")

        if self._cache is None:
            raise TorchMetricsUserError("The internal cache should exist to unsync the Metric.")

        # if we synced, restore to cache so that we can continue to accumulate un-synced state
        for attr, val in self._cache.items():
            setattr(self, attr, val)
        self._is_synced = False
        self._cache = None

    @contextmanager
    def sync_context(
        self,
        dist_sync_fn: Optional[Callable] = None,
        process_group: Optional[Any] = None,
        should_sync: bool = True,
        should_unsync: bool = True,
        distributed_available: Optional[Callable] = None,
    ) -> Generator:
        """Context manager to synchronize the states between processes when running in a distributed setting and
        restore the local cache states after yielding.

        Args:
            dist_sync_fn: Function to be used to perform states synchronization
            process_group:
                Specify the process group on which synchronization is called.
                default: `None` (which selects the entire world)
            should_sync: Whether to apply to state synchronization. This will have an impact
                only when running in a distributed setting.
            should_unsync: Whether to restore the cache state so that the metrics can
                continue to be accumulated.
            distributed_available: Function to determine if we are running inside a distributed setting
        """
        self.sync(
            dist_sync_fn=dist_sync_fn,
            process_group=process_group,
            should_sync=should_sync,
            distributed_available=distributed_available,
        )

        yield

        self.unsync(should_unsync=self._is_synced and should_unsync)

    def _wrap_compute(self, compute: Callable) -> Callable:
        @functools.wraps(compute)
        def wrapped_func(*args: Any, **kwargs: Any) -> Any:
            if self._update_count == 0:
                rank_zero_warn(
                    f"The ``compute`` method of metric {self.__class__.__name__}"
                    " was called before the ``update`` method which may lead to errors,"
                    " as metric states have not yet been updated.",
                    UserWarning,
                )

            # return cached value
            if self._computed is not None:
                return self._computed

            # compute relies on the sync context manager to gather the states across processes and apply reduction
            # if synchronization happened, the current rank accumulated states will be restored to keep
            # accumulation going if ``should_unsync=True``,
            with self.sync_context(
                dist_sync_fn=self.dist_sync_fn,
                should_sync=self._to_sync,
                should_unsync=self._should_unsync,
            ):
                value = compute(*args, **kwargs)
                self._computed = _squeeze_if_scalar(value)

            return self._computed

        return wrapped_func

    @abstractmethod
    def update(self, *_: Any, **__: Any) -> None:
        """Override this method to update the state variables of your metric class."""

    @abstractmethod
    def compute(self) -> Any:
        """Override this method to compute the final metric value from state variables synchronized across the
        distributed backend."""

    def reset(self) -> None:
        """This method automatically resets the metric state variables to their default value."""
        self._update_count = 0
        self._forward_cache = None
        self._computed = None

        for attr, default in self._defaults.items():
            current_val = getattr(self, attr)
            if isinstance(default, Tensor):
                setattr(self, attr, default.detach().clone().to(current_val.device))
            else:
                setattr(self, attr, [])

        # reset internal states
        self._cache = None
        self._is_synced = False

    def clone(self) -> "Metric":
        """Make a copy of the metric."""
        return deepcopy(self)

    def __getstate__(self) -> Dict[str, Any]:
        # ignore update and compute functions for pickling
        return {k: v for k, v in self.__dict__.items() if k not in ["update", "compute", "_update_signature"]}

    def __setstate__(self, state: Dict[str, Any]) -> None:
        # manually restore update and compute functions for pickling
        self.__dict__.update(state)
        self._update_signature = inspect.signature(self.update)
        self.update: Callable = self._wrap_update(self.update)  # type: ignore
        self.compute: Callable = self._wrap_compute(self.compute)  # type: ignore

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ("higher_is_better", "is_differentiable", "full_state_update"):
            raise RuntimeError(f"Can't change const `{name}`.")
        super().__setattr__(name, value)

    @property
    def device(self) -> "torch.device":
        """Return the device of the metric."""
        return self._device

    def type(self, dst_type: Union[str, torch.dtype]) -> "Metric":
        """Method override default and prevent dtype casting.

        Please use `metric.set_dtype(dtype)` instead.
        """
        return self

    def float(self) -> "Metric":
        """Method override default and prevent dtype casting.

        Please use `metric.set_dtype(dtype)` instead.
        """
        return self

    def double(self) -> "Metric":
        """Method override default and prevent dtype casting.

        Please use `metric.set_dtype(dtype)` instead.
        """
        return self

    def half(self) -> "Metric":
        """Method override default and prevent dtype casting.

        Please use `metric.set_dtype(dtype)` instead.
        """
        return self

    def set_dtype(self, dst_type: Union[str, torch.dtype]) -> "Metric":
        """Special version of `type` for transferring all metric states to specific dtype
        Arguments:
            dst_type (type or string): the desired type
        """
        return super().type(dst_type)

    def _apply(self, fn: Callable) -> Module:
        """Overwrite _apply function such that we can also move metric states to the correct device when `.to`,
        `.cuda`, etc methods are called."""
        this = super()._apply(fn)
        # Also apply fn to metric states and defaults
        for key, value in this._defaults.items():
            if isinstance(value, Tensor):
                this._defaults[key] = fn(value)
            elif isinstance(value, Sequence):
                this._defaults[key] = [fn(v) for v in value]

            current_val = getattr(this, key)
            if isinstance(current_val, Tensor):
                setattr(this, key, fn(current_val))
            elif isinstance(current_val, Sequence):
                setattr(this, key, [fn(cur_v) for cur_v in current_val])
            else:
                raise TypeError(
                    "Expected metric state to be either a Tensor" f"or a list of Tensor, but encountered {current_val}"
                )

        # make sure to update the device attribute
        # if the dummy tensor moves device by fn function we should also update the attribute
        self._device = fn(torch.zeros(1, device=self.device)).device

        # Additional apply to forward cache and computed attributes (may be nested)
        if this._computed is not None:
            this._computed = apply_to_collection(this._computed, Tensor, fn)
        if this._forward_cache is not None:
            this._forward_cache = apply_to_collection(this._forward_cache, Tensor, fn)

        return this

    def persistent(self, mode: bool = False) -> None:
        """Method for post-init to change if metric states should be saved to its state_dict."""
        for key in self._persistent:
            self._persistent[key] = mode

    def state_dict(
        self,
        destination: Dict[str, Any] = None,
        prefix: str = "",
        keep_vars: bool = False,
    ) -> Optional[Dict[str, Any]]:
        destination = super().state_dict(destination=destination, prefix=prefix, keep_vars=keep_vars)
        # Register metric states to be part of the state_dict
        for key in self._defaults:
            if not self._persistent[key]:
                continue
            current_val = getattr(self, key)
            if not keep_vars:
                if isinstance(current_val, Tensor):
                    current_val = current_val.detach()
                elif isinstance(current_val, list):
                    current_val = [cur_v.detach() if isinstance(cur_v, Tensor) else cur_v for cur_v in current_val]
            destination[prefix + key] = deepcopy(current_val)  # type: ignore
        return destination

    def _load_from_state_dict(
        self,
        state_dict: dict,
        prefix: str,
        local_metadata: dict,
        strict: bool,
        missing_keys: List[str],
        unexpected_keys: List[str],
        error_msgs: List[str],
    ) -> None:
        """Loads metric states from state_dict."""

        for key in self._defaults:
            name = prefix + key
            if name in state_dict:
                setattr(self, key, state_dict.pop(name))
        super()._load_from_state_dict(
            state_dict, prefix, local_metadata, True, missing_keys, unexpected_keys, error_msgs
        )

    def _filter_kwargs(self, **kwargs: Any) -> Dict[str, Any]:
        """filter kwargs such that they match the update signature of the metric."""

        # filter all parameters based on update signature except those of
        # type VAR_POSITIONAL (*args) and VAR_KEYWORD (**kwargs)
        _params = (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        _sign_params = self._update_signature.parameters
        filtered_kwargs = {
            k: v for k, v in kwargs.items() if (k in _sign_params.keys() and _sign_params[k].kind not in _params)
        }

        exists_var_keyword = any(v.kind == inspect.Parameter.VAR_KEYWORD for v in _sign_params.values())
        # if no kwargs filtered, return all kwargs as default
        if not filtered_kwargs and not exists_var_keyword:
            # no kwargs in update signature -> don't return any kwargs
            filtered_kwargs = {}
        elif exists_var_keyword:
            # kwargs found in update signature -> return all kwargs to be sure to not omit any.
            # filtering logic is likely implemented within the update call.
            filtered_kwargs = kwargs
        return filtered_kwargs

    def __hash__(self) -> int:
        # we need to add the id here, since PyTorch requires a module hash to be unique.
        # Internally, PyTorch nn.Module relies on that for children discovery
        # (see https://github.com/pytorch/pytorch/blob/v1.9.0/torch/nn/modules/module.py#L1544)
        # For metrics that include tensors it is not a problem,
        # since their hash is unique based on the memory location but we cannot rely on that for every metric.
        hash_vals = [self.__class__.__name__, id(self)]

        for key in self._defaults:
            val = getattr(self, key)
            # Special case: allow list values, so long
            # as their elements are hashable
            if hasattr(val, "__iter__") and not isinstance(val, Tensor):
                hash_vals.extend(val)
            else:
                hash_vals.append(val)

        return hash(tuple(hash_vals))

    def __add__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.add, self, other)

    def __and__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.bitwise_and, self, other)

    # Fixme: this shall return bool instead of Metric
    def __eq__(self, other: "Metric") -> "Metric":  # type: ignore
        return CompositionalMetric(torch.eq, self, other)

    def __floordiv__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.floor_divide, self, other)

    def __ge__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.ge, self, other)

    def __gt__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.gt, self, other)

    def __le__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.le, self, other)

    def __lt__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.lt, self, other)

    def __matmul__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.matmul, self, other)

    def __mod__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.fmod, self, other)

    def __mul__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.mul, self, other)

    # Fixme: this shall return bool instead of Metric
    def __ne__(self, other: "Metric") -> "Metric":  # type: ignore
        return CompositionalMetric(torch.ne, self, other)

    def __or__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.bitwise_or, self, other)

    def __pow__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.pow, self, other)

    def __radd__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.add, other, self)

    def __rand__(self, other: "Metric") -> "Metric":
        # swap them since bitwise_and only supports that way and it's commutative
        return CompositionalMetric(torch.bitwise_and, self, other)

    def __rfloordiv__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.floor_divide, other, self)

    def __rmatmul__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.matmul, other, self)

    def __rmod__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.fmod, other, self)

    def __rmul__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.mul, other, self)

    def __ror__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.bitwise_or, other, self)

    def __rpow__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.pow, other, self)

    def __rsub__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.sub, other, self)

    def __rtruediv__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.true_divide, other, self)

    def __rxor__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.bitwise_xor, other, self)

    def __sub__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.sub, self, other)

    def __truediv__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.true_divide, self, other)

    def __xor__(self, other: "Metric") -> "Metric":
        return CompositionalMetric(torch.bitwise_xor, self, other)

    def __abs__(self) -> "Metric":
        return CompositionalMetric(torch.abs, self, None)

    def __inv__(self) -> "Metric":
        return CompositionalMetric(torch.bitwise_not, self, None)

    def __invert__(self) -> "Metric":
        return self.__inv__()

    def __neg__(self) -> "Metric":
        return CompositionalMetric(_neg, self, None)

    def __pos__(self) -> "Metric":
        return CompositionalMetric(torch.abs, self, None)

    def __getitem__(self, idx: int) -> "Metric":
        return CompositionalMetric(lambda x: x[idx], self, None)

    def __getnewargs__(self) -> Tuple:
        return (Metric.__str__(self),)

    def __iter__(self):
        raise NotImplementedError("Metrics does not support iteration.")


def _neg(x: Tensor) -> Tensor:
    return -torch.abs(x)


class CompositionalMetric(Metric):
    """Composition of two metrics with a specific operator which will be executed upon metrics compute."""

    def __init__(
        self,
        operator: Callable,
        metric_a: Union[Metric, int, float, Tensor],
        metric_b: Union[Metric, int, float, Tensor, None],
    ) -> None:
        """
        Args:
            operator: the operator taking in one (if metric_b is None)
                or two arguments. Will be applied to outputs of metric_a.compute()
                and (optionally if metric_b is not None) metric_b.compute()
            metric_a: first metric whose compute() result is the first argument of operator
            metric_b: second metric whose compute() result is the second argument of operator.
                For operators taking in only one input, this should be None
        """
        super().__init__()

        self.op = operator

        if isinstance(metric_a, Tensor):
            self.register_buffer("metric_a", metric_a)
        else:
            self.metric_a = metric_a

        if isinstance(metric_b, Tensor):
            self.register_buffer("metric_b", metric_b)
        else:
            self.metric_b = metric_b

    def _sync_dist(self, dist_sync_fn: Optional[Callable] = None, process_group: Optional[Any] = None) -> None:
        # No syncing required here. syncing will be done in metric_a and metric_b
        pass

    def update(self, *args: Any, **kwargs: Any) -> None:
        if isinstance(self.metric_a, Metric):
            self.metric_a.update(*args, **self.metric_a._filter_kwargs(**kwargs))

        if isinstance(self.metric_b, Metric):
            self.metric_b.update(*args, **self.metric_b._filter_kwargs(**kwargs))

    def compute(self) -> Any:
        # also some parsing for kwargs?
        if isinstance(self.metric_a, Metric):
            val_a = self.metric_a.compute()
        else:
            val_a = self.metric_a

        if isinstance(self.metric_b, Metric):
            val_b = self.metric_b.compute()
        else:
            val_b = self.metric_b

        if val_b is None:
            return self.op(val_a)

        return self.op(val_a, val_b)

    @torch.jit.unused
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        val_a = (
            self.metric_a(*args, **self.metric_a._filter_kwargs(**kwargs))
            if isinstance(self.metric_a, Metric)
            else self.metric_a
        )
        val_b = (
            self.metric_b(*args, **self.metric_b._filter_kwargs(**kwargs))
            if isinstance(self.metric_b, Metric)
            else self.metric_b
        )

        if val_a is None:
            return None

        if val_b is None:
            if isinstance(self.metric_b, Metric):
                return None

            # Unary op
            return self.op(val_a)

        # Binary op
        return self.op(val_a, val_b)

    def reset(self) -> None:
        if isinstance(self.metric_a, Metric):
            self.metric_a.reset()

        if isinstance(self.metric_b, Metric):
            self.metric_b.reset()

    def persistent(self, mode: bool = False) -> None:
        if isinstance(self.metric_a, Metric):
            self.metric_a.persistent(mode=mode)
        if isinstance(self.metric_b, Metric):
            self.metric_b.persistent(mode=mode)

    def __repr__(self) -> str:
        _op_metrics = f"(\n  {self.op.__name__}(\n    {repr(self.metric_a)},\n    {repr(self.metric_b)}\n  )\n)"
        repr_str = self.__class__.__name__ + _op_metrics

        return repr_str

    def _wrap_compute(self, compute: Callable) -> Callable:
        return compute
