from collections import defaultdict


class ConceptDrift:

    def score(self, snapshots):
        """
        Measures how concepts evolve over time.
        """

        timeline = []

        for snap in snapshots:
            concepts = set()

            for node in snap.get("graph", {}).get("nodes", {}).values():
                concepts.update(node.get("concepts", []))

            timeline.append({
                "timestamp": snap.get("timestamp"),
                "concepts": concepts
            })

        drift_scores = []

        for i in range(1, len(timeline)):
            prev = timeline[i - 1]["concepts"]
            curr = timeline[i]["concepts"]

            added = len(curr - prev)
            removed = len(prev - curr)

            drift_scores.append({
                "timestamp": timeline[i]["timestamp"],
                "drift": added + removed
            })

        return drift_scores
