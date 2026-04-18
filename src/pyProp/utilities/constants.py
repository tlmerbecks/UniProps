from enum import Enum
from itertools import combinations


class phases(Enum):
    none = "none"
    l = "liquid"
    g = "gaseous"   
    tp = "two-phase"
    sl = "supercritical liquid"
    sg = "supercritical gas"
    s = "supercritical"

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
    
    xMr = "molecular weight of liquid phase"
    yMr = "molecular weight of vapour phase"
    Mr = "molecular weight"

    xmolar = "mole fractions of liquid phase"
    ymolar = "mole fractions of vapour phase"
    zmolar = "mole fractions of fluid"

    xmass = "mole fractions of liquid phase"
    ymass = "mole fractions of vapour phase"
    zmass = "mole fractions of fluid"

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
    variables.Dmolar,
    variables.Hmolar,
    variables.P,
    variables.Qmolar,
    variables.Smolar,
    variables.T,
    variables.Umolar
]

# the default variable pairs
# _default_pairs = [pairs(v1.value + v2.value) for (v1, v2) in list(combinations(_default_variables, 2))]
_default_pairs = [
    pairs.DmolarHmolar,
    pairs.DmolarP,
    pairs.DmolarSmolar,
    pairs.DmolarT     ,
    pairs.DmolarUmolar,
    pairs.HmolarP     ,
    pairs.HmolarQmolar,
    pairs.HmolarSmolar,
    pairs.HmolarT     ,
    pairs.HmolarUmolar,
    pairs.PQmolar     ,
    pairs.PSmolar     ,
    pairs.PT,
    pairs.PUmolar     ,
    pairs.QmolarSmolar,
    pairs.QmolarT     ,
    pairs.QmolarUmolar,
    pairs.SmolarT     ,
    pairs.SmolarUmolar,
    pairs.TUmolar 
]

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


# mapping between pairs and the corresponvariables
_pair_to_vars = {v1.value + v2.value: (v1, v2) for (v1, v2) in list(combinations(variables, 2)) if (v1.value+v2.value in pairs)}
_pair_to_vars.update({v2.value + v1.value: (v2, v1) for (v1, v2) in list(combinations(variables, 2)) if (v1.value+v2.value in pairs)})
_pair_to_vars = {pairs(k): v for k, v in _pair_to_vars.items()}


_vars_to_pair = {v: k for k, v in _pair_to_vars.items()}

