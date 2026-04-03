from numpy import log10

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..pyProp_state import BaseState
    from .constants import properties



def obj_p_T(p: float, 
            state: "BaseState", 
            T: float, 
            prop: "properties", 
            y: float, 
            pcrit: float, 
            kwargs: dict):
    """
    Calculate objective for a given pressure p, given a temperature T
    """
    state._PT(p, T, **kwargs)

    diff = log10(((state.get(prop) - y) / (y + 1e-15))**2 + 1e-15)

    penal = log10(pcrit / p)

    return diff + penal


def obj_T_Q(T: float, 
            state: "BaseState", 
            Q: float, 
            prop: "properties", 
            y: float, 
            pcrit: float, 
            kwargs: dict):
    """
    Calculate objective for a given pressure p, given a temperature T
    """

    state._QmolarT(Q, T, **kwargs)

    diff = log10(((state.get(prop) - y) / (y + 1e-15))**2 + 1e-15)

    penal = log10(pcrit / state.p())

    return diff + penal