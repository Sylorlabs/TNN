# PREREG: CYCLES-CONVERGENT -- Does Sequences+Halting Handle Convergent-Signal Cycles?

Committed BEFORE any implementation. Frozen kill bars; no weakening after results.
Commit order: this prereg (plus NAMECHECK.md Steps 0-2) strictly precedes all implementation.

## 1. Question

C425 (CYCLES-OSCILLATORY, verdict PASS, 2026-10-03) closed the
oscillatory family: period-2 on-cycle, tail-entry lasso, and period-3
all solve via bounded exact-length trials with end-of-pass
termination, and the (b) fixpoint halt is verified period-1-specific
(it neither misfires on revisits nor is needed for any win). From
C420's boundary list, the remaining untested cycle families are
convergent-signal and multi-structure feedback. This battery closes
the first of those.

A convergent-signal cycle: re-applying one structure advances the
signal monotonically toward a limit, never reaching exact equality in
finite steps. In this integer-valued machinery that is realized as a
strictly advancing walk through fresh states: every step produces a
new value, no state is ever revisited, and the output==input halt
never fires within the bounded window. This differs from fixpoint
(exact equality stops the trial), from oscillatory (periodic
revisits), and from the alternating chain (linear progression ending
in a taught fixpoint): here the answer is an interior point of the
walk or the walk's end, and termination can only be the bounded
exact-length trial itself.

The frozen halting vocabulary is: (a) miss v<0, fail; (b) v==prev,
break (exact equality only); (c) i>=cap, break; (d) end of pass. It
contains no change-below-threshold halt and no diminishing-difference
check. The question: does the frozen mechanism handle convergent
workloads anyway (via bounded exact-length trials with end-of-pass
termination), with (b) correctly silent throughout?

Three tests, all on the fully FROZEN mechanism and base (gc_uni.zag +
gc_base.zag, zero modifications, no extensions):

- QC1 (convergent, interior answer, no-limit chain): a 9-hop chain of
  fresh states; query starts at the chain head, answer is the state at
  depth 3, the chain continuing past it. Tests the basic convergent
  run: the winning trial must stop at an interior point by end-of-pass
  with (b) silent, since no fixpoint exists anywhere in the window.
- QC2 (convergent, deeper interior answer): same chain shape on fresh
  identifiers; answer at depth 5. The k=3 and k=4 trials execute and
  fail by falling short, so the win at k=5 proves exact-length
  matching (no periodicity to exploit: only k=d can win).
- QC3 (convergent to the chain end): a 3-hop chain whose end state has
  no outgoing edge (the limit of the walk). Query starts at the head,
  answer is the end state. Tests that arrival at the limit does NOT
  misfire the (b) halt: v=7204 differs from prev=7203, so the win is
  end-of-pass, and reaching the limit is correctly distinguished from
  being at a fixpoint.

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
All copied with sha256 verification; C7 audits they are unmodified.

Bounds: SEQMAX=8, CAP=8 (frozen values, not learned; the claim under
test is the halting vocabulary over convergence, not the bound values).
Under SEQMAX=CAP=8 the (c) cap halt can never fire strictly before
end-of-pass. Note stepf semantics: STEP with no outgoing edge returns
its input (identity at chain end); (b) still requires v==prev, i.e.
two consecutive equal values, so merely arriving at the chain end
from a different state does not halt.

## 3. Workload designs and frozen predictions

Shared inventory (every exercised identifier is a bare integer):
m0 = class 4 STEP on 701 (the convergent MAP);
m1 = class 1 COUNT on 606; m2 = class 1 COUNT on 605;
m3 = class 1 COUNT on 607 (distractors, block reused verbatim from
cycles_oscillatory: nothing collides with the 70xx-72xx chain states).
Distractor facts: (6101,605,6102); (6201,606,6202),(6201,606,6203);
(6301,607,9301).
Teaches: m1: (6201,2); m2: (6101,1); m3: (6301,1).
Learned masks: m0 in{1} out{1,2} (each chain's end state is never a
fact subject, so the final teach output is kind 2);
m1/m2/m3 in{1} out{2} (the count values 1 and 2 are never fact
subjects, so they stay kind 2).
No IDENT MAP in the inventory: kept comparable to the oscillatory
inventory (COUNT-only distractors); with s!=exp in all three queries
IDENT could not win trivially in any case.

Admission fact used by all three: at every k in 3..8 exactly one
sequence is admitted, [0 x k]. Any occurrence of 1/2/3 breaks an
adjacency (out{j}={2} against every in mask {1}) or the final kout
check (out{j}={2} does not contain kout=1); [0,j] pairs fail the final
kout check; [j,0] and [j,k] fail adjacency. Hence the prefix is
identical in all three worlds: 1 admitted single ([0]), 0 admitted
x!=y pairs, WIDEN=1 retries all 12 rejected pairs (all fail on COUNT
miss; each pair trial prints exactly one INTER= line, the v1 value).

### 3.1 QC1: convergent, interior answer, no-limit chain (PROB=QC1)

setup_qc1:
- Facts: (7001,701,7002), (7002,701,7003), ..., (7009,701,7010).
  9 hops through 10 fresh states; 7010 has no outgoing edge.
- m0 teaches: (7001,7002), ..., (7009,7010) (9 teaches).
- Query: s=7001, kin=1, kout=1, exp=7004, nm=4, seqmax=8, cap=8.
  exp is interior: the walk continues 7005..7010 past the answer.
- Termination: end-of-pass after a bounded run of exactly 3 steps.
  Neither (b) nor (c) fires on the winning trial (all values
  distinct); no fixpoint exists anywhere in the window.

Frozen execution:
- Singles: [0] admitted: 7001->7002 != 7004 (1 try, no INTER print).
  [1],[2],[3] rejected (out{2} does not contain kout=1).
- WIDEN=1: 12 rejected pairs, all fail (COUNT miss; one INTER= line
  each: -2 for the nine pairs starting with a COUNT MAP, 7002 for the
  three [0,j] pairs). 12 tries.
- k=3: exactly 1 admitted sequence, [0,0,0] (n=0, tried first):
  7001->7002->7003->7004, end-of-pass, cur=7004 == exp. SUCCESS.
  3 observe calls on m0. 1 try.
- k=4..8 never run; no WIDEN=2 (a win stops the search).

Predictions:
- Report: `ARM=GC PROB=QC1 ANS=7004 TRIES=14` (1 + 12 + 1).
- Trace: the last 3 INTER= lines before the QC1 report are
  7002,7003,7004 (the winning trial; no early halt fired).
- Total INTER= lines in the QC1 section: 15 (12 pair trials x 1 +
  3 winning-trial steps). Any early halt or miss anywhere in the
  section would reduce this count, so 15 proves (b)/(c)/(a) never
  fired in the whole QC1 run.
- Census: m0 inmask=1 outmask=3 n=12 (9 teaches + 3 trial observes);
  m1/m2/m3 inmask=1 outmask=2 n=1.

### 3.2 QC2: convergent, deeper interior answer (PROB=QC2)

setup_qc2:
- Facts: (7101,701,7102), ..., (7109,701,7110). 9 hops, 10 fresh
  states; 7110 has no outgoing edge.
- m0 teaches: (7101,7102), ..., (7109,7110) (9 teaches).
- Query: s=7101, kin=1, kout=1, exp=7106, nm=4, seqmax=8, cap=8.
  exp is at depth 5, interior.
- Termination: end-of-pass after a bounded run of exactly 5 steps.
  The k=3 and k=4 trials execute and fail by falling short, proving
  exact-length matching: with no periodicity, only k=d wins.

Frozen execution:
- Singles: [0] admitted: 7101->7102 != 7106 (1 try). [1],[2],[3]
  rejected.
- WIDEN=1: 12 rejected pairs, all fail (one INTER= line each). 12 tries.
- k=3: [0,0,0] only: 7101->7102->7103->7104, end-of-pass,
  cur=7104 != 7106. 1 try.
- k=4: [0,0,0,0] only: ->7105, end-of-pass, cur=7105 != 7106. 1 try.
- k=5: [0,0,0,0,0] only: ->7106, end-of-pass, cur=7106 == exp.
  SUCCESS. 1 try.
- k=6..8 never run; no WIDEN=2.

Predictions:
- Report: `ARM=GC PROB=QC2 ANS=7106 TRIES=16` (1 + 12 + 1 + 1 + 1).
- Trace: the last 5 INTER= lines before the QC2 report are
  7102,7103,7104,7105,7106.
- Total INTER= lines in the QC2 section: 24 (12 + 3 + 4 + 5); any
  early halt anywhere would reduce it.
- Census: m0 inmask=1 outmask=3 n=14 (9 teaches + 5 trial observes);
  m1/m2/m3 inmask=1 outmask=2 n=1.

### 3.3 QC3: convergent to the chain end (PROB=QC3)

setup_qc3:
- Facts: (7201,701,7202), (7202,701,7203), (7203,701,7204).
  7204 is the chain end (no outgoing edge): the limit of the walk.
- m0 teaches: (7201,7202), (7202,7203), (7203,7204) (3 teaches).
- Query: s=7201, kin=1, kout=1, exp=7204, nm=4, seqmax=8, cap=8.
  exp is the limit itself, reached at depth 3.
- Termination: end-of-pass after a bounded run of exactly 3 steps.
  Arrival at the limit does not fire (b): v=7204 differs from
  prev=7203. Reaching the limit is thus distinguished from being at
  a fixpoint (which would need v==prev).

Frozen execution:
- Singles: [0] admitted: 7201->7202 != 7204 (1 try). [1],[2],[3]
  rejected.
- WIDEN=1: 12 rejected pairs, all fail. 12 tries.
- k=3: [0,0,0] only: 7201->7202->7203->7204, end-of-pass,
  cur=7204 == exp. SUCCESS. 1 try.
- No WIDEN=2.

Predictions:
- Report: `ARM=GC PROB=QC3 ANS=7204 TRIES=14` (1 + 12 + 1).
- Trace: the last 3 INTER= lines before the QC3 report are
  7202,7203,7204.
- Total INTER= lines in the QC3 section: 15; any early halt would
  reduce it.
- Census: m0 inmask=1 outmask=3 n=6 (3 teaches + 3 trial observes);
  m1/m2/m3 inmask=1 outmask=2 n=1.

## 4. Pre-declared analysis: the threshold-vocabulary gap

The frozen vocabulary contains no change-below-threshold halt and no
diminishing-difference check; (b) is exact equality only. Detecting
"the signal has converged enough" is not expressible. For the value
queries in this battery that gap is observationally equivalent to
bounded exact-length trials, and the equivalence is preregistered here
rather than discovered after the fact: over a deterministic walk
through fresh states, with d steps from s to exp and no revisits, the
trial [0 x k] wins for the smallest k>=3 with k=d (repetitions are
never tried at k=2: the prefix enumerates x!=y only, and WIDEN=1
retries only rejected x!=y pairs), provided k<=8 and the kind masks
admit. QC1: d=3, k=3. QC2: d=5, k=5. QC3: d=3, k=3, with the limit
reached but (b) correctly silent since v!=prev. All within SEQMAX=8.

A task that genuinely required data-dependent threshold stopping
(stop when the change drops below a threshold unknown at query time,
with continuation past the stopping point destroying the answer)
would need a new principle. That is characterized here, not
implemented: the mechanism stays frozen and no convergence-specific
handler is added. If any of C3/C4/C5 fails, the REPORT characterizes
the failure as INFORMATIVE-FAIL per Section 7 rather than patching
the vocabulary.

## 5. Build plan

1. Lane repo init (done). This PREREG.md + NAMECHECK.md commit alone.
2. Copy frozen sources with sha256 verification: gc_uni.zag,
   gc_base.zag, uni_nomain.zag.
3. Write cc_setups.zag (setup_qc1, setup_qc2, setup_qc3),
   cc_main.zag (three queries, reports, censuses).
4. Assemble: cc_full.zag = gc_base.zag + uni_nomain.zag + gc_uni.zag
   + cc_setups.zag + cc_main.zag. One binary cc_fbin (the mechanism
   is fully frozen; no extension, no control, no reduction needed).
   Compile with pinned safebin znc. Run 3x, pairwise cmp.
5. build.sh encodes all audits fail-closed (set -e): toolchain guard,
   frozen digests, 3/3 cmp, report-line greps, trace-tail greps,
   total-INTER counts, census greps, no-WIDEN=2 check, setup-hygiene
   grep (C9), opacity grep (C8).

## 6. Frozen kill bars

- C1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Steps 0-2 + .gitignore ONLY) strictly precedes all
  implementation commits (audited via the lane-local git log).
- C2 DETERMINISM: PASS iff 3/3 runs of cc_fbin are pairwise
  byte-identical (cmp); digests recorded.
- C3 QC1-PASS: PASS iff the binary reports
  `ARM=GC PROB=QC1 ANS=7004 TRIES=14`, no WIDEN=2 appears in the QC1
  section, the last 3 INTER= lines before the QC1 report are
  7002,7003,7004, and the QC1 section contains exactly 15 INTER=
  lines total.
- C4 QC2-PASS: PASS iff the binary reports
  `ARM=GC PROB=QC2 ANS=7106 TRIES=16`, no WIDEN=2 in the QC2 section,
  the last 5 INTER= lines before the QC2 report are
  7102,7103,7104,7105,7106, and the QC2 section contains exactly 24
  INTER= lines total.
- C5 QC3-PASS: PASS iff the binary reports
  `ARM=GC PROB=QC3 ANS=7204 TRIES=14`, no WIDEN=2 in the QC3 section,
  the last 3 INTER= lines before the QC3 report are
  7202,7203,7204, and the QC3 section contains exactly 15 INTER=
  lines total.
- C6 CENSUS: PASS iff every CENSUS line matches the Section 3
  predictions exactly (m0 inmask=1 outmask=3 n=12/14/6; m1/m2/m3
  inmask=1 outmask=2 n=1).
- C7 FROZEN-INTACT: PASS iff the lane copies of gc_uni.zag,
  gc_base.zag, uni_nomain.zag match the Section 2 digests.
- C8 OPACITY: PASS iff grep over all built sources for banned
  domain-story tokens
  `hypothesis|refine|evaluat|domain|plan|causal|navigat|arithmet|grammar|language|audio|interven|belie|goal|agent`
  (case-insensitive) returns empty, AND every exercised identifier is
  a bare integer.
- C9 SETUP-HYGIENE: PASS iff cc_setups.zag contains no iteration
  (`while`), no repeat/period check, and no direct `exec_map` call:
  setups pose facts + MAPs + teaches only, the same discipline as
  C425's qo_setups.zag.

## 7. Verdict mapping

- C1/C7/C8/C9 FAIL -> VOID.
- C2 FAIL -> UNDECIDED (name the decisive rerun).
- C3 FAIL -> INFORMATIVE-FAIL (convergent interior): the frozen
  mechanism does not handle the basic convergent run; REPORT
  characterizes the missed or misfired trial (in particular whether
  the (b) halt fired spuriously on distinct values).
- C4 FAIL (with C3 PASS) -> INFORMATIVE-FAIL (depth): depth-3
  convergence works but depth-5 does not; REPORT says which step
  diverged.
- C5 FAIL (with C3/C4 PASS) -> INFORMATIVE-FAIL (limit): interior
  convergence works but arrival at the chain end does not; REPORT
  characterizes whether (b) misfired on limit arrival.
- C6 FAIL -> INFORMATIVE-FAIL (contracts): kind-mask learning moved
  under convergence; investigate before any claim.
- All PASS -> PASS: the frozen sequences+halting mechanism handles
  convergent-signal cycles (interior answers at depth 3 and 5,
  arrival at the walk limit) with zero mechanism change; termination
  is by bounded exact-length trial (end-of-pass) with the (b) halt
  correctly silent throughout; the threshold-vocabulary gap of
  Section 4 is observationally equivalent for these value queries.

## 8. Honest boundaries (pre-declared)

- Bounded runs only: the battery covers fixed-depth value queries;
  data-dependent stop-at-threshold is not in the halting vocabulary
  (see Section 4 for the exact equivalence claim).
- exp is still supplied for end-to-end verification; the tests target
  the proposal space and the halting vocabulary over convergence.
- SEQMAX=8/CAP=8 remain frozen researcher bounds, not learned values.
  An answer needing k>8 would fail on bounds; not tested here. Under
  SEQMAX=CAP=8 the (c) cap halt can never fire strictly before
  end-of-pass.
- No IDENT MAP in the inventory (documented in Section 3); the
  distractor inventory is COUNT-only by design, matching C425.
- Overshoot trials (k>d) are never executed: the increasing-k search
  stops at the first win, so exact-length matching is established
  from below only (QC2's k=3/k=4 failures); the longer-than-needed
  direction is structural, not empirically exercised.
- The (b) halt is exact-equality-specific by construction; this
  battery verifies it stays silent across convergent runs including
  arrival at the walk limit (QC3), and is never needed for the wins
  (all three wins are end-of-pass).
- Multi-structure feedback cycles remain untested after this battery.

## 9. Predicted outcome

PASS expected on C3/C4/C5 with the exact TRIES values, INTER tails,
total INTER counts, and census lines of Section 3. The predicted
scientific result: the frozen sequences+halting mechanism handles
convergent-signal cycles with no mechanism change, extending the
composition envelope (pipelines, fixpoint sequences, alternating
chains, data-dependent halting, HALT-kind signal, oscillatory cycles,
and now convergent-signal cycles). The threshold vocabulary gap is
characterized, not patched.
