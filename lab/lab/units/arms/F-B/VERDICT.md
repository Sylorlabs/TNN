# VERDICT — Arm F-B (Branching-continuation cuts), Track A

**Date:** 2026-09-21
**Arm:** F-B — Branching-continuation cuts (CUT family)
**Adjudicated by:** crew U5 (marathon)
**Verdict:** **KILLED** (frozen kill disjunct 2 fires: within noise of F-S)

## Frozen kill criterion (verbatim, PREREG_FREEZE.md §3, line 483)

> **M3 < C-W's both corpora; OR within noise of F-S on all metrics both corpora
> — redundant arm, keep F-S, retire F-B.**

"Within noise" operationalization (documented): absolute difference < 0.5
percentage points (tight epsilon for deterministic zero-RNG system).

## Kill-criterion evaluation

### Disjunct 1: M3 < C-W's — DOES NOT FIRE

| Arm | M3 survival | M3 fresh recall |
|-----|-------------|-----------------|
| C-W | 100.0 | 100.0 |
| F-B | 100.0 | 100.0 |

100.0 < 100.0 is FALSE. Disjunct 1 does not fire.

Note on "both corpora": C-W exposes a single combined M3 (not per-corpus).
F-B's M3 is also combined (1000 valuable across both corpora). The mechanical
reading (F-B_M3 < C-W_M3) is applied; the ambiguity is documented.

### Disjunct 2: Within noise of F-S on all metrics — FIRES

| Metric | F-S | F-B | Δ | Within noise? |
|--------|-----|-----|---|---------------|
| M1 recall (prose) | 100.0 | 100.0 | 0.0 | YES |
| M1 recall (code) | 100.0 | 100.0 | 0.0 | YES |
| M1 boundary (prose) | 100.0 | 100.0 | 0.0 | YES |
| M1 boundary (code) | 100.0 | 100.0 | 0.0 | YES |
| M2 final (t1/t2/t3) | 100.0 | 100.0 | 0.0 | YES |
| M3 survival | 100.0 | 100.0 | 0.0 | YES |
| M3 fresh recall | 100.0 | 100.0 | 0.0 | YES |
| M4 rev (prose) | 100.0 | 100.0 | 0.0 | YES |
| M4 rev (code) | 100.0 | 100.0 | 0.0 | YES |
| M6 tax (p2c) | 0.0 | 0.0 | 0.0 | YES |
| M6 tax (c2p) | 0.0 | 0.0 | 0.0 | YES |

All capability metrics are within noise. **Disjunct 2 FIRES → KILLED.**

**On M5:** F-S did not report M5; F-B FAILs (18.2× per-byte, 568 entries/KB
vs 1.5× / 10/KB bars). The "all metrics" condition is evaluated on capability
metrics (M1-M4, M6) where comparator data exists. M5 is a cost metric, scored
separately; it does not block the kill.

**On M7:** F-B is N/A (dedup probe); F-S reported 50.0/100.0. Not a kill-relevant
capability metric.

**On chunk counts:** F-S prose 211 chunks; F-B prose 4,402,039 chunks (20,000×).
Vast mechanistic difference, but "metrics" in the kill criterion refers to
M-scores, not descriptive statistics. The cost manifests in M5 (FAIL). F-B is
not the "cheaper sibling" — it is a more expensive way to achieve the same
scores. Documented; does not block the kill.

## Scorecard (1x) — summary

| Mode | Key result |
|------|------------|
| m1-1x-prose | recall 100.0, boundary 100.0, 4,402,039 units |
| m1-1x-code | recall 100.0, boundary 100.0, 5,287,970 units |
| m2-t1/t2/t3 | final 100.0/100.0, 1 episode, fast-then-flat |
| m3-1x | survival 100.0, fresh 100.0, mgmt 8050, weaken 50 |
| m4-1x-prose | rev 100.0/100.0, killsub 0 |
| m4-1x-code | rev 100.0/100.0, killsub 0 |
| m5-1x | 1000 units, 18.2× per-byte (FAIL), 568/KB (FAIL) |
| m6-p2c-1x | rec 100.0, tax 0.0, memorizer 0/ok |
| m6-c2p-1x | rec 100.0, tax 0.0, memorizer 0/ok |
| m7-1x | N/A (dedup probe) |
| m8-1x | Gate running; compact workload (see deviations) |

Full scorecard: `docs/scorecard_r1_1x.json` (15 modes).

## Binding verdict

**KILLED.** Frozen disjunct 2 fires: F-B is within noise of F-S on all
capability metrics (M1, M2, M3, M4, M6). Per the frozen criterion: "redundant
arm, keep F-S, retire F-B."

The arm is retired. F-S is kept.

## M8 gate (N=5 × 2 reruns)

**Result: PASS** (2026-09-22 01:20 UTC)

All 10 runs completed (rc=0). stdout.txt byte-identical across all 5
perturbations (clean, frag, aslr, starve, freelist) × 2 reruns.

Note: M8 uses compact workload (t1 corpora + 100-valuable/1000-step M3),
not full M1 prose + M1 code + full M3. Documented as declared deviation.
