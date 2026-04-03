PackageFactories = []
# now try to add the factories in turn
try:
    from .coolprop import CoolPropFactory
    PackageFactories.append(CoolPropFactory)
except:
    pass

try:
    from .thermopack import thermopackFactory  
    PackageFactories.append(thermopackFactory)
except:
    pass