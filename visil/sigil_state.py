import json
import subprocess
from visil.core_pipeline import VISILCorePipeline


class SigilStateExtractor:

    def __init__(self, repo_path="."):
        self.repo_path = repo_path

    # -------------------------
    # EXTRACT VISIL STATE
    # -------------------------
    def extract(self, graph):

        pipeline = VISILCorePipeline(graph)

        perception = pipeline.perceive(mode="focus")

        return {
            "graph_hash": self._hash_graph(graph),
            "attention": perception.get("attention"),
            "drift": perception.get("drift"),
            "view": perception.get("view")
        }

    # -------------------------
    # SIMPLE HASH (STABILITY KEY)
    # -------------------------
    def _hash_graph(self, graph):

        raw = json.dumps(graph, sort_keys=True)

        return str(hash(raw))

    # -------------------------
    # BUILD COMMIT MESSAGE
    # -------------------------
    def build_commit_message(self, graph, base_msg="VISIL update"):

        state = self.extract(graph)

        summary = {
            "graph_hash": state["graph_hash"],
            "attention_mean": sum([a.get("attention", 0) for a in state["attention"]]) if state["attention"] else 0,
            "drift": state["drift"]
        }

        return f"{base_msg} | SIGIL:{json.dumps(summary)}"
