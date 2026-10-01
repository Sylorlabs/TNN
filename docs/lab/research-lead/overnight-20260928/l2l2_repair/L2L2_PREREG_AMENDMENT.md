# L2L2 Prereg Amendment: Mode 2 Causal Ablation

**Status: PREREGISTRATION AMENDMENT.** Frozen before implementation of mode 2.
Amends prereg `4b4c8c345` (PREREG_L2L2.md). Does not modify the original prereg.

## Background

Audit `af9a9765a` found P3 CAUSAL ABLATION was not performed as specified. The
original prereg required "run B with trusted=0, offset_hyp=unknown" (retained state,
specific component zeroed). The committed code has no such run; mode 1 is the fresh
control misdescribed as an ablation. Honest standing: P3 NOT-PERFORMED.

## Amendment: Mode 2

Add mode 2 to the learner: run family B with A's retained state EXCEPT the
transferred component forced to zero.

### Precise specification

After family A completes (offset kA=3, x in 1..20):

- Retain: the mem table buffer `mx` (shared, as in mode 0), `offset_hyp` and
  `trusted` copied from post-A state.
- Ablate: `form_known` forced to 0 (the parameter `form_known_in=0`).
  Per the result's mechanism trace, `form_known` is the named transferred state:
  knowledge that the offset form is viable, which skips the 4-example memorization
  preamble (`fit_ok` requires `used>=5` when `form_known=0`).

Mode 2 call: `run_family(mx, st_abl, 21, 20, 7, 0)` where `st_abl` has `offset_hyp`
and `trusted` copied from post-A `st`, and the mem buffer `mx` is the same shared
buffer used in mode 0.

### Validity bars for the amended P3

- P3a ABLATION SLOWS: `exB_abl` (mode 2) must be approximately the A speed
  (within 2 of `exA`). If `exB_abl` stays near the transfer speed (`exB`), the
  ablation fails to isolate the causal state and P3 fails.
- P3b SPECIFICITY: mode 2 differs from mode 0 ONLY in `form_known_in`
  (1 vs 0). All other inputs identical. This isolates `form_known` as the causal
  variable.

### Determinism (closes original P4 gap)

- 3/3 runs byte-identical. All three raw outputs committed as
  `L2L2_REPAIR_RUN1.txt`, `L2L2_REPAIR_RUN2.txt`, `L2L2_REPAIR_RUN3.txt`.
- Exit 0, zero stderr.

### Governance

- Pure Zag. Zero Python at every stage. Zero em-dash bytes in docs.

## Verdict rule for this amendment

REPAIR-PASS iff P3a, P3b, determinism (3/3), and governance all pass.
If REPAIR-PASS, the original P3 is closed and L2L2 may be cited as
ablation-verified. If any bar fails, report honestly.

## Files

- `l2l2_repair.zag`: learner + families + mode 2 (unfrozen variant copy)
- `L2L2_REPAIR_RUN1.txt`, `L2L2_REPAIR_RUN2.txt`, `L2L2_REPAIR_RUN3.txt`: raw outputs
- `L2L2_REPAIR.md`: result report

## Non-claims

- This does not change L2L2's bounded classification (L1/L2, not L3).
- This does not retroactively validate the original BUILD-PASS (5/5) verdict.
- Mode 2 tests `form_known` specifically, per the result's mechanism trace.
  It does not test the prereg's original `trusted=0, offset_hyp=unknown`
  formulation, which named a different (less accurate) state description.
