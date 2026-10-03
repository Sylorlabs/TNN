# PREREG: RANK-PATTERN (K2 pattern-sensitivity + T_rank=1 variant)

Date: 2026-10-03. Worker: RANK-PATTERN (non-ledger task; claim
minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_pattern/.
Frozen: this file is committed alone before any implementation.
No errata; no post-result bar changes.

## Background

RANK-LAZY (VERDICT=FAIL 4/7) froze the lazy periodic-swap win on
M2C2 (NET4 = 1091 + 6 = 1097 < 1132) but found it
pattern-sensitive: wins under heavier churn V1 (-31) and
extra-churner V2 (-11), reverses under no-owner-16 V3 (+9) and
single-owner V4 (+2). Its K3 showed threshold-crossed re-rank at
T_rank=2 is pure cost (NET5=1159): it fronts entries that leave
cold on the same hit, so the fronting benefit can never be
collected. The follow-up asks: (a) what about V3/V4 reverses the
win, and is there a principled way to predict when lazy ranking
wins; (b) whether a threshold variant that re-ranks BELOW the
promotion threshold (T_rank=1, fronting entries that stay
resident) can beat the schedule.

## Frozen hypotheses

- H1 (mechanism): each swap-with-front at slot s is a bet with
  payoff pay_k - s*xh_k + s*yh_k, where pay_k = 1 if s > 0 else
  0, xh_k = number of later cold hits on the fronted entry
  before it next moves or leaves cold, yh_k = the same count for
  the displaced entry. Lazy ranking wins iff the swap schedule
  systematically fronts entries with more forward cold-hit mass
  than the entries they displace. The K3 pathology
  (rank-then-promote) is the degenerate case xh_k = 0 with
  yh_k >= 0, which can never pay.
- H2 (predictor): ranking only permutes cold positions; the
  hit-key sequence and the install/promote key sequences are
  invariant across rk. Therefore the counterfactual lazy scan
  cost is computable from the FIFO (rk=0) trace alone.
  Prediction procedure for a new churn pattern: run FIFO once,
  record the cold event trace, simulate the every-8th-hit swap
  schedule on that trace, read the sign of the predicted delta.
- H3 (T_rank=1): fronting on the first cold hit of each
  residency (rc >= 1, below the promotion threshold T=2) fronts
  entries that stay resident to be re-hit, so the fronting
  benefit that T_rank=2 could never bank becomes collectible.
  Whether the extra displacement churn outweighs it is a genuine
  unknown; the kill bars decide.

## Frozen design (additive on RANK-LAZY rank_lazy.zag; no redesign)

1. Copy to rank_pattern.zag; LANE=RANK-PATTERN. M layout
   unchanged (4160 bytes). All M behavior for rk=0..5 unchanged.
2. Cold event trace (diagnostic; read-only on M, written to a
   separate TR buffer, never affects the substrate): per world,
   TR[0] = record count, TR[1] = overflow flag (0/1); records of
   3 x i32 at byte offset 16 + 12*i: (etype, key, slot).
   etype 1 = cold hit (slot recorded BEFORE any rank move),
   etype 2 = cold install (slot used, fresh or overflow),
   etype 3 = promote (entry leaves cold), etype 4 = passmark
   (slot field carries pass id 1..4 for R1..R4). Hooks:
   cold_lookup on hit; exile_victim at both install sites;
   promote_slot at both promote sites; run_promo at the start of
   each recovery pass. Frozen capacity 1536 records; on overflow
   the flag is set and the predictor is VOID (K2/K3 FAIL).
3. thresh_rerank_t(M, s, t): rk=5 calls with t=2 (carried
   behavior, no rows use it here); rk=6 calls with t=1 (frozen
   T_rank=1): on a cold hit, after the rc increment, if
   rget(M,s) >= t and the ranked flag is clear, one
   swap-with-front (honest cost 1 iff s > 0; no-op at s = 0);
   the flag follows the ranked entry (set at slot 0 after the
   move; the displaced entry's flag is cleared). Move-then-
   promote placement as in rk=5. At most one firing per hit,
   hence rkT6 <= recT6 structurally.
4. 19 rows x 144 bytes. Row order: 0 M2C2-rk0, 1 M2C2-rk4,
   2 V1-rk0, 3 V1-rk4, 4 V2-rk0, 5 V2-rk4, 6 V3-rk0, 7 V3-rk4,
   8 V4-rk0, 9 V4-rk4, 10 M2C2-rk6, 11 V1-rk6, 12 V2-rk6,
   13 V3-rk6, 14 V4-rk6, 15 V5-rk0, 16 V5-rk4, 17 V6-rk0,
   18 V6-rk4. Worlds: M2C2 (mode=1, w=21, c2w=10),
   V1 (mode=1, w=40, c2w=10), V2 (mode=2, w=21, c2w=10),
   V3 (mode=3, w=21, c2w=10), V4 (mode=0, w=21, c2w=10),
   V5 (mode=1, w=30, c2w=10), V6 (mode=3, w=40, c2w=10).
   All pol=6, pm=1. NET = ccT + rkT with ccT at row offset 92
   and rkT at row offset 128.
5. In-binary predictor (main, after all rows; operates on TR
   buffers and R rows only, never touches M). For each base
   world W in {M2C2, V1, V2, V3, V4} with rk0 trace A and rk4
   trace B:
   a. Hit-key sequences of A and B must be identical
      (else predictor VOID).
   b. Layout validation: replay A maintaining slotkey[64] and
      keyslot[4096]; on install/promote update the maps; on
      every hit assert keyslot[key] equals the recorded slot
      (proves event logging complete and faithful).
   c. Simulation: replay A's events with the periodic swap
      applied on every 8th cold hit; charge sim slot + 1 per
      hit; pay 1 per swap with s > 0; maintain per-swap
      attribution counters (xh for the fronted key, yh for the
      displaced key), each closed when its key next moves
      (swap), is promoted, or is installed over.
   d. predicted_delta = sum over swaps of
      (pay - s*xh + s*yh); measured_delta =
      (ccT4 - ccT0) + rkT4; sim_pay must equal measured rkT4;
      sim_ccT4 must equal measured ccT4.
   e. Print per-world summary (nswaps, pay, s*xh sum, s*yh
      sum, predicted, measured) and per-swap lines
      (hit index, pass, s, xkey, ykey, xh, yh, contribution).
6. Prospective prediction: after row 15 (V5-rk0) print PREDICT
   with the simulated sign; after row 16 print CONFIRM against
   measured. Same for V6 rows 17/18. The prediction is computed
   from the rk0 trace only, before the rk4 row is consulted.

## Frozen kill bars

- K1 SUBSTRATE-ANCHOR: row 0 bit-for-bit equals the frozen
  RANK-LAZY row-0 values: R+0:35, R+4:0, R+8:20, R+12:15,
  R+16:80, R+20:48, R+24:0, R+28:76, R+32:0, R+36:35, R+40:40,
  R+44:420, R+48:20, R+52:35, R+56:0, R+60:0, R+64:0, R+68:35,
  R+72:0, R+76:0, R+80:0, R+84:35, R+88:56, R+92:1132,
  R+96:28, R+100:35, R+104:16, R+108:712, R+112:8, R+116:35,
  R+120:80, R+124:48, R+128:0, R+132:0, R+136:0. The trace
  hooks are read-only on M, so any deviation fails the bar.
- K2 PREDICTOR-EXACT: for all 5 base worlds: no trace
  overflow, hit-key sequences identical across rk0/rk4,
  sim_ccT4 == measured ccT4, sim_pay == measured rkT4, and
  predicted_delta == measured_delta as exact integers.
- K3 PREDICT-NEW: V5 and V6: sign(predicted) ==
  sign(measured) and |predicted - measured| <= 2. 2/2 required.
- K4 TRANK1-HEADLINE: NET6 < NET4 on M2C2 (row 10 vs row 1).
- K5 TRANK1-ROBUST: NET6 < NET0 on >= 3 of the 5 worlds
  (rows 10..14 vs rows 0, 2, 4, 6, 8).
- K6 O1-MAINTENANCE: M2C2 row 10: rkT6 <= recT6,
  rkmT6 <= recT6, rkT6 < 553. Carried: rkT4 <= 7 (reported).
- K7 INVARIANCE+LEDGER: outcome offsets identical across rk
  within each world for pairs (0,1), (0,10), (2,3), (2,11),
  (4,5), (4,12), (6,7), (6,13), (8,9), (8,14), (15,16),
  (17,18); exile == ev + drop + promote on all 19 rows
  (cdrop reported, unconstrained, per RANK-LAZY's K6 finding
  that cdrop == 0 overspecified the world-dependent
  cold-overflow path).
- K8 DETERMINISM: 3/3 runs byte-identical (external sha256).

## Verdict rule

VERDICT=PASS iff K1..K8 all PASS. Any other combination is
VERDICT=FAIL (n/8). The bars above are frozen; no weakening,
no post-result changes. K2's exact-equality bars are exact
because the mechanism is an accounting identity under the
checked preconditions; a failure falsifies either the event
logging or H1/H2, both informative. K4/K5 are genuine unknowns.
