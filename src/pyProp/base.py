from typing import Dict, Callable, Tuple

from .settings import DO_WORKAROUND
from .settings import PMIN, PMAX

from .constants import pairs, properties, phases, variables
from .utils import inputs_to_default_inputs, pair_to_vars, vars_to_pair, var_to_property
from scipy.optimize import root_scalar, minimize_scalar, minimize

from .residuals import res_T_p, res_Q_p, res_p_T, res_Q_T, res_T_Q
from .objectives import obj_p_T, obj_T_Q


class BaseState:

    package: str
    model: str
    eos: object

    _components: list
    _mole_fractions: list
    _molar_masses: list

    def __init__(self):

        self._update_func_lookup: Dict[pairs, Callable] = {
            pairs.DmolarHmolar : self._DmolarHmolar,
            pairs.DmolarP : self._DmolarP,
            pairs.DmolarQmolar : self._DmolarQmolar,
            pairs.DmolarSmolar : self._DmolarSmolar,
            pairs.DmolarT : self._DmolarT,
            pairs.DmolarUmolar : self._DmolarUmolar,

            pairs.HmolarP : self._HmolarP,
            pairs.HmolarQmolar : self._HmolarQmolar,
            pairs.HmolarSmolar : self._HmolarSmolar,
            pairs.HmolarT : self._HmolarT,
            pairs.HmolarUmolar : self._HmolarUmolar,

            pairs.PQmolar : self._PQmolar,
            pairs.PSmolar : self._PSmolar,
            pairs.PT : self._PT,
            pairs.PUmolar : self._PUmolar,

            pairs.QmolarSmolar : self._QmolarSmolar,
            pairs.QmolarT : self._QmolarT,
            pairs.QmolarUmolar : self._QmolarUmolar,

            pairs.SmolarT : self._SmolarT,
            pairs.SmolarUmolar : self._SmolarUmolar,
            
            pairs.TUmolar : self._TUmolar,
            }
        
        self._property_func_lookup: Dict[properties, Callable] = {
            properties.p : self.p,
            properties.T : self.T,

            properties.Qmass : self.Qmass,
            properties.Qmolar : self.Qmolar,

            properties.Dmass : self.Dmass,
            properties.Dmolar : self.Dmolar,

            properties.Hmass : self.hmass,
            properties.Hmolar : self.hmolar,
            
            properties.Smass : self.smass,
            properties.Smolar : self.smolar,
            
            properties.Umass : self.umass,
            properties.Umolar : self.umolar,
            
            properties.Vmass : self.vmass,
            properties.Vmolar : self.vmolar,

            properties.Tcrit: self.Tcrit,
            properties.pcrit: self.pcrit,
            properties.Dcrit: self.Dcrit,
            properties.Dmass_crit: self.Dmass_crit,
            properties.Dmolar_crit: self.Dmolar_crit,

            properties.Mr: self.Mr,

            properties.Tbubble: self.Tbubble,
            properties.pbubble: self.pbubble,

            properties.Tdew: self.Tdew,
            properties.pdew: self.pdew,

            properties.xMr: self.xMr,
            properties.yMr: self.yMr,
            
            properties.xmolar: self.xmolar,
            properties.ymolar: self.ymolar,
            properties.zmolar: self.zmolar,

            properties.xmass: self.xmass,
            properties.ymass: self.ymass,
            properties.zmass: self.zmass,
            }
    

    def update(self, pair, val1, val2, unit1=None, unit2=None, **kwargs) -> None:

        func, var1, val1_SI, var2, val2_SI = self._preprocess(pair, val1, unit1, val2, unit2)

        try:
            result = func(val1_SI, val2_SI, **kwargs)
        except ValueError as e:
            msg = f"WARNING! Package \"{self.package}\" with model \"{self.model}\" has raised an error \"{e}\"."
            print(msg)

            if DO_WORKAROUND:
                try:
                    print("Attempting to workaround...")
                    result = self._workaround(var1, val1_SI, var2, val2_SI, **kwargs)
                    print("Workaround completed!")
                except:
                    msg = f"Workaround for missing calculation mode failed!"
                    raise Exception(msg)
            else:
                msg = f"Package \"{self.package}\" with model \"{self.model}\" has raised an error \"{e}\"."
                raise ValueError(msg)

        return self._postprocess(result)
    
    def _preprocess(self, pair, val1, unit1, val2, unit2) -> Tuple[Callable, variables, float, variables, float]:

        vals_SI = []
        for unit, val in zip((unit1, unit2), (val1, val2)):
            if unit is None:
                pass
            else:
                print(f"Converting {unit} to SI")

            vals_SI.append(val)

        # check is pair is of the correct type, otherwise try to convert
        if not isinstance(pair, pairs):
            pair = pairs(pair)

        # obtain the variables
        vars = pair_to_vars(pair)

        # obtain the default pair, and variables, conversions and values in the correct order
        dpair, dvar1, dvar2 = inputs_to_default_inputs(pair, vals_SI)

        # now convert the values to the default variable (if required)
        vals_SI = []
        for dvar in (dvar1, dvar2):
            if dvar["conv"] is None:
                if dvar["var"] == variables.Qmolar and variables.Qmass in vars:
                    # the mass to molar quality requires a special conversion
                    vals_SI.append(self._Qmass_to_Qmolar(dvar["val"]))
                else:
                    # the variable is already the default variable and needs no conversion
                    vals_SI.append(dvar["val"])
            else:
                vals_SI.append(dvar["val"] * self.Mr()**dvar["conv"])

        # get the function corresponding to the default pair
        func = self._get_update_func(dpair)

        return func, dvar1["var"], vals_SI[0], dvar2["var"], vals_SI[1]
    
    def _get_update_func(self, pair) -> Callable:

        try:
            func = self._update_func_lookup[pair]
        except KeyError:
            msg = f"The update pair ({pair.name}) is not supported"
            raise KeyError(msg)
        
        return func
    
    def _postprocess(self, result) -> None:

        pass

    # utilities for converting between mass and molar based vapour quality
    def _Qmass_to_Qmolar(self, Qmass: float) -> float:

        Mr = self.Mr()
        yMr = self.yMr()

        return Qmass * (Mr/yMr)

    def _Qmolar_to_Qmass(self, Qmolar: float) -> float:

        Mr = self.Mr()
        yMr = self.yMr()

        return Qmolar * (yMr/Mr)
    
    def _massfrac_to_molefrac(self, massfrac:list[float], Mr) -> list[float]:

        molefrac = [mi*Mr/Mri for mi, Mri in zip(massfrac, self._molar_masses)]

        return molefrac
    
    def _molefrac_to_massfrac(self, molefrac:list[float], Mr) -> list[float]:

        massfrac = [ni*Mri/Mr for ni, Mri in zip(molefrac, self._molar_masses)]

        return massfrac
    


    # the definitions of the base calculation pairs
    def _DmolarHmolar(self, Dmolar: float, Hmolar: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a DmolarHmolar method for the {self.model} model"
        raise NotImplementedError
    
    def _DmolarP(self, Dmolar: float, p: float, **kwargs)  -> None:
        msg = f"The API for {self.package} does not implement yet a DmolarP method for the {self.model} model"
        raise NotImplementedError

    def _DmolarQmolar(self, Dmolar: float, Qmolar: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a DmolarQmolar method for the {self.model} model"
        raise NotImplementedError
    
    def _DmolarSmolar(self, Dmolar: float, Smolar: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a DmolarSmolar method for the {self.model} model"
        raise NotImplementedError
    
    def _DmolarT(self, Dmolar: float, T: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a DmolarT method for the {self.model} model"
        raise NotImplementedError   

    def _DmolarUmolar(self, Dmolar: float, Umolar: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a DmolarUmolar method for the {self.model} model"
        raise NotImplementedError


    def _HmolarP(self, Hmolar: float, p: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a HmolarP method for the {self.model} model"
        raise NotImplementedError

    def _HmolarQmolar(self, Hmolar: float, Qmolar: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a HmolarQmolar method for the {self.model} model"
        raise NotImplementedError

    def _HmolarSmolar(self, Hmolar: float, Smolar: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a HmolarSmolar method for the {self.model} model"
        raise NotImplementedError
       
    def _HmolarT(self, Hmolar: float, T: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a HmolarT method for the {self.model} model"
        raise NotImplementedError
    
    def _HmolarUmolar(self, Hmolar: float, Umolar: float, **kwargs) -> None:
        msg = f"The API for {self.package} does not implement yet a HmolarUmolar method for the {self.model} model"
        raise NotImplementedError
    
   
    def _PQmolar(self, p: float, Qmolar: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a pQmolar method for the {self.model} model"
        raise NotImplementedError

    def _PSmolar(self, p: float, Smolar: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a pSmolar method for the {self.model} model"
        raise NotImplementedError

    def _PT(self, p: float, T: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a pT method for the {self.model} model"
        raise NotImplementedError

    def _PUmolar(self, p: float, Umolar: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a pUmolar method for the {self.model} model"
        raise NotImplementedError


    def _QmolarSmolar(self, Qmolar: float, Smolar: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a QmolarSmolar method for the {self.model} model"
        raise NotImplementedError

    def _QmolarT(self, Qmolar: float, T: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a QmolarT method for the {self.model} model"
        raise NotImplementedError
    
    def _QmolarUmolar(self, Qmolar: float, Umolar: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a QmolarT method for the {self.model} model"
        raise NotImplementedError


    def _SmolarT(self, Smolar: float, T: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a SmolarT method for the {self.model} model"
        raise NotImplementedError

    def _SmolarUmolar(self, Smolar: float, Umolar: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a SmolarUmolar method for the {self.model} model"
        raise NotImplementedError
    

    def _TUmolar(self, T: float, Umolar: float, **kwargs) -> None:

        msg = f"The API for {self.package} does not implement yet a TUmolar method for the {self.model} model"
        raise NotImplementedError


    # the definitions of the workaround functions
    def _workaround(self, var1: variables, 
                    val1: float, 
                    var2: variables, 
                    val2: float, 
                    pmin: float | None =None, 
                    pmax: float | None=None, 
                    **kwargs):

        if pmin is None:
            pmin = PMIN
        elif pmin < PMIN:
            pmin = PMIN

        if pmax is None:
            pmax = PMAX
        elif pmax > PMAX:
            pmax = PMAX

        vars = (var1, var2)
        vals = (val1, val2)

        if variables.P in vars:
            ip = vars.index(variables.P)
            iy = int(not(ip))

            sol = self._PY(vals[ip], vars[iy], vals[iy], **kwargs)

        elif variables.T in vars:
            iT = vars.index(variables.T)
            iy = int(not(iT))

            sol = self._TY(vals[iT], vars[iy], vals[iy], pmin, pmax, **kwargs)

        elif variables.Qmolar in vars:
            iQ = vars.index(variables.Qmolar)
            iy = int(not(iQ))

            sol = self._QY(vals[iQ], vars[iy], vals[iy], pmin, **kwargs)

        else:

            sol = self._YZ(vals, vars, **kwargs)

        assert sol

    def _PY(self, p: float, var: variables, y: float, **kwargs):

        pcrit = self.pcrit()
        Tcrit = self.Tcrit()

        prop = var_to_property(var)

        if p >= pcrit:
            sol = root_scalar(res_T_p, args=(self, p, prop, y, kwargs), method="secant", x0=Tcrit, x1=Tcrit+(1+1e-4))
            return sol.converged
        
        self._PQmolar(p, 0, **kwargs)
        # self.update(pairs.pQmolar, p, 0, **kwargs)
        Tbubble = self.T()
        ybubble = self.get(prop)

        self._PQmolar(p, 1, **kwargs)
        # self.update(pairs.pQmolar, p, 1, **kwargs)
        Tdew = self.T()
        ydew = self.get(prop)

        if (ybubble - y) * (y - ydew) >= 0:
            # two-phase segion
            sol = root_scalar(res_Q_p, args=(self, p, prop, y, kwargs), method="brentq", bracket=[0, 1])

            return sol.converged
        
        if (ybubble - y) * (ybubble - ydew) < 0:
            # single phase - between (p, Q=0) and (p, T=Tmax)
            sol = root_scalar(res_T_p, args=(self, p, prop, y, kwargs), method="secant", x0=Tbubble * (1 - 1e-6), x1=Tbubble * (1 - 1e-5))

            return sol.converged

        else:
            # single phase - between (p, Q=1) and (p, Tmin)
            sol = root_scalar(res_T_p, args=(self, p, prop, y, kwargs), method="secant", x0=Tdew * (1 - 1e-6), x1=Tdew * (1 - 1e-5))
            
            return sol.converged
    
    def _TY(self, T: float, var: variables, y: float, pmin: float, pmax: float, **kwargs):

        # list of variables, where TY may have multiple solutions
        tricky_TY = [variables.Hmolar, variables.Umolar]

        pcrit = self.pcrit()
        Tcrit = self.Tcrit()

        prop = var_to_property(var)

        if T >= Tcrit:
            if prop in tricky_TY:
                sol = minimize_scalar(obj_p_T, args=(self, T, prop, y, pcrit, kwargs), bounds=[pmin, pmax])

                return sol.success  # type: ignore
            else:
                sol = root_scalar(res_p_T, args=(self, T, prop, y, kwargs), method="secant", x0=pcrit, x1=pcrit+(1+1e-4))

                return sol.converged
        
        self.update(pairs.QmolarT, 0, T, **kwargs)
        pbubble = self.p()
        ybubble = self.get(prop)

        self.update(pairs.QmolarT, 1, T, **kwargs)
        pdew = self.p()
        ydew = self.get(prop)

        self._PT(pmax, T)
        # self.update(pairs.pT, pmax, T)
        ymax = self.get(prop)

        if (ymax - y) * (y - ybubble) > 0:
            # liquid phase - between (T, Q=0) and (T, p=pmax)
            if prop in tricky_TY:
                sol = minimize_scalar(obj_p_T, args=(self, T, prop, y, pcrit, kwargs), bounds=[pbubble * (1 + 1e-6), pmax])

                return sol.success  # type: ignore
            else:
                sol = root_scalar(res_p_T, args=(self, T, prop, y, kwargs), method="brentq", bracket=[pbubble * (1 + 1e-6), pmax])

                return sol.converged
        
        elif (ybubble - y) * (y - ydew) >= 0:
            # two-phase - between (T, Q=0) and (T, Q=1)
            sol = root_scalar(res_Q_T, args=(self, T, prop, y, kwargs), method="brentq", bracket=[0, 1])
            # Note: even in case of var in [variables.Hmolar, etc.], the optimisation is not needed here, 
            # for pure fluids anyway, because psat is constant with quality, hence the penalty factor is
            # just a shift, and better convergence can be achieved with a simple root-finding solution

            return sol.converged

        elif (ydew - y) * (ybubble - ydew) > 0:
            # vapor phase - between (T, Q=1) and (T, p=pmin)

            if prop in tricky_TY:
                sol = minimize_scalar(obj_p_T, args=(self, T, prop, y, pcrit, kwargs), bounds=[pdew * (1 - 1e-6), pmin])

                return sol.success  # type: ignore
            else:
                sol = root_scalar(res_p_T, args=(self, T, prop, y, kwargs), method="brentq", bracket=[pdew * (1 - 1e-6), pmin])

                return sol.converged
        
        else:
            msg = f"Solution p for T={T} and {var.name}=y is outwith the pressure range of pmin={pmin} and pmax={pmax}"
            raise ValueError(msg)

    def _QY(self, Q: float, var: variables, y: float, pmin: float, **kwargs):

        # list of variables, where TY may have multiple solutions
        tricky_QY = [variables.Hmolar, variables.Umolar]

        prop = var_to_property(var)

        pcrit = self.pcrit()
        Tcrit = self.Tcrit()
        self.update(pairs.PT, pcrit, Tcrit)
        ycrit = self.get(prop)

        self.update(pairs.PQmolar, pmin, Q)
        Tmin = self.T()
        ymin = self.get(prop)

        if (ycrit - y) * (y - ymin) >= 0:
            if prop in tricky_QY:
                sol = minimize_scalar(obj_T_Q, args=(self, Q, prop, y, pcrit, kwargs), bounds=[Tmin, Tcrit])

                return sol.success  # type: ignore
            else:
                sol = root_scalar(res_T_Q, args=(self, Q, prop, y, kwargs), method="brentq", bracket=[Tmin, Tcrit])

                return sol.converged
        else:
            msg = f"Solution p for Q={Q} and {prop.name}={y} is outwith the pressure range of pmin={pmin} and pcrit={pcrit}"
            raise ValueError(msg)

    def _YZ(self, vals: tuple[float, float], vars: tuple[variables,variables], **kwargs):

        _pair_py = vars_to_pair(variables.P, vars[0])
        _pair_pz = vars_to_pair(variables.P, vars[1])

        y, z = vals

        p0 = self.pcrit() * 1.1

        def p_YZ(p):
            
            self.update(_pair_py, p, y, **kwargs)
            T_y = self.T()

            self.update(_pair_pz, p, z, **kwargs)
            T_z = self.T()

            diff = (T_y/T_z) - 1

            return diff
        
        sol = root_scalar(p_YZ, method="secant", x0=p0, x1=p0 * (1 + 1e-4), rtol=1e-6)

        return sol.converged

    # definitions of the functions for retrieving various properties
    def get(self, property: properties, *args, unit=None, **kwargs):

        # check is pair is of the correct type, otherwise try to convert
        if not isinstance(property, properties):
            property = properties(property)
        
        try:
            func = self._property_func_lookup[property]
        except KeyError:
            msg = f"The property {property.value} is not supported"
            raise KeyError(msg)

        var_SI = func(*args, **kwargs)

        if unit is None:
            var = var_SI
        else:
            # need to convert the units
            print("converting SI to unit")
            var = var_SI * 1

        return var


    def pcrit(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.pcrit, unit=unit)
        
        return self._pcrit()
    
    def _pcrit(self) -> float:
        return -1.


    def Tcrit(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Tcrit, unit=unit)
        
        return self._Tcrit()
    
    def _Tcrit(self) -> float:
        return -1.


    def Dcrit(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Dcrit, unit=unit)
        
        return self._Dcrit()
    
    def _Dcrit(self) -> float:
        return -1.

    def Dmass_crit(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Dmass_crit, unit=unit)
        
        return self._Dmass_crit()
    
    def _Dmass_crit(self) -> float:
        return -1.

    def Dmolar_crit(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Dmolar_crit, unit=unit)
        
        return self._Dmolar_crit()
    
    def _Dmolar_crit(self) -> float:
        return -1.
    

    def Mr(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Mr, unit=unit)
        
        return self._Mr()
    
    def _Mr(self) -> float:
        return -1.


    def p(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.p, unit=unit)
        
        return self._p()

    def _p(self) -> float:
        return -1


    def T(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.T, unit=unit)
        
        return self._T()

    def _T(self) -> float:
        return -1.

    
    def Qmass(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Qmass, unit=unit)
        
        return self._Qmolar_to_Qmass(self.Qmolar())
    
    def Qmolar(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Qmolar, unit=unit)

        phase = self.phase()

        if phase in [phases.l, phases.sl]:
            return 0.
        elif phase in [phases.g, phases.sg, phases.s]:
            return 1.
        elif phase in [phases.tp]:
            return self._Qmolar()
        else:
            return -1.
    
    def _Qmolar(self) -> float:
        return -1
    

    def Dmass(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Dmass, unit=unit)
        
        return self._Dmass()
    
    def _Dmass(self) -> float:
        return -1.

    def Dmolar(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Dmolar, unit=unit)
        
        return self._Dmolar()
    
    def _Dmolar(self) -> float:
        return -1.


    def vmass(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Vmass, unit=unit)
        
        return self._vmass()
    
    def _vmass(self) -> float:
        return 1 / self._Dmass()

    def vmolar(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Vmolar, unit=unit)
        
        return self._vmolar()
    
    def _vmolar(self) -> float:
        return 1 / self._Dmolar()


    def hmass(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Hmass, unit=unit)
        
        return self._hmass()
    
    def _hmass(self) -> float:
        return -1.

    def hmolar(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Hmolar, unit=unit)
        
        return self._hmolar()
    
    def _hmolar(self) -> float:
        return -1.


    def smass(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Smass, unit=unit)
        
        return self._smass()
    
    def _smass(self) -> float:
        return -1.

    def smolar(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Smolar, unit=unit)
        
        return self._smolar()
    
    def _smolar(self) -> float:
        return -1.


    def umass(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Umass, unit=unit)
        
        return self._umass()
    
    def _umass(self) -> float:
        return -1.

    def umolar(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.Umolar, unit=unit)
        
        return self._umolar()
    
    def _umolar(self) -> float:
        return -1.


    def phase(self, **kwargs) -> phases:
        return self._phase()
    
    def _phase(self) -> phases:
        return phases.none


    def Tbubble(self, p, unit=None, punit=None) -> float:
        if not unit is None:
            return self.get(properties.Tbubble, unit=unit)
                
        return self._Tbubble(p, unit=punit)
    
    def _Tbubble(self, p, unit=None) -> float:

        self.update(pairs.PQmolar, p, 0, unit1=unit)

        return self.T()


    def pbubble(self, T, unit=None, Tunit=None) -> float:
        if not unit is None:
            return self.get(properties.pbubble, unit=unit)
        
        return self._pbubble(T, unit=Tunit)
    
    def _pbubble(self, T, unit=None) -> float:

        self.update(pairs.QmolarT, 0, T, unit1=unit)

        return self.p()


    def Tdew(self, p, unit=None, punit=None) -> float:
        if not unit is None:
            return self.get(properties.Tdew, unit=unit)
        
        return self._Tdew(p, unit=punit)
    
    def _Tdew(self, p, unit=None) -> float:

        self.update(pairs.PQmolar, p, 1, unit1=unit)

        return self.T()


    def pdew(self, T, unit=None, Tunit=None, **kwargs) -> float:
        if not unit is None:
            return self.get(properties.pdew, unit=unit)
        
        return self._pdew(T, unit=Tunit)
    
    def _pdew(self, T, unit=None, **kwargs) -> float:

        self.update(pairs.QmolarT, 1, T, unit1=unit)

        return self.p()

    def xMr(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.xMr, unit=unit)
        
        return self._xMr()
    
    def _xMr(self) -> float:
        return self.Mr()
    
    def yMr(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.yMr, unit=unit)
        
        return self._yMr()
    
    def _yMr(self) -> float:
        return self.Mr()

    def xmolar(self, unit=None) -> list[float]:
        if not unit is None:
            return self.get(properties.xmolar, unit=unit)
        
        return self._xmolar()
    
    def _xmolar(self) -> list[float]:
        return [1.]
    
    def xmass(self, unit=None) -> list[float]:
        if not unit is None:
            return self.get(properties.xmass, unit=unit)
        
        return self._xmass()
    
    def _xmass(self) -> list[float]:
        return [1.]
    
    def ymolar(self, unit=None) -> list[float]:
        if not unit is None:
            return self.get(properties.ymolar, unit=unit)
        
        return self._ymolar()
    
    def _ymolar(self) -> list[float]:
        return [1.]
    
    def ymass(self, unit=None) -> list[float]:
        if not unit is None:
            return self.get(properties.ymass, unit=unit)
        
        return self._ymass()
    
    def _ymass(self) -> list[float]:
        return [1.]


    def zmolar(self, unit=None) -> list[float]:
        if not unit is None:
            return self.get(properties.zmolar, unit=unit)
        
        return self._zmolar()
    
    def _zmolar(self) -> list[float]:
        return [1.]
    
    def zmass(self, unit=None) -> list[float]:
        if not unit is None:
            return self.get(properties.zmass, unit=unit)
        
        return self._zmass()
    
    def _zmass(self) -> list[float]:
        return [1.]