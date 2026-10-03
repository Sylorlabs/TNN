# JUDGE_BRIEF.md - F1-REPAIR repair-dynamics discrimination

Provenance:
- RENDER_SHA: 5935c5169 (sealed evaluation commit; prereg b4afb6236,
  implementation fadaee3fb, fixtures cbded055d, all on branch
  tnn-native-lab, local only)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: F1 BUILD-FAIL, F1-FOLLOWUP BUFFER-NOT-PREDICTIVE
- NEW_KNOWLEDGE_CLAIM: The frozen full-buffer repair signature is
  refuted by a fresh-seed counterexample (seed 10 repaired on a
  partial buffer), but the trace evidence shows repair bursts, not
  the greedy trial, deciding outcomes: a relaxed repair-to-zero
  signature separates all 20 degenerate-path seeds across two seed
  series.

## Verdict: GREEDY-CONFIRMED (per the frozen decision rule)

Governing bars (frozen in PREREG_REPAIR.md, committed alone at
b4afb6236 before any probe was built, any fresh fixture was
generated, or any fresh run executed; binary under test is F1's
frozen impl/f1_learn, sha256 verified before runs):

- 24 fresh sealed 6100-series sum2 worlds; 3/3 byte-identical
  reruns on all 48 invocations; zero NOTRIG, zero parse failures.
- Overfit rate 6/24 = 25 percent (seeds 3, 4, 5, 11, 13, 22; all
  0 to 7 percent hidden; all 18 correct seeds at 30/30).
- Degenerate-path subset D = 11 seeds (3, 4, 5, 10, 11, 12, 13,
  15, 17, 20, 22). Frozen signature S=1 on seeds 12, 15, 17, 20
  (all CORRECT, repair bursts at episodes 7, 23, 14, 12 on full
  buffers); S=0 on the other 7.
- Counterexample pairs within D: seed 10 (S=0, CORRECT 30/30)
  vs seeds 3, 4, 5, 11, 13, 22 (S=0, OVERFIT): 6 pairs.
  PREREG_REPAIR.md section 3(c) fired exactly as written.
- K-C0A: PASS (zero semantic markers in new lane code; probe is
  an external trace reader; frozen binary unmodified).
- Commit-order self-check: prereg (b4afb6236) precedes
  implementation (fadaee3fb), which precedes fixtures
  (cbded055d), which precede sealed runs and evaluation
  (5935c5169). No bar moved after freezing.

## What the verdict label does and does not mean

The label follows the frozen rule mechanically. Its mechanistic
gloss ("repair bursts are epiphenomenal") is NOT supported by the
traces, and reporting it bare would mislead:

- Seed 10's first two constructs are the degenerate doubling
  (ADD r0,f0,f0; ADD r0,r0,r0), identical in form to OVERFIT
  seeds 3, 4, and 22. The first-two-constructs story cannot
  explain its CORRECT outcome.
- What explains it is a later repair burst: TRIGGER 3 on a
  partial buffer (buf=4) constructed [ADD r0,f0,f0; ADD r0,r0,f1;
  ADD r0,r0,f1] with err 16->12->6->0, revising the degenerate
  structure to a correct one.
- None of the 7 S=0 OVERFIT D-seeds has any later burst reaching
  err_after=0 on any buffer size; their later bursts stall or
  make partial constructs that never reach zero. No
  non-degenerate seed has any later to-zero burst.
- Under the relaxed signature S' (later trigger burst to
  err_after=0, any buffer size), the D-subset separates 11/11 on
  the fresh series and 9/9 on the 5100 training series: 20/20
  degenerate-path seeds across two series, repair-to-zero iff
  CORRECT.

So the counterexample refutes the frozen signature's buf=8
clause (overfit to the 5100 calibration, where all observed
repairs happened to be full-buffer), not the repair story. The
failure is a repair-dynamics phenomenon: degenerate-path seeds
whose later bursts run to zero go CORRECT; those whose bursts
stall go OVERFIT.

## Recommended next experiment

Do not treat this as a win for attacking the depth-1 trial. The
data calls for a fresh prereg testing the relaxed repair
signature S' on new sealed worlds, then a repair-time policy
experiment: what distinguishes later bursts that run to zero
from those that stall (buffer composition at trigger time,
win/buf dynamics, why partial-buffer repairs succeed when they
do). The degenerate path is necessary for overfit in this
series (6/6 overfit seeds are D-seeds); repair-to-zero decides
the outcome within D.

## What the judge should know

1. The frozen verdict is GREEDY-CONFIRMED by rule 3(c); the
   trace evidence favors the repair story with the buffer-size
   clause relaxed. Both are reported; neither was softened.
2. Methodology is reusable: dev/repsig and dev/repapply are
   pure-Zag, validated by exact reproduction of the 5100
   calibration table (REPAIR-CONFIRMED there), and repsig takes
   any f1_learn train trace.
3. Zero new semantic cases, modes, bridges, or handlers; the F1
   binary was used read-only throughout.

Evidence paths (all under
docs/lab/rsi/runs/wave-20261001-2321pdt/F1-REPAIR/):
- PREREG_REPAIR.md, SEALED_EVAL_REPAIR.md, NAMECHECK.md
- dev/CALIBRATION_5100_REPAIR.md
- dev/repsig.zag, dev/repapply.zag, dev/repsig, dev/repapply,
  dev/f1_wgen, dev/f1_score
- sealed4/ (fixtures, gen4.sh, run_repair.sh,
  FIXTURE_SHA256.txt)
- runs4/ (1, 2, 3 repetitions; DETERMINISM_SHA256.txt;
  fresh_table.txt; fresh_scores.txt; fresh_reps.txt;
  verdict.txt; run_repair.log)

No em-dashes in this document.
