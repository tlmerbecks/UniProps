from UniProps import State
from UniProps.utilities.constants import variables, _default_pairs, pairs
from UniProps.utilities.conversions import pair_to_vars
from UniProps import settings

import CoolProp as cp
import numpy as np


def test_HEOS_calc_modes():
    settings.DO_WORKAROUND = False

    fld_PT = cp.AbstractState("HEOS", "Water")
    fld_PT.update(cp.PT_INPUTS, 101325, 350)

    fld_PQ = cp.AbstractState("HEOS", "Water")
    fld_PQ.update(cp.PQ_INPUTS, 101325, 1)


    vals_PT = {
        variables.Dmolar: fld_PT.rhomolar(),
        variables.Hmolar: fld_PT.hmolar(),
        variables.P: fld_PT.p(),
        variables.Smolar: fld_PT.smolar(),
        variables.T: fld_PT.T(),
        variables.Umolar: fld_PT.umolar()
    }

    vals_PQ = {
        variables.Dmolar: fld_PQ.rhomolar(),
        variables.Hmolar: fld_PQ.hmolar(),
        variables.P: fld_PQ.p(),
        variables.Qmolar: fld_PQ.Q(),
        variables.Smolar: fld_PQ.smolar(),
        variables.T: fld_PQ.T(),
        variables.Umolar: fld_PQ.umolar()
    }

    unsupported_pairs = (  # CoolProp does not yet support these calculation pairs
        pairs.HmolarT,
        pairs.HmolarQmolar,  # supposedly supported for Q=1, but does not seem so...
        pairs.HmolarUmolar,
        pairs.QmolarSmolar,  # supposedly supported for Q=0 and Q=1
        pairs.QmolarUmolar,
        pairs.SmolarUmolar,
        pairs.TUmolar
        )
    
    for pair in _default_pairs:

        # for some reason these are particularly dangerous in pytest and cause 
        # weird crashes... standalone it "works" ok though... strange
        if pair in [pairs.QmolarSmolar,]: 
            continue 
        
        fld = cp.AbstractState("HEOS", "Water")
        state = State.from_instance(fld)

        var1, var2 = pair_to_vars(pair)

        if variables.Qmolar in [var1, var2]:
            val1, val2 = vals_PQ[var1], vals_PQ[var2]
        else:
            val1, val2 = vals_PT[var1], vals_PT[var2]

        try:
            state.update(pair, val1, val2)
        except:
            assert pair in unsupported_pairs
            continue

