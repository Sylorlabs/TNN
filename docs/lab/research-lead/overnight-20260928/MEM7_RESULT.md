# MEM7_RESULT.md -- H-MEM7: decayed recency-weighted merit (builder result)

Verdict: H-MEM7 SURVIVES, 6/6 frozen kill bars. The H-MEM6 red-team's
open concern (the fixed 20-query window is a step function; the
in-window 1-vs-2 merit knife-edge is real) is addressed by the
preregistered mechanism: protection merit is now recency-weighted
(decayed), not a binary in-window count. No em dashes are used in
this file (loop documentation rule).

## 1. Lineage

- Red-team open concern: MEM6_ADV_RESULT.md (H-MEM6 red team,
  SURVIVES, prereg c52c1a60d, 54/54 checks). The red team confirmed
  the in-window 1-vs-2 knife-edge (two in-window queries shield
  slot7, one leaves it evictable; X-M6-1a harm 7, honestly reported
  as CHURN-FULL:1) and left open that merit decaying smoothly rather
  than cliffing at 2 might dominate the fixed-window step function.
- H-MEM7 prereg: PREREG_MEM7.md (md5
  98a94a6a15b8a2d55f6d37dfc6c523ad), frozen alone in commit
  3c09ddb02 BEFORE any H-MEM7 implementation existed in the repo.
- H-MEM7 implementation: mem7_learn.zag (this directory), md5
  696cfb780a991413a8c4cbfe17e85973. The prereg commit 3c09ddb02 is
  a strict ancestor of the implementation commit.
- H-MEM7 evidence: MEM7_RAW_OUTPUT.txt (this directory), md5
  79fdc6eea90c8ed9c019e6893e693bba; three consecutive runs
  byte-identical (same md5 x3), exit 0, zero FAIL lines, 27 PASS
  lines, ALL BARS PASS.
- mem6_learn.zag is untouched; the H-MEM6 evidence stands as
  committed. Baseline for regression: frozen MEM6_RAW_OUTPUT.txt,
  md5 b505e265efe2a48d78d57be85c66a6ad (verified in-repo before
  the freeze).
- Toolchain: znc 2026.07.0-dev (edition 2026), pure Zag throughout.
  No Python was used anywhere: no generators, no verifiers, no
  analysis scripts, no scratch computation. Hand derivations were
  done by reading the source; pre-freeze scratch validation used
  only the Zag compiler and shell diff/cmp/md5sum in /tmp, and the
  committed implementation is byte-identical to the scratch-validated
  source (md5 696cfb780a991413a8c4cbfe17e85973 both).

## 2. The mechanism (R6, exactly as preregistered)

New function decmerit(W,ST,Q,s,win): sum of linear recency weights
over the operating window. Weight = (position - window_start + 1):
1 for the oldest query in the window, win (20) for the newest. Max
single-query weight is 20.

New frozen constant MTHRESH() = 25, calibrated for win=20: a single
maximally fresh query (weight 20) is never merit; the lightest
protectable shape is a complementary recency pair (e.g. 12+13).

elig() is now: eviction-eligible iff stored and (not protected, or
seq >= prot, or decmerit(W,ST,Q,s,win) < MTHRESH). Within the age
window a slot is protected iff decmerit >= 25.

Two frozen properties, both used in the bars:
- Age-window lemma: any 2 queries since learning protect (weights
  >= 12 each, lightest pair 12+13 = 25). Every R5 fresh-merit shape
  is preserved by construction.
- R6-protected implies >= 2 in-window queries (one query maxes at
  weight 20 < 25), so R6 only ever removes R5 protection, never adds
  it.

Frozen scope decision: R6 changes protection merit ONLY. winuses()
is kept unchanged and replay_cost() stays count-based over the same
window. H-MEM7 attacks the merit cliff, not the harm scale.
MERITK (2) is superseded for protection decisions, retained in
source for lineage.

## 3. Bar-by-bar results (all measured, all PASS)

### K-M7-1a: fresh query pair protects (decmerit=39)

Measured: pair-fresh: decmerit(slot7)=39. Protected: LFU
victim=slot0(proc0). Unprotected: LRU victim=slot0(proc0). fresh:
wprot=LFU vprot=slot0 cprot=1 wun=LRU vun=slot0 verdict=1.
CHURN-FULL:1 (winner flips LFU->LRU; eviction
slot0(proc0)->slot0(proc0)). K-M7-1a PASS. Matches the frozen
hand-derivation exactly.

### K-M7-1b: stale-in-window pair does NOT protect (decmerit=3)

Measured: pair-stale: decmerit(slot7)=3. Protected: LRU
victim=slot0(proc0). Unprotected: LRU victim=slot0(proc0). stale:
wprot=LRU vprot=slot0 cprot=1 wun=LRU vun=slot0 verdict=0.
CHURN-FULL:0 (winner stable at LRU; eviction unchanged). K-M7-1b
PASS. Same counts as K-M7-1a (2 queries), different recency,
different protection: under R5 this pair would protect
(winuses=2) and read :1. The discriminating prediction held.

### K-M7-2: merit ramp (smooth decay, no window-edge step)

Measured ramp (k, decmerit, elig):
(0,39,0),(1,37,0),(2,35,0),(3,33,0),(4,31,0),(5,29,0),(6,27,0),
(7,25,0),(8,23,1). Merit decreases by exactly 2 per appended
filler query; protection drops exactly when decmerit < 25 (k=8),
while both proc7 queries are still inside the window. K-M7-2 PASS.
Under R5 the slot would have stayed protected until k=20: the
X-M6-3a step is now a graded ramp, as preregistered.

### K-M7-3: fresh merit protects (F-M6-3b, setup_flip3, PRESERVED)

The F-M6-3b section output is byte-identical to the frozen
MEM6_RAW_OUTPUT.txt section (verified by section diff: zero
differences). slot7's decmerit is 39 >= 25, so the fresh-merit :1
path (wprot=FIFO vprot=slot0, wun=LRU vun=slot7, cv=1) is preserved
under decayed merit. K-M7-3 PASS.

### K-M7-4: fallback under decayed merit (F-M7-3c)

Measured: FALLBACK-ALL-PROTECTED emitted; fbf=1; per-policy:
LFU victim=slot0(proc0) cost=3, LRU victim=slot0(proc0) cost=3,
FIFO victim=slot0(proc0) cost=3, LIFO victim=slot7(proc7) cost=2,
RANDOM victim=slot6(proc6) cost=2; selected: LIFO cost=2 TIE; evict
slot7 proc7 uses=2 lastq=98; stored proc8 at slot7 prot_until=110.
fbsel=LIFO(3), has_proc(8)=1. K-M7-4 PASS. The per-policy
victims/costs are unchanged from F-M6-3c by construction; only the
merit accounting changed (complementary recency pairs >= 25).

### K-M7-5: preserved bars (regression)

diff of MEM7_RAW_OUTPUT.txt against the frozen MEM6_RAW_OUTPUT.txt
yields exactly three hunks, all preregistered:
- lines 104-105: F-M6-3c section header + hand-built description
  replaced by the F-M7-3c versions;
- lines 118-119: F-M6-3c check/PASS lines replaced by the F-M7-3c
  versions;
- lines 197-221: appended K-M7-1a, K-M7-1b, K-M7-2 sections.
Every other line is byte-identical, including the F-M6-3b section,
all stream fixtures (A2/B2/C2 with band checks, sweeps, futures,
pressures), the flat fixture, K-M4-1a/K-M4-2/K-M4-3a/K-M4-3b,
K-M5-1/K-M5-2/K-M5-3a, K-M3-1, K-M2-3, K-M2-5, K-M6-1, K-M6-2.
K-M7-5 PASS. The frozen rationale holds: no slot gained protection
(R6-protected implies R5-protected), and the only
protected->evictable flip in the suite is the superseded F-M6-3c
fixture state.

### K-M7-6: determinism

Three consecutive runs byte-identical (md5
79fdc6eea90c8ed9c019e6893e693bba x3), exit 0, zero FAIL lines.
K-M7-6 PASS.

## 4. Causal interpretation

The red team's open concern was that the fixed 20-query window is a
regime choice and smooth-decay merit might dominate the cliff at 2.
R6 confirms the concern was well aimed and repairs it at the merit
level: the merit signal is now continuous in recency (the ramp in
K-M7-2), the protection decision grades stale-but-in-window queries
as non-merit (K-M7-1b) while preserving fresh-merit protection by
construction (age-window lemma; K-M7-1a, K-M7-3), and the full
preserved suite is byte-identical except the intended hunks (K-M7-5).
The repair is strictly conservative: R6 only ever removes R5
protection, so no new shielding behavior was introduced anywhere.

## 5. Honest remaining boundaries (for the H-MEM7 red team)

- The binary protection edge remains, now at decmerit=25: a recency
  pair of weights 12+12=24 does not protect while 12+13=25 does.
  The edge is now in recency-mass with an auditable continuous
  score beneath it, but it is still a knife-edge. Probe the 24-vs-25
  margin.
- Replay harm stays count-based (frozen scope decision). Merit and
  harm now differ in shape (decayed vs count) over the same window.
  A harm-weighting unification hypothesis is the obvious next step;
  attack the current split.
- MTHRESH=25 is calibrated for win=20. Linear (not exponential)
  decay and the threshold value are authored. Try to break the
  calibration: find a workload where linear decay protects the wrong
  slot.
- The X-M6-1a harm shape (shield cost-2, sacrifice cost-9) is
  narrowed but not eliminated: under R6 the shielding slot must
  have recency-mass >= 25, which bounds but does not remove
  protection-induced harm. The trace still reports it honestly via
  CHURN-FULL:1.
- Classification: bounded L2 mechanism refinement. No mechanism here
  establishes L3. The menu, the operating window, MTHRESH, and the
  linear decay weights are authored.

## 6. Governance

- Pure Zag: no Python anywhere (editing, generators, verifiers,
  analysis, harnesses, scratch). Pre-freeze scratch validation used
  only the Zag compiler and shell diff/cmp/md5sum in /tmp.
- Prereg PREREG_MEM7.md committed alone (3c09ddb02) before any
  H-MEM7 implementation existed in the repo; strict ancestry
  verified (prereg commit is a strict ancestor of the implementation
  commit).
- No frozen bar was weakened or redefined after results. One
  fixture was superseded before execution (F-M6-3c -> F-M7-3c) with
  the mechanism-driven rationale recorded in the prereg.
- No em dashes in the prereg, the source, or this result doc
  (verified by byte grep).
- No binaries committed. Commits local only; only explicitly owned
  paths staged.
