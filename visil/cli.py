import json
import sys


# -------------------------
# UTIL
# -------------------------
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


# -------------------------
# ENTRY
# -------------------------
def main():

    if len(sys.argv) < 2:

        print("""
VISIL CLI (Unified Cognitive Interface)

USAGE:

  view   <graph.json>
  replay <graph_or_snapshots.json>
  field  <graph.json> [mode]
  sigil  <event.json> <graph.json>

MODES:
  focus | time | concept | structure

NOTES:
- All operations go through VISILCorePipeline
- Replay is unified perception over time/state
- Field is spatial projection of attention
- Sigil binds cognition state into Git commits
""")
        return

    command = sys.argv[1]

    # -------------------------
    # VIEW MODE
    # -------------------------
    if command == "view":

        from visil.core_pipeline import VISILCorePipeline

        if len(sys.argv) < 3:
            print("Usage: view <graph.json>")
            return

        graph = load_json(sys.argv[2])

        pipeline = VISILCorePipeline(graph)

        result = pipeline.perceive(mode="focus")

        print(json.dumps(result, indent=2))
        return

    # -------------------------
    # REPLAY MODE
    # -------------------------
    if command == "replay":

        from visil.replay import VISILReplay

        if len(sys.argv) < 3:
            print("Usage: replay <graph_or_snapshots.json>")
            return

        data = load_json(sys.argv[2])

        replay = VISILReplay(data)

        result = replay.run(mode="focus")

        print(json.dumps(result, indent=2))
        return

    # -------------------------
    # FIELD MODE (SPATIAL LENS)
    # -------------------------
    if command == "field":

        from visil.core_pipeline import VISILCorePipeline
        from visil.field import VISILField

        if len(sys.argv) < 3:
            print("Usage: field <graph.json> [mode]")
            return

        graph = load_json(sys.argv[2])

        pipeline = VISILCorePipeline(graph)

        field = VISILField(pipeline)

        mode = sys.argv[3] if len(sys.argv) > 3 else "focus"

        result = field.compute_field(mode=mode)

        print(json.dumps(result, indent=2))
        return

    # -------------------------
    # SIGIL MODE (GIT BINDING)
    # -------------------------
    if command == "sigil":

        from visil.sigil_git import SigilGitBinder

        if len(sys.argv) < 4:
            print("Usage: sigil <event.json> <graph.json>")
            return

        event = load_json(sys.argv[2])
        graph = load_json(sys.argv[3])

        binder = SigilGitBinder(".")

        result = binder.process_event(event, graph)

        print("SIGIL committed:", result)
        return

    # -------------------------
    # UNKNOWN COMMAND
    # -------------------------
    print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
