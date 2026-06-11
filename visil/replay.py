import copy
from datetime import datetime


class VISILReplay:

    def __init__(self, snapshots):
        """
        snapshots = list of historical graph states
        """
        self.snapshots = sorted(
            snapshots,
            key=lambda s: s.get("timestamp", "")
        )

    # -------------------------
    # GET STATE AT TIME T
    # -------------------------
    def at_time(self, timestamp):
        target = datetime.fromisoformat(timestamp.replace("Z", ""))

        closest = None

        for snap in self.snapshots:
            ts = snap.get("timestamp")

            if not ts:
                continue

            t = datetime.fromisoformat(ts.replace("Z", ""))

            if t <= target:
                closest = snap
            else:
                break

        return copy.deepcopy(closest) if closest else None

    # -------------------------
    # REPLAY RANGE
    # -------------------------
    def range(self, start, end):
        start_t = datetime.fromisoformat(start.replace("Z", ""))
        end_t = datetime.fromisoformat(end.replace("Z", ""))

        results = []

        for snap in self.snapshots:
            ts = snap.get("timestamp")
            if not ts:
                continue

            t = datetime.fromisoformat(ts.replace("Z", ""))

            if start_t <= t <= end_t:
                results.append(copy.deepcopy(snap))

        return results

    # -------------------------
    # DIFF BETWEEN STATES
    # -------------------------
    def diff(self, a, b):
        a_nodes = set(a.get("graph", {}).get("nodes", {}).keys())
        b_nodes = set(b.get("graph", {}).get("nodes", {}).keys())

        return {
            "added": list(b_nodes - a_nodes),
            "removed": list(a_nodes - b_nodes),
            "stable": list(a_nodes & b_nodes)
        }
