# VERDICT — Arm W (multi-granularity), Track A closeout

**Date:** 2026-09-21
**Arm:** W — Multi-granularity (STRUCT family)
**Adjudicated by:** verdict gap-fill crew (Track A closeout)
**Verdict: UNADJUDICATED** — evidence genuinely insufficient (missing items below)

## Frozen kill criterion (verbatim, §3 of `units/PREREG_FREEZE.md`, extracted programmatically)

> Any one: (i) composite battery score does not beat S alone by ≥15% — W is S with extra steps; (ii) justification gate refuses >5% of selections — the selector is unsound; (iii) determinism gate fails; (iv) floor rule fires.

## Why UNADJUDICATED

No binding criterion can be evaluated against existing evidence:

- **Kill (i):** requires W's "composite battery score" vs S alone. No
  composite-battery-score definition exists in the frozen prereg or in
  W's `cl/ARM_SPEC.md` (126 lines; quotes the frozen row but defines no
  composite). W has no composite battery run; S's `VERDICT.md` (PASS 1x)
  reports M1–M9 but no composite number either. Evaluating (i) would
  require inventing the composite — creating criteria, not applying them.
- **Kill (ii):** requires the justification-gate refusal rate. No
  measurement exists (the selector/refusal path in `cl/ARM_SPEC.md` §2 is
  specified; no refusal-rate output was ever produced).
- **Kill (iii):** requires the determinism gate (M8). `work/m8/` and
  `work/smoke/` are empty; no M8 evidence exists.
- **Kill (iv):** requires floor-rule metrics. None exist.

## What exists

- Builds: `work/w_bin` (ELF x86-64, statically linked).
- One truncated M1-prose output: `work/m1_prose_v0_r1.txt` — the
  metrics-v1 JSON line is cut off mid-`"fields":{`, so even M1-prose is
  not honestly readable.
- Harness scripts: `work/harness/` (corpora builders, `run_metric.sh`,
  `m8_gate.sh`, `m8_compare.py`) — tooling, not results.
- `ledger.bin` at arm root (unattributed).
- Design spec: `cl/ARM_SPEC.md` (three levels L0/L1/L2, selector with
  justification gate, S-rule crystallization).

## What's missing (to adjudicate)

1. A complete 1x battery (M1–M9, double runs, byte-identical) for W.
2. A frozen definition of the "composite battery score" plus W's and
   S's composite numbers for the ≥15% comparison.
3. Justification-gate refusal-rate measurement (the >5% bar).
4. M8 determinism evidence and floor-rule metrics.

**Result: W UNADJUDICATED — the arm builds, but no binding kill
criterion is measurable on existing evidence.**
