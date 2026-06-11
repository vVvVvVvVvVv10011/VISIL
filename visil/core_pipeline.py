from visil.lenses import VISILLenses
from visil.attention import AttentionEngine
from visil.drift import DriftEngine


class VISILCorePipeline:

    def __init__(self, graph):

        self.graph = graph
        self.lenses = VISILLenses(graph)
        self.attention = AttentionEngine(graph)
        self.drift = DriftEngine(graph)

    # -------------------------
    # MAIN PERCEPTION ENTRY
    # -------------------------
    def perceive(self, mode="focus"):

        nodes = self.graph.get("nodes", {})
        edges = self.graph.get("edges", [])

        view = self.lenses.apply(mode)

        attention_map = self.attention.score(nodes)

        drift_map = self.drift.compute(nodes)

        enriched_nodes = []

        for node_id, node in nodes.items():

            enriched_nodes.append({
                **node,
                "attention": attention_map.get(node_id, 1.0),
                "drift": drift_map.get(node_id, 0.0)
            })

        return {
            "lens": mode,
            "view": {n["id"]: n for n in enriched_nodes},
            "attention": [
                {"id": k, "attention": v}
                for k, v in attention_map.items()
            ],
            "drift": drift_map,
            "edges": edges
        }
