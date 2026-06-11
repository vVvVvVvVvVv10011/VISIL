import copy
from datetime import datetime


class VISILReplay:

    def __init__(self, snapshots):
        """
        snapshots = [
            {
                "timestamp": ISO-8601,
                "commit": str,
                "graph": {...}
            }
        ]
        """
        self.snapshots = sorted(
            snapshots,
            key=lambda s: s.get("timestamp", "")
        )

    # -------------------------
    # GET STATE AT TIME
    # -------------------------
    def at_time(self, timestamp):
        target = datetime.fromisoformat(timestamp.replace("Z", ""))

        selected = None

        for snap in self.snapshots:
            ts = snap.get("timestamp")
            if not ts:
                continue

            t = datetime.fromisoformat(ts.replace("Z", ""))

            if t <= target:
                selected = snap
            else:
                break

        return copy.deepcopy(selected)

    # -------------------------
    # RANGE REPLAY
    # -------------------------
    def range(self, start, end):
        start_t = datetime.fromisoformat(start.replace("Z", ""))
        end_t = datetime.fromisoformat(end.replace("Z", ""))

        return [
            copy.deepcopy(s)
            for s in self.snapshots
            if start_t <= datetime.fromisoformat(s["timestamp"].replace("Z", "")) <= end_t
        ]

    # -------------------------
    # GET LATEST STATE
    # -------------------------
    def latest(self):
        return copy.deepcopy(self.snapshots[-1]) if self.snapshots else None

    # -------------------------
    # BASIC DIFF
    # -------------------------
    def diff(self, a, b):
        a_nodes = set(a.get("graph", {}).get("nodes", {}).keys())
        b_nodes = set(b.get("graph", {}).get("nodes", {}).keys())

        return {
            "added": list(b_nodes - a_nodes),
            "removed": list(a_nodes - b_nodes),
            "stable": list(a_nodes & b_nodes)
        }
