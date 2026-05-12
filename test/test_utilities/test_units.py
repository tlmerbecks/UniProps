from UniProps import State, pairs
from UniProps.utilities.units import (
    convert_to_SI,
    convert_from_SI
    )

import numpy as np

def test_density_conversion():

    val = 10

    val_SI = convert_to_SI(val, "g/m3")
    val_ = convert_from_SI(val_SI, "g/m3")
    assert np.isclose(val, val_)

def test_enthalpy_conversion():

    val = 10

    val_SI = convert_to_SI(val, "BTU/kg")
    val_ = convert_from_SI(val_SI, "BTU/kg")
    assert np.isclose(val, val_)

def test_entropy_conversion():

    val = 10

    val_SI = convert_to_SI(val, "BTU/kg/degF")
    val_ = convert_from_SI(val_SI, "BTU/kg/degF")
    assert np.isclose(val, val_)

def test_fraction_conversion():

    val = 10

    val_SI = convert_to_SI(val, "%")
    val_ = convert_from_SI(val_SI, "%")
    assert np.isclose(val, val_)

def test_pressure_conversion():

    val = 10

    val_SI = convert_to_SI(val, "psi")
    val_ = convert_from_SI(val_SI, "psi")
    assert np.isclose(val, val_)

def test_temperature_conversion():

    val = 10

    val_SI = convert_to_SI(val, "degR")
    val_ = convert_from_SI(val_SI, "degR")
    assert np.isclose(val, val_)

def test_volume_conversion():

    val = 10

    val_SI = convert_to_SI(val, "cc")
    val_ = convert_from_SI(val_SI, "cc")
    assert np.isclose(val, val_)

def test_PT_calculation():

    p0 = 101325
    T0 = 350

    p_bar = convert_from_SI(p0, "bar")
    T_degR = convert_from_SI(T0, "degR")

    SI_state = State.from_primitives("coolprop", "HEOS", "water")
    SI_state.update(pairs.PT, p0, T0)

    state = State.from_primitives("coolprop", "HEOS", "water")
    state.update(pairs.PT, p_bar, T_degR, unit1="bar", unit2="degR")

    assert np.isclose(SI_state.Dmass(), state.Dmass())

