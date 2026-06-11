class EventCompressor:

    def compress(self, events):
        """
        Groups identical structural operations
        without altering semantic meaning.
        """

        buckets = {}

        for e in events:
            key = f"{e.get('type')}::{e.get('node', {}).get('id') or e.get('edge', {}).get('from')}"

            if key not in buckets:
                buckets[key] = []

            buckets[key].append(e)

        compressed = []

        for k, group in buckets.items():
            compressed.append({
                "group": k,
                "count": len(group),
                "events": group,
                "compressed": True
            })

        return compressed
