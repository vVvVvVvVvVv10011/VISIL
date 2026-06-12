"""
VISIL Structural Lens
Minimal boot-safe lens implementation.
"""

def structural_lens(signal: dict):
    """
    Basic structural perception lens.

    Converts raw signal into node-based view.
    """

    view = {}

    if not isinstance(signal, dict):
        return view

    for key, value in signal.items():
        node_id = str(key)

        view[node_id] = {
            "id": node_id,
            "concepts": _extract(value),
            "attention": 1.0,
            "drift": 0.0,
        }

    return view


def _extract(value):
    """
    Lightweight deterministic concept extraction.
    No NLP dependencies.
    """

    if isinstance(value, str):
        return value.split()[:3]

    if isinstance(value, (list, tuple)):
        return [str(v) for v in value[:3]]

    if isinstance(value, dict):
        return list(value.keys())[:3]

    return [str(value)]
