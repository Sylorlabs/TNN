# PREREG: CYCLES-FEEDBACK -- Does Sequences+Halting Handle Multi-Structure Feedback Cycles?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all implementation.

## 1. Question

C428 (CYCLES-CONVERGENT, verdict PASS, 2026-10-03) closed the
convergent-signal family: interior answers at depth 3 and 5 on a
no-limit chain and arrival at the walk limit all solve via bounded
exact-length trials with end-of-pass termination, and the (b) fixpoint
halt is verified exact-equality-specific (silent across all convergent
runs including limit arrival). From C420's boundary list, the one
remaining untested cycle family is multi-structure feedback cycles.
This battery closes the cycle family map.

A multi-structure feedback cycle: a closed trajectory whose every
closure path necessarily traverses two or more distinct structures.
Concretely: structure A transforms region X to region Y, structure B
transforms region Y back to region X. Neither structure's relation
contains a directed cycle on its own (each is a DAG in isolation);
the cycle is emergent from A+B composition. A's output feeds B and
B's output feeds A. This differs from every family tested so far:

- fixpoint (GEN-CYCLES): one structure re-applied, trajectory reaches
  a taught identity and the (b) halt is the operative stop.
- oscillatory (C425): one structure re-applied, the cycle lives
  inside a single MAP's relation ([0,0,0,0] wins).
- convergent (C428): one structure re-applied, trajectory through
  fresh states, interior or limit answer.
- alternating chain (C420 T1): two structures alternate, but the
  trajectory is linear through fresh states toward a taught fixpoint
  ([0,1,0,1,0] never revisits a state). The alternation is fact
  layout, not feedback.

The feedback test is the revisit: the composed trajectory returns to
a previously visited state, and every return path uses both
structures. The frozen halting vocabulary is unchanged: (a) miss
v<0, fail; (b) v==prev, break (exact equality only); (c) i>=cap,
break; (d) end of pass. The question: does the frozen mechanism run
genuine A/B feedback loops with correct termination (end-of-pass,
(b) silent on the winner, (b) honestly halting the losing trials
that walk into dead ends), with no new principle?

Three tests, all on the fully FROZEN mechanism and base (gc_uni.zag +
gc_base.zag, zero modifications, no extensions):

- QF1 (feedback loop, full-loop return): a period-4 loop through
  both structures; query starts on the loop, answer is the start
  state after one full A,B,A,B pass. Tests that the mechanism runs
  the genuine feedback alternation [0,1,0,1] with (b) silent on the
  winner.
- QF2 (feedback lasso: 2-step tail + period-4 2-structure loop):
  entry via structure A into the loop; query starts at the tail,
  answer is the first repeated state (seen at step 2, repeated at
  step 6). Tests tail entry into feedback: the winner must run the
  tail and then exactly one full loop pass, stopping at the
  detection-point parity.
- QF3 (feedback loop, mid-loop stop): same loop as QF1; query starts
  on the loop, answer is an interior loop state 3 loop-steps away.
  Tests exact-length stopping inside the loop: the win is [0,1,0] at
  k=3 by end-of-pass, proving termination is trial-length matching,
  not revisit detection (the vocabulary has no repeat check).

## 2. Frozen mechanism (untouched; tested, not redesigned)

`gc_solve` in gc_uni.zag (sha256
33cbd90db2ce77fb837a6542f70a8758f72e3210d6b9d6d5db4d325b035b03f6):
frozen uni_solve prefix (admitted singles, admitted ordered pairs x!=y,
WIDEN=1 retries rejected x!=y pairs; [i,i] pairs are never tried in the
prefix), then for k=3..seqmax lexicographic sequences admitted by the
chain kind rule, executed stepwise with halting (a) miss v<0 fail,
(b) v==prev break, (c) i>=cap break, (d) end of pass; success iff halted
value == exp; every step of a winning trial recorded via observe.
Base gc_base.zag (sha256
0a12cc9a4f9b10fc8c4ce2a2f65294d48d8d402f827ceeb9d3d6126e754cb125),
U region uni_nomain.zag (sha256
e741ecde990d55345e2fe3aa794c75aa11a8fc5d5c54cf995aa38cb5dfcbb1b3).
All copied with sha256 verification; F7 audits they are unmodified.

Bounds: SEQMAX=8, CAP=8 (frozen values, not learned; the claim under
test is the halting vocabulary over feedback, not the bound values).
Under SEQMAX=CAP=8 the (c) cap halt can never fire strictly before
end-of-pass. Note stepf semantics: STEP with no outgoing edge returns
its input (identity at a dead end); (b) still requires v==prev, i.e.
two consecutive equal values.

## 3. Workload designs and frozen predictions

Shared inventory (every exercised identifier is a bare integer):
m0 = class 4 STEP on 801 (structure A: X region to Y region);
m1 = class 4 STEP on 802 (structure B: Y region back to X region);
m2 = class 1 COUNT on 605; m3 = class 1 COUNT on 606
(distractors, block reused from cycles_oscillatory/cycles_convergent:
nothing collides with the 79xx-81xx/89xx states).
Distractor facts: (6101,605,6102); (6201,606,6202),(6201,606,6203).
Teaches: m2: (6101,1); m3: (6201,2).
Learned masks: m2/m3 in{1} out{2} (the count values 1 and 2 are never
fact subjects, so they stay kind 2).

Feedback edge sets (preregistered; F10 audits the setups match):
- rel 801 (structure A): 8001->8101, 8002->8102; plus the QF2-only
  tail 7999->8000, 8000->8001. As a directed graph this is a DAG:
  no 801-only directed cycle exists.
- rel 802 (structure B): 8101->8002, 8102->8001, and the trap edge
  8001->8999 (8999 is a dead end: never a fact subject, no outgoing
  edges). As a directed graph this is also a DAG: no 802-only
  directed cycle exists.
- The only directed cycle in the union is the emergent feedback
  loop 8001->8101->8002->8102->8001, which uses both relations.
  Genuine feedback: A's output (81xx) feeds B, B's output (80xx)
  feeds A.

Why no trivial single wins (documented, not hidden): with exp=s on
the loop (QF1), a STEP MAP with no outgoing edge at s would act as
identity and win as a single without ever running the loop (the
C425 IDENT problem). Here m0 has an outgoing 801 edge at 8001
(8001->8101), and m1's 802 edge at 8001 leads to the 8999 dead end
(a deliberate trap: sequences that take it die honestly via the (b)
halt at 8999). So no structure is identity at s, and the loop must
be run.

Admission fact used by all three: at every k in 3..8 exactly the
{0,1}^k sequences are admitted (2^k of them). Any occurrence of 2/3
breaks an adjacency (out{2}={2} against every in mask {1}) or the
final kout check (out{2}={2} does not contain kout=1). Hence the
prefix is identical in all three worlds: 2 admitted singles ([0]:
one hop; [1]: to the trap or identity), 0 admitted x!=y pairs
beyond [0,1] and [1,0], WIDEN=1 retries the 10 rejected pairs (all
fail on COUNT miss or dead-end; each pair trial prints exactly one
INTER= line, the v1 value).

Learned masks: m0 in{1} out{1} (all 80xx/81xx states are fact
subjects); m1 in{1} out{1,2} (8999 is an object but never a
subject, so bit 2 is set by the trap teach).

### 3.1 QF1: feedback loop, full-loop return (PROB=QF1)

setup_qf1:
- Facts: (8001,801,8101), (8002,801,8102),
  (8101,802,8002), (8102,802,8001), (8001,802,8999).
- m0 teaches: (8001,8101), (8002,8102).
- m1 teaches: (8101,8002), (8102,8001), (8001,8999).
- Query: s=8001, kin=1, kout=1, exp=8001, nm=4, seqmax=8, cap=8.
- The answer is one full loop pass away: 8001->8101->8002->8102
  ->8001. Termination: end-of-pass after a bounded run of exactly
  4 steps; (b) silent on the winner (all adjacent values distinct).

Frozen execution:
- Singles: [0] admitted: 8001->8101 != 8001 (1 try, no INTER print).
  [1] admitted: 8001->8999 != 8001 (1 try). [2],[3] rejected.
- Pairs: [0,1] admitted: 8001->8101->8002 != 8001 (1 try, one
  INTER= line). [1,0] admitted: 8001->8999->8999 != 8001 (1 try).
  WIDEN=1: 10 rejected pairs, all fail (one INTER= line each).
  12 tries total in the pair phase.
- k=3: 8 admitted ({0,1}^3), all fail: [0,0,0] and [0,0,1] (b)-halt
  at step 2 (A at 8101 has no 801 edge) with cur=8101; [0,1,0]
  ends 8102; [0,1,1] (b)-halts at step 3 (B at 8002 has no 802
  edge) with cur=8002; [1,*,*] (b)-halt at step 2 with cur=8999.
  8 tries. No 3-step return to 8001 exists (only B at 8102 leads
  into 8001, unreachable in 2 steps from 8001).
- k=4: 16 admitted ({0,1}^4). n=0..20 all fail; n=21 [0,1,0,1]
  admitted: 8001->8101->8002->8102->8001, end-of-pass,
  cur=8001 == exp. SUCCESS. 22 tries. The [0,1,0,1] alternation is
  the unique 4-step return (any (b)-halted trial ends stuck at
  8101/8102/8002/8999, none of which is 8001).
- k=5..8 never run; no WIDEN=2 (a win stops the search).

Predictions:
- Report: `ARM=GC PROB=QF1 ANS=8001 TRIES=44` (2 + 2 + 10 + 8 + 22).
- Trace: the last 4 INTER= lines before the QF1 report are
  8101,8002,8102,8001 (the winning trial; no early halt fired).
- Census: m0 inmask=1 outmask=1 n=4 (2 teaches + 2 trial observes);
  m1 inmask=1 outmask=3 n=5 (3 teaches + 2 trial observes);
  m2/m3 inmask=1 outmask=2 n=1.

### 3.2 QF2: feedback lasso, tail entry (PROB=QF2)

setup_qf2:
- Facts: (7999,801,8000), (8000,801,8001) [2-step tail into the loop],
  (8001,801,8101), (8002,801,8102),
  (8101,802,8002), (8102,802,8001), (8001,802,8999).
- m0 teaches: (7999,8000), (8000,8001), (8001,8101), (8002,8102).
- m1 teaches: (8101,8002), (8102,8001), (8001,8999).
- Query: s=7999, kin=1, kout=1, exp=8001, nm=4, seqmax=8, cap=8.
  exp=8001 is the first repeated state: first seen at step 2,
  repeated at step 6 (one full loop pass later).
- Termination: end-of-pass after a bounded run of exactly 6 steps;
  (b) silent on the winner.

Frozen execution:
- Singles: [0]: 7999->8000 != 8001 (1 try). [1]: 7999->7999
  (no 802 edge: identity) != 8001 (1 try). [2],[3] rejected.
- Pairs: [0,1]: 7999->8000->8000 != 8001 (1 try). [1,0]:
  7999->7999->8000 != 8001 (1 try). WIDEN=1: 10 rejected pairs,
  all fail. 12 tries in the pair phase.
- k=3: 8 admitted, all fail ([0,0,0] ends 8101; [0,0,1] ends 8999;
  [0,1,*] (b)-halt at step 2 with cur=8000; [1,*,*] (b)-halt at
  step 1 with cur=7999). 8 tries.
- k=4: 16 admitted, all fail ([0,0,0,0]/[0,0,0,1] variants end
  8101/8002 or (b)-halt; [0,0,1,*] die at 8999; the rest (b)-halt
  at step 1 or 2). 16 tries.
- k=5: 32 admitted, all fail ([0,0,0,1,0] ends 8102; [0,0,0,1,1]
  (b)-halts at step 5 with cur=8002; the rest die earlier).
  32 tries. No 5-step arrival at 8001: arrivals happen at steps
  2, 6, 10, ... (period 4 after first sighting).
- k=6: 64 admitted. n=0..4 fail (all (b)-halt at step 4 with
  cur=8101, or die at 8999, or end 8102); n=5 [0,0,0,1,0,1]
  admitted: 7999->8000->8001->8101->8002->8102->8001,
  end-of-pass, cur=8001 == exp. SUCCESS. 6 tries. The winner is
  the unique 6-step arrival (tail [0,0] then loop [0,1,0,1]).
- k=7..8 never run; no WIDEN=2.

Predictions:
- Report: `ARM=GC PROB=QF2 ANS=8001 TRIES=76`
  (2 + 2 + 10 + 8 + 16 + 32 + 6).
- Trace: the last 6 INTER= lines before the QF2 report are
  8000,8001,8101,8002,8102,8001.
- Census: m0 inmask=1 outmask=1 n=8 (4 teaches + 4 trial observes);
  m1 inmask=1 outmask=3 n=5 (3 teaches + 2 trial observes);
  m2/m3 inmask=1 outmask=2 n=1.

### 3.3 QF3: feedback loop, mid-loop stop (PROB=QF3)

setup_qf3: same facts, MAPs, and teaches as setup_qf1.
- Query: s=8001, kin=1, kout=1, exp=8102, nm=4, seqmax=8, cap=8.
  exp is an interior loop state, 3 loop-steps away:
  8001->8101->8002->8102.
- Termination: end-of-pass after a bounded run of exactly 3 steps;
  (b) silent on the winner. This is the feedback analog of QC1:
  the trial stops at an interior point of the loop by exact-length
  matching, not by any revisit detection.

Frozen execution:
- Singles: [0]: 8001->8101 != 8102 (1 try). [1]: 8001->8999
  != 8102 (1 try). [2],[3] rejected.
- Pairs: [0,1]: 8001->8101->8002 != 8102 (1 try). [1,0]:
  8001->8999->8999 != 8102 (1 try). WIDEN=1: 10 rejected pairs,
  all fail. 12 tries in the pair phase.
- k=3: 8 admitted. n=0 [0,0,0]: (b)-halt at step 2, cur=8101.
  n=1 [0,0,1]: (b)-halt at step 2, cur=8101. n=2 [0,1,0]
  admitted: 8001->8101->8002->8102, end-of-pass,
  cur=8102 == exp. SUCCESS. 3 tries. The [0,1,0] win is the
  unique 3-step arrival at 8102 (only A at 8002 leads into 8102,
  reached in 2 steps only by [0,1]).
- k=4..8 never run; no WIDEN=2.

Predictions:
- Report: `ARM=GC PROB=QF3 ANS=8102 TRIES=17` (2 + 2 + 10 + 3).
- Trace: the last 3 INTER= lines before the QF3 report are
  8101,8002,8102.
- Census: m0 inmask=1 outmask=1 n=4 (2 teaches + 2 trial observes);
  m1 inmask=1 outmask=3 n=4 (3 teaches + 1 trial observe);
  m2/m3 inmask=1 outmask=2 n=1.

## 4. Pre-declared analysis: feedback and the halting vocabulary

The frozen vocabulary has no revisit check and no structure-aware
stop; a "stop when the loop closes" signal is not expressible. For
the value queries in this battery that gap is observationally
equivalent to bounded exact-length trials, preregistered here: over
the 2-structure loop of period 4, with d loop-steps from s to exp
along the deterministic walk, the alternating trial [0,1,...] wins
for the smallest k>=3 with k congruent to d mod 4 on-loop
(repetitions are never tried at k=2; the prefix enumerates x!=y
only), provided k<=8 and the kind masks admit. QF1: d=4, k=4.
QF3: d=3, k=3. QF2: tail t=2 then d=4 loop steps, k=6. All within
SEQMAX=8.

The (b) halt plays an honest supporting role here that it did not
play in the oscillatory/convergent batteries: losing trials that
walk a structure into a dead end (A at 8101/8102, B at 8002, either
at 8999) are stopped by output==input, which is the correct
fixpoint signal at a dead end, and it never misfires on a winning
trial because adjacent loop values are always distinct. The trap
edge 8001->8999 additionally tests that the search is not lured by
a plausible-looking B step: every sequence taking it dies at 8999
via (b) and the true loop is still found.

A feedback loop with a self-loop edge (adjacent equal values on the
intended trajectory) would (b)-halt mid-loop; that is the correct
fixpoint semantics, not a failure of feedback handling, and is not
tested here. Data-dependent stop-at-loop-closure (period unknown at
query time, continuation past closure destroying the answer) would
need a new principle; characterized here, not implemented. If any
of F3/F4/F5 fails, the REPORT characterizes the failure as
INFORMATIVE-FAIL per Section 7 rather than patching the vocabulary.

## 5. Build plan

1. Lane repo init (done). This PREREG.md + NAMECHECK.md commit alone.
2. Copy frozen sources with sha256 verification: gc_uni.zag,
   gc_base.zag, uni_nomain.zag.
3. Write qf_setups.zag (setup_qf1, setup_qf2, setup_qf3),
   qf_main.zag (three queries, reports, censuses).
4. Assemble: qf_full.zag = gc_base.zag + uni_nomain.zag + gc_uni.zag
   + qf_setups.zag + qf_main.zag. One binary qf_fbin (the mechanism
   is fully frozen; no extension, no control, no reduction needed).
   Compile with pinned safebin znc. Run 3x, pairwise cmp.
5. build.sh encodes all audits fail-closed (set -e): toolchain guard,
   frozen digests, 3/3 cmp, report-line greps, trace-tail greps,
   no-WIDEN=2 check, census greps, feedback-edge audit (F10),
   setup-hygiene grep (F9), opacity grep (F8).

## 6. Frozen kill bars

- F1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Steps 0-2 + .gitignore ONLY) strictly precedes all
  implementation commits (audited via the lane-local git log).
- F2 DETERMINISM: PASS iff 3/3 runs of qf_fbin are pairwise
  byte-identical (cmp); digests recorded.
- F3 QF1-PASS: PASS iff the binary reports
  `ARM=GC PROB=QF1 ANS=8001 TRIES=44`, no WIDEN=2 appears in the QF1
  section, and the last 4 INTER= lines before the QF1 report are
  8101,8002,8102,8001.
- F4 QF2-PASS: PASS iff the binary reports
  `ARM=GC PROB=QF2 ANS=8001 TRIES=76`, no WIDEN=2 in the QF2 section,
  and the last 6 INTER= lines before the QF2 report are
  8000,8001,8101,8002,8102,8001.
- F5 QF3-PASS: PASS iff the binary reports
  `ARM=GC PROB=QF3 ANS=8102 TRIES=17`, no WIDEN=2 in the QF3 section,
  and the last 3 INTER= lines before the QF3 report are
  8101,8002,8102.
- F6 CENSUS: PASS iff every CENSUS line matches the Section 3
  predictions exactly (QF1: m0 inmask=1 outmask=1 n=4, m1 inmask=1
  outmask=3 n=5; QF2: m0 inmask=1 outmask=1 n=8, m1 inmask=1
  outmask=3 n=5; QF3: m0 inmask=1 outmask=1 n=4, m1 inmask=1
  outmask=3 n=4; m2/m3 inmask=1 outmask=2 n=1 in all three worlds).
- F7 FROZEN-INTACT: PASS iff the lane copies of gc_uni.zag,
  gc_base.zag, uni_nomain.zag match the Section 2 digests.
- F8 OPACITY: PASS iff grep over all built sources for banned
  domain-story tokens
  `hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent`
  (case-insensitive) returns empty, AND every exercised identifier is
  a bare integer.
- F9 SETUP-HYGIENE: PASS iff qf_setups.zag contains no iteration
  (`while`), no repeat/period check, and no direct `exec_map` call:
  setups pose facts + MAPs + teaches only, the same discipline as
  C428's cc_setups.zag.
- F10 FEEDBACK-GENUINE: PASS iff the 801 edge list extracted from
  qf_setups.zag is exactly {8001->8101, 8002->8102} plus the
  QF2-only tail {7999->8000, 8000->8001}, the 802 edge list is
  exactly {8101->8002, 8102->8001, 8001->8999}, and neither edge
  list contains a directed cycle on its own (audited by inspection
  of the extracted lists against this preregistered inventory).

## 7. Verdict mapping

- F1/F7/F8/F9/F10 FAIL -> VOID.
- F2 FAIL -> UNDECIDED (name the decisive rerun).
- F3 FAIL -> INFORMATIVE-FAIL (feedback loop): the frozen mechanism
  does not run the basic 2-structure feedback loop; REPORT
  characterizes the missed or misfired trial (in particular whether
  the (b) halt fired spuriously on the winner or the search was
  lured by the 8999 trap edge).
- F4 FAIL (with F3 PASS) -> INFORMATIVE-FAIL (tail entry): the loop
  runs on-loop but tail entry into feedback does not; REPORT says
  which step diverged.
- F5 FAIL (with F3/F4 PASS) -> INFORMATIVE-FAIL (mid-loop stop):
  full-loop and lasso feedback work but interior loop stopping does
  not; REPORT characterizes why.
- F6 FAIL -> INFORMATIVE-FAIL (contracts): kind-mask learning moved
  under feedback; investigate before any claim.
- All PASS -> PASS: the frozen sequences+halting mechanism handles
  multi-structure feedback cycles (full-loop return, tail-entry
  lasso, mid-loop stop) with zero mechanism change; the cycle is
  emergent from A+B composition (neither structure cycles alone);
  termination is by bounded exact-length trial (end-of-pass) with
  the (b) halt correctly silent on winners and honestly stopping
  dead-end losers; the loop-closure vocabulary gap of Section 4 is
  observationally equivalent for these value queries.

## 8. Honest boundaries (pre-declared)

- Bounded runs only: the battery covers fixed-length value queries;
  data-dependent stop-at-loop-closure is not in the halting
  vocabulary (see Section 4 for the exact equivalence claim).
- exp is still supplied for end-to-end verification; the tests target
  the proposal space and the halting vocabulary over feedback.
- SEQMAX=8/CAP=8 remain frozen researcher bounds, not learned values.
  A feedback loop of period 9+, or an answer needing k>8, would fail
  on bounds; not tested here. Under SEQMAX=CAP=8 the (c) cap halt can
  never fire strictly before end-of-pass.
- No IDENT MAP in the inventory (documented in Section 3); the
  distractor inventory is COUNT-only by design, matching C425/C428.
  The no-trivial-single argument is documented in Section 3 rather
  than hidden.
- Overshoot trials (k>d) are never executed: the increasing-k search
  stops at the first win, so exact-length matching is established
  from below only.
- The (b) halt is exact-equality-specific by construction; this
  battery verifies it stays silent on all three winning feedback
  trials while honestly stopping the dead-end losing trials.
- This battery closes the cycle family map from C420's boundary
  list: fixpoint, alternating-chain, oscillatory, convergent-signal,
  and now multi-structure feedback cycles are all tested.

## 9. Predicted outcome

PASS expected on F3/F4/F5 with the exact TRIES values, INTER tails,
and census lines of Section 3. The predicted scientific result: the
frozen sequences+halting mechanism handles multi-structure feedback
cycles with no mechanism change, extending the composition envelope
(pipelines, fixpoint sequences, alternating chains, data-dependent
halting, HALT-kind signal, oscillatory cycles, convergent-signal
cycles, and now 2-structure feedback cycles). The loop-closure
vocabulary gap is characterized, not patched.
