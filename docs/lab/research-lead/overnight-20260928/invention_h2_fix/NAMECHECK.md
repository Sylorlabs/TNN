# NAMECHECK.md -- Invention H2 Overflow Fix Worker

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
`guard-check-done`). Safebin contains 42 symlinked tools (coreutils, git,
pinned znc); `python3`/`python` do not resolve in this worker's PATH.

Toolchain in use for all build/run/verify steps: `~/safebin/znc` (pinned
znc), `~/safebin/sh`, `~/safebin/git`, `~/safebin/sha256sum`,
`~/safebin/cmp`, plus other safebin coreutils only.

Guard status: PASS. No forbidden executable invoked. Pure Zag for all
research logic (mechanism, fix, driver, builds, runs).

## Step 1: Source provenance

- `h2f_base.zag`: byte-identical copy of the red-team's `rt_base.zag`
  (SHA-256 dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  matches the H2 worker's recorded base hash and the red-team REPORT.md).
  Frozen mechanism base; NOT modified.
- `h2f_driver.zag`: byte-identical copy of the red-team's `rt_driver.zag`
  (SHA-256 41f8967a6f77f9b9cfe99cbfbcd5d5451102bead1a0ba02c287d0c3f83dc34a8).
  Adversarial battery unchanged; NOT modified.
- `h2f_patch.zag`: copy of the red-team's `rt_patch.zag` (frag_on=1) with
  ONLY the candidate-buffer general-bound fix applied (see REPORT.md for
  the bound proof). No search-order, cap, or depth change.
- `h2f_patch_nc.zag`: same fix with the one-line frag_on=0 diff, mirroring
  the red-team's rt_patch vs rt_patch_nc relationship.

## Step 2: Build and run record

- `h2f_full.zag` = h2f_base + h2f_patch + h2f_driver (concatenation, same
  order as the red-team's rt_full.zag).
- `h2f_full_nc.zag` = h2f_base + h2f_patch_nc + h2f_driver.
- `znc h2f_full.zag -o h2f_bin`; `znc h2f_full_nc.zag -o h2f_nc_bin`.
- Each binary run 3x; byte-identical outputs verified with sha256sum/cmp.
- Run outputs: `h2f_run1.txt`, `h2f_run2.txt`, `h2f_run3.txt`,
  `h2f_nc_run1.txt`, `h2f_nc_run2.txt`, `h2f_nc_run3.txt`.

## Step 3: Kill-bar discipline

No red-team kill bar was weakened. The A4 KILL is addressed by fixing the
memory-safety defect it exposed (undersized candidate buffer), not by
changing what counts as a pass. A1/A2/A3/A4c verdicts are re-checked
against the fixed binaries without moving their bars; A1's verifier
limitation is documented as OPEN (see REPORT.md), not patched around.
