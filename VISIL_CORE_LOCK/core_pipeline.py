from visil.sigil_adapter import SigilAdapter


class VISILCorePipeline:
    """
    Canonical VISIL execution engine.

    Flow:
    SIGIL → Temporal Kernel → Mode Execution
    """

    def __init__(self):
        self.kernel = VISILTemporalKernel()
        self.sigil = SigilAdapter()

    # -----------------------------
    # SINGLE ENTRY POINT
    # -----------------------------
    def perceive(self, graph, mode="view"):

        # 1. SIGIL normalization layer
        raw_state = self.sigil.load_history(graph)
        state = self.sigil.to_initial_state(raw_state)

        # -----------------------------
        # VIEW MODE (STATIC SNAPSHOT)
        # -----------------------------
        if mode == "view":
            return self.kernel.integrate(state)

        # -----------------------------
        # REPLAY MODE (TEMPORAL PASS)
        # -----------------------------
        elif mode == "replay":
            return self.kernel.integrate(state)

        # -----------------------------
        # FIELD MODE (DYNAMIC SIMULATION)
        # -----------------------------
        elif mode == "field":
            return self.kernel.step_live(state)

        # -----------------------------
        # SAFE FALLBACK
        # -----------------------------
        return self.kernel.integrate(state)
