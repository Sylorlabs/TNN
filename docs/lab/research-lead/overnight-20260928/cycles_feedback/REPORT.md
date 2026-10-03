# REPORT: CYCLES-FEEDBACK -- Verdict INFORMATIVE-FAIL (prereg arithmetic error; mechanism vindicated by trace)

Date: 2026-10-03. Worker: cycles-feedback.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_feedback/`.
Battery: preregistered multi-structure feedback-cycle tests for
GEN-CYCLES/C420's frozen sequences+halting mechanism, the last untested
family from C420's boundary list. Pure Zag, pinned safebin znc.
Prereg committed alone (`43c0baa`); implementation follows in this
commit (see lane-local git log). No amendments to the implementation.

## Verdict: INFORMATIVE-FAIL (prereg arithmetic error)

F3 as frozen fails: the binary reports
`ARM=GC PROB=QF1 ANS=8001 TRIES=28`, not the preregistered TRIES=44.
Per Section 7 this is INFORMATIVE-FAIL. The autopsy (below) shows the
failure is a bookkeeping error in the prereg, not a mechanism failure:

- The prereg predicted the QF1 winner [0,1,0,1] at "lexicographic n=21"
  and hence 22 tried sequences at k=4 (TRIES=44). Both numbers are
  wrong. The frozen enumerator (`gc_run_len`) walks all nm^k = 256
  sequences and skips rejected ones; [0,1,0,1] sits at n=17, and the
  tried sequences at k=4 are n = 0, 1, 4, 5, 16, 17 (the {0,1}^4
  sequences; all others contain 2/3 and are rejected by the chain
  rule). So k=4 contributes 6 tries, not 22, and the correct TRIES is
  2 + 2 + 10 + 8 + 6 = 28. The prereg's "n=21" is not even the
  contiguous-enumeration index (that would be 17); it was computed
  with mismatched positional weights.
- Every scientific prediction about QF1 holds exactly: the winner is
  [0,1,0,1] at k=4, termination is end-of-pass, the (b) halt is silent
  on the winner, the last-4 INTER tail is 8101,8002,8102,8001, no
  WIDEN=2 fires, and the census lines match. The trace proves the
  frozen mechanism ran the genuine 2-structure feedback loop exactly
  as designed.

F4 (QF2) and F5 (QF3) PASS exactly as preregistered, including their
TRIES values (76 and 17). The mechanism is vindicated on all three
feedback workloads; the wave verdict is INFORMATIVE-FAIL only because
the frozen F3 bar's TRIES constant was miscalculated in the prereg.
No bar is altered here: F3 stands as FAIL, and a corrected prereg
(TRIES=28, winner at n=17, 6th tried) is left as a transparent
follow-up re-freeze, not claimed in this wave.

## Results

Build: one binary from pinned safebin znc (zagd-unavailable warning is
environmental and non-blocking, as in GEN-CYCLES/C420/C425/C428):
- qf_fbin (frozen base + frozen U + frozen mechanism; QF1, QF2, QF3)

Runs: 3/3 byte-identical (cmp); digest:
- qf_run1.txt:
  538fd190e096063abf1ae6856eacc6465219a7fbc69cd1b2fe1bce2624f51b37

Traces:
- QF1: prefix 14 tries (2 admitted singles [0]: 8001->8101, [1]:
  8001->8999; 2 admitted pairs [0,1]: INTER=8101, [1,0]: INTER=8999;
  WIDEN=1 retries 10 rejected pairs: INTER 8101,8101,8999,8999,-2x6).
  k=3: 8 tried (n=0,1,4,5,16,17 of 64), all fail: the four [0,0,*,*]
  (b)-halt at step 2 with cur=8101; [0,1,0] ends 8102; [0,1,1]
  (b)-halts at step 3 with cur=8002; the four [1,*,*] (b)-halt at
  step 2 with cur=8999 (the trap edge dies honestly). k=4: 6 tried
  (n=0,1,4,5,16,17 of 256): n=0,1,4,5 (b)-halt at step 2 with
  cur=8101; n=16 [0,1,0,0] (b)-halts at step 4 with cur=8102;
  n=17 [0,1,0,1] wins: 8001->8101->8002->8102->8001, end-of-pass,
  cur=8001==exp. Report `ARM=GC PROB=QF1 ANS=8001 TRIES=28`.
  Census: m0 inmask=1 outmask=1 n=4; m1 inmask=1 outmask=3 n=5.
- QF2: prefix 14 tries (singles [0]: 7999->8000, [1]: 7999->7999;
  pairs [0,1],[1,0]; WIDEN=1 10 pairs). k=3: 8 tried, all fail.
  k=4: 16 tried, all fail. k=5: 32 tried, all fail (no 5-step
  arrival at 8001 exists: arrivals happen at steps 2, 6, 10, ...).
  k=6: 6 tried (n=0,1,4,5,16,17 of 4096); n=17 [0,0,0,1,0,1] wins:
  7999->8000->8001->8101->8002->8102->8001, end-of-pass,
  cur=8001==exp. Report `ARM=GC PROB=QF2 ANS=8001 TRIES=76`
  (2+2+10+8+16+32+6). No WIDEN=2. Census: m0 inmask=1 outmask=1
  n=8; m1 inmask=1 outmask=3 n=5.
- QF3: prefix 14 tries. k=3: 3 tried (n=0 [0,0,0] (b)-halt step 2
  cur=8101; n=1 [0,0,1] (b)-halt step 2 cur=8101; n=4 [0,1,0]
  wins): 8001->8101->8002->8102, end-of-pass, cur=8102==exp.
  Report `ARM=GC PROB=QF3 ANS=8102 TRIES=17` (2+2+10+3).
  No WIDEN=2. Census: m0 inmask=1 outmask=1 n=4; m1 inmask=1
  outmask=3 n=4.

## Kill bar results

- F1 COMMIT-ORDER: PASS. Prereg commit `43c0baa` (PREREG.md +
  NAMECHECK.md + .gitignore only) strictly precedes this
  implementation commit in the lane-local git log.
- F2 DETERMINISM: PASS. 3/3 pairwise byte-identical.
- F3 QF1-PASS: FAIL. Binary reports
  `ARM=GC PROB=QF1 ANS=8001 TRIES=28` (preregistered 44); no
  WIDEN=2 in the QF1 section, last-4 INTER tail exactly
  8101,8002,8102,8001 as preregistered. The TRIES mismatch is a
  prereg arithmetic error (see Verdict): the winner [0,1,0,1] is
  the 6th tried sequence at k=4 (n=0,1,4,5,16,17), not the 22nd.
- F4 QF2-PASS: PASS. `ARM=GC PROB=QF2 ANS=8001 TRIES=76`, no
  WIDEN=2 in the QF2 section, last-6 INTER tail
  8000,8001,8101,8002,8102,8001.
- F5 QF3-PASS: PASS. `ARM=GC PROB=QF3 ANS=8102 TRIES=17`, no
  WIDEN=2 in the QF3 section, last-3 INTER tail 8101,8002,8102.
- F6 CENSUS: PASS. All twelve CENSUS lines match Section 3 exactly
  (QF1: m0 n=4, m1 n=5; QF2: m0 n=8, m1 n=5; QF3: m0 n=4, m1 n=4;
  m2/m3 inmask=1 outmask=2 n=1 in all three worlds).
- F7 FROZEN-INTACT: PASS. Lane gc_uni.zag / gc_base.zag /
  uni_nomain.zag match the GEN-CYCLES digests.
- F8 OPACITY: PASS. Banned-token grep over all built sources empty;
  every exercised identifier a bare integer.
- F9 SETUP-HYGIENE: PASS. qf_setups.zag has no `while`, no
  `exec_map`, no repeat/fixpoint check: facts + MAPs + teaches only.
- F10 FEEDBACK-GENUINE: PASS. The 801 edge list is exactly
  {7999->8000, 8000->8001, 8001->8101, 8002->8102} and the 802 edge
  list exactly {8101->8002, 8102->8001, 8001->8999}; neither
  relation contains a directed cycle on its own, so the
  8001->8101->8002->8102->8001 loop is genuinely emergent from
  A+B composition.

## What the result shows (and does not show)

Shows: (1) the frozen sequences+halting mechanism runs genuine
multi-structure feedback cycles with zero mechanism change: a
full-loop return through an emergent 2-structure loop (QF1), a
tail-entry lasso stopping at the first-repeat parity (QF2), and a
mid-loop stop by exact-length matching (QF3) all solve via bounded
trials terminating at end-of-pass; (2) the feedback is genuine by
the F10 audit: neither MAP's relation cycles alone (both are DAGs),
so the closed trajectory exists only through A+B composition, with
A's output feeding B and B's output feeding A; this is distinct
from the alternating chain (C420 T1), whose trajectory never
revisits a state, and from single-structure oscillation (C425),
whose cycle lives in one MAP's relation; (3) the (b) halt is
correctly silent on all three winning feedback trials while
honestly stopping the dead-end losing trials (including every
sequence lured by the 8001->8999 trap edge); (4) the kind-contract
machinery admits exactly the {0,1}^k sequences at every length,
keeping the search on the two feedback structures.

Does not show: a PASS verdict for this wave (F3 as frozen fails on
the TRIES constant; the verdict is INFORMATIVE-FAIL per the
committed mapping). Data-dependent stop-at-loop-closure remains
outside the halting vocabulary (characterized in PREREG Section 4,
not patched). Overshoot trials (k>d) are never executed; SEQMAX=8/
CAP=8 remain frozen bounds; exp is still supplied for end-to-end
verification.

## Cycle family map: closed

With this battery, every family from C420's boundary list is now
tested on the frozen sequences+halting mechanism: pipelines (U),
single-structure fixpoint chains (GEN-CYCLES), alternating
two-structure fixpoint chains (C420 T1), data-dependent operative
halting (C420 T2), the additive HALT-kind signal (C420 T3),
oscillatory cycles (C425: period-2, lasso, period-3),
convergent-signal cycles (C428: interior depth-3/5, walk limit),
and multi-structure feedback cycles (this battery: full-loop
return, tail-entry lasso, mid-loop stop). The envelope grew by
testing, not by redesign: gc_uni.zag and gc_base.zag are
byte-identical to the GEN-CYCLES frozen digests throughout.
