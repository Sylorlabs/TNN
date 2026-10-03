# PREREG2: CYCLES-FEEDBACK-REFIX -- Fresh Re-freeze of the C430 Feedback Battery

Committed BEFORE any re-run. Fresh preregistration, NOT an amendment
to C430's PREREG.md (which stands unaltered with its INFORMATIVE-FAIL
verdict). Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly
precedes all re-run artifacts.

## 1. Provenance and the correction

C430 (CYCLES-FEEDBACK, lane
`docs/lab/research-lead/overnight-20260928/cycles_feedback/`, verdict
INFORMATIVE-FAIL, 2026-10-03) tested the frozen GEN-CYCLES/C420
sequences+halting mechanism on multi-structure feedback cycles: QF1
full-loop return through an emergent 2-structure loop, QF2 tail-entry
lasso, QF3 mid-loop stop by exact-length matching. The wave failed F3
on a prereg bookkeeping error only.

C430's REPORT autopsy (carried here verbatim in substance):
- The prereg predicted `ARM=GC PROB=QF1 ANS=8001 TRIES=44`, derived
  from a claimed winner "[0,1,0,1] at lexicographic n=21" and hence
  "22 tried sequences at k=4".
- The frozen enumerator (`gc_run_len`) walks all nm^k sequences and
  skips rejected ones. At k=4 (nm=4) the tried sequences are
  n = 0, 1, 4, 5, 16, 17: every other n in 0..255 contains a 2/3 digit
  and is rejected by the chain kind rule. The winner [0,1,0,1] sits
  at n=17 and is the 6th tried sequence, so k=4 contributes 6 tries,
  not 22. The prereg's "n=21" was computed with mismatched positional
  weights ([0,1,0,1] = 0*64 + 1*16 + 0*4 + 1 = 17, not 21).
- Correct TRIES = 2 + 2 + 10 + 8 + 6 = 28.
- Every scientific prediction about QF1 held exactly in the C430
  trace: winner [0,1,0,1] at k=4, end-of-pass termination, the (b)
  halt silent on the winner, the last-4 INTER tail exactly
  8101,8002,8102,8001, no WIDEN=2, and the census lines matching.
  F4 (QF2, TRIES=76) and F5 (QF3, TRIES=17) passed exactly as
  preregistered.

This PREREG2 re-freezes the battery with the corrected QF1
predictions (TRIES=28; winner at n=17; 6th tried at k=4) and restates
every other prediction from C430's PREREG unchanged. Nothing about
the mechanism, base, setups, or binary changes: the executed artifact
is the exact qf_fbin binary built in C430 (sha256 recorded in
NAMECHECK.md Step 1), copied with digest verification and NOT
rebuilt.

Why a fresh prereg and not an amendment: governance forbids amending
a frozen prereg after results are known (retroactive bar changes are
void-on-sight). The C430 verdict stands as INFORMATIVE-FAIL. This
wave closes the bookkeeping by re-freezing corrected bars in a new
lane and re-running the unchanged binary under them.

## 2. Question (unchanged from C430)

Does the frozen sequences+halting mechanism run genuine
multi-structure feedback cycles with correct termination? Three
tests on the FROZEN mechanism and base (gc_uni.zag + gc_base.zag,
zero modifications, no extensions):

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

The frozen halting vocabulary is unchanged: (a) miss v<0, fail;
(b) v==prev, break (exact equality only); (c) i>=cap, break;
(d) end of pass. Bounds: SEQMAX=8, CAP=8 (frozen values, not
learned). Under SEQMAX=CAP=8 the (c) cap halt can never fire
strictly before end-of-pass. stepf semantics: STEP with no outgoing
edge returns its input (identity at a dead end); (b) still requires
v==prev, i.e. two consecutive equal values.

## 3. Frozen artifact (not rebuilt)

The executed artifact is the qf_fbin binary from the C430 lane,
sha256
c7c459e556f94f53b42be53d57f26d5fb6e024004a6511c6179599b1a48dddf3,
copied with digest verification before any execution. It was
assembled in C430 from gc_base.zag + uni_nomain.zag + gc_uni.zag +
qf_setups.zag + qf_main.zag with the frozen digests recorded in
NAMECHECK.md Step 1. This wave does not recompile, reassemble, or
alter the binary or any source. The only changed artifact in this
lane is the preregistration itself.

## 4. Workload designs and frozen predictions (QF1 corrected)

Shared inventory (every exercised identifier is a bare integer):
m0 = class 4 STEP on 801 (structure A: X region to Y region);
m1 = class 4 STEP on 802 (structure B: Y region back to X region);
m2 = class 1 COUNT on 605; m3 = class 1 COUNT on 606
(distractors, block reused from cycles_oscillatory/cycles_convergent).
Distractor facts: (6101,605,6102); (6201,606,6202),(6201,606,6203).
Teaches: m2: (6101,1); m3: (6201,2).
Learned masks: m2/m3 in{1} out{2} (the count values 1 and 2 are never
fact subjects, so they stay kind 2).

Feedback edge sets (carried from C430, unchanged):
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

### 4.1 QF1: feedback loop, full-loop return (PROB=QF1) -- CORRECTED

setup_qf1 (carried from C430, unchanged):
- Facts: (8001,801,8101), (8002,801,8102),
  (8101,802,8002), (8102,802,8001), (8001,802,8999).
- m0 teaches: (8001,8101), (8002,8102).
- m1 teaches: (8101,8002), (8102,8001), (8001,8999).
- Query: s=8001, kin=1, kout=1, exp=8001, nm=4, seqmax=8, cap=8.
- The answer is one full loop pass away: 8001->8101->8002->8102
  ->8001. Termination: end-of-pass after a bounded run of exactly
  4 steps; (b) silent on the winner (all adjacent values distinct).

Frozen execution (corrected enumeration):
- Singles: [0] admitted: 8001->8101 != 8001 (1 try, no INTER print).
  [1] admitted: 8001->8999 != 8001 (1 try). [2],[3] rejected.
  2 tries.
- Pairs: [0,1] admitted: 8001->8101->8002 != 8001 (1 try, one
  INTER= line). [1,0] admitted: 8001->8999->8999 != 8001 (1 try).
  WIDEN=1: 10 rejected pairs, all fail (one INTER= line each).
  12 tries in the pair phase; 14 tries total in the prefix.
- k=3: 8 tried (n=0,1,4,5,16,17,20,21 of 64, the {0,1}^3
  sequences), all fail: [0,0,0] and [0,0,1] (b)-halt at step 2
  (A at 8101 has no 801 edge) with cur=8101; [0,1,0] ends 8102;
  [0,1,1] (b)-halts at step 3 (B at 8002 has no 802 edge) with
  cur=8002; the four [1,*,*] (b)-halt at step 2 with cur=8999.
  8 tries. No 3-step return to 8001 exists (only B at 8102 leads
  into 8001, unreachable in 2 steps from 8001).
- k=4: 6 tried (n=0,1,4,5,16,17 of 256; every other n contains a
  2/3 digit and is rejected by the chain rule): n=0 [0,0,0,0],
  n=1 [0,0,0,1], n=4 [0,0,1,0], n=5 [0,0,1,1] all (b)-halt at
  step 2 with cur=8101; n=16 [0,1,0,0] (b)-halts at step 4 with
  cur=8102; n=17 [0,1,0,1] admitted:
  8001->8101->8002->8102->8001, end-of-pass,
  cur=8001 == exp. SUCCESS. The winner is the 6th tried sequence
  at k=4. 6 tries. The [0,1,0,1] alternation is the unique 4-step
  return (any (b)-halted trial ends stuck at 8101/8102/8002/8999,
  none of which is 8001).
- k=5..8 never run; no WIDEN=2 (a win stops the search).

Predictions (corrected):
- Report: `ARM=GC PROB=QF1 ANS=8001 TRIES=28` (2 + 2 + 10 + 8 + 6).
- Trace: the last 4 INTER= lines before the QF1 report are
  8101,8002,8102,8001 (the winning trial; no early halt fired).
- Census: m0 inmask=1 outmask=1 n=4 (2 teaches + 2 trial observes);
  m1 inmask=1 outmask=3 n=5 (3 teaches + 2 trial observes);
  m2/m3 inmask=1 outmask=2 n=1.

### 4.2 QF2: feedback lasso, tail entry (PROB=QF2) -- UNCHANGED

setup_qf2 (carried from C430, unchanged):
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
  all fail. 12 tries in the pair phase; 14 in the prefix.
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

Predictions (unchanged from C430):
- Report: `ARM=GC PROB=QF2 ANS=8001 TRIES=76`
  (2 + 2 + 10 + 8 + 16 + 32 + 6).
- Trace: the last 6 INTER= lines before the QF2 report are
  8000,8001,8101,8002,8102,8001.
- Census: m0 inmask=1 outmask=1 n=8 (4 teaches + 4 trial observes);
  m1 inmask=1 outmask=3 n=5 (3 teaches + 2 trial observes);
  m2/m3 inmask=1 outmask=2 n=1.

### 4.3 QF3: feedback loop, mid-loop stop (PROB=QF3) -- UNCHANGED

setup_qf3: same facts, MAPs, and teaches as setup_qf1 (C430).
- Query: s=8001, kin=1, kout=1, exp=8102, nm=4, seqmax=8, cap=8.
  exp is an interior loop state, 3 loop-steps away:
  8001->8101->8002->8102.
- Termination: end-of-pass after a bounded run of exactly 3 steps;
  (b) silent on the winner.

Frozen execution:
- Singles: [0]: 8001->8101 != 8102 (1 try). [1]: 8001->8999
  != 8102 (1 try). [2],[3] rejected.
- Pairs: [0,1]: 8001->8101->8002 != 8102 (1 try). [1,0]:
  8001->8999->8999 != 8102 (1 try). WIDEN=1: 10 rejected pairs,
  all fail. 12 tries in the pair phase; 14 in the prefix.
- k=3: 8 admitted. n=0 [0,0,0]: (b)-halt at step 2, cur=8101.
  n=1 [0,0,1]: (b)-halt at step 2, cur=8101. n=4 [0,1,0]
  admitted: 8001->8101->8002->8102, end-of-pass,
  cur=8102 == exp. SUCCESS. 3 tries. The [0,1,0] win is the
  unique 3-step arrival at 8102 (only A at 8002 leads into 8102,
  reached in 2 steps only by [0,1]).
- k=4..8 never run; no WIDEN=2.

Predictions (unchanged from C430):
- Report: `ARM=GC PROB=QF3 ANS=8102 TRIES=17` (2 + 2 + 10 + 3).
- Trace: the last 3 INTER= lines before the QF3 report are
  8101,8002,8102.
- Census: m0 inmask=1 outmask=1 n=4 (2 teaches + 2 trial observes);
  m1 inmask=1 outmask=3 n=4 (3 teaches + 1 trial observe);
  m2/m3 inmask=1 outmask=2 n=1.

## 5. Re-run plan

1. Lane repo init (done). This PREREG2.md + NAMECHECK.md (+
   .gitignore) commit alone.
2. Copy the frozen qf_fbin from the C430 lane; verify its sha256
   against NAMECHECK.md Step 1 before any execution (F7).
3. Run the binary 3x (qf_rerun1.txt, qf_rerun2.txt, qf_rerun3.txt),
   pairwise cmp (F2); record digests; check the re-run digest equals
   the C430 run digest (binary unchanged, deterministic).
4. rerun.sh encodes all audits fail-closed (set -e): toolchain
   guard, binary digest, 3/3 cmp, report-line greps, trace-tail
   greps, no-WIDEN=2 check, census greps.
5. REPORT.md with the verdict; commit as the re-run commit.

## 6. Frozen kill bars

- F1 COMMIT-ORDER: PASS iff this prereg commit (PREREG2.md +
  NAMECHECK.md Steps 0-2 + .gitignore ONLY) strictly precedes all
  re-run artifacts (qf_fbin copy, rerun.sh, run outputs, REPORT.md)
  in the lane-local git log.
- F2 DETERMINISM: PASS iff 3/3 re-runs of the frozen qf_fbin are
  pairwise byte-identical (cmp); digests recorded. Consistency
  check: the re-run digest equals the C430 run digest
  538fd190e096063abf1ae6856eacc6465219a7fbc69cd1b2fe1bce2624f51b37.
- F3 QF1-PASS: PASS iff the binary reports
  `ARM=GC PROB=QF1 ANS=8001 TRIES=28`, no WIDEN=2 appears in the QF1
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
- F6 CENSUS: PASS iff every CENSUS line matches the Section 4
  predictions exactly (QF1: m0 inmask=1 outmask=1 n=4, m1 inmask=1
  outmask=3 n=5; QF2: m0 inmask=1 outmask=1 n=8, m1 inmask=1
  outmask=3 n=5; QF3: m0 inmask=1 outmask=1 n=4, m1 inmask=1
  outmask=3 n=4; m2/m3 inmask=1 outmask=2 n=1 in all three worlds).
- F7 BINARY-INTACT: PASS iff the lane copy of qf_fbin matches the
  NAMECHECK.md Step 1 digest (nothing is rebuilt in this wave; the
  binary digest replaces the source-digest audit).
- F8/F9/F10 (opacity, setup hygiene, feedback-genuine): carried
  from C430 by reference (all PASS there on the byte-identical
  sources this binary was built from; no source changes and no
  rebuild occur in this wave, so they are not re-audited).

## 7. Verdict mapping

- F1/F7 FAIL -> VOID.
- F2 FAIL -> UNDECIDED (name the decisive rerun).
- F3/F4/F5/F6 FAIL -> INFORMATIVE-FAIL (report characterizes the
  divergence exactly as in C430 Section 7; no bar is altered here).
- All PASS -> PASS: the C430 feedback results are confirmed under
  the corrected prereg; the frozen sequences+halting mechanism
  handles multi-structure feedback cycles (full-loop return,
  tail-entry lasso, mid-loop stop) with zero mechanism change; the
  cycle is emergent from A+B composition (neither structure cycles
  alone, established in C430 F10); termination is by bounded
  exact-length trial (end-of-pass) with the (b) halt correctly
  silent on winners and honestly stopping dead-end losers. This
  closes the bookkeeping on the feedback family.

## 8. Honest boundaries (pre-declared, carried from C430)

- Bounded runs only: fixed-length value queries; data-dependent
  stop-at-loop-closure is not in the halting vocabulary (see C430
  PREREG Section 4 for the exact equivalence claim).
- exp is still supplied for end-to-end verification; the tests target
  the proposal space and the halting vocabulary over feedback.
- SEQMAX=8/CAP=8 remain frozen researcher bounds, not learned values.
  Under SEQMAX=CAP=8 the (c) cap halt can never fire strictly before
  end-of-pass.
- No IDENT MAP in the inventory; the distractor inventory is
  COUNT-only by design (carried from C430 Section 3).
- Overshoot trials (k>d) are never executed: the increasing-k search
  stops at the first win.
- The (b) halt is exact-equality-specific by construction; this wave
  re-verifies it stays silent on all three winning feedback trials
  while honestly stopping the dead-end losing trials.
- This wave changes no scientific conclusion of C430: it corrects
  one prereg constant (QF1 TRIES 44 -> 28, with the corrected
  enumeration n=0,1,4,5,16,17 and the winner [0,1,0,1] at n=17, 6th
  tried) and confirms the mechanism's behavior under it.

## 9. Predicted outcome

PASS expected on all bars. The predicted result: the unchanged
frozen binary reports TRIES=28/76/17 with the exact INTER tails and
census lines of Section 4 across 3/3 byte-identical runs, closing
the feedback family bookkeeping with a clean PASS under the
corrected prereg.
