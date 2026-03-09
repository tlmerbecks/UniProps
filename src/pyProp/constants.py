from enum import Enum
from itertools import combinations

PMIN = 1e-9
PMAX = 1e9
TMIN = 0
TMAX = None


class variables(Enum):
    P = "P"
    Dmass = "Dmass"
    Dmolar = "Dmolar"
    Hmass = "Hmass"
    Hmolar = "Hmolar"
    Qmass = "Qmass"
    Qmolar = "Qmolar"
    Smass = "Smass"
    Smolar = "Smolar"
    T = "T"
    Umass = "Umass"
    Umolar = "Umolar"

class pairs(Enum):
    DmassHmass = "DmassHmass"
    DmassHmolar = "DmassHmolar"
    DmassP = "DmassP"
    DmassQmass = "DmassQmass"
    DmassQmolar = "DmassQmolar"
    DmassSmass = "DmassSmass"
    DmassSmolar = "DmassSmolar"
    DmassT = "DmassT"
    DmassUmass = "DmassUmass"
    DmassUmolar = "DmassUmolar"
    DmolarHmass = "DmolarHmass"
    DmolarHmolar = "DmolarHmolar"
    DmolarP = "DmolarP"
    DmolarQmass = "DmolarQmass"
    DmolarQmolar = "DmolarQmolar"
    DmolarSmass = "DmolarSmass"
    DmolarSmolar = "DmolarSmolar"
    DmolarT = "DmolarT"
    DmolarUmass = "DmolarUmass"
    DmolarUmolar = "DmolarUmolar"
    HmassDmass = "HmassDmass"
    HmassDmolar = "HmassDmolar"
    HmassP = "HmassP"
    HmassQmass = "HmassQmass"
    HmassQmolar = "HmassQmolar"
    HmassSmass = "HmassSmass"
    HmassSmolar = "HmassSmolar"
    HmassT = "HmassT"
    HmassUmass = "HmassUmass"
    HmassUmolar = "HmassUmolar"
    HmolarDmass = "HmolarDmass"
    HmolarDmolar = "HmolarDmolar"
    HmolarP = "HmolarP"
    HmolarQmass = "HmolarQmass"
    HmolarQmolar = "HmolarQmolar"
    HmolarSmass = "HmolarSmass"
    HmolarSmolar = "HmolarSmolar"
    HmolarT = "HmolarT"
    HmolarUmass = "HmolarUmass"
    HmolarUmolar = "HmolarUmolar"
    PDmass = "PDmass"
    PDmolar = "PDmolar"
    PHmass = "PHmass"
    PHmolar = "PHmolar"
    PQmass = "PQmass"
    PQmolar = "PQmolar"
    PSmass = "PSmass"
    PSmolar = "PSmolar"
    PT = "PT"
    PUmass = "PUmass"
    PUmolar = "PUmolar"
    QmassDmass = "QmassDmass"
    QmassDmolar = "QmassDmolar"
    QmassHmass = "QmassHmass"
    QmassHmolar = "QmassHmolar"
    QmassP = "QmassP"
    QmassSmass = "QmassSmass"
    QmassSmolar = "QmassSmolar"
    QmassT = "QmassT"
    QmassUmass = "QmassUmass"
    QmassUmolar = "QmassUmolar"
    QmolarDmass = "QmolarDmass"
    QmolarDmolar = "QmolarDmolar"
    QmolarHmass = "QmolarHmass"
    QmolarHmolar = "QmolarHmolar"
    QmolarP = "QmolarP"
    QmolarSmass = "QmolarSmass"
    QmolarSmolar = "QmolarSmolar"
    QmolarT = "QmolarT"
    QmolarUmass = "QmolarUmass"
    QmolarUmolar = "QmolarUmolar"
    SmassDmass = "SmassDmass"
    SmassDmolar = "SmassDmolar"
    SmassHmass = "SmassHmass"
    SmassHmolar = "SmassHmolar"
    SmassP = "SmassP"
    SmassQmass = "SmassQmass"
    SmassQmolar = "SmassQmolar"
    SmassT = "SmassT"
    SmassUmass = "SmassUmass"
    SmassUmolar = "SmassUmolar"
    SmolarDmass = "SmolarDmass"
    SmolarDmolar = "SmolarDmolar"
    SmolarHmass = "SmolarHmass"
    SmolarHmolar = "SmolarHmolar"
    SmolarP = "SmolarP"
    SmolarQmass = "SmolarQmass"
    SmolarQmolar = "SmolarQmolar"
    SmolarT = "SmolarT"
    SmolarUmass = "SmolarUmass"
    SmolarUmolar = "SmolarUmolar"
    TDmass = "TDmass"
    TDmolar = "TDmolar"
    THmass = "THmass"
    THmolar = "THmolar"
    TP = "TP"
    TSmass = "TSmass"
    TSmolar = "TSmolar"
    TQmass = "TQmass"
    TQmolar = "TQmolar"
    TUmass = "TUmass"
    TUmolar = "TUmolar"
    UmassDmass = "UmassDmass"
    UmassDmolar = "UmassDmolar"
    UmassHmass = "UmassHmass"
    UmassHmolar = "UmassHmolar"
    UmassP = "UmassP"
    UmassQmass = "UmassQmass"
    UmassQmolar = "UmassQmolar"
    UmassSmass = "UmassSmass"
    UmassSmolar = "UmassSmolar"
    UmassT = "UmassT"
    UmolarDmass = "UmolarDmass"
    UmolarDmolar = "UmolarDmolar"
    UmolarHmass = "UmolarHmass"
    UmolarHmolar = "UmolarHmolar"
    UmolarP = "UmolarP"
    UmolarQmass = "UmolarQmass"
    UmolarQmolar = "UmolarQmolar"
    UmolarSmass = "UmolarSmass"
    UmolarSmolar = "UmolarSmolar"
    UmolarT = "UmolarT"

class properties(Enum):
    p = "pressure"
    T = "temperature"
    Q = "quality"
    D = "density"
    Dcrit = "critical density"
    s = "entropy"
    h = "enthalpy"
    u = "internal energy"
    v = "volume"
    pcrit = "critical pressure"
    pbubble = "bubble point pressure"
    pdew = "dew point pressure"
    Tcrit = "critical temperature"
    Tbubble = "bubble point temperature"
    Tdew = "dew point pressure"
    Mr = "molecular weight"

    Smass = "specific entropy"
    Hmass = "specific enthalpy"
    Umass = "specific internal energy"
    Dmass = "density"
    Dmass_crit = "critical density"
    Vmass = "specific volume"
    Qmass = "mass quality"

    Smolar = "molar entropy"
    Hmolar = "molar enthalpy"
    Umolar = "molar internal energy"
    Dmolar = "molar density"
    Dmolar_crit = "critical molar density"
    Vmolar = "molar volume"
    Qmolar = "molar quality"


# the default variables
_default_variables = [
    variables.P,
    variables.Dmolar,
    variables.Hmolar,
    variables.Qmolar,
    variables.Smolar,
    variables.T,
    variables.Umolar
]

# the default variable pairs
_default_pairs = [pairs(v1.value + v2.value) for (v1, v2) in list(combinations(_default_variables, 2))]

# mapping of the variables to its corresponding default variable
_var_to_default_var = {
    variables.P : variables.P,
    variables.Dmass : variables.Dmolar,
    variables.Dmolar : variables.Dmolar,
    variables.Hmass : variables.Hmolar,
    variables.Hmolar : variables.Hmolar,
    variables.Qmass : variables.Qmolar,
    variables.Qmolar : variables.Qmolar,
    variables.Smass : variables.Smolar,
    variables.Smolar : variables.Smolar,
    variables.T : variables.T,
    variables.Umass : variables.Umolar,
    variables.Umolar : variables.Umolar,
    }
def var_to_default_var(var):
    return _var_to_default_var[var]


# the conversion factors for for each variable to its default variable
_var_conv = {
    (variables.Dmass, variables.Dmolar): -1, 
    (variables.Dmolar, variables.Dmass): 1,
    (variables.Hmass, variables.Hmolar): 1,
    (variables.Hmolar, variables.Hmass): 1,
    (variables.Qmass, variables.Qmolar): None,
    (variables.Qmolar, variables.Qmass): None,
    (variables.Smass, variables.Smolar): 1,
    (variables.Smolar, variables.Smass): 1,
    (variables.Umass, variables.Umolar): 1,
    (variables.Umolar, variables.Umass): 1,
    }
def conversion(from_var, to_var):
    return _var_conv.get((from_var, to_var), None)


# mapping between the state variables and the corresponding property 
_var_to_property = {
    variables.P : properties.p,
    variables.Dmass : properties.Dmass,
    variables.Dmolar : properties.Dmolar,
    variables.Hmass : properties.Hmass,
    variables.Hmolar : properties.Hmolar,
    variables.Qmass : properties.Qmass,
    variables.Qmolar : properties.Qmolar,
    variables.Smass : properties.Smass,
    variables.Smolar : properties.Smolar,
    variables.T : properties.T,
    variables.Umass : properties.Umass,
    variables.Umolar : properties.Umolar,
}
def var_to_property(var):
    return _var_to_property[var]


# mapping between pairs and the corresponvariables
_pair_to_vars = {v1.value + v2.value: (v1, v2) for (v1, v2) in list(combinations(variables, 2)) if (v1.value+v2.value in pairs)}
_pair_to_vars.update({v2.value + v1.value: (v2, v1) for (v1, v2) in list(combinations(variables, 2)) if (v1.value+v2.value in pairs)})
_pair_to_vars = {pairs(k): v for k, v in _pair_to_vars.items()}
def pair_to_vars(pair):
    return _pair_to_vars[pair]


_vars_to_pair = {v: k for k, v in _pair_to_vars.items()}
def vars_to_pair(var1, var2):
    return _vars_to_pair[(var1, var2)]


def pair_to_default_pair(pair):
    var1, var2 = pair_to_vars(pair)

    dvar1 = var_to_default_var(var1)
    dvar2 = var_to_default_var(var2)

    dpair = vars_to_pair(dvar1, dvar2)
    if dpair not in _default_pairs:
        dpair = vars_to_pair(dvar2, dvar1)

    return dpair


def inputs_to_default_inputs(pair, vals):
    # obtain the variables and values
    var1, var2 = pair_to_vars(pair)
    val1, val2 = vals

    # obtain the corresponding default variables
    dvar1 = var_to_default_var(var1)
    dvar2 = var_to_default_var(var2)

    # obtain the conversion factors
    conv1 = conversion(var1, dvar1)
    conv2 = conversion(var2, dvar2)

    # construct the "default" pair from the default variables
    dpair = vars_to_pair(dvar1, dvar2)
    if dpair not in _default_pairs:
        # "default" pair is reversed, so swap the variables, values and conversion
        dvar1, dvar2 = dvar2, dvar1
        val1, val2 = val2, val1
        conv1, conv2 = conv2, conv1

        # update the default pair
        dpair = vars_to_pair(dvar1, dvar2)

    return dpair, {"var": dvar1, "val": val1, "conv" : conv1}, {"var": dvar2, "val": val2, "conv" : conv2}


class phases(Enum):
    l = "liquid"
    g = "gaseous"   
    tp = "two-phase"
    sl = "supercritical liquid"
    sg = "supercritical gas"
    s = "supercritical"


if __name__ == "__main__":
    print(pair_to_default_pair(pairs.PHmass))