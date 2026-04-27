from .constants import pairs

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..UniProps_state import BaseState
    from .constants import properties


def res_p_T(p: float, 
            state: "BaseState", 
            T: float, 
            prop: "properties", 
            y: float, 
            kwargs: dict):
    """
    Calculate residual for pressure p, given a temperature T
    """
    state._PT(p, T, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res


def res_T_p(T:float, 
            state: "BaseState", 
            p: float, 
            prop: "properties", 
            y: float, 
            kwargs: dict):
    """
    Calculate residual for temperature T, given a pressure p
    """

    return res_p_T(p, state, T, prop, y, kwargs)


def res_Q_p(Q: float, 
            state: "BaseState", 
            p: float, 
            prop: "properties", 
            y: float, 
            kwargs: dict):
    """
    Calculate residual for quality Q, given a pressure p
    """
    state._PQmolar(p, Q, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res

def res_Q_T(Q: float, 
            state: "BaseState", 
            T: float, 
            prop: "properties", 
            y: float, 
            kwargs: dict):
    """
    Calculate residual for quality Q, given a pressure p
    """

    state._QmolarT(Q, T, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res

def res_T_Q(Q: float, 
            state: "BaseState", 
            T: float, 
            prop: "properties", 
            y: float, 
            kwargs: dict):
    """
    Calculate residual for temperature T, given a quality Q
    """

    state._QmolarT(Q, T, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res

