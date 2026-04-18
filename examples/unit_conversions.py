import CoolProp as cp
from pyProp import State, pairs

cp_state = cp.AbstractState("HEOS", "Water")

state = State(cp_state)

# Calculation and Results in SI
state.update(pairs.PT, 101325, 350)

print(state.p())
print(state.T())
print(state.Dmass())
print(state.hmass())

# Calculation using non-SI units but Results in SI
state.update(pairs.PT, 1.01325, 350-273.15, unit1="bar", unit2="degC")

print(state.p())
print(state.T())
print(state.Dmass())
print(state.hmass())

# Calculation and Results using non-SI units
state.update(pairs.PT, 1.01325, 350-273.15, unit1="bar", unit2="degC")

print(state.p(unit="bar"))
print(state.T(unit="degC"))
print(state.Dmass(unit="g/m3"))
print(state.hmass(unit="kJ/kg"))