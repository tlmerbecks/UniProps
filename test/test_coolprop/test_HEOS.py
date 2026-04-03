from pyProp import State
from pyProp.utilities.constants import variables, _default_pairs, pairs
from pyProp.utilities.conversions import pair_to_vars
from pyProp.settings import DO_WORKAROUND

import CoolProp as cp


def test_HEOS_calc_modes():
    DO_WORKAROUND = False

    fld = cp.AbstractState("HEOS", "Water")
    fld.update(cp.PT_INPUTS, 101325, 350)

    vals = {
        variables.Dmolar: fld.rhomolar(),
        variables.Hmolar: fld.hmolar(),
        variables.P: fld.p(),
        variables.Qmolar: 0.5,
        variables.Smolar: fld.smolar(),
        variables.T: fld.T(),
        variables.Umolar: fld.umolar()
    }

    unsupported_pairs = (  # CoolProp does not yet support these calculation pairs
        pairs.HmolarT,
        pairs.HmolarQmolar,
        pairs.HmolarUmolar,
        pairs.QmolarSmolar,  # supposedly supported for Q=0 and Q=1, but does not seem so...
        pairs.QmolarUmolar,
        pairs.SmolarUmolar,
        pairs.TUmolar
        )

    state = State(fld)

    for pair in _default_pairs:

        var1, var2 = pair_to_vars(pair)
        val1, val2 = vals[var1], vals[var2]

        try:
            print(pair, val1, val2)
            state.update(pair, val1, val2)
        except:
            assert pair in unsupported_pairs

            continue

        

