from visil.lens_registry import get_default_lenses
from visil.attention import apply_attention


class VISILCorePipeline:
    """
    VISIL Core Perception Pipeline

    Flow:
        signal → lenses → merge → attention → view
    """

    def perceive(self, signal: dict, mode: str = "view", lenses=None) -> dict:
        """
        Main perception entrypoint.

        Args:
            signal: input graph or event state
            mode: view | replay | field | drift
            lenses: optional override lens set
        """

        if lenses is None:
            lenses = get_default_lenses()

        view = {}

        for lens in lenses:
            output = lens(signal)

            # each lens returns {node_id: data}
            for node_id, data in output.items():
                if node_id not in view:
                    view[node_id] = data
                else:
                    view[node_id] = self._merge(view[node_id], data)

        return {
            "mode": mode,
            "view": apply_attention(view)
        }

    def _merge(self, a: dict, b: dict) -> dict:
        """
        Merge lens outputs deterministically.
        Numeric values are averaged.
        Non-numeric values override.
        """

        merged = dict(a)

        for k, v in b.items():
            if isinstance(v, (int, float)):
                merged[k] = (merged.get(k, 0) + v) / 2
            else:
                merged[k] = v

        return merged
