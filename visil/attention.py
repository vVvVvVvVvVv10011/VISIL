"""
VISIL Attention Layer

Deterministic salience weighting over VISIL perception output.
No state mutation. No side effects.
"""

def apply_attention(view: dict) -> dict:
    """
    Applies salience weighting to VISIL node structures.

    Expected input:
        {
            "nodes": {...},
            "edges": {...},
            ...
        }

    Returns:
        dict with weighted attention applied
    """

    if not isinstance(view, dict):
        return {"view": view}

    nodes = view.get("nodes", {})
    edges = view.get("edges", {})

    def score_node(node):
        base = node.get("weight", 1.0)

        concepts = node.get("concepts", [])
        concept_boost = len(concepts) * 0.25

        timestamp = node.get("timestamp", None)
        recency_bias = 0.1 if timestamp else 0.0

        return base + concept_boost + recency_bias

    weighted_nodes = {}

    for node_id, node in nodes.items():
        weighted_nodes[node_id] = {
            **node,
            "attention": score_node(node)
        }

    weighted_edges = {}

    for edge_id, edge in edges.items():
        weighted_edges[edge_id] = {
            **edge,
            "attention": edge.get("weight", 1.0)
        }

    return {
        **view,
        "nodes": weighted_nodes,
        "edges": weighted_edges
    }
