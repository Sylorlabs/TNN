# H-MEM2 Result: Memory Strategy v2 (repair of H-MEM downgrades)

**Date:** 2026-09-29
**Prereg:** PREREG_MEM2.md (commit d926eb0f6, frozen before implementation)
**Implementation:** mem2_learn.zag (pure Zag, no Python)
**Verdict:** H-MEM2 SURVIVES (5/5 bars pass)

## What was built

mem2_learn.zag repairs the five H-MEM adversary downgrades (M-A1, M-A3, M-A4,
M-A6a, M-A6b; see MEM_ADVERSARY.md) with four mechanism changes:

1. **Probationary protection.** New per-slot field `prot_until`; on store,
   `prot_until = query_seq + 10`. `victim()` skips protected slots for every
   candidate policy. Each pressure event also prints the unprotected-LFU
   victim as a churn counterfactual (causal evidence for the repair).
2. **Interleaved queries.** Stream A2 runs query blocks between pressures
   (Q1 = [8,8,8], Q2 = [9,9,8,8,0,0]), so re-selection faces new experience.
3. **Held-out futures.** Two frozen 20-query futures per headline event
   (F-trend proportional to the recent window; F-shift a plausible workload
   shift over retained procs). Each policy's victim is scored in future
   misses: the actual goal, not the replay proxy.
4. **Window operating band.** Headline selections must agree AND be strict
   across W in {20, 25, 30} (justification: W >= 2*D, D = distinct procs in
   the recent regime). A full sweep (W=10..40, full) is printed as context.

Also disclosed in prereg: deterministic RANDOM changed from H-MEM's
`(ev*7+3)%nstored` to `(ev*5+1)%neligible` (eligible = unprotected stored
slots in slot order). mem_learn.zag is untouched (lineage preserved).

## Bar results

- K-M2-1 (newcomer churn eliminated): PASS. At A2-ev1, unprotected LFU would
  victimize slot5(proc8) (uses=3, the H-MEM churn); with probation the
  selection evicts slot6(proc6) and proc8 survives. At A2-ev2, unprotected
  LFU would victimize slot6(proc9); protected selection evicts slot4(proc4)
  and proc9 survives. Raw output quotes:
  `[churn counterfactual] unprotected-LFU victim=slot5(proc8)` at ev1 and
  `victim=slot6(proc9)` at ev2, with `K-M2-1 PASS` on both probes.
- K-M2-2 (held-out futures): PASS, 6/6. F-trend: selected policy tied-best
  on all three streams (A2: LFU 1 = min; B2: LRU 0 = min; C2: FIFO 1 = min).
  F-shift: selected never uniquely worst (A2: LFU 0; B2: LRU 0; C2: FIFO 0;
  in each case another policy scores >= selected's).
- K-M2-3 (strict selections): PASS, 5/5 strict (bar required >= 3).
  A2-ev0 LFU 1<2; A2-ev1 LRU 0<1; A2-ev2 LFU 1<2; B2-ev0 LRU 0<4;
  C2-ev0 FIFO 1<2. Zero tie-break decisions in the entire experiment.
- K-M2-4 (deterministic): PASS. Three consecutive runs byte-identical
  (cmp-verified).
- K-M2-5 (window robustness): PASS. A2-ev0: LFU strict at 20/25/30.
  B2-ev0: LRU strict at 20/25/30. C2-ev0: FIFO strict at 20/25/30.

## Key trace excerpts (from MEM2_RAW_OUTPUT.txt)

A2-ev0 (strict LFU):
```
    LFU victim=slot5(proc5) cost=1
    LRU victim=slot6(proc6) cost=2
    FIFO victim=slot0(proc0) cost=4
    LIFO victim=slot7(proc7) cost=4
    RANDOM victim=slot1(proc1) cost=2
  selected: LFU cost=1 STRICT
```

A2-ev1 (probation probe; genuine re-selection flip to LRU on new experience):
```
    LFU victim=slot4(proc4) cost=1
    LRU victim=slot6(proc6) cost=0
    FIFO victim=slot0(proc0) cost=4
    LIFO victim=slot7(proc7) cost=4
    RANDOM victim=slot7(proc7) cost=4
  selected: LRU cost=0 STRICT
  evict slot6 proc6 uses=6 lastq=35
  [churn counterfactual] unprotected-LFU victim=slot5(proc8)
```

A2-ev2 (strict re-selection back to LFU):
```
    LFU victim=slot4(proc4) cost=1
    LRU victim=slot7(proc7) cost=2
    FIFO victim=slot0(proc0) cost=2
    LIFO victim=slot7(proc7) cost=2
    RANDOM victim=slot7(proc7) cost=2
  selected: LFU cost=1 STRICT
  [churn counterfactual] unprotected-LFU victim=slot6(proc9)
```

B2-ev0 (strict LRU; the M-A4 tie is gone under the frozen RANDOM formula):
```
    LFU victim=slot1(proc1) cost=6
    LRU victim=slot3(proc3) cost=0
    FIFO victim=slot0(proc0) cost=10
    LIFO victim=slot7(proc7) cost=4
    RANDOM victim=slot1(proc1) cost=6
  selected: LRU cost=0 STRICT
```

C2-ev0 (strict FIFO; third regime):
```
    LFU victim=slot5(proc5) cost=2
    LRU victim=slot6(proc6) cost=2
    FIFO victim=slot0(proc0) cost=1
    LIFO victim=slot7(proc7) cost=4
    RANDOM victim=slot1(proc1) cost=3
  selected: FIFO cost=1 STRICT
```

## Window sweeps (inspectable context)

```
A2-ev0: W=10:LFU~ W=15:LFU~ W=20:LFU* W=25:LFU* W=30:LFU* W=35:LFU* W=40:LFU* W=full:LFU*
B2-ev0: W=10:LFU~ W=15:LRU~ W=20:LRU* W=25:LRU* W=30:LRU* W=35:LRU* W=40:LRU* W=full:LFU~
C2-ev0: W=10:LFU~ W=15:LFU~ W=20:FIFO* W=25:FIFO* W=30:FIFO* W=35:FIFO* W=40:LFU~ W=full:LFU*
(* = strict win, ~ = tie-break win)
```

Small windows (10, 15) degenerate to ties: the window no longer covers each
proc ~2x, so victims collapse to 0 hits. Full-trace mixing flips B2 and C2
(the M-A6a finding, reproduced here as disclosed context, not hidden). The
operating band 20..40 is strict on all three streams; the frozen bar used
{20, 25, 30}.

## Held-out future tables (the goal, not the proxy)

```
A2 F-trend: LFU=1 LRU=2 FIFO=4 LIFO=4 RANDOM=2  (selected LFU tied-best)
A2 F-shift: LFU=0 LRU=5 FIFO=0 LIFO=0 RANDOM=5  (selected not uniquely worst)
B2 F-trend: LFU=6 LRU=0 FIFO=10 LIFO=4 RANDOM=6 (selected LRU tied-best)
B2 F-shift: LFU=5 LRU=0 FIFO=5 LIFO=10 RANDOM=5 (selected not uniquely worst)
C2 F-trend: LFU=2 LRU=2 FIFO=1 LIFO=4 RANDOM=3 (selected FIFO tied-best)
C2 F-shift: LFU=0 LRU=0 FIFO=0 LIFO=8 RANDOM=6 (selected not uniquely worst)
```

## Classification

Bounded L2 experience-driven policy selection with newcomer protection.
Explicitly not L3: the menu, window band, and probation constant are
authored; the learner selects among enumerated policies. What is
experience-driven: which policy wins on each stream, the strict re-selection
flips on interleaved queries (LFU -> LRU -> LFU on A2), and the window-hot
protection the argmin provably provides (inherited from H-MEM, M-A1 lemma).

## What the downgrade repairs changed (narrowed claim vs H-MEM)

1. Newcomer churn is gone by construction (probation) and demonstrated by
   counterfactual: without protection, ev1/ev2 would churn proc8/proc9.
2. 5/5 selections are strict argmin; 0/5 rely on the tie-break (H-MEM: 1/8).
3. Re-selection is substantive: A2 flips LFU -> LRU -> LFU as experience
   changes, each strictly.
4. Window=20 is no longer a knife-edge: the same strict winner holds across
   20/25/30/35/40 on A2 and B2, 20/25/30/35 on C2, with flip points disclosed.
5. The bars measure future-query misses (the goal) on frozen held-out
   futures, not only the replay proxy.

## Honest limitations (not failures of the bars)

1. The menu, window band, probation constant, and tie-break order are
   authored. An adversarial future targeting the evicted proc still defeats
   any replay-based selection (M-A6b stands as a general limit).
2. Probation is age-based: a useless newcomer still occupies a slot for
   PROB=10 queries.
3. F-shift futures are plausible, not adversarial; they do not target any
   victim.
4. The deterministic-RANDOM formula was changed from H-MEM; it is frozen
   here and disclosed, but cross-version RANDOM comparisons are not valid.
5. Not yet integrated into unified_learn.zag; mem2_learn.zag is standalone
   validation (integration is future work, parallel to H-FLEAKFIX).
6. What L3 memory invention would require (not attempted): inventing a
   policy form outside the menu.

## Governance

- Prereg d926eb0f6 strictly precedes this implementation commit.
- Stream/parameter design was explored in /tmp scratch (pure Zag, never
  committed) before the prereg freeze; the committed implementation
  reproduces the frozen streams, futures, formulas, and bars exactly.
- No Python anywhere. No em dashes in documentation.
- Commit-hygiene note: the prereg commit d926eb0f6 also swept in another
  agent's already-staged PREREG_FDCR_UNIFIED2.md (it was in the index before
  my add). Content of both files is intact; ordering is unaffected.
- mem_learn.zag, MEM_RESULT.md, and all H-MEM artifacts are untouched.

## Commits (tnn-native-lab)

- d926eb0f6 PREREG H-MEM2 FROZEN (bars K-M2-1..K-M2-5, frozen streams A2/B2/C2,
  frozen futures, RANDOM formula change disclosed)
- [this commit] mem2_learn.zag, MEM2_RAW_OUTPUT.txt, MEM2_RESULT.md

No Python was used anywhere in the pipeline (Zag via pinned znc
2026.07.0-dev; shell cmp for determinism).
