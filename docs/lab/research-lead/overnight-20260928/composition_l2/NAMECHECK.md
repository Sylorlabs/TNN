# NAMECHECK: Composition L2 Adaptive Worker

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, 2026-10-02:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed NOTHING; only `guard-check-done`.
No forbidden executable is reachable in this worker's PATH.

Continuation worker re-verification (2026-10-02): the guard block above
was re-executed at continuation startup; `which python3 python` again
printed nothing, only `guard-check-done`. Safebin znc sha256 still
matches the pinned compiler
(498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
All continuation computation is pure Zag; shell used only to invoke
znc, run binaries, and do git/file operations.

Compiler check: `sha256sum` of `$HOME/safebin/znc` equals the sha256 of
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
The safebin znc IS the pinned compiler.

All research computation below is pure Zag. Shell is used only to invoke znc,
run binaries, and do git/file operations.

## Step 1: Preregistration

PREREG.md (frozen kill bars K1-K12) is committed BEFORE any implementation.
Commit order is verified below.

## Step 2: Implementation record

- `l2_patch.zag`: variant of `composition_unified/un_patch.zag` with MAP
  adaptation operators (EXTEND / TRUNCATE / SPECIALIZE), variant candidate
  codes, `un_satisfy_v` dispatch, ADAPT-STAT emission.
- `l2_driver.zag`: adapt-on battery (L1 regression, L2 extend, truncate,
  specialize, ablations, fresh controls, reuse, provenance).
- `l2_driver_na.zag`: adapt-off control driver (NOADAPT arms only).
- `l2_full.zag` = `composition_C/cc_base.zag` + `l2_patch.zag` +
  `l2_driver.zag`. `l2_full_na.zag` = cc_base + `l2_patch_na.zag` +
  `l2_driver_na.zag` (`l2_patch_na.zag` differs by exactly one line:
  `adapt_on()` returns 0).

### Step 2b: Continuation fixes (2026-10-02, post-prereg, implementation only)

The first-pass build failed every arm vacuously (all ans=-2, zero MAPs
promoted). Root causes found by the continuation worker:

1. Both drivers never called `tnn2_init` on their `z_alloc` workspaces
   (the frozen baseline driver does). Added `tnn2_init(wN)` after each
   alloc in `l2_driver.zag` and `l2_driver_na.zag`. This alone took the
   battery from 0/14 to 14/14 arms passing.
2. `cand_ins` tie-break was reverse MAP-id (newcomer before equals),
   contradicting the PREREG's "ties stable by MAP id" and the frozen
   baseline's insertion. Fixed to stable (newcomer after equals, ascending
   MAP id on ties).

Neither fix touches the frozen hypothesis, battery spec, or kill bars.
`l2_patch_na.zag` regenerated from `l2_patch.zag` by one-line sed
(verified: diff shows exactly the `adapt_on` line). Both full sources
reassembled by concatenation and rebuilt with the pinned safebin znc.

## Step 3: Determinism

Each binary is run 3 times; stdout sha256 digests must match byte for byte.
Run outputs are stored as `l2_run1.txt` .. `l2_run3.txt` and
`l2_na_run1.txt` .. `l2_na_run3.txt`.

Continuation results: `l2_bin` 3/3 byte-identical
(529e0e7debca4ec0bb2670ad44aa161c6954fb01121d07e6c8caeff97ecc9426);
`l2_na_bin` 3/3 byte-identical
(aabe551df8dee2451750e867e85dc3276814b0fdc0122102787ec58c78ec1d1c).

## Step 4: Verdict

Recorded in REPORT.md after the frozen bars are checked against the runs.
Continuation verdict: COMPOSITION-L2-COMPLETE, 12/12 frozen kill bars pass,
per-operator success rates recorded in REPORT.md.
