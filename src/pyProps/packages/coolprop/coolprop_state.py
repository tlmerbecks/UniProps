import CoolProp as cp
from pyProps.pyProps_state import BaseState
from pyProps.utilities.constants import phases


phases_map = {
    cp.iphase_liquid : phases.l,
    cp.iphase_supercritical_liquid : phases.sl,
    cp.iphase_twophase : phases.tp,
    cp.iphase_gas : phases.g,
    cp.iphase_supercritical_gas : phases.sg,
    cp.iphase_supercritical : phases.s
}


class CoolPropState(BaseState):

    r"""
    The wrapper for :code:`CoolProp.AbstractState` classes

    Parameters
    ----------
    state: cp.AbstractState
        The CoolProp AbstractState to be wrapped
    model_type: str
        The backend used
    
    Note:
    -----
    CoolProp generally supports the following calculation modes. That said, not 
    all CoolProp backends support all calculation modes:
    * DH
    * DP
    * DQ
    * DS
    * DT
    * DU
    * HP
    * HQ
    * HS
    * HT
    * PQ
    * PS
    * PT
    * QS
    * QT

    CoolProp does not support the following calculation modes:    
    * HU
    * QU
    """

    def __init__(self, state: cp.AbstractState, model_type:str):
        super().__init__()

        self.package = "CoolProp"
        self.eos: cp.AbstractState = state
        self.model = model_type

        self._components=self.eos.fluid_names()
        self._mole_fractions=self.eos.get_mole_fractions()
        self._molar_masses= [self.eos.get_fluid_constant(i, cp.imolar_mass) for i, fld in enumerate(self._components)]


    def _DmolarHmolar(self, Dmolar, Hmolar, **kwargs):
        self.eos.update(cp.DmolarHmolar_INPUTS, Dmolar, Hmolar)

    def _DmolarP(self, Dmolar, p, **kwargs):
        self.eos.update(cp.DmolarP_INPUTS, Dmolar, p)

    def _DmolarQmolar(self, Dmolar, Qmolar, **kwargs):
        self.eos.update(cp.DmolarQ_INPUTS, Dmolar, Qmolar)

    def _DmolarSmolar(self, Dmolar, Smolar, **kwargs):
        self.eos.update(cp.DmolarSmolar_INPUTS, Dmolar, Smolar)

    def _DmolarT(self, Dmolar, T, **kwargs):
        self.eos.update(cp.DmolarT_INPUTS, Dmolar, T)

    def _DmolarUmolar(self, Dmolar, Umolar, **kwargs):
        self.eos.update(cp.DmolarUmolar_INPUTS, Dmolar, Umolar)

    def _HmolarP(self, Hmolar, p, **kwargs):
        self.eos.update(cp.HmolarP_INPUTS, Hmolar, p)

    def _HmolarQmolar(self, Hmolar, Qmolar, **kwargs):
        if self.Qmolar != 1:
            raise ValueError("CoolProp only supports h-Q calculations for Q=1")
        
        self.eos.update(cp.HmolarQ_INPUTS, Hmolar, Qmolar)

    def _HmolarSmolar(self, Hmolar, Smolar, **kwargs):
        self.eos.update(cp.HmolarSmolar_INPUTS, Hmolar, Smolar)

    def _HmolarT(self, Hmolar, T, **kwargs):
        self.eos.update(cp.HmolarT_INPUTS, Hmolar, T)

    # CoolProp does not have a HmolarUmolar calculation mode


    def _PQmolar(self, p, Qmolar, **kwargs):
        self.eos.update(cp.PQ_INPUTS, p, Qmolar)

    def _PSmolar(self, p, Smolar, **kwargs):
        self.eos.update(cp.PSmolar_INPUTS, p, Smolar)

    def _PT(self, p, T, **kwargs):

        self.eos.update(cp.PT_INPUTS, p, T)

    def _PUmolar(self, p, Umolar, **kwargs):

        self.eos.update(cp.PUmolar_INPUTS, p, Umolar)


    def _QmolarSmolar(self, Qmolar, Smolar, **kwargs):
        if Qmolar != 0 and Qmolar != 1:
            raise ValueError("CoolProp only supports Q-s calculations for Q=0 or Q=1")

        self.eos.update(cp.QSmolar_INPUTS, Qmolar, Smolar)

    def _QmolarT(self, Qmolar, T, **kwargs):
        self.eos.update(cp.QT_INPUTS, Qmolar, T)

    # CoolProp does not implement a QmolarUmolar mode


    def _SmolarT(self, Smolar, T, **kwargs):
        self.eos.update(cp.SmolarT_INPUTS, Smolar, T)

    def _SmolarUmolar(self, Smolar, Umolar, **kwargs):
        self.eos.update(cp.SmolarUmolar_INPUTS, Smolar, Umolar)


    def _TUmolar(self, T, Umolar, **kwargs):
        self.eos.update(cp.TUmolar_INPUTS, T, Umolar)



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

    def _xMr(self) -> float:
        if self.phase == phases.tp:
            return self.eos.saturated_liquid_keyed_output(cp.imolar_mass)
        return self.Mr()
        
    def _yMr(self) -> float:
        if self.phase == phases.tp:
            return self.eos.saturated_liquid_keyed_output(cp.imolar_mass)
        return self.Mr()
    
    def _xmolar(self) -> list[float]:
        return self.eos.mole_fractions_liquid()
        
    def _xmass(self) -> list[float]:
        xmolar = self.eos.mole_fractions_liquid()
        xMr = self.xMr()

        return self._molefrac_to_massfrac(xmolar, xMr)
        
    def _ymolar(self) -> list[float]:
        return self.eos.mole_fractions_vapor()
    
    def _ymass(self) -> list[float]:
        ymolar = self.eos.mole_fractions_vapor()
        yMr = self.yMr()

        return self._molefrac_to_massfrac(ymolar, yMr)
    
    def _zmolar(self) -> list[float]:
        return self.eos.get_mole_fractions()
        
    def _zmass(self) -> list[float]:
        return self.eos.get_mass_fractions()