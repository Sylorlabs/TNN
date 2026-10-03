# PREREG: RANK-CHEAP (cheaper ranking-maintenance primitives)

Frozen 2026-10-03 12:05 UTC. Worker: RANK-CHEAP (non-ledger task;
claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_cheap/

## Question

COLD-RANKING (VERDICT=PASS 7/7) priced EAGER per-hit ranking and
found it a net loss: every cold hit pays O(position) to move while
the scan saving is bounded by the same position (NET 2034/1380 vs
FIFO 1132). This lane prices CHEAPER maintenance primitives:

- rk=3 SWAP-WITH-FRONT (eager, O(1)/hit): on every cold hit at
  slot s>0, swap the hit entry with slot 0 (one physical slot
  exchange). No shifting of the stack.
- rk=4 PERIODIC-SWAP (lazy, every 8th hit): the same primitive,
  applied only when a per-row hit counter reaches 8 (then reset).

Headline question: does O(1) maintenance make ranking a net win
(NET < 1132)? Tradeoff: less precise ordering vs cheaper
maintenance.

## Frozen design (additive on COLD-RANKING; no redesign)

Substrate: cold_rank.zag copied verbatim. Additive new code only:

1. Header offset 72: hits_since_rank (u32; zeroed by mem_zero at
   each row start, since mem_zero clears the whole 4096-byte
   arena).
2. `swap_front(M,s)`: if s<1 return 0; else cslot_swap(M,s,0),
   rank_cost += 1, rank_moves += 1; return 0 (the entry's new
   slot). The rc byte travels with the entry via cslot_swap, as in
   COLD-RANKING.
3. `periodic_swap(M,s)`: hsr = header72 + 1; header72 = hsr; if
   hsr < 8 return s (no move, entry stays); header72 = 0; if s<1
   return 0; else cslot_swap(M,s,0), rank_cost += 1,
   rank_moves += 1; return 0.
4. cold_lookup: after the rc increment and before the promotion
   check (same move-then-promote placement as COLD-RANKING),
   `if(rk==3){ns=swap_front(M,s);}` and
   `if(rk==4){ns=periodic_swap(M,s);}`. rk==1/2 paths carried over
   unchanged.
5. main: three rows on the M2C2 scenario (pol=6, mode=1, w=21,
   c2w=10, pm=1): rk=0 (anchor), rk=3, rk=4. Row layout unchanged
   (144 bytes; offsets 128 rkT, 132 rkmT, 136 rk). Tags
   COND=RC-M2C2-RK0/RK3/RK4.

Pricing assumption (frozen): rank_cost counts ONE unit per
physical slot exchange, i.e. the honest price of the O(1)
primitive, at the same slot-position granularity as the cold scan
cost. It does NOT charge the s positions the entry "travels".
rank_moves counts cold hits that advanced the entry >=1 slot (a
swap from s>=1 to slot 0 qualifies).

Why N=8: 56 total cold hits per row are frozen by D1/D2 below;
56/8 = 7 gives exactly 7 rank events per row, small enough to
show the laziness tradeoff sharply against 56 eager events.

## Frozen derivations

- D1 OUTCOME INVARIANCE. Ranking changes only cold slot
  positions. The rc byte travels with its entry (cslot_swap).
  Promotion triggers on rc>=2 for the same entries on the same
  hits (promote_slot moves by content from the post-move slot).
  promote_slot's target selection never consults the cold tier,
  and rank code never touches the pool tier. Hence hot-tier
  hit/miss sequences, cold hit sequences, and all outcome fields
  are identical across rk in {0,3,4}: pre=35, post=0, bacc=20,
  raw=15, cf=80, ev=48, drop=0, exile=76, cdrop=0, r1=r2=r3=35,
  rec1=40, prm1=20, rec2=rec3=0, prm2=prm3=0, postH=35, recT=56,
  prmT=28, r4=35, rec4=16, prm4=8, postH2=35.
- D2 HIT COUNT. Total cold hits per row = recT = 56 (frozen by
  D1). R1 contributes 40, R4 contributes 16, R2/R3 contribute 0.
- D3 RK=3 MAINTENANCE BOUND. Each of the 56 cold hits pays 0
  (s=0) or 1 (s>0) rank cost. Therefore rkT3 <= 56 and
  rkmT3 <= 56. In particular rkT3 < 553 = rkT(rk2),
  COLD-RANKING's importance-bubble maintenance (frozen there):
  swap-with-front is strictly cheaper to maintain than the
  cheapest eager mode priced so far.
- D4 RK=4 EVENT COUNT. hsr reaches 8 exactly at global cold hits
  8,16,24,32,40,48,56 (56 total hits frozen by D2) and resets to
  0 each time: exactly 7 rank events per row, each paying <=1.
  Therefore rkT4 <= 7 and rkmT4 <= 7, hence rkT4 < 553.
- D5 ANCHOR. The rk=0 path is behavior-identical to
  cold_rank.zag's rk=0: the new rk==3/rk==4 branches are no-ops,
  swap_front/periodic_swap are never called, header 72 is never
  touched. Therefore the rk=0 row reproduces EXILE-PROMOTION's
  PXP-M2C2 row bit-for-bit: cc1=420, ccT=1132, cc4=712, rkT=0,
  rkmT=0, and every K1 field below.
- D6 NET-WIN HYPOTHESIS. NET3 = ccT3 + rkT3 with rkT3 <= 56.
  Swap-with-front gives each touched entry MTF-class front
  placement (the entry ends at slot 0 after its first touch, as
  with move-to-front; repeated touches are then free), so its
  scan cost is expected in the MTF ballpark (ccT=1045) or better
  while maintenance collapses from 989 to <=56. Frozen
  prediction: NET3 < 1132 (cheaper maintenance makes ranking a
  net win). Margin 1132 - NET3 is reported as the size of the win.
- D7 TRADEOFF HYPOTHESIS. Periodic swap applies the identical
  primitive 8x less often, so its ordering is coarser: frozen
  prediction ccT3 <= ccT4 (eager ordering at least as good as
  lazy). The report will quote the empirical exchange rate:
  scan points lost per maintenance point saved between rk=3 and
  rk=4.

What this lane does NOT test: importance signals beyond
current-residency rc; ranking under cold overflow; other
policies, doses, or pm values; sealed post-freeze worlds; other
lazy schedules (threshold-crossed re-rank, full periodic
re-sort).

## Frozen kill bars (K1..K6 in-binary, K7 external)

Row offsets: rk=0 at ro=0, rk=3 at ro=144, rk=4 at ro=288.

- K1 ANCHOR-RK0: rk=0 row == EXILE-PROMOTION PXP-M2C2 exactly:
  pre=35, post=0, bacc=20, raw=15, cf=80, ev=48, drop=0,
  exile=76, cdrop=0, r1=35, rec1=40, cc1=420, prm1=20, r2=35,
  rec2=0, cc2=0, prm2=0, r3=35, rec3=0, cc3=0, prm3=0,
  postH=35, recT=56, ccT=1132, prmT=28, r4=35, rec4=16,
  cc4=712, prm4=8, postH2=35, cfT=80, evT=48, rkT=0,
  rkmT=0, rk=0. Any drift is FAIL.
- K2 O1-MAINTENANCE: rkT3 <= 56, rkmT3 <= 56, rkT3 < 553;
  rkT4 <= 7, rkmT4 <= 7, rkT4 < 553. (Both new primitives are
  strictly cheaper to maintain than importance-bubble's 553.)
- K3 NET-WIN: NET3 = ccT3 + rkT3 < 1132. (Does O(1)
  maintenance make ranking a net win?)
- K4 TRADEOFF: ccT3 <= ccT4. (Eager ordering at least as good
  as 1-in-8 lazy ordering.)
- K5 INVARIANCE: for ro in {0,144,288}: rec1=40, prm1=20;
  rec2=rec3=0, prm2=prm3=0; rec4=16, prm4=8; recT=56, prmT=28;
  postH=postH2=35; r1=r2=r3=35; pre=35, post=0; bacc=20,
  raw=15, cf=80; exile=76, ev=48; drop=0, cdrop=0.
- K6 LEDGER: for ro in {0,144,288}:
  exile == ev + drop + promote; cdrop == 0.
- K7 DETERMINISM: 3/3 runs byte-identical (sha256 equal),
  checked externally.

VERDICT=PASS iff K1..K6 pass in-binary and K7 passes externally.
Bars are never weakened or reinterpreted after results; the dated
erratum process (derivation errors only) is the sole correction
path.
