import CoolProp as cp
from pyProp.base import BaseState
from pyProp.constants import phases, pairs, properties
from scipy.optimize import minimize


phases_map = {
    cp.iphase_liquid : phases.l,
    cp.iphase_supercritical_liquid : phases.sl,
    cp.iphase_twophase : phases.tp,
    cp.iphase_gas : phases.g,
    cp.iphase_supercritical_gas : phases.sg,
    cp.iphase_supercritical : phases.s
}


class CoolPropState(BaseState):

    def __init__(self, state):
        super().__init__(state)

        self.package = "CoolProp"

        self.eos = state


    def _PT(self, p, T, **kwargs):

        self.eos.update(cp.PT_INPUTS, p, T)

    def _PDmolar(self, p, Dmolar, **kwargs):

        self.eos.update(cp.DmolarP_INPUTS, Dmolar, p)

    def _PQmolar(self, p, Qmolar, **kwargs):
        
        self.eos.update(cp.PQ_INPUTS, p, Qmolar)

    def _PSmolar(self, p, Smolar, **kwargs):

        self.eos.update(cp.PSmolar_INPUTS, p, Smolar)

    def _PHmolar(self, p, Hmolar, **kwargs):

        self.eos.update(cp.HmolarP_INPUTS, Hmolar, p)

    def _PUmolar(self, p, Umolar, **kwargs):

        self.eos.update(cp.PUmolar_INPUTS, p, Umolar)


    def _TDmolar(self, T, Dmolar, **kwargs):

        self.eos.update(cp.DmolarT_INPUTS, Dmolar, T)

    def _TQmolar(self, T, Qmolar, **kwargs):

        self.eos.update(cp.QT_INPUTS, Qmolar, T)
    
    def _TSmolar(self, T, Smolar, **kwargs):

        self.eos.update(cp.SmolarT_INPUTS, Smolar, T)

    def _THmolar(self, T, Hmolar, **kwargs):

        self.eos.update(cp.HmolarT_INPUTS, Hmolar, T)

    def _TUmolar(self, T, Umolar, **kwargs):

        self.eos.update(cp.TUmolar_INPUTS, T, Umolar)


    def _HmolarSmolar(self, Hmolar, Smolar, **kwargs):

        self.eos.update(cp.HmolarSmolar_INPUTS, Hmolar, Smolar)

    def _DmolarHmolar(self, Dmolar, Hmolar, **kwargs):

        self.eos.update(cp.DmolarHmolar_INPUTS, Dmolar, Hmolar)

    def _DmolarSmolar(self, Dmolar, Smolar, **kwargs):

        self.eos.update(cp.DmolarSmolar_INPUTS, Dmolar, Smolar)

    def _DmolarUmolar(self, Dmolar, Umolar, **kwargs):

        self.eos.update(cp.DmolarUmolar_INPUTS, Dmolar, Umolar)

    def _DmolarQmolar(self, Dmolar, Qmolar, **kwargs):

        self.eos.update(cp.DmolarQ_INPUTS, Dmolar, Qmolar)

    def _QmolarSmolar(self, Qmolar, Smolar, **kwargs):

        self.eos.update(cp.QSmolar_INPUTS, Qmolar, Smolar)

    def _QmolarHmolar(self, Qmolar, Hmolar, **kwargs):

        self.eos.update(cp.HmolarQ_INPUTS, Hmolar, Qmolar)



    def _p(self):
        return self.eos.p()
    
    def _T(self):
        return self.eos.T()
    
    def _phase(self): # type: ignore
        phase_type = phases_map[self.eos.phase()]

        return phase_type
    
    def _Qmolar(self):
        return self.eos.Q()
    
    def _Dmass(self):
        return self.eos.rhomass()

    def _Dmolar(self):
        return self.eos.rhomolar()

    def _hmolar(self):
        return self.eos.hmolar()
    
    def _hmass(self):
        return self.eos.hmass()
    
    def _smolar(self):
        return self.eos.smolar()

    def _smass(self):
        return self.eos.smass()
    
    def _umolar(self):
        return self.eos.umolar()

    def _umass(self):
        return self.eos.umass()


    def _Mr(self):
        return self.eos.molar_mass()
    
    def _pcrit(self):
        return self.eos.p_critical()
    
    def _Tcrit(self):
        return self.eos.T_critical()
        
    def _Dmass_crit(self):
        return self.eos.rhomass_critical()
    
    def _Dmolar_crit(self):
        return self.eos.rhomolar_critical()