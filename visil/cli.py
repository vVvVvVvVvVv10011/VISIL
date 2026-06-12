import sys
import json
from visil.core_pipeline import VISILCorePipeline


def load_graph(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python -m visil.cli view <graph.json>")
        print("  python -m visil.cli replay <graph.json>")
        print("  python -m visil.cli field <graph.json>")
        return

    command = sys.argv[1]
    graph_path = sys.argv[2]

    graph = load_graph(graph_path)
    pipeline = VISILCorePipeline()

    if command == "view":
        result = pipeline.perceive(graph, mode="view")

    elif command == "replay":
        result = pipeline.perceive(graph, mode="replay")

    elif command == "field":
        result = pipeline.perceive(graph, mode="field")

    else:
        print(f"Unknown command: {command}")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
