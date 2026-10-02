# PREREG: H-MEM4 Red Team (Adversary)

**Date:** 2026-09-29
**Status:** FROZEN (committed before any adversary implementation or execution)
**Target:** H-MEM4 repair claim, `mem4_learn.zag` at commit `9b98d1fa9`
(H-MEM4 SURVIVES 5/5; R1 full counterfactual, R2 merit-gated probation
with GRACE=3, R3 L1>=6 plus ADVERSARIAL-TARGET strict-majority screen).
**Stance:** the repair claim is assumed false. Each attack below has an
explicit frozen verdict rule. Pure Zag. No Python.

## Frozen fixture arithmetic (hand-derived, checked before execution)

Shared state skeleton for X-M4-1/2/3 (seq=100, nq=20, ev=0, win=20):
slots 0..6 hold procs 0..6 with uses {10,20,30,40,50,60,70},
lastq {91,92,93,94,95,96,97}, sseq {0,1,2,3,4,5,6}, prot 50 (expired);
Q (20, window order): proc0 x6, proc1 x3, proc2 x3, proc3 x2, proc4 x2,
proc5 x2, proc6 x2 (proc7 absent, cost 0).

### X-M4-2a fixture (grace-window harm)
Slot7: proc7, uses=0, lastq=0, sseq=7, prot=108 (learned at seq 98,
age = 100-(108-10) = 2 < GRACE=3, grace-protected, meritless).
Unprotected (up=0): LFU victim slot7 cost 0; LRU victim slot7 cost 0;
FIFO victim slot0 cost 6; LIFO victim slot7 cost 0; RANDOM ev=0 ne=8
k=1 -> slot1 cost 3. argmin: 0 first-seen -> LFU, vun=slot7, cost 0.
Protected (up=1): slot7 ineligible. LFU victim slot0 (min uses 10)
cost 6; LRU victim slot0 cost 6; FIFO victim slot0 cost 6; LIFO victim
slot6 (max sseq) cost 2; RANDOM ne=7 k=1 -> slot1 cost 3. argmin: LIFO
cost 2 < 3 < 6. wprot=LIFO, vprot=slot6(proc6, uses=70).
Verdict must read CHURN-FULL:1 (winner flips LIFO->LFU; eviction
slot6(proc6)->slot7(proc7)).

### X-M4-2b fixture (fig-leaf merit)
Same as X-M4-2a except: nq=25, seq=105, Q[0..4]=[7,1,2,3,4] (the single
merit query for proc7 is stale, outside the 20-query window),
Q[5..24] = the 20 above (window lo=5); slot7: uses=1, lastq=50,
sseq=7, prot=112 (learned at seq 102, age = 105-(112-10) = 3, not <
GRACE; seq < prot so within window; uses>0 -> merit-protected).
All costs identical to X-M4-2a: unprotected LFU evicts slot7 at cost 0;
protected LIFO evicts slot6(proc6, uses=70) at cost 2.

### X-M4-3 fixture (sub-majority adversarial future)
State of X-M4-2a at the pressure event; sel=LIFO, victim proc6.
Future F (20): proc6 x10, proc0 x4, proc1 x3, proc2 x3.
Screen 1: vp=proc6, fvp=10, 10*2=20 > 20 false -> no ADVERSARIAL-TARGET.
Screen 2: L1 vs window = |6-4|+|3-3|+|3-3|+|2-0|+|2-0|+|2-0|+|2-10|
= 2+0+0+2+2+2+8 = 16 >= 6 -> DIST-DIFFERS2.
Misses: LFU=4 (proc0), LRU=4, FIFO=4, LIFO=10 (proc6), RANDOM=3 (proc1).
Selected LIFO uniquely worst -> K-M3-2 FAIL (selected not min),
with no adversarial diagnosis.

## Attacks and frozen verdict rules

**X-M4-1 (counterfactual soundness).** Attempt to make the verdict's
natural reading ("protection changed nothing about the eviction outcome"
for :0) false. Differential check on three fixtures (K-M4-1b flip,
X-M4-2a, X-M4-2b): recompute (wun, vun) independently and compare the
evicted proc identity. SUCCEEDS iff (verdict==0 AND pid(vprot) !=
pid(vun)) OR (verdict==1 AND wprot==wun AND pid(vprot)==pid(vun)).
Any SUCCEED -> H-MEM4 KILLED (R1 dishonest). If the check holds on all
fixtures, X-M4-1 FAILS (no finding; verdict sound by construction for
its defined outcome).

**X-M4-2a (grace-window harm).** SUCCEEDS iff the frozen run shows the
protected mechanism evicting a queried proc (slot6/proc6, uses=70) at
replay cost 2 while the unprotected counterfactual evicts the
never-queried newcomer (slot7/proc7, uses=0) at cost 0: the exact X-M3-1b
harm pattern (cost 0 -> 2, queried proc sacrificed for a useless
newcomer), recurring inside the 3-query grace window. Any SUCCEED ->
H-MEM4 DOWNGRADED (R2 narrowed: merit-gating has a 3-query exception
where a uses=0 newcomer is absolutely protected).

**X-M4-2b (fig-leaf merit).** SUCCEEDS iff the same harm recurs with
slot7 at uses=1 (one stale query), age past GRACE, protected by the
merit gate: protected evicts slot6/proc6 at cost 2, unprotected evicts
slot7 at cost 0. Any SUCCEED -> H-MEM4 DOWNGRADED (R2 narrowed: the
merit threshold uses>0 is satisfied by a single query, so the X-M3-1b
harm recurs behind a fig leaf of merit).

**X-M4-3 (sub-majority targeting).** SUCCEEDS-AS-BOUNDARY iff the frozen
run shows fut_score3 returning 0 (K-M3-2 FAIL, selected uniquely worst)
with no ADVERSARIAL-TARGET on the 10/20 (50 percent, non-strict-majority)
future. This confirms the builder's disclosed limit
("strict-majority screen misses sub-majority targeting"); it does not
change the verdict.

**X-M4-4 (regression).** Rebuild `mem4_learn.zag` unmodified; md5 of
stdout must equal frozen `7921b0f4bc917d9ccb3627aa41d1ca97`; 3 runs
byte-identical; all five K-M4 bars reproduce. Source audit: no fixture
literals inside the mechanism region (lines 1..500). SUCCEEDS (as an
attack) iff any of these fail -> H-MEM4 DOWNGRADED or KILLED by severity.

## Verdict aggregation

- X-M4-1 SUCCEED -> KILLED. X-M4-4 SUCCEED -> DOWNGRADED or KILLED.
- X-M4-2a or X-M4-2b SUCCEED -> DOWNGRADED (claim narrowed, mechanism
  otherwise intact). X-M4-3 SUCCEED -> BOUNDARY (disclosure confirmed).
- All attacks FAIL -> H-MEM4 SURVIVES red team (claim stands as stated).
