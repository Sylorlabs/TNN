# REPORT: COLD-RANKING (LRU/importance ranking within cold)

Date: 2026-10-03. Worker: COLD-RANKING (non-ledger task; claim
minting paused). Lane:
`docs/lab/research-lead/overnight-20260928/cold_ranking/`.

## Verdict

**PASS 7/7** under the amended prereg (K1..K6 in-binary, K7
external: 3/3 runs byte-identical,
sha256 `f97e8fc6777118017b56f05d6572faa67e8f2b5f3957366648f9c10fc0e2b03f`).

Honest accounting of the amendment: the initial frozen run produced
VERDICT=FAIL on a worker-side derivation error, corrected through
the transparent erratum process (no mechanism or implementation
change to the ranking machinery):
- E1: the frozen R4 derivation forgot within-pass
  self-interference. In R4's owner-1 pass the 8 repositionings
  stack the entries at slots 0..7, so the owner-2 pass does not
  find each entry at slot 0: MTF reverse-stacks (owner-2 hits each
  at slot 7), while bubble-up halts at rc ties (owner-2 hits at
  slots 0..7). Corrected: cc4(rk1)=420+N, cc4(rk2)=392+N with an
  exact +28 gap (same N), rk4(rk1)=404+N, rk4(rk2)=348+N,
  rkm4=16/15. The first run's measurements (cc4 435/407,
  rkT 989/553, rkmT 55/34) already matched the corrected model with
  N=15 and stay exploratory; the verdict rests SOLELY on the clean
  re-freeze: amended assertions, rebuilt binary, three fresh runs.

## What was built

Rank machinery added additively on the EXILE-PROMOTION substrate
(hot mechanism, cold tier, exile, FIFO cold overflow, recovery
path, promotion at T=2, all carried over unchanged; K1 proves rk=0
reproduces EXILE-PROMOTION's PXP-M2C2 row bit-for-bit). Additive
code only:
- header offsets 64 (rank_cost, slot-positions advanced) and 68
  (rank_moves, hits advancing >=1 slot);
- cslot_swap / mtf_move / bubble_up: slot moves relocate the
  20-byte cold entry AND its rc byte together (the signal never
  detaches);
- rk threaded through mem_read_recov / test_A_recov / cold_lookup:
  rk=0 none, rk=1 move-to-front on every cold hit (recency),
  rk=2 bubble-up while rc(s) > rc(s-1) (importance);
- rank move on every cold hit after the rc increment and before
  the promotion check (move-then-promote); promote_slot uses the
  entry's post-move slot.

## Measured table (M2C2, pm=1, per rk)

| rk | R1 cc | ccT | rkT | rkmT | R4 cc | NET=ccT+rkT |
|----|-------|-----|-----|------|-------|-------------|
| 0 (FIFO) | 420 | 1132 | 0 | 0 | 712 | 1132 |
| 1 (MTF/recency) | 610 | 1045 | 989 | 55 | 435 | 2034 |
| 2 (bubble/importance) | 420 | 827 | 553 | 34 | 407 | 1380 |

All other fields identical across rk (K4): rec1=40, prm1=20,
rec2=rec3=0, rec4=16, prm4=8, recT=56, prmT=28, postH=postH2=35,
exile=76, ev=48, drop=0, cdrop=0. Ledger holds: exile ==
ev+drop+promote in all three rows (K5).

## Answers to the design questions

**Does ranking reduce the positional cost? (cc4=712 -> ?)**
Yes: 712 -> 435 (move-to-front) and 712 -> 407 (importance
bubble). The scan savings are real and match the corrected
derivation exactly (N=15: 420+15, 392+15). Total scan also falls:
ccT 1132 -> 1045 / 827.

**What is the cost of maintaining the ranking? Does it offset the
savings?** Yes, and it more than offsets them. Maintenance
(rkT, same slot-position granularity as cold scan cost): 989 for
MTF, 553 for importance bubble. Honest totals: NET 2034 (rk=1)
and 1380 (rk=2) vs FIFO's 1132. Ranking is a net LOSS on total
cost in this workload: every cold hit pays O(position) to move,
while the scan saving per hit is bounded by the same position.
The honest finding from EXILE-PROMOTION stands but is now priced:
positional cost is real, and curing it with per-hit ranking costs
more than it saves.

**Three mechanism-level findings worth keeping:**

1. MTF INFLATES the promotion-pass scan (R1 cc 420 -> 610).
   Move-to-front fights the promotion's slot-0 refill: each
   owner-2 hit finds its entry at slot 19 (the previous
   promotion's victim refilled slot 0), so the rank move
   systematically undoes the layout the workload wants. Naive
   recency is actively harmful during promotion passes.
2. Within-pass self-interference (erratum E1). Rank moves within
   one pass push earlier entries right, so the second touch of
   each entry re-scans the stack. MTF reverse-stacks (owner-2
   hits at slot 7 each); bubble-up tie-stacks (hits at slots
   0..7). The +28 gap between the modes is exact (same N), a
   sharp discriminator the bars now freeze.
3. Importance strictly dominates recency here. rk=2 moves entries
   only on evidence (rc strictly exceeding the predecessor):
   identical-or-better scan (ccT 827 < 1045, cc4 407 < 435) at
   nearly half the maintenance (rkT 553 < 989, rkmT 34 < 55).
   Moving on every touch (pure recency) pays for 38 R1 moves
   that evidence-gating avoids (19).

**What this does NOT change:** outcomes. K4 proves ranking alters
costs only: recovery counts, promotion counts, hot restoration,
exile/eviction/drop accounting, and cold_drop are identical across
rk=0/1/2. Ranking is a cost-shaping discipline, not a capability
change, and in this workload the shape it produces is worse.

## Kill-bar summary

- K1 ANCHOR-RK0: rk=0 row bit-for-bit EXILE-PROMOTION PXP-M2C2
  (cc4=712, ccT=1132, rkT=0). PASS (substrate unchanged).
- K2 SCAN-SAVINGS: cc4 435/407 < 712; cc4(rk1)==cc4(rk2)+28
  (exact stacking gap); bounds [420,448]/[392,420]; ccT both <
  1132; cc1(rk1)==610 (MTF inflation), cc1(rk2)==420. PASS.
- K3 OFFSET: NET 2034/1380 > 1132 (maintenance more than offsets);
  rkT(rk1) > rkT(rk2) > 0; 974<=989<=1002; 538<=553<=566. PASS.
- K4 INVARIANCE: all outcome fields identical across rk. PASS.
- K5 LEDGER: exile == ev+drop+promote, cdrop=0, all rows. PASS.
- K6 RANK-ACCOUNTING: rkmT 0/55/34 exactly. PASS.
- K7 DETERMINISM: 3/3 byte-identical (clean re-freeze). PASS.

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `command -v python3` / `command -v python` verified empty before
  the build and before the runs; znc pinned 2026.07.0-dev,
  cmp-verified byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 before the prereg
  commit. No python invoked at any point in this lane; no
  PROCESS-FAIL condition triggered.
- grep audit on the implementation: no `while.*!(` negated
  conjunctions (bubble_up uses a go-flag loop), no _zag_print,
  no `as *i32` slice construction; single approved `as *u8` in
  z_alloc (carried over); if-nesting at most 3.
- Commits local only, never pushed, explicit pathspecs, no reset.
  Prereg committed alone first (36f64000c); pre-implementation
  amendment (26332aa58); erratum E1 (c841af7dd); implementation
  and artifacts committed after the re-freeze verdict.
- The stale repo-wide cherry-pick from another worker was not
  touched.

## What this does NOT test (honest accounting)

- Cheaper maintenance primitives (swap-with-front at O(1) per
  hit, lazy/periodic ranking): the named follow-up. This lane
  prices EAGER per-hit ranking only.
- Importance signals beyond current-residency rc (a lifetime
  counter needs key-keyed state; the rc-reset-on-install that
  promotion requires destroys cross-residency importance).
- Ranking under cold overflow (cold never fills here; cdrop=0).
- Rank modes with pm=0, other policies, or other doses.
- Sealed post-freeze worlds.

## Artifacts

- `cold_rank.zag`: implementation (pure Zag; EXILE-PROMOTION
  substrate + additive rank machinery).
- `cold_rank_bin`: built binary (clean re-freeze build).
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical runs
  (sha256 `f97e8fc6777118017b56f05d6572faa67e8f2b5f3957366648f9c10fc0e2b03f`).
- `err1.txt`, `err2.txt`, `err3.txt`, `err_build.txt`: empty
  stderr logs.
- `PREREG.md` (with dated erratum E1), `NAMECHECK.md`, `REPORT.md`.
