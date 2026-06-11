class DriftEngine:
    """
    VISIL Drift Layer
    Measures structural instability over time.
    """

    def __init__(self, graph):
        self.graph = graph

    def compute(self, nodes):
        """
        Returns:
            dict[node_id] -> float drift score
        """

        drift = {}

        for node_id, node in nodes.items():

            timestamp = node.get("timestamp", "")
            concepts = node.get("concepts", [])

            # base instability
            time_factor = len(timestamp) * 0.01

            # semantic volatility
            concept_factor = abs(len(concepts) - 2) * 0.15

            # missing structure penalty
            missing = 0.2 if not concepts else 0.0

            drift[node_id] = time_factor + concept_factor + missing

        return drift
