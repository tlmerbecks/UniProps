from typing import TYPE_CHECKING

from .errors import PackageError
from .coolprop import CoolPropFactory
# from .thermopack import thermopackFactory


if TYPE_CHECKING:
    from .base import BaseState


PackageFactories = [
    CoolPropFactory,
    # thermopackFactory,
    ]


def State(state) -> "BaseState":

    for factory in PackageFactories:

        try:
            model = factory(state)
        except PackageError:
            continue

        return model
    
    msg = "No compatible backend was found"
    raise PackageError(msg)