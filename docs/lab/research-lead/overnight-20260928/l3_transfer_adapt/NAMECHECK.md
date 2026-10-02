# NAMECHECK.md - L3 Transfer-Adapt Worker

## Step 0: Toolchain guard (2026-10-02, before any work)

- Built `$HOME/safebin` with the allowed tools (git, znc, sh, bash, ls,
  cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum,
  git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` active for every command in this session.
- `which python3 python` returns nothing under the safebin PATH.
  Zero forbidden executables. Record: PASS.
- No forbidden interpreter was invoked at any point in this session.

## Provenance

- Worker: L3 Transfer-Adapt Worker (subagent, depth 2/2), spawned
  2026-10-02 by the parent orchestrator.
- Repo: `~/workspace/tnn-rsi`, branch `tnn-native-lab`.
- Deliverables:
  `docs/lab/research-lead/overnight-20260928/l3_transfer_adapt/`.

## What was built

1. `PREREG.md` - frozen kill bars T1-T8, falsifiers, audit list.
   Committed ALONE before any implementation existed.
2. `learner.zag` - generic X/Y/M machinery, learner-owned intermediate
   library with provenance (parent entry, parent op), and the generic
   L2 adaptation operators EXTEND, TRUNCATE, SPECIALIZE plus the
   lib_adapt transfer policy (exact probe, adaptation scan, else fresh
   construction).
3. `driver.zag` - frozen world tables (FORAGE, RELAY reused from
   l3_transfer; AEGIS new), three arms, in-binary assertions, and
   driver-side exhaustive uniqueness audits of the adaptation
   neighborhoods.
4. `build.sh`, `full.zag`, `l3a_bin`, `compile.log`.
5. `run1.txt`, `run2.txt`, `run3.txt` - 3/3 byte-identical, ALL PASS.
6. `REPORT.md` - results against the frozen bars.

## Constraints honored

- Pure Zag for all research logic. Shell used only to invoke znc, run
  the binary, and do git/file operations.
- Prereg committed before implementation; no amendments were needed.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases (frozen grep
  audit: all patterns 0).
- Zero em/en dashes in loop documentation (byte verified).
- Paper untouched. Commits local only, nothing pushed.
- Every git add and git commit uses explicit pathspecs.
