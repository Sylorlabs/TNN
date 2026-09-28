# Superseded artifacts — field-index bug (2026-09-24)

These artifacts were produced by trainer binaries whose TSV parser read
feature columns (f2..f8, garbage) instead of the preregistered (f1..f8):
`src/train.zag` and `src/gate.zag` used `tabs[7+k]`/`tabs[8+k]` (0-based
fields 8..15) instead of `tabs[6+k]`/`tabs[7+k]` (fields 7..14).

The bug was documented in VERDICT.md ("Layer 1") and CONFIRMED empirically:
with the fixed parser, a Python replication of epoch 0 (phase 0) matches the
binary exactly (loss 413952921, gviol 14, b −776); the buggy binary logged
epoch-0 loss 3393284222 — a different feature stream.

All artifacts here are SUPERSEDED. The canonical results were regenerated
from the fixed sources; see VERDICT_TRAINING.md.
