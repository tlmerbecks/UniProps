from .base import CoolPropState


class HEOSCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "HEOS"


class PRCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "PengRobinson"


class SRKCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "SoaveRedlichKwong"


class REFPROPCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "REFPROP"

