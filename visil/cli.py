import sys
import json

from visil.core_pipeline import VISILCorePipeline
from visil.VVV_ARCHIVE.integrity_gate import check_system_integrity


# -------------------------
# UTIL
# -------------------------
def load_graph(path: str) -> dict:
    """
    Loads a VISIL graph from disk.
    """
    with open(path, "r") as f:
        return json.load(f)


# -------------------------
# INTEGRITY GATE (HARD STOP)
# -------------------------
def gate() -> bool:
    """
    VISIL HARD EXECUTION GATE

    Blocks execution if system integrity is invalid.
    This is a REQUIRED precondition for all VISIL operations.
    """

    try:
        result = check_system_integrity()
    except Exception as e:
        print("[VISIL GATE FAILURE] Integrity check crashed:", str(e))
        return False

    if not result:
        print("[VISIL BLOCKED] System integrity validation failed.")
        return False

    return True


# -------------------------
# CORE ENTRYPOINT
# -------------------------
def main():
    args = sys.argv[1:]

    # ALWAYS RUN GATE FIRST
    if not gate():
        return

    # HELP / USAGE
    if len(args) < 2:
        print("""
VISIL CLI (v1.0-core)

USAGE:
  view   <graph.json>
  drift  <graph.json>
  field  <graph.json>

DESCRIPTION:
  view   → structural snapshot of perception graph
  drift  → temporal change analysis across state
  field  → spatial simulation of node relations

ARCHITECTURE RULES:
- Execution is blocked if integrity gate fails
- All computation flows through VISILCorePipeline
- No external mutation outside pipeline contract
- Deterministic output required for all modes
""")
        return

    command = args[0]
    path = args[1]

    # LOAD INPUT
    graph = load_graph(path)

    # PIPELINE INIT
    pipeline = VISILCorePipeline(graph)

    # ROUTING
    if command == "view":
        result = pipeline.run(mode="view")

    elif command == "drift":
        result = pipeline.run(mode="drift")

    elif command == "field":
        result = pipeline.run(mode="field")

    else:
        print(f"[VISIL ERROR] Unknown command: {command}")
        return

    # OUTPUT
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
