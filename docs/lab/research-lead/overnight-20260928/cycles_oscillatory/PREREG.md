# PREREG: CYCLES-OSCILLATORY -- Does Sequences+Halting Handle Oscillatory Cycles?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all implementation.

## 1. Question

C420 (CYCLES-GENERALIZE, verdict PASS, 2026-10-03) proved sequences+halting
general over fixpoint families: an alternating two-structure fixpoint
chain, data-dependent halting as the operative stop of a winning trial,
and the HALT-kind contract signal as a strictly additive extension. Its
honest boundary: "oscillatory, convergent-signal, and multi-structure
feedback cycles remain untested."

This battery tests the first of those: oscillatory cycles, where the
state revisits (A to B to A to B...) rather than converging to a
fixpoint. The frozen halting vocabulary is: (a) miss v<0, fail;
(b) v==prev, break (the fixpoint signal); (c) i>=cap, break;
(d) end of pass. Note (b) is period-1 only: on a period-2-or-longer
oscillation it never fires, which is the correct non-misfire behavior
under test here.

The question: does the frozen mechanism handle oscillatory workloads
anyway (via bounded exact-length trials with end-of-pass termination),
or does oscillation need a new principle (for example a repeat-history
halt that stops at the first observed repeat)?

Three tests, all on the fully FROZEN mechanism and base (gc_uni.zag +
gc_base.zag, zero modifications, no extensions):

- O-Q1 (period-2, on-cycle start): a single-structure oscillator A<->B;
  query starts on the cycle, answer is the start state. Bounded run of
  2 periods. Tests that (b) does not misfire on state revisits and that
  repetitions execute correctly through the sequence machinery.
- O-Q2 (lasso: 2-step tail + period-2): an entry phase leads into the
  oscillation; query starts at the tail, answer is the first repeated
  state. Tests entry-phase robustness: the mechanism must run through
  the tail and stop exactly at the detection point parity.
- O-Q3 (period-3): an odd-period single-structure oscillator; query
  starts on the cycle, answer is the start state. Tests a non-parity
  period, where the prefix pair machinery cannot help (repetitions are
  never tried at k=2).

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
All copied with sha256 verification; O7 audits they are unmodified.

Bounds: SEQMAX=8, CAP=8 (frozen values, not learned; the claim under
test is the halting vocabulary over oscillation, not the bound values).

## 3. Workload designs and frozen predictions

Shared inventory (every exercised identifier is a bare integer):
m0 = class 4 STEP on 601 (the oscillator MAP);
m1 = class 1 COUNT on 606; m2 = class 1 COUNT on 605;
m3 = class 1 COUNT on 607 (distractors).
Distractor facts: (6101,605,6102); (6201,606,6202),(6201,606,6203);
(6301,607,9301).
Teaches: m1: (6201,2); m2: (6101,1); m3: (6301,1).
Learned masks: m0 in{1} out{1} (oscillator states are fact subjects);
m1/m2/m3 in{1} out{2} (the count values 1 and 2 are never fact
subjects, so they stay kind 2).
No IDENT MAP in the inventory: with s=exp on the cycle (QO1, QO3),
IDENT would win as a trivial single without ever running the
oscillator. Its exclusion is documented here, not hidden.

### 3.1 QO1: period-2, on-cycle start (PROB=QO1)

setup_qo1:
- Facts: (6001,601,6002), (6002,601,6001). A 2-state oscillator.
- m0 teaches: (6001,6002), (6002,6001).
- Query: s=6001, kin=1, kout=1, exp=6001, nm=4, seqmax=8, cap=8.
- Termination: end-of-pass after a bounded run of exactly 2 periods
  (4 steps). Neither (b) nor (c) fires on the winning trial.

Frozen execution:
- Singles: [0] admitted: 6001->6002, != exp (1 try). [1],[2],[3]
  rejected (out{2} does not contain kout=1).
- Ordered pairs x!=y: 0 admitted ([0,j] fail the final kout check;
  [j,0] and [j,k] fail the adjacency check). WIDEN=1 retries all 12
  rejected x!=y pairs; all fail (COUNT on 606/605/607 at 6001 or 6002
  finds no edges, returns -2, miss; each prints one INTER= line).
- k=3: exactly 1 admitted sequence, [0,0,0] (n=0): the chain rule
  forces every position to 0 (only m0 has out{1}). Trial:
  6001->6002->6001->6002, end-of-pass, cur=6002 != exp. The (b) halt
  does not fire (no adjacent equal values). 1 try.
- k=4: exactly 1 admitted sequence, [0,0,0,0] (n=0):
  6001->6002->6001->6002->6001, end-of-pass, cur=6001 == exp.
  SUCCESS. 4 observe calls on m0. 1 try.
- No WIDEN=2 (a win stops the search).

Predictions:
- Report: `ARM=GC PROB=QO1 ANS=6001 TRIES=15` (1 single + 12 WIDEN=1
  pairs + 1 k=3 + 1 k=4).
- Trace: the last 4 INTER= lines before the QO1 report are
  6002,6001,6002,6001 (the winning trial; no early halt fired).
- Census: m0 inmask=1 outmask=1 n=6 (2 teaches + 4 trial observes);
  m1/m2/m3 inmask=1 outmask=2 n=1.

### 3.2 QO2: lasso, 2-step tail + period-2 (PROB=QO2)

setup_qo2:
- Facts: (6001,601,6002), (6002,601,6003), (6003,601,6004),
  (6004,601,6003). Tail 6001->6002->6003, then 6003<->6004.
- m0 teaches: (6001,6002), (6002,6003), (6003,6004), (6004,6003).
- Query: s=6001, kin=1, kout=1, exp=6003, nm=4, seqmax=8, cap=8.
  exp=6003 is the first repeated state (first seen at step 2,
  repeated at step 4).
- Termination: end-of-pass after a bounded run that enters the
  oscillation and stops exactly at the detection-point parity
  (4 steps). Neither (b) nor (c) fires on the winning trial.

Frozen execution:
- Singles: [0] admitted: 6001->6002 != 6003 (1 try). [1],[2],[3]
  rejected.
- WIDEN=1: 12 rejected pairs, all fail (COUNT miss at 6001 or 6002).
- k=3: [0,0,0] only: 6001->6002->6003->6004, cur=6004 != 6003.
  1 try.
- k=4: [0,0,0,0] only: 6001->6002->6003->6004->6003, cur=6003 == exp.
  SUCCESS. 1 try.
- No WIDEN=2.

Predictions:
- Report: `ARM=GC PROB=QO2 ANS=6003 TRIES=15`.
- Trace: the last 4 INTER= lines before the QO2 report are
  6002,6003,6004,6003.
- Census: m0 inmask=1 outmask=1 n=8 (4 teaches + 4 trial observes);
  m1/m2/m3 inmask=1 outmask=2 n=1.

### 3.3 QO3: period-3 oscillator (PROB=QO3)

setup_qo3:
- Facts: (6001,601,6002), (6002,601,6003), (6003,601,6001).
- m0 teaches: (6001,6002), (6002,6003), (6003,6001).
- Query: s=6001, kin=1, kout=1, exp=6001, nm=4, seqmax=8, cap=8.
- Termination: end-of-pass after a bounded run of exactly 1 period
  (3 steps). Neither (b) nor (c) fires.

Frozen execution:
- Singles: [0]: 6001->6002 != 6001 (1 try). [1],[2],[3] rejected.
- WIDEN=1: 12 rejected pairs, all fail (COUNT miss).
- k=3: [0,0,0] (n=0): 6001->6002->6003->6001, end-of-pass,
  cur=6001 == exp. SUCCESS on the first sequence-phase trial. 1 try.
- k=4 never runs. No WIDEN=2.

Predictions:
- Report: `ARM=GC PROB=QO3 ANS=6001 TRIES=14` (1 + 12 + 1).
- Trace: the last 3 INTER= lines before the QO3 report are
  6002,6003,6001.
- Census: m0 inmask=1 outmask=1 n=6 (3 teaches + 3 trial observes);
  m1/m2/m3 inmask=1 outmask=2 n=1.

## 4. Pre-declared analysis: the detection-vocabulary gap

The frozen vocabulary contains no period-greater-than-1 repeat check;
detecting "a state I have seen before" is not expressible. For the
value queries in this battery that gap is observationally equivalent
to bounded exact-length trials, and the equivalence is preregistered
here rather than discovered after the fact: over a fixed period-p
oscillator, with d steps from s to exp along the deterministic walk,
the trial [0 x k] wins for the smallest k>=3 with k congruent to d
mod p (repetitions are never tried at k=2: the prefix enumerates x!=y
only, and WIDEN=1 retries only rejected x!=y pairs), provided k<=8 and
the kind masks admit. QO1: p=2, d=0 mod 2, k=4. QO2: p=2, d=2, k=4.
QO3: p=3, d=0 mod 3, k=3. All within SEQMAX=8.

A task that genuinely required data-dependent stopping (period unknown
at query time, with continuation past the detection point destroying
the answer) would need a new principle, a repeat-history halt. That
is characterized here, not implemented: the mechanism stays frozen
and no oscillation-specific handler is added. If any of O3/O4/O5
fails, the REPORT characterizes the failure as INFORMATIVE-FAIL per
Section 7 rather than patching the vocabulary.

## 5. Build plan

1. Lane repo init (done). This PREREG.md + NAMECHECK.md commit alone.
2. Copy frozen sources with sha256 verification: gc_uni.zag,
   gc_base.zag, uni_nomain.zag.
3. Write qo_setups.zag (setup_qo1, setup_qo2, setup_qo3),
   qo_main.zag (three queries, reports, censuses).
4. Assemble: qo_full.zag = gc_base.zag + uni_nomain.zag + gc_uni.zag
   + qo_setups.zag + qo_main.zag. One binary qo_fbin (the mechanism
   is fully frozen; no extension, no control, no reduction needed).
   Compile with pinned safebin znc. Run 3x, pairwise cmp.
5. build.sh encodes all audits fail-closed (set -e): toolchain guard,
   frozen digests, 3/3 cmp, report-line greps, trace-tail greps,
   census greps, no-WIDEN=2 check, setup-hygiene grep (O9), opacity
   grep (O8).

## 6. Frozen kill bars

- O1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Steps 0-2 ONLY) strictly precedes all implementation
  commits (audited via the lane-local git log).
- O2 DETERMINISM: PASS iff 3/3 runs of qo_fbin are pairwise
  byte-identical (cmp); digests recorded.
- O3 QO1-PASS: PASS iff the binary reports
  `ARM=GC PROB=QO1 ANS=6001 TRIES=15`, no WIDEN=2 appears in the QO1
  section, and the last 4 INTER= lines before the QO1 report are
  6002,6001,6002,6001.
- O4 QO2-PASS: PASS iff the binary reports
  `ARM=GC PROB=QO2 ANS=6003 TRIES=15`, no WIDEN=2 in the QO2 section,
  and the last 4 INTER= lines before the QO2 report are
  6002,6003,6004,6003.
- O5 QO3-PASS: PASS iff the binary reports
  `ARM=GC PROB=QO3 ANS=6001 TRIES=14`, no WIDEN=2 in the QO3 section,
  and the last 3 INTER= lines before the QO3 report are
  6002,6003,6001.
- O6 CENSUS: PASS iff every CENSUS line matches the Section 3
  predictions exactly (m0 inmask=1 outmask=1 n=6/8/6; m1/m2/m3
  inmask=1 outmask=2 n=1).
- O7 FROZEN-INTACT: PASS iff the lane copies of gc_uni.zag,
  gc_base.zag, uni_nomain.zag match the Section 2 digests.
- O8 OPACITY: PASS iff grep over all built sources for banned
  domain-story tokens
  `hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent`
  (case-insensitive) returns empty, AND every exercised identifier is
  a bare integer.
- O9 SETUP-HYGIENE: PASS iff qo_setups.zag contains no iteration
  (`while`), no repeat/period check, and no direct `exec_map` call:
  setups pose facts + MAPs + teaches only, the same discipline as
  C420's cg_setups.zag.

## 7. Verdict mapping

- O1/O7/O8/O9 FAIL -> VOID.
- O2 FAIL -> UNDECIDED (name the decisive rerun).
- O3 FAIL -> INFORMATIVE-FAIL (period-2): the frozen mechanism does
  not handle the basic oscillatory run; REPORT characterizes the
  missed or misfired trial (in particular whether the (b) halt fired
  spuriously on a revisit).
- O4 FAIL (with O3 PASS) -> INFORMATIVE-FAIL (entry phase): the
  mechanism handles on-cycle oscillation but not tail entry; REPORT
  says which step diverged.
- O5 FAIL (with O3/O4 PASS) -> INFORMATIVE-FAIL (odd period):
  period-2 works but period-3 does not; REPORT characterizes why.
- O6 FAIL -> INFORMATIVE-FAIL (contracts): kind-mask learning moved
  under oscillation; investigate before any claim.
- All PASS -> PASS: the frozen sequences+halting mechanism handles
  oscillatory cycles (period-2 on-cycle, tail-entry lasso, period-3)
  with zero mechanism change; termination is by bounded exact-length
  trial (end-of-pass); the detection-vocabulary gap of Section 4 is
  observationally equivalent for these value queries.

## 8. Honest boundaries (pre-declared)

- Bounded runs only: the battery covers fixed-period value queries;
  data-dependent stop-at-first-repeat is not in the halting
  vocabulary (see Section 4 for the exact equivalence claim).
- exp is still supplied for end-to-end verification; the tests target
  the proposal space and the halting vocabulary over oscillation.
- SEQMAX=8/CAP=8 remain frozen researcher bounds, not learned values.
  A period-9+ oscillator, or an answer needing k>8, would fail on
  bounds; not tested here. Under SEQMAX=CAP=8 the (c) cap halt can
  never fire strictly before end-of-pass.
- No IDENT MAP in the inventory (documented in Section 3); the
  distractor inventory is COUNT-only by design.
- Convergent-signal cycles and multi-structure feedback cycles remain
  untested after this battery.
- The (b) halt is period-1-specific by construction; this battery
  verifies it neither misfires on period-2/3 revisits nor is needed
  for the wins (all three wins are end-of-pass).

## 9. Predicted outcome

PASS expected on O3/O4/O5 with the exact TRIES values, INTER tails,
and census lines of Section 3. The predicted scientific result: the
frozen sequences+halting mechanism handles oscillatory cycles with no
mechanism change, extending the composition envelope (pipelines,
fixpoint sequences, alternating chains, data-dependent halting,
HALT-kind signal, and now oscillatory cycles). The detection
vocabulary gap is characterized, not patched.
