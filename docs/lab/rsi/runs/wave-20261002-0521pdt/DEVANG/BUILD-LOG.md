# BUILD-LOG.md: DEVANG5 file creation order (wave-20261002-0521pdt)

Commit-order self-check: the prereg's first commit (6e787022b) strictly
precedes every implementation commit below. The Family E baseline
measurement used the frozen DEVANG4 binary only.

## Order of creation

1. `NAMECHECK.md` (Step 0 toolchain guard; safebin, no python3).
2. `PREREG_DEVANG5.md` (frozen). Committed ALONE as 6e787022b.
3. `baseline/familye_eps.txt` (six Family E lines, copied verbatim
   from the frozen prereg section 5, plus `0 6` header).
4. `baseline/baseE_run{1,2,3}.log/.err` (frozen devang4 binary,
   sha256 verified `cfba24f1...`, `segb-scene`, 3/3 runs).
   Result: 2/6 (E2, E6 correct). Premise (<= 2/6) HOLDS.
   Note: hand arithmetic predicted 0/6; the measured 2/6 is the
   governing number. The deviation is documented, not explained
   away; POSSEG's prediction (6/6) is tested by implementation.
5. `devang5.zag` (copied from devang4.zag, then minimal FINREG
   delta via surgical edits; no Python at any step).
6. `devang5` (compiled with pinned znc; `devang5_compile.err`
   holds only pre-existing style warnings).
7. `dev_fama.log` / `dev_fama.err` (Family A dev run, exit 0,
   zero stderr; numbers identical to DEVANG4 dev output).
8. Family D dev diagnostic (throwaway, /tmp): devang5
   `segb-scene` on the 0221pdt Family D episodes: 6/6
   (devang4: 2/6). Mechanism behaves as designed. No design or
   code change was made in response to any Family E observation;
   Family D is a superseded diagnostic, not sealed.
9. `genseal5.zag` (implements exactly PREREG_DEVANG5.md section 8;
   scene generators copied verbatim from genseal4.zag).
10. `genseal5` (compiled with pinned znc).
11. Generator validation with ALTERED seeds (888011/888012) into
    /tmp (format checks, spec-compliance checks, solvability smoke
    test: devang5 `segb` 12/12 on throwaway B; `sealc-fresh`
    learner runs clean on throwaway C). Throwaway output
    discarded. One spec-compliance note: my first-draft
    gen_neg/gen_rel/gen_size differed from genseal4's; replaced
    with verbatim copies before the frozen-seed run (spec
    compliance fix, not a spec change).
12. `sealed5/` (frozen-seed run, once): `sealed_b5.txt`,
    `sealed_b5_key.txt`, `sealed_c5.txt`, `SHA256SUMS`, plus a
    copy of the `genseal5` binary used. Builder never read sealed
    contents or keys (line counts and sizes only).
13. `scoree.zag` (mechanical scorer: clone of scoreb.zag printing
    only `E: x/y`; per prereg section 9).

## Prereg errata (transparent, no bar changes)

- E1: prereg section 8 says "12 fresh words" for C-doubleprime but
  lists 11 with frozen roles (zek, nubo, zok, wimi, ix, dox, plub,
  sliq, gabo, imlau, gabexu). The explicit list governs;
  implemented as listed. No kill bar is affected.

## Sealed runs (to be appended)

(pending)
