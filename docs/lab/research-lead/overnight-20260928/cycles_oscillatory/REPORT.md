# REPORT: CYCLES-OSCILLATORY -- Verdict PASS

Date: 2026-10-03. Worker: cycles-oscillatory.
Lane: `docs/lab/research-lead/overnight-20260928/cycles_oscillatory/`.
Battery: preregistered oscillatory-cycle tests for GEN-CYCLES/C420's
frozen sequences+halting mechanism. Pure Zag, pinned safebin znc.
Prereg committed alone (`9f15278`); implementation commit follows in
this same commit (see lane-local git log). No amendments: every frozen
prediction matched exactly.

## Verdict: PASS

The frozen, unmodified sequences+halting mechanism handles oscillatory
cycles. All three workloads solve with the exact preregistered TRIES,
INTER trace tails, and census lines:

- O-Q1 (period-2, on-cycle start): `ARM=GC PROB=QO1 ANS=6001 TRIES=15`.
  The winning trial is [0,0,0,0] at k=4 (first sequence-phase trial of
  its length): 6001->6002->6001->6002->6001, end-of-pass halt,
  6001==exp. The (b) fixpoint halt never fires on the revisits, which
  is the correct non-misfire: (b) is period-1-specific and the
  oscillation is period-2.
- O-Q2 (lasso: 2-step tail + period-2): `ARM=GC PROB=QO2 ANS=6003
  TRIES=15`. Winner [0,0,0,0] at k=4:
  6001->6002->6003->6004->6003, end-of-pass, 6003==exp. The answer is
  the first repeated state (seen at step 2, repeated at step 4); the
  frozen trial stops exactly at the detection-point parity without any
  repeat-detection machinery.
- O-Q3 (period-3): `ARM=GC PROB=QO3 ANS=6001 TRIES=14`. Winner [0,0,0]
  at k=3 (n=0, the first sequence-phase trial overall):
  6001->6002->6003->6001, end-of-pass, 6001==exp.

## Results

Build: one binary from pinned safebin znc (zagd-unavailable warning is
environmental and non-blocking, as in GEN-CYCLES/C420):
- qo_fbin (frozen base + frozen U + frozen mechanism; QO1, QO2, QO3)

Runs: 3/3 byte-identical (cmp); digest:
- qo_run1.txt:
  dca3f6403da85e079b9efd539404cb9c24144bf79e97fec401e0c0e8b2f0bc2b

Traces (all predictions from PREREG Section 3 confirmed):
- QO1: prefix 13 tries (1 admitted single [0]: 6001->6002; 0 admitted
  x!=y pairs; WIDEN=1 retries all 12 rejected pairs, each failing on
  a COUNT miss with one INTER= line). k=3: [0,0,0] admitted only,
  fails with cur=6002 (INTER 6002,6001,6002). k=4: [0,0,0,0] wins
  (INTER 6002,6001,6002,6001). No (b) or (c) halt on any oscillator
  trial. No WIDEN=2.
- QO2: prefix 13 tries (single [0]: 6001->6002 != 6003; WIDEN=1 12
  pairs all miss). k=3: [0,0,0] fails with cur=6004
  (INTER 6002,6003,6004). k=4: [0,0,0,0] wins
  (INTER 6002,6003,6004,6003). No WIDEN=2.
- QO3: prefix 13 tries (single [0]: 6001->6002; WIDEN=1 12 pairs all
  miss). k=3: [0,0,0] wins immediately
  (INTER 6002,6003,6001). k=4 never runs. No WIDEN=2.

Census (all as preregistered): QO1 m0 inmask=1 outmask=1 n=6; QO2 m0
inmask=1 outmask=1 n=8; QO3 m0 inmask=1 outmask=1 n=6; m1/m2/m3
inmask=1 outmask=2 n=1 in all three worlds.

## Kill bar results

- O1 COMMIT-ORDER: PASS. Prereg commit `9f15278` (PREREG.md +
  NAMECHECK.md + .gitignore only) strictly precedes this implementation
  commit in the lane-local git log.
- O2 DETERMINISM: PASS. 3/3 pairwise byte-identical.
- O3 QO1-PASS: PASS. `ARM=GC PROB=QO1 ANS=6001 TRIES=15`, no WIDEN=2
  in the QO1 section, last-4 INTER tail 6002,6001,6002,6001.
- O4 QO2-PASS: PASS. `ARM=GC PROB=QO2 ANS=6003 TRIES=15`, no WIDEN=2
  in the QO2 section, last-4 INTER tail 6002,6003,6004,6003.
- O5 QO3-PASS: PASS. `ARM=GC PROB=QO3 ANS=6001 TRIES=14`, no WIDEN=2
  in the QO3 section, last-3 INTER tail 6002,6003,6001.
- O6 CENSUS: PASS. m0 n=6/8/6 with inmask=1 outmask=1; m1/m2/m3
  inmask=1 outmask=2 n=1, all present with exact per-workload counts.
- O7 FROZEN-INTACT: PASS. Lane gc_uni.zag / gc_base.zag /
  uni_nomain.zag match the GEN-CYCLES digests.
- O8 OPACITY: PASS. Banned-token grep over all built sources empty;
  every exercised identifier a bare integer.
- O9 SETUP-HYGIENE: PASS. qo_setups.zag has no `while`, no
  `exec_map`, no repeat/fixpoint check: facts + MAPs + teaches only.

## What the PASS shows (and does not show)

Shows: (1) the frozen halting vocabulary handles oscillatory cycles
with zero mechanism change: period-2 on-cycle, a tail-entry lasso, and
period-3 all solve via bounded exact-length trials terminating at
end-of-pass; (2) the (b) fixpoint halt is correctly period-1-specific:
it neither misfires on period-2/3 revisits nor is needed for any win;
(3) the chain kind rule admits pure repetitions ([0,0,0],
[0,0,0,0]) exactly when the masks allow, and the COUNT distractors
(which can only miss here) prune the trial space to a single admitted
sequence per length, keeping TRIES at 14/15; (4) the preregistered
detection-vocabulary analysis (PREREG Section 4) is empirically
consistent: the winner in each workload is [0 x k] for the smallest
k>=3 with k congruent to d mod p (repetitions are never tried at k=2,
since the prefix enumerates x!=y only), so for fixed-period value
queries the absent repeat-history halt is observationally equivalent
to exact-length trials.

Does not show: data-dependent stop-at-first-repeat (period unknown at
query time with destructive continuation) remains outside the halting
vocabulary; that gap is characterized, not patched, per the frozen
mechanism rule. Convergent-signal cycles and multi-structure feedback
cycles remain untested. SEQMAX=8/CAP=8 remain frozen bounds; a
period-9+ oscillator would fail on bounds, which this battery does not
probe. exp is still supplied for end-to-end verification.

## Composition envelope status

After this battery the frozen sequences+halting mechanism covers:
pipelines (U), re-applicable sequences over single-structure fixpoints
(GEN-CYCLES), alternating multi-structure fixpoint sequences (C420
T1), data-dependent operative halting (C420 T2), the additive HALT-kind
signal (C420 T3), and now oscillatory cycles: period-2 bounded runs
on-cycle (QO1), tail-entry lasso runs stopping at detection parity
(QO2), and odd-period runs (QO3). The envelope grew by testing, not by
redesign: gc_uni.zag and gc_base.zag are byte-identical to the
GEN-CYCLES frozen digests. Remaining untested cycle families from
C420's boundary list: convergent-signal cycles and multi-structure
feedback cycles.
