import json
import sys


# -------------------------
# LOAD GRAPH
# -------------------------
def load_graph(path):
    with open(path, "r") as f:
        return json.load(f)


# -------------------------
# MAIN ENTRY
# -------------------------
def main():

    if len(sys.argv) < 2:

        print("""
VISIL CLI

COMMANDS:
  view   <graph.json>      → run VISIL perception lens
  replay <snapshots.json>  → reconstruct historical states
  sigil  <event.json>      → commit event into Git history

RULE:
  VISIL is read-only except SIGIL write gate
""")
        return

    mode = sys.argv[1]

    # -------------------------
    # VIEW MODE (READ ONLY)
    # -------------------------
    if mode == "view":

        if len(sys.argv) < 3:
            print("Usage: view <graph.json>")
            return

        from visil.engine import VISILEngine

        graph = load_graph(sys.argv[2])

        engine = VISILEngine(graph)

        result = engine.view()

        print(json.dumps(result, indent=2))
        return

    # -------------------------
    # REPLAY MODE (READ ONLY)
    # -------------------------
    if mode == "replay":

        if len(sys.argv) < 3:
            print("Usage: replay <snapshots.json>")
            return

        from visil.replay import VISILReplay

        snapshots = load_graph(sys.argv[2])

        replay = VISILReplay(snapshots)

        latest = replay.latest()

        print(json.dumps(latest, indent=2))
        return

    # -------------------------
    # SIGIL MODE (WRITE GATE)
    # -------------------------
    if mode == "sigil":

        if len(sys.argv) < 3:
            print("Usage: sigil <event.json>")
            return

        from visil.sigil_git import SigilGitBinder

        binder = SigilGitBinder(".")

        with open(sys.argv[2], "r") as f:
            event = json.load(f)

        result = binder.process_event(event)

        print("SIGIL committed:", event.get("id"))
        return

    # -------------------------
    # UNKNOWN MODE
    # -------------------------
    print("Unknown command:", mode)


if __name__ == "__main__":
    main()
