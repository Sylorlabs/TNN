# NAMECHECK: DDES steps 4+5 (independent reproduction from committed source + simple-baseline comparison)

Wave: wave-20261002-0221pdt. Lane: DDES.
Lane dir: docs/lab/rsi/runs/wave-20261002-0221pdt/DDES/
Worker: research worker (depth 2/2), no child subagents spawned.

## Step 0: toolchain guard (recorded before any other work)

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh:
  SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
- Exported PATH="$HOME/safebin" for all subsequent work.
- `which python3` returns nothing (exit 1); `which python` returns nothing.
- `which znc` resolves to /home/hatch/safebin/znc (pinned znc,
  Linux x86_64 build abed8aa1, znc 2026.07.0-dev edition 2026).
- Guard check result: PYTHON3_NOT_FOUND (pass), PYTHON_NOT_FOUND
  (pass). Pure-Zag constraint acknowledged: any forbidden-executable
  invocation makes this wave PROCESS-FAIL and must be disclosed
  immediately.

## Provenance finding (recorded before prereg)

The committed DDESv2 lane sources live at commit 947675258
(wave-20261001-1721pdt wave record). The later commit
f461e812d (wave-20261001-2321pdt H5R2-SKEPTIC2 implementation)
deleted the entire DDESv2 lane from the committed tree (mass
deletion, flagged in that wave's GIT-HEALTH commit). The
working-copy dir docs/lab/rsi/runs/wave-20261001-1721pdt/DDESv2/
is untracked and its five .zag sources sha256-match the
947675258 blobs exactly. This lane therefore extracts build
sources via `git show 947675258:...` into its own lane dir,
verifies sha256 against the pinned values in the prereg, and
builds from those extracted copies only.

## Lane plan

1. PREREG_DDES_REPRO.md (frozen kill bars, pinned source hashes,
   expected transcript hashes, baseline spec) committed ALONE
   before any rebuild.
2. Extract the five committed .zag sources from 947675258;
   sha256-verify against prereg pins; stop on any mismatch.
3. Build all five binaries with pinned znc (plain build, no
   instrumentation); record build stderr.
4. Run each binary 3/3; sha256-compare transcripts against the
   frozen record; re-verify K-R1 through K-R9 from the rebuilt
   runs. Any byte or verdict divergence = REPRODUCTION-FAIL:
   stop, report the diff, do not patch forward.
5. Implement the frozen simple baseline (ddes_randbase.zag) per
   the prereg spec; run; write BASELINE_COMPARISON.md with
   per-world numbers and a self-red-team on the binding caveats.
6. Verdict line (BUILD-PASS/BUILD-FAIL on reproduction only)
   with the three caveats restated verbatim; report back.
