import CoolProp as cp
import numpy as np

from .coolprop_state import CoolPropState

from UniProps.utilities.errors import PackageError

class CoolPropFactory:

    @staticmethod
    def from_instance(instance):

        if not isinstance(instance, cp.AbstractState):
            raise PackageError("state is not supported by CoolProp")

        model_type = instance.backend_name().removesuffix("Backend").removesuffix("Mixture")
        mixture = (len(instance.get_mole_fractions()) > 1)
        
        if mixture:
            model_type = model_type + "Mixture"

        try:
            state = CoolPropState(instance, model_type)
        except Exception as e:
            msg = f"The CoolProp state could not be wrappend due to the following error: \n{str(e)}"
            raise Exception(msg)
        
        return state
    
    @staticmethod
    def from_primitives(model, composition, molar=True):

        mixture = False
        if isinstance(composition, str):
            comp_string = composition
        elif isinstance(composition, dict):
            if len(composition) > 1:
                mixture = True
                comp_string = "&".join(list(composition.keys()))

                fracs = np.array(list(composition.values()))
                fracs = list(fracs/fracs.sum())

            else:
                comp_string = list(composition.keys())[0]
        
        else:
            msg = f"The composition must either be defined as a str (for pure fluids) or dictionary (for pure fluids and mixtures)"
            raise ValueError(msg)

        instance = cp.AbstractState(model, comp_string)

        if mixture:
            # set the fractions as mole-fractions for now so we can initialise the wrapper
            instance.set_mole_fractions(fracs)  # type: ignore

        state = CoolPropFactory.from_instance(instance)

        if mixture and not molar:
            mole_fracs = state._massfrac_to_molefrac(fracs)  # type: ignore
            instance.set_mole_fractions(mole_fracs)

        return state


