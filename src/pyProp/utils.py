from .constants import (
    _var_to_default_var,
    _var_conv,
    _var_to_property,
    _pair_to_vars,
    _vars_to_pair,
    _default_pairs,
    )

from typing import TYPE_CHECKING, Iterable, Tuple, Dict
if TYPE_CHECKING:
    from .constants import variables, properties, pairs 


def var_to_default_var(var: variables) -> variables:
    return _var_to_default_var[var]


def conversion(from_var: variables, to_var: variables) -> float | None:
    return _var_conv.get((from_var, to_var), None)


def var_to_property(var: variables) -> properties:
    return _var_to_property[var]


def pair_to_vars(pair: pairs) -> tuple[variables, variables]:
    return _pair_to_vars[pair]


def vars_to_pair(var1: variables, var2: variables) -> pairs:
    return _vars_to_pair[(var1, var2)]


def pair_to_default_pair(pair: pairs) -> pairs:
    var1, var2 = pair_to_vars(pair)

    dvar1 = var_to_default_var(var1)
    dvar2 = var_to_default_var(var2)

    dpair = vars_to_pair(dvar1, dvar2)
    if dpair not in _default_pairs:
        dpair = vars_to_pair(dvar2, dvar1)

    return dpair

# def inputs_to_default_inputs(pair: pairs, vals: Iterable[float]) -> tuple[pairs, dict[str, variables | float | None], dict[str, variables | float | None]]:
def inputs_to_default_inputs(pair: pairs, vals: Iterable[float]) -> Tuple[pairs, Dict, Dict]:
    # obtain the variables and values
    var1, var2 = pair_to_vars(pair)
    val1, val2 = vals

    # obtain the corresponding default variables
    dvar1 = var_to_default_var(var1)
    dvar2 = var_to_default_var(var2)

    # obtain the conversion factors
    conv1 = conversion(var1, dvar1)
    conv2 = conversion(var2, dvar2)

    # construct the "default" pair from the default variables
    dpair = vars_to_pair(dvar1, dvar2)
    if dpair not in _default_pairs:
        # "default" pair is reversed, so swap the variables, values and conversion
        dvar1, dvar2 = dvar2, dvar1
        val1, val2 = val2, val1
        conv1, conv2 = conv2, conv1

        # update the default pair
        dpair = vars_to_pair(dvar1, dvar2)

    return dpair, {"var": dvar1, "val": val1, "conv" : conv1}, {"var": dvar2, "val": val2, "conv" : conv2}