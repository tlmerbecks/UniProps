from .base import CoolPropState
from pyProp.constants import pairs, properties

import CoolProp as cp
from scipy.optimize import brentq, minimize, root_scalar
import numpy as np

from time import perf_counter

class HEOSCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "HEOS"

    # def _workaround(self, prop1, val1, prop2, val2, pmin=None, pmax=None, **kwargs):

    #     if pmin is None:
    #         pmin = self.eos.trivial_keyed_output(cp.iP_min)
    #     elif pmin < self.eos.trivial_keyed_output(cp.iP_min):
    #         pmin = self.eos.trivial_keyed_output(cp.iP_min)

    #     if pmax is None:
    #         pmax = self.eos.pmax()
    #     elif pmax > self.eos.pmax():
    #         pmax = self.eos.pmax()

    #     pcrit = self.pcrit()

    #     def func(x):
    #         T, D = x
    #         self.update(pairs.TD, T, D)

    #         diff1 = np.log10(((self.get(prop1) - val1) / (val1 + 1e-15))**2 + 1e-15)
    #         diff2 = np.log10(((self.get(prop2) - val2) / (val2 + 1e-15))**2 + 1e-15)

    #         penal = np.log10(pcrit / self.get(properties.p))

    #         obj = diff1 + diff2 + penal

    #         return obj
        
    #     props = [prop1, prop2]
    #     vals = [val1, val2]

    #     if properties.T in props:
    #         iT = props.index(properties.T)
    #         iy = int(not(iT))

    #         T = vals[iT]

    #         x0 = (T, self.Dcrit())

    #         self.update(pairs.pT, pmin, T)
    #         Dmin = self.D()

    #         self.update(pairs.pT, pmax, T)
    #         Dmax = self.D()

    #         bounds = [
    #             (T, T),
    #             (Dmin, Dmax)
    #             ]
    #         x0 = (
    #             T,
    #             Dmax
    #             )
    #         constraints=[]

    #     else:
    #         msg = ""
    #         raise NotImplementedError(msg)

    #     sol = minimize(
    #         func,
    #         x0,
    #         bounds=bounds,
    #         constraints=constraints
    #         )
        
    #     assert sol.success

    #     T, D = sol.x
    #     self.update(pairs.TD, T, D)

    #     diff1 = ((self.get(prop1) - val1) / (val1 + 1e-15))**2
    #     diff2 = ((self.get(prop2) - val2) / (val2 + 1e-15))**2
    #     if diff1 + diff2 > 1e-6:
    #         msg = f"Minimisation completed successfully, but the failed to converge on {prop1.value} ({val1}) and {prop2.value} ({val2})"
    #         raise ValueError(msg)

