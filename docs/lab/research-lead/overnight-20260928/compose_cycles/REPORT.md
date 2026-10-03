# REPORT: COMPOSE-CYCLES -- Verdict INFORMATIVE-FAIL (U)

Date: 2026-10-03. Worker: compose-cycles.
Battery: preregistered cycle-composition boundary test on the unified
behavior-contract composition operation U (COMPOSE-COLLAPSE, verdict
SUBSUMPTION). Pure Zag, pinned safebin znc. Prereg committed alone
before implementation (`35a9cfa`).

## Verdict: INFORMATIVE-FAIL (U)

U cannot compose cycles. The frozen U trial logic
(byte-identical `ref_uc_uni.zag`, main stripped), run on a meaningful
fixpoint-iteration workload whose answer requires 4 re-applications of
a structure, exhausts its entire proposal space -- 2 admitted singles,
2 admitted ordered pairs, 10 widened pairs -- and reports no solution
(ANS=-2, found=0), exactly as the prereg's depth-2 bound enumeration
predicted. This is not a bug in U; it is U's architecture: U's execution
rule is a BOUNDED DEPTH-2 PIPELINE TRIAL with no re-application of a
structure and no termination vocabulary. A 4-deep fixpoint iteration is
outside its proposal space by construction.

## Results

Build: `znc cyc_full.zag -o cyc_bin` (pinned safebin znc; native binary,
no external tools).

- `cyc_run1/2/3.txt`: 3/3 byte-identical, sha256
  `93e5b0d9c7de054d91f5a1d73f0b3fb7358d73a8a17f117ff1f47e6de89320e2`
- Report line: `ARM=UNI PROB=QC ANS=-2 TRIES=14`
- Trial trace (matches the frozen Section 5.1 enumeration exactly):
  - Singles: MAP 0 (STEP) -> 1002, MAP 2 (IDENT) -> 1101; MAP 1 and
    MAP 3 kind-rejected (out{2} vs kout=1). Neither is 1005.
  - Admitted pairs: (0,2): INTER=1002 -> 1002; (2,0): INTER=1001 ->
    1002. Neither is 1005.
  - WIDEN=1 fired (exhaustive admitted failure, learner-observed).
    Retried pairs: (0,1)->1, (0,3)->-2, (1,0)->2, (1,2)->2, (1,3)->-2,
    (2,1)->2, (2,3)->-2, (3,0)->-2, (3,1)->-2, (3,2)->-2.
    None is 1005.
- Census confirms zero success-recording: MAP contract observation
  counts (n=5,5,1,1) equal the teach counts exactly -- `observe` never
  fired, because no trial verified end-to-end. The failure left no
  spurious learned state behind.

## Kill bar results

- C1 COMMIT-ORDER: PASS. Prereg commit `35a9cfa` (PREREG.md +
  NAMECHECK.md only) strictly precedes the implementation commit
  (git log order verified).
- C2 DETERMINISM: PASS. 3/3 pairwise byte-identical (cmp); digest above.
- C3 U-BOUNDARY: PASS. UNI report line shows ANS=-2 (found=0),
  matching the frozen Section 5.1 enumeration byte for byte
  (INTER sequence, WIDEN=1, TRIES=14 all as predicted).
- C4 BASE-DIFF: PASS. `diff ref_uc_base.zag cyc_base.zag` shows
  exactly the three frozen Section-7 hunks (18c18 class comment,
  127a128,140 stepf, 133a147 exec_map branch); arena offsets and
  classes 0-3 untouched.
- C5 NO-CYCLE-HANDLER: PASS. `grep -c exec_map cyc_new.zag` = 0,
  `grep -c while cyc_new.zag` = 0. The driver poses the workload
  purely as data (facts + MAPs + teach) plus one `uni_solve` query;
  it implements no iteration and no fixpoint check.
- C6 OPACITY: PASS. Banned domain-story token grep over all built
  sources returns empty; every exercised identifier is a bare integer.

## Boundary characterization (the informative content of the FAIL)

Exercised code paths in the frozen U logic, in order:

1. `uni_admit_single` over 4 MAPs: admitted {0, 2} by kind-set
   compatibility (in{1}/out{1} vs kin=1/kout=1); rejected {1, 3}.
2. Single-MAP trial: each admitted MAP applied exactly once;
   end-to-end verification against exp=1005 failed.
3. `uni_admit_pair` over 12 ordered pairs: admitted {(0,2), (2,0)};
   each applied exactly once (x then y); verification failed.
4. WIDEN=1: the 10 filter-rejected pairs retried once (triggered solely
   by exhaustive admitted failure); verification failed.
5. Return with found=0, ANS=-2. No fallback beyond widening exists.

What is missing, precisely:

- (a) RE-APPLICATION: no construct applies a structure (or pair) more
  than once. The pair (0,0) -- STEP twice -- is not even proposable
  (x!=y), let alone STEP four times.
- (b) TERMINATION VOCABULARY: U has no way to express "stop when the
  output equals the input" (fixpoint), "stop on convergence signal",
  or "stop after k passes". Its only stop rules are "a trial verified
  end-to-end" and "trials exhausted".
- (c) STATE CARRY: each trial starts from the query's start subject s;
  there is no channel by which one trial's output becomes the next
  trial's input. A cycle is exactly such a channel plus (b).

The workload was designed (M1-M5, PREREG Section 3) so that (a)-(c)
are NECESSARY, not incidental: the fixpoint is 4 applications away
(M3, proven by the exhaustive enumeration above), termination is a
property of the state (M2, R(x)==x), and the evaluation signal is
adversarially non-monotonic (M4, counts 2,1,3,1,2), blocking naive
early-stopping. The driver contains no loop by audit (C5), so the
negative result is attributable to U's proposal space alone.

## What this does NOT show (honest limits)

- It does not show that NO extension of U could handle cycles; it
  shows the FROZEN U cannot, and exactly why.
- It tests one cycle family (fixpoint iteration, 4-chain). Oscillatory
  cycles, convergent-signal cycles, and multi-structure feedback cycles
  were not tested (pre-declared, PREREG Section 12).
- GEN was not tested: no GEN implementation exists (pre-declared).
- The oracle answer exp was supplied for end-to-end verification (as
  in the P6 battery); the test targeted U's proposal space.

## General-principle direction (not implemented; for a follow-up battery)

Per PREREG Section 11 (frozen before results): the missing principle
must be general, never a cycle handler. Preregistered shape: generalize
U's "ordered trial" from {singles, ordered pairs, each applied once} to
TRIAL OVER RE-APPLICABLE STRUCTURE SEQUENCES WITH LEARNED HALTING --
a proposed sequence (repetitions allowed) executes stepwise; after each
step a halting condition is checked; halting is expressed in the existing
contract vocabulary (output-kind HALT signal, output==input fixpoint, or
step cap); end-to-end verification retained. Pipelines are the special
case (halt after one pass); cycles are sequences with data-dependent
halt. It reduces to U exactly when sequences are restricted to length
<= 2 with halt-after-once: a strict generalization, not a parallel
engine. Implementing and testing this needs its own preregistered
battery; this lane only establishes the boundary it must cross.

## Disclosed implementation fixes (honest record)

Two deviations, both mechanical, both disclosed:

1. `build.sh` C4 audit: the first draft filtered diff `>`-lines by a
   keyword allowlist that missed stepf body lines (`let n...`,
   `i=i+1;`). Replaced with an exact hunk-header check
   (`18c18`, `127a128,140`, `133a147`), which is the precise reading
   of the frozen C4 bar ("shows exactly the Section 7 edits").
2. `cyc_new.zag` comment rewording: a header comment mentioned the
   token `exec_map`, tripping the frozen mechanical C5 grep
   (`grep -c exec_map ... == 0`). Reworded the comment to "no direct
   structure-application call"; no code changed. The file genuinely
   contains no such call.
