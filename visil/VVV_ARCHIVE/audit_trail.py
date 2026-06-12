"""
VISIL Audit Trail

Tracks system behavior over time and detects structural drift.
"""

import json
import time
from datetime import datetime
from pathlib import Path


AUDIT_LOG = Path("visil_audit_log.jsonl")


class VISILAuditTrail:
    def __init__(self):
        self.log_path = AUDIT_LOG

    # -----------------------------
    # LOG PERCEPTION RUN
    # -----------------------------
    def record(self, input_graph, output_view, mode="view"):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "mode": mode,
            "input_signature": self._signature(input_graph),
            "output_signature": self._signature(output_view),
            "node_count": len(output_view.get("view", {})),
        }

        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    # -----------------------------
    # SIMPLE STRUCTURAL HASH
    # -----------------------------
    def _signature(self, data):
        if isinstance(data, dict):
            return {
                "keys": sorted(list(data.keys())),
                "size": len(data),
            }

        return {
            "type": str(type(data)),
            "size": len(str(data)),
        }

    # -----------------------------
    # READ HISTORY
    # -----------------------------
    def load_history(self, limit=50):
        if not self.log_path.exists():
            return []

        with open(self.log_path, "r") as f:
            lines = f.readlines()[-limit:]

        return [json.loads(line) for line in lines]

    # -----------------------------
    # SIMPLE DRIFT DETECTION
    # -----------------------------
    def detect_drift(self):
        history = self.load_history()

        if len(history) < 2:
            return {"drift": "insufficient_data"}

        last = history[-1]
        prev = history[-2]

        drift = {
            "node_change": last["node_count"] - prev["node_count"],
            "mode_shift": last["mode"] != prev["mode"],
        }

        return drift
