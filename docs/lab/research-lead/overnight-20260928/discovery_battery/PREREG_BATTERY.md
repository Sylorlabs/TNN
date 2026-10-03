# PREREG: Minimal Discriminating Battery for Program Discovery (Battery v1)

Date: 2026-09-30.
Status: FROZEN PREREGISTRATION. No implementation is authorized by this document.
Authority: freezes section 6 of `arch_review/ARCHITECTURE_REVIEW.md` (commit 18be93c3e).
Scope: all four discovery hypotheses (A residual, B fragments, C counterexample growth, D MAP-Elites control).

## 0. Commit order bar

This prereg commit must strictly precede the first implementation commit of every
hypothesis (A, B, C, D). Verified by `git merge-base --is-ancestor` before any
battery result is accepted. Any hypothesis implementation whose ancestry does not
contain this commit is void for battery purposes.

## 1. Frozen substrate (K1)

The GENEXEC2 interpreter exactly as committed in 8d5f58b89. No VM edits during
hypothesis evaluation. Any run executed against a modified interpreter is void.

Frozen op set (opcodes as in 8d5f58b89):
PUSH(c) with c in -9..9, IN0, IN1, ADD, SUB, MUL, DIV, MOD, NEG, DUP, DROP,
SWAP, OVER, LT, EQ, GT, JZ(k), JNZ(k), JMP(k), CALL(f), RET.
Result of a program is the top of stack after execution.
DIV edge semantics: divisor zero yields 0, else truncated a/b.
MOD edge semantics: divisor zero yields 0, else nonnegative mod_nonneg(a,b).
Underflowed stack operations are no-ops, exactly as in the committed interpreter.

Each hypothesis is new construction machinery over this frozen VM. The review's
R5 bar stands: a beam variant (population of candidate programs grown by
appending ops, retained by ranking on a scalar output score, fixed width or CAP)
is banned for hypotheses A, B, C. Larger beams, reweighted scores, and
task specific prefix protection are excluded.

## 2. Frozen task episodes (K1)

Fixed order T0 through T6. Persistent hypothesis state (libraries, fragments,
archives, counters) is carried across tasks in this order and the per task
report includes a persistent state diff. Train episodes are the only episodes a
hypothesis may use for decisions. Held-out episodes are scored after the
hypothesis reports, never during construction.

- T0 2x+1: train x in 0..8 (9 episodes). Held-out x in -8..-1 and 9..16 (16).
- T1 abs: train x in -8..8 (17). Held-out x in -12..12 excluding -8..8 (8).
  Matches the GENEXEC2 held-out exactly.
- T2 mod3: train x in 0..16 (17). Held-out x in 17..33 (17).
- T3 parity: train a,b in 0..4 (25). Held-out a,b in 0..7 excluding the 0..4
  square (39). Target is 1 if (a+b) even else 0.
- T4 nested abs: train x in -6..6 (13), target ||x|-2|.
  Held-out x in -10..10 excluding -6..6 (8).
- T5 fragment composition: train x in -4..8 (13), target |x|+|x-2|.
  Held-out x in -8..12 excluding -4..8 (8).
- T6 adversary: sealed (section 5). At least 9 train and at least 8 held-out
  episodes, held-out disjoint from train, both fixed in the sealed spec.

SOLVE is defined as exact integer equality of top of stack with the target on
ALL train episodes. Partial credit is reported as exact count but does not
count as SOLVE. Hidden accuracy is the fraction of held-out episodes exact,
reported separately; it is not part of SOLVE.

## 3. Frozen budget (K1)

Per (hypothesis, task): 1,000,000 candidate evaluations OR 300 seconds wall
clock, whichever is reached first. Budget exhaustion without SOLVE is recorded
as FAIL for that task. One candidate evaluation is defined as one candidate
program executed against the full train episode set. Wall clock is measured per
task from first construction step to report.

Determinism: 3 runs per (hypothesis, task), byte identical on the frozen seed
recorded in the hypothesis's own prereg. Non identical runs are invalid; the
hypothesis run is void until determinism is achieved and explained.

## 4. Frozen metrics (K1)

Reported per (hypothesis, task), in the committed result file:
1. train exact count and SOLVE/FAIL verdict;
2. hidden accuracy on held-out episodes;
3. candidate evaluations consumed;
4. wall clock seconds;
5. examples consumed: distinct train episodes used for construction decisions
   (for passive methods this equals the train count; for active methods the
   count actually queried);
6. partial structures retained at termination (integer; the hypothesis prereg
   defines what counts, the battery requires the number);
7. library state: fragments promoted during the task, total library size,
   CALL count in the final program per fragment id;
8. reuse events: each use on task j of a fragment induced on task k<j,
   with fragment id and both task ids;
9. final bytecode length: main program op count plus the op counts of all
   called fragment bodies;
10. construction trace with the mechanism mandatory events of section 4;
11. persistent state diff across the task sequence;
12. transfer: for T4, T5, T6, evaluations to SOLVE with carried state AND with
    fresh state (fresh state rerun), reported as a pair. Carried is primary.

## 5. Confirmation rule (K2)

The review's discrimination matrix is frozen as the outcome prediction set:

Task          | A residual | B fragments | C cex growth | D MAP-Elites
2x+1 (T0)     | SOLVE      | SOLVE       | SOLVE        | SOLVE
abs (T1)      | FAIL       | SOLVE       | SOLVE        | FAIL
mod3 (T2)     | SOLVE      | SOLVE       | SOLVE        | SOLVE
parity (T3)   | SOLVE      | SOLVE       | SOLVE        | SOLVE
nested (T4)   | FAIL       | SOLVE       | SOLVE        | FAIL
fragcomp (T5) | FAIL       | SOLVE       | SOLVE        | FAIL
adversary T6  | conditional| conditional | conditional  | conditional

A prediction is CONFIRMED if and only if (a) the observed outcome matches the
predicted outcome under the frozen SOLVE definition, AND (b) the committed
construction trace shows the predicted mechanism via the mandatory events
below, verified by independent inspection of the committed trace. Outcome match
without mechanism trace is recorded as UNCONFIRMED: it neither confirms nor
falsifies.

Mechanism mandatory trace events (per hypothesis, key tasks):
- A on T0: residual vector logged per construction step; the step choosing
  PUSH 1 then ADD must be justified in the trace by a constant residual of 1;
  no ranked population of candidate programs anywhere in the trace.
- A on T1: predicted FAIL; the trace must show the failure report with a
  sign partitioned residual (diagnosis, not success).
- A on T2/T3: SOLVE with residual driven steps; the T3 trace must show the
  residual defined over the joint input (a, b).
- B on T1: induction event for the ABS fragment carrying its semantic
  signature on the probe set, with the substructure it was extracted from.
- B on T4: at least 2 retrieval events for the ABS fragment (behavioral match
  recorded before each CALL) and at least 2 CALLs to the same fragment id in
  the final program.
- B on T5: at least 2 CALLs to the ABS fragment with retrieval events.
- B on T2: induction event for a periodic fold fragment.
- C on T1: exactly the predicted split discipline: linear repair attempted and
  shown failing the no-breakage check on both sides, then one split event on a
  probe separating x<0 from x>=0 (for example [IN0, PUSH 0, LT]), each branch
  repaired; final program has 2 regions and 0 CALLs.
- C on T4: at least 2 nested split events with probes and partitions; final
  program has 0 CALLs. This is the KEY DISCRIMINATOR against B on the same
  task: B shows CALLs plus retrieval, C shows splits and zero CALLs.
- C on T0/T2/T3: repair events only (counterexample episode, appended op,
  passing set preserved by re-evaluation), no splits.
- D on T0: niche insertion records showing the deceptive prefix
  [IN0, PUSH 2, MUL, PUSH 1] retained in its niche independent of score, then
  ADD appended by mutation. This tests the P1 postmortem claim directly.
- D on T1/T4/T5: predicted FAIL (no conditional machinery). Any SOLVE on
  these tasks invalidates the control (see control validity).

Falsifiers (frozen from the review; any firing falsifies the named claim):
- A-F1: A fails T0 or T2. The residual complexity driver is inadequate; A is
  falsified.
- A-F2: the trace shows multiple candidate programs ranked by a residual
  score. A collapses into the banned beam class and is rejected as genuinely
  different.
- A-F3: A solves T1 straight line. Investigate before any claim: either the
  op alphabet secretly expresses abs without comparison (VM or task flaw) or
  conditional machinery was smuggled in.
- B-F1: T4 or T5 solved with no semantic retrieval events in the trace, or
  retrieval precision at chance. The composition claim is falsified.
- B-F2: induced fragments are byte identical whole task solutions reused
  verbatim with no substructure extraction step in the trace. B collapses to
  GENEXEC2 P2 and is falsified as genuinely different.
- B-F3: the library accumulates near duplicate fragments with no behavioral
  dedup of the index. The semantic indexing claim is falsified; the mechanism
  is memoization, not induction.
- C-F1: C fails T0. The repair operator is inadequate; C is falsified.
- C-F2: C's T4 trace shows fragment CALLs instead of nested splits, or B's T4
  trace shows splits instead of CALLs. The mechanism claim is falsified.
  Traces are mandatory, not just outcomes.
- C-F3: split count grows with episode count rather than true regions (split
  count far exceeds true regions on T6). The split discipline is falsified;
  the mechanism is overfitting, not structural growth.
- C-F4: the repair step maintains a ranked population of candidate repairs.
  That is beam search inside the repair operator; C is rejected as genuinely
  different.
- D-F1 (control validity): D fails T0. The control is misconfigured and must
  be fixed before serving as a baseline.
- D-F2 (control validity): D solves T4 or T5. Either the tasks are straight
  line solvable (task design flaw, check the found program) or conditional or
  fragment machinery leaked into the control. Invalidate and fix.
- Review level: if all four hypotheses FAIL tasks T0 through T5 within the
  frozen budget, the review's assessment (discovery is the defect, not the VM)
  is overturned and a VM level review replaces further discovery work.

No L3 claim follows from battery success alone. After a CONFIRMED battery, the
mandatory Criterion 0 sequence applies: source audit (where do the final
procedure semantics live), then persistence, reuse, transfer, revision, and
adversarial unseen structure tests.

## 6. Adversary T6 sealed design protocol (K3)

T6 is designed by an independent adversary AFTER all four hypothesis
implementations freeze. This prereg freezes the design constraints and the
sealing protocol, not T6 itself.

Designer and timing:
- The T6 adversary is a worker independent of all hypothesis implementers.
- The T6 spec commit must strictly follow every hypothesis implementation
  freeze commit (verified by git ancestry) and strictly precede any T6
  evaluation run.
- Hypotheses are evaluated on T6 train episodes only after the seal; the
  implementers never see T6 before their mechanisms freeze. The seal is
  one directional.

Validity constraints on the sealed T6 (all mandatory):
- V1 computability: a target program exists in the frozen op set; the
  adversary exhibits it and logs its exact outputs on all train and held-out
  episodes of the sealed spec.
- V2 material difference: T6 must require a structure materially different
  from T0..T5. It must not be a straight line arithmetic map, a single kink
  absolute value, a periodic mod, or a two input parity. The exhibited target
  program must contain at least one of JZ, JNZ, JMP, CALL.
- V3 budget adequacy: the exhibited target program has at most 40 ops total
  (main plus called fragments), keeping T6 inside the adequacy envelope.
- V4 episodes: at least 9 train episodes and at least 8 held-out episodes,
  held-out disjoint from train, both fixed in the sealed spec.
- V5 no reverse engineering: the adversary records which conditional
  predictions T6 is intended to discriminate, but T6 must satisfy V2 on its
  own structural merits, independent of the predictions.

Sealing protocol:
- S1: the adversary writes T6_SPEC.md (function definition, exact train and
  held-out episode lists, exhibited target program, verification run log)
  into a sealed directory.
- S2: the adversary commits it alone and records the sha256 of T6_SPEC.md in
  the evaluation log.
- S3: at evaluation time the harness exposes ONLY the train episodes to each
  frozen hypothesis. Held-out episodes and the target program are revealed
  only after all hypotheses report on T6.
- S4: any T6 evaluation run whose ancestry does not show the seal commit
  after all implementation freeze commits is void.

Evaluation of the staked conditional predictions on the sealed T6:
- A: SOLVE iff the sealed function's residual decomposes through constant
  seeking steps; the trace decides.
- B: SOLVE iff T6 decomposes into subpatterns matching induced fragment
  signatures; FAIL with no novel primitive required is the sharpest C0-C
  signal for B.
- C: SOLVE iff T6 is piecewise with repairable regions; the split count in
  the trace should track the true region count (C-F3 guards overfitting).
- D: SOLVE iff T6 is straight line synthesizable within budget; V2 makes
  this unlikely by construction, so a D SOLVE on T6 triggers a V2 audit.

## 7. Governance

- Pure Zag for all hypothesis implementations, harnesses, and evaluation
  scripts. No Python anywhere, including scratch analysis.
- No threshold weakening after results. If this protocol needs a fix, amend
  transparently, re-freeze, and void results taken under the old protocol.
- This document contains no em dashes, verified by byte grep before commit.
- Battery results are reported per hypothesis with all 12 metrics of section
  4 committed alongside raw logs. Builders report BUILD-PASS or BUILD-FAIL
  against their own preregistered bars; battery confirmation is evaluated
  separately under section 5.
