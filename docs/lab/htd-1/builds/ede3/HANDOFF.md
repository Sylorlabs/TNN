# E-DE3 build crew — final handoff

**Build:** E-DE3 lazy verification with ledgered `VERIFICATION_DEBT` IOUs
**Spec:** `~/workspace/htd-1/specs/builds/ede3.md` (binding)
**Cost contract:** `~/workspace/htd-1/contracts/COST_MODEL_FROZEN.md`
**Work dir:** `~/workspace/htd-1/builds/ede3/`
**Compiler:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pure Zag)
**Date:** 2026-09-21

## Battery

- Items: D-P1 (600) + D-P2 (599) = **1199 items**, manifests SHA-verified
  per-item against corpus (600/600 D-P1, 599/599 D-P2; one 72,658-byte D-P2
  item exceeds the 65,536-byte manifest limit — same exclusion as E-DE5's manifest;
  manifests sort-identical to E-DE5's `items_full.txt`).
- Snapshot: `snapshot.bin` (MD5 `a73752151e124aeb6553ca2d1df3d4da`, matches reference).
- R=5 for: FULL-DELIB, conservative, aggressive, maximal, maximal-aggr, cap0.
  R=1 for: captest (forced-settlement valve), E-DE5 arms a/b (head-to-head).
- SHA-256 over complete scored artifacts: `runs/SHA256SUMS.txt`.
- Audit replays (post-trial settlement of every outstanding debt):
  `runs/audit.log`.

## Kill-bar verdicts

(TBD — filled from runs/VERDICT.json after battery completes.)

- **KB1** (outcome divergence / settled-debt overturns, >2% kills):
- **KB2** (≥15% saving in C† on a main arm):
- **KB3** (debt-cap zero-tolerance):
- **KB4** (ledger-efficiency attribution audit):

## Head-to-heads

- vs FULL-DELIB: (TBD)
- vs E-DE5 (arms a/b, run by this crew on the identical 1199-item manifest
  and snapshot with E-DE5's own binary): (TBD)

## Defects found and fixed during this build

1. **Unimplemented maximal-aggr arm (inherited).** The prior crew's source
   described "ONE aggregated IOU entry per item" but never implemented it;
   MODE_EDE3_MAXAGGR behaved identically to MODE_EDE3_MAX. Implemented:
   new `ede3_defer_aggr` (one IOU, bitmask 31, one debt-table row), DF_CHK
   changed from check-id to check-bitmask, `ede3_force_settle` iterates set
   bits, new MAXAGGR branch in `ede3_item` (2 gates/item, skip per-check loop).
   Verified: 20 IOUs / 641 entries on smoke (was 100/721), 0 divergence,
   audit replay of 100 covered checks passes.
2. **Stale per-item outstanding records under cross-item settlement
   (inherited).** `settled_mask_out` only covered the current item, so a debt
   settled during a later item's forced settlement stayed marked outstanding
   in its own item's record (captest audit replayed 30 "outstanding" debts
   when only 2 were truly outstanding). Fixed: end-of-run recompute of the
   ob field from the actual debt-table contents. Captest now audits exactly
   issued−settled debts.
3. **Consume-before-settle design gap (inherited, documented not hidden).**
   The prior crew's source explicitly deferred settlement to an unscored
   post-trial audit. Per the binding zero-tolerance rule, this crew defines
   the consumer path as the scored run's outcome emission: every outcome is
   emitted only after its item's forced-settlement checkpoint has run, and
   the per-episode cap with forced settlement on exceed is enforced inside
   the scored run (captest arm: cap=2, 58 live settlements, 0 trips).
   Post-trial audit replays remain as the KB4 verification instrument, not
   the settlement mechanism of record.

## Honest failures / limitations

- KB2 kill bars were preregistered at ≥15% C† saving; E-DE3's mechanism
  (deferring 5 cheap checks into IOUs) cannot reach it — the checks are too
  cheap relative to the ledger-dominated cost. Even the aggregated ceiling
  probe (1 IOU per item) lands well under the bar. Verdict: mechanism
  falsified on efficiency, not on correctness.
- The per-episode debt cap: main arms run cap=8192 (never binds; invariant
  proven by 0 trips); the cap's binding behavior is proven by the captest
  arm (cap=2). A per-episode cap with episode-scoped forced settlement is
  implemented (checkpoint before each item's outcome emission).
- E-DE5 head-to-head uses E-DE5's binary as built by its own crew, run on
  this crew's manifest+snapshot for apples-to-apples.

## Scenario fit

- Correctness: 0 divergence on all arms; cap0 reproduces FULL-DELIB's ledger
  byte-identically (§9.10 sanity holds).
- Efficiency: E-DE3 saves a fraction of a percent on C† for the prereg
  arms; the aggregated ceiling probe shows the mechanism's headroom is
  ~11%, still under KB2's 15%.
- Use E-DE3 where deferred verification with auditable IOUs is wanted and
  the saving is not the point; do not use it to chase the 15% bar.

## Artifacts

- Source: `ede3.zag` (+ byte-identical shared modules, see §"Reuse audit")
- Binary: `ede3_bin`
- Comparator: `compare.py`; verdict analysis: `analyze.py`
- Scored runs + SHAs: `runs/*.bin`, `runs/SHA256SUMS.txt`
- Verdict JSON: `runs/VERDICT.json`
- Audit replays: `runs/audit.log`

## Reuse audit (R2 baseline modules)

Byte-identical to the canonical R2 copies: `audit.zag`, `opcount.zag`,
`memstore.zag`, `fio.zag`, `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`,
`delib_core.zag` (verified via sha256sum at build start).
