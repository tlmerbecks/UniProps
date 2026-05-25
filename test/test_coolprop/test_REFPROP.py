from UniProps import State
from UniProps.utilities.constants import variables, _default_pairs, pairs
from UniProps.utilities.conversions import pair_to_vars
from UniProps import settings

import CoolProp as cp
from contextlib import contextmanager

"""
Tests for the HEOS coolprop backend - verifying the supported vs. unsupported 
calculation modes, whether the workaround methods are working as expected.
"""

backend = "REFPROP"
fluid = "Water"

p0 = 101325  # Pa - the pressure of the reference cases
T0 = 350  # K - the temperature of the reference case
Q0 = 1  # the quality of the reference case

# I think all pairs are supported...
unsupported_pairs = (
        )

fld_PT = cp.AbstractState(backend, fluid)
fld_PT.update(cp.PT_INPUTS, p0, T0)

fld_PQ = cp.AbstractState(backend, fluid)
fld_PQ.update(cp.PQ_INPUTS, p0, Q0)

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


@contextmanager
def temporary_option():
    settings.DO_WORKAROUND = True
    try:
        yield
    finally:
        # The finally block ensures the reset happens even if an exception occurs
        settings.DO_WORKAROUND = False

def test_HEOS_unsupported_modes():
    """
    Tests whether the support for calculation modes has changed between versions. 
    I.e. modes that used be unsupported should still be unsupported.
    """
    settings.DO_WORKAROUND = False

    succeeded = 0
    for pair in unsupported_pairs:

        # for some reason these are particularly dangerous in pytest and cause 
        # weird crashes... standalone it "works" ok though... strange
        if pair in [pairs.QmolarSmolar,]: 
            continue 

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        var1, var2 = pair_to_vars(pair)

        if variables.Qmolar in [var1, var2]:
            val1, val2 = vals_PQ[var1], vals_PQ[var2]
        else:
            val1, val2 = vals_PT[var1], vals_PT[var2]

        try:
            state.update(pair, val1, val2)
        except:
            continue

        succeeded += 1

    assert succeeded == 0


def test_HEOS_calc_modes():
    """
    Tests whether the support for calculation modes has changed between versions. 
    I.e. modes that used be supported should still be supported.
    """
        
    settings.DO_WORKAROUND = False

    failed = 0
    for pair in _default_pairs:

        # for some reason these are particularly dangerous in pytest and cause 
        # weird crashes... standalone it "works" ok though... strange
        if pair in unsupported_pairs: 
            continue 
        
        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        var1, var2 = pair_to_vars(pair)

        if variables.Qmolar in [var1, var2]:
            val1, val2 = vals_PQ[var1], vals_PQ[var2]
        else:
            val1, val2 = vals_PT[var1], vals_PT[var2]

        try:
            state.update(pair, val1, val2)
        except:
            failed += 1
            continue

    assert failed == 0

