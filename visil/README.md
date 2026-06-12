VISIL — Developer Internal Spec

Virtual Isolated Signal Illumination Layer

⚠️ CLASSIFICATION

Internal system documentation. Not intended for public release.

---

1. System Truth

VISIL is a multi-lens perception engine embedded within ATRIUM.

Its purpose is not storage, execution, or reasoning.

Its purpose is:

«transform signal into structured perception under attention constraints»

---

2. Canonical Execution Model

signal
  ↓
lens execution (parallel)
  ↓
output merge
  ↓
attention weighting
  ↓
normalized view

---

3. Core Invariant

VISIL = f(signal) → attention-weighted structure

This invariant must hold for all system states.

Any modification that violates this relationship is a breaking change, not a refactor.

---

4. Lens System Contract

4.1 Lens Definition

A lens is a pure function:

lens(signal: dict) -> dict[node_id, attributes]

Hard constraints:

- no side effects
- no external I/O
- deterministic output for identical input
- no global state mutation

---

4.2 Lens Registry Rules

Defined in:

lens_registry.py

Rules:

- registry is static at runtime
- no dynamic registration after initialization
- lens order is semantically meaningful
- registry output must be immutable (tuple preferred)

---

4.3 Allowed Lens Types

Structural Lens

- topology extraction
- entity relationships
- static graph interpretation

Attention Lens

- salience weighting
- importance scoring
- focus modulation

Temporal Lens

- delta detection
- sequence interpretation
- change over time modeling

---

5. Core Pipeline Contract

Defined in:

core_pipeline.py

Responsibilities:

1. load lenses from registry
2. execute lenses independently
3. merge outputs deterministically
4. apply attention weighting
5. return normalized view object

---

Merge Rules

Numeric fields:

avg(a, b)

Non-numeric fields:

overwrite(b)

---

6. Attention System Contract

Defined in:

attention.py

Rules:

- attention modifies structure, not raw signal
- attention must be deterministic per run
- no external memory injection allowed

---

7. Drift System

Defined in:

drift.py

Purpose:

- detect structural change across time
- quantify stability of perception graph

Drift is defined as:

«comparison of successive VISIL outputs»

---

8. Field System

Defined in:

field.py  
field_sim.py  
field_renderer.py

Purpose:

- represent node relationships as dynamic space
- simulate structural interaction
- render perception geometry

Field is an interpretation layer, not storage.

---

9. CLI Contract

Defined in:

cli.py

Modes:

- view → static perception snapshot
- drift → change analysis
- field → spatial interpretation

The CLI must never modify core state.

---

10. Archive Policy (NON-CORE MODULES)

Non-core modules exist as historical or experimental state.

Rules:

- non-core code must not be imported by core pipeline
- non-core code must not define lenses
- non-core code must not affect runtime perception

---

11. Mutation Rules

Forbidden:

- runtime lens modification
- dynamic registry injection
- attention override from external modules
- silent fallback behavior

Required:

- explicit failure on missing components
- deterministic execution
- full traceability of lens output

---

12. System Integrity Model

VISIL assumes:

- single trusted operator
- local execution environment
- deterministic runtime behavior

No multi-user permission layer exists.

Security is structural, not authentication-based.

---

13. Failure Behavior

System must:

- fail loudly on missing modules
- avoid silent degradation
- never approximate missing lenses

---

14. Versioning Philosophy

VISIL is not versioned by features.

It is versioned by changes to:

- lens behavior
- attention weighting
- merge logic
- perception model

Everything else is non-breaking.

---

15. Mental Model

VISIL is:

«a lens stack applied to a signal field that collapses into structured perception»

Not a pipeline.
Not a toolchain.
A controlled perception manifold.

---

END OF INTERNAL SPEC
