import sys
import json
from visil.core_pipeline import VISILCorePipeline


# -------------------------
# UTIL
# -------------------------
def load_graph(path):
    with open(path, "r") as f:
        return json.load(f)


# -------------------------
# ENTRY
# -------------------------
def main():
    args = sys.argv[1:]

    if len(args) < 2:
        print("""
VISIL CLI (v1.0-core)

USAGE:
  view   <graph.json>
  drift  <graph.json>
  field  <graph.json>

MODES:
  view   → structural snapshot
  drift  → temporal change analysis
  field  → spatial projection

NOTES:
- All operations route through VISILCorePipeline
- No mutation of graph state occurs
- Output is deterministic per lens stack
""")
        return

    command = args[0]
    path = args[1]

    graph = load_graph(path)
    pipeline = VISILCorePipeline(graph)

    if command == "view":
        result = pipeline.run(mode="view")
    elif command == "drift":
        result = pipeline.run(mode="drift")
    elif command == "field":
        result = pipeline.run(mode="field")
    else:
        print(f"Unknown command: {command}")
        return

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
