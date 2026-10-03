# REPORT: RANK-LAZY (frozen lazy-ranking replication + threshold variant)

Date: 2026-10-03. Worker: RANK-LAZY (non-ledger task; claim
minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_lazy/.

## Verdict

**FAIL (4/7)** under the frozen prereg (K1..K6 in-binary, K7
external: 3/3 runs byte-identical,
sha256 `8e90e6aa42011eba2a7c25d0513f42472d620f0342feb22ea8c0e1e453e6e85d`).

K1 PASS, K2 FAIL, K3 FAIL, K4 PASS, K5 PASS, K6 FAIL, K7 PASS.
The headline result is frozen and positive; the three failures
are one genuine scientific negative, one mechanical bar
overspecification, and one genuine robustness negative. No
erratum is filed: the implementation matches the frozen design.
The bars are not weakened.

## What was built

Additive on RANK-CHEAP's rank_cheap.zag (carried over, no
redesign):
- M buffer 4096 -> 4160 bytes; ranked-flag side table at offset
  4096 (64 x u8, one per cold slot); zeroed by mem_zero,
  cleared on promote/exile alongside the rc reset;
- thresh_rerank (rk=5, threshold-crossed re-rank): on a cold hit,
  after the rc increment, if rc >= T_rank (frozen T_rank = 2)
  and the entry's ranked flag is clear, one swap-with-front
  (honest cost 1 iff s > 0; no-op at s = 0); the flag follows
  the ranked entry and fires at most once per residency;
  move-then-promote placement; promote_slot uses the post-move
  slot;
- rk==5 branch in cold_lookup; rk=0/1/2/3/4 logic unchanged.

11 rows per run (144 bytes/row): M2C2 (mode=1, w=21, c2w=10)
rk=0/4/5; V1 (mode=1, w=40) rk=0/4; V2 (mode=2, w=21) rk=0/4;
V3 (mode=3, w=21) rk=0/4; V4 (mode=0, w=21) rk=0/4; all pol=6,
pm=1. The substrate has no RNG; "different seeds" is realized
as different churn patterns (mode/dose variation), stated in
the frozen prereg.

## Measured table (per world, NET = ccT + rkT)

| world | NET0 (FIFO) | NET4 (lazy) | delta |
|-------|-------------|-------------|-------|
| M2C2  | 1132        | 1097        | -35   |
| V1    | 2388        | 2357        | -31   |
| V2    | 1100        | 1089        | -11   |
| V3    | 1036        | 1045        | +9    |
| V4    | 408         | 410         | +2    |

M2C2 rk=5 (threshold variant): ccT5=1132, rkT5=27,
NET5=1159.

## Kill-bar summary

- K1 HEADLINE-NET4: PASS. Anchor row bit-for-bit
  EXILE-PROMOTION PXP-M2C2 (substrate unchanged), and
  NET4 = 1091 + 6 = 1097 < 1132, exactly replicating
  RANK-CHEAP's exploratory row. The lazy net win is now a
  frozen result on M2C2.
- K2 ROBUST-SEED: FAIL (2/4 < 3). The win holds under heavier
  churn (V1, -31) and the extra-churner pattern (V2, -11) but
  reverses under the no-owner-16 pattern (V3, +9) and
  single-owner churn (V4, +2). The 35-point M2C2 win is
  pattern-sensitive, not a general property of lazy ranking.
- K3 THRESHOLD-VARIANT: FAIL (NET5=1159 >= 1132).
  Importance-triggered re-rank is pure cost: ccT5=1132 is
  exactly FIFO's scan cost (the displacement is perfectly
  scan-neutral), rkT5=27 is dead maintenance. Interpretation:
  rank-then-promote can never bank a fronting benefit because
  the ranked entry leaves cold in the same hit; the
  displacement pathology fires with zero benefit. This
  sharpens RANK-CHEAP's finding: laziness helps only when the
  fronted entry stays resident to be re-hit.
- K4 O1-MAINTENANCE: PASS. rkT4=6 <= 7; rkT5=27 <= recT5=56
  (each residency fires at most once); both < 553.
- K5 INVARIANCE: PASS. All outcome fields identical across
  rk within every world; ranking remains cost-shaping only.
- K6 LEDGER: FAIL on a mechanical overspecification. The
  frozen bar required cdrop == 0 on all 11 rows, but V1
  (w=40) and V2 (mode=2) fill the 64-slot cold tier and take
  the documented FIFO cold-overflow path (cdrop=23 and 5,
  identical across rk within each world). The actual
  accounting invariant, exile == ev + drop + promote, holds
  in all 11 rows (e.g. V1: 110 = 86 + 0 + 24; V2:
  96 = 68 + 0 + 28). The bar overspecified a
  world-dependent quantity; the ledger itself is intact.
  The bar is not amended post-result; it stands as failed.
- K7 DETERMINISM: PASS. 3/3 byte-identical,
  sha256 `8e90e6aa42011eba2a7c25d0513f42472d620f0342feb22ea8c0e1e453e6e85d`.

## Mechanism-level findings worth keeping

1. The frozen headline is positive: periodic swap (every 8th
   cold hit) nets 35 points over FIFO on M2C2 at maintenance
   cost 6, replicated exactly (ccT4=1091, rkT4=6). This is no
   longer exploratory.
2. The win is pattern-sensitive (K2): -31/-11 under heavier
   or multi-churner patterns, +9/+2 under no-owner-16 and
   single-owner churn. Lazy ranking is a conditional win,
   not a general one.
3. Threshold-crossed re-rank fails in the informative
   direction (K3): triggering on the entry's own importance
   signal (rc >= 2) ranks exactly the entries about to be
   promoted, so the fronting benefit can never be collected.
   Schedule-lazy (rk=4) fronts entries that stay resident;
   threshold-lazy (rk=5) fronts entries that leave. The
   distinction matters.
4. The O(1) cost-model derivations held exactly for both new
   primitives (rkT4=6, rkT5=27 <= 56), and invariance/ledger
   confirm ranking remains a cost-shaping discipline, not a
   capability change.

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `command -v python3` / `command -v python` verified empty
  before the prereg commit; znc 2026.07.0-dev cmp-verified
  byte-identical to src/tools/toolchain/znc_linux_x86_64_abed8aa1
  before the prereg commit. No python invoked at any point in
  this lane; no PROCESS-FAIL condition triggered.
- grep audit on the implementation: no `while.*!(` negated
  conjunctions, no _zag_print, no `as *i32` slice
  construction; if-nesting at most 3; single approved
  `as *u8` in z_alloc (carried over).
- Commits local only, never pushed, explicit pathspecs, no
  reset. Prereg committed alone first (13e1f8d57);
  implementation and artifacts committed after the verdict.
  No errata; no post-result bar changes.

## What this does NOT test (honest accounting)

- Whether the pattern-sensitivity of the lazy win (K2)
  traces to a specific layout/churn interaction worth a
  further frozen bar; sealed post-freeze worlds; other
  policies, doses, or pm values; ranking under cold overflow
  beyond the observed cdrop path.

## Artifacts

- `rank_lazy.zag`: implementation (pure Zag; RANK-CHEAP
  substrate + ranked-flag table + thresh_rerank + rk=5
  branch + 11-row main).
- `rank_lazy_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  runs (sha256 `8e90e6aa42011eba2a7c25d0513f42472d620f0342feb22ea8c0e1e453e6e85d`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty stderr logs;
  `err_build.txt`: one benign znc warning line about zagd
  unavailability.
- `PREREG.md` (frozen 2026-10-03, no errata),
  `NAMECHECK.md`, `REPORT.md`.
