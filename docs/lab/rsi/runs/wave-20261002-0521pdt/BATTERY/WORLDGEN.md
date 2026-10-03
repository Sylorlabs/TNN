# WORLDGEN.md: E10 build record (wave-20261002-0521pdt, lane BATTERY-E9)

## Commit-order self-check (T-K1)

- PREREG_E10.md SHA-256 `6d7cb92dbfe59a7622196f28bc55ac5c58c7e2c467c268b214df44fa98046952`
  computed BEFORE any battery artifact existed (sha256sum ran before
  `git add`). No .zag, .sh, .txt, or binary in this lane existed at
  that time (only PREREG_E10.md, NAMECHECK.md, CORRECTIONS.md).
- Freeze commit `d22862d07` contains the prereg and NAMECHECK.md from
  this lane. It ALSO contains 72 files from the concurrent ARENA lane
  (staged by another worker; this worker's `git commit` without a
  pathspec swept the shared index). Zero E10 battery artifacts
  (world/template/driver/scorer/generator) were in the commit or
  existed before the prereg hash: verified by file listing (only the
  two BATTERY files) and mtime order. T-K1's substance holds; the
  contamination is recorded transparently in SEALED_RESULTS.md and
  REDTEAM_SELF.md. No history rewrite was performed (shared repo,
  concurrent workers); the ARENA worker's files are intact.
- Sealed PIs derived AFTER the freeze commit, mechanically from the
  frozen prereg hash (PI_RECORD.txt, PI_ENV.sh). No world, template,
  or driver existed at derivation time.

## Toolchain

- safebin active (36 tools, no python3/python; `which python3` empty).
- Pinned znc `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
- New AGENTS.md toolchain lesson applied (2026-10-02, second znc
  miscompile): all E10 Zag tools use the safe-emit discipline (one
  preallocated output buffer + cursor, a single
  `_zag_raw_syscall(1,1,ptr,len)` write at end; no `_zag_print` for
  dynamic content). Every binary's stdout bytes were verified before
  use (od -c spot checks; usage paths; a positive LEAKCHECK case ->
  WORLD-INVALID exit 2).
- Pinned-compiler rule observed: no `as *i32` + slice construction;
  u8-cell loop idiom throughout. No forbidden executable invoked.

## Tools built (post-freeze)

- `e10_score.zag` -> `e10_score_bin`: transcript scorer; HIT/NEED/
  CHOICE directives; T-K15(b) leakcheck (no NEED/bar probe's
  (s,r,expected) OBSERVE-taught; M2 exempt per prereg). Logic adapted
  from E9's e9_score.zag; emit layer rewritten safe.
- `e10_degen.zag` -> `e10_degen_bin`: D0/D1/D2 degenerate transcript
  generator. Logic from E9's degen.zag; emit layer rewritten safe.
- `e10_score_m2w1.zag`, `e10_score_m2w2.zag`, `e10_score_m2w3.zag`:
  T-K8/T-K9/T-K10 sub-bar scorers (driver-log + transcript + truths +
  vocab). New code, safe emit.
- `e10_inspect.zag` -> `e10_inspect_bin`: read-only state diagnostic
  (TRIAL counters, POLICYROOT, MAP list, UNCERT/GUIDE counts). Never
  part of a bar. (Note: prints one `MAP s=0 r=0` artifact line on the
  M1 block; inspector simplification artifact, diagnostic only.)
- `e10_m2_driver.sh`: deterministic bash driver for the three M2
  worlds (template phases, sealed PIs from env, vocab-verify
  fail-closed, COLLATERAL logging). No timestamps/PIDs in outputs.
- `run_blocks.sh`: block runner (fresh state per block, persistent
  within block; T-K3 shim hash check per run; fail-closed).

## World files (transcribed exactly from PREREG_E10.md section 6)

- Static: `m1w1_world.txt` (18 lines, 4 probes),
  `m1w2_world.txt` (18 lines, 6 probes),
  `m1w3_world.txt` (12 lines, 5 probes),
  `m3w1_world.txt` (15 lines, 6 probes),
  `m3w2_world.txt` (21 lines, 8 probes),
  `m3w3_world.txt` (19 lines, 8 probes).
- Templates: `m2w1_template.txt`, `m2w2_template.txt`,
  `m2w3_template.txt` (driver-grown per prereg 6.4-6.6).
- Barspecs: `m1w1.barspec`, `m1w2.barspec`, `m1w3.barspec`,
  `m3w1.barspec`, `m3w2.barspec`, `m3w3.barspec` (indices re-verified
  against the streams: pre-freeze audit in prereg 7.5 confirmed
  mechanically by QUERY counts: 4/6/5/6/8/8).

## Sealed PI derivation (post-freeze, mechanical)

H = sha256(PREREG_E10.md) =
`6d7cb92dbfe59a7622196f28bc55ac5c58c7e2c467c268b214df44fa98046952`
(bytes 6d 7c b9 2d = 109 124 185 45):
- W1: 109 mod 6 = 1 -> 1->A, 2->C, 3->B.
- W2: 124 mod 2 = 0 -> 1->A, 2->B.
- W3 ep A: 185 mod 2 = 1 -> 1->B, 2->A; ep B: 45 mod 2 = 1 -> 1->C, 2->A.
Recorded in PI_RECORD.txt / PI_ENV.sh; manifest-hashed.

## Manifest

`WORLD_MANIFEST.sha256`: 28 files (prereg, namecheck, corrections,
PI records, 6 static worlds, 3 templates, 6 barspecs, 6 zag sources,
driver, block runner). `sha256sum -c` clean (0 bad).

## Anti-smuggling (T-K4)

`grep -rE '\b6[0-9]{4}\b'` over `tnn2_build/tnn2.zag` and
`core_freeze_tnn2_shim/freeze_shim2.zag`: zero matches. (Two
coincidental hash-fragment hits in the gitignored `.zag-cache`
compiler cache only; documented benign, same precedent as E9.)
