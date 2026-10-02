# PREREG: Memory Strategy v2 (H-MEM2) -- repair of H-MEM adversary downgrades

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation; see commit order note)
**Hypothesis H-MEM2:** The H-MEM eviction-selection mechanism, repaired with
(1) a probationary period protecting newcomers, (2) queries interleaved
between pressure events, (3) held-out future-query evaluation, and (4) a
justified multi-window operating band, selects experience-driven eviction
policies strictly (not by tie-break), protects newcomers from churn, and its
selections validate against future queries rather than only the replay proxy.

## Background

H-MEM SURVIVED WITH DOWNGRADE (adversary `f020e94f4`, `MEM_ADVERSARY.md`).
The downgrades this test repairs:

- M-A1: post-first-pressure "re-selection" was degenerate newcomer churn.
  Repair: probationary protection for newly stored procedures.
- M-A3: 7 of 8 pressure events were winner-cost ties resolved by the authored
  tie-break; only 1 strict selection. Repair: streams designed (and verified
  in /tmp scratch, pure Zag, before this freeze) for strict argmin, plus
  interleaved queries so re-selections face substantive choices.
- M-A4: Stream B "LRU strictly" was a tie with RANDOM won by tie-break.
  Repair: disclosed change of the deterministic-RANDOM formula (see below);
  all headline selections are strict wins, verified in scratch.
- M-A6a: window=20 was load-bearing and authored. Repair: the selection must
  agree AND be strict across the operating band W in {20, 25, 30}, with the
  band justified (W >= 2*D, D = distinct procs in the recent regime, so each
  proc is expected to appear ~2x and degenerate 0-ties collapse), plus a
  full window sweep printed as inspectable context with flip points disclosed.
- M-A6b: bars measured the replay proxy, never future-query performance.
  Repair: two frozen held-out futures per headline event; the selected policy
  is scored on future misses (the actual goal).

What is NOT claimed: L3 policy-form invention (menu still authored); tuning
of the window or probation constant from experience (both authored and
disclosed); optimality against adversarial futures.

## Mechanism (delta vs H-MEM)

Store: 8 slots x 28 bytes. Layout mirrors mem_learn.zag plus one field:
+0 used, +4 proc_id, +8 use_count, +12 last_q, +16 store_seq,
+20 prot_until (query-seq number until which the slot is protected).

Probation: on store, prot_until = current query seq + PROB, PROB = 10
(authored, disclosed; about half the operating window: long enough for a
newcomer to see real traffic, short enough to expire). victim() skips
protected slots for every policy. If every stored slot were protected
(pathological), selection falls back to unprotected choice and reports it;
this does not occur in the frozen streams. At each pressure event the program
also prints the unprotected-LFU victim as context: the churn that probation
prevents (causal evidence, not a bar).

Candidate policies: LFU, LRU, FIFO, LIFO, RANDOM (same authored menu as
H-MEM). Deterministic RANDOM: k-th eviction-eligible slot in slot order,
k = (ev*5+1) % neligible. This DIFFERS from H-MEM's (ev*7+3) % nstored;
the change is disclosed here and frozen in this prereg. Rationale: any fixed
deterministic stand-in is equally arbitrary; this one is frozen before the
committed implementation and the streams are verified against it.

Replay cost: recent-window queries hitting the victim's proc, window W.
Selection: argmin; tie-break order LFU, LRU, FIFO, LIFO, RANDOM (disclosed,
unchanged from H-MEM).

Interleaving: queries run between pressure events on stream A2 (see below),
so re-selection is tested against new experience (addresses H-MEM honest
limitation #2, static trace under pressure).

## Frozen streams

All proc ids are small ints; learn order is always procs 0..7 into slots 0..7.

### Stream A2 (stable popularity; headline: strict LFU at ev0)

- Ancient (33 queries, in order):
  5,5, 0,0,0,0, 7,7,7,7, 3,3,3,3, 6,6,6,6,
  1,1,1,1,1, 2,2,2,2,2, 4,4,4,4,4
- Recent window (20 queries, in order):
  6,6, 5, 0,0,0,0, 7,7,7,7, 3,3,3,3, 1,1, 2,2, 4
- Hand-verified (scratch): totals p5=3 (unique min), last_q oldest p6;
  W=20 costs LFU->p5:1, LRU->p6:2, FIFO->p0:4, LIFO->p7:4, RANDOM->p1:2.
  Winner LFU strictly. Band W=20/25/30: all LFU strictly (scratch-verified).
- ev0: learn proc8. Then interleave Q1 = [8,8,8].
- ev1: learn proc9 (probation probe). Scratch-verified: unprotected-LFU
  victim = slot5(proc8) = the churn H-MEM exhibited; protected selection:
  LFU->p4:1, LRU->p6:0, FIFO->p0:4, LIFO->p7:4, RANDOM->p7:4.
  Winner LRU strictly (a genuine re-selection flip on new experience:
  proc6 went cold). proc8 survives.
- Interleave Q2 = [9,9,8,8,0,0]. ev2: learn proc10. Scratch-verified:
  LFU->p4:1, LRU->p7:2, FIFO->p0:2, LIFO->p7:2, RANDOM->p7:2.
  Winner LFU strictly; unprotected-LFU victim = slot6(proc9); proc9 survives.

### Stream B2 (shifting popularity; headline: strict LRU at ev0)

- Phase 1 (40): proc3 x40.
- Phase 2 (46, in order): 6x6, 2x6, 4x6, 5x6, 7x6, 1x6, 0x10.
- Hand-verified (scratch): W=20 costs LFU->p1:6, LRU->p3:0, FIFO->p0:10,
  LIFO->p7:4, RANDOM->p1:6. Winner LRU strictly.
  Band W=20/25/30: all LRU strictly (scratch-verified).
- ev0: learn proc8. Single pressure.

### Stream C2 (scan workload, oldest-loaded now cold; headline: strict FIFO)

- Ancient (30 queries, in order):
  5, 6,6,6,6, 0(x10), 7,7, 3,3, 1,1,1, 2,2,2,2, 4,4,4,4
- Recent window (20 queries, in order):
  6,6, 5,5, 0, 7,7, 3,3, 1,1, 2, 4, 7, 3, 1, 2, 4, 7, 3
- Hand-verified (scratch): totals p5=3 (unique min), last_q oldest p6;
  W=20 costs LFU->p5:2, LRU->p6:2, FIFO->p0:1, LIFO->p7:4, RANDOM->p1:3.
  Winner FIFO strictly. Band W=20/25/30: all FIFO strictly (scratch-verified).
- ev0: learn proc8. Single pressure.

## Frozen held-out futures (never seen by the selector)

Per headline event, two futures of 20 queries each, scored as misses per
policy (queries targeting that policy's ev0 victim):

- A2 F-trend (proportional to W=20 window):
  0,0,0,0, 7,7,7,7, 3,3,3,3, 6,6, 1,1, 2,2, 5, 4.
  Scratch: misses LFU=1, LRU=2, FIFO=4, LIFO=4, RANDOM=2. Selected LFU = min.
- A2 F-shift (attention moves to mid-tier retained procs):
  1x5, 2x5, 4x5, 6x5.
  Scratch: misses LFU=0, LRU=5, FIFO=0, LIFO=0, RANDOM=5.
  Selected LFU not uniquely worst.
- B2 F-trend: 0x10, 1x6, 7x4.
  Scratch: misses LFU=6, LRU=0, FIFO=10, LIFO=4, RANDOM=6. Selected LRU = min.
- B2 F-shift (workload moves to proc7, a retained proc):
  7x10, 0x5, 1x5.
  Scratch: misses LFU=5, LRU=0, FIFO=5, LIFO=10, RANDOM=5.
  Selected LRU not uniquely worst.
- C2 F-trend (same as W=20 window):
  6,6,5,5,0,7,7,3,3,1,1,2,4,7,3,1,2,4,7,3.
  Scratch: misses LFU=2, LRU=2, FIFO=1, LIFO=4, RANDOM=3. Selected FIFO = min.
- C2 F-shift (scan continues onto newer procs):
  7x8, 3x6, 1x6.
  Scratch: misses LFU=0, LRU=0, FIFO=0, LIFO=8, RANDOM=6.
  Selected FIFO not uniquely worst.

The futures are plausible regime continuations/shifts over retained procs;
none targets the selected policy's victim adversarially (contrast M-A6b F2).

## Kill bars (frozen)

- K-M2-1 (newcomer churn eliminated): After A2-ev1, proc8 is still stored,
  and the printed unprotected-LFU context victim is slot5(proc8) (the churn
  that would have occurred). After A2-ev2, proc9 is still stored, and the
  unprotected-LFU context victim is slot6(proc9).
- K-M2-2 (held-out futures measure the goal): For each of the 3 headline
  events x 2 futures: on F-trend, the selected policy's miss count equals
  the minimum over the menu; on F-shift, the selected policy is not uniquely
  worst (some other policy has misses >= selected's).
- K-M2-3 (strict, experience-driven selections): At least 3 of the 5
  pressure events (A2-ev0, A2-ev1, A2-ev2, B2-ev0, C2-ev0) select by strict
  argmin (winner cost strictly below every other candidate's). Expected per
  scratch: 5/5 strict (LFU, LRU, LFU, LRU, FIFO).
- K-M2-4 (deterministic): Three consecutive runs of the binary produce
  byte-identical stdout (verified with cmp).
- K-M2-5 (window robustness): For each headline event, the selected policy
  is identical across W in {20, 25, 30} and the win is strict at each
  (A2: LFU, B2: LRU, C2: FIFO). A full sweep (W=10,15,20,25,30,40,full) is
  printed as inspectable context; small windows may degenerate to ties and
  full-trace mixing may flip B2/C2 (disclosed, not bars).

Verdict rule: H-MEM2 SURVIVES iff all five bars pass. Any failure kills or
downgrades per the loop's transparent amendment process.

## Controls and baselines

- Unprotected-LFU victim printed at every pressure event (churn counterfactual).
- Window sweep printed per headline event (M-A6a style transparency).
- The H-MEM binary/behavior is the baseline: newcomer churn at ev1/ev2.

## Deliverables

- mem2_learn.zag (pure Zag, no Python anywhere)
- MEM2_RAW_OUTPUT.txt (authoritative raw stdout, all runs)
- MEM2_RESULT.md (verdict per bar, trace excerpts, sweep tables,
  classification, remaining limits)

Classification if SURVIVES: bounded L2 experience-driven policy selection
with newcomer protection; explicitly not L3, not policy-form invention.

## Commit order note

Stream/parameter design was explored in /tmp scratch (pure Zag, never
committed) before this freeze. This prereg commit strictly precedes the
implementation commit. The committed implementation must reproduce the
frozen streams, futures, formulas, and bars exactly.

## Honest limitations (carried forward)

1. The candidate menu, window band, and probation constant are authored.
   What is experience-driven: which menu item wins, when, and the
   re-selection flips.
2. F-shift futures are plausible, not adversarial; an adversarial future
   targeting the evicted proc defeats any replay-based selection (M-A6b).
3. Probation is age-based, not merit-based; a useless newcomer still
   occupies a slot for PROB queries.
4. What L3 memory invention would require (not attempted): inventing a
   policy form outside the menu.
