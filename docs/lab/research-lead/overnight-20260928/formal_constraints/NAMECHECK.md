# NAMECHECK: formal_constraints (Learner-Built Constraint Channel)

Worker: Formal Constraints Auto-Applied Worker (fresh respawn, 2026-10-02).
Repo: ~/workspace/tnn-rsi, branch tnn-native-lab. Local only, never pushed.

## Step 0: toolchain guard (mandatory, recorded)

Commands run at session start:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned EMPTY (no output before
"guard-check-done"). PATH=/home/hatch/safebin with 49 linked tools.
No forbidden executable exists in the worker PATH.
No python, python3, or any other interpreter was invoked at any point
in this session. All computation: pinned znc plus POSIX shell tools
(grep, awk, cmp, sha256sum).

Pinned compiler: $HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
(znc 2026.07.0-dev, edition 2026).

## Step 1: prereg commit-order self-check

- Commit 0cf6fe35f froze PREREG.md ALONE (no source, no binary).
- Implementation (fc_main.zag) and this run/report commit come AFTER.
- The prereg's first commit strictly precedes the implementation's
  commit. Self-check: PASS.
- PREREG.md was not modified after freezing (it is byte-identical to
  the committed version; verified by git status showing no
  modification).

## Step 2: binary provenance

- fc_main.zag: 547 lines, pure Zag, one `fn main(` entry point
  (dup check in fc_build.sh confirms exactly 1).
- fc_bin built from the current fc_main.zag via fc_build.sh
  (sh + pinned znc only) at 2026-10-02 17:41 UTC.
- STALE-BINARY INCIDENT (process note): the fc_bin found in the
  directory at session start (timestamp 16:21:53 UTC) was compiled
  BEFORE the final fc_main.zag edit (source timestamp 16:22:50 UTC)
  and produced different output (Arm L found=0, fidelity_L=304/468).
  It was never committed and never reported. The source was
  recompiled in place; the stale binary was overwritten. All results
  in this report come from the rebuilt binary.

## Step 3: determinism (K1)

Three runs of fc_bin, outputs fc_run1.txt / fc_run2.txt / fc_run3.txt:
- run1 sha256: 496b61cce575e22656eab108a2b837ceb15be13e3b58670d1a4c6dbd40699f10
- run2 sha256: 496b61cce575e22656eab108a2b837ceb15be13e3b58670d1a4c6dbd40699f10
- run3 sha256: 496b61cce575e22656eab108a2b837ceb15be13e3b58670d1a4c6dbd40699f10
- cmp confirms 3/3 byte-identical. K1: PASS.

## Step 4: no-wire audit (K6)

grep over the 128-line learner-induction source section
(extracted between "SECTION: learner constraint induction" and
"SECTION: researcher channel") for:
grammar|codec|decode|divisor|sentence|wellformed|pair|literal|D0
Result: ZERO matches. K6: PASS.
The induction section uses only generic vocabulary
(field, feature, div, mod, range, accept, reject, clause).

## Step 5: purity

- Source is pure Zag; build is sh + znc; analysis is grep/awk/cmp/sha256sum.
- Zero Python invocations in this session (guard verified at start;
  no interpreter calls after).
- K7: PASS.

## Step 6: governance constraints

- 0 modes/bridges/handlers in the learner path. The arm flag
  (0/1/2) is a harness condition selector, not a learner mode; the
  learner (induction + registry content) is identical in all arms.
- Paper untouched. Nothing pushed (commits local only).
- No em/en dashes in any deliverable doc of this lane.
