"""
VISIL Drift Analyzer

Self-observes VISIL behavior over time using audit logs.
Provides:
- structural drift detection
- trend analysis
- lens influence estimation
- interpretive explanation of system change
"""

import json
from collections import defaultdict


class VISILDriftAnalyzer:
    """
    Reads VISIL audit logs and extracts behavioral drift signals.
    """

    def __init__(self, audit_path="visil_audit_log.jsonl"):
        self.audit_path = audit_path

    # -----------------------------
    # LOAD AUDIT HISTORY
    # -----------------------------
    def load_history(self):
        """
        Loads VISIL audit log entries.
        """
        try:
            with open(self.audit_path, "r") as f:
                return [json.loads(line) for line in f.readlines()]
        except FileNotFoundError:
            return []

    # -----------------------------
    # IMMEDIATE STRUCTURAL DRIFT
    # -----------------------------
    def structural_drift(self):
        """
        Compares last two executions for structural change.
        """
        history = self.load_history()

        if len(history) < 2:
            return {
                "status": "insufficient_data"
            }

        last = history[-1]
        prev = history[-2]

        return {
            "node_delta": last["node_count"] - prev["node_count"],
            "mode_shift": last["mode"] != prev["mode"],
        }

    # -----------------------------
    # LONG-TERM TREND ANALYSIS
    # -----------------------------
    def trend(self):
        """
        Computes long-term structural stability trends.
        """
        history = self.load_history()

        node_counts = [h["node_count"] for h in history]

        if not node_counts:
            return {
                "status": "no_data"
            }

        return {
            "avg_nodes": sum(node_counts) / len(node_counts),
            "min_nodes": min(node_counts),
            "max_nodes": max(node_counts),
        }

    # -----------------------------
    # LENS INFLUENCE ESTIMATION
    # -----------------------------
    def lens_influence(self):
        """
        Estimates how system structure is changing over time.

        NOTE:
        This is a heuristic model — not causal truth.
        """
        history = self.load_history()

        if len(history) < 2:
            return {
                "status": "insufficient_data"
            }

        influence_map = defaultdict(int)

        for i in range(1, len(history)):
            delta = history[i]["node_count"] - history[i - 1]["node_count"]

            if delta > 0:
                influence_map["expansion"] += delta
            elif delta < 0:
                influence_map["compression"] += abs(delta)
            else:
                influence_map["stable"] += 1

        return dict(influence_map)

    # -----------------------------
    # HUMAN INTERPRETATION LAYER
    # -----------------------------
    def interpret(self):
        """
        Converts drift signals into readable system meaning.
        """
        history = self.load_history()

        if len(history) < 2:
            return "Insufficient data for interpretation."

        last = history[-1]
        prev = history[-2]

        delta = last["node_count"] - prev["node_count"]

        if delta > 0:
            return "Perception expanded — VISIL is producing richer structure."
        elif delta < 0:
            return "Perception compressed — VISIL is simplifying structure."
        else:
            return "Perception stable — no structural change detected."

    # -----------------------------
    # FULL REPORT (PUBLIC API)
    # -----------------------------
    def report(self):
        """
        Full system drift report.
        """
        return {
            "structural_drift": self.structural_drift(),
            "trend": self.trend(),
            "lens_influence": self.lens_influence(),
            "interpretation": self.interpret(),
        }
