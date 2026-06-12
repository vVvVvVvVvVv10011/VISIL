class AttentionEngine:
    """
    VISIL Attention Layer
    Converts node structure into salience weights.
    """

    def __init__(self, graph):
        self.graph = graph

    def score(self, nodes):
        """
        Returns:
            dict[node_id] -> float attention score
        """

        scores = {}

        for node_id, node in nodes.items():

            base = node.get("weight", 1.0)

            concepts = node.get("concepts", [])
            concept_boost = len(concepts) * 0.25

            timestamp = node.get("timestamp", "")
            recency_bias = 0.1 if timestamp else 0.0

            scores[node_id] = base + concept_boost + recency_bias

        return scores
