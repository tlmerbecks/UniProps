from .pure import HEOSCoolPropState, PRCoolPropState, SRKCoolPropState, REFPROPCoolPropState

from pyProp.errors import PackageError
import CoolProp as cp


Models = {
    'HelmholtzEOSBackend' : HEOSCoolPropState,
    "PengRobinsonBackend" : PRCoolPropState,
    "SRKBackend" : SRKCoolPropState,
    "REFPROPBackend" : REFPROPCoolPropState,
    }

def CoolPropFactory(state):
    if not isinstance(state, cp.AbstractState):
        raise PackageError("state is not supported by CoolProp")

    model_type = state.backend_name()
    pure = (len(state.get_mole_fractions()) == 1)

    try:
        model = Models[model_type](state)
    except KeyError:
        msg = f"The CoolProp model {model_type} is not yet supported"
        raise KeyError(msg)
    
    return model