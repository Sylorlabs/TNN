# REPORT: CYCLES-FEEDBACK-REFIX -- Verdict PASS (bookkeeping complete)

Date: 2026-10-03. Worker: cycles-feedback-refix.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_feedback_refix/`.
Battery: fresh re-freeze of the C430 (CYCLES-FEEDBACK,
INFORMATIVE-FAIL) multi-structure feedback-cycle battery under a
corrected prereg (QF1 TRIES 44 -> 28), executed by re-running the
UNCHANGED frozen binary. Pure binary re-run; nothing rebuilt; no
source or binary modifications. Prereg (PREREG2.md + NAMECHECK.md)
committed alone (`9aea0fa`) before all re-run artifacts (see
lane-local git log).

## Verdict: PASS

All kill bars pass. The frozen C430 binary, executed unchanged,
reports exactly what the fresh prereg predicts:

- F3 (corrected): `ARM=GC PROB=QF1 ANS=8001 TRIES=28`, last-4 INTER
  tail 8101,8002,8102,8001, no WIDEN=2 in the QF1 section.
- F4: `ARM=GC PROB=QF2 ANS=8001 TRIES=76`, last-6 INTER tail
  8000,8001,8101,8002,8102,8001, no WIDEN=2.
- F5: `ARM=GC PROB=QF3 ANS=8102 TRIES=17`, last-3 INTER tail
  8101,8002,8102, no WIDEN=2.
- F6: all twelve CENSUS lines match (QF1: m0 n=4, m1 n=5; QF2:
  m0 n=8, m1 n=5; QF3: m0 n=4, m1 n=4; m2/m3 inmask=1 outmask=2
  n=1 in all three worlds).

The C430 verdict (INFORMATIVE-FAIL on the prereg arithmetic error)
stands unaltered in its own lane. This wave closes the bookkeeping:
the mechanism's behavior was always correct; only the prereg
constant was wrong, and it is now re-frozen correctly with a clean
PASS. The feedback family is closed.

## Results

Re-run: the frozen qf_fbin from the C430 lane, copied with sha256
verification (digest
c7c459e556f94f53b42be53d57f26d5fb6e024004a6511c6179599b1a48dddf3,
identical to the C430 build artifact), NOT rebuilt.
- qf_rerun1/2/3.txt: 3/3 pairwise byte-identical (cmp); digest
  538fd190e096063abf1ae6856eacc6465219a7fbc69cd1b2fe1bce2624f51b37,
  equal to the C430 qf_run1.txt digest recorded in NAMECHECK.md
  Step 1. The binary is unchanged and deterministic.

Traces (identical to C430's, byte for byte):
- QF1: prefix 14 tries (2 admitted singles, 2 admitted pairs,
  WIDEN=1 10 rejected pairs). k=3: 8 tried, all fail. k=4: 6 tried
  (n=0,1,4,5,16,17): n=0,1,4,5 (b)-halt at step 2 with cur=8101;
  n=16 [0,1,0,0] (b)-halts at step 4 with cur=8102; n=17
  [0,1,0,1] wins: 8001->8101->8002->8102->8001, end-of-pass,
  cur=8001==exp. Report `ARM=GC PROB=QF1 ANS=8001 TRIES=28`
  (2+2+10+8+6). The winner is the 6th tried sequence at k=4,
  exactly as re-frozen.
- QF2: prefix 14 tries. k=3: 8 tried, all fail. k=4: 16 tried,
  all fail. k=5: 32 tried, all fail. k=6: 6 tried; n=5
  [0,0,0,1,0,1] wins: 7999->8000->8001->8101->8002->8102->8001,
  end-of-pass, cur=8001==exp. Report
  `ARM=GC PROB=QF2 ANS=8001 TRIES=76`.
- QF3: prefix 14 tries. k=3: 3 tried (n=0,1 [0,0,0]/[0,0,1]
  (b)-halt step 2 cur=8101; n=4 [0,1,0] wins):
  8001->8101->8002->8102, end-of-pass, cur=8102==exp. Report
  `ARM=GC PROB=QF3 ANS=8102 TRIES=17`.

## Kill bar results

- F1 COMMIT-ORDER: PASS. Prereg commit `9aea0fa` (PREREG2.md +
  NAMECHECK.md + .gitignore only) strictly precedes this re-run
  commit in the lane-local git log.
- F2 DETERMINISM: PASS. 3/3 pairwise byte-identical; re-run digest
  equals the C430 run digest.
- F3 QF1-PASS: PASS (corrected bar). TRIES=28 as re-frozen.
- F4 QF2-PASS: PASS. TRIES=76.
- F5 QF3-PASS: PASS. TRIES=17.
- F6 CENSUS: PASS. All twelve CENSUS lines match.
- F7 BINARY-INTACT: PASS. Lane qf_fbin digest matches NAMECHECK.md
  Step 1; nothing rebuilt.
- F8/F9/F10: carried from C430 by reference (all PASS there on the
  byte-identical sources this binary was built from; no source
  changes and no rebuild in this wave).

## What the result shows (and does not show)

Shows: (1) the corrected prereg predicts the frozen binary's exact
behavior on all three feedback workloads, including the corrected
QF1 enumeration (tried n=0,1,4,5,16,17 at k=4; winner [0,1,0,1] at
n=17, 6th tried; TRIES=28); (2) the frozen sequences+halting
mechanism handles multi-structure feedback cycles (full-loop
return, tail-entry lasso, mid-loop stop) with zero mechanism change,
as established scientifically in C430; (3) the C430
INFORMATIVE-FAIL was purely a prereg arithmetic error, now closed
with a clean PASS under transparent re-freeze, per governance
(fresh prereg, no amendment, no retroactive bar change).

Does not show: any new scientific result beyond C430. This wave is
bookkeeping: it changes no conclusion about the mechanism, which
was vindicated by trace in C430. The cycle family map remains
closed as reported in C430: pipelines (U), single-structure
fixpoint chains (GEN-CYCLES), alternating two-structure fixpoint
chains (C420 T1), data-dependent operative halting (C420 T2), the
additive HALT-kind signal (C420 T3), oscillatory cycles (C425),
convergent-signal cycles (C428), and multi-structure feedback
cycles (C430/C430-refix) are all tested on the frozen mechanism
with zero redesign.
