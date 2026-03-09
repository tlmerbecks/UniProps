from .errors import PackageError
from . import PackageFactories
from .base import BaseState

def State(state) -> BaseState:

    for factory in PackageFactories:

        try:
            model = factory(state)
        except PackageError:
            continue

        return model
    
    msg = "No compatible backend was found"
    raise PackageError(msg)