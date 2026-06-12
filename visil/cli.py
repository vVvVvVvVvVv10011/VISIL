import sys
import json
from visil.core_pipeline import VISILCorePipeline


def load_graph(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        print("VISIL commands:")
        print("  visil view <graph.json>")
        print("  visil replay <graph.json>")
        print("  visil field <graph.json>")
        print("  visil drift <graph.json>")
        return

    command = args[0]
    graph_path = args[1] if len(args) > 1 else None

    # SAFE DEFAULT
    if not graph_path:
        print("Missing graph.json")
        return

    graph = load_graph(graph_path)
    pipeline = VISILCorePipeline()

    if command == "view":
        result = pipeline.perceive(graph, mode="view")

    elif command == "replay":
        result = pipeline.perceive(graph, mode="replay")

    elif command == "field":
        result = pipeline.perceive(graph, mode="field")

    elif command == "drift":
        result = pipeline.perceive(graph, mode="drift")

    else:
        print(f"Unknown command: {command}")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
