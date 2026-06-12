import inspect
import types

class LensViolation(Exception):
    pass


def enforce_lens_purity(lens_fn):
    """
    Wraps a lens and enforces structural purity constraints.
    """

    def wrapper(signal):
        _validate_callable(lens_fn)
        _validate_no_side_effects(lens_fn)

        result = lens_fn(signal)

        _validate_output(result)

        return result

    return wrapper


def _validate_callable(fn):
    if not callable(fn):
        raise LensViolation("Lens is not callable")


def _validate_no_side_effects(fn):
    src = inspect.getsource(fn)

    forbidden = [
        "open(",
        "write(",
        "import os",
        "import sys",
        "subprocess",
        "setattr",
        "__dict__",
    ]

    for f in forbidden:
        if f in src:
            raise LensViolation(f"Forbidden operation detected in lens: {f}")


def _validate_output(output):
    if not isinstance(output, dict):
        raise LensViolation("Lens output must be dict[node_id -> attributes]")
