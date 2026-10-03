# NAMECHECK.md -- H2 Completeness Repair Worker

## Step 0: Worker toolchain guard (mandatory)

Executed at session start, before any research operation:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output before
`guard-check-done`). Safebin holds the allowed coreutils, git, and the
pinned znc; `python3`/`python` do not resolve in this worker's PATH.

Toolchain for all build/run/verify steps: `~/safebin/znc` (pinned znc
symlinking to the repo's `src/tools/toolchain/znc_linux_x86_64_abed8aa1`),
`~/safebin/sh`, `~/safebin/git`, `~/safebin/sha256sum`, plus other
safebin coreutils only. No other znc on PATH was used for builds.

Guard status: PASS. No forbidden executable invoked. Pure Zag for all
research logic (mechanism, repair, drivers, builds, runs).

Worker driver note (from AGENTS.md lesson, redteam2 H2/H3): MAPs are
taught via direct `t2_trial` calls in the B1 driver (identical MAP
inventory, no rebind assemblies); full ev_query is reserved for the
goal queries under test. The B1 driver is a byte-identical copy of
redteam2's, so this holds by inheritance.

## Step 1: Source provenance

- `h2c_base.zag`: byte-identical copy of the H2 mechanism base
  (SHA-256 dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  matches the fix report and redteam2 REPORT.md). Frozen base; NOT
  modified by this worker.
- `h2c_patch.zag`: copy of the fixer's `h2f_patch.zag` (SHA-256
  fe38482c187f0637930fcd29d57de5adb0da5ca479ada364bebef808fb7aac60
  before edit). UNFROZEN repair target: the ONLY file this worker
  edits. Edit scope (frozen by PREREG.md): `ir_frag_candidates`
  enumeration order only (flat (flen,map,start) -> banded round-robin);
  cap 48, depth 3, D*B buffer, satisfiability, used-exclusion, DFS,
  verifier all unchanged.
- `h2c_patch_nc.zag`: one-line frag_on=0 variant of the repaired patch
  (whole-MAP control), mirroring the fixer's patch/patch_nc pair.
- `h2c_driver.zag`: byte-identical copy of the fixer's `h2f_driver.zag`
  (SHA-256 41f8967a6f77f9b9cfe99cbfbcd5d5451102bead1a0ba02c287d0c3f83dc34a8).
  Fix battery A1/A2/A3/A5/A4c/A4; NOT modified.
- `h2c_stress_driver.zag`: byte-identical copy of the fixer's
  `h2f_stress_driver.zag` (SHA-256
  4a616682b761cbc8c38fb7d19ff593cec57f313a69b1c4c8757ea3b3414ccbba).
  100-fragment stress; NOT modified.
- `h2c_b1_driver.zag`: byte-identical copy of redteam2's
  `rt2_h2_driver.zag` (SHA-256
  3656a1fe228b6c04692e9807ee7531c2eb1c463b561b59c1ab5540d20b9f49ef).
  B1a/B1c/B2/B4 arms; NOT modified.

## Step 2: Build and run record

- `h2c_full.zag` = h2c_base + h2c_patch + h2c_driver.
- `h2c_full_nc.zag` = h2c_base + h2c_patch_nc + h2c_driver.
- `h2c_full_b1.zag` = h2c_base + h2c_patch + h2c_b1_driver.
- `h2c_stress_full.zag` = h2c_base + h2c_patch + h2c_stress_driver.
- `znc <full>.zag -o <bin>` with pinned znc; warnings only.
- Each binary run 3x; outputs compared with cmp/sha256sum (3/3
  byte-identical required).
- Run outputs: `h2c_run1/2/3.txt`, `h2c_nc_run1/2/3.txt`,
  `h2c_b1_run1/2/3.txt`, `h2c_stress_run1/2/3.txt`.

## Step 3: Kill-bar discipline

No red-team or fix kill bar was weakened. The B1 KILL is addressed by
repairing the enumeration unfairness it exposed (banded round-robin),
not by changing what counts as a pass. The prereg (PREREG.md) was
committed BEFORE any implementation edit; the implementation commit is
strictly later. A1/A2/A3/A4c/A5 verdicts are re-checked against the
repaired binaries without moving their bars. Per-loop governance: this
lane's prereg first-commit strictly precedes the implementation.
