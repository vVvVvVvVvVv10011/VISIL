from visil.lenses_structural import structural_lens
from visil.lenses_attention import attention_lens
from visil.lenses_temporal import temporal_lens


# -----------------------------
# IMMUTABLE LENS REGISTRY
# -----------------------------
LENS_REGISTRY = {
    "structural": structural_lens,
    "attention": attention_lens,
    "temporal": temporal_lens,
}


def get_default_lenses():
    """
    Canonical lens set used by VISILCore.
    This is the ONLY approved entry point for lens selection.
    """
    return list(LENS_REGISTRY.values())


def get_lens(name: str):
    """
    Safe lookup. No dynamic execution allowed.
    """
    if name not in LENS_REGISTRY:
        raise ValueError(f"Unknown VISIL lens: {name}")

    return LENS_REGISTRY[name]


def list_lenses():
    return list(LENS_REGISTRY.keys())
