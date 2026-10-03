# PREREG: Memory Strategy v3 (H-MEM3) -- repair of H-MEM2 red-team downgrades

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation; see commit order note)
**Hypothesis H-MEM3:** The H-MEM2 eviction-selection mechanism, repaired so that
(1) the churn counterfactual is computed for the selected policy with an
explicit prevented/not-prevented verdict, (2) the documented all-protected
fallback actually exists in code, (3) held-out futures are machine-checked
independent of the selection window, (4) the future bar requires the selected
policy to tie the minimum rather than merely avoid being uniquely worst, and
(5) the strictness claim is scoped to skewed-popularity regimes, selects
experience-driven eviction policies strictly on skewed workloads, protects
newcomers from churn with honest causal evidence, and its selections validate
against window-independent future queries.

## Background

H-MEM2 SURVIVED WITH DOWNGRADE (red team `MEM2_ADVERSARY.md`, committed on
`tnn-native-lab`). The four downgrade findings this test repairs:

- X-M2-1a: the ev1 "churn counterfactual" printed the unprotected-LFU victim,
  but the mechanism selected LRU at ev1, and LRU's victim was slot6(proc6)
  with or without protection. The printed counterfactual described a policy
  the mechanism did not select; the "(the churn that would have occurred)"
  parenthetical was false for ev1. Repair (R1): the counterfactual is now
  computed for the SELECTED policy (protected vs unprotected victim of the
  argmin winner) and the mechanism emits an explicit CHURN-PREVENTED:1/0
  verdict. K-M2-1 is SUPERSEDED by K-M3-1 (rationale: the old bar's
  parenthetical was false for ev1; the survivor checks, newcomers still
  stored, are retained inside K-M3-1).
- X-M2-2c: every F-trend future had per-proc frequencies IDENTICAL to the
  W=20 selection window, so F-trend misses were mathematically the replay
  proxy relabeled. Repair (R3): F-trend is dropped. Six new shift futures
  (two per headline event) are each machine-checked DIST-DIFFERS against the
  W=20 window frequency vector before scoring. K-M2-2 is SUPERSEDED by K-M3-2
  (rationale: the old bar's "validates against future queries rather than
  only the replay proxy" claim was false for F-trend).
- X-M2-2a: the F-shift "not uniquely worst" bar was satisfied by 5/5 policies
  at A2, so it could not distinguish the selection from an arbitrary choice.
  Repair (R4): the bar is now "selected policy ties the minimum miss count",
  and the harness prints n_tying_min as discriminativeness context.
- X-M2-3: the 5/5 strict selections are a joint property of (mechanism +
  researcher-designed skewed streams); a flat round-robin workload degenerates
  to ties on all three band windows. Repair (R5): the strictness claim is
  scoped to skewed-popularity regimes in this prereg and in the
  classification; a flat boundary fixture is included in the harness to
  demonstrate the reported ties (documentation, not a strictness bar).
- Doc bug (X-M2-4c): the H-MEM2 prereg documented an all-protected fallback
  that was never implemented (victim() returns -1; no fallback path). Repair
  (R2): the fallback is IMPLEMENTED. When every stored slot is protected,
  selection falls back to the unprotected argmin, emits FALLBACK-ALL-PROTECTED,
  and sets the ST fallback flag. A dedicated fixture covers it (K-M3-4).

What is NOT claimed: L3 policy-form invention (menu still authored); tuning
of the window or probation constant from experience (both authored and
disclosed); optimality against adversarial futures; strictness on flat
workloads.

## Mechanism (delta vs H-MEM2)

Store: 8 slots x 28 bytes, unchanged layout (+0 used, +4 proc_id, +8
use_count, +12 last_q, +16 store_seq, +20 prot_until). ST record gains one
field: +12 fallback flag (0/1), set by pressure() on the fallback path.

Probation: unchanged (prot_until = store seq + PROB, PROB = 10; victim()
skips protected slots).

Selection: factored into argmin_pol() over the five policies with a
protection-mode parameter; behavior identical to H-MEM2 when protection
applies. If the protected argmin winner has no eligible victim (all slots
protected), selection falls back to the unprotected argmin and reports it.

Counterfactual (R1): at each pressure event, after selecting bestp, the
harness computes protected-victim = victim(bestp, use_prot=1) and
unprotected-victim = victim(bestp, use_prot=0), prints both, and prints
CHURN-PREVENTED:1 iff they differ (protection changed the selected policy's
victim), else CHURN-PREVENTED:0. On the fallback path the verdict is
CHURN-PREVENTED:0 with the fallback noted.

Candidate policies: LFU, LRU, FIFO, LIFO, RANDOM (authored menu, unchanged).
Deterministic RANDOM: k = (ev*5+1) % neligible over eligible slots in slot
order (unchanged from H-MEM2). Tie-break order LFU, LRU, FIFO, LIFO, RANDOM
(disclosed, unchanged).

Replay cost, window band {20,25,30}, interleaved queries: unchanged from
H-MEM2.

## Frozen streams

Identical to H-MEM2 (PREREG_MEM2.md): stream A2 (stable popularity; ev0
learn proc8, interleave [8,8,8], ev1 learn proc9, interleave [9,9,8,8,0,0],
ev2 learn proc10), stream B2 (shifting popularity; ev0 learn proc8), stream
C2 (scan workload; ev0 learn proc8). Headline selections: A2-ev0 LFU,
A2-ev1 LRU, A2-ev2 LFU, B2-ev0 LRU, C2-ev0 FIFO. Scratch-verified in /tmp
(pure Zag) before this freeze; expected values below are the scratch results.

## Frozen held-out futures (never seen by the selector)

Two per headline event, 20 queries each. All are near-future continuations
under shifted attention in which the evicted proc remains cold. None is
adversarial toward the selected policy (adversarial futures remain out of
scope per honest limitation 2). Expected miss tables verified in /tmp
scratch before this freeze.

A2 (selected LFU; victims LFU->proc5, LRU->proc6, FIFO->proc0, LIFO->proc7,
RANDOM->proc1):
- F-S1: 5,5, 6x5, 0x5, 7x4, 1x4.
  Expected: DIST-DIFFERS:1; misses LFU=2 LRU=5 FIFO=5 LIFO=4 RANDOM=4;
  selected unique min (n_tying_min=1).
- F-S2: 5, 6x6, 0x4, 7x4, 1x5.
  Expected: DIST-DIFFERS:1; misses LFU=1 LRU=6 FIFO=4 LIFO=4 RANDOM=5;
  selected unique min (n_tying_min=1).

B2 (selected LRU; victims LFU->proc1, LRU->proc3, FIFO->proc0, LIFO->proc7,
RANDOM->proc1):
- F-S1: 3, 1x5, 0x5, 7x5, 2x4.
  Expected: DIST-DIFFERS:1; misses LFU=5 LRU=1 FIFO=5 LIFO=5 RANDOM=5;
  selected unique min (n_tying_min=1).
- F-S2: 1x6, 0x6, 7x4, 2x4.
  Expected: DIST-DIFFERS:1; misses LFU=6 LRU=0 FIFO=6 LIFO=4 RANDOM=6;
  selected unique min (n_tying_min=1).

C2 (selected FIFO; victims LFU->proc5, LRU->proc6, FIFO->proc0, LIFO->proc7,
RANDOM->proc1):
- F-S1: 0,0, 5x5, 6x5, 7x4, 1x4.
  Expected: DIST-DIFFERS:1; misses LFU=5 LRU=5 FIFO=2 LIFO=4 RANDOM=4;
  selected unique min (n_tying_min=1).
- F-S2: 0, 5x6, 6x5, 7x4, 1x4.
  Expected: DIST-DIFFERS:1; misses LFU=6 LRU=5 FIFO=1 LIFO=4 RANDOM=4;
  selected unique min (n_tying_min=1).

The bar requires only that the selected policy ties the minimum; the
unique-min margins above are disclosed context, not additional bars.

## Frozen boundary fixtures

- Flat popularity (R5 scope): 40 round-robin queries (procs 0..7, 5x each).
  Expected: band windows 20/25/30 report TIE (LFU~ on all three per scratch).
  This is scope documentation, not a strictness bar: it demonstrates that
  strictness is a (mechanism, skewed-regime) property and that the mechanism
  reports ties honestly.
- All-protected fallback (R2): store 8 procs, run 0 queries (seq=0, all
  prot_until=10), then pressure. Expected: FALLBACK-ALL-PROTECTED emitted,
  fallback flag set, selection = unprotected argmin = LFU by tie-break
  (all replay costs 0), victim slot0(proc0), proc8 stored, no crash.

## Kill bars (frozen)

- K-M3-1 (honest counterfactual; SUPERSEDES K-M2-1): At A2-ev1 the winner is
  LRU; the selected-policy counterfactual is protected-victim=slot6(proc6),
  unprotected-victim=slot6(proc6); CHURN-PREVENTED:0 is printed; proc8 is
  still stored. At A2-ev2 the winner is LFU; the counterfactual is
  protected-victim=slot4(proc4), unprotected-victim=slot6(proc9);
  CHURN-PREVENTED:1 is printed; proc9 is still stored.
- K-M3-2 (independent futures; SUPERSEDES K-M2-2): For each of the 3
  headline events x 2 futures: DIST-DIFFERS:1 against the W=20 window vector,
  and the selected policy's miss count ties the minimum over the menu.
- K-M3-3 (preserved bars): K-M2-3 retained: at least 3 of the 5 pressure
  events select by strict argmin (expected 5/5 per scratch: LFU, LRU, LFU,
  LRU, FIFO). K-M2-5 retained: at each headline event the selected policy is
  identical across W in {20,25,30} and strict at each (A2: LFU, B2: LRU,
  C2: FIFO). The flat boundary fixture runs and reports ties (scope
  documentation; the unscoped "selects strictly" reading is narrowed).
- K-M3-4 (fallback implemented): On the all-protected fixture the fallback
  flag is set, FALLBACK-ALL-PROTECTED is emitted, the selection equals the
  unprotected argmin (LFU), proc8 is stored, and the run does not crash.
- K-M3-5 (deterministic): Three consecutive runs of the binary produce
  byte-identical stdout (verified with cmp).

Verdict rule: H-MEM3 SURVIVES iff all five bars pass. Any failure kills or
downgrades per the loop's transparent amendment process.

## Controls and baselines

- Selected-policy counterfactual printed at every pressure event (R1).
- Window sweep printed per headline event (H-MEM2 context, retained).
- n_tying_min printed per future (R4 discriminativeness context).
- DIST-DIFFERS machine-checked per future (R3 independence check).
- The H-MEM2 binary/behavior is the baseline: misdescribed ev1
  counterfactual, circular F-trend, vacuous F-shift bar, unimplemented
  fallback.

## Deliverables

- mem3_learn.zag (pure Zag, no Python anywhere)
- MEM3_RAW_OUTPUT.txt (authoritative raw stdout, all runs)
- MEM3_RESULT.md (verdict per bar, trace excerpts, classification,
  remaining limits)

Classification if SURVIVES: bounded L2 experience-driven policy selection
with newcomer protection and honest counterfactuals, on
researcher-designed skewed-popularity streams; explicitly not L3, not
policy-form invention.

## Commit order note

Mechanism deltas and future/miss tables were validated in /tmp scratch
(pure Zag, never committed) before this freeze. This prereg commit strictly
precedes the implementation commit. The committed implementation must
reproduce the frozen streams, futures, formulas, and bars exactly.

## Honest limitations (carried forward)

1. The candidate menu, window band, and probation constant are authored.
   What is experience-driven: which menu item wins, when, and the
   re-selection flips.
2. Futures are researcher-frozen and non-adversarial; an adversarial future
   targeting the evicted proc defeats any replay-based selection.
3. Probation is age-based, not merit-based; a useless newcomer still
   occupies a slot for PROB queries.
4. Strictness is a (mechanism, skewed-regime) property; flat workloads
   degenerate to ties, which the mechanism reports honestly.
5. What L3 memory invention would require (not attempted): inventing a
   policy form outside the menu.
