# LANE_RESULT.md: DDES R2 independent re-verification (wave 20260930-2021pdt, lane ddes_r2_verify)

Independent re-verification of DDES R2 kill bars K-R2.1..K-R2.6. Resolves the
11:21 M4 verdict "DDES R2 PROVISIONAL pending independent re-verification".

## Frozen references

- Prereg: commit d31e901b0, file
  docs/lab/rsi/runs/wave-20260930-1121pdt/ddes/PREREG_DDESREPAIR2.md
  (committed alone; verified strict ancestor of the implementation commit
  via `git merge-base --is-ancestor d31e901b0 b42b10db5`: OK).
- Implementation: commit b42b10db5, file
  docs/lab/rsi/runs/wave-20260930-1121pdt/ddes/ddesr2.zag plus committed
  evidence run1.txt/run2.txt/run3.txt and binary ddesr2_bin.
- Zero-regression reference: docs/lab/research-lead/overnight-20260928/ddes/DDES_RAW.txt
  (frozen 56db8d606 A-E run output).

## Independent reproduction (this lane, pure safebin)

- Recompiled ddesr2.zag with pinned znc (safebin, `--no-zagd`): exit 0,
  zero stderr bytes. Binary at
  docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_r2_verify/ddesr2_verify_bin.
- Ran the rebuilt binary 3x: vrun1.txt, vrun2.txt, vrun3.txt.
  - sha256 of all three: 50a990d33f5074b05d0bb6c56a0f54fb6f58175f7266011e4a95f57f2fd33ae4
  - Identical to committed run1.txt/run2.txt/run3.txt (same hash; cmp confirms).
  - Exit 0 on all three runs; zero stderr bytes on all three (vrun1.err,
    vrun2.err, vrun3.err all 0 bytes).

## Per-bar verdicts

### K-R2.1 (t*=0 condition detected and flagged): CONFIRMED

- Both World F config traces contain the exact line
  `FLAG TSTAR-ZERO-BOUNDARY floor=1` (byte-checked with od: plain ASCII,
  no stray bytes), at run1.txt lines 70 and 79.
- Each flag line sits directly between the TARGET line (t*=0) and the
  PLAN line (lines 69/70/71 and 78/79/80).
- Zero occurrences of the flag string anywhere in the Worlds A-E block.
- Kill conditions (flag absent on either config, or flag on A-E): not met.

### K-R2.2 (no silent wrong convergence on World F): CONFIRMED

- cfg0 (truth h0): TARGET V*=2 t*=0 schema=1; FLAG; PLAN [S,W,OY];
  EXEC real=1; PRED h0=1 h1=0; SURVIVE h0; ELIM h1; CONVERGE-OK.
- cfg1 (truth h1): TARGET V*=2 t*=0 schema=1; FLAG; PLAN [S,W,OY];
  EXEC real=0; PRED h0=1 h1=0; ELIM h0; SURVIVE h1; CONVERGE-OK.
- The surviving hypothesis matches truth on both configs. Both plans are
  exactly [S,W,OY] (one W tick; zero-wait plans absent).
- Whole run: CONVERGE-OK count = 10, CONVERGE-FAIL count = 0. No PLAN
  line in the file lacks a W tick before the observation action.
- Kill conditions (true hypothesis eliminated, failed convergence,
  zero-W plan): not met.

### K-R2.3 (zero regression on A-E): CONFIRMED

- The Worlds A-E trace block (every line before `WORLD F` in run1.txt)
  is byte-identical to DDES_RAW.txt's trace lines (cmp on the 1062-byte
  prefix; diff empty). The only delta against the whole DDES_RAW.txt file
  is its own terminal line `SUMMARY ok=9/9 plans_built=8`, which belongs
  to the older 9-run binary and cannot appear mid-file in an 11-run; the
  prereg's own counter language (plans_built=10, SUMMARY ok=11/11 for the
  full run) requires exactly this comparison.
- candidates_built reads 8 on the D cfg1 PLAN line (after the E section),
  9 and 10 on the two F configs; SUMMARY ok=11/11 plans_built=10.
- Kill conditions (byte difference in A-E block, counter mismatch): not met.

### K-R2.4 (determinism): CONFIRMED

- Independent 3/3 byte-identical runs (sha256 match above), exit 0,
  zero stderr bytes on every run. The independent runs also reproduce the
  committed evidence byte-for-byte.
- Kill conditions (divergence, nonzero exit, stderr bytes): not met.

### K-R2.5 (purity): CONFIRMED, with one recorded caveat

- This lane: safebin only. NAMECHECK.md Step 0 records `command -v
  python3` and `command -v python` both empty; no Python was invoked or
  needed at any stage (compile via znc, runs, sha256/cmp/diff/grep/od/awk
  all from the safebin).
- Builder's NAMECHECK attests zero Python invocations at implementation,
  build, and run stages (python3 was present in their PATH but never
  invoked). Independent corroboration: the committed evidence is
  reproduced byte-for-byte from the Zag source using a PATH in which
  Python cannot resolve, so the full evidence chain is regenerable with
  zero Python involvement.
- check_no_dash.sh on all committed ddes/ files (ddesr2.zag, run1-3.txt,
  NAMECHECK.md, PREREG_DDESREPAIR2.md): exit 0, zero em-dash/en-dash bytes.
- Kill conditions (any Python use, any forbidden byte): not met.

### K-R2.6 (no new enumeration): CONFIRMED

- Diff of ddesr2.zag against the frozen BUILD-PASS source ddes.zag @
  56db8d606 shows exactly the prereg-specified changes and nothing else:
  the eff_waits(t*) clamp, the synthesize_plan wait bound cur_t < w with
  w = eff_waits(t*), the predict threshold arrival <= w, the t*=0 flag
  emission guarded only by `best_t==0` on the derived target (not on any
  delay value, variable id, or world id), plus the World F test-harness
  data table and its driver block.
- The synthesis path still assembles exactly one plan per config
  (candidates_built increments by 1, total 10 across 10 plans); no
  candidate-generating loop, no length constant (wait count derived from
  t*), no comparison between assembled plans. The frontier comparison
  operates on arrival-time arrays, and the p0==p1 check operates on
  predictor outputs, not on assembled plans.
- No new dedicated semantic case was added; the clamp and flag are
  generic boundary conditions on the derived target t*, of the kind the
  prereg explicitly likens to the existing null-schema fallback.
- Kill conditions (candidate-generating loop, length constant,
  comparison between assembled plans): not met.

## Overall

All six kill bars K-R2.1..K-R2.6 CONFIRMED by independent reproduction
and independent static audit. No bar failed. No protected-core change,
no new dedicated semantic case, no bar weakened.

Recommendation to the coordinator: the "DDES R2 PROVISIONAL" status from
the 11:21 M4 verdict can be lifted; DDES R2 (REPAIR-PASS on the frozen
bars) is confirmed as independently verified evidence.

## Evidence paths (this lane)

- docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_r2_verify/NAMECHECK.md
- docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_r2_verify/build_verify.err
- docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_r2_verify/ddesr2_verify_bin
- docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_r2_verify/vrun1.txt (plus vrun1.err, vrun2.txt, vrun2.err, vrun3.txt, vrun3.err)
- docs/lab/rsi/runs/wave-20260930-2021pdt/ddes_r2_verify/LANE_RESULT.md (this file)

## Blockers

None. Lane completed without invoking any forbidden executable; no
PROCESS-FAIL condition triggered. No commits made (per task; the wave
coordinator commits at wave end).
