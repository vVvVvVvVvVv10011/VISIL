"""
VISIL Attention Layer

Applies salience weighting to perception output.
"""

def apply_attention(view: dict) -> dict:
    """
    Normalizes and weights node attention values.
    """

    if not isinstance(view, dict):
        return {"view": {}}

    weighted = {}

    for node_id, data in view.items():

        attention = data.get("attention", 1.0)

        # clamp attention (stability constraint)
        attention = max(0.1, min(attention, 2.0))

        weighted[node_id] = {
            **data,
            "attention": attention,
        }

    return weighted
