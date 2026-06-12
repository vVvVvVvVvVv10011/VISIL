"""
VISIL Attention Lens
Minimal placeholder lens for salience weighting.
"""

def attention_lens(signal: dict):
    view = {}

    if not isinstance(signal, dict):
        return view

    for key, value in signal.items():
        node_id = str(key)

        view[node_id] = {
            "id": node_id,
            "attention": 1.2,  # slight salience boost
            "concepts": _extract(value),
            "drift": 0.0,
        }

    return view


def _extract(value):
    if isinstance(value, str):
        return value.split()[:3]
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value[:3]]
    if isinstance(value, dict):
        return list(value.keys())[:3]
    return [str(value)]
