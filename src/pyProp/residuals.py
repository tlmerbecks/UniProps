from.constants import pairs


def res_p_T(p, state, T, prop, y, kwargs):
    """
    Calculate residual for pressure p, given a temperature T
    """
    state._PT(p, T, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res


def res_T_p(T, state, p, prop, y, kwargs):
    """
    Calculate residual for temperature T, given a pressure p
    """

    return res_p_T(p, state, T, prop, y, kwargs)


def res_Q_p(Q, state, p, prop, y, kwargs):
    """
    Calculate residual for quality Q, given a pressure p
    """
    state._PQmolar(p, Q, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res

def res_Q_T(Q, state, T, prop, y, kwargs):
    """
    Calculate residual for quality Q, given a pressure p
    """

    state._QmolarT(Q, T, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res

def res_T_Q(Q, state, T, prop, y, kwargs):
    """
    Calculate residual for temperature T, given a quality Q
    """

    state._QmolarT(Q, T, **kwargs)

    res = (state.get(prop) - y) / (y + 1e-15)

    return res

