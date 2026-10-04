# DEVANG3 Implementation Report (wave-20261001-2321pdt)

## Binary
- SHA-256: `36f5047dd123a144569adaba5d7d86efcdf2126fa762790fe083ef620525151d`
- Built with pinned znc: `/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Flags: `--no-zagd --no-analyze --no-foreground-cache`
- Determinism: 3/3 byte-identical reruns confirmed (fama sha256 `206e5dfa84f9c70ccf2060a8084e3c258b82e46f2ccdbcaafd6d363866e9714b` x3; KR0: 3/3 exit 0, zero stderr).

## Change vs 2021pdt baseline
Exactly one cognition line changed in `seg_dp` (plus comment updates):
- `sc=-50+ilog(L+1)*5;` became `sc=-50-1*L;`
  (novel-segment length bonus flipped to a linear length penalty).
- The scoring comment block above `seg_dp` rewritten to document the fix.
- The file header comment updated to reference this wave's prereg.
- `seg_dp_raw` (C0 control), cold start, lexicon, grounding, negator/comparative
  detection, interpretation, and the sealed interface are byte-identical
  in behavior to the 2021pdt baseline.

## Line count vs governance cap
- Baseline (2021pdt devang3.zag): 1564 lines.
- This implementation: 1571 lines (+7: comment block rewrite and header).
- **Cognition lines (new/changed): 1** (the scoring line). Well under the <120 cap.

## Development results (Family A, `fama`)
- **K1**: 10/10 (need >= 8/10) PASS
- **K2-K7,K9**: 7/7 (need >= 4) PASS
- **K8**: PASS (learner 20/20 vs best control 17/20)
- **K_C0**: PASS (learner 20/20 vs C0 13/20 = 35pp; K1 10 vs 3 = 7 words)
- **K_ABL-A** (dev analog): PASS (ablation K1 8/10 < learner 10/10, degrades)
- **DEV-PASS** (all Family A dev bars)

## Regression results (2021pdt sealed worlds, not kill bars)
- Family B: 12/12 (was 8/12). All four previously failing probes fixed,
  no regressions on the eight that passed.
- Family C (`sealc-fresh`, learner): 11/20 (was 11/20). No regression.

## Tuning notes (pre-prereg, /tmp only; not in lane)
- The linear penalty (`-50-1*L`) was selected over the length bonus after
  hand-arithmetic on the four failing probes showed the bonus had the wrong
  sign. Verified: K1 10/10, old-B 12/12 on a /tmp copy before the prereg
  was frozen.
- A quadratic-penalty tie-break variant was tried and dropped (no dev
  benefit, added complexity).
- Single-char cold start was tried and dropped (whole-utterance merges;
  the 3-char cold start is the load-bearing bootstrap).
- Dev Family C probes (builder-designed, 3-6 char words): 15/20 (mixed),
  19/20 (3-char only), 19/20 (3-char + 4-char fixed-position). The fresh
  sealed Family C uses 3-char content words plus 4-char negator/comparative
  in fixed positions.

## Files in lane
- `devang3.zag`: implementation (1571 lines)
- `devang3`: built binary (sha256 above)
- `PREREG_DEVANG3.md`: frozen prereg (committed alone at 5b7e55706)
- `NAMECHECK.md`: governance steps
- `sealed/genB.zag`, `sealed/genC.zag`: fresh sealed generators (pure Zag)
- `sealed/sealed_b.txt`, `sealed/sealed_b_key.txt`: fresh Family B
- `sealed/sealed_c.txt`: fresh Family C
- `SEALED_B.md`, `SEALED_C.md`: sealed notes with pre-run sha256
- `dev_fama.log`, `dev_fama.err`: dev test logs
- `IMPLEMENTATION.md`: this file
- `BUILD-LOG.md`: build history
