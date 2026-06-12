"""
VISIL Temporal Lens
Minimal placeholder for time-aware perception.
"""

def temporal_lens(signal: dict):
    view = {}

    if not isinstance(signal, dict):
        return view

    for key, value in signal.items():
        node_id = str(key)

        view[node_id] = {
            "id": node_id,
            "concepts": _extract(value),
            "attention": 1.0,
            "drift": 0.1,  # slight temporal bias
            "timestamped": True
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
