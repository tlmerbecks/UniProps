from enum import Enum


class Packages(Enum):
    COOLPROP = "coolprop"


PackageFactories = {}
# now try to add the factories in turn
try:
    from .coolprop import CoolPropFactory
    PackageFactories[Packages.COOLPROP] = CoolPropFactory
except:
    pass
