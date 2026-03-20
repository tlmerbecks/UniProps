from .base import CoolPropState


class HEOSCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "HEOS"


class PRCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "PengRobinson"

    def _Qmolar(self):
        return self.eos.Q()


class SRKCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "SoaveRedlichKwong"

    def _Qmolar(self):
        return self.eos.Q()


class REFPROPCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "REFPROP"

