# REPORT: RANK-CHEAP (cheaper ranking-maintenance primitives)

Date: 2026-10-03. Worker: RANK-CHEAP (non-ledger task; claim
minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_cheap/.

## Verdict

**FAIL (5/7)** under the frozen prereg (K1..K6 in-binary, K7
external: 3/3 runs byte-identical,
sha256 `4038211b59217e24d5cc482a3dde74a1fb338b01351ecb832447b26bd24ed30c`).

K1 PASS, K2 PASS, K3 FAIL, K4 FAIL, K5 PASS, K6 PASS, K7 PASS.
The two failures are informative, not mechanical: the frozen
derivations D3/D4 (maintenance bounds) held exactly, the anchor
held exactly, invariance and ledger held. What failed were the
two hypotheses about scan savings (D6/D7). No erratum is filed:
the implementation matches the frozen design; the world did not
match the prediction. The bars are not weakened.

## What was built

Additive on the COLD-RANKING substrate (carried over unchanged;
mtf_move/bubble_up carried as substrate, not exercised):
- header offset 72: hits_since_rank (per-row cold-hit counter,
  zeroed by mem_zero at each row start);
- swap_front (rk=3, eager O(1)): on every cold hit at slot s>0,
  one cslot_swap(M,s,0); rank_cost += 1 per swap (the honest price
  of the O(1) primitive at scan-cost granularity); rank_moves += 1;
  returns slot 0. No-op at s=0;
- periodic_swap (rk=4, lazy): the same primitive applied only
  every 8th cold hit (hsr reaches 8, then resets); other hits leave
  the entry in place; returns the post-move slot;
- rk==3/rk==4 branches in cold_lookup after the rc increment and
  before the promotion check (same move-then-promote placement);
  promote_slot uses the post-move slot.

## Measured table (M2C2, pm=1, per rk)

| rk | R1 cc | ccT | rkT | rkmT | R4 cc | NET=ccT+rkT |
|----|-------|-----|-----|------|-------|-------------|
| 0 (FIFO) | 420 | 1132 | 0 | 0 | 712 | 1132 |
| 3 (swap/eager) | 421 | 1134 | 55 | 55 | 713 | 1189 |
| 4 (periodic/lazy) | 423 | 1091 | 6 | 6 | 668 | 1097 |

All other fields identical across rk (K5): rec1=40, prm1=20,
rec2=rec3=0, rec4=16, prm4=8, recT=56, prmT=28, postH=postH2=35,
exile=76, ev=48, drop=0, cdrop=0. Ledger holds in all three rows
(K6).

## Answers to the design questions

**Does O(1) maintenance make ranking a net win? (NET < 1132?)**
For EAGER swap-with-front: no. NET3=1189 > 1132 (K3 FAIL). The
D6 hypothesis was wrong in a specific way: swap-with-front does
not achieve MTF-class scan savings. ccT3=1134 is slightly WORSE
than FIFO's 1132. The swap primitive's displacement pathology
cancels its fronting benefit: every swap throws slot-0's occupant
to a deep slot, and that damage offsets the gain of fronting the
hit entry. Maintenance collapsed (55 vs MTF's 989 and
importance-bubble's 553, exactly within the frozen bound <=56),
but there is no scan saving to set against it, so the honest
total is a net loss of 57.

**What is the tradeoff? (less precise ordering vs cheaper
maintenance)**
The frozen D7 hypothesis (more maintenance = better ordering)
failed in the informative direction (K4 FAIL: ccT3=1134 >
ccT4=1091). For this primitive there is NO tradeoff: laziness
strictly dominates eagerness on both axes. Periodic swap (7 rank
events, 6 paying) saves 49 maintenance points AND 43 scan points
relative to eager swap. Interpretation: the 1-in-8 schedule reaps
the fronting benefit for genuinely hot entries while disturbing
the layout 8x less often, so the displacement pathology rarely
fires.

**Exploratory (not a frozen bar): periodic swap IS a net win.**
NET4 = 1091 + 6 = 1097 < 1132, a net win of 35 over FIFO at
maintenance cost 6. This was not preregistered (K3 covered NET3
only), so it stays exploratory: the honest follow-up is a lane
that freezes NET4 < 1132 as its headline bar, possibly with a
threshold-crossed variant alongside the periodic schedule.

## Mechanism-level findings worth keeping

1. Swap-with-front is a WORSE ordering primitive than doing
   nothing, eagerly applied (ccT 1132 -> 1134). Fronting the hit
   entry is not free even at O(1) maintenance: the displaced
   entry pays. MTF's adjacent-shift is gentler to the displaced
   entries (they shift right by 1 and stay near the front) than
   swap's throw-to-deep-slot.
2. Laziness fixes the pathology it creates. The same primitive
   applied 1-in-8 hits beats FIFO's scan (1091 < 1132) because
   the layout is disturbed rarely enough that fronted entries
   stay fronted.
3. The O(1) accounting derivations held exactly: rkT3=55 <= 56
   (55 of 56 hits at s>0), rkT4=6 <= 7 (7 events, one at s=0).
   The per-hit cost model for the primitive is exact, not
   approximate.
4. Ranking remains a cost-shaping discipline, not a capability
   change: K5/K6 confirm outcomes, recovery counts, promotions,
   and the exile ledger are identical across rk=0/3/4.

## Kill-bar summary

- K1 ANCHOR-RK0: rk=0 row bit-for-bit EXILE-PROMOTION PXP-M2C2
  (cc4=712, ccT=1132, rkT=0). PASS (substrate unchanged).
- K2 O1-MAINTENANCE: rkT3=55 <= 56, rkmT3=55 <= 56, rkT3 < 553;
  rkT4=6 <= 7, rkmT4=6 <= 7, rkT4 < 553. PASS (D3/D4 exact).
- K3 NET-WIN: NET3=1189 >= 1132. FAIL (D6 refuted).
- K4 TRADEOFF: ccT3=1134 > ccT4=1091. FAIL (D7 refuted;
  laziness dominates eagerness on both axes).
- K5 INVARIANCE: all outcome fields identical across rk. PASS.
- K6 LEDGER: exile == ev+drop+promote, cdrop=0, all rows. PASS.
- K7 DETERMINISM: 3/3 byte-identical. PASS.

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `command -v python3` / `command -v python` verified empty before
  the prereg commit; znc pinned 2026.07.0-dev, cmp-verified
  byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
  before the prereg commit. No python invoked at any point in this
  lane; no PROCESS-FAIL condition triggered.
- grep audit on the implementation: no `while.*!(` negated
  conjunctions, no _zag_print, no `as *i32` slice construction;
  if-nesting at most 3; single approved `as *u8` in z_alloc
  (carried over).
- Commits local only, never pushed, explicit pathspecs, no reset.
  Prereg committed alone first (17d46248f); implementation and
  artifacts committed after the verdict. No errata; no
  post-result bar changes.

## What this does NOT test (honest accounting)

- The exploratory NET4=1097 net win is not a frozen-bar result;
  it needs its own preregistered lane.
- Threshold-crossed re-rank (rank only when rc crosses a
  threshold) vs the periodic schedule.
- Importance signals beyond current-residency rc; ranking under
  cold overflow; other policies, doses, or pm values; sealed
  post-freeze worlds.

## Artifacts

- `rank_cheap.zag`: implementation (pure Zag; COLD-RANKING
  substrate + additive swap_front / periodic_swap).
- `rank_cheap_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical runs
  (sha256 `4038211b59217e24d5cc482a3dde74a1fb338b01351ecb832447b26bd24ed30c`).
- `err1.txt`, `err2.txt`, `err3.txt`, `err_build.txt`: empty
  stderr logs (err_build.txt carries one benign znc warning line
  about zagd unavailability).
- `PREREG.md` (frozen 2026-10-03 12:05 UTC, no errata),
  `NAMECHECK.md`, `REPORT.md`.
