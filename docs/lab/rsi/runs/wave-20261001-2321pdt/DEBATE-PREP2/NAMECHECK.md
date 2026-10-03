# NAMECHECK.md - DEBATE-PREP2 worker, wave-20261001-2321pdt

## Step 0: Toolchain verification (worker toolchain guard, 2026-09-30)

- Safebin setup script: `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Script output: `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- PATH set to: `/home/hatch/safebin`
- `which python3` output: (nothing; exit code 1) - python3 does NOT resolve in worker PATH
- Script self-verify lines: "verify: python3 absent from safebin PATH (OK)", "verify: python absent from safebin PATH (OK)"
- znc: OK (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`)
- Documentation lane: no experiments, no Python, no Zag invocation. Shell and git/file ops only.
- Working copy: `~/workspace/tnn-rsi`, branch `tnn-native-lab`. No push. Commits local only under `docs/lab/rsi/runs/wave-20261001-2321pdt/DEBATE-PREP2/` via explicit pathspec.
- Read-only toward DEBATE-SLATE/, DEBATE-PREP/, and synthesis dirs.
