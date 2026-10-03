# CORE FREEZE CHALLENGE: FREEZE RECORD

Date: 2026-09-30. Worker: Core Freeze Challenge Freeze Worker.
Status: CORE-FROZEN. Stage gate: Stage 1 (freeze) complete.
Protocol: FREEZE_PROTOCOL.md (frozen at 66e3c3f38), section 2.3.
Stage 0: READINESS-PASS at e129b2fbd.

## What is frozen

Cognition source (protocol 2.1): the single compiled source file
`core_freeze/stage0/world_learn.zag` plus the build command and flags below.
The pinned toolchain identity is recorded for provenance; the toolchain is
not cognition source.

The binary under freeze is `core_freeze/stage0/world_learn_bin`.
No cognition changes were made by this worker: only this markdown record
was added.

## Frozen commit (baseline)

The exact commit being frozen is:

e129b2fbd aec8d7c65e9a7c76402e51796bd6bb3

This is the Stage 0 READINESS-PASS commit. All source and binary hashes
below were recomputed from that commit's blobs and from fresh rebuilds of
the same source.

## Hashes

- Cognition source (world_learn.zag, sha256):
  b761efd90cb1b8f9fa31f319dfde8e98c52e3f4eacf5e826817adcf10d206249
- Frozen binary (world_learn_bin, sha256):
  8733af3d28148263f9ce41d979043379b9e6d637f09dcab42eff2374f3a59960
- Initial (null-world) learner state (null_state.bin, sha256):
  c35020473aed1b4642cd726cad727b63fff2824ad68cedd7ffb73c7cbd890479
- Pinned toolchain (src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256):
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef

## Build command and flags (verbatim)

Executed from the repository root:

    src/tools/toolchain/znc_linux_x86_64_abed8aa1 world_learn.zag -o world_learn_bin

No flags beyond the output selector. Analyzer issued the same 44 warnings
(all class A0102 ignored-return-value) as in Stage 0; exit code 0.

## Reproducible build verification (protocol 2.3)

The source was built twice from the frozen blobs in a scratch directory:

- build 1 sha256: 8733af3d28148263f9ce41d979043379b9e6d637f09dcab42eff2374f3a59960
- build 2 sha256: 8733af3d28148263f9ce41d979043379b9e6d637f09dcab42eff2374f3a59960
- the two builds are byte-identical to each other and byte-identical to the
  Stage 0 committed binary.

Functional check: a fresh build ran the null world (empty event stream) and
emitted `WORLD_BEGIN`, `WORLD_END events=0 answers=0`, `STATE_SAVED`, exit 0,
empty stderr, and a state file whose sha256 equals the recorded initial state
above.

## Region declaration and interface references

- Persistent learner state: the single 32768-byte W, exact byte ranges
  declared in `core_freeze/stage0/REGIONS.md`. Only declared persistent
  regions may carry information across worlds. Scratch is process-local and
  never written to the state file.
- World interface: the three generic integer-id events OBSERVE / QUERY / ACT,
  specified in `core_freeze/stage0/INTERFACE.md`. The interface spec is
  frozen with this commit.

## Verification procedure (post-freeze)

After every world, and after the full battery, the challenge runner
recomputes sha256 of the cognition-source file and of the binary and
compares against this record. Any mismatch halts the battery immediately
and the challenge verdict is FREEZE-CHALLENGE-VOID (protocol section 7).
Equality of hashes is the entire test. Verification uses shell and
sha256sum only.

## Architecture delta at freeze

- Cognition source lines changed by the freeze worker: 0.
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0.
- New task-specific handlers: 0. Learner-state structures created: 0.

## Freeze worker kill-bar verdicts

- K1 (rebuilt binary hash matches the Stage 0 binary): PASS. Two fresh
  builds byte-identical to e129b2fbd:world_learn_bin.
- K2 (FREEZE_RECORD.md contains source hash, binary hash, build command,
  and the void-on-mismatch rule): PASS, stated affirmatively in this file.
- K3 (pure markdown, dash-clean, contaminated paper untouched): PASS.
  This file is markdown only; no Python was used; check_no_dash.sh will be
  run before commit; docs/lab/research-lead/overnight-20260928/
  TNN_RESEARCH_PAPER_20260929.md is untouched (zero diff).
