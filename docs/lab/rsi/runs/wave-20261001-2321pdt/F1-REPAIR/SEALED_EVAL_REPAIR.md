# SEALED_EVAL_REPAIR.md - F1-REPAIR sealed test results

Lane F1-REPAIR, wave wave-20261001-2321pdt. Sealed runs executed
2026-10-02 ~00:20 PDT against the frozen F1 binary
`../F1/impl/f1_learn` (sha256
6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847,
verified before running; match confirmed). 24 fresh sealed sum2
worlds (frozen 6100-series seeds, manifest sealed4/FIXTURE_SHA256.txt,
all hashes verified before runs). Frozen rule from PREREG_REPAIR.md
(committed alone at b4afb6236 before any probe was built, any fresh
fixture was generated, or any fresh run executed; implementation
committed at fadaee3fb; fixture manifest committed at cbded055d
before any sealed run).

No em-dashes are used in this document.

## 1. Determinism evidence

Each of the 48 sealed invocations (24 seeds x train/hidden) was
executed 3 times (runs4/1, runs4/2, runs4/3). All corresponding
outputs are byte-identical across the three repetitions
(cmp-verified, zero diffs). SHA-256 of all runs4/1 outputs is
recorded in runs4/DETERMINISM_SHA256.txt. The 24-seed set with 3/3
determinism per seed is complete (24/24). Zero NOTRIG worlds, zero
trace-parse failures.

## 2. Overfit rate on fresh worlds (frozen classification)

OVERFIT = hidden accuracy below 80 percent (f1_score acc on the
30-probe masked set, frozen pure-Zag scorer). CORRECT = at least 80
percent. The split is cleanly bimodal; no seed is near the boundary.

| seed | hidden | class |
|---|---|---|
| 3 | 0/30 = 0% | OVERFIT |
| 4 | 0/30 = 0% | OVERFIT |
| 5 | 2/30 = 7% | OVERFIT |
| 11 | 0/30 = 0% | OVERFIT |
| 13 | 0/30 = 0% | OVERFIT |
| 22 | 1/30 = 3% | OVERFIT |
| 0,1,2,6,7,8,9,10,12,14,15,16,17,18,19,20,21,23 | 30/30 = 100% | CORRECT |

Overfit rate: 6/24 = 25 percent, same catastrophic signature as the
5100-series (6/24) and 8100-series (8/24): every overfit seed scores
0 to 7 percent. All 6 overfit seeds are degenerate-path seeds
(deg=1); no non-degenerate seed overfit.

## 3. Frozen signature and rule application (pure-Zag repsig/repapply)

Per-seed frozen repair-burst signature S (REPAIR-BURST = later
trigger with buf=8 whose burst runs to err_after=0; D = degenerate
second construct in the first-trigger burst, per PREREG_REPAIR.md
section 2):

| seed | trig | deg | S | nrep | reps (ep) | label |
|---|---|---|---|---|---|---|
| 0 | 2 | 0 | 0 | 0 | - | CORRECT |
| 1 | 1 | 0 | 0 | 0 | - | CORRECT |
| 2 | 1 | 0 | 0 | 0 | - | CORRECT |
| 3 | 1 | 1 | 0 | 0 | - | OVERFIT |
| 4 | 1 | 1 | 0 | 0 | - | OVERFIT |
| 5 | 1 | 1 | 0 | 0 | - | OVERFIT |
| 6 | 1 | 0 | 0 | 0 | - | CORRECT |
| 7 | 1 | 0 | 0 | 0 | - | CORRECT |
| 8 | 1 | 0 | 0 | 0 | - | CORRECT |
| 9 | 1 | 0 | 0 | 0 | - | CORRECT |
| 10 | 1 | 1 | 0 | 0 | - | CORRECT |
| 11 | 1 | 1 | 0 | 0 | - | OVERFIT |
| 12 | 1 | 1 | 1 | 1 | 7 (buf=8) | CORRECT |
| 13 | 1 | 1 | 0 | 0 | - | OVERFIT |
| 14 | 1 | 0 | 0 | 0 | - | CORRECT |
| 15 | 1 | 1 | 1 | 1 | 23 (buf=8) | CORRECT |
| 16 | 1 | 0 | 0 | 0 | - | CORRECT |
| 17 | 1 | 1 | 1 | 1 | 14 (buf=8) | CORRECT |
| 18 | 1 | 0 | 0 | 0 | - | CORRECT |
| 19 | 1 | 0 | 0 | 0 | - | CORRECT |
| 20 | 1 | 1 | 1 | 1 | 12 (buf=8) | CORRECT |
| 21 | 1 | 0 | 0 | 0 | - | CORRECT |
| 22 | 1 | 1 | 0 | 0 | - | OVERFIT |
| 23 | 1 | 0 | 0 | 0 | - | CORRECT |

D-subset (deg=1): seeds 3, 4, 5, 10, 11, 12, 13, 15, 17, 20, 22
(D = 11). S=1: seeds 12, 15, 17, 20 (all CORRECT). S=0: seeds 3,
4, 5, 10, 11, 13, 22 (six OVERFIT, one CORRECT: seed 10).

Frozen decision rule (PREREG_REPAIR.md section 3):
(a) D = 11 >= 6: pass.
(b) D_S1 = 4 >= 2 and D_S0 = 7 >= 2: pass.
(c) Counterexample pairs within D (identical S, different
    label): seed 10 (S=0, CORRECT) pairs with seeds 3, 4, 5, 11,
    13, 22 (S=0, OVERFIT): 6 pairs.

## 4. Verdict: GREEDY-CONFIRMED (per the frozen decision rule)

Section 3(c) fired: a counterexample pair exists within D
(identical frozen repair signature S=0, different outcomes).
The verdict is therefore GREEDY-CONFIRMED, with the pair list
above. No bar was weakened; the rule fired exactly as frozen.

## 5. Mechanistic post-hoc (explanatory only, not the verdict)

The counterexample refutes the frozen signature's full-buffer
clause, not the repair story. Seed 10's train trace shows:

- TRIGGER 1 (buf=2): degenerate doubling (ADD r0,f0,f0;
  ADD r0,r0,r0), err 28->12->4, STALL.
- TRIGGER 3 (buf=4): burst [ADD r0,f0,f0; ADD r0,r0,f1;
  ADD r0,r0,f1], err 16->12->6->0. A repair burst that runs the
  trial-buffer error to zero, on a partial (4-episode) buffer.

Seed 10 was repaired; the frozen signature missed it only
because it required buf=8. None of the 7 S=0 OVERFIT D-seeds
has any later burst reaching err_after=0 on any buffer size:
their later bursts stall outright or make single partial
constructs (e.g. 34->29, 23->16, 18->14, 32->25) that never
reach zero. No non-degenerate seed has any later to-zero burst.

Under the relaxed signature S' (later trigger burst to
err_after=0, any buffer size), the D-subset separates 11/11 on
this fresh series: S'=1 (seeds 10, 12, 15, 17, 20) all CORRECT;
S'=0 (seeds 3, 4, 5, 11, 13, 22) all OVERFIT. The relaxed
signature is also consistent with all 5100 training data (9/9;
verified: no partial-buffer to-zero burst exists there, so the
buf=8 clause was never load-bearing on training, it merely
happened that all training repairs were full-buffer).

H-GREEDY's mechanistic gloss ("repair bursts are epiphenomenal;
the first two constructs fully determine the outcome") is not
supported by the counterexample: seed 10's first two constructs
are the degenerate doubling, identical in form to OVERFIT seeds
3, 4, and 22; the first-two-constructs story cannot explain its
CORRECT outcome, while the later repair burst at TRIGGER 3
directly precedes it. The frozen verdict label follows the
frozen rule; the trace evidence favors the repair story with
the buffer-size clause relaxed.

## 6. K-C0A audit (PASS)

Grep audit over all new lane code (dev/repsig.zag,
dev/repapply.zag, sealed4/*.sh): zero hits for forbidden
protected-semantic markers, downgrade kill-pattern markers, and
menu/kit/candidate-family markers. The only marker-name hits in
the lane are inside PREREG_REPAIR.md section 10 itself, where
the audit specification names the markers it checks for. The
probe and applier are external trace readers; they contain no
learner logic and no semantic cases. The frozen binary was not
modified.

## 7. Architecture accounting

0 cognition-substrate source lines added; no file outside this
lane touched; the F1, F1-FOLLOWUP, and F1-BUFFER lanes were
read-only (f1_wgen/f1_score copied; traces inspected, never
modified). New code is sealed methodology only. No new semantic
cases, modes, bridges, routers, or handlers.

## 8. Recommended next experiment

The data calls for a fresh prereg testing the relaxed repair
signature (S' = later trigger burst to err_after=0, any buffer
size) on new sealed worlds, not an attack on the depth-1 trial:
the frozen verdict notwithstanding, the traces show repair
bursts deciding outcomes, and the open question is what makes
a later burst run to zero versus stall (a repair-time policy
experiment: buffer composition at trigger time, win/buf
dynamics, and why partial-buffer repairs succeed when they do).

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1-REPAIR/):
- PREREG_REPAIR.md (frozen signature, rule, bars)
- dev/CALIBRATION_5100_REPAIR.md (training calibration)
- dev/repsig.zag, dev/repapply.zag, dev/repsig, dev/repapply
  (pure-Zag tools; validated on 5100: exact calibration
  reproduction, REPAIR-CONFIRMED there)
- dev/f1_wgen, dev/f1_score (read-only copies; wgen verified
  byte-identical on the 8100 reference fixture)
- sealed4/ (24 fresh fixtures, gen4.sh, run_repair.sh,
  FIXTURE_SHA256.txt)
- runs4/ (1, 2, 3 repetitions; DETERMINISM_SHA256.txt;
  fresh_table.txt; fresh_scores.txt; fresh_reps.txt;
  verdict.txt; run_repair.log)
