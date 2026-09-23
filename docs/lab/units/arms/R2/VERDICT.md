# Arm R2 — Compounding-Elimination Cuts | FINAL VERDICT

**Date:** 2026-09-21
**Arm:** R2 — Compounding-elimination cuts
**Family:** CUT
**Mechanism:** Candidate boundaries proposed cheaply (every 64B boundary, zero
lookup), eliminated by compounding evidence (8B-pair FNV-1a recurrence check,
online left-to-right running counts; accept iff count≥1).
**Verdict:** **KILL** (binding kill criterion met via disjunct (a); ceiling-effect
tie with arm R, not a loss)

## Authority

1. Frozen `units/PREREG_FREEZE.md` §3 row (extracted programmatically from the
   repo file, line 489 — quoted VERBATIM below, never from memory).
2. Arm R's committed evidence (`sylorlabs/TNN@76849610b8`, "Arm R: optimization
   port, bug fix, 1x battery, KILL verdict") used as DATA; arm R was NOT
   rebuilt.
3. R2's own fresh 1× battery (`work/battery_r2/`, 18/18 legs byte-identical
   double runs) plus this crew's M1 re-run (`work/r2_rerun/`).

## Binding kill criterion (VERBATIM from PREREG_FREEZE.md §3)

> | R2 — Compounding-elimination cuts | CUT | Candidate boundaries proposed cheaply, eliminated by compounding evidence; proposals-per-accepted-cut must fall over the corpus (eliminations compound). | Verified-boundary recall (M1) on held-out probes does not beat arm R by ≥3 points (receipts don't buy recall at 10× compute); OR proposals-per-accepted-cut does not fall over the corpus — core claim fails. **R2/Z1 merge decision: A-37 (default: both tested).** |

## Kill adjudication

### Disjunct (a) — "Verified-boundary recall (M1) on held-out probes does not beat arm R by ≥3 points"

| Corpus | R2 M1 recall (re-run this crew) | Arm R M1 recall (committed 76849610b8) | Margin |
|--------|------|------|------|
| prose | 100.0 | 100.0 | 0.0 |
| code | 100.0 | 100.0 | 0.0 |

- **R2's number:** re-run 2026-09-21 with the frozen R2 build (`work/r2_bin`)
  via `units/arms/harness/run_metric.sh` against `corpora/r1`:
  `mode=m1-1x-prose rc1=0 rc2=0 stdout=IDENTICAL fatal=0`,
  `mode=m1-1x-code rc1=0 rc2=0 stdout=IDENTICAL fatal=0`.
  METRIC_JSON: recall 100.0 / boundary 100.0 both corpora; swap probes 63/63.
  Artifacts: `work/r2_rerun/m1-1x-{prose,code}/` (STATUS.txt, run1/, run2/).
- **R's number:** `docs/lab/units/arms/R/VERDICT.md` at `76849610b8`:
  "Held-out recall (M1): R-cuts vs 64-byte baseline — prose 100.0 / 100.0,
  code 100.0 / 100.0." R's kill fired on this exact ceiling tie.
- **Adjudication:** R2 beats arm R by 0.0 points, which is < 3 points.
  **Disjunct (a) is TRUE → kill fires.** This resolves the
  PROVISIONAL-PENDING-R status: the comparison was blocked on R's committed
  numbers; those numbers are now 100.0/100.0, exactly the ceiling the R2 crew
  predicted (≤97.0 needed to survive).

### Disjunct (b) — "proposals-per-accepted-cut does not fall over the corpus"

From the fresh 1× scorecard (`work/battery_r2/scorecard_r2_1x.json`,
raw per-decile TAG/R2_CURVE pairs):

- prose: early-3 mean 12.577 → late-3 mean 5.350 (decile ratios
  20.37, 11.51, 9.75, 7.79, 7.27, 6.34, 5.61, 5.31, 5.33, 5.41 —
  monotone decline to asymptote).
- code: early-3 mean 3.869 → late-3 mean 2.338 (decile ratios
  5.10, 3.83, 3.15, 2.91, 2.73, 2.42, 2.56, 2.41, 2.32, 2.29).

**Disjunct (b) is FALSE** — proposals-per-accepted-cut falls on both corpora;
the core claim holds. R2 dies despite this.

### Result

- Clause (a): TRUE (tie at ceiling; margin 0.0 < 3 points)
- Clause (b): FALSE (compounding holds)
- **Kill ((a) OR (b)): TRUE → R2 KILLED, binding.**

## Interpretation

This is a ceiling-effect tie, not a loss: R2's verified-boundary recall is
100.0 on both held-out corpora, and arm R's committed recall is also 100.0 on
both. The M1 task cannot discriminate between two perfect mechanisms, so the
literal OR-kill — which demands R2 beat R by ≥3 points — fires against R2,
exactly as it fired against R itself (R died on a literal OR-kill versus the
64-byte baseline on the same 100%-vs-100% tie).

Note the mirror: arm R died proving recall *ties*; R2 dies demanding recall
*margin*. Both deaths are artifacts of the same ceiling. The frozen criterion
is applied as written; no prereg amendment is requested by this crew.

**R2/Z1 merge decision A-37 (default: both tested):** the merge does not
proceed — R2 is killed; Z1 is adjudicated separately on its own numbers.

## Evidence basis (all fresh, two crews)

- Binary: `work/r2_bin` rebuilt from `cl/arm.zag` with the frozen toolchain
  (`znc_linux_x86_64_abed8aa1`); compiles clean, warnings only.
- Full 1× battery `work/battery_r2/` (R2 crew, fresh): **18/18 legs passed** —
  every leg ran twice, rc=0×2, stdout byte-IDENTICAL, fatal=0 on all metric
  legs. M8 gate PASS (5 perturbations × 2 reruns, artifacts byte-identical).
- This crew's M1 re-run `work/r2_rerun/` (2026-09-21): m1-1x-prose and
  m1-1x-code re-run twice each, rc=0×2, stdout IDENTICAL, fatal=0;
  METRIC_JSON fragments in `fragment.jsonl`.
- Zero RNG in any decision path (source-audited; battery reruns
  byte-identical). Pure Zag.
- Scorecard: `work/battery_r2/scorecard_r2_1x.json` (== `scorecard_r2_r1.json`).

## Corpus note (honest bookkeeping)

`corpora/r1/prose.bin` (5,638,480 B, mtime 2026-09-21 05:45) differs from the
file present at the R2 crew's original battery run (m1 units 11,871 then,
13,970 now). The metrics that drive the kill adjudication — verified-boundary
recall and boundary scores — are 100.0 in both runs, and both of this crew's
reruns are internally byte-identical, so the kill adjudication is unaffected.

## Standing provisional cells (unchanged, from the R2 crew's verdict)

- **A15 (M1 ID-swap probe): PROVISIONAL-PENDING-FREEZE.** Implemented literally
  per ARM_SPEC §3; 63/63 ok.
- **A7/A8 (M7): PROVISIONAL-PENDING-FREEZE.** M7 reuse bar FAILS
  (1.36 vs 1.5) — reported as-is; non-binding for the kill but a real miss:
  the compounding-elimination mechanism's chunk identity is too aggressive
  for the reuse bar on this schedule. Not patched, not hidden.
- M8 freelist perturbation is the documented no-op (slot placement is a pure
  function of unit ID); per-proposal/per-elimination ledger entries are the
  documented M5 deviation.

## Bottom line

**R2: KILLED (binding, disjunct (a)).** R2 beats arm R by 0.0 points on
verified-boundary recall (100.0 vs 100.0 on both corpora), short of the
required ≥3-point margin. Core claim (compounding) holds — proposals-per-
accepted-cut falls on both corpora — but the OR-kill fires on the head-to-
head clause. Ceiling-effect tie, not a loss.
