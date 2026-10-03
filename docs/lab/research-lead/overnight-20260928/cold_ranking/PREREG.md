# PREREG: COLD-RANKING (LRU/importance ranking within cold)

Date: 2026-10-03. Worker: COLD-RANKING (non-ledger task; claim
minting paused). Lane:
`docs/lab/research-lead/overnight-20260928/cold_ranking/`.

## Motivation (from EXILE-PROMOTION's honest finding)

EXILE-PROMOTION reached VERDICT=PASS 7/7 with one honest finding:
reheat cost is POSITIONAL. In PXP-M2C2, R4's 8 re-exiled entries
sat at cold slots 40..47, so reheating them cost cc4=712, above a
no-promo single pass (575). The report names the follow-up
explicitly: LRU/importance ranking *within* cold. This lane is that
follow-up, built additively on EXILE-PROMOTION (substrate +
promotion machinery carried over unchanged; no redesign).

## Frozen design

Cold tier lookup is currently FIFO by slot position; scan cost per
hit = position+1. Two rank modes are added, selected by frozen
parameter rk threaded through mem_read_recov / test_A_recov /
cold_lookup:

- rk=0: no ranking. cold_lookup behaves exactly as in
  EXILE-PROMOTION (the anchor; K1 requires bit-for-bit equality
  with the published PXP-M2C2 row).
- rk=1 (recency / move-to-front): on every cold hit, after the
  recovery-count increment and before the promotion check, the hit
  entry is moved to cold slot 0; slots [0,s-1] shift right by one.
  rank_cost += s (slot-positions advanced); rank_moves += 1 iff
  s > 0.
- rk=2 (importance / bubble by recovery count): on every cold hit,
  after the recovery-count increment and before the promotion
  check, the hit entry bubbles left while rc(s) > rc(s-1)
  (strictly greater; ties do not move). rank_cost += positions
  advanced; rank_moves += 1 iff advanced > 0.

Uniform rules (frozen):

1. Rank repositioning happens on EVERY cold hit (move-then-promote
   order): the promotion check at T=2 runs after the move. Work
   spent moving an entry that is then promoted counts as honest
   overhead.
2. The recovery-count byte moves WITH its slot. Slot moves relocate
   the 20-byte cold entry and its rc byte together; the signal never
   detaches from its entry.
3. Cost units: rank_cost counts slot-positions advanced, the same
   granularity as cold_cost's slots-examined. NET = ccT + rkT is the
   honest total for "does maintenance offset the savings".
4. exile-seq (co+16) stays per-entry and moves with the slot; cold
   overflow eviction (min exile-seq) is position-independent and
   unchanged. (Cold never fills in these conditions: occupancy 28 <
   64, cdrop=0 throughout.)
5. New header offsets: 64 rank_cost, 68 rank_moves. All other
   offsets identical to EXILE-PROMOTION.

Conditions (frozen): the M2C2 scenario only (pol=6, mode=1, w=21,
c2w=10: teach, churn, three recovery passes, second churn, R4),
run once per rk in {0,1,2}. pm=1 throughout (promotion machinery
from EXILE-PROMOTION, threshold T=2).

## Erratum E1 (2026-10-03, post first-run; derivation error, no
mechanism change)

The frozen R4 derivation forgot within-pass self-interference. In
R4's owner-1 pass the 8 hits each reposition their entry, pushing
previously-moved entries right, so the entries end STACKED at slots
0..7 rather than each sitting at slot 0 for the owner-2 pass:

- rk=1 (MTF): owner-1 stacks them in REVERSE hit order; owner-2
  hits each land at slot 7 (cc 8, rk 7 per hit): owner-2 cc=64,
  rk=56, 8 advancing moves.
- rk=2 (bubble): the strict-> tie rule STOPS each entry behind
  equal-rc predecessors (h_j halts at slot j-1); owner-1 rk is
  S-28 not S. Owner-2 hits land at slots 0..7 in hit order: cc=36,
  rk=28, 7 advancing moves.

With S = 348+N the summed owner-1 hit positions (N in [0,28] as
before), corrected R4: cc4(rk1) = 420+N in [420,448];
cc4(rk2) = 392+N in [392,420]; hence cc4(rk1) - cc4(rk2) = 28
EXACTLY (same N); rk4(rk1) = 404+N in [404,432];
rk4(rk2) = 348+N in [348,376]; rkm4 = 16 / 15. Corrected totals:
rk=1: ccT = 1030+N (<=1058), rkT = 974+N in [974,1002],
rkmT = 55, NET = 2004+2N; rk=2: ccT = 812+N (<=840),
rkT = 538+N in [538,566], rkmT = 34, NET = 1350+2N. The
implementation is unchanged; only this derivation and the
affected bars (K2's cc4-equality replaced by the +28 gap plus
bounds, K3's rkT(rk1) bounds, K6's move counts) are amended. The
first run stays exploratory; the verdict rests on the clean
re-freeze (amended assertions, rebuilt binary, three fresh runs).

## Frozen derivations (M2C2)

Assumption A1 (stated, falsifiable): the 20 owner-1 A keys sit at
cold slots 0..19 in test order (i=1..10, hop 1 then hop 2).
EXILE-PROMOTION's cc1=420 = 2x210 is consistent with this; the run
below tests it. If A1 is wrong, the R1 rk=1 numbers below are
wrong and the erratum process applies.

R1: cold holds 28 entries at slots 0..27; the 20 A keys at slots
0..19 (A1). Each A key is hit twice: owner-1 check (rc 0->1, stays
cold), owner-2 check (rc 1->2, promotes). Owner-4/8 checks are hot.

- rk=1: owner-1 pass hits slots 0..19 in order: cc 210, rank cost
  0+1+...+19 = 190, 19 advancing moves; entries end reversed
  [K_20..K_1]. owner-2 pass: each hit finds its key at slot 19
  (the previous promotion's victim refills slot 0): cc 20x20 =
  400, rank cost 20x19 = 380, 20 moves; 20 promotions.
  R1: cc1=610, rk1=570, rkm1=39.
  NOTE: MTF INFLATES the promotion-pass scan (610 > 420): the
  rank move fights the promotion's slot-0 refill.
- rk=2: owner-1 pass: every hit sets rc=1; all predecessors rc=1,
  strict > fails, zero moves; cc 210, rk 0. owner-2 pass: rc->2,
  each entry bubbles past only the rc=0 pool victims ahead of it
  (predecessors are exactly the victims under A1):
  0+1+...+19 = 190, 19 moves; cc 210. R1: cc1=420, rk1=190,
  rkm1=19.
- Post-R1 cold layout is IDENTICAL for rk=0,1,2 (slots 0..19 = 20
  exiled pool victims in promotion order; slots 20..27 = 8
  never-hit entries), because every moved A entry is promoted out
  in the same pass in the same key order and victims always land
  at first-free slots.

R2/R3: no cold hits (rec=0 in EXILE-PROMOTION); no moves; layout
unchanged. Second churn: no cold hits; 28 exiles install at slots
28..55; the 8 re-exiled A entries land at slots 40..47 (E1
derivation, unaffected by rk since no cold hits occurred).

R4: the 8 A entries sit at cold slots 40..47 (E1 of
EXILE-PROMOTION, unaffected by rk: no cold hits occur between R1
and R4, and churn2's exile order is rk-independent). They are hit
in test order in owner-1 (rc 0->1, reposition), owner-2 (rc 1->2,
promote), owner-4/8 hot. The owner-1 repositionings stack the
entries at slots 0..7 (see erratum E1):

- rk=1: owner-1 MTFs stack reverse hit order; owner-2 hits each at
  slot 7. cc4 = 420+N, rk4 = 404+N, rkm4 = 16.
- rk=2: owner-1 bubbles halt at ties (slots 0..7 in hit order);
  owner-2 hits at slots 0..7. cc4 = 392+N, rk4 = 348+N, rkm4 = 15.
- N = non-inversion pairs between hit order and slot order,
  0 <= N <= 28 (bounded only); the SAME N governs both modes, so
  cc4(rk1) - cc4(rk2) = 28 exactly.

Totals (predicted; corrected per E1):

- rk=0: ccT=1132, rkT=0, NET=1132 (EXILE-PROMOTION's row).
- rk=1: ccT = 610 + 420 + N = 1030 + N (<= 1058 < 1132: total scan
  still reduced, but R1 scan is INFLATED 420 -> 610);
  rkT = 570 + 404 + N = 974 + N (in [974, 1002]);
  NET = 2004 + 2N >= 2004 > 1132.
- rk=2: ccT = 420 + 392 + N = 812 + N (<= 840 < 1132);
  rkT = 190 + 348 + N = 538 + N (in [538, 566]);
  NET = 1350 + 2N >= 1350 > 1132.
- rkmT: rk=1: 39 + 16 = 55; rk=2: 19 + 15 = 34; rk=0: 0.

Predicted headline: ranking DOES reduce the R4 positional scan
cost (cc4 712 -> 420+N / 392+N), but maintenance cost more than
offsets it: NET never beats FIFO (2004+ / 1350+ vs 1132). Pure
recency (rk=1) additionally INFLATES the R1 promotion-pass scan
(420 -> 610) because move-to-front fights the promotion's slot-0
refill, and its reverse-stacking costs an exact +28 vs tie-stacking
in R4. Importance (rk=2) moves entries only on evidence (rc
strictly exceeding the predecessor) and leaves R1 scan at 420.
Order-independent lower bounds (sanity): cc1(rk=1) >= 420,
rk1(rk=1) >= 380.

## Frozen kill bars

Row layout (144 bytes): 0 pre, 4 post, 8 bacc, 12 raw, 16 cf,
20 ev, 24 drop, 28 exile, 32 cdrop, 36 postR1, 40 rec1, 44 cc1,
48 prm1, 52 postR2, 56 rec2, 60 cc2, 64 prm2, 68 postR3, 72 rec3,
76 cc3, 80 prm3, 84 postH, 88 recT, 92 ccT, 96 prmT, 100 postR4,
104 rec4, 108 cc4, 112 prm4, 116 postH2, 120 cfT, 124 evT,
128 rkT, 132 rkmT, 136 rk, 140 spare.

- K1 ANCHOR-RK0: the rk=0 row equals EXILE-PROMOTION's published
  PXP-M2C2 row exactly: pre=35, post=0, bacc=20, raw=15, cf=80,
  ev=48, drop=0, exile=76, cdrop=0; R1 35/40/420/20; R2 and R3
  35/0/0/0; postH=35; recT=56; ccT=1132; prmT=28;
  R4 35/16/712/8; postH2=35; cfT=80; evT=48; and rkT=0, rkmT=0.
  Any drift means the substrate was not carried over unchanged:
  FAIL.
- K2 SCAN-SAVINGS: cc4(rk=1) < 712 and cc4(rk=2) < 712;
  cc4(rk=1) == cc4(rk=2) + 28 (MTF reverse-stacking vs bubble
  tie-stacking; same N, exact gap per E1); 420 <= cc4(rk=1) <= 448;
  392 <= cc4(rk=2) <= 420; ccT(rk=1) < 1132 and ccT(rk=2) < 1132;
  cc1(rk=1) == 610 (MTF inflates the promotion-pass scan vs FIFO's
  420: the rank move fights the promotion's slot-0 refill);
  cc1(rk=2) == 420 (importance ranking leaves R1 scan unchanged).
  If ranking does not reduce the R4 positional scan cost, its
  stated purpose fails: FAIL.
- K3 OFFSET (the honest bar): NET(rk=1) = ccT+rkT > 1132 and
  NET(rk=2) > 1132 (maintenance more than offsets the savings;
  ranking is not a net win); rkT(rk=1) > rkT(rk=2) > 0 (importance
  cheaper to maintain than pure recency); 974 <= rkT(rk=1) <= 1002;
  538 <= rkT(rk=2) <= 566. If either NET beats FIFO, the prereg's
  honest prediction is falsified (report as FAIL of the prediction,
  with the measured numbers).
- K4 INVARIANCE: identical across rk=0,1,2: rec1=40, prm1=20,
  rec2=rec3=0, prm2=prm3=0, rec4=16, prm4=8, recT=56, prmT=28,
  postR1=postR2=postR3=35, postH=35, postH2=35, exile=76, ev=48,
  drop=0, cdrop=0, pre=35, post=0. Ranking must change costs only,
  never outcomes: FAIL on any difference.
- K5 LEDGER: exile == ev + drop + promote for rk=0,1,2;
  cdrop=0 in all three rows. (Ranking must not disturb the priced
  accounting.)
- K6 RANK-ACCOUNTING: rkmT(rk=1)==55, rkmT(rk=2)==34,
  rkmT(rk=0)==0. (Exact move counts from the corrected derivation:
  rk=1: 19+20 R1, 8+8 R4; rk=2: 0+19 R1, 8+7 R4.)
- K7 DETERMINISM: 3/3 byte-identical runs (external sha256
  comparison). VOID-grade.

Verdict rule: PASS requires K1..K7 all PASS. A FAIL on K3's
inequality direction (NET beating FIFO) is reported as a failed
prediction with measured numbers, not re-derived.

## What this does NOT test

- Importance signals beyond current-residency rc (a lifetime
  counter would need key-keyed state, new machinery beyond the
  additive brief; the rc-reset-on-install that promotion needs
  destroys cross-residency importance, which is itself a finding).
- Ranking under cold overflow (cold never fills here; cdrop=0).
- Rank modes interacting with pm=0 or other policies/doses.
- Whether a cheaper maintenance primitive (swap-with-front,
  lazy ranking) changes the NET comparison.
- Sealed post-freeze worlds.

## Toolchain and hygiene

- Pure Zag; safebin mandatory (PATH=$HOME/safebin); `command -v
  python3` verified empty before build and before runs; znc pinned
  2026.07.0-dev, cmp-verified against
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the prereg
  commit.
- grep audit on new code: no `while.*!(` negated conjunctions, no
  _zag_print, no `as *i32` slice construction, single approved
  `as *u8` in z_alloc (carried over), if-nesting at most 3.
- Commits local only, never pushed, explicit pathspecs, no reset.
  Prereg committed alone first (strict commit order).
