# pyProps - unified API for fluid modelling

There are a number of popular fluid modelling libraries (e.g. CoolProp, REFPROP, fluidprop, thermopack, etc.), however they each implement a different API for orchestrating calculations. This makes it difficult to seamlessly switch between fluid models without implementing a custom wrapper. pyProps aims to provide that wrapper and standardise the workflow for instantiating fluid models, performing calculations and retrieving properties.

# Installation

```
pip install pyProps
```

# Features

* Supported Libraries
    - CoolProp (HEOS, SRK, PR) 
    - RefProp (via CoolProp)
* Calculations for all combinations of density, enthalpy, entropy, internal energy, pressure, quality and temperature are supported - both for molar and mass-based specifications.
* Evaluate state properties: density, enthalpy, entropy, internal energy, pressure, quality, temperature, volume - both molar and mass-based; bubble-point pressure/temperature, dew-point pressure/temperature; total/vapour/liquid phase molecular weight, mass fraction, mole fraction

# Roadmap
* Add additional libraries
    - fluidprop
    - thermopack
    - ...
* Expose more properties and default methods where a library does not provide these
* Add detailed documentation and examples
* Expand unit tests

# Examples

## Wrapping Fluid Models

Create a fluid representation in your preferred fluid modelling library, then apply the pyProps wrapper:

```
import CoolProp as cp
from pyProps import State, pairs

cp_state = cp.AbstractState("HEOS", "Water")

state = State(cp_state)
state.update(pairs.PT, 101325, 350)

print(state.p())
print(state.T())
print(state.Dmass())
print(state.hmass())
```

## Handling of missing calculation modes

A fluid modelling libraries may not support all combinations of state variable pairs; for example, the CoolProp SRK backend does not support enthalpy-pressure calculations, see [website](https://coolprop.org/coolprop/Cubics.html#caveats) and [github](https://github.com/CoolProp/CoolProp/blob/a3a8040360b8869d64b8438a56d730d7d35eeac4/src/Backends/Cubics/CubicBackend.cpp#L321). Until now, if we wanted to perform such a calculation we would have to implement a custom routine - within pyProps these routines have already been implemented.

The following will raise an error as the enthalpy-pressure calcualtion is not supported
```
import CoolProp as cp

p = 101325
T = 350

fld = cp.AbstractState("SRK", "Water")
fld.update(cp.PT_INPUTS, p, T)

hmass = fld.hmass()

fld.update(cp.HmassP_INPUTS, hmass, p)
```

To perform this calculation with pyProps, we wrap the fluid model and set `pyProps.settings.DO_WORKAROUND=True`
```
from pyProps import State, pairs
state = State(fld)

from pyProps import settings
settings.DO_WORKAROUND = True

state.update(pairs.HmassP, hmass, p)

print(T, state.T())
```

Moreover, some calculation modes may not yield a unique solution, e.g. enthalpy-temperature calculations may have multiple solutions. In this case the pyProps solver tries to find the solutions with the maximum pressure.

In the following case, the initial state corresponds to the maximum pressure state, hence the initial and final pressure are the same,
```
import CoolProp as cp
fld = cp.AbstractState("HEOS", "water")

from pyProps import State, pairs
from pyProps import settings
settings.DO_WORKAROUND = True

state = State(fld)

# evaluate some base state
state.update(pairs.PT, 101325, 350)
p0 = state.p()
h0 = state.hmass()
T0 = state.T()

state.update(pairs.HmassT, h0, T0)
print(f"p0: {p0:.4e} p:{state.p():.4e}")
print(f"T0: {T0:.4e} T:{state.T():.4e}")
print(f"hmass0: {h0:.4e} hmass:{state.hmass():.4e}")
```

However, there are also cases where this is not the case and a higher pressure state exists that can be described by the same enthalpy and temperature combination
```
state.update(pairs.PQmolar, 101325, 0.1)

p0 = state.p()
h0 = state.hmass()
T0 = state.T()

try:
    state.update(pairs.HmassT, h0, T0)
except Exception as e:
    # the calculation failed
    print("Whoops the calculation has failed... this should not have happened")
    exit()

print(f"p0: {p0:.4e} p:{state.p():.4e}")
print(f"T0: {T0:.4e} T:{state.T():.4e}")
print(f"hmass0: {h0:.4e} hmass:{state.hmass():.4e}")
```




enthalpy-temperature calculations for native models (since multiple solutions may exist), or the cubic eos backends only support a small subset of


