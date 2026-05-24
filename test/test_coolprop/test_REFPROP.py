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

unsupported_pairs = (
    # pairs.HmolarT,
    # pairs.HmolarQmolar,  # supposedly supported for Q=1, but does not seem so...
    # pairs.HmolarUmolar,
    # pairs.QmolarSmolar,  # supposedly supported for Q=0 and Q=1
    # pairs.QmolarUmolar,
    # pairs.SmolarUmolar,
    # pairs.TUmolar
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


def test_HT_workaround():

    with temporary_option():

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        try:
            state.update(pairs.HmolarT, vals_PT[variables.Hmolar], vals_PT[variables.T])
        except:
            assert False


def test_HQ_workaround():
    with temporary_option():

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        try:
            state.update(pairs.HmolarQmolar, vals_PQ[variables.Hmolar], vals_PQ[variables.Qmolar])
        except:
            assert False

def test_HU_workaround():
    with temporary_option():

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        try:
            state.update(pairs.HmolarUmolar, vals_PT[variables.Hmolar], vals_PT[variables.Umolar])
        except:
            assert False


def test_QS_workaround():
    with temporary_option():

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        try:
            state.update(pairs.HmolarSmolar, vals_PT[variables.Hmolar], vals_PT[variables.Smolar])
        except:
            assert False


def test_QU_workaround():
    with temporary_option():

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        try:
            state.update(pairs.QmolarUmolar, vals_PQ[variables.Qmolar], vals_PQ[variables.Umolar])
        except:
            assert False


def test_SU_workaround():
    with temporary_option():

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        try:
            state.update(pairs.SmolarUmolar, vals_PT[variables.Smolar], vals_PT[variables.Umolar])
        except:
            assert False


def test_TU_workaround():
    with temporary_option():

        fld = cp.AbstractState(backend, fluid)
        state = State.from_instance(fld)

        try:
            state.update(pairs.TUmolar, vals_PT[variables.T], vals_PT[variables.Umolar])
        except:
            assert False


def test_HQ_workaround_extended():

    T = 350
    Qs = [0, 0.25, 0.5, 0.75, 0.8, 0.9, 0.95, 1.0]

    with temporary_option():

        for Q in Qs:

            fld = cp.AbstractState(backend, fluid)
            state = State.from_instance(fld)

            state.update(pairs.QmolarT, Q, T)

            hmolar = state.hmolar()

            state.update(pairs.HmolarQmolar, hmolar, Q)

    