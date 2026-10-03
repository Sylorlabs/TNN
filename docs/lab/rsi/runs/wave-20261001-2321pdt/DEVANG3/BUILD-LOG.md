# DEVANG3 Build Log (wave-20261001-2321pdt)

## File creation order
1. `NAMECHECK.md`: Step 0 (safebin, toolchain verification).
2. `PREREG_DEVANG3.md`: frozen prereg. Committed ALONE at 5b7e55706.
3. `devang3.zag`: copied from 2021pdt baseline (1564 lines); one scoring
   line changed (`sc=-50+ilog(L+1)*5;` to `sc=-50-1*L;`); scoring comment
   block and header comment updated.
4. `devang3`: built binary via pinned znc (sha256
   36f5047dd123a144569adaba5d7d86efcdf2126fa762790fe083ef620525151d).
5. `dev_fama.log`, `dev_fama.err`: Family A dev test logs.
6. `IMPLEMENTATION.md`: implementation report.
7. `sealed/genB.zag`, `sealed/genC.zag`: fresh sealed generators.
8. `sealed/genB`, `sealed/genC`: compiled generator binaries.
9. `sealed/sealed_b.txt`, `sealed/sealed_b_key.txt`, `sealed/sealed_c.txt`:
   fresh sealed files (generated blind; contents not inspected).
10. `SEALED_B.md`, `SEALED_C.md`: sealed notes with pre-run sha256.
11. `BUILD-LOG.md`: this file.

## Implementation edit history
1. Copied 2021pdt `devang3.zag` (1564 lines, unedited).
2. Line 389 (`seg_dp`, learner only): `sc=-50+ilog(L+1)*5;` replaced with
   `sc=-50-1*L; // linear novel-length PENALTY (was bonus);
   wave-20261001-2321pdt fix`.
3. Rewrote the scoring comment block above `seg_dp` (documents the sign
   flip and why).
4. Updated the file header comment (prereg reference for this wave).
5. No other lines touched. `seg_dp_raw` (C0), cold start, lexicon,
   grounding, detection, interpretation, sealed interface unchanged.

## Pre-prereg tuning (all in /tmp, not in lane)
- /tmp/tune1.zag: linear penalty k=1. K1 10/10, old sealed_B 12/12,
  old sealed_C 11/20 (no regression), dev Family A DEV-PASS.
- /tmp/tune2.zag: single-char cold start. FAILED (whole-utterance merges
  in lexicon). Dropped.
- /tmp/tune4.zag: quadratic tie-break. No dev benefit. Dropped.
- /tmp/dev_genC*.zag: dev Family C probes. 15/20 (3-6 char), 19/20
  (3-char only), 19/20 (3-char + 4-char fixed-position negator/comparative).
  Informed the fresh sealed Family C design (3-char content, 4-char
  negator/comparative in fixed positions).

## Toolchain notes
- Pinned znc: `/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Safebin active; `which python3` returns nothing (verified Step 0).
- No forbidden executable invoked at any stage.

## Test results summary (dev)
- Fama: DEV-PASS (K1 10/10, K8 pass, K_C0 pass, 7/7 sub-bars).
- Determinism: 3/3 byte-identical fama outputs.
- Regression old-B: 12/12. Regression old-C: 11/20.
