"""
VISIL Integrity Gate

Prevents architectural drift by enforcing system boundaries at runtime.
"""

import importlib
import sys


# -----------------------------
# FORBIDDEN SYSTEMS
# -----------------------------
FORBIDDEN_IMPORTS = {
    "visil.field",
    "visil.field_sim",
    "visil.field_renderer",
    "visil.temporal_kernel",
    "visil.sigil_state",
    "visil.sigil_git",
    "visil.state_model",
    "visil.replay",
    "visil.git_replay",
    "visil.event_compress",
}


class VISILIntegrityError(Exception):
    pass


def check_imports():
    """
    Scan loaded modules and block forbidden architectural contamination.
    """
    for mod in list(sys.modules.keys()):
        if mod in FORBIDDEN_IMPORTS:
            raise VISILIntegrityError(
                f"VISIL integrity violation: forbidden module loaded -> {mod}"
            )


def safe_import(module_name: str):
    """
    Controlled import gate for VISIL runtime.
    """
    if module_name in FORBIDDEN_IMPORTS:
        raise VISILIntegrityError(
            f"Blocked import attempt: {module_name}"
        )

    return importlib.import_module(module_name)


def validate_runtime(core_lock_signature: dict, runtime_signature: dict):
    """
    Compares active VISIL behavior to CORE_LOCK reference.

    This is your drift detector.
    """
    drift_keys = []

    for k in core_lock_signature:
        if k not in runtime_signature:
            drift_keys.append(k)

        elif type(core_lock_signature[k]) != type(runtime_signature[k]):
            drift_keys.append(k)

    if drift_keys:
        raise VISILIntegrityError(
            f"VISIL drift detected in keys: {drift_keys}"
        )

    return True
