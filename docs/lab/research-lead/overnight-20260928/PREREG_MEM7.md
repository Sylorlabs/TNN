# PREREG_MEM7.md -- H-MEM7: decayed recency-weighted merit (preregistration)

Status: FROZEN. Written and committed BEFORE any H-MEM7 implementation
exists in the repo. This document alone governs the H-MEM7 verdict.
No em dashes are used in this file (loop documentation rule).

## 1. The open concern being attacked

H-MEM6 SURVIVED its independent red team (MEM6_ADV_RESULT.md, prereg
c52c1a60d, 54/54 checks). The red team found no structural violation,
but confirmed two real boundaries and left one open concern:

(a) The in-window 1-vs-2 merit knife-edge is real: two in-window
queries shield slot7, one in-window query leaves it evictable, and on
the X-M6-1a fixture shielding the cost-2 slot forced eviction of a
cost-9 slot (measured protection-induced harm 7, honestly reported as
CHURN-FULL:1).

(b) The fixed 20-query window is a step function: on X-M6-3a a slot
with 2 in-window queries is protected and becomes evictable the moment
the older query crosses the window edge, with no graded transition.
The red team's open concern, quoted: the window is a regime choice,
and "merit that decays smoothly rather than cliffs at 2 might
dominate it."

H-MEM7 is a mechanism-level repair of (b) that preserves the honest
load-bearing behavior of (a): replace the binary winuses >= 2 gate
with recency-weighted (decayed) merit.

## 2. Hypothesis H-MEM7

DECAYED (RECENCY-WEIGHTED) MERIT: within the age window
(seq < prot), a slot is protected iff its procedure's recency-weighted
query mass over the operating window reaches a frozen threshold.
Each in-window query contributes a linear recency weight (1 for the
oldest query in the window, win for the newest); the merit signal is
therefore smooth in recency: a query sliding out of the window sheds
weight gradually instead of flipping a binary count.

Consequences, stated before execution:
- The in-window 1-vs-2 count cliff is replaced by a recency-graded
  merit: two stale-but-in-window queries no longer confer protection,
  while two fresh queries do. R6 distinguishes by recency what R5
  could not.
- The X-M6-3a window-edge step becomes a ramp: merit decays 39, 37,
  35, ... as filler queries arrive, and protection drops exactly when
  the mass falls below threshold, while both queries are still
  inside the window.
- Fresh merit still protects by construction (age-window lemma,
  section 3), so every R5 load-bearing shape is preserved.

## 3. Mechanism (exact, frozen)

New function decmerit(W,ST,Q,s,win): sum over i in
[max(0,nq-win)..nq) of (i - lo + 1) for positions i where Q[i] equals
slot s's pid, with lo = max(0,nq-win). Weight is 1 for the oldest
query in the window, win for the newest. The maximum single-query
weight is win (20).

New constant MTHRESH() = 25, frozen, calibrated for win=20.
Rationale, frozen: (i) a single query, however fresh (max weight 20),
is never merit, preserving the R4/R5 "single query is not merit"
principle; (ii) the lightest protectable shape is a complementary
recency pair (e.g. weights 12+13 = 25); (iii) the age-window lemma
below holds exactly at 25.

elig() becomes: stored, and (not protected, or seq >= prot, or
decmerit(W,ST,Q,s,win) < MTHRESH). Equivalently: within the age window
a slot is protected iff decmerit >= 25.

Age-window lemma (frozen): any 2 queries since learning protect. A
slot's own queries since learning are among the last <= 9 queries of
Q (age window is PROB=10), so their weights are >= win-8 = 12, and
the lightest pair sums to 12+13 = 25 = MTHRESH. Hence every
fresh-merit shape from R5 is preserved by construction. Conversely,
R6-protected implies >= 2 in-window queries (one query maxes at
weight 20 < 25), so R6 only ever removes R5 protection, never adds
it: any protection decision that flips under R6 flips from
protected to evictable.

Scope decision (frozen): R6 changes protection merit ONLY.
winuses() is kept unchanged and replay_cost() stays count-based over
the same window. H-MEM7 attacks the merit cliff, not the harm scale;
unifying the harm weighting is deferred to a future hypothesis and
is named as an expected red-team attack surface (section 6).

MERITK (2) is superseded by MTHRESH for protection decisions and is
retained in source for lineage only. Threading is unchanged: Q and
win are already threaded through elig, nelig, victim, and all
callers. pressure uses win=20; all main() victim call sites use
win=20. Band/sweep windows (25, 30, full) run only on age-expired
states in this suite, so MTHRESH's win=20 calibration is never
exercised outside its design window here.

## 4. Frozen kill bars

### K-M7-1a: fresh query pair protects (recency-graded merit)

Fixture setup_m7pair(W,ST,Q,24,25), frozen: slot7 holds proc7
(uses=2 all-time, lastq=101, sseq=7, prot=109, age-open at seq=105);
slots 0..6 age-expired (prot=50). Q has nq=26; proc7's two queries
at positions 24,25; the other 24 queries are fixed fillers
(2x0,3x1,3x2,2x3,5x4,2x5,7x6) in increasing position order. Window =
Q[6..26), weights = pos-5.
Hand-derived expectation: weights 19+20 = 39 >= 25, so slot7 is
protected. Protected (slot7 excluded): LFU -> slot0 (uses 10, cost
1), LRU -> slot0 (cost 1), FIFO -> slot0 (cost 1), LIFO -> slot6
(cost 7), RANDOM -> slot1 (cost 2); argmin -> LFU, victim slot0,
cost 1. Unprotected: LFU -> slot7 (uses 2, cost 2), LRU -> slot0
(cost 1), FIFO -> slot0 (cost 1), LIFO -> slot7 (cost 2),
RANDOM -> slot1 (cost 2); argmin -> LRU, victim slot0, cost 1.
Verdict 1 (winner flips LFU->LRU; eviction slot0->slot0).

PASS iff: decmerit(slot7)=39, wprot=LFU(0), vprot=slot0, cprot=1,
wun=LRU(1), vun=slot0, cv=1. Any other outcome is a FAIL of H-MEM7.

### K-M7-1b: stale-in-window pair does NOT protect

Same fixture with setup_m7pair(W,ST,Q,6,7): proc7's two queries at
positions 6,7 (weights 1+2 = 3 < 25). Same counts as K-M7-1a (2
queries), different recency.
Hand-derived expectation: slot7 is evictable, so protected and
unprotected modes agree: LFU -> slot7 (cost 2), LRU -> slot0
(cost 1), FIFO -> slot0 (cost 1), LIFO -> slot7 (cost 2),
RANDOM -> slot1 (cost 2); argmin -> LRU, victim slot0, cost 1.
Verdict 0. Under R5 this pair would protect (winuses=2) and read
:1: R6 distinguishes by recency where R5 could not.

PASS iff: decmerit(slot7)=3, wprot=LRU(1), vprot=slot0, cprot=1,
wun=LRU(1), vun=slot0, cv=0. Any other outcome is a FAIL of H-MEM7.

### K-M7-2: merit ramp (smooth decay, no window-edge step)

Fixture, frozen: slot7 holds proc7 (uses=2, prot=120, age-open at
seq=105 < 120); slots 0..6 use prot=50 (expired, not consulted).
Q starts with 24x proc0 then 2x proc7 at Q[24],Q[25] (nq=26). Then 8
filler queries for proc0 are appended one at a time (st_query); after
each, decmerit(slot7) and elig(slot7, win=20, use_prot=1) are read.
Hand-derived expectation: at step k (k=0..8), nq=26+k, lo=6+k, the
two proc7 queries have weights (19-k)+(20-k), so decmerit = 39-2k:
39,37,35,33,31,29,27,25,23. elig = 0 (protected) for k=0..7, 1
(evictable) at k=8 when merit falls below MTHRESH=25. Protection is
lost at k=8 while both queries are still inside the window. Under R5
(count-based) the slot would stay protected until k=20: the step is
now a ramp.

PASS iff all nine (decmerit, elig) pairs match
(39,0),(37,0),(35,0),(33,0),(31,0),(29,0),(27,0),(25,0),(23,1).
Any deviation is a FAIL of H-MEM7.

### K-M7-3: fresh merit protects (F-M6-3b, setup_flip3, PRESERVED)

The H-MEM6 setup_flip3 fixture is preserved byte-identical: slot7's
two proc7 queries are the newest in the window (positions 18,19;
weights 19+20 = 39 >= 25), so slot7 stays protected under R6, and
every replay cost is unchanged (replay_cost is count-based).
Hand-derived expectation: identical to H-MEM6: wprot=FIFO(2),
vprot=slot0, wun=LRU(1), vun=slot7, cv=1.

PASS iff the F-M6-3b section output is byte-identical to the frozen
MEM6_RAW_OUTPUT.txt section. This bar proves the decayed merit
preserves the honest load-bearing :1 path.

### K-M7-4: fallback under decayed merit (F-M7-3c)

Hand-built all-decayed-protected state (supersedes F-M6-3c, section
5): 8 slots, each uses=2, lastq=91+s, sseq=s, prot=108, seq=100,
nq=20. Q layout (positions 0..19):
0,1,2,3,0,1,2,3,4,5,6,7,7,6,5,4,3,2,1,0.
Decmerit per pid (weights = pos+1): p0: 1+5+20=26, p1: 2+6+19=27,
p2: 3+7+18=28, p3: 4+8+17=29, p4: 9+16=25, p5: 10+15=25,
p6: 11+14=25, p7: 12+13=25. Every slot >= 25: all protected.
pressure(W,Q,ST,9,8).
Hand-derived expectation: FALLBACK-ALL-PROTECTED emitted, fbf=1;
unprotected argmin: LFU -> slot0 (cost 3), LRU -> slot0 (cost 3),
FIFO -> slot0 (cost 3), LIFO -> slot7 (cost 2), RANDOM -> slot6
(cost 2); argmin -> LIFO(3), victim slot7, cost 2 TIE (RANDOM also
cost 2); proc8 stored at slot7, prot_until=110, no crash. The
per-policy victims and costs are unchanged by construction (counts:
p0..p3: 3, p4..p7: 2).

PASS iff: FALLBACK-ALL-PROTECTED emitted, st_fbf==1, fbsel=LIFO(3),
has_proc(8)==1.

### K-M7-5: preserved bars (regression)

Baseline: the frozen MEM6_RAW_OUTPUT.txt
(md5 b505e265efe2a48d78d57be85c66a6ad, verified in-repo before the
freeze).
PASS iff the full stdout is byte-identical to that baseline EXCEPT:
(a) the F-M6-3c section header, hand-built description line, and
check/PASS lines are replaced by the F-M7-3c versions (the
per-policy victim/cost lines, FALLBACK-ALL-PROTECTED emit, evict
and store lines are unchanged); (b) the K-M7-1a, K-M7-1b, and K-M7-2
sections are appended after K-M6-2. All other bars (STREAM A2/B2/C2
with band checks, sweeps, futures, pressures; flat fixture; K-M4-1a,
K-M4-2, K-M4-3a, K-M4-3b; K-M5-1, K-M5-2, K-M5-3a; K-M3-1; K-M2-3;
K-M2-5; F-M6-3b; K-M6-1; K-M6-2) must report PASS exactly as in the
frozen MEM6 output.
Rationale (frozen, derived before execution): at every preserved
selection event, either (i) every slot is age-expired (seq >= prot),
so elig never consults merit (all stream/sweep/band/future fixtures:
A2 seq>=53, B2 seq>=86, C2 seq>=50, flat seq>=40, M4AA/M4AW seq=53);
or (ii) the age-open slots' protection decisions are identical under
R6 by the age-window lemma or by zero merit: A2-ev1 proc8 slot
(decmerit 57 >= 25, protected as under R5), A2-ev2 proc8 slot
(39 >= 25) and proc9 slot (31 >= 25), M4-ev1 proc8 slot (0 queries,
evictable as under R5), setup_xm51 slot7 (queries outside the
window, decmerit 0, evictable), setup_flip3 slot7 (decmerit 39,
protected), harm fixtures (slot7 decmerit 0). Since R6-protected
implies R5-protected, no slot can gain protection; the only
decisions that can flip are protected->evictable, and the frozen
analysis shows exactly one such flip in the suite: the F-M6-3c
fixture state (superseded, section 5).

### K-M7-6: determinism

PASS iff three consecutive runs are byte-identical, exit 0, and
contain zero FAIL lines.

## 5. Explicit supersessions

- F-M6-3c is SUPERSEDED by F-M7-3c. Under R6 the old Q layout leaves
  slots 0,1,2 with decmerit 6,15,24 < 25, so the old fixture state is
  honestly no longer all-protected; the fallback bar would fail there
  for the right reason (decayed merit working as designed). The new
  layout constructs the all-protected state with complementary
  recency pairs, keeping the per-policy victims and costs frozen.
  This is a mechanism-driven fixture replacement, recorded before
  execution, not a bar weakened after results.
- F-M6-3b (setup_flip3) is PRESERVED, not superseded: slot7's
  decmerit is 39 >= 25, so the fixture still constructs the fresh
  merit :1 path, and its section must be byte-identical.
- setup_xm51, setup_flip, setup_flip2, and all stream fixtures remain
  in source (unfrozen lineage); their asserted bars are unchanged.

## 6. Honest remaining boundaries

- The binary protection edge remains, now at decmerit=25 instead of
  winuses=2: a recency pair of weights 12+12=24 does not protect
  while 12+13=25 does. What R6 removes is the window-edge step and
  the in-window count cliff; what remains is a knife-edge in
  recency-mass, now with an auditable continuous score (decmerit)
  beneath it. A future red team should probe the 24-vs-25 margin.
- Replay harm stays count-based (frozen scope decision, section 3).
  A future hypothesis may unify the weighting; until then the merit
  and harm accountings differ in shape (decayed vs count) over the
  same window.
- MTHRESH=25 is calibrated for win=20, the only window at which
  protection decisions occur in this suite. Linear (not exponential)
  decay and the threshold value are authored. Not L3.
- Classification: bounded L2 mechanism refinement. No mechanism here
  establishes L3.

## 7. Execution and governance rules

- Pure Zag only: no Python anywhere (editing, generators, verifiers,
  analysis, harnesses, scratch). Disclosure does not cure a violation.
- This prereg is committed alone BEFORE any H-MEM7 implementation
  exists in the repo. The prereg commit must be a strict ancestor of
  the implementation commit.
- Verdict names the exact frozen bars above. No bar may be weakened
  or redefined after results.
- Commits are local (tnn-native-lab branch); nothing is pushed without
  Micah's explicit approval. Commit only explicitly owned paths; never
  broad-stage concurrent workers' files. On .git/index.lock, wait for
  the live lock; never remove it.
- Never commit binaries, caches, or unnecessary generated artifacts.
- Negative evidence and lineage are preserved; invalid claims are
  marked RETRACTED, SUPERSEDED, INVALID, or VOID.
- Classification remains bounded L2, not L3. No mechanism here
  establishes L3.

## 8. Hand-derivation record (pre-freeze)

All expectations in section 4 were hand-derived from the frozen
mechanism in section 3 before any implementation existed in the repo.
Pre-freeze work additionally included scratch validation in /tmp
(Zag compiler + shell diff/cmp only, no Python), which confirmed the
hand derivations; the committed implementation is byte-identical to
the scratch-validated source. The full derivations are reproduced in
MEM7_RESULT.md with the raw outputs they are checked against.
