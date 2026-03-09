from .base import CoolPropState


class REFPROPCoolPropState(CoolPropState):

    def __init__(self, state):
        super().__init__(state)

        self.model = "HEOS"
