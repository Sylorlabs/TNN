# NAMECHECK: DDES steps 7+8 (OOD test + ablation)

Wave: wave-20261002-0521pdt. Lane: DDES.
Lane dir: docs/lab/rsi/runs/wave-20261002-0521pdt/DDES/
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
- Pinned-znc code rule acknowledged: no `as *i32` + q[0..n] slice
  construction inside functions; u8-cell loop idiom with
  little-endian pack/unpack helpers (copied verbatim from the
  proven ddes_alt.zag utils).

## Lane plan

1. NAMECHECK.md (this file) committed alone.
2. PREREG_DDES78.md (frozen kill bars, six sealed OOD worlds, five
   ablation variants, full prediction tables) committed ALONE before
   any implementation exists.
3. Implement ddes_78.zag in pure Zag after the prereg commit:
   frozen DDES V2 derivation machinery (arrival computation,
   frontier scan, plan synthesis, predictor, sealed world
   simulator) plus the four controlled ablation variants.
4. Build with pinned znc (plain build, no instrumentation);
   record build stderr. Run 3/3; transcripts must be
   byte-identical, exit 0, zero stderr bytes.
5. Write SEALED_EVAL.md (step 7 OOD verdict), ABLATION.md
   (step 8 verdicts), REDTEAM_SELF.md (knowledge-vs-architecture,
   metric gaming, presentation fabrication). Dash-scan every lane
   file with check_no_dash.sh before each commit.
6. Verdicts BUILD-PASS / BUILD-FAIL / PARTIAL per step against the
   frozen bars, with commit ids. Commits lane-scoped with explicit
   pathspec; no push; no promotion claim; ceiling stays bounded L2
   with persistence; the three binding caveats bind every citation.
