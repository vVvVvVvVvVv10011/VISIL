class AttentionScorer:

    def score_node(self, node, time_factor=1.0, structure_factor=1.0):
        """
        Attention = what VISIL *would focus on* if it were observing.
        """

        base = node.get("weight", 1.0)

        concepts = len(node.get("concepts", []))

        # stability = structural presence
        structure = structure_factor

        # temporal decay = attention shift over time
        time = time_factor

        return (base * 0.6 + concepts * 0.4) * structure * time

    def score_graph(self, graph):
        nodes = graph.get("nodes", {}).values()

        scored = []

        for n in nodes:
            scored.append({
                "id": n.get("id"),
                "attention": self.score_node(n)
            })

        return sorted(scored, key=lambda x: x["attention"], reverse=True)
