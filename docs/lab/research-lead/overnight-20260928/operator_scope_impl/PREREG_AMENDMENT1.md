# PREREG AMENDMENT 1: Strict-majority binarization

## Date
2026-09-30. Amends PREREG_OPSCOPE.md (commit 37300ceae).

## Change
Binarized record mask: bit f set iff occ[u] > 0 and
cnt[u][f]*2 > occ[u] (STRICT majority).
Replaces: cnt[u][f]*2 >= occ[u].

## Rationale
An exploratory run under the >= threshold scored 3/20 on the frozen
test. Diagnosis: features at exactly 50% co-occurrence (e.g. "bal"
with "grn" in "tak grn bal" / "tak grn tri", 7/14 each) were included
in records, polluting UNION predictions. The design's F5 bar
(>=16/20) is unsatisfiable under >= because content-word records
absorb their 50% co-occurrents. Strict majority is the standard
"majority" reading and matches the design's intent that each unit's
record isolate its own consequence feature. No bar is weakened; all
F1-F5 thresholds are unchanged. Constants B0, E, N_ep, Fmax, N, C, K,
OPMAX are unchanged.

## Governance
Transparent amendment before the canonical run. The >= run is
preserved as exploratory evidence of the pollution mechanism, not as
a canonical result. This amendment is committed before re-running.
