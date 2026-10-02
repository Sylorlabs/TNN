# NAMECHECK: CONTLEARN-REDTEAM (independent second opinion)

## Step 0: Toolchain verification (worker toolchain guard)

- Activated: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` then `export PATH="$HOME/safebin"`.
- Safebin output: 36 tools linked, `znc: OK`, `python3 absent from safebin PATH (OK)`, `python absent from safebin PATH (OK)`, `SAFEBIN-READY`.
- Verification: `which python3` returned nothing (exit 1) after PATH export.
- Role: INDEPENDENT RED-TEAM REVIEWER of lane CONTLEARN verdict, wave-20261001-2021pdt. Independent of the CONTLEARN and CONTLEARN-IMPL workers. Read-only analysis of committed files; may re-run committed `cl_driver` binary read-only for determinism spot checks. No new implementation, no forbidden executables.

## Step 1: Identity
- Tasked by parent orchestrator as skeptical second opinion on the INTEGRATION-DEMONSTRATED verdict.
- Bound claim under review: on a fixed 149-event 6-phase script, the frozen TNN-2 core showed REUSE_COUNT 30/30 (floor 20), R1c 6, R2c 3, R3c 3, R4c 12, R5c 6; K4 0 missing edges; K5 controls equal with C-P6 0/18; K6 3/3 identical. Claimed bound: >= 20 white-box cross-phase citations on this fixed script; no L3, no generality.

## Step 2: Output discipline
- Writes confined to `docs/lab/rsi/runs/wave-20261001-2021pdt/CONTLEARN/`: new files only (`NAMECHECK_REDTEAM.md`, `REDTEAM_REVIEW.md`). No commits (coordinator commits). No push. No `git reset --hard`. No rebase. No em-dashes in documentation.

## Step 3: Determinism probe results (read-only, completed)

- SHA-256 of committed artifacts matches DRIVER.md exactly: `cl_driver`
  `c8c089b8a0a25f9727719d386aad31fd584a171b3ccbe5ed3bc0b5a72c0e81b7`;
  `cl_driver.zag`
  `b7a1877eb64545b2490ad2ee50f0b818dfd8ff6ac08e6f84e00a00cd0d45a43a`;
  `cl_combined.zag`
  `4aba249d9ab81530d658fdf14c2b6ba43b83dd2386f8aa6f67b5accfef404d07`.
- Re-ran committed `cl_driver` read-only (`printf 'TREAT'` / `printf 'C-P6'`
  on stdin; the mode token must match stdin exactly with no trailing
  newline, else MODE_FAIL). Stdout hashes reproduce RUN_LOG.md: TREAT
  `53ff2c990e4f7f8d29c8b1bb809cf6616226b9f6bd3dd28d06210dc54446bc44`;
  C-P6 `218854b0cc91580580aafc86f404bcab6c5df8eba14ceca65ed00756251adc81`;
  zero stderr bytes. K6 independently reproduced.
- Transcript counts verified: 149 EV lines in TREAT; P4 section exactly 6
  events; oracle lines R1C 6, R2C 3, R3C 3, R4C 12, R5C 6, REUSE_COUNT 30
  present as reported.
