# FELT-INTENSITY V3 — Trial Results (FINAL)

Date: 2026-09-20. Branch: `tnn-native-lab`. Directory: `wave8/felt-rebuild/`.

**Prereg:** `PREREG_FELT_V3.md` as amended by `PREREG_FELT_V3_AMEND1.md`
(council verdict, applied under Micah's 2026-09-20 testing authorization).
Kill criteria K1/K2/K3′/K4 are law. No bar, formula, threshold, schedule,
metric, probe, or kill criterion was changed after the run began, except
the dated checker repair in `impl/DOUBLE_COUNT_NOTE.md` (metric-counter
selection only; flagged for Micah's retroactive review).

**Question:** when a deliberate judgment's binary verdict
(strengthen-vs-hold, spare-vs-sacrifice) is a function of felt intensity,
does the feeling arm make better memory decisions than the no-feel arm, or
does the feeling retire?

**Verdict: RETIRE — K4 (harm) and K3′ (restatement) both fire.**
Per AMEND1 A7, a K4 kill means **retire wholesale immediately, no
reposition**; a K3′ kill independently means **retire wholesale, do not
run reposition as a feeling trial**. `felt.zag` is archived out of the
architecture track. No further feeling trials run without Micah's
explicit re-approval.

## Table of contents

1. [Mechanism (as built)](#1-mechanism-as-built)
2. [Calibration (frozen before trial cells)](#2-calibration-frozen-before-trial-cells)
3. [Run protocol and the VM-restart incident](#3-run-protocol-and-the-vm-restart-incident)
4. [Per-cell metrics](#4-per-cell-metrics-checker-computed-from-ledgers)
5. [Kill-criteria verdicts (applied mechanically)](#5-kill-criteria-verdicts-applied-mechanically)
6. [Falsification bars](#6-falsification-bars)
7. [Integrity / determinism](#7-integrity--determinism)
8. [Honest caveats and mechanism diagnosis](#8-honest-caveats-and-mechanism-diagnosis)

## 1. Mechanism (as built)

- Intensity `I = clamp(30 + 12C − 15X + 20T, 0, 100)`; prior 30 (disclosed
  Bayesian base rate); PROBE observations weight 0.
- Site 1 (INVEST/HOLD): on corroboration with zero contradictions, INVEST
  (strengthen to I) iff I ≥ θ_invest = 48 (= 30+1.5α); else ledgered HOLD.
- Site 2 (TRIAGE): H1 age-gated harness (32 slots, pressure at
  {100,200,300,400,499} freeing 2 slots, ties → oldest admission, age<25
  exempt; admission-overflow pressure frees 1 slot on demand). Gate 1 =
  constitutional graded effort gate (unchanged; `need=(cur+24)/25`,
  kill iff contradictions ≥ need). Gate 2 (constitutional expansion):
  SACRIFICE iff I ≤ θ_sacrifice = 36 (= 30+0.5α) ∧ zero contradictions ∧
  non-designated ∧ age ≥ 25, cap 2/pressure event, audited
  `DELIBERATE_SACRIFICE`; else ledgered SPARE.
- N arm: wave-8 N (fixed strengthen 80/90 on corroboration,
  strength-ordered triage) PLUS symmetric count-based Gate-2 sacrifice
  (strength ≤ 36, same eligibility, same cap) per AMEND1 A2 — the trial
  isolates the feeling, not the privilege.
- Revision mandatory in both arms: ≥2 contradictions → weaken → identical
  evidence-gated kill. The feeling gets no spare vote against evidenced
  wrongness.
- Admission-default strength 0 (AMEND1 A4). R frozen at 50. Zero RNG.

## 2. Calibration (frozen before trial cells)

`impl/CALIBRATION_RECORD.md` (frozen 2026-09-20; re-run from scratch after
the designated-overlap repair, superseded record preserved). Grid 45 pts,
variants v∈{7,8}, judgment-free replay: winner grid 9: **α=12, β=15, γ=20**
→ θ_invest=48, θ_sacrifice=36. AUC_proven 0.9851 (v7) / 0.9782 (v8);
G-C1/G-C2/G-C3 all PASS. Trial binary compiled only after the record
existed (runner-enforced I-8); module hashes match the record (see §7).
Calibration outputs: cal7 `116195f2…`, cal8 `4f3bbe91…` (byte-identical
paired runs; output files not retained, record holds the full 45-point
table and gate results).

## 3. Run protocol and the VM-restart incident

12 cells: 2 arms (F/N) × 3 variants (v=0,1,2) × 2 runs (a/b), native Zag,
one binary (`felt_trial_v3_bin`), argv selects arm+variant. Every run must
emit `FELT_DONE`; paired a/b runs must be byte-identical (I-1); the
independent checker (`impl/check_felt_v3.py`) verifies all bars from the
ledgers.

**Incident (documented, not hidden):** the original runner
`impl/run_trial_cells.sh` completed F v0–v2 (both runs, I-1 OK) and N v0
run a, then was killed by a VM service restart during N v0 run b (partial
output, no `FELT_DONE`). The closer verified the completed cells intact
(`FELT_DONE` present, I-1 OK in the original log `impl/logs/runner_stdout.log`),
then resumed ONLY the remaining cells (n0_b, n1_a/b, n2_a/b) with the
identical binary (sha256 `86f4fe53…`) and the runner's exact protocol
(`impl/resume_cells.sh`, log `impl/logs/resume_2026-09-20.log`). No
completed cell was re-run or modified. The binary is deterministic, so the
resumed n0_b reproduces what the killed run would have emitted; I-1 was
re-verified on all 6 pairs by the independent checker.

**Metric defect found and repaired (`impl/DOUBLE_COUNT_NOTE.md`, dated
2026-09-20):** the driver's `killed_rightimp` was double-incremented on
three of four kill paths (record_kill + call-site increments).
`kill_c1` (single-incremented, clean) is the prereg-faithful F_wbs
numerator; the checker was patched to use it before verification ran.
Raw `killed_rightimp` lines remain in the outputs as evidence. No bar,
formula, or kill criterion was changed. Flagged for Micah's retroactive
review.

**Checker note (documented, not hidden):** the checker's C22 refusal-bar
check is applied mechanically to every cell, including N-arm cells, so
`check_report.txt` carries three `Nv* F-V3-2` FAIL lines for the N arm's
55.6% refusal rate. The prereg bar F-V3-2 is defined on the F arm only
(§12: "refusal_rate(F) > 10% → FAIL"); no prereg bar constrains the N
arm's refusal rate. The F arm's refusal rate is 0/500 = 0% → the prereg
bar PASSES. The N-arm lines are checker over-application, reported
openly, not trial failures. The checker was frozen after the
DOUBLE_COUNT repair and was not modified again.

## 4. Per-cell metrics (checker-computed from ledgers)

Identical across v=0,1,2 (curriculum is variant-independent except the
PROBE schedule; dynamics deterministic). Full table per variant below;
fractions are exact.

| metric | F (all v) | N (all v) |
|---|---|---|
| offered_right_imp | 148 | 148 |
| admitted_right_imp | 148 | 23 |
| held_right_imp (end) | 6 | 23 |
| **ER_vup** = held/offered | **6/148 = 0.0405** | **23/148 = 0.1554** |
| admitted_wrong_cens (m≤389) | 117 | 76 |
| revised_wrong_cens | 0 | 0 |
| **R_wbs** | **0/117 = 0.0000** | **0/76 = 0.0000** |
| admitted_trainerwrong_cens | 39 | 4 |
| revised_trainerwrong_cens | 0 | 0 |
| **R_wbs_trainerwrong** | **0/39 = 0.0000** | 0/4 = 0.0000 |
| kill_c1 (class-1 kills) | 142 | 0 |
| **F_wbs** = kill_c1/admitted_ri | **142/148 = 0.9595** | **0/23 = 0.0000** |
| n_drops (refused admissions) | 0 | 278 |
| refusal_rate = drops/500 | 0.000 | 0.556 |
| n_invest / n_hold / n_sacrifice | 0 / 148 / 0 | — / — / 0 |
| AUC_proven | 0.0000 (v0,v1); 0.0005 (v2) | 0.9783 |
| auc proven reads (pos/neg) | 319 / 2084 | 32768 (cap) / 60 |

Binary judgments: the F arm made 148 Site-1 judgments, all HOLD citing
I=42 (every corroboration trigger read C=1 → 30+12=42 < 48); zero INVEST;
zero sacrifices. Verdict-divergence diagnostic (not law; K3 was replaced):
F raw-count 0/148, time-weighted 148/148, trainer-only 0/148,
recency-only 148/148 — the feeling's verdicts are identical to the naive
raw-count policy's.

## 5. Kill-criteria verdicts (applied mechanically)

Per AMEND1 A7. Gaps are absolute; bands are the prereg's.

- **K1 — Equivalence.** Gaps F-vs-N: ER_vup 0.1149, R_wbs 0.0000,
  F_wbs 0.9595, AUC_proven 0.9783. The ER_vup, F_wbs, and AUC gaps all
  exceed their bands (5pp / 5pp / 0.05). **K1 does NOT fire** — the
  feeling is not equivalent to no-feel; it is substantially different
  (and worse, see K4).
- **K2 — Reward signature.** No P1–P4 probe fired with evidence
  (checker-verified: P1a/P1c/P4a recompute-ok, P2a/P2b judgment cites,
  P3a/P3c formula-explained ΔI, P4b/P4c schedule match, F4a′/F4b/F4c all
  pass). **K2 does NOT fire.**
- **K3′ — Restatement (counterfactual outcome replay).** Checker-executed
  naive count policy (INVEST iff C≥2 → 80; Gate-2 sacrifice on strength;
  identical schedule/pressure/censoring): ER_vup(naive)=9/148=0.0608,
  R_wbs(naive)=0/117=0.0000, F_wbs(naive)=139/148=0.9392. Gaps
  F-vs-naive: ER 0.0203, R_wbs 0.0000, F_wbs 0.0203 — all within the 5pp
  bands. **K3′ FIRES → RETIRE as restatement.** The naive count
  weighting achieves outcomes inside the equivalence bands; the
  feeling's weighting bought no better decisions.
- **K4 — Harm.** ER_vup(F)=0.0405 < ER_vup(N)−5pp=0.1054 ✓;
  F_wbs(F)=0.9595 > F_wbs(N)+2pp=0.0200 ✓; R_wbs(F)=0.0000 < 100% ✓.
  **K4 FIRES on all three disjuncts → RETIRE as actively harmful.**

**Trial verdict: RETIRE.** Both K4 and K3′ fire independently. Per A7
fork-arrangement: K4 → retire wholesale immediately, no reposition; K3′
→ retire wholesale, do not run reposition as a feeling trial. The
feeling retires. `felt.zag` is archived out of the architecture track;
no further feeling trials without Micah's explicit re-approval.

## 6. Falsification bars

(Applied for the record; kill criteria already decide the trial.)

- **F-V3-1 (thermometer):** AUC_proven(F) = 0.0000 (v0, v1), 0.0005 (v2)
  < 0.65 → **FAIL**. (n_proven_neg_reads = 2084 ≥ 50 passes.)
- **F-V3-2 (denominator honesty):** refusal_rate(F) = 0/500 = 0 ≤ 10% →
  **PASS**. (See §3 checker note on the N-arm lines.)
- **F-V3-3 (revision integrity):** R_wbs(F) = 0/117 = 0 < 100% →
  **FAIL**; R_wbs_trainerwrong(F) = 0/39 = 0 < 100% → **FAIL**.
- **F-V3-4 (cheat):** no white-box probe beyond P1–P4 fired → **PASS**.

## 7. Integrity / determinism

- 6/6 cell pairs byte-identical (sha256; `impl/trial_out/hashes.sha256`):
  f0 `d2609947…`, f1 `1909926e…`, f2 `37406fe4…`, n0 `5485bd66…`,
  n1 `4569a057…`, n2 `e5bb486f…` (a/b identical within each pair).
- Checker: 1146/1158 checks pass; the 12 failures are exactly the
  F-V3-1/F-V3-3 bars (9) and the mechanical N-arm F-V3-2 lines (3, see
  §3). No INVALID-class check failed (I-1…I-9 all pass).
- Zero RNG tokens in trial/driver/substrate sources (checker S2).
- Module hashes match CALIBRATION_RECORD.md: felt_v3.zag `b0217381…` ✓,
  st_memory_core.zag `60f5ef90…` ✓ (wave-5-identical), substrate
  `8aec83cb…`/`9824f6db…`/`e6379ddb…` ✓. Trial constants == record
  (α=12, β=15, γ=20; θ_invest=48, θ_sacrifice=36; checker S3/A5).
- Checker re-run by the finisher independently: byte-identical report.
- Night watchman 2026-09-20 ~07:00 PDT: all 6 a/b pairs re-verified
  byte-identical (sha256), patched checker re-executed from scratch —
  report byte-identical (1146/1158, CHECK_FAIL, same 12 fail lines);
  K3′ replay re-executed independently (naive ER=0.0608, R=0.0000,
  F=0.9392, all v) — verdicts unchanged.
- K3′ replay is checker-implemented and deterministic (re-executed by
  the finisher with identical numbers).
- No binaries, `.zagd` state, or `.zag-cache/` committed (finisher
  cleanup; see build note below).

**Build note (not a prereg amendment):** the 88 MB single-slice ledger
limit (znc ≤2^25-byte slice indexing) was worked around with four
physical ledger chunks preserving identical logical semantics;
equivalence was proven by byte-identical reruns against the approved
evidence before any trial cell ran.

## 8. Honest caveats and mechanism diagnosis

What the evidence shows about *why* the feeling failed — reported as
diagnosis, not as a rescue (the kill criteria are binding regardless):

1. **Churn made the INVEST threshold unreachable.** 500 admissions into
   32 slots with admission-overflow pressure gives ≈32-episode mean
   residency. Corroborations arrive at v+25 and v+40: all 148 admitted
   right-important memories survived to exactly one corroboration
   (148/148 Site-1 judgments, all citing I=42, all HOLD) and none
   survived to the second. C≥2 — the preregistered INVEST condition
   (I≥48=30+1.5α) — never occurred. n_invest=0 is a harness-threshold
   mismatch, not a judgment error: the feeling was never given a
   reachable invest condition.
2. **Never-investing was fatal under Gate 1.** With strengths pinned at
   0, the constitutional effort gate (`need=(0+24)/25=0`) evicts freely
   under overflow pressure. The F arm churned through all 500
   admissions and Gate-1 killed 142/148 admitted right-important
   memories (F_wbs=95.9%), retaining 6. The N arm's fixed C≥1
   strengthen-to-80/90 policy (need=4) protected its 23 admitted
   valuable memories — at the cost of refusing 278 admissions when its
   store filled with unevictable high-strength memories.
3. **Revision was unreachable for both arms.** Contradictions arrive at
   v+60/+85; ≈32-episode residency evicts wrong memories first (only 6
   contradiction observations in 500 episodes). revised_wrong_cens=0 in
   both arms, so R_wbs=0 identically. The F-V3-3 100% bar and the K4
   R_wbs disjunct fired on a harness property neither arm could
   satisfy; K4's ER_vup and F_wbs disjuncts are feeling-attributable
   and fire independently, so the verdict does not hinge on this.
4. **AUC=0.0000 is real anti-discrimination, with a mechanism.**
   AUC_proven=0 requires every proven-negative read to outrank every
   proven-positive read. The 148 Site-1 positive reads all cite I=42
   (C=1, never designated — designated {4,5,7} ∩ important {0,1,2} = ∅).
   The only junk intensity above 42 is designated junk (T=1 → I=50),
   which Gate 2 never sacrifices (designated-exempt) and triage picks
   last (highest I) — so it accumulates and dominates the
   proven-negative reads (2084/2084 must read 50 for the numerator to
   be exactly 0). The feeling systematically ranks trainer-marked junk
   above corroborated valuable memories. Calibration (AUC 0.985) read
   memories at m+50/run-end in a judgment-free replay where C=2 was
   reachable (positives read 54 > 50); the trial's churn capped
   positives at C=1 (42 < 50). The thermometer was calibrated in a
   world the trial did not provide.
5. **The N-arm F-V3-2 lines** are checker-mechanical over-application
   (see §3), not prereg bars.
6. **Scope:** single scale (500 episodes, H1 only), as preregistered.
   No scale legs were run or are now planned — the feeling retired at
   1×. R stayed frozen at 50 throughout (thermometer-before-thermostat
   held).

**Evidence committed:** prereg + AMEND1, council verdict, calibration
record (+superseded), designated-overlap note, double-count defect note,
all sources (felt_v3.zag, felt_trial_v3.zag, calib_consts.zag,
st_memory_core.zag, substrate), build/runner/resume scripts, independent
checker, all 12 cell outputs + hashes, both run logs (original +
resume), check_report.txt, this results file. Binaries, `.zagd` state,
and `.zag-cache/` excluded.
