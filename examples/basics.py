import CoolProp as cp
from pyProp import State, pairs

cp_state = cp.AbstractState("HEOS", "Water")

state = State(cp_state)
state.update(pairs.PT, 101325, 350)

print(state.p())
print(state.T())
print(state.Dmass())
print(state.hmass())
