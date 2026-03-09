from .base import CoolPropState

import numpy as np
import CoolProp as cp


PMIN = 1e-9
PMAX = 1e9


class CubicCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "Cubic"    


class PRCoolPropState(CubicCoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "PengRobinson"


class SRKCoolPropState(CubicCoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "SoaveRedlichKwong"

