import json
import sys
from visil.core import VISIL


def load_graph(path):
    with open(path) as f:
        return json.load(f)


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m visil.cli <lens> <graph.json> [threshold]")
        return

    lens = sys.argv[1]
    path = sys.argv[2]

    graph = load_graph(path)
    visil = VISIL(graph)

    if lens == "focus":
        threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        result = visil.view("focus", threshold=threshold)
    else:
        result = visil.view(lens)

    print(json.dumps(result, indent=2))
