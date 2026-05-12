from .utilities.errors import PackageError
from .packages import Packages, PackageFactories


from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .UniProps_state import BaseState


class State:
    r"""
    The factory class for wrapping or creating wrapped model instances
    """

    @staticmethod
    def from_instance(instance) -> "BaseState":
        r"""
        The factory method for wrapping model instances

        This should be used if the model instance is complex, e.g. custom Binary
        Interaction Coefficients for mixture constituent pairs 

        Parameters
        ----------
        instance: Any
            The instance of a model, e.g. cp.AbstractState("HEOS", "water")

        Returns
        -------
        BaseState

        Raises
        ------
        PackageError
            if no compatible package is found        
        """

        for factory in PackageFactories.values():
            try:
                state = factory.from_instance(instance)
            except PackageError:
                continue

            return state
        
        msg = "No compatible backend was found"
        raise PackageError(msg)
    
    @staticmethod
    def from_primitives(package : str | Packages, model: str, composition: str | dict, molar: bool =True) -> "BaseState":
        r"""
        The facotry for instantiating and wrapping the model instance

        This can be used for simple models instances that do not require customisation

        Parameters
        ----------
        package: str | Packages
            the package to be used, e.g. coolprop or Packages.COOLPROP
        model: str
            the model to be used, e.g. HEOS or SRK in coolprop
        composition: str | dict
            if str, the name of the component
            if dict, the names and mole fractions of the components
        molar: bool
            whether the fractions specified as part of the composition should 
            be interpreted as mole or mass fractions. Default, mole fractions

        Returrns
        --------
        BaseState

        Raises
        ------
        PackageError
        """
        
        if not isinstance(package, Packages):
            try:
                package = Packages(package)
            except Exception as e:
                msg = f"The specified package \"{package}\" is not supported"
                raise PackageError(msg)

        factory = PackageFactories[package]

        state = factory.from_primitives(model, composition, molar=molar)

        return state
    
