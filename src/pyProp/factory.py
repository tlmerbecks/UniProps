from .utilities.errors import PackageError
from .packages import PackageFactories

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .pyProp_state import BaseState


def State(state: Any) -> "BaseState":
    r"""
    The factory method for wrapping model instances

    Parameters
    ----------
    state: Any
        The instance of a model

    Returns
    -------
    BaseState

    Raises
    ------
    PackageError
        if no compatible package is found
    """

    for factory in PackageFactories:

        try:
            model = factory(state)
        except PackageError:
            continue

        return model
    
    msg = "No compatible backend was found"
    raise PackageError(msg)