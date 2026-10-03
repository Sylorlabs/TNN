# REPORT: CYCLES-CONVERGENT -- Verdict PASS

Date: 2026-10-03. Worker: cycles-convergent.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_convergent/`.
Battery: preregistered convergent-signal-cycle tests for GEN-CYCLES/C420's
frozen sequences+halting mechanism. Pure Zag, pinned safebin znc.
Prereg committed alone (`c4b99d0`); implementation commit follows in
this same commit (see lane-local git log). No amendments: every frozen
prediction matched exactly.

## Verdict: PASS

The frozen, unmodified sequences+halting mechanism handles
convergent-signal cycles. All three workloads solve with the exact
preregistered TRIES, INTER trace tails, total INTER counts, and census
lines:

- QC1 (convergent, interior answer, no-limit chain):
  `ARM=GC PROB=QC1 ANS=7004 TRIES=14`. The winning trial is [0,0,0]
  at k=3 (the first sequence-phase trial): 7001->7002->7003->7004,
  end-of-pass halt, 7004==exp. The answer is interior: the walk
  continues 7005..7010 past it, and no fixpoint exists anywhere in
  the window, so end-of-pass is the only possible operative stop.
- QC2 (convergent, deeper interior answer):
  `ARM=GC PROB=QC2 ANS=7106 TRIES=16`. The k=3 trial fails by falling
  short (cur=7104), the k=4 trial fails by falling short (cur=7105),
  and [0,0,0,0,0] at k=5 wins: 7101->...->7106, end-of-pass,
  7106==exp. With no periodicity, only the exact k=d trial can win;
  the executed failures prove the matching is exact-length, not
  approximate.
- QC3 (convergent to the chain end):
  `ARM=GC PROB=QC3 ANS=7204 TRIES=14`. Winner [0,0,0] at k=3:
  7201->7202->7203->7204, end-of-pass, 7204==exp. Arrival at the
  limit does not misfire the (b) halt (v=7204 differs from prev=7203):
  reaching the limit is correctly distinguished from being at a
  fixpoint.

## Results

Build: one binary from pinned safebin znc (zagd-unavailable warning is
environmental and non-blocking, as in GEN-CYCLES/C420/C425):
- cc_fbin (frozen base + frozen U + frozen mechanism; QC1, QC2, QC3)

Runs: 3/3 byte-identical (cmp); digest:
- cc_run1.txt:
  e3e662dc4826520a2422aa21d21ecddf4c1e40b8f21be6a5ac06e86d9cae932d

Traces (all predictions from PREREG Section 3 confirmed):
- QC1: prefix 13 tries (1 admitted single [0]: 7001->7002, no INTER
  print; 0 admitted x!=y pairs; WIDEN=1 retries all 12 rejected pairs:
  the three [0,j] pairs print INTER=7002 then COUNT-miss, the nine
  COUNT-first pairs print INTER=-2). k=3: [0,0,0] admitted only, wins
  (INTER 7002,7003,7004). Total 15 INTER= lines in the section: no
  (a)/(b)/(c) halt fired anywhere in the QC1 run. No WIDEN=2.
- QC2: prefix 13 tries (single [0]: 7101->7102 != 7106; WIDEN=1 12
  pairs all miss). k=3: [0,0,0] fails with cur=7104
  (INTER 7102,7103,7104). k=4: [0,0,0,0] fails with cur=7105
  (INTER 7102,7103,7104,7105). k=5: [0,0,0,0,0] wins
  (INTER 7102,7103,7104,7105,7106). Total 24 INTER= lines: no early
  halt anywhere. No WIDEN=2.
- QC3: prefix 13 tries (single [0]: 7201->7202; WIDEN=1 12 pairs all
  miss). k=3: [0,0,0] wins immediately
  (INTER 7202,7203,7204): the (b) halt stays silent on arrival at the
  chain end. Total 15 INTER= lines. No WIDEN=2.

Census (all as preregistered): QC1 m0 inmask=1 outmask=3 n=12;
QC2 m0 inmask=1 outmask=3 n=14; QC3 m0 inmask=1 outmask=3 n=6;
m1/m2/m3 inmask=1 outmask=2 n=1 in all three worlds.

## Kill bar results

- C1 COMMIT-ORDER: PASS. Prereg commit `c4b99d0` (PREREG.md +
  NAMECHECK.md + .gitignore only) strictly precedes this
  implementation commit in the lane-local git log.
- C2 DETERMINISM: PASS. 3/3 pairwise byte-identical.
- C3 QC1-PASS: PASS. `ARM=GC PROB=QC1 ANS=7004 TRIES=14`, no WIDEN=2
  in the QC1 section, last-3 INTER tail 7002,7003,7004, 15 INTER=
  lines total in the section.
- C4 QC2-PASS: PASS. `ARM=GC PROB=QC2 ANS=7106 TRIES=16`, no WIDEN=2
  in the QC2 section, last-5 INTER tail 7102,7103,7104,7105,7106,
  24 INTER= lines total in the section.
- C5 QC3-PASS: PASS. `ARM=GC PROB=QC3 ANS=7204 TRIES=14`, no WIDEN=2
  in the QC3 section, last-3 INTER tail 7202,7203,7204, 15 INTER=
  lines total in the section.
- C6 CENSUS: PASS. m0 inmask=1 outmask=3 n=12/14/6 with exact
  per-workload counts; m1/m2/m3 inmask=1 outmask=2 n=1, all present.
- C7 FROZEN-INTACT: PASS. Lane gc_uni.zag / gc_base.zag /
  uni_nomain.zag match the GEN-CYCLES digests.
- C8 OPACITY: PASS. Banned-token grep over all built sources empty;
  every exercised identifier a bare integer.
- C9 SETUP-HYGIENE: PASS. cc_setups.zag has no `while`, no
  `exec_map`, no repeat/fixpoint check: facts + MAPs + teaches only.

## What the PASS shows (and does not show)

Shows: (1) the frozen halting vocabulary handles convergent-signal
cycles with zero mechanism change: an interior answer on a no-limit
chain (QC1), a deeper interior answer with executed fall-short
failures proving exact-length matching (QC2), and arrival at the walk
limit (QC3) all solve via bounded exact-length trials terminating at
end-of-pass; (2) the (b) fixpoint halt is correctly
exact-equality-specific under convergence: it stays silent across all
convergent trials, including arrival at the chain end (QC3), where a
less precise "no outgoing edge" halt would have misfired; the total
INTER counts (15/24/15) prove no early halt fired anywhere in any
run; (3) the chain kind rule admits pure repetitions ([0,0,0],
[0,0,0,0,0]) exactly when the masks allow, and the COUNT distractors
prune the trial space to a single admitted sequence per length,
keeping TRIES at 14/16/14; (4) the preregistered threshold-vocabulary
analysis (PREREG Section 4) is empirically consistent: the winner in
each workload is [0 x k] for the smallest k>=3 with k=d (d = steps
from s to exp along the fresh-state walk; repetitions are never tried
at k=2), so for fixed-depth value queries the absent
change-below-threshold halt is observationally equivalent to
exact-length trials.

Does not show: data-dependent stop-at-threshold (threshold unknown at
query time with destructive continuation) remains outside the halting
vocabulary; that gap is characterized, not patched, per the frozen
mechanism rule. Overshoot trials (k>d) are never executed because the
increasing-k search stops at the first win; exact-length matching is
established from below only. Multi-structure feedback cycles remain
untested. SEQMAX=8/CAP=8 remain frozen bounds; an answer needing k>8
would fail on bounds, which this battery does not probe. exp is still
supplied for end-to-end verification.

## Composition envelope status

After this battery the frozen sequences+halting mechanism covers:
pipelines (U), re-applicable sequences over single-structure fixpoints
(GEN-CYCLES), alternating multi-structure fixpoint sequences (C420
T1), data-dependent operative halting (C420 T2), the additive HALT-kind
signal (C420 T3), oscillatory cycles: period-2 bounded runs on-cycle
(C425 QO1), tail-entry lasso runs stopping at detection parity (C425
QO2), and odd-period runs (C425 QO3), and now convergent-signal
cycles: interior answers at depth 3 and 5 on no-limit chains (QC1,
QC2) and arrival at the walk limit (QC3). The envelope grew by
testing, not by redesign: gc_uni.zag and gc_base.zag are byte-identical
to the GEN-CYCLES frozen digests. Remaining untested cycle family from
C420's boundary list: multi-structure feedback cycles.
