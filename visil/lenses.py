class VISILLenses:

    def __init__(self, graph):
        self.graph = graph

    # REQUIRED CONTRACT
    def apply(self, mode="focus"):

        nodes = self.graph.get("nodes", {})

        return {
            "focus": self._focus(nodes),
            "time": self._time(nodes),
            "concept": self._concept(nodes)
        }.get(mode, self._focus(nodes))

    # FIELD PERCEPTION LAYER (CORE)
    def _focus(self, nodes):

        return {
            k: v for k, v in nodes.items()
        }

    def _time(self, nodes):

        return sorted(nodes.values(), key=lambda n: n.get("timestamp", ""))

    def _concept(self, nodes):

        out = {}

        for n in nodes.values():
            for c in n.get("concepts", []):
                out.setdefault(c, []).append(n)

        return out
