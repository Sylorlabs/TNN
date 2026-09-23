# BUILD_LOG.md — U: Recompute-on-demand

## Source
- `cl/arm.zag` (pure Zag, zero randomness).
- Substrate: `substrate/R33_NATIVE_SHA256_V2.zag`, `substrate/R33_NATIVE_IO_V1.zag`
  (copied to trial dir per AGENTS.md lesson).
- Toolchain: `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## Build history (2026-09-21)
- Multiple iterations to fix: M2 double-normalization bug, cid_of missing
  t2/t3 corpora, d_recall negative-index bug (missing [a,b) clip), duel_edits
  expected-bytes sync, M9 JSON interleaving.
- Final binary: `/home/hatch/workspace/u_test` (236,018 bytes).
- 77 analyzer warnings (A0102 ignored return values; non-blocking).

## Compliance status
The source COMPILES but is NOT frozen-spec compliant for the BLOCKED items
in AMBIGUITIES.md (A1–A4, A9). Provisional values are used for engineering
only. All runs are reported as provisional, NOT accepted frozen evidence,
until the blocks are resolved.

## Battery
- Workdir: `work/r1-1x/` (under ~/workspace, per rule).
- Runner: `work/run_u_battery.sh` (custom; omits the two memorizer-control
  legs — NOT the official complete battery).
- Harness legs via `run_metric.sh` (double-run, stdout-identical check).
- M8 gate via `m8_gate.sh`: PASS (5 perturbations × 2 reruns, byte-identical).

## Known issues
- Duel heisenbug at E=150+: ROOT-CAUSED 2026-09-21 — silent i32 overflow in
  `duel_edits` edit-position computation `(e*total)/E` (wraps negative at
  r1 corpus sizes for E>=150; mirror write `prose[off]=255` panics). Fixed
  with i64 arithmetic; same latent overflow in `t_m9` fixed. Full duel
  E=0..1000 completes cleanly; both reruns byte-identical stdout, rc=0.
- The custom runner is not the official complete battery (missing memorizer
  controls). Results are provisional.

## Rebuild (2026-09-21, heisenbug fix)
- Fixed `duel_edits` and `t_m9` in `cl/arm.zag` (i64 edit-position
  arithmetic; two-line change + comments).
- New binary: `/home/hatch/workspace/u_test` (rebuilt; 236,105 bytes main).
- Full duel re-run: E=0..1000, both reruns byte-identical, rc=0.
- M9 re-run: e0=175944, e10=175944, e50=203976, e100=727756, e200=727848,
  e500=727204, e1000=727204, rekey=0, hits=0; byte-identical across reruns.
- No commit of binaries, .zagd, .zag-cache/ (workspace build artifacts only).

## Adjudication (2026-09-21, MARATHON CREW U11) — binding verdict: PASS
Full record: `units/arms/U/ADJUDICATION.md`.
- Frozen §3 extracted programmatically (extract/ + extract/kills.txt +
  extract/terms.txt); VERDICT.md/AMBIGUITIES.md A1–A4 blocks resolved or
  proven non-load-bearing (A1: radius-sensitivity sweep U_R ∈
  {32,64,128,256} full duel E=0..1000 each, double-run byte-identical,
  rc=0, no kill at any radius; R=512 E=0 data point + mechanism-backed
  bounding argument for R≥512; A2: MA1/RC1 rate governs only the
  D-falsification interpretation, not U's kills; A3: U/DReg share the
  identical u_derive code path, duel translation-invariant; A4: DReg is the
  faithful kill-(ii) comparator — Track-A arm D uses a different rule).
- Fresh source build → `work/adjud/build/u_fresh` (236,105 bytes main,
  77 analyzer warnings); m1-1x-prose stdout+stderr byte-identical to
  `/home/hatch/workspace/u_test`. Source search: no rand/LCG/getrandom/
  clock/seed; no `as []i32`/`as []u32`/`as []u16`, no large-struct casts,
  no nested structs, no slice equality (byte arenas + two flat structs).
- M8 gate re-run on fresh binary: 5 perturbations × 2 runs, all rc=0,
  byte-identical — M8GATE PASS (`work/adjud/m8_gate.log`).
- Missing memorizer controls now run under official double-run rule:
  memctrl-p2c-1x, memctrl-c2p-1x (rc=0, stdout IDENTICAL;
  `work/adjud/memctrl/`).
- Kill evaluation (duel E=0..1000, byte-identical reruns): (i) cpu_u
  14,182,612 vs cpu_d 279,875,710 → 0.051×, not >10× — NOT fired;
  (ii) E=100: total_u 1,727,480,888 < total_d 2,219,096,277, U wins 22.1%
  — NOT fired; (iii) determinism gate PASS — NOT fired. U wins every
  E ∈ {0,10,50,100,200,500,1000}; crossover none; zero byte mismatches.
- M4 corrected: arm's all-or-nothing 0.0 is a scoring artifact; instrumented
  probe (`work/adjud/probe/`, print-only, not arm source) localized all 28
  failures to claimed-span stage on code content-defect units; per-unit M4
  = content 372/400 = 93.0%, boundary 100/100 = 100.0% (both ≥ 80%/class).
- M9 corrected: pre-fix fragment superseded; post-fix byte-identical runs:
  e0=175944, e10=175944, e50=203976, e100=727756, e200=727848, e500=727204,
  e1000=727204, rekey=0, hits=0 — plateau holds.
- No commit of binaries, .zagd, .zag-cache/ (workspace build artifacts
  only). VERDICT.md → PASS (BINDING); AMBIGUITIES.md updated; verdict
  sheet U line → PASS (counts: PASS 21, PROVISIONAL 11).
