# NAMECHECK: COGOPS-STRATEGY

Worker: COGOPS-STRATEGY. Date: 2026-10-03.
Lane: `docs/lab/research-lead/overnight-20260928/cogops_strategy/`

## Step 0: toolchain guard (worker startup)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`:
  NOT FOUND in this checkout (same finding as the COGOPS-DETECTION
  worker). Fallback: `$HOME/safebin` exists directly.
- `export PATH="$HOME/safebin"` before every command.
- `$HOME/safebin` verified directly: 49 entries, no `python3`, no
  `python`. `which python3` and `which python` return nothing before
  and after every build/run.
- Pinned znc: `$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
  (2026.07.0-dev), the single compiler for the one build.
- All computation pure Zag. Shell only for: znc invocation, running
  the binary, git operations, file assembly (cat/cmp/grep), and
  byte-verification (sha256sum, cmp). Zero forbidden-executable
  invocations.
- New Zag scanned for the `while.*!(` negated-conjunction pattern:
  clean. if-nesting kept at 3 or fewer with hoisted flags per the
  znc defect notes in AGENTS.md.
- Git writes via `/usr/bin/git` absolute path (safebin git symlink
  EPERM workaround), explicit pathspecs, current branch only,
  nothing pushed.

## Step 1: lane isolation

- Lane directory: `docs/lab/research-lead/overnight-20260928/cogops_strategy/`
- Builds on COGOPS-DETECTION (`../cogops_detection/`): c10_base.zag
  is cmp-identical to c9_base.zag; c10_learn.zag lines 1..1331 are
  cmp-identical to c9_learn.zag lines 1..1331 (the frozen c8 prefix);
  the additive section is new (strategy layer). No frozen function
  modified.
