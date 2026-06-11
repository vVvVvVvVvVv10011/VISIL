class FieldSimulation:

    def __init__(self, nodes, edges):

        self.nodes = nodes
        self.edges = edges

        # initialize state
        self.state = {
            node_id: {
                "attention": node.get("attention", 1.0),
                "drift": node.get("drift", 0.0),
                "velocity": 0.0
            }
            for node_id, node in nodes.items()
        }

    def step(self):

        new_state = {}

        for node_id, state in self.state.items():

            attention = state["attention"]
            drift = state["drift"]
            velocity = state["velocity"]

            # 1. drift pushes instability upward
            drift_force = drift * 0.1

            # 2. attention stabilizes system
            stability_force = attention * 0.05

            # 3. edge coupling (neighbors influence motion)
            edge_force = self._edge_influence(node_id)

            # update velocity (field motion)
            velocity = velocity + drift_force - stability_force + edge_force

            # decay to prevent explosion
            velocity *= 0.92

            # update attention as emergent property
            attention = max(0.1, attention + velocity * 0.05)

            new_state[node_id] = {
                "attention": attention,
                "drift": drift,
                "velocity": velocity
            }

        self.state = new_state
        return self.state

    def _edge_influence(self, node_id):

        influence = 0.0

        for edge in self.edges:

            if edge.get("from") == node_id:
                influence += 0.02

            if edge.get("to") == node_id:
                influence -= 0.01

        return influence
