# NAMECHECK.md (governance worker, wave wave-20260930-1421pdt)

## Step 0 (WORKER TOOLCHAIN GUARD, mandatory)

- `which python3` returned: `/usr/bin/python3` (system runtime binary; not removed from PATH; coordinator has documented that removing it would break runtime tools).
- Guard commitment: no python/python3, no C/C++, JS, or Rust interpreter will be invoked by this worker in this wave. Shell is used only for: invoking znc, running compiled binaries, git read-only ops, moving/copying files. All computational research logic must be pure Zag (none needed in this lane: governance work only, no computation performed).
- Toolchain check status: PASS at session start. If a forbidden executable is invoked, this wave is automatically PROCESS-FAIL; this file will record it immediately.

## Lane scope

- Lane directory (write ONLY here): `~/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20260930-1421pdt/gov/`
- Scratch: `/tmp/gov-1421/`
- Working copy: `~/workspace/tnn-rsi`, branch `tnn-native-lab`, run-start tip `d5984f313`
- Git posture: read-only (no commit, no push, no branch switch, no fetch/merge)

## Outputs produced this wave

- INTERACTIVE_SURVEY_1421.md
- ARCH_ACCOUNTING_1421.md
- COMMITORDER_1421.md
- DEBATE_MOTIONS_1421.md
- LOOPSTATE_DRAFT_1421.md

(All end with _1421 to match the wave stamp; no em-dashes used in any doc.)
