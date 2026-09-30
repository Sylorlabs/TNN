# RESULT: F3 Phase 3 T-NEG amended run (T-NEG-A)

Date: 2026-09-30. Worker: F3 T-NEG Executor.
Verdict: **TNEG-PASS**.

## 1. Ancestry (all in git history, no step skipped or reordered)

1. Amendment committed: c35da8aa0 (PREREG_F3P3_AMENDMENT_A.md).
   No code changed by the amendment.
2. world_tneg_a.zag created per amendment section 2 (byte-identical
   copy of sealed world_tneg.zag plus appended main block).
   Diff gate: PASS (additions only: one blank line plus the six-line
   main block; no modified or deleted lines).
3. Freeze committed: 179ec88a4 (world_tneg_a.zag + FREEZE_TNEG_A.md;
   message cites the amendment and records sha256
   47f38c99d5f96a5f09c7ffa4316ab30ecbff19265e7a7de4002baa32a3324cf4).
4. Freeze hash recorded in the freeze note: 54182f72b (note only;
   frozen artifact unchanged; no build or test ran before 179ec88a4).
5. BUILD.sh updated per amendment section 2 (T-NEG line uses
   world_tneg_a.zag): ad965b2c6. Latent T-CONJ world path fixed to
   D-relative so the script runs from the repo root: 3f2cd4a47.
   Harness path fix only; no frozen prediction, falsifier, learner,
   or world content changed.
6. BUILD.sh run after all freeze commits: exit code 0.
   - bin_p3c written (159575 bytes), 3 T-CONJ runs.
   - bin_p3n written (159270 bytes), 3 T-NEG runs.
   - md5: 3/3 T-CONJ identical (63bc88e2ce74281a2afb70d64971814e);
     3/3 T-NEG identical (f54a67c952423ac3b8a94c530d15e4e4).
   - T-CONJ rerun logs are byte-identical to the committed passing
     logs from the original phase (no working-tree modification).

## 2. T-NEG judgment vs frozen predictions (prereg section 3)

- P-PROP-N: PASS. `PROP V=Y lit=X@1 ok=2`; candidates `Y: 1`;
  ruleset `V=Y rule=0 [X@1]`. Exactly one candidate: (X,+,1).
- P-TRIAL-N: PASS. `F3P3 TRIAL V=Y rule=0 seq=[SX,W,OY]` then
  `F3P3 RULE_CONFIRMED V=Y rule=0 obs=1`. No refutation of the rule.
- P-FAIL-N: PASS. `F3P3 PLAN [SX,W] (attempt 1)` then
  `F3P3 GOAL_REAL 0 (attempt 1)`. Z=1 blocks Y as predicted.
- P-GROW-N: PASS. `F3P3 GOAL_FAIL_GROW_ATTEMPT` then
  `F3P3 GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@1`;
  `F3P3 HAS_NEG_AFTER_GROW 1`. The 2-literal rule {(X,+,1),(Z,-,1)}
  is formed and the GROW_OK line names the negative literal.
- P-REPLAN-N: PASS. `F3P3 PLAN [SX,CZ,W] (attempt 2)` (plan clears
  Z) then `F3P3 GOAL_REAL 1 (attempt 2)`.
- P-COST-N: PASS. `F3P3 NEXPS 3 COST_OK 1`. 3 <= 8.
- P-DET-N: PASS. 3/3 byte-identical (md5 above); all six run stderr
  files are 0 bytes; build exit code 0; `F3P3 RESULT` line present:
  `F3P3 RESULT PHASE3-TESTED K1=PASS K2=PASS K3=PENDING-3x`.
  The harness marker `TNEG DONE mask=0` is present as specified
  (marker only, not a verdict).

## 3. Falsifiers (prereg section 4)

- F-GROW-N: not fired (GROW_OK names !Z@1).
- F-REPLAN-N: not fired (second attempt GOAL_REAL=1).
- F-PROP-N: not fired (Y candidate set exactly {(X,+,1)}).
- F-DET: not fired (3/3 identical per world).
- F-SOURCE: not fired. The learner f3_p3.zag is the frozen
  implementation, unchanged; it reads only the w_* interface.
  world_tneg_a.zag adds only the main() harness entry point.
- F-PURITY: not fired, with one disclosed observation. Zero Python
  was invoked at any stage of this run (sh, cp, printf, diff,
  sha256sum, grep, git, md5sum, znc only). All researcher-authored
  files and all learner-emitted logs contain zero em/en-dash bytes.
  The znc compiler itself emits em-dash bytes (E2 80 94) inside its
  A0102 warning diagnostics, which appear in build_p3n.err. The
  identical compiler-emitted bytes are present in the original
  phase's build_p3c.err, which the phase judged pure-Zag; the bytes
  are toolchain diagnostics, not researcher-authored content, so
  F-PURITY is not fired. This is disclosed, not hidden.

## 4. Executor kill bars

- K1 (diff gate passes): PASS. Verified before freeze.
- K2 (3/3 byte-identical): PASS. md5-confirmed for T-NEG; T-CONJ
  rerun also 3/3 identical and matches committed logs.
- K3 (pure Zag, zero Python): PASS. No Python anywhere in this run,
  including creation, diff, hashing, build, and verification.

## 5. Phase 3 implication

Amendment section 6: if T-NEG passes its bars while T-CONJ still
passes, the Phase 3 verdict may be revised from BUILD-FAIL to the
honest outcome the frozen bars produce. T-CONJ reran byte-identical
to its committed passing logs; T-NEG passes every frozen prediction
with no falsifier fired. The frozen Phase 3 K2 bar (T-NEG tested per
section 2; negation literal learned via GROW on goal failure;
replanned goal achieved within cost bound) is now met, and this
clean rerun is K4-clean (the original K4 violation was a python3
byte check in the superseded run, not repeated here). The honest
outcome the frozen bars produce is **Phase 3 BUILD-PASS**.

No bar was weakened to force this pass. The sealed world_tneg.zag
remains unmodified in history as evidence of the original defect.
