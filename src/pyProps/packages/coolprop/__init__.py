import CoolProp as cp

from .coolprop_state import CoolPropState
from pyProps.utilities.errors import PackageError


def CoolPropFactory(state):
    if not isinstance(state, cp.AbstractState):
        raise PackageError("state is not supported by CoolProp")

    model_type = state.backend_name().removesuffix("Backend").removesuffix("Mixture")
    mixture = (len(state.get_mole_fractions()) > 1)
    
    if mixture:
        model_type = model_type + "Mixture"

    try:
        model = CoolPropState(state, model_type)
    except Exception as e:
        msg = f"The CoolProp state could not be wrappend due to the following error: \n{str(e)}"
        raise Exception(msg)
    
    return model