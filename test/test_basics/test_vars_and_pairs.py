from pyProp.utilities.constants import (
    pairs,
    variables,
    properties
    )
from pyProp.utilities.conversions import (
    pair_to_vars,
    vars_to_pair,
    pair_to_default_pair,
    var_to_default_var,
    var_to_property,
    inputs_to_default_inputs
    )


def test_pair_to_vars():

    pair = pairs.PT

    vars = pair_to_vars(pair)
    assert vars[0] == variables.P
    assert vars[1] == variables.T

def test_vars_to_pair():

    var1 = variables.P
    var2 = variables.T

    pair = vars_to_pair(var1, var2)
    assert pair == pairs.PT

def test_pair_to_default_pair_TP():
    
    pair = pairs.TP
    dpair = pair_to_default_pair(pair)
    assert dpair == pairs.PT

def test_pair_to_default_pair_DH():
    
    pair = pairs.DmassHmass
    dpair = pair_to_default_pair(pair)
    assert dpair == pairs.DmolarHmolar

def test_var_to_default_var():

    var = variables.Dmass
    dvar = var_to_default_var(var)
    assert dvar == variables.Dmolar

def test_var_to_property():

    var = variables.P
    prop = var_to_property(var)
    assert prop == properties.p

def test_inputs_to_default_inputs_PT():

    # test TP pair
    pair = pairs.TP
    vals = (298, 101325)

    dinputs = inputs_to_default_inputs(pair, vals)
    assert dinputs[0] == pairs.PT
    
    dinputs1 = dinputs[1]
    assert dinputs1["var"] == variables.P
    assert dinputs1["val"] == 101325
    assert dinputs1["conv"] == None

    dinputs2 = dinputs[2]
    assert dinputs2["var"] == variables.T
    assert dinputs2["val"] == 298
    assert dinputs2["conv"] == None

def test_inputs_to_default_inputs_SH():

    # test SmolarHmass pair
    pair  = pairs.SmolarHmass
    vals = ("s", "h")
    
    dinputs = inputs_to_default_inputs(pair, vals)
    assert dinputs[0] == pairs.HmolarSmolar

    dinputs1 = dinputs[1]
    assert dinputs1["var"] == variables.Hmolar
    assert dinputs1["val"] == "h"
    assert dinputs1["conv"] == 1

    dinputs2 = dinputs[2]
    assert dinputs2["var"] == variables.Smolar
    assert dinputs2["val"] == "s"
    assert dinputs2["conv"] == None  # no conversion is needed as Smolar is already the default var





