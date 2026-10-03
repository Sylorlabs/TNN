# PREREG: RANK-LAZY (frozen lazy-ranking replication and threshold variant)

Date: 2026-10-03. Worker: RANK-LAZY (non-ledger task; claim
minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_lazy/.
Frozen: this file is committed alone before any implementation.
No errata; no post-result bar changes.

## Background

RANK-CHEAP (VERDICT=FAIL 5/7) found, exploratory only: the lazy
periodic-swap primitive (rk=4, rank every 8th cold hit) achieved
NET4 = ccT4 + rkT4 = 1091 + 6 = 1097 < 1132, a net win of 35 over
FIFO at maintenance cost 6, with the O(1) maintenance bounds held
exactly. Because K3 covered NET3 only, the NET4 win was not
preregistered and stays exploratory. This lane freezes it.

## Frozen design

Additive on RANK-CHEAP's rank_cheap.zag (carried over unchanged
except the additions below):

1. M buffer 4096 -> 4160 bytes. New ranked-flag side table at
   offset 4096: 64 x u8, one flag per cold slot ("ranked this
   residency"). Zeroed by mem_zero (zero loop extended to 4160).
   Cleared on promote_slot and on every exile_victim install,
   alongside the existing rc reset (rset).
2. thresh_rerank (rk=5, threshold-crossed re-rank): on a cold hit,
   after the rc increment and before the promotion check
   (move-then-promote placement, promote_slot uses the post-move
   slot): if rc >= T_rank (frozen T_rank = 2) and the entry's
   ranked flag is clear, perform ONE swap-with-front
   (cslot_swap(M,s,0); honest cost rank_cost += 1 and
   rank_moves += 1 iff s > 0; no-op and no cost at s = 0), set
   the ranked flag for the ranked entry (slot 0 after the move;
   the displaced entry's flag is cleared), return the post-move
   slot. Fires at most once per entry per residency. This is
   importance-triggered (the entry's own recovery count crossing
   the frozen threshold), not schedule-triggered.
3. cold_lookup: new `if(rk==5){ns=thresh_rerank(M,s);}` branch
   after the rk==4 branch. All other substrate behavior
   (hot path, exile, FIFO cold overflow, promotion at T=2,
   pm-gating, rk=0/1/2/3/4 logic) unchanged.
4. Row layout unchanged (144 bytes/row). 11 rows per run.

On seeds: the substrate contains no RNG; every run is
deterministic given the churn program. "Different seeds" is
realized honestly as different churn patterns (mode/dose
variation below), not synthetic randomness.

## Frozen runs (all pol=6, pm=1; R1/R2/R3 recovery passes + c2w
second churn + R4, as in RANK-CHEAP run_promo)

- M2C2 (mode=1, w=21, c2w=10): rk=0 (anchor), rk=4 (headline
  replication), rk=5 (threshold variant).
- V1 heavier churn (mode=1, w=40, c2w=10): rk=0, rk=4.
- V2 extra churner (mode=2, w=21, c2w=10): rk=0, rk=4.
- V3 no-owner-16 churn (mode=3, w=21, c2w=10): rk=0, rk=4.
- V4 single-owner churn (mode=0, w=21, c2w=10): rk=0, rk=4.

Row order: 0 M2C2-rk0, 1 M2C2-rk4, 2 M2C2-rk5,
3 V1-rk0, 4 V1-rk4, 5 V2-rk0, 6 V2-rk4,
7 V3-rk0, 8 V3-rk4, 9 V4-rk0, 10 V4-rk4.

## Frozen derivations and kill bars

- D1 (K1 HEADLINE-NET4): NET4 = ccT4 + rkT4 < 1132 on M2C2.
  Replication target from RANK-CHEAP's exploratory row is
  ccT4=1091, rkT4=6, NET4=1097; the frozen bar is the inequality,
  not the point value. The rk=0 M2C2 row must also reproduce
  EXILE-PROMOTION's PXP-M2C2 row bit-for-bit (cc4=712,
  ccT=1132, rkT=0, rec1=40, prm1=20, rec4=16, prm4=8, recT=56,
  prmT=28, exile=76, ev=48, postH=postH2=35, pre=35, post=0,
  bacc=20, rawA=15), proving the substrate carried over
  unchanged. PASS requires both the anchor and NET4 < 1132.
- D2 (K2 ROBUST-SEED): the lazy win generalizes across churn
  patterns. For each variant V1..V4, NET4 < NET0 using that
  world's own FIFO row as baseline. PASS requires >= 3 of 4
  variants. A pattern-specific fluke fails this bar.
- D3 (K3 THRESHOLD-VARIANT): NET5 = ccT5 + rkT5 < 1132 on M2C2.
  Importance-triggered re-rank must also net a win vs FIFO.
  (Genuine unknown: rank-then-promote disturbs the layout while
  the ranked entry leaves cold, so this may fail; failure is
  informative, not mechanical.)
- D4 (K4 O1-MAINTENANCE, M2C2 rows): rkT4 <= 7 and rkmT4 <= 7
  (carried from RANK-CHEAP D4: 56 cold hits, every-8th event,
  at most 7 paying); rkT5 <= recT and rkmT5 <= recT (a paying
  rank event needs a distinct cold hit; the flag fires at most
  once per residency); rkT4 < 553 and rkT5 < 553 (both strictly
  cheaper than importance-bubble's 553).
- D5 (K5 INVARIANCE): ranking changes costs only, never
  outcomes. Within each world (M2C2 across rk=0/4/5; each
  variant across rk=0/4), all outcome offsets must be equal:
  0,4,8,12,16,20,24,28,32 (pre/post/bacc/raw/cf/ev/drop/
  exile/cdrop), 36,40,48,52,56,64,68,72,80 (R1..R3 postR/rec/
  prm), 84,88,96 (postH/recT/prmT), 100,104,112,116 (R4),
  120,124 (cfT/evT). Scan-cost offsets (44,60,76,92,108),
  rank offsets (128,132,136) are allowed to differ.
- D6 (K6 LEDGER): for all 11 rows, exile == ev + drop +
  promote, and cdrop == 0.
- D7 (K7 DETERMINISM): 3/3 runs byte-identical (external
  sha256 comparison).

## Verdict rule

VERDICT=PASS iff K1..K7 all PASS. Any other combination is
VERDICT=FAIL (n/7). The bars above are frozen; no weakening,
no post-result changes. An informative K3 failure (threshold
variant not a net win) still yields FAIL overall under the
frozen rule and is reported as such.
