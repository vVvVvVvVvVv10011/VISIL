import json
import subprocess
from datetime import datetime


class SigilGitBinder:

    def __init__(self, repo_path="."):
        self.repo_path = repo_path

    # -------------------------
    # APPLY EVENT TO GRAPH
    # -------------------------
    def apply_event(self, graph, event):
        etype = event.get("type")

        if etype == "add":
            node = event.get("node")
            if node and "id" in node:
                graph["nodes"][node["id"]] = node

        elif etype == "update":
            node = event.get("node")
            if node and "id" in node:
                existing = graph["nodes"].get(node["id"], {})
                existing.update(node)
                graph["nodes"][node["id"]] = existing

        elif etype == "connect":
            edge = event.get("edge")
            if edge:
                graph["edges"].append(edge)

        return graph

    # -------------------------
    # COMMIT GRAPH STATE
    # -------------------------
    def commit_graph(self, message):
        subprocess.run(["git", "add", "graph.json"], cwd=self.repo_path)

        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.repo_path
        )

    # -------------------------
    # EVENT → COMMIT PIPELINE
    # -------------------------
    def process_event(self, event):
        with open("graph.json", "r") as f:
            graph = json.load(f)

        graph = self.apply_event(graph, event)

        with open("graph.json", "w") as f:
            json.dump(graph, f, indent=2)

        msg = f"SIGIL event {event.get('id')} @ {event.get('timestamp')}"

        self.commit_graph(msg)

        return graph
