from abc import ABC, abstractmethod
import json


# =========================================================
# BASE CONTRACT
# =========================================================

class VISILFieldRenderer(ABC):

    @abstractmethod
    def render(self, field_json):
        """
        Takes a VISIL Field JSON object and renders it.

        Contract:
        - MUST NOT mutate input
        - MUST NOT depend on core logic
        - MUST treat input as immutable perception snapshot
        """
        pass


# =========================================================
# CLI IMPLEMENTATION (DEFAULT LENS)
# =========================================================

class CLIFIELDRenderer(VISILFieldRenderer):

    def render(self, field_json):

        print("\n====================")
        print("   VISIL FIELD VIEW")
        print("====================\n")

        nodes = field_json.get("nodes", [])
        edges = field_json.get("edges", [])
        field = field_json.get("field", {})

        # -------------------------
        # NODE LAYER
        # -------------------------
        print("NODES:\n")

        for node in nodes:

            print(
                f"- ID: {node.get('id')} | "
                f"POS: ({node.get('x'):.2f}, {node.get('y'):.2f}) | "
                f"W: {node.get('weight', 0):.2f} | "
                f"A: {node.get('attention', 0):.2f} | "
                f"D: {node.get('drift', 0):.2f} | "
                f"C: {node.get('concepts', [])}"
            )

        # -------------------------
        # EDGE LAYER
        # -------------------------
        print("\nEDGES:\n")

        for edge in edges:

            print(
                f"- {edge.get('from')} → {edge.get('to')} | "
                f"strength={edge.get('strength', 0):.2f}"
            )

        # -------------------------
        # FIELD SUMMARY
        # -------------------------
        print("\nFIELD SUMMARY:\n")

        print(json.dumps(field, indent=2))

        print("\n====================\n")


# =========================================================
# JSON EXPORT RENDERER (FOR PIPELINES / REPLAY / GIT)
# =========================================================

class JSONFieldRenderer(VISILFieldRenderer):

    def render(self, field_json):
        """
        Pure passthrough renderer for logging, replay, or Git binding.
        """

        return json.dumps(field_json, indent=2)


# =========================================================
# SAFE FACTORY
# =========================================================

def get_renderer(mode="cli"):
    """
    Returns appropriate renderer based on output target.
    """

    if mode == "json":
        return JSONFieldRenderer()

    return CLIFIELDRenderer()
