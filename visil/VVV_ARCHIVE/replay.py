from visil.core_pipeline import VISILCorePipeline


class VISILReplay:

    def __init__(self, snapshots):
        self.snapshots = self.normalize(snapshots)

    # -------------------------
    # NORMALIZATION LAYER
    # -------------------------
    def normalize(self, data):

        # CASE 1: already list of snapshots
        if isinstance(data, list):
            return data

        # CASE 2: dict of nodes (your current format)
        if isinstance(data, dict):

            # convert graph into single snapshot
            return [{
                "timestamp": "latest",
                "graph": data
            }]

        return []

    # -------------------------
    # PIPELINE OVER TIME
    # -------------------------
    def run(self, mode="focus"):

        results = []

        for snap in self.snapshots:

            # SAFE EXTRACTION
            graph = snap.get("graph") or snap

            pipeline = VISILCorePipeline(graph)

            output = pipeline.perceive(mode=mode)

            results.append({
                "timestamp": snap.get("timestamp", "unknown"),
                "output": output
            })

        return results

    # -------------------------
    # LATEST ONLY
    # -------------------------
    def latest(self, mode="focus"):

        if not self.snapshots:
            return {}

        last = self.snapshots[-1]

        graph = last.get("graph") or last

        pipeline = VISILCorePipeline(graph)

        return pipeline.perceive(mode=mode)
