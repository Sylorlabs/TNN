# PREREG: H-MEM Adversary Attacks (M-A1..M-A6)

**Date:** 2026-09-29
**Status:** FROZEN (committed before any attack execution)
**Role:** Independent adversary for H-MEM. Assume the claim is false.
  Attack it as bounded L2 (experience-driven menu selection). Do NOT demand
  L3 invention; the builder explicitly disclaimed it.

## Claim under attack

H-MEM SURVIVES (6/6). A learner with per-slot experience statistics
(use_count, last_q) and a menu of 5 candidate eviction policies
(LFU, LRU, FIFO, LIFO, RANDOM) selects a memory strategy under store
pressure by replaying its own query trace (recent-window miss cost) and
picking argmin. Stream A selected LFU, Stream B selected LRU.
Classified bounded L2, explicitly not L3.

## Frozen attack list

### M-A1: newcomer churn and the hot-newcomer probe

Suggested kill: "M-A1 kills the 'effective strategy' reading if a hot
newcomer is evicted while a cold old proc survives."

Frozen stream (mem_adv.zag, attack A1):
- Learn procs 0..7 into slots 0..7.
- Queries: procs 0..7 x6 each (48 queries, seq 1..48).
- Pressure ev0, window=20, learn proc8.
  Expected: LFU/LRU/FIFO/RANDOM tie at cost 0; LFU wins tie-break;
  evict slot0 (proc0); store proc8 at slot0.
- Queries: proc8 x5 (seq 49..53). proc8 is now LFU's victim
  (uses 5 < 6) with 5 window hits.
- Pressure ev1, window=20, learn proc9.
  Expected: LRU wins strictly (cost 0 < LFU cost 5); evict slot1
  (proc1); hot newcomer proc8 SURVIVES.
- Queries: procs 2..7 x4 each (seq 54..77; uses now 10 each).
  proc9 has 0 uses.
- Pressure ev2, window=20, learn proc10.
  Expected: 5-way cost tie at 0; LFU/LRU/LIFO/RANDOM agree on victim
  proc9; LFU wins tie-break; unqueried newcomer churned.

Kill criterion: KILL the "effective strategy" reading ONLY IF the
mechanism evicts a newcomer with strictly more window hits than some
surviving proc (hot newcomer evicted while a colder proc survives).
Note the lemma to be checked: this is unreachable when "hot" means
strictly greatest window hits, because argmin never selects a policy
whose victim costs more than the minimum. The empirical probe tests
the reachable boundary (LFU victimizes the hot newcomer; argmin must
overrule it).

Downgrade criterion: DOWNGRADE the "revisable, data-driven re-selection
on every pressure event" language if post-first-pressure events show
multi-policy victim agreement with winner-cost ties (selection vacuous).

### M-A2: trace staleness (two regimes)

Frozen stream (attack A2):
- Learn procs 0..7.
- Regime 1 (ancient): procs 0..7 x100 each (800 queries, seq 1..800).
- Regime 2 (recent): proc0 x20 (seq 801..820; fills the window).
- Pressure ev0, window=20, learn proc8.
- Baseline: identical regime 2, but regime 1 = procs 0..7 x1 each.

Kill/downgrade criterion: DOWNGRADE "experience-driven selection" if the
800-query ancient history flips the selected policy relative to the
baseline. KILL only if the flipped-to policy is also worse on a
regime-2-continuation future (not expected; criterion recorded for
completeness).

Expected: NO-KILL. The windowed cost should make selection robust to
ancient history. The attack also records the evicted victim's printed
lifetime stats (expect uses=100 for an ancient proc) as an
inspectability caveat: the trace display conflates lifetime with recent.

### M-A3: degenerate agreement

Dedicated frozen stream (attack A3):
- Learn procs 0..7.
- Queries: procs 1..7 x5 each (35 queries); proc0 NEVER queried.
- Pressure ev0, window=20, learn proc8.
  Expected: LFU/LRU/FIFO victim = slot0 (proc0), cost 0 (3-policy
  victim agreement); LIFO victim = slot7 (proc7), cost 5;
  RANDOM (ev0, k=3) victim = slot3 (proc3), cost 0.
  Winner: LFU by 4-way cost tie. Selection among the tied candidates
  is vacuous; the authored tie-break decides.

Tabulation (no new code): classify each of the builder's 8 pressure
events from MEM_RAW_OUTPUT.txt by (a) victim agreement across policies,
(b) winner-cost ties.

Downgrade criterion: DOWNGRADE the "developed a strategy" reading if a
majority of all examined pressure events (builder's 8 + A3) show
victim agreement across 2+ policies or a winner-cost tie resolved by
the authored tie-break.

### M-A4: independent recomputation

Re-derive the prereg's hand-computed victims and costs from the
committed SOURCE (mem_learn.zag), not from the doc. Check every
victim slot, every cost, the RANDOM policy arithmetic
(k = ((ev*7+3) % nstored)), tie-break application, and the vicA_ok /
vicB_ok check logic.

Kill criterion: KILL the "6/6" if any frozen bar's expectation is
arithmetically wrong in a way that makes a bar actually fail.
Downgrade criterion: DOWNGRADE the record if frozen expectations
contain inaccuracies that do not fail bars (already spotted candidate:
prereg says Stream B "Winner: LRU, strictly", but RANDOM also scores
cost 0 at ev0, so the win was by tie-break, not strict).

### M-A5: governance

- (a) Prereg commit 304918d7b strictly precedes implementation commit
  75842e367: ancestor check plus timestamps, both on tnn-native-lab.
- (b) No Python in the builder's pipeline: no .py files in the work
  directory; "python" appears in builder files only in "Pure Zag.
  No Python." declarations.
- (c) Independent rebuild of mem_learn.zag from the committed source
  with the pinned znc (2026.07.0-dev); two runs byte-identical via
  shell cmp; fresh output byte-identical via cmp against the committed
  MEM_RAW_OUTPUT.txt.

Kill criterion: ANY governance failure KILLS H-MEM as a preregistered
result (per loop governance: commit-order violations and Python
use are void-on-sight).

### M-A6: menu-rigging (proxy versus future)

M-A6a: window-size fragility (attack code):
- Replicate Stream B exactly; select with window in {10, 20, 40, 86}
  on a fresh store each time.
  Hand-derived expectations: win=10 -> LFU (4-way tie at 0);
  win=20 -> LRU (tie with RANDOM at 0, tie-break); win=40 -> LRU
  strictly (costs 6,0,10,6); win=86 -> LFU (tie LFU/LIFO at 6).
- Replicate Stream A exactly; select with window in {10, 20, 68}.
  Hand-derived expectations: win=10 -> LRU (tie LRU/FIFO at 0);
  win=20 -> LFU strictly (costs 1,5,3,2); win=68 -> LFU strictly
  (costs 3,9,17,4).
Downgrade criterion: DOWNGRADE the K-M5 "data-dependent selection"
narrative if either stream's selected policy varies with the authored
window parameter (selection is then (data x authored-window)-dependent,
not purely experience-driven).

M-A6b: held-out future (attack code):
- Replicate Stream A through pressure ev0 (window=20, learn proc8).
  Record each policy's victim proc BEFORE eviction.
  Expected victims: LFU->proc5, LRU->proc6, FIFO->proc0, LIFO->proc7,
  RANDOM->proc3. Selected: LFU (strict, cost 1).
- Future F1 (trend continuation): 20 queries of proc0. Count per-policy
  future misses = future queries hitting that policy's victim.
  Expected: LFU 0, LRU 0, FIFO 20, LIFO 0, RANDOM 0.
- Future F2 (regime flip): 20 queries of proc5 (the evicted proc).
  Expected: LFU 20, LRU 0, FIFO 0, LIFO 0, RANDOM 0.
Downgrade criterion: DOWNGRADE the word "effective" in the hypothesis
if the proxy's strict winner is the menu's worst performer on any
held-out future. The bars measure the proxy, never the goal; the
proxy-goal link is assumed, not demonstrated. (Not a kill:
stationarity is the cost model's stated rationale; the attack maps
the boundary of what was shown.)

## Verdict rule

- H-MEM KILLED iff any KILL criterion fires.
- Else H-MEM SURVIVES iff all six frozen bars verify as written.
- Qualifier WITH DOWNGRADE iff any DOWNGRADE criterion fires.
  Downgrades narrow the interpretation; they do not rewrite history.

## Deliverables (all committed to tnn-native-lab)

1. PREREG_MEM_ADV.md (this file; committed BEFORE any attack runs).
2. mem_adv.zag (pure Zag attack harness) + MEM_ADV_RAW_OUTPUT.txt.
3. MEM_ADVERSARY.md (verdict per attack: KILL / DOWNGRADE / NO-KILL
   with evidence).

## Method constraints

Pure Zag only. No Python anywhere, including analysis and verification
(shell cmp, grep, awk, sort, diff only). znc 2026.07.0-dev pinned.
