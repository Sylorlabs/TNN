# H-MEM Result: Memory Strategy Invention Test

**Date:** 2026-09-29
**Prereg:** PREREG_MEM.md (commit 304918d7b, frozen before implementation)
**Implementation:** mem_learn.zag (pure Zag, no Python)
**Verdict:** H-MEM SURVIVES WITH DOWNGRADE (6/6 bars pass as written;
independent adversary narrowed the interpretation, 2026-09-29)

## What was built

An 8-slot procedure store with generic per-slot experience statistics
(use_count, last_q), a menu of five candidate eviction policies
(LFU, LRU, FIFO, LIFO, RANDOM), and a selection mechanism: replay the
learner's own query trace, compute each candidate's recent-window
(last-20-queries) miss cost, select argmin with disclosed tie-break order
(LFU, LRU, FIFO, LIFO, RANDOM). On store-full pressure, evict the winner's
victim and store the newcomer. Every pressure event prints the full
candidate/cost/winner/victim trace.

## Bar results

- K-M1a (Stream A not hardcoded, not first-in): PASS. Selected LFU;
  first victim slot5 (proc5, uses=3), not slot0 (FIFO victim, cost 3).
  Selected cost 1 strictly below FIFO cost 3.
- K-M1b (Stream B): PASS. Selected LRU; first victim slot3
  (proc3, uses=40, lastq=40), not slot0. Selected cost 0 strictly below
  FIFO cost 10.
- K-M2 (inspectable): PASS. Per-event traces printed for all 8 pressure
  events (see MEM_RAW_OUTPUT.txt). Each names every candidate, its victim
  slot and proc, its replay cost, the winner, and the victim's stats.
- K-M3a (Stream A retention): PASS. Final store: procs 0,1,2,3,4,11,6,7.
  Procs 0..4 (pre-pressure totals 6+) all retained. First-evicted proc5 had
  the minimum pre-pressure total (3).
- K-M3b (Stream B recency over frequency): PASS. proc3, despite the highest
  total use_count (40), was evicted first because it was stale (lastq=40,
  zero recent-window queries). proc0 (10 recent queries) retained. Final
  store: procs 0,1,2,11,4,5,6,7.
- K-M4 (deterministic): PASS. Two consecutive runs byte-identical
  (cmp-verified).
- K-M5 (data-dependent selection): PASS. Stream A selected LFU;
  Stream B selected LRU. Same code, different experience, different memory
  strategy. A hardcoded policy cannot do this.

## Key trace excerpts

Stream A, pressure 0 (full candidate table):

```
    LFU victim=slot5(proc5) cost=1
    LRU victim=slot6(proc6) cost=5
    FIFO victim=slot0(proc0) cost=3
    LIFO victim=slot7(proc7) cost=2
    RANDOM victim=slot3(proc3) cost=2
  selected: LFU cost=1
  evict slot5 proc5 uses=3 lastq=66
```

Stream B, pressure 0:

```
    LFU victim=slot1(proc1) cost=6
    LRU victim=slot3(proc3) cost=0
    FIFO victim=slot0(proc0) cost=10
    LIFO victim=slot7(proc7) cost=4
    RANDOM victim=slot3(proc3) cost=0
  selected: LRU cost=0
  evict slot3 proc3 uses=40 lastq=40
```

Note the Stream B result: the procedure with the highest lifetime use count
(40) is evicted first. Raw frequency would have kept it. The replay
evaluation is not a restatement of any single policy: on Stream B, LFU
(minimum total uses) selects proc1 at cost 6 while LRU selects proc3 at
cost 0. The cost model genuinely discriminates among candidates.

## Classification

Bounded L2 experience-driven policy selection. Explicitly NOT L3: the
candidate menu is authored; the learner selects among enumerated policies
rather than inventing new policy forms. The experience statistics are
gathered by generic counters; the selection is data-driven and revisable
(re-selection runs on every pressure event against the current trace).

## Honest limitations (not failures of the bars, but real weaknesses)

1. Newcomer churn: after the first eviction, the newly stored procedure
   (0 uses, never queried) becomes the immediate next victim under both
   LFU and LRU (pressure events 1-3 on both streams). The policies have no
   newcomer protection or probationary period. A stronger memory strategy
   would need one.
2. Static trace under pressure: no queries were interleaved between pressure
   events, so re-selection after event 0 was trivial. Interleaved
   query/pressure streams would stress the revisability claim harder.
3. Unbounded trace memory: the trace never forgets; ancient queries
   permanently shape last_q comparisons. A real continuing learner needs
   trace decay or summarization, otherwise very old history misleads.
4. The recent-window size (20) and the cost model are authored. The learner
   does not tune them.
5. What L3 memory invention would require (not attempted): inventing a
   policy form outside the menu, for example consolidation of behaviorally
   subsumed procedures, generational stores, or content-addressed merging.

## Relation to other work

- Does not repair F-LEAK (NQ4, separate arc by a parallel agent). The
  eviction layer built here could later subsume the "full = fail" behavior
  that F-LEAK exploits, but that integration is not attempted.
- The store layout mirrors unified_learn.zag proc_store conventions; the
  eviction layer is new and standalone. No changes were made to the unified
  learner.

## Red team (independent adversary, completed 2026-09-29)

Adversary prereg: `ef71f58f2` (M-A1..M-A6, frozen before any attack ran).
Adversary evidence and verdict: `f020e94f4`
(`mem_adv.zag`, `MEM_ADV_RAW_OUTPUT.txt`, `MEM_ADVERSARY.md`).
Pure Zag throughout; no Python.

**Verdict: H-MEM SURVIVES WITH DOWNGRADE.** All six frozen bars verify as
written and governance is clean, so the hypothesis is not killed. The
interpretation is narrowed (see below).

Per-attack results:

- M-A1 (hot newcomer): NO-KILL on the kill criterion, DOWNGRADE on
  re-selection. The kill (hot newcomer evicted while a colder proc survives)
  is unreachable by construction: a policy victimizing a proc with h window
  hits costs exactly h, so strict argmin can never evict the window-hottest
  proc. Empirically confirmed: LFU victimized a hot newcomer (cost 5) but
  argmin overruled it and selected LRU (cost 0); the newcomer survived. This
  is evidence FOR the mechanism. Downgrade: post-first-pressure events are
  degenerate newcomer churn (multi-way cost ties at 0, unqueried newcomer
  evicted), making "re-selection on every pressure event" substantively
  vacuous.
- M-A2 (trace staleness): NO-KILL. 800 ancient queries changed nothing:
  selection identical to the 8-query baseline. The windowed cost is robust to
  arbitrary ancient history. Caveat: victim stats printed in the trace are
  lifetime (an evicted proc showed "uses=100", all ancient), so the K-M2
  display conflates lifetime with recent.
- M-A3 (degenerate agreement): DOWNGRADE. 7 of the 8 builder pressure events
  show victim agreement and/or winner-cost ties decided by the authored
  tie-break. Only Stream A event 0 was a strict, non-degenerate,
  experience-driven selection.
- M-A4 (independent recomputation): NO-KILL on bars, with a RECORD
  CORRECTION (see below). All frozen arithmetic verified from source.
- M-A5 (governance): PASS. Prereg `304918d7b` is an ancestor of
  implementation `75842e367`. No Python anywhere. Independent rebuild from
  committed source: two fresh runs byte-identical via cmp, and fresh output
  byte-identical to committed MEM_RAW_OUTPUT.txt.
- M-A6a (window fragility): DOWNGRADE. Both streams' selections vary with the
  authored window size (Stream B: win10->LFU, win20->LRU, win40->LRU,
  win86->LFU; Stream A: win10->LRU, win20->LFU, win68->LFU). Window=20 is
  load-bearing for the K-M5 narrative.
- M-A6b (held-out future): DOWNGRADE of "effective". On held-out futures
  after Stream A's strict LFU win: trend continuation -> selected LFU
  tied-best (0 misses); regime flip (evicted proc5 queried x20) -> selected
  LFU strictly worst of the menu (20 misses vs 0 for all others). The bars
  measure the proxy (recent-window cost), never the goal (future misses);
  the proxy-goal link rests on an assumed stationarity rationale, not a
  demonstration.

### Record correction (M-A4)

The prereg's "Winner: LRU, strictly" for Stream B is inaccurate: RANDOM also
scored cost 0 at event 0 (victim slot3), so LRU won by the disclosed
tie-break, not strictly. No frozen bar breaks as written (K-M1b asserts the
LRU selection and slot3 victim, both true), but the headline Stream B result
must henceforth be cited as "LRU selected by tie-break over RANDOM (both
cost 0)".

### Narrowed claim the evidence supports

Argmin over replay costs selects LFU (strictly, once: Stream A event 0) and
LRU (by tie-break over RANDOM: Stream B event 0) on two authored streams
with the authored window=20. Selection is not hardcoded, provably protects
window-hot procs, is robust to ancient history, and is deterministic and
independently reproducible. What is NOT supported: "developed an effective
memory strategy" in general (held-out regime flip defeats it), or
substantive "re-selection on every pressure event" (degenerate after event
0). The window size is load-bearing and authored.

Classification stands: bounded L2 experience-driven policy selection,
explicitly not L3 and not policy-form invention.
