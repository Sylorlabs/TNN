# NAMECHECK.md - L3 Transfer Worker

## Step 0: Toolchain guard (2026-10-02, before any work)

- Built `$HOME/safebin` with the 36 allowed tools (git, znc, sh, bash, ls,
  cp, mv, rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum,
  git-receive-pack, git-upload-pack).
- `export PATH="$HOME/safebin"` active for every command in this session.
- `which python3 python` returns nothing. Zero forbidden executables.
- Record: PASS. No forbidden interpreter was invoked at any point.

## Provenance

- Worker: L3 Transfer Worker (subagent, depth 2/2), spawned 2026-10-02
  10:57:41 PDT by the parent orchestrator.
- Repo: `~/workspace/tnn-rsi`, branch `tnn-native-lab`.
- Deliverables: `docs/lab/research-lead/overnight-20260928/l3_transfer/`.

## What was built

1. `PREREG.md` - frozen kill bars T1-T8, falsifiers, audit list.
   Committed ALONE as `abcb1e53d` before any implementation existed.
2. `learner.zag` - generic X/Y/M machinery plus the learner-owned
   intermediate library (lib_store, lib_probe, lib_reuse, lib_adapt).
3. `driver.zag` - frozen world tables, three arms, in-binary assertions.
4. `build.sh`, `full.zag`, `l3t_bin`, `compile.log`.
5. `run1.txt`, `run2.txt`, `run3.txt` - 3/3 byte-identical, ALL PASS.
6. `REPORT.md` - results against the frozen bars.

## Constraints honored

- Pure Zag for all research logic. Shell used only to invoke znc, run
  the binary, and do git/file operations.
- Prereg committed before implementation; two transparent amendments
  (AMEND-1, AMEND-2) recorded in PREREG.md before the frozen runs.
- 0 modes, 0 bridges, 0 handlers, 0 new semantic cases (frozen grep
  audit: all patterns 0).
- Zero em/en dashes in loop documentation (byte verified).
- Paper untouched. Commits local only, nothing pushed.
- Commit uses explicit pathspecs.
