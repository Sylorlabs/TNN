# PREREG: Memory Strategy v5 (H-MEM5) -- substantive merit threshold

**Date:** 2026-09-29
**Status:** FROZEN (committed before implementation; see commit order note)
**Hypothesis H-MEM5:** The H-MEM4 eviction-selection mechanism, with
probation redefined so that protection is earned solely by demonstrated
merit (uses >= MERITK = 2) and never granted by age alone (no absolute
grace), closes the X-M4-2a grace-window harm and the X-M4-2b fig-leaf
merit harm while preserving every surviving H-MEM4 claim: the R1 full
counterfactual, the R3 adversarial-target screen and L1 bar, all
regression streams, and the fallback path.

## Background

H-MEM4 SURVIVED 5/5 then DOWNGRADED on red team (`MEM4_ADV_RESULT.md`,
2026-09-29). Two attacks succeeded; the other two failed (no finding)
and one confirmed a disclosed boundary:

- X-M4-2a (grace-window harm): the exact X-M3-1b harm pattern (protected
  mechanism evicts a queried proc at replay cost 2 while the
  unprotected counterfactual evicts the never-queried newcomer at cost
  0) recurs inside the 3-query absolute grace. Slot7 newcomer (proc7,
  uses=0, age=2 < GRACE=3) is absolutely protected; protected LIFO
  evicts slot6 (proc6, uses=70) at cost 2; unprotected LFU evicts slot7
  at cost 0. Cost 0 -> 2. The builder's K-M4-2 bar used proc8 at age=9
  (past grace), so it never covered this window.
- X-M4-2b (fig-leaf merit): the same harm recurs past grace with
  uses=1 (one stale query outside the 20-query window, age=3). The
  merit gate uses>0 is satisfied by a single query.
- X-M4-1 FAILS (R1 stands: the (winner, victim) pair is exhaustive for
  the eviction outcome on all three fixtures). X-M4-4 FAILS (5/5
  regression holds; stdout md5 7921b0f4bc917d9ccb3627aa41d1ca97).
- X-M4-3 SUCCEED-AS-BOUNDARY (builder's disclosed strict-majority
  limit confirmed exactly as disclosed).

The red team's causal interpretation: closing the class needs a
substantive merit threshold (uses >= k for k > 1, or recency-weighted
merit). That is a new hypothesis, not a repair. H-MEM5 is that new
hypothesis, in its minimal form: uses >= 2, no absolute grace.

## Mechanism (R4; delta vs H-MEM4)

`elig()` is rewritten. Within the age window (st_seq(ST) < st_prot(W,s)),
a slot is protected iff st_uses(W,s) >= MERITK (2); otherwise it is
evictable. There is no absolute grace: a newcomer with 0 or 1 queries
is evictable from the moment it is stored. A meritless age-protected
slot's protection is void (as in H-MEM4); now the fig-leaf case
(uses=1) is void too, and the grace window is gone entirely.

New constant: `fn MERITK()i32 { return 2; }`. The `GRACE()` constant is
removed (superseded, not retroactively altered: H-MEM4's frozen verdicts
stand as executed).

Rationale for k=2 (authored, disclosed): a single query is not evidence
of merit (it can be a probe, a misroute, or noise); two queries are the
smallest substantive signal. A larger k would be more conservative but
is not needed to close either demonstrated attack, and k=2 is the
minimal threshold satisfying the red team's stated requirement (k > 1).

Everything else is unchanged: the 8x28 store layout, ST record, the
five authored policies and tie-break order, deterministic RANDOM,
replay_cost, the window band {20,25,30}, interleaved queries, R1
churn_verdict(), R3 l1_dist()/dist_differs2()/fut_score3(), and the
all-protected fallback path.

## Frozen fixture arithmetic (hand-derived, scratch-validated pre-freeze)

### F-M5-1 (K-M5-1; X-M4-2a fixture, frozen from PREREG_MEM4_ADV.md)

State: seq=100, nq=20, ev=0, win=20. Slots 0..6: procs 0..6, uses
{10,20,30,40,50,60,70}, lastq {91,92,93,94,95,96,97}, sseq {0..6},
prot=50 (expired). Slot7: proc7, uses=0, lastq=0, sseq=7, prot=108
(learned at seq 98, age=2). Q (20): proc0 x6, proc1 x3, proc2 x3,
proc3 x2, proc4 x2, proc5 x2, proc6 x2 (proc7 absent, cost 0).

Under H-MEM5, slot7 (uses=0 < 2) is evictable under protection, so the
protected eligible set equals the unprotected set (all 8 slots).

- LFU: min uses -> slot7, cost 0. LRU: min lastq (0) -> slot7, cost 0.
  FIFO: min sseq -> slot0, cost 6. LIFO: max sseq -> slot7, cost 0.
  RANDOM: ev=0, ne=8, k=(0*5+1)%8=1 -> slot1, cost 3.
- argmin: LFU=0 first-seen wins. wprot=LFU, vprot=slot7, cprot=0.
- Unprotected: identical. wun=LFU, vun=slot7.
- churn_verdict returns 0; print: "CHURN-FULL:0 (winner stable at LFU;
  eviction unchanged)".

The X-M4-2a harm (protected evicts proc6 at cost 2) does not occur.

### F-M5-2 (K-M5-2; X-M4-2b fixture, frozen from PREREG_MEM4_ADV.md)

State: nq=25, seq=105, ev=0, win=20. Q[0..4]=[7,1,2,3,4] (the single
merit query for proc7 is stale, outside the 20-query window);
Q[5..24] = the 20 queries above. Slots 0..6 as in F-M5-1 (prot=50,
expired at seq=105). Slot7: proc7, uses=1, lastq=50, sseq=7, prot=112
(learned at seq 102, age=3, within window).

Under H-MEM5, slot7 (uses=1 < 2) is evictable under protection. Window
costs identical to F-M5-1 (proc7 absent from Q[5..24]).

- wprot=LFU, vprot=slot7, cprot=0; wun=LFU, vun=slot7;
  churn_verdict returns 0 with "winner stable at LFU; eviction
  unchanged".

The X-M4-2b harm (protected evicts proc6 at cost 2 behind one stale
query of merit) does not occur.

### F-M5-3a (K-M5-3; frozen setup_flip state, SUPERSEDED expectation)

Frozen `setup_flip()` state (ST seq=100, nq=20; Q = 10x proc5, 5x
proc0, 5x proc6; slots 0..6 as in PREREG_MEM4.md; slot7: proc7,
uses=0, lastq=0, sseq=7, prot=108; ev=5).

Under H-MEM5, slot7 is evictable under protection (uses=0 < 2), so the
protected and unprotected eligible sets coincide (all 8 slots).

- LFU: min uses (0) -> slot7, cost 0. LRU: min lastq (0) -> slot7,
  cost 0. FIFO: min sseq -> slot0, cost 5. LIFO: max sseq (7) ->
  slot7, cost 0. RANDOM: ev=5, ne=8, k=(25+1)%8=2 -> slot2, cost 0.
- wprot=LFU, vprot=slot7, wun=LFU, vun=slot7, churn_verdict=0;
  print: "CHURN-FULL:0 (winner stable at LFU; eviction unchanged)".

This SUPERSEDES the K-M4-1b expectation (which relied on the grace
protection that H-MEM5 removes). The old flip fixture now documents
that the grace-window flip no longer occurs.

### F-M5-3b (K-M5-3; new flip fixture setup_flip2, uses=2)

Identical to setup_flip except slot7 has uses=2 (merit-positive under
MERITK=2), lastq=0, sseq=7, prot=108; ev=5. Slot7 is protected under
protection (seq=100 < 108, uses=2 >= 2).

Protected (eligible slots 0..6):
- LFU: min uses -> slot5 (uses=1), cost 10. LRU: min lastq (1) ->
  slot5, cost 10. FIFO: min sseq -> slot0, cost 5. LIFO: max sseq ->
  slot6, cost 5. RANDOM: ne=7, k=26%7=5 -> slot5, cost 10.
- argmin: FIFO=5 and LIFO=5 tie; first-seen FIFO wins.
  wprot=FIFO, vprot=slot0.

Unprotected (all 8 slots):
- LFU: min uses -> slot5 (uses=1 < 2), cost 10. LRU: min lastq (0) ->
  slot7, cost 0. FIFO: slot0, cost 5. LIFO: max sseq (7) -> slot7,
  cost 0. RANDOM: ne=8, k=26%8=2 -> slot2, cost 0.
- argmin: LFU=10, then LRU=0 < 10 wins. wun=LRU, vun=slot7.

churn_verdict returns 1; print: "CHURN-FULL:1 (winner flips
FIFO->LRU; eviction slot0(proc0)->slot7(proc7))".

This preserves :1 path coverage under the new rule and proves the
merit-positive slot's protection is load-bearing (without it the
winner would be LRU, not FIFO).

### F-M5-3c (K-M5-3; new all-merit-protected fallback fixture)

Hand-built state: seq=100, nq=20, Q = 20x proc7. All 8 slots:
pid=i, uses=2, lastq=91+i, sseq=i, prot=108 (learned at seq 98; every
slot is merit-protected under H-MEM5). pressure(ev=9, newpid=8).

- Protected argmin: no eligible slot -> victim -1 for all policies ->
  FALLBACK-ALL-PROTECTED; fbf flag=1; unprotected recomputation:
  LFU -> slot0 (all uses=2, first wins), cost 0; LRU -> slot0
  (lastq 91 min), cost 0; FIFO -> slot0, cost 0; LIFO -> slot7,
  cost 20; RANDOM: ev=9, ne=8, k=(45+1)%8=6 -> slot6, cost 0.
- argmin: LFU=0 first-seen wins. fbsel=LFU. Evict slot0, store proc8
  at slot0 (prot_until=110). churn_verdict takes the fallback path
  (returns 0 with the fallback noted). No crash.

Checks: fbf==1, fbsel==LFU, has_proc(8)==1. This replaces the old
K-M3-4 fixture (0 queries, all uses=0), which under H-MEM5 is no
longer all-protected (uses=0 < 2 makes every slot evictable, so no
fallback triggers there).

## Kill bars (frozen)

- K-M5-1 (grace-window harm closed; X-M4-2a): On F-M5-1, the protected
  mechanism selects LFU and evicts slot7 (proc7, uses=0) at replay cost
  0; wprot==LFU==wun; vprot==slot7==vun; cprot==0; churn_verdict
  returns 0 printing "CHURN-FULL:0 (winner stable at LFU; eviction
  unchanged)". The cost-0->2 harm does not occur. (If the harm
  recurred, the bar fails honestly; there is no third option.)
- K-M5-2 (fig-leaf merit closed; X-M4-2b): On F-M5-2, the protected
  mechanism selects LFU and evicts slot7 (proc7, uses=1, stale) at
  replay cost 0; wprot==LFU==wun; vprot==slot7==vun; churn_verdict
  returns 0 with "winner stable at LFU; eviction unchanged". The harm
  does not occur behind the single stale query.
- K-M5-3 (preserved and superseded bars):
  (a) K-M4-1a (F1): unchanged. At ev1 pre-pressure: wprot==LFU,
  wun==LFU, vprot==slot7, vun==slot7, cprot==0, printed verdict
  CHURN-FULL:0 "winner stable at LFU". pressure(ev=1) selects LFU,
  evicts slot7(proc8, uses=0) at cost 0; has_proc(8)==0,
  has_proc(0)==1, has_proc(9)==1.
  (b) K-M4-1b SUPERSEDED by F-M5-3a: on the frozen setup_flip state,
  wprot==LFU, vprot==slot7, wun==LFU, vun==slot7, churn_verdict==0,
  print "CHURN-FULL:0 (winner stable at LFU; eviction unchanged)".
  (c) New F-M5-3b: wprot==FIFO, vprot==slot0, wun==LRU, vun==slot7,
  churn_verdict==1, print names "winner flips FIFO->LRU" and
  "eviction slot0(proc0)->slot7(proc7)".
  (d) K-M4-2, K-M4-3a, K-M4-3b, K-M2-3, K-M2-5, the flat fixture, all
  band checks, all six held-out futures: unchanged behavior. (On every
  builder stream, every slot that is within its protection window at a
  selection event has uses >= 2 or an expired window; verified by
  scratch diff: only the fallback and K-M4-1b sections differ from the
  frozen MEM4 output.)
  (e) K-M3-4 fallback SUPERSEDED by F-M5-3c: fbf==1,
  FALLBACK-ALL-PROTECTED emitted, fbsel==LFU (unprotected tie-break),
  has_proc(8)==1, no crash.
- K-M5-4 (deterministic): Three consecutive runs of the binary produce
  byte-identical stdout (verified with cmp).

Verdict rule: H-MEM5 SURVIVES iff all four bars pass. Any failure
kills or downgrades per the loop's transparent amendment process.

## Controls and baselines

- The H-MEM4 binary/behavior is the baseline: GRACE=3 absolute
  protection, uses>0 merit gate, full counterfactual, L1>=6 plus
  strict-majority adversarial-target screen.
- The scratch differential (elig-change-only binary vs frozen
  MEM4_RAW_OUTPUT.txt, md5 7921b0f4bc917d9ccb3627aa41d1ca97) is the
  regression control: the only stdout differences are the fallback
  section and the K-M4-1b section, both intended supersessions.
- A merit-positive newcomer (uses=2) must still be protected: covered
  by F-M5-3b (slot7's protection changes the protected winner from
  LRU to FIFO).

## Deliverables

- mem5_learn.zag (pure Zag, no Python anywhere)
- MEM5_RAW_OUTPUT.txt (authoritative raw stdout, all runs)
- MEM5_RESULT.md (verdict per bar, trace excerpts, classification,
  remaining limits)

Classification if SURVIVES: bounded L2 experience-driven policy
selection with substantive-merit newcomer protection (no age-based
grace), outcome-level churn verdicts, and explicit adversarial-future
detection, on researcher-designed skewed-popularity streams;
explicitly not L3, not policy-form invention.

## Commit order note

The R4 elig() delta and all fixture arithmetic above were
hand-derived first, then validated in /tmp scratch (pure Zag, never
committed) before this freeze: (1) an elig-change-only build of
mem4_learn.zag was diffed against the frozen MEM4_RAW_OUTPUT.txt
(only the fallback and K-M4-1b sections differ, as intended); (2) the
four new fixtures (F-M5-1, F-M5-2, F-M5-3b, F-M5-3c) were executed in
scratch and reproduced the frozen expectations on first run with no
fixture tuning. This prereg commit strictly precedes the
implementation commit. The committed implementation must reproduce
the frozen streams, fixtures, formulas, and bars exactly.

## Honest limitations (carried forward and new)

1. The candidate menu, window band, and constants (PROB=10, MERITK=2,
   L1MIN=6, strict-majority target threshold) are authored. What is
   experience-driven: which menu item wins, when, and the re-selection
   flips.
2. Futures are researcher-frozen and non-adversarial; adversarial
   futures are explicitly detected and excluded, not defeated.
   Robustness against them is not claimed.
3. MERITK=2 is the minimal substantive threshold. Stale merit is a
   known residual: a procedure with uses>=2 from ancient queries and
   no recent queries is still protected (no recency weighting). That
   would be H-MEM6, not this hypothesis.
4. A newcomer is now evictable until it demonstrates merit (2
   queries). A procedure that would earn its first queries just after
   a pressure event can churn before demonstrating merit. The
   protection window is earned, not granted.
5. Strictness is a (mechanism, skewed-regime) property; flat workloads
   degenerate to ties, which the mechanism reports honestly.
6. The adversarial-target screen uses a strict-majority threshold; a
   future that punishes the victim proc at below-majority mass is not
   flagged.
7. What L3 memory invention would require (not attempted): inventing a
   policy form outside the menu.
8. Not yet integrated into the unified learner.
