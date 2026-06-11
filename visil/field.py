import math


class VISILField:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    # -------------------------
    # NODE POSITIONING FIELD
    # -------------------------
    def compute_field(self, mode="focus"):

        data = self.pipeline.perceive(mode=mode)

        nodes = data["view"].get("nodes", [])
        attention = data["attention"]

        field = []

        for i, node in enumerate(nodes):

            weight = attention[i] if i < len(attention) else 1.0

            # -------------------------
            # POSITIONAL FIELD (synthetic layout)
            # -------------------------
            angle = (i + 1) * 0.61803398875 * math.pi * 2  # golden ratio spread

            radius = 1.0 / (weight + 0.1)

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius

            field.append({
                "id": node.get("id", str(i)),
                "weight": weight,
                "x": x,
                "y": y,
                "drift": data["drift"]
            })

        return field
