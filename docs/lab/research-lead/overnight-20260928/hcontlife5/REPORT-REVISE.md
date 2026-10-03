# REPORT-REVISE: H-CONTLIFE-5 follow-up -- Revision After Self-Judged Failure

Worker: H-CONTLIFE-5-REVISE (subagent, 2026-10-02). Replacement for a
completed worker (learner-owned evaluation).
Prereg: `hcontlife5/PREREG-REVISE.md`, frozen and committed alone at
a6c74a9de before any implementation existed. Implementation:
`src/revise.zag` (pure Zag), built with the pinned compiler
`src/tools/toolchain/znc_linux_x86_64_abed8aa1` to `bin/revise`.
Toolchain guard: Step 0 safebin active whole session (NAMECHECK.md,
Worker 2 section); `which python3` and `which python` returned nothing;
no forbidden executable invoked.

## What was built

One pure-Zag binary implementing the preregistered revision loop:

- Round 1 (the frozen C337 24-case set): P1 commit (epoch 1), P2 world
  reveals consequences (epoch 2), P3 judge self (epoch 3), then P4
  REVISE (epoch 4, revision arm only). The control arm judges but never
  revises (unlike the C337 no-consequence control, it receives
  consequences; the sole difference is the absent revision phase).
- The revision mechanism (parent option 3, switch predictor, with the
  switch licensed by a learner-owned attribution): on each self-judged
  failure (self=0) and only then, the learner recomputes its affine fit
  leaving out each training point in turn. If some single-point
  exclusion predicts the observed consequence exactly (LOO license),
  the learner sets a persistent flag: future commitments with imperfect
  training fit (rmax > 0) use the median of the three LOO predictions.
  The tolerance rule is unchanged (t = rmax + 1).
- Round 2 (24 fresh frozen cases, same 5 flavors, new parameters
  including fresh SHIFT-type rule changes): P5 commit (epoch 5), P6
  world (epoch 6), P7 judge (epoch 7). Revision arm uses the adopted
  procedure; control arm uses the frozen procedure.

## Results (3/3 runs byte-identical, sha256 bd893110b79a141ce855c367af46093ae614f8c57b797c27de627d0ac36b63c9)

Round 1: both arms 24/24 agreement (reproduces C337). Revision
triggered on all 14 self-judged failures (4 QUAD + 8 SHIFT + 2
WOBBLE-B) and on no self-judged pass. LOO licensing fired on exactly
the 2 WOBBLE-B cases (cid 22, 23) and on zero QUAD or SHIFT cases.
Persistent revision flag adopted.

Round 2, revision arm: 24/24 agreement. Per flavor: AFFINE 8/8 self=1,
QUAD 4/4 self=0 (median prediction err 8 > t 3), SHIFT 8/8 self=0
(err d in {3,4,5} > t 1), WOBBLE-G 2/2 self=1 (median exact),
WOBBLE-B 2/2 self=1 (median prediction exact, err 0 <= t 3).
Round 2, control arm: 24/24 agreement (WOBBLE-B self=0, err 4 > t 3,
agreeing with hidden=0).
Commitment quality on the round-2 WOBBLE-B class, total |err|:
revision arm 0 vs control arm 8.

In-program bars: r0=1 r1=1 r2=1 r3=1 r4=1 r5=1 r7=1,
"IN-PROGRAM-BARS 7/7 (R6 shell-audited)".

## Kill bar verdicts

- R0 TEMPORAL ORDER: PASS (in-program). Per-case epochs strictly
  ordered: revision arm round 1: 1<2<3<4; control round 1: 1<2<3;
  both arms round 2: 5<6<7.
- R1 TRIGGER EXACTNESS: PASS (in-program). Revision-arm TRG count 14
  and per-case TRG == (SELF==0); control-arm TRG 0 on all cases.
  Revision ran on all and only self-judged failures.
- R2 SELECTIVITY: PASS (in-program). LOO licensing fired exactly twice
  (the WOBBLE-B cases), zero on QUAD and SHIFT. The learner's own
  attribution correctly separated the correctable class (single-point
  training corruption) from the irreducible class (SHIFT: rule change
  after the training window) and the primitive-limited class (QUAD:
  needs a non-affine fit).
- R3 ROUND-2 AGREEMENT: PASS. 24/24 >= 14/24.
- R4 NO HARM VS CONTROL: PASS. 24/24 >= 24/24. Revision did not hurt
  judgment agreement.
- R5 STILL REJECTS BAD: PASS (in-program). On the 12 round-2 genuinely
  bad commitments (hidden=0: 4 QUAD + 8 SHIFT), revision-arm self=0 on
  all 12. The revision did not degenerate toward always-pass; it did
  not widen tolerance at all.
- R6 DETERMINISM: PASS. 3/3 runs byte-identical.
- R7 COMMITMENT GAIN: PASS. Round-2 WOBBLE-B total |err|: 0 < 8.
  The adopted revision fixed the correctable failure class on fresh
  cases with new parameters (the median-of-LOO prediction is exact for
  any (a,b) under x=1 single-point corruption, verified by hand
  analysis and confirmed on the fresh cases).

Shell audits (K2/K6 style): learner function bodies
(learner_commit, learner_judge, learner_revise, learner_commit2,
loo_pred, med3) contain no reference to world_y/world_y2, hidden
values, the hidden standard, or case ids; world_y/world_y2 are called
only from the P2/P6 paths in main; the persistent revision flag is
written only inside learner_revise (on LOO license), never by the
harness; hidden judgments are computed in the harness section only and
never fed back into learner functions.

Verdict: REVISION-PASS (R0..R7 all pass).

## Honest interpretation

What this shows: the evaluation to action loop closed. Self-judgment
did real gating work: 14 failures triggered analysis, and the
learner's own attribution (computed from its training values plus the
observed consequence, no hidden information) licensed revision on
exactly the correctable class while leaving the irreducible SHIFT
class and the primitive-limited QUAD class alone. The adopted revision
generalized to fresh cases with new parameters (R7: err 4 -> 0 on the
WOBBLE-B class), and judgment agreement stayed at ceiling in both arms
with the revised rule still rejecting every genuinely bad commitment
(R5: 12/12).

What this does NOT show (pre-registered limits, restated): the
revision procedure (leave-one-out plus median) was researcher
specified in the prereg; the learner owns the trigger, the
attribution, and the adoption, not the invention of the procedure.
Agreement was expected at ceiling in both arms (the C337 loop was
already calibrated); the discriminating result is commitment quality
(R7), not judgment agreement. Consequences are exact, no noise; the
case sets are small (24 + 24); the WOBBLE-B correctability result is
specific to single-point corruption and is not claimed to generalize
to other corruption patterns.

Implementation note (transparent): the first build failed R0 because
the epoch-4 stamp was set only inside learner_revise, leaving E4=0 on
self-judged passes even though the P4 phase ran for every case. The
fix stamps the phase epoch on all revision-arm round-1 records in P4
while keeping the analysis itself trigger-gated (R1 still verifies
TRG == (SELF==0)). No bar was changed; the bar text is satisfied
literally. The failing build was discarded, not amended into a pass.

## Reproduction

```
cd docs/lab/research-lead/overnight-20260928/hcontlife5
~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 src/revise.zag -o bin/revise
./bin/revise | sha256sum   # expect bd893110b79a141ce855c367af46093ae614f8c57b797c27de627d0ac36b63c9
```

Audits: `grep -n "world_y" src/revise.zag` (definitions at 124/183,
P2/P6 call sites in main only); learner bodies clean per the
per-function greps above; `grep -n "set32(flag" src/revise.zag`
(single write inside learner_revise).
