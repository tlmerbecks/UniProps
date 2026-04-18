import CoolProp as cp
from pyProp import State, pairs

cp_state = cp.AbstractState("HEOS", "Water")

state = State(cp_state)
state.update(pairs.PT, 101325, 350)

p0 = state.p()
h0 = state.hmass()
T0 = state.T()

# CoolProp does not natively support HT calculations for the HEOS backend. 
# The reason being that there may be multiple solutions. 
try:
    state.update(pairs.HmassT, h0, T0)
except Exception as e:
    # the calculation failed
    print(e)

# pyProp can attempt to workaround unsupported calculation modes, but first we
# need to activate this option
from pyProp import settings
settings.DO_WORKAROUND = True

try:
    state.update(pairs.HmassT, h0, T0)
except Exception as e:
    # the calculation failed
    print("Whoops the calculation has failed... this should not have happened")
    exit()


print("The workaround completed successfully!")

print(f"p0: {p0:.4e} p:{state.p():.4e}")
print(f"T0: {T0:.4e} T:{state.T():.4e}")
print(f"hmass0: {h0:.4e} hmass:{state.hmass():.4e}")

# However if we consider a different base state, where there are multiple solutions
# then the calculation will find the state with the maximum pressure

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








# Where multiple solutions exist, pyProp tries to find the maximum pressure
# state that honours the conditions.  
