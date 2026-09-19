# LH-6 — BLOCKED_ON_STABILITY

**Agent:** E3 · **Date:** 2026-09-19

LH-6 (scaled 4×4 learner core, `r34v4_learner_core.zag`) was **not built**,
per the preregistered gate: "runs only if LH-1/LH-2 show stable learning."

Stability evidence checked and found missing:
- `variants/LH-1/RESULT.md` — does not exist.
- `variants/LH-2/RESULT.md` — does not exist.
- `find ~/workspace/tnn-lab -name RESULT.md` — zero results anywhere.

No sibling stability result exists to clear the gate. In addition, the
LH-5 reward-corruption ramp (same agent, same session) found the 2×2
delayed-credit learner is fragile at 10% reward corruption (spurious
context switches → 0/16 block collapses) — the kind of instability the
gate exists to catch.

**Unblock condition:** LH-1 and LH-2 publish RESULT.md showing stable
learning at horizon; then LH-6 may proceed with the new named learner
core and the same isolation check. Full rationale in
`variants/LH-5/RESULT.md`.
