# NAMECHECK.md -- Invention H2 Red-Team Worker

## Step 0: Toolchain guard (mandatory)

Executed at startup (2026-10-02, before any research command):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed nothing; `guard-check-done` printed.
`PATH=/home/hatch/safebin` for every subsequent command in this task.
Zero forbidden executables invoked. All computation in pure Zag; all shell
use limited to file assembly, builds, runs, and text inspection.
Pinned compiler for builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.

## Step 1: Identity

Worker: Invention Hypothesis 2 red team (fragment recombination).
Mission: independent adversarial attack on the H2 claim at commit
31391237a: sub-MAP fragment extraction plus constraint-satisfaction
recombination, novel 6-link form [1,1,1,2,2,2], strictly greater expressive
power than Composition C on the same goal, honest L2 bound.
Method: design a fresh adversarial battery (6 arms), build two binaries
from the H2 mechanism (frag_on=1) and its whole-MAP-only control
(frag_on=0, one-line diff), run each 3x byte-identical, report
KILL / BOUND / SURVIVE per attack. Genuine adversary: attacks were designed
to break the claims, and one attack (A5) was designed to confirm a claimed
limitation could be closed.

## Step 2: Base

Unfrozen work only. Frozen TNN-2 core read-only, never modified.
- `rt_base.zag`: byte-identical copy of
  `invention_recombine/ir_base.zag` (SHA-256
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6,
  verified after copy).
- `rt_patch.zag`: byte-identical copy of
  `invention_recombine/ir_patch.zag` (the H2 mechanism, frag_on=1).
- `rt_patch_nc.zag`: one-line diff of rt_patch.zag (frag_on 1 -> 0);
  verified by diff, exactly one line differs.
- `rt_driver.zag`: red-team battery (new file, ~350 lines, test code only).
- `rt_full.zag` = rt_base + rt_patch + rt_driver.
  `rt_full_nc.zag` = rt_base + rt_patch_nc + rt_driver.
- `rt_bin` / `rt_nc_bin`: pinned znc builds (warnings only, build clean).
- `rt_run1/2/3.txt`: 3/3 byte-identical (frag binary exits 1: deterministic
  A4 panic, see REPORT.md). `rt_nc_run1/2/3.txt`: 3/3 byte-identical,
  exit 0.

## Step 3: Outputs

- `rt_driver.zag`: six attack arms (A1/A2/A3/A5/A4c/A4).
- `rt_bin`, `rt_nc_bin`: compiled adversaries.
- `rt_run1/2/3.txt`, `rt_nc_run1/2/3.txt`: transcripts.
- `REPORT.md`: per-attack verdicts with evidence.
- This file.

Pure Zag. No em dashes or en dashes in loop documentation. Paper untouched.
Nothing pushed. 0 modes / 0 bridges / 0 handlers / 0 new semantic cases.
Red-team driver adds test code only; the mechanism under attack is
unmodified from commit 31391237a.
