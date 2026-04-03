from .utilities.errors import PackageError
from .packages import PackageFactories

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .pyProp_state import BaseState


def State(state) -> "BaseState":

    for factory in PackageFactories:

        try:
            model = factory(state)
        except PackageError:
            continue

        return model
    
    msg = "No compatible backend was found"
    raise PackageError(msg)