# PREREG_MEM6.md -- H-MEM6: recency-weighted merit (preregistration)

Status: FROZEN. Written and committed BEFORE any H-MEM6 implementation,
build, or execution. This document alone governs the H-MEM6 verdict.
No em dashes are used in this file (loop documentation rule).

## 1. The downgrade being repaired

H-MEM5 was DOWNGRADED (not killed) by its red team (PREREG_MEM5_ADV.md).
The killing fixture X-M5-1: slot7 holds proc7 with uses=2, both queries
ancient and absent from the 20-query operating window. Protected mode
shields slot7 and evicts slot6 at replay cost 2; unprotected mode evicts
slot7 at cost 0. Outcome: LIFO -> LFU, slot6 -> slot7, cost harm 0 -> 2.
Supporting fixture X-M5-2: changing slot7 from uses=1 to uses=2 creates a
one-query protection cliff (a single ancient query flips the outcome).

Causal diagnosis (agreed): protection merit is all-time (st_uses) while
replay harm is window-scoped. The mismatch lets ancient, currently
irrelevant uses protect a cost-zero eviction target. A principled repair
must use recent, window-aligned evidence, not a higher cumulative
threshold.

## 2. Hypothesis H-MEM6

RECENCY-WEIGHTED MERIT: within the age window (seq < prot), a slot is
protected iff its procedure was queried at least MERITK (2) times in the
operating window (the same window replay_cost uses). All-time uses no
longer confer protection by themselves: stale merit (uses >= MERITK from
ancient, window-absent queries) expires.

Consequences, stated before execution:
- Merit and harm are scope-unified: a slot with window cost below
  MERITK can never be shielded. The X-M5-1 pattern (shield a cost-0
  slot while a queried procedure is sacrificed) cannot recur.
- The X-M5-2 one-query cliff is gone at the margin: uses=1 vs uses=2
  all-time no longer flips the outcome when both are window-absent.
- Fresh merit still protects: a slot with >= 2 in-window queries inside
  its age window is protected exactly as before, so protection remains
  load-bearing.

## 3. Mechanism (exact, frozen)

New function winuses(W,ST,Q,s,win): count of queries for slot s's pid in
Q[max(0,nq-win)..nq), the same window replay_cost uses.

elig() becomes: stored, and (not protected, or seq >= prot, or
winuses(W,ST,Q,s,win) < MERITK). Equivalently: within the age window a
slot is protected iff winuses >= MERITK (2).

Threading: Q and win are threaded through elig, nelig, victim, and all
their callers (argmin_pol, select_win, is_strict_up, fut_score2,
fut_score3, churn_verdict, pressure, main). pressure uses win=20 (its
hardcoded operating window); all main() victim call sites use win=20.

replay_cost is refactored to share winuses() with elig() (identical loop,
one implementation), so protection merit and eviction harm are computed
over the same evidence window.

MERITK remains 2. Only the evidence scope changes (all-time -> window).

## 4. Frozen kill bars

### K-M6-1: stale merit expires (X-M5-1 fixture, frozen from PREREG_MEM5_ADV.md)

Fixture: slots 0..6: pid=i, uses={10,20,30,40,50,60,70},
lastq={91..97}, sseq={0..6}, prot=50 (expired). Slot7: pid=7, uses=2,
lastq=101, sseq=7, prot=109 (open: seq=105 < 109). Q (26): Q[0]=7,
Q[1]=7, Q[2]=0, Q[3]=1, Q[4]=2, Q[5]=3, then 6x proc0, 3x proc1,
3x proc2, 2x proc3, 2x proc4, 2x proc5, 2x proc6. win=20, ev=0.
Hand-derived expectation: winuses(proc7)=0 < 2, so slot7 is evictable
under protection. Protected: LFU -> slot7 (cost 0). Unprotected: LFU ->
slot7. Verdict 0.

PASS iff: wprot=LFU(0), vprot=slot7, cprot=0, wun=LFU(0), vun=slot7,
cv=0. Any other outcome is a FAIL of H-MEM6.

### K-M6-2: no cliff at the margin (X-M5-2a and X-M5-2b fixtures)

Variant A: K-M6-1 fixture with slot7 uses=1. Variant B: K-M6-1 fixture
with slot7 uses=2 (verbatim X-M5-1). Both are window-absent
(winuses=0). Hand-derived expectation: both yield verdict 0 with
identical (wprot, vprot, cprot) = (LFU, slot7, 0). The 1->2 all-time
flip changes nothing because the marginal query is ancient.

PASS iff: both variants yield wprot=LFU(0), vprot=slot7, cprot=0,
cv=0. Any divergence between the variants is a FAIL of H-MEM6.

### K-M6-3: fresh merit protects (F-M6-3b, setup_flip3)

Fixture: same slot state as the H-MEM5 setup_flip2 (slot7: proc7,
uses=2, lastq=0, sseq=7, prot=108; slots 0..6 as in setup_flip2;
seq=100, nq=20, ev=5), but Q gives every proc >= 2 in-window queries:
3x proc0, 2x each of procs 1..4, 4x proc5, 3x proc6, 2x proc7.
Window costs: p0:3, p1:2, p2:2, p3:2, p4:2, p5:4, p6:3, p7:2.
Hand-derived expectation: winuses(proc7)=2 >= MERITK, so slot7 is
protected under R5. Protected (slot7 excluded): LFU -> slot5 (cost 4),
LRU -> slot5 (cost 4), FIFO -> slot0 (cost 3), LIFO -> slot6 (cost 3),
RANDOM -> slot5 (cost 4); argmin -> FIFO, victim slot0, cost 3.
Unprotected: LFU -> slot5 (cost 4), LRU -> slot7 (cost 2),
FIFO -> slot0 (cost 3), LIFO -> slot7 (cost 2), RANDOM -> slot2
(cost 2); argmin -> LRU, victim slot7, cost 2. Verdict 1
(CHURN-FULL:1: winner flips FIFO->LRU, eviction slot0(proc0)->
slot7(proc7)).

PASS iff: wprot=FIFO(2), vprot=slot0, wun=LRU(1), vun=slot7, cv=1.
This proves fresh merit protection is load-bearing: without it the
winner would be LRU, not FIFO.

### K-M6-4: fallback under window merit (F-M6-3c)

Hand-built all-window-protected state: 8 slots, each uses=2, lastq=91+s,
sseq=s, prot=108, seq=100, nq=20; Q = 3x each of procs 0..3, 2x each of
procs 4..7 (every pid >= 2 window queries). pressure(W,Q,ST,9,8).
Hand-derived expectation: every slot protected -> FALLBACK-ALL-PROTECTED
emitted, fbf=1, unprotected argmin: LFU -> slot0 (cost 3), LRU -> slot0
(cost 3), FIFO -> slot0 (cost 3), LIFO -> slot7 (cost 2),
RANDOM -> slot6 (cost 2); argmin -> LIFO, victim slot7, cost 2; proc8
stored, no crash.

PASS iff: FALLBACK-ALL-PROTECTED emitted, st_fbf==1, fbsel=LIFO(3),
has_proc(8)==1.

### K-M6-5: preserved bars (regression)

PASS iff the full stdout is byte-identical to the frozen
MEM5_RAW_OUTPUT.txt EXCEPT: (a) the K-M5-3b section is replaced by the
F-M6-3b section (same frozen shape, different fixture); (b) the K-M5-3c
section is replaced by the F-M6-3c section; (c) the K-M6-1 and K-M6-2
sections are appended. All other bars (STREAM A2/B2/C2 with band checks,
sweeps, futures, pressures; flat fixture; K-M4-1a, K-M4-2, K-M4-3a,
K-M4-3b; K-M5-1, K-M5-2, K-M5-3a; K-M3-1; K-M2-3; K-M2-5) must report
PASS exactly as in the frozen MEM5 output. Rationale for the two
supersessions: setup_flip2's slot7 uses=2 is stale merit under R5 (zero
window queries), so the old flip honestly no longer occurs there; the
old fallback fixture's slots 0..6 have zero window queries, so that
state is honestly no longer all-protected.

### K-M6-6: determinism

PASS iff three consecutive runs are byte-identical, exit 0, and contain
zero FAIL lines.

## 5. Explicit supersessions

- K-M5-3b (setup_flip2 expectation) is SUPERSEDED by F-M6-3b
  (setup_flip3). The stale fixture's "merit-positive" premise is
  redefined by H-MEM6: uses=2 with zero window queries is stale merit,
  not merit. The :1 path is preserved with fresh merit. This is a
  mechanism-driven fixture replacement, recorded before execution, not
  a bar weakened after results.
- K-M5-3c (fallback fixture) is SUPERSEDED by F-M6-3c. "All-protected"
  now means all-window-protected.
- setup_flip2 remains in source (unfrozen lineage) but is no longer
  asserted on.

## 6. Honest remaining boundaries

- The window-uses=1 vs 2 knife-edge remains, now in the correct scope: a
  single in-window query is not merit. A future red team may probe
  whether the in-window cliff produces harm; the scope unification
  bounds it (a shielded slot always has window cost >= 2, so the
  X-M5-1 pattern of shielding a cost-0 slot cannot recur).
- Protection can still increase replay cost when it shields a cost-2
  slot while a cost-3 slot is sacrificed; that is the mechanism working
  as intended, honestly reported by CHURN-FULL:1.
- Menu, operating window, and MERITK are authored. Not L3.

## 7. Execution and governance rules

- Pure Zag only: no Python anywhere (editing, generators, verifiers,
  analysis, harnesses, scratch). Disclosure does not cure a violation.
- This prereg is committed alone BEFORE any H-MEM6 implementation,
  build, or execution. The prereg commit must be a strict ancestor of
  the implementation commit.
- Verdict names the exact frozen bars above. No bar may be weakened or
  redefined after results.
- Commits are local (tnn-native-lab branch); nothing is pushed without
  Micah's explicit approval. Commit only explicitly owned paths; never
  broad-stage concurrent workers' files. On .git/index.lock, wait for
  the live lock; never remove it.
- Never commit binaries, caches, or unnecessary generated artifacts.
- Negative evidence and lineage are preserved; invalid claims are
  marked RETRACTED, SUPERSEDED, INVALID, or VOID.
- Classification remains bounded L2, not L3. No mechanism here
  establishes L3.

## 8. Hand-derivation record (pre-execution)

All expectations in section 4 were hand-derived from the frozen
mechanism in section 3 before any implementation or execution. The
derivations are reproduced in full in MEM6_RESULT.md with the raw
outputs they are checked against.
