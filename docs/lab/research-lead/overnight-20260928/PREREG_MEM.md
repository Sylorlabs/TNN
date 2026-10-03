# PREREG: Memory Strategy Invention Test (H-MEM)

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation)
**Hypothesis H-MEM:** A learner given (a) per-slot experience statistics gathered
by generic counters and (b) a small menu of candidate eviction policies can
develop an effective memory strategy under store pressure by replaying its own
experience trace to evaluate candidates and selecting the winner, with an
inspectable trace. The selected policy must depend on the stream statistics,
not be hardcoded.

## Background

- All current TNN mechanisms use researcher-designed memory: fixed slots,
  first-fit allocation, no eviction policy beyond "full = fail"
  (unified_learn.zag proc_store, 16 slots, returns -1 when full).
- F-LEAK (confirmed in H-STRESS): failed bridge splits waste proc slots.
  This test does not repair F-LEAK; it builds the eviction layer that could
  later subsume "full = fail".
- Canonical state section 7: "Memory strategy invention (fifth frontier):
  not attempted."
- Micah's innovation standard lists "new memory organization" as a claim
  type requiring novelty, utility, reuse, causal evidence, transfer, and
  red-team survival.

## Honest scope

This test targets bounded L2 at best (experience-driven menu selection among
authored candidate policies). It is NOT L3: the learner does not invent new
policy forms. L3 memory invention would require inventing a policy outside the
menu (for example consolidation of subsumed procedures, or a novel replacement
rule the researcher did not enumerate). The candidate menu is authored; the
experience statistics are gathered generically; the selection is data-driven.
If the learner cannot select from experience and needs a hardcoded policy, that
is a negative result and will be reported as such.

## Mechanism

Store: 8 slots (small, to force pressure quickly). Slot metadata: used flag,
proc_id, use_count (queries served), last_q (sequence number of most recent
query, 0 if never queried), store_seq (insertion order). Layout mirrors
unified_learn.zag proc_store conventions (used at +0, descriptor bytes after).

Experience statistics are updated generically on every query event. No policy
logic lives in the counters.

Candidate policies (authored menu):
- LFU: evict the slot with minimum use_count (tie: lowest slot index).
- LRU: evict the slot with minimum last_q (tie: lowest slot index).
- FIFO: evict the slot with minimum store_seq.
- LIFO: evict the slot with maximum store_seq.
- RANDOM: evict the ((ev*7+3) % nstored)-th stored slot in slot order, where ev
  is the pressure event number. Deterministic. Reported as context only.

Replay cost: let the trace be the sequence of query events. The recent window
is the last 20 queries. cost(policy) = number of recent-window queries that
target the policy's victim. Rationale: recent queries predict near-future
queries; a good eviction minimizes near-future misses. This cost model is
authored; the selection given the cost model is experience-driven.

Selection: argmin over candidates by replay cost. Tie-break order is fixed and
disclosed: LFU, LRU, FIFO, LIFO, RANDOM. On each pressure event the learner
prints every candidate's victim and cost, the winner, and the victim's stats.

Pressure handling: when a learn arrives and the store is full, run selection,
evict the winner's victim, store the new procedure.

## Frozen streams

Stream A (stable popularity; expected selection: LFU):
- Learn procs 0..7 into slots 0..7, in order.
- Early queries (48): (proc0,14),(proc1,10),(proc2,7),(proc3,5),(proc4,4),
  (proc5,2),(proc6,4),(proc7,2).
- Recent window queries, last 20 (window pairs in order):
  (proc6,5),(proc0,3),(proc1,3),(proc2,2),(proc3,2),(proc4,2),(proc5,1),(proc7,2).
- Totals: p0=17, p1=13, p2=9, p3=7, p4=6, p5=3, p6=9, p7=4.
- Last-query order: p6 oldest, then p0,p1,p2,p3,p4,p5,p7.
- Hand-computed victims and costs: LFU -> slot5 (proc5), cost 1.
  LRU -> slot6 (proc6), cost 5. FIFO -> slot0 (proc0), cost 3.
  LIFO -> slot7 (proc7), cost 2. Winner: LFU, strictly.
- Pressure: 4 events, learning proc8, proc9, proc10, proc11.
- Expected: P1 evicts slot5; P2 evicts proc8 (0 uses); P3 evicts proc9;
  P4 evicts proc10. Final store holds procs 0,1,2,3,4,6,7,11.

Stream B (shifting popularity; expected selection: LRU):
- Learn procs 0..7 into slots 0..7, in order.
- Phase 1 (40): (proc3,40).
- Phase 2 (46): (proc6,6),(proc2,6),(proc4,6),(proc5,6),(proc7,6),(proc1,6),
  (proc0,10).
- Recent window = last 20 queries (seq 67..86 of 86).
- Totals: p0=10, p1=6, p2=6, p3=40, p4=6, p5=6, p6=6, p7=6.
- Hand-computed victims and costs: LFU -> slot1 (proc1), cost 6.
  LRU -> slot3 (proc3), cost 0. FIFO -> slot0 (proc0), cost 10.
  LIFO -> slot7 (proc7), cost 4. Winner: LRU, strictly.
- Pressure: 4 events, learning proc8, proc9, proc10, proc11.
- Expected: P1 evicts slot3 (proc3, stale despite 40 uses); P2 evicts proc8;
  P3 evicts proc9; P4 evicts proc10. Final store holds procs 0,1,2,4,5,6,7,11.

## Kill bars (frozen)

- K-M1 (not hardcoded, not first-in): On Stream A the first victim is slot5;
  on Stream B the first victim is slot3. Neither is slot0 (the FIFO victim).
  The selected policy's replay cost is strictly below the FIFO victim's cost
  on both streams (A: 1 < 3; B: 0 < 10).
- K-M2 (inspectable): For every pressure event the program prints each
  candidate policy, its victim slot and proc, its replay cost, the selected
  winner, and the victim's use_count and last_q. The result doc quotes this
  trace verbatim.
- K-M3a (Stream A retention): After all 4 pressure events, procs 0,1,2,3,4
  (pre-pressure totals of 6 or more) are all still stored. The first-evicted
  proc (proc5) had the minimum pre-pressure use_count.
- K-M3b (Stream B recency over frequency): proc3, despite the highest total
  use_count (40), is the first evicted (it is stale). proc0 (10 recent
  queries) is still stored at the end.
- K-M4 (deterministic): Two consecutive runs of the binary produce
  byte-identical stdout (verified with cmp).
- K-M5 (data-dependent selection): The selected policy on Stream A (LFU)
  differs from the selected policy on Stream B (LRU). Same code, different
  experience, different memory strategy.

Verdict rule: H-MEM SURVIVES iff all six bars pass. Any failure kills the
hypothesis as stated (re-characterization requires a transparent prereg
amendment and re-freeze, not a post-hoc edit).

## Controls and baselines

- FIFO-only and RANDOM-only victims and costs are printed as context on both
  streams (not bars).
- The "full = fail" baseline (current unified_learn.zag behavior) is the
  status quo this mechanism would replace: it stores nothing under pressure.

## Deliverables

- mem_learn.zag (pure Zag, no Python anywhere)
- MEM_RAW_OUTPUT.txt (authoritative raw stdout, both runs)
- MEM_RESULT.md (verdict per bar, trace excerpts, classification, limits)

Classification if SURVIVES: bounded L2 experience-driven policy selection.
Explicitly not L3, not policy-form invention.
