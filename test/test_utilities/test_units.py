from UniProps.utilities.units import (
    convert_to_SI,
    convert_from_SI
    )

import numpy as np

def test_unit_conversion():

    val = 10

    # density
    val_SI = convert_to_SI(val, "g/m3")
    val_ = convert_from_SI(val_SI, "g/m3")
    assert np.isclose(val, val_)

    # enthalpy
    val_SI = convert_to_SI(val, "BTU/kg")
    val_ = convert_from_SI(val_SI, "BTU/kg")
    assert np.isclose(val, val_)

    # entropy
    val_SI = convert_to_SI(val, "BTU/kg/degF")
    val_ = convert_from_SI(val_SI, "BTU/kg/degF")
    assert np.isclose(val, val_)

    # fraction
    val_SI = convert_to_SI(val, "%")
    val_ = convert_from_SI(val_SI, "%")
    assert np.isclose(val, val_)

    # pressure
    val_SI = convert_to_SI(val, "psi")
    val_ = convert_from_SI(val_SI, "psi")
    assert np.isclose(val, val_)

    # temperature
    val_SI = convert_to_SI(val, "degR")
    val_ = convert_from_SI(val_SI, "degR")
    assert np.isclose(val, val_)

    # volume
    val_SI = convert_to_SI(val, "cc")
    val_ = convert_from_SI(val_SI, "cc")
    assert np.isclose(val, val_)



