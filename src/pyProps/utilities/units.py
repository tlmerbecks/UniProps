import pint

ureg = pint.UnitRegistry()
ureg.define("m3 = m ** 3")
ureg.define("m2 = m ** 2")

_Q = ureg.Quantity  # type: ignore

def convert_to_SI(val: float, unit: str) -> float:
    val_unit = _Q(val, unit)

    val_SI = val_unit.to_base_units()

    return val_SI.magnitude

def convert_from_SI(val_SI: float, unit: str) -> float:

    _val = _Q(1, unit)

    unit_SI = _val.to_base_units().units

    val_SI_unit_SI = ureg(f"{val_SI} {unit_SI}")

    val = val_SI_unit_SI.to(unit)

    return val.magnitude
