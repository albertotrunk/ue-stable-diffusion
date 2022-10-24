"""
Copyright (C) 2020-2021 Jiri Borovec <...>
"""
import inspect
from functools import partial, wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from warnings import warn

#: Default template warning message fot redirecting callable
TEMPLATE_WARNING_CALLABLE = (
    "The `%(source_name)s` was deprecated since v%(deprecated_in)s in favor of `%(target_path)s`."
    " It will be removed in v%(remove_in)s."
)
#: Default template warning message for chnaging argument mapping
TEMPLATE_WARNING_ARGUMENTS = (
    "The `%(source_name)s` uses deprecated arguments: %(argument_map)s."
    " They were deprecated since v%(deprecated_in)s and will be removed in v%(remove_in)s."
)
#: Tempalte for mapping from old to new examples
TEMPLATE_ARGUMENT_MAPPING = "`%(old_arg)s` -> `%(new_arg)s`"
#: Default template warning message for no target func/method
TEMPLATE_WARNING_NO_TARGET = (
    "The `%(source_name)s` was deprecated since v%(deprecated_in)s."
    " It will be removed in v%(remove_in)s."
)

deprecation_warning = partial(warn, category=DeprecationWarning)


def get_func_arguments_types_defaults(func: Callable) -> List[Tuple[str, Tuple, Any]]:
    """
    Parse function arguments, types and default values

    Args:
        func: a function to be xeamined

    Returns:
        sequence of details for each position/keyward argument

    Example:
        >>> get_func_arguments_types_defaults(get_func_arguments_types_defaults)
        [('func', typing.Callable, <class 'inspect._empty'>)]

    """
    func_default_params = inspect.signature(func).parameters
    func_arg_type_val = []
    for arg in func_default_params:
        arg_type = func_default_params[arg].annotation
        arg_default = func_default_params[arg].default
        func_arg_type_val.append((arg, arg_type, arg_default))
    return func_arg_type_val


def _update_kwargs_with_args(func: Callable, fn_args: tuple, fn_kwargs: dict) -> dict:
    """ Update in case any args passed move them to kwargs and add defaults

    Args:
        func: particular function
        fn_args: function position arguments
        fn_kwargs: function keyword arguments

    Returns:
        extended dictionary with all args as keyword arguments

    """
    if not fn_args:
        return fn_kwargs
    func_arg_type_val = get_func_arguments_types_defaults(func)
    # parse only the argument names
    arg_names = [arg[0] for arg in func_arg_type_val]
    # convert args to kwargs
    fn_kwargs.update(dict(zip(arg_names, fn_args)))
    return fn_kwargs


def _update_kwargs_with_defaults(func: Callable, fn_kwargs: dict) -> dict:
    """ Update in case any args passed move them to kwargs and add defaults

    Args:
        func: particular function
        fn_kwargs: function keyword arguments

    Returns:
        extended dictionary with all args as keyword arguments

    """
    func_arg_type_val = get_func_arguments_types_defaults(func)
    # fill by source defaults
    fn_defaults = {arg[0]: arg[2] for arg in func_arg_type_val if arg[2] != inspect._empty}  # type: ignore
    fn_kwargs = dict(list(fn_defaults.items()) + list(fn_kwargs.items()))
    return fn_kwargs


def _raise_warn(
    stream: Callable,
    source: Callable,
    template_mgs: str,
    **extras: str,
) -> None:
    """Raise deprecation warning with in given stream ...

    Args:
        stream: a function which takes message as the only position argument
        source: function/methods which is wrapped
        template_mgs: python formatted string message which has build-ins arguments
        extras: string arguments used in the template message
    """
    source_name = source.__qualname__.split('.')[-2] if source.__name__ == "__init__" else source.__name__
    source_path = f'{source.__module__}.{source_name}'
    msg_args = dict(
        source_name=source_name,
        source_path=source_path,
        **extras,
    )
    stream(template_mgs % msg_args)


def _raise_warn_callable(
    stream: Callable,
    source: Callable,
    target: Union[None, bool, Callable],
    deprecated_in: str,
    remove_in: str,
    template_mgs: Optional[str] = None,
) -> None:
    """
    Raise deprecation warning with in given stream, redirecting callables

    Args:
        stream: a function which takes message as the only position argument
        source: function/methods which is wrapped
        target: function/methods which is mapping target
        deprecated_in: set version when source is deprecated
        remove_in: set version when source will be removed
        template_mgs: python formatted string message which has build-ins arguments:

            - ``source_name`` just the functions name such as "my_source_func"
            - ``source_path`` pythonic path to the function such as "my_package.with_module.my_source_func"
            - ``target_name`` just the functions name such as "my_target_func"
            - ``target_path`` pythonic path to the function such as "any_package.with_module.my_target_func"
            - ``deprecated_in`` version passed to wrapper
            - ``remove_in`` version passed to wrapper

    """
    if callable(target):
        target_name = target.__name__
        target_path = f'{target.__module__}.{target_name}'
        template_mgs = template_mgs or TEMPLATE_WARNING_CALLABLE
    else:
        target_name, target_path = "", ""
        template_mgs = template_mgs or TEMPLATE_WARNING_NO_TARGET
    _raise_warn(
        stream,
        source,
        template_mgs,
        deprecated_in=deprecated_in,
        remove_in=remove_in,
        target_name=target_name,
        target_path=target_path
    )


def _raise_warn_arguments(
    stream: Callable,
    source: Callable,
    arguments: Dict[str, str],
    deprecated_in: str,
    remove_in: str,
    template_mgs: Optional[str] = None,
) -> None:
    """
    Raise deprecation warning with in given stream, note about arguments

    Args:
        stream: a function which takes message as the only position argument
        source: function/methods which is wrapped
        arguments: mapping from deprecated to new arguments
        deprecated_in: set version when source is deprecated
        remove_in: set version when source will be removed
        template_mgs: python formatted string message which has build-ins arguments:

            - ``source_name`` just the functions name such as "my_source_func"
            - ``source_path`` pythonic path to the function such as "my_package.with_module.my_source_func"
            - ``argument_map`` mapping from deprecated to new argument "old_arg -> new_arg"
            - ``deprecated_in`` version passed to wrapper
            - ``remove_in`` version passed to wrapper

    """
    args_map = ', '.join([TEMPLATE_ARGUMENT_MAPPING % dict(old_arg=a, new_arg=b) for a, b in arguments.items()])
    template_mgs = template_mgs or TEMPLATE_WARNING_ARGUMENTS
    _raise_warn(stream, source, template_mgs, deprecated_in=deprecated_in, remove_in=remove_in, argument_map=args_map)


def deprecated(
    target: Union[bool, None, Callable],
    deprecated_in: str = "",
    remove_in: str = "",
    stream: Optional[Callable] = deprecation_warning,
    num_warns: int = 1,
    template_mgs: Optional[str] = None,
    args_mapping: Optional[Dict[str, str]] = None,
    args_extra: Optional[Dict[str, Any]] = None,
    skip_if: Union[bool, Callable] = False,
) -> Callable:
    """
    Decorate a function or class ``__init__`` with warning message
     and pass all arguments directly to the target class/method.

    Args:
        target: Function or method to forward the call. If set ``None``, no forwarding is applied and only warn.
        deprecated_in: Define version when the wrapped function is deprecated.
        remove_in: Define version when the wrapped function will be removed.
        stream: Set stream for printing warning messages, by default is deprecation warning.
            Setting ``None``, no warning is shown to user.
        num_warns: Custom define number or warning raised. Negative value (-1) means no limit.
        template_mgs: python formatted string message which has build-ins arguments:
            ``source_name``, ``source_path``, ``target_name``, ``target_path``, ``deprecated_in``, ``remove_in``
            Example of a custom message is::

                "v%(deprecated_in)s: `%(source_name)s` was deprecated in favor of `%(target_path)s`."

        args_mapping: Custom argument mapping argument between source and target and options to suppress some,
            for example ``{'my_arg': 'their_arg`}`` passes "my_arg" from source as "their_arg" in target
            or ``{'my_arg': None}`` ignores the "my_arg" from source function.
        args_extra: Custom filling extra argument in target function, mostly if they are required
            or your needed default is different from target one, for example ``{'their_arg': 42}``
        skip_if: Conditional skip for this wrapper, e.g. in case of versions

    Returns:
        wrapped function pointing to the target implementation with source arguments

    Raises:
        TypeError: if there are some argument in source function which are missing in target function

    """

    def packing(source: Callable) -> Callable:

        @wraps(source)
        def wrapped_fn(*args: Any, **kwargs: Any) -> Any:
            # check if user requested a skip
            shall_skip = skip_if() if callable(skip_if) else bool(skip_if)
            if not isinstance(shall_skip, bool):
                raise TypeError("User function `shall_skip` shall return bool, but got: %r" % type(shall_skip))
            if shall_skip:
                return source(*args, **kwargs)

            nb_called = getattr(wrapped_fn, '_called', 0)
            setattr(wrapped_fn, "_called", nb_called + 1)
            # convert args to kwargs
            kwargs = _update_kwargs_with_args(source, args, kwargs)

            reason_callable = target is None or callable(target)
            reason_argument = {}
            if args_mapping and target:
                reason_argument = {a: b for a, b in args_mapping.items() if a in kwargs}
            # short cycle with no reason for redirect
            if not (reason_callable or reason_argument):
                # todo: eventually warn that there is no reason to use wrapper, e.g. mapping args does not exist
                return source(**kwargs)

            # warning per argument
            if reason_argument:
                arg_warns = [getattr(wrapped_fn, f'_warned_{arg}', 0) for arg in reason_argument]
                nb_warned = min(arg_warns)
            else:
                nb_warned = getattr(wrapped_fn, '_warned', 0)

            # warn user only N times in lifetime or infinitely...
            if stream and (num_warns < 0 or nb_warned < num_warns):
                if reason_callable:
                    _raise_warn_callable(stream, source, target, deprecated_in, remove_in, template_mgs)
                    setattr(wrapped_fn, "_warned", nb_warned + 1)
                elif reason_argument:
                    _raise_warn_arguments(stream, source, reason_argument, deprecated_in, remove_in, template_mgs)
                    attrib_names = [f'_warned_{arg}' for arg in reason_argument]
                    for n in attrib_names:
                        setattr(wrapped_fn, n, getattr(wrapped_fn, n, 0) + 1)

            if reason_callable:
                kwargs = _update_kwargs_with_defaults(source, kwargs)
            if args_mapping and target:  # covers target as True and callable
                # filter args which shall be skipped
                args_skip = [arg for arg in args_mapping if not args_mapping[arg]]
                # Look-Up-table mapping
                kwargs = {args_mapping.get(arg, arg): val for arg, val in kwargs.items() if arg not in args_skip}

            if args_extra and target:  # covers target as True and callable
                # update target argument by extra arguments
                kwargs.update(args_extra)

            if not callable(target):
                return source(**kwargs)

            target_is_class = inspect.isclass(target)
            target_func = target.__init__ if target_is_class else target  # type: ignore
            target_args = [arg[0] for arg in get_func_arguments_types_defaults(target_func)]

            # get full args & name of varkw
            target_full_arg_spec = inspect.getfullargspec(target_func)
            varkw = target_full_arg_spec.varkw

            missed = [arg for arg in kwargs if arg not in target_args]
            if missed and varkw is None:
                # if kwargs in target_args, skip it.
                raise TypeError("Failed mapping, arguments missing in target source: %s" % missed)
            # all args were already moved to kwargs
            return target_func(**kwargs)

        return wrapped_fn

    return packing
