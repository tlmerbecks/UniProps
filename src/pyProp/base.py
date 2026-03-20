from .settings import DO_WORKAROUND
from .settings import PMIN, PMAX

from .constants import pairs, properties, phases, variables
from .utils import inputs_to_default_inputs, pair_to_vars, vars_to_pair
from scipy.optimize import root_scalar, minimize_scalar, minimize

from .residuals import res_T_p, res_Q_p, res_p_T, res_Q_T, res_T_Q
from .objectives import obj_p_T, obj_T_Q


class BaseState:

    def __init__(self, state):

        self.package = None
        self.model = None

        self.eos = None

        self._update_func_lookup = {
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
        
        self._property_func_lookup = {
            properties.p.value : self.p,
            properties.T.value : self.T,

            properties.Qmass.value : self.Qmass,
            properties.Qmolar.value : self.Qmolar,

            properties.Dmass.value : self.Dmass,
            properties.Dmolar.value : self.Dmolar,

            properties.Hmass.value : self.hmass,
            properties.Hmolar.value : self.hmolar,
            
            properties.Smass.value : self.smass,
            properties.Smolar.value : self.smolar,
            
            properties.Umass.value : self.umass,
            properties.Umolar.value : self.umolar,
            
            properties.Vmass.value : self.vmass,
            properties.Vmolar.value : self.vmolar,

            properties.Tcrit.value: self.Tcrit,
            properties.pcrit.value: self.pcrit,
            properties.Dcrit.value: self.Dcrit,
            properties.Dmass_crit.value: self.Dmass_crit,
            properties.Dmolar_crit.value: self.Dmolar_crit,

            properties.Mr.value: self.Mr,

            properties.Tbubble.value: self.Tbubble,
            properties.pbubble.value: self.pbubble,

            properties.Tdew.value: self.Tdew,
            properties.pdew.value: self.pdew,
            }
    

    def update(self, pair, val1, val2, unit1=None, unit2=None, **kwargs):

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
    
    def _preprocess(self, pair, val1, unit1, val2, unit2):

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
    
    def _get_update_func(self, pair):

        try:
            func = self._update_func_lookup[pair]
        except KeyError:
            msg = f"The update pair ({pair.name}) is not supported"
            raise KeyError(msg)
        
        return func
    
    def _postprocess(self, result):

        pass

    # utilities for converting between mass and molar based vapour quality
    def _Qmass_to_Qmolar(self, Qmass):

        return Qmass * 1.
    
    def _Qmolar_to_Qmass(self, Qmolar):

        return Qmolar * 1.


    def _DmolarHmolar(self, Dmolar, Hmolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a DmolarHmolar method for the {self.model} model"
        raise NotImplementedError
    
    def _DmolarP(self, Dmolar, p, **kwargs):

        msg = f"The API for {self.package} does not implement yet a DmolarP method for the {self.model} model"
        raise NotImplementedError

    def _DmolarQmolar(self, Dmolar, Qmolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a DmolarQmolar method for the {self.model} model"
        raise NotImplementedError
    
    def _DmolarSmolar(self, Dmolar, Smolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a DmolarSmolar method for the {self.model} model"
        raise NotImplementedError
    
    def _DmolarT(self, Dmolar, T, **kwargs):

        msg = f"The API for {self.package} does not implement yet a DmolarT method for the {self.model} model"
        raise NotImplementedError   

    def _DmolarUmolar(self, Dmolar, Umolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a DmolarUmolar method for the {self.model} model"
        raise NotImplementedError


    def _HmolarP(self, Hmolar, p, **kwargs):

        msg = f"The API for {self.package} does not implement yet a HmolarP method for the {self.model} model"
        raise NotImplementedError

    def _HmolarQmolar(self, Hmolar, Qmolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a HmolarQmolar method for the {self.model} model"
        raise NotImplementedError

    def _HmolarSmolar(self, Hmolar, Smolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a HmolarSmolar method for the {self.model} model"
        raise NotImplementedError
       
    def _HmolarT(self, Hmolar, T, **kwargs):

        msg = f"The API for {self.package} does not implement yet a HmolarT method for the {self.model} model"
        raise NotImplementedError
    
    def _HmolarUmolar(self, Hmolar, Umolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a HmolarUmolar method for the {self.model} model"
        raise NotImplementedError
    
   
    def _PQmolar(self, p, Qmolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a pQmolar method for the {self.model} model"
        raise NotImplementedError

    def _PSmolar(self, p, Smolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a pSmolar method for the {self.model} model"
        raise NotImplementedError

    def _PT(self, p, T, **kwargs):

        msg = f"The API for {self.package} does not implement yet a pT method for the {self.model} model"
        raise NotImplementedError

    def _PUmolar(self, p, Umolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a pUmolar method for the {self.model} model"
        raise NotImplementedError


    def _QmolarSmolar(self, Qmolar, Smolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a QmolarSmolar method for the {self.model} model"
        raise NotImplementedError

    def _QmolarT(self, Qmolar, T, **kwargs):

        msg = f"The API for {self.package} does not implement yet a QmolarT method for the {self.model} model"
        raise NotImplementedError
    
    def _QmolarUmolar(self, Qmolar, Umolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a QmolarT method for the {self.model} model"
        raise NotImplementedError


    def _SmolarT(self, Smolar, T, **kwargs):

        msg = f"The API for {self.package} does not implement yet a SmolarT method for the {self.model} model"
        raise NotImplementedError

    def _SmolarUmolar(self, Smolar, Umolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a SmolarUmolar method for the {self.model} model"
        raise NotImplementedError
    

    def _TUmolar(self, T, Umolar, **kwargs):

        msg = f"The API for {self.package} does not implement yet a TUmolar method for the {self.model} model"
        raise NotImplementedError


    def _workaround(self, var1, val1, var2, val2, pmin=None, pmax=None, **kwargs):

        if pmin is None:
            pmin = PMIN
        elif pmin < PMIN:
            pmin = PMIN

        if pmax is None:
            pmax = PMAX
        elif pmax > PMAX:
            pmax = PMAX

        vars = [var1, var2]
        vals = [val1, val2]

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

    def _PY(self, p, var, y, **kwargs):

        pcrit = self.pcrit()
        Tcrit = self.Tcrit()

        if p >= pcrit:
            sol = root_scalar(res_T_p, args=(self, p, var, y, kwargs), method="secant", x0=Tcrit, x1=Tcrit+(1+1e-4))
            return sol.converged
        
        self._PQmolar(p, 0, **kwargs)
        # self.update(pairs.pQmolar, p, 0, **kwargs)
        Tbubble = self.T()
        ybubble = self.get(var)

        self._PQmolar(p, 1, **kwargs)
        # self.update(pairs.pQmolar, p, 1, **kwargs)
        Tdew = self.T()
        ydew = self.get(var)

        if (ybubble - y) * (y - ydew) >= 0:
            # two-phase segion
            sol = root_scalar(res_Q_p, args=(self, p, var, y, kwargs), method="brentq", bracket=[0, 1])

            return sol.converged
        
        if (ybubble - y) * (ybubble - ydew) < 0:
            # single phase - between (p, Q=0) and (p, T=Tmax)
            sol = root_scalar(res_T_p, args=(self, p, var, y, kwargs), method="secant", x0=Tbubble * (1 - 1e-6), x1=Tbubble * (1 - 1e-5))

            return sol.converged

        else:
            # single phase - between (p, Q=1) and (p, Tmin)
            sol = root_scalar(res_T_p, args=(self, p, var, y, kwargs), method="secant", x0=Tdew * (1 - 1e-6), x1=Tdew * (1 - 1e-5))
            
            return sol.converged
    
    def _TY(self, T, var, y, pmin, pmax, **kwargs):

        # list of variables, where TY may have multiple solutions
        tricky_TY = [variables.Hmolar, variables.Umolar]

        pcrit = self.pcrit()
        Tcrit = self.Tcrit()

        if T >= Tcrit:
            if var in tricky_TY:
                sol = minimize_scalar(obj_p_T, args=(self, T, var, y, pcrit, kwargs), bounds=[pmin, pmax])

                return sol.success  # type: ignore
            else:
                sol = root_scalar(res_p_T, args=(self, T, var, y, kwargs), method="secant", x0=pcrit, x1=pcrit+(1+1e-4))

                return sol.converged
        
        self.update(pairs.QmolarT, 0, T, **kwargs)
        pbubble = self.p()
        ybubble = self.get(var)

        self.update(pairs.QmolarT, 1, T, **kwargs)
        pdew = self.p()
        ydew = self.get(var)

        self._PT(pmax, T)
        # self.update(pairs.pT, pmax, T)
        ymax = self.get(var)

        if (ymax - y) * (y - ybubble) > 0:
            # liquid phase - between (T, Q=0) and (T, p=pmax)
            if var in tricky_TY:
                sol = minimize_scalar(obj_p_T, args=(self, T, var, y, pcrit, kwargs), bounds=[pbubble * (1 + 1e-6), pmax])

                return sol.success  # type: ignore
            else:
                sol = root_scalar(res_p_T, args=(self, T, var, y, kwargs), method="brentq", bracket=[pbubble * (1 + 1e-6), pmax])

                return sol.converged
        
        elif (ybubble - y) * (y - ydew) >= 0:
            # two-phase - between (T, Q=0) and (T, Q=1)
            sol = root_scalar(res_Q_T, args=(self, T, var, y, kwargs), method="brentq", bracket=[0, 1])
            # Note: even in case of var in [variables.Hmolar, etc.], the optimisation is not needed here, 
            # for pure fluids anyway, because psat is constant with quality, hence the penalty factor is
            # just a shift, and better convergence can be achieved with a simple root-finding solution

            return sol.converged

        elif (ydew - y) * (ybubble - ydew) > 0:
            # vapor phase - between (T, Q=1) and (T, p=pmin)

            if var in tricky_TY:
                sol = minimize_scalar(obj_p_T, args=(self, T, var, y, pcrit, kwargs), bounds=[pdew * (1 - 1e-6), pmin])

                return sol.success  # type: ignore
            else:
                sol = root_scalar(res_p_T, args=(self, T, var, y, kwargs), method="brentq", bracket=[pdew * (1 - 1e-6), pmin])

                return sol.converged
        
        else:
            msg = f"Solution p for T={T} and {var.name}=y is outwith the pressure range of pmin={pmin} and pmax={pmax}"
            raise ValueError(msg)

    def _QY(self, Q, prop, y, pmin, **kwargs):

        # list of variables, where TY may have multiple solutions
        tricky_QY = [variables.Hmolar, variables.Umolar]

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

    def _YZ(self, vals, props, **kwargs):

        _pair_py = vars_to_pair(variables.P, props[0])
        _pair_pz = vars_to_pair(variables.P, props[1])

        y, z = vals

        p0 = self.pcrit() * 1.1

        def p_YZ(p):
            
            # funcy(p, y, **kwargs)
            self.update(_pair_py, p, y, **kwargs)
            T_y = self.T()

            # funcz(p, z, **kwargs)
            self.update(_pair_pz, p, z, **kwargs)
            T_z = self.T()

            diff = (T_y/T_z) - 1

            return diff
        
        sol = root_scalar(p_YZ, method="secant", x0=p0, x1=p0 * (1 + 1e-4), rtol=1e-6)

        return sol.converged


    def get(self, property, *args, unit=None, **kwargs):

        # check is pair is of the correct type, otherwise try to convert
        if not isinstance(property, properties):
            property = properties(property)
        
        try:
            func = self._property_func_lookup[property.value]
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


    def pcrit(self, unit=None):
        if not unit is None:
            return self.get(properties.pcrit, unit=unit)
        
        return self._pcrit()
    
    def _pcrit(self):
        return -1.


    def Tcrit(self, unit=None):
        if not unit is None:
            return self.get(properties.Tcrit, unit=unit)
        
        return self._Tcrit()
    
    def _Tcrit(self):
        return -1.


    def Dcrit(self, unit=None):
        if not unit is None:
            return self.get(properties.Dcrit, unit=unit)
        
        return self._Dcrit()
    
    def _Dcrit(self):
        return -1.

    def Dmass_crit(self, unit=None):
        if not unit is None:
            return self.get(properties.Dmass_crit, unit=unit)
        
        return self._Dmass_crit()
    
    def _Dmass_crit(self):
        return -1.

    def Dmolar_crit(self, unit=None):
        if not unit is None:
            return self.get(properties.Dmolar_crit, unit=unit)
        
        return self._Dmolar_crit()
    
    def _Dmolar_crit(self):
        return -1.
    

    def Mr(self, unit=None):
        if not unit is None:
            return self.get(properties.Mr, unit=unit)
        
        return self._Mr()
    
    def _Mr(self):
        return -1.


    def p(self, unit=None):
        if not unit is None:
            return self.get(properties.p, unit=unit)
        
        return self._p()

    def _p(self):
        return -1


    def T(self, unit=None) -> float:
        if not unit is None:
            return self.get(properties.T, unit=unit)
        
        return self._T()

    def _T(self) -> float:
        return -1.

    
    def Qmass(self, unit=None):
        if not unit is None:
            return self.get(properties.Qmass, unit=unit)
        
        return self._Qmolar_to_Qmass(self.Qmolar())
    
    def Qmolar(self, unit=None):
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
    
    def _Qmolar(self):
        return -1
    

    def Dmass(self, unit=None):
        if not unit is None:
            return self.get(properties.Dmass, unit=unit)
        
        return self._Dmass()
    
    def _Dmass(self):
        return -1.

    def Dmolar(self, unit=None):
        if not unit is None:
            return self.get(properties.Dmolar, unit=unit)
        
        return self._Dmolar()
    
    def _Dmolar(self):
        return -1.


    def vmass(self, unit=None):
        if not unit is None:
            return self.get(properties.Vmass, unit=unit)
        
        return self._vmass()
    
    def _vmass(self):
        return 1 / self._Dmass()

    def vmolar(self, unit=None):
        if not unit is None:
            return self.get(properties.Vmolar, unit=unit)
        
        return self._vmolar()
    
    def _vmolar(self):
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


    def smass(self, unit=None):
        if not unit is None:
            return self.get(properties.Smass, unit=unit)
        
        return self._smass()
    
    def _smass(self):
        return -1.

    def smolar(self, unit=None):
        if not unit is None:
            return self.get(properties.Smolar, unit=unit)
        
        return self._smolar()
    
    def _smolar(self):
        return -1.


    def umass(self, unit=None):
        if not unit is None:
            return self.get(properties.Umass, unit=unit)
        
        return self._umass()
    
    def _umass(self):
        return -1.

    def umolar(self, unit=None):
        if not unit is None:
            return self.get(properties.Umolar, unit=unit)
        
        return self._umolar()
    
    def _umolar(self):
        return -1.


    def phase(self, **kwargs):
        return self._phase()
    
    def _phase(self):
        return -1.


    def Tbubble(self, p, unit=None, punit=None):
        if not unit is None:
            return self.get(properties.Tbubble, unit=unit)
                
        return self._Tbubble(p, unit=punit)
    
    def _Tbubble(self, p, unit=None):

        self.update(pairs.PQmolar, p, 0, unit1=unit)

        return self.T()


    def pbubble(self, T, unit=None, Tunit=None):
        if not unit is None:
            return self.get(properties.pbubble, unit=unit)
        
        return self._pbubble(T, unit=Tunit)
    
    def _pbubble(self, T, unit=None):

        self.update(pairs.QmolarT, 0, T, unit1=unit)

        return self.p()


    def Tdew(self, p, unit=None, punit=None):
        if not unit is None:
            return self.get(properties.Tdew, unit=unit)
        
        return self._Tdew(p, unit=punit)
    
    def _Tdew(self, p, unit=None):

        self.update(pairs.PQmolar, p, 1, unit1=unit)

        return self.T()


    def pdew(self, T, unit=None, Tunit=None, **kwargs):
        if not unit is None:
            return self.get(properties.pdew, unit=unit)
        
        return self._pdew(T, unit=Tunit)
    
    def _pdew(self, T, unit=None, **kwargs):

        self.update(pairs.QmolarT, 1, T, unit1=unit)

        return self.p()
        