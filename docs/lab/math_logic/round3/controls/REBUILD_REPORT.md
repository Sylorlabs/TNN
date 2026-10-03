# MATH R3 — Control Rebuild Report

Date: 2026-09-25. Crew: CONTROL REBUILD. Task: verbatim rebuild of the two
R3 control engines (DUAL-R1, REF-FIRST) and exact re-verification against
the frozen R2 evidence.

## 1. Verbatim builds

Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero source changes — both binaries built from the committed sources with
the exact commands in their BUILD docs. Sources in the working tree are
untouched (no local git; tree SHAs of the built sources are recorded).

### DUAL-R1 (round-1 DUAL, R2 verdict winner)
- Source: `math_logic/engines/dual/dual.zag` (SHA-256
  `4173bcbf05543f7c0c8fa56a1239ee4f61b8a7cb66e0e21e59693ad20307ce8e`)
- Shared: `engines/common/*` + verbatim `deliberation_depth/harness/dlb_delib.zag`
  (SHA-256 `35393253fe98528ef5fb79fe214109254d5a4a3695cee1a904035d29e96ed122`
  — identical to the reffirst copy and to the SHA pinned in
  `round2/engines/reffirst/BUILD_REFFIRST.md`).
- CWD: `engines/dual` (per `BUILD_DUAL.md`).
- Command: `znc_linux_x86_64_abed8aa1 dual.zag --no-zagd --no-analyze
  --no-foreground-cache -o round3/controls/dual_r1_bin`.
- Result: BUILD SUCCESS, no warnings emitted.
- Binary SHA-256: `a4531d84ddfee3171d33ee3c29ea3b17c85e3e8ec8e6773790ddd03d303943c6`
  (309,710 bytes). Placed at `math_logic/round3/controls/dual_r1_bin`
  (NOT committed to the repo — R2 convention, sources only).

### REF-FIRST (best R2 engine)
- Source: `math_logic/round2/engines/reffirst/reffirst.zag` (SHA-256
  `0d2a9d6de2ab9269e083002c715ef9ba48ee114b8214d2b732498a8f572fa5b1`)
- Local `dlb_delib.zag` copy byte-identical to the deliberation_depth
  harness original (SHA-256 `35393253fe98528ef5fb79fe214109254d5a4a3695cee1a904035d29e96ed122`).
- CWD: `round2/engines/reffirst` (per `BUILD_REFFIRST.md`).
- Command: `znc_linux_x86_64_abed8aa1 reffirst.zag --no-zagd --no-analyze
  --no-foreground-cache -o round3/controls/reffirst_bin`.
- Result: BUILD SUCCESS, no warnings emitted.
- Binary SHA-256: `5d41fabc4b82023f52038102921eff3d6a16b3333b3522e3ff223017dd6de15d`
  (339,932 bytes). Placed at `math_logic/round3/controls/reffirst_bin`
  (NOT committed — sources only).

## 2. Static checks

- Zero-RNG grep backstop over both engine sources (+ both dlb_delib copies +
  engines/common): CLEAN — the only match is the comment "Zero RNG, no
  wall-clock" in dlb_delib.zag.
- Sealed guard: both binaries exit **3** on an input path containing
  "sealed" (problem file and store path both guarded).

## 3. R2 number reproduction

Runner: `round3/controls/rerun_r3_controls.py` — mirrors
`round2/evidence/r2/runners/run_battery.py` scoring semantics exactly
(incl. the F-SEAL-01 B2_07 WITHHELD correction). Engine CWD =
`math_logic/`. DUAL: `dual_r1_bin <prob> <out>`. REF-FIRST:
`reffirst_bin <prob> <out> <bound>` (bound 8; B6X 128). 3 external runs
per problem, byte-identical asserted; divergence/timeout → hard fail.

Oracle: frozen R2 evidence —
`round2/evidence/r2/results_formal_all_batteries.json` (B2R–B5X) and
`round2/evidence/r2/results_formal_b2r_b3r_b4r_b4x_b6x.json` (B6X).
`oracle_exact` = rebuilt-binary output matches the R2 record on verdict,
confidence, derivation count, AND full output SHA-256, per problem.

| Battery | DUAL-R1 (rebuilt) | DUAL-R1 (R2) | REF-FIRST (rebuilt) | REF-FIRST (R2) |
|---|---|---|---|---|
| B2R | 12/12 | 12/12 | 12/12 | 12/12 |
| B3R | 10/10 | 10/10 | 10/10 | 10/10 |
| B4R | 15/15 | 15/15 | 12/15 | 12/15 |
| B4X | 10/15 | 10/15 | 6/15 | 6/15 |
| B5X | 36/60 (24 false_derived) | 36/60 (24 false_derived) | 36/60 (24 false_derived) | 36/60 (24 false_derived) |
| B6X | 3/3 | 3/3 | 3/3 | 3/3 |

**VERDICT: ALL R2 NUMBERS REPRODUCE EXACTLY.** Beyond the aggregate
counts: **every one of the 115 problems per engine (230 total) matches
the frozen R2 record byte-for-byte** (oracle_exact = 230/230 — verdict,
confidence, derivation count, and complete output SHA-256 all identical
to R2). Zero divergent reruns (3/3 external runs byte-identical on all
problems, on top of each binary's own in-process 3x assertion), zero
timeouts, zero exit≠0.

Note on the DUAL B6X leg: R2 ran B6X with an evaluation-only bound-128
variant (`dual_b6x_bin`); the verbatim rebuild used bound 8. Empirically
the verbatim binary reproduces all three B6X problems at the R2
verdicts AND the R2 derivation counts (121/112/105-style: B6X_01 = 121
for DUAL, 123 for REF-FIRST — matching the R2 records), so the
variant's bound change is behaviorally inert on this battery. No source
change was needed; the verbatim binary stands as the R3 control.

## 4. Artifacts

- `math_logic/round3/controls/dual_r1_bin` — verified DUAL-R1 binary (not committed).
- `math_logic/round3/controls/reffirst_bin` — verified REF-FIRST binary (not committed).
- `math_logic/round3/controls/rerun_r3_controls.py` — rerun script (mirrors R2 runner).
- `math_logic/round3/controls/rerun_results_r3_controls.json` — full per-problem
  results (verdict/confidence/derivations/output SHA × 3-run wall time).
- `math_logic/round3/controls/rerun_out/` — raw per-problem outputs (230 × 3 runs).
