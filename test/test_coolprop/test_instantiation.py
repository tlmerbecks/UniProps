from UniProps import State, pairs

import CoolProp as cp
import numpy as np

def test_instantiation_from_instance():

    fld = cp.AbstractState("HEOS", "Water")

    state = State.from_instance(fld)

def test_instantiation_from_primitives_pure():

    package = "coolprop"
    model = "HEOS"
    composition = "water"

    p0 = 101325
    T0 = 350

    fld = cp.AbstractState(model, composition)
    fld.update(cp.PT_INPUTS, p0, T0)
    
    state = State.from_primitives(package, model, composition)
    state.update(pairs.PT, p0, T0)

    assert np.isclose(fld.rhomass(), state.Dmass())

def test_instantiation_from_primitives_mixture():

    package = "coolprop"
    model = "SRK"
    composition = {"methane": 0.1, "decane": 0.9}
    molar = True

    p0 = 101325
    T0 = 350
    Q0 = 0.5

    comps = list(composition.keys())
    fracs = list(composition.values())

    fld = cp.AbstractState(model, "&".join(comps))
    fld.set_mole_fractions(fracs)

    fld.update(cp.PQ_INPUTS, p0, 0.5)
    
    state = State.from_primitives(package, model, composition, molar=True)
    state.update(pairs.PQmolar, p0, Q0)

    assert np.isclose(fld.rhomass(), state.Dmass())

    state = State.from_primitives(package, model, composition, molar=False)

    assert all(np.isclose(frac, z) for frac, z in zip(fracs, state.zmass()))

