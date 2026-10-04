# PREREG: H-MEM5 Independent Red Team (Adversary)

**Date:** 2026-09-29
**Status:** FROZEN (committed alone before any adversary implementation or execution)
**Target:** `mem5_learn.zag` at the H-MEM5 result commit (H-MEM5 SURVIVES 4/4).
**Stance:** The repair claim is assumed false. Four attacks, each with an
explicit frozen verdict rule. All fixture arithmetic below is hand-derived
from the committed `mem5_learn.zag` source (read-only) before this freeze.

## Background

H-MEM5 (R4) rewrote `elig()`: within the age window (`st_seq < st_prot`)
a slot is protected iff `st_uses >= MERITK (2)`; the `GRACE=3` absolute
protection is removed. The builder's verdict: "the grace-window harm and
the fig-leaf merit harm are closed at the mechanism level on their exact
frozen fixtures." Disclosed residuals: (a) stale merit (uses>=2 from
ancient queries remains protected; no recency weighting; H-MEM6
material); (b) a newcomer is evictable until it earns 2 queries.

The builder's rationale for k=2 (PREREG_MEM5.md): "a single query is not
evidence of merit (probe, misroute, noise); two queries are the smallest
substantive signal."

## Attack X-M5-1: stale-merit harm (primary downgrade vector)

**Idea.** The merit gate counts ALL-TIME uses (`st_uses` is cumulative,
never reset, never decayed); the eviction decision is WINDOW-scoped
(`replay_cost` over the last 20 queries). A slot with uses=2 whose two
queries are ancient and outside the operating window is "meritorious"
(all-time) but costless to evict (window cost 0). Protecting it can only
increase cost. This is the X-M4-2a harm pattern (protected sacrifices a
queried proc at cost 2 while unprotected evicts the window-absent
newcomer at cost 0) recurring behind uses=2 stale merit instead of
uses=0 grace or uses=1 fig-leaf.

**Frozen fixture.** seq=105, nq=26, ev=0, win=20.
Slots 0..6: pid=i, uses={10,20,30,40,50,60,70}, lastq={91,92,93,94,95,96,97},
sseq={0,1,2,3,4,5,6}, prot=50 (expired: 105 >= 50).
Slot7: pid=7, uses=2, lastq=101, sseq=7, prot=109 (learned at seq 99;
its 2 queries at seq 100,101 are ancient; 105 < 109 so the window is open).
Q (26): Q[0]=7, Q[1]=7 (the 2 ancient merit queries), Q[2]=0, Q[3]=1,
Q[4]=2, Q[5]=3 (advance queries, outside the operating window),
Q[6..11]=0 (6x), Q[12..14]=1 (3x), Q[15..17]=2 (3x), Q[18..19]=3 (2x),
Q[20..21]=4 (2x), Q[22..23]=5 (2x), Q[24..25]=6 (2x).
Operating window = Q[6..25] (lo = 26-20 = 6): proc7 absent, cost 0.

**Hand-derived expectations.**
Protected (use_prot=1): slot7 is protected (105 < 109 and 2 >= 2);
eligible = slots 0..6 (ne=7).
- LFU -> slot0 (uses=10 min), cost 6. LRU -> slot0 (lastq=91 min), cost 6.
- FIFO -> slot0 (sseq=0 min), cost 6. LIFO -> slot6 (sseq=6 max), cost 2.
- RANDOM: ev=0, ne=7, k=(0*5+1)%7=1 -> second eligible slot -> slot1, cost 3.
- argmin: LIFO=2 wins outright. wprot=LIFO (3), vprot=slot6, cprot=2.
Unprotected: LFU -> slot7 (uses=2 is the global min), cost 0.
wun=LFU (0), vun=slot7.
churn_verdict: wprot(3) != wun(0) -> returns 1, printing
"CHURN-FULL:1 (winner flips LIFO->LFU; eviction slot6(proc6)->slot7(proc7))".
The protected mechanism sacrifices proc6 (70 uses, cost 2) to shield
proc7 (2 ancient queries, window cost 0). Cost 0 -> 2.

**Frozen kill rule.** X-M5-1 SUCCEEDS (→ DOWNGRADE) iff the observed
run shows wprot=3 (LIFO), vprot=slot6, cprot=2, wun=0 (LFU), vun=slot7,
and churn_verdict=1 with "winner flips LIFO->LFU" and
"slot6(proc6)->slot7(proc7)". X-M5-1 FAILS iff wprot=0, vprot=slot7,
cprot=0, verdict 0 (the harm does not occur).

**Why this is a downgrade and not a boundary confirmation.** The builder
disclosed the mechanism fact ("uses>=2 ancient remains protected") but
did NOT disclose or demonstrate that the cost-0→2 harm recurs through
it. The H-MEM5 headline hypothesis claims the harm is "closed at the
mechanism level"; the natural reading is that the harm pattern
(protection-induced sacrifice of a queried proc for a window-absent
newcomer) is closed, not merely two fixtures. Per the X-CV4-1 precedent:
a disclosure of a mechanism fact does not convert a successful
demonstration of the harm into a non-finding. If X-M5-1 succeeds, the
narrowed claim is: the protection-induced cost harm is closed for
uses in {0,1} and for fresh uses>=2, but recurs for stale uses>=2
(all-time merit without recency). The "substantive merit" threshold is
all-time count; two ancient window-absent queries suffice to shield a
cost-0 newcomer at cost 0→2. Follow-up: H-MEM6 (recency-weighted merit),
as the builder anticipated.

## Attack X-M5-2: the one-query cliff (supporting evidence)

**Idea.** The repair's entire efficacy rests on the uses=1 vs uses=2
knife-edge. By the builder's own rationale a single query "is not
evidence of merit (probe, misroute, noise)" — yet a single marginal
query is exactly what moves a slot across the cliff from evictable to
protected. Demonstrate the discontinuity: two fixtures identical in
every respect except slot7's uses (1 vs 2).

**Frozen fixtures.** X-M5-2a: the X-M5-1 fixture with slot7 uses=1
(lastq=101, all else identical). X-M5-2b: the X-M5-1 fixture verbatim
(slot7 uses=2).

**Hand-derived expectations.**
X-M5-2a (uses=1): slot7 evictable (1 < 2); all 8 slots eligible.
LFU -> slot7 (uses=1 min), cost 0. wprot=LFU, vprot=slot7, cprot=0;
wun=LFU, vun=slot7; churn_verdict=0 ("winner stable at LFU;
eviction unchanged").
X-M5-2b (uses=2): the X-M5-1 harm (verdict 1, cost 0→2).

**Frozen kill rule.** X-M5-2 SUCCEEDS (supporting evidence for the
downgrade; not an independent verdict driver) iff X-M5-2a yields
verdict 0 with (wprot=LFU, vprot=slot7, cprot=0) AND X-M5-2b yields
verdict 1 with the X-M5-1 harm signature. This shows one query —
the very unit the builder calls non-evidence — flips the outcome from
"evict newcomer at cost 0" to "sacrifice proc6 at cost 2".

## Attack X-M5-3: newcomer churn (expected honest negative)

**Idea.** Residual (b): a newcomer is evictable until it earns 2
queries. Test whether this produces a protection-induced cost harm
against the newcomer. Note the structural fact: the newcomer (uses<=1)
is never protected, so it is eligible in both modes; a
protection-induced harm against it would require the protected mode to
evict it at higher cost than the unprotected mode evicts something
else. Because uses=1 is the global LFU minimum, both modes' LFU pick
the newcomer and agree. Expected: no divergence (honest negative),
bounding the residual to unrepresentable opportunity cost rather than
protection-induced cost harm. Also recorded: the qualitative inversion
(the mechanism evicts the fresher uses=1 newcomer while shielding the
staler uses=2 slot) as an observation, not a finding.

**Frozen fixture.** seq=105, nq=21, ev=0, win=20.
Slots 0..4: pid=i, uses={10,20,30,40,50}, lastq={91,92,93,94,95},
sseq={0,1,2,3,4}, prot=50 (expired).
Slot5: pid=5, uses=2, lastq=90, sseq=5, prot=109 (protected: 105<109, 2>=2).
Slot6: pid=6, uses=70, lastq=96, sseq=6, prot=50 (expired).
Slot7: pid=7, uses=1, lastq=104, sseq=7, prot=109 (evictable: 1<2).
Q (21): Q[0]=5 (history); Q[1..6]=0 (6x), Q[7..9]=1 (3x), Q[10..12]=2 (3x),
Q[13..14]=3 (2x), Q[15..16]=4 (2x), Q[17..18]=6 (2x), Q[19]=7 (1x),
Q[20]=5 (1x). Window = Q[1..20] (lo=1): costs 0:6, 1:3, 2:3, 3:2, 4:2,
6:2, 7:1, 5:1.

**Hand-derived expectations.**
Protected: eligible = {0,1,2,3,4,6,7} (slot5 protected).
- LFU -> slot7 (uses=1 min), cost 1. LRU -> slot0 (lastq=91 min;
  slot5's lastq=90 is excluded), cost 6. FIFO -> slot0, cost 6.
- LIFO -> slot7 (sseq=7 max), cost 1.
- RANDOM: ne=7, k=1 -> slot1, cost 3.
- argmin: LFU=1 vs LIFO=1 tie -> first-seen LFU wins.
  wprot=LFU, vprot=slot7, cprot=1.
Unprotected: LFU -> slot7 (uses=1 < 2), cost 1. wun=LFU, vun=slot7.
churn_verdict=0 ("winner stable at LFU; eviction unchanged").

**Frozen kill rule.** X-M5-3 SUCCEEDS iff the protected mode evicts the
uses=1 newcomer at cost C while the unprotected mode evicts a different
slot at cost < C (a protection-induced harm against the newcomer).
Expected outcome per the derivation: FAILS (verdict 0, no divergence;
honest negative).

## Attack X-M5-4: regression (expected no finding)

Rebuild `mem5_learn.zag` from the committed source blob
(`git show HEAD:...`, cmp-verified identical to the worktree file),
compile with the pinned `znc`, run 3x. SUCCEEDS (red-team finding) iff
the stdout md5 differs from the frozen `2888f9331dae55f802055ec65e9101fb`
or any bar fails / any FAIL line appears. Expected: FAILS (byte-identical,
ALL BARS PASS, 0 FAIL lines).

## Verdict rule

- If X-M5-1 SUCCEEDS: **H-MEM5 DOWNGRADED (not killed).** The frozen
  K-M5-1..K-M5-4 bars still pass (they are fixture-scoped and are not
  re-litigated); the downgrade narrows the interpretive claim as in
  "Why this is a downgrade" above. X-M5-2 then stands as supporting
  evidence; X-M5-3/X-M5-4 report as executed.
- If X-M5-1 FAILS: **H-MEM5 SURVIVES this red team** (all attacks
  reported as executed).

## Controls

- Harness = lines 1..498 of the committed `mem5_learn.zag`
  (mechanism region through `learn_stream`; cmp-verified byte-identical
  against `git show HEAD:...`) + attack-only `main` and fixture
  builders. No mechanism edits. No fixture literals inside the
  mechanism region (verified by grep for "109"/"slot7" etc. — the
  mechanism uses only accessors).
- Every attack run 3x; byte-identical via cmp; exit 0.
- Pure Zag throughout: no Python in fixtures, harness, build,
  execution, analysis, or editing (file-editing tool for edits,
  `znc` for builds, shell/coreutils for runs/diffs/hashes).
- Binaries in /tmp/mem5adv only; never committed. Only adversary-owned
  paths staged. No em dashes in loop documentation.

## Deliverables

- `mem5_adv.zag` (adversary harness)
- `MEM5_ADV_RAW_OUTPUT.txt` (authoritative raw stdout, all runs)
- `MEM5_ADV_RESULT.md` (verdict per attack, trace excerpts,
  causal interpretation, narrowed claim if downgraded)
