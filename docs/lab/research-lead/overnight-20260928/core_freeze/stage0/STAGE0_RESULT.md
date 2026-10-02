# STAGE 0 READINESS RESULT: READINESS-PASS

Date: 2026-09-30. Worker: Core Freeze Challenge Stage 0 Readiness Worker.
Protocol: FREEZE_PROTOCOL.md section 3 (Stage 0 gate), frozen at 66e3c3f38.
Candidate: composed continuing learner at dc20745db (LEARNER-REVERT-PASS).

## Verdict

READINESS-PASS. The freeze candidate is executable under the frozen protocol: the world-input interface is added as disclosed plumbing, persistent vs scratch regions are declared, and the null-world run passes all Stage 0 bars.

## What was built

`core_freeze/stage0/world_learn.zag`: the dc20745db source copied verbatim, with exactly two classes of change:

1. The hardcoded P1-P11 episode script (old `fn main()i32`) was renamed to `fn legacy_p1_p11()void` and preserved verbatim as pre-freeze provenance for the committed LEARNER-REVERT-PASS evidence. Exactly two mechanical lines changed: the signature and the trailing `return 0;` to `return;`. It is not called by the new main and is not part of the challenge path.
2. The Stage 0 world interface was appended after a marked banner: 12 new fns (word matchers, line/field scanners, integer parser, per-line router, stream driver, new main). It reads `<world.txt>`, routes OBSERVE/QUERY into the existing cognitive drivers learn()/query(), emits ACT as the documented fixed default `CHOICE 0`, and implements the frozen save/load of the 32768-byte state via `<state.bin>`.

Built with the pinned toolchain: `znc_linux_x86_64_abed8aa1 world_learn.zag -o world_learn_bin` (build exit 0; 44 analyzer warnings, all class A0102 ignored-return-value, same class as the original build's warnings).

## Kill-bar results

K1 (interface adds no semantic cases, modes, handlers, or cognitive machinery): PASS, stated affirmatively.
- Fn-body diff of all 63 functions in revert_learn.zag against world_learn.zag: 62 cognitive fns byte-identical; the 63rd (old main) equals legacy_p1_p11 with exactly the two disclosed mechanical edits.
- Whole-file diff: the only removed line is `fn main()i32 {`; every added non-comment line is inside the marked interface block (170 added lines, all parser/driver/main plumbing).
- The interface branches only on the three generic event words and integer syntax; no branch inspects world vocabulary, ids, or family. ACT emits a fixed default; no selection logic exists. No mode flags, no new handlers, no new semantic cases anywhere in the diff.

K2 (null-world run 3/3 byte-identical, exit 0, empty stderr): PASS.
- Empty world file (0 bytes), fresh state path, three runs:
  - stdout 3/3 byte-identical: `WORLD_BEGIN`, `WORLD_END events=0 answers=0`, `STATE_SAVED`.
  - exit code 0 on all three runs.
  - stderr empty (0 bytes) on all three runs.
  - state files 3/3 byte-identical and equal to the recorded initial state: 32768 zero bytes, sha256 c35020473aed1b4642cd726cad727b63fff2824ad68cedd7ffb73c7cbd890479.

K3 (pure Zag/markdown, dash-clean, contaminated paper untouched): PASS.
- All new files are .zag or .md. Zero Python. check_no_dash.sh clean on every new file.
- `git status` confirms docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md untouched (zero diff).

## Interface design (three sentences)

The binary takes a world spec file and a state file on argv; the world file is a line-oriented text stream of three generic integer-id events (OBSERVE, QUERY, ACT) with no natural language, no task labels, and no family identifiers. OBSERVE and QUERY route 1:1 into the existing cognitive drivers learn() and query(); ACT emits the fixed default CHOICE 0 as an explicitly documented placeholder since the substrate has no generic action-selection machinery. After the stream, the full 32768-byte W is written back to the state file, so one learner process per world carries the declared persistent state forward with zero source changes.

## Region declaration summary

Persistent: the single 32768-byte W (tick W[0..4), foundation-evict flag W[8..12), 36x44-byte fact store W[64..1648), collateral slots W[2000..2048), DDES ledger slice W[16384..32768); the rest zero/unused). Scratch: world file bytes, transient state-load buffer, integer parser temporaries; all process-local, none ever written to the state file. Code region immutable. Full declaration in REGIONS.md; initial (null-world) state sha256 c35020473aed1b4642cd726cad727b63fff2824ad68cedd7ffb73c7cbd890479.

## Null-world measurements

- stdout (3/3 identical): 52 bytes, `WORLD_BEGIN\nWORLD_END events=0 answers=0\nSTATE_SAVED\n`.
- stderr: 0 bytes all runs. Exit: 0 all runs.
- State delta: zero bytes changed (state equals initial state).
- Wall clock per run: under 1 second.

## Smoke tests (beyond the gate, interface function check)

- 4-event world (OBSERVE/QUERY/ACT/QUERY-unknown): exit 0; `OBSERVED 1 10 4`, `ANSWER 1 10 4`, `CHOICE 0`, `ANSWER 2 10 -2` (the -2 is the existing cognitive not-found sentinel). Second run on the same state file reproduces identical behavior: the fact persisted across process invocations.
- Corrupt world (`OBSERVE 1 10`): `ERROR line 1`, exit 1, state file untouched.
- Missing world file / wrong argc / corrupt-length state file: exit 2 with stderr diagnostics.

## Architecture delta

- Source lines added for plumbing: 212 (interface banner, comments, and code; 170 non-comment lines), plus 8 comment lines for the legacy-driver banner.
- Cognitive lines changed: 0. (Two mechanical lines in the moved legacy driver: signature and trailing return.)
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0. New task-specific handlers: 0. Learner-state structures created: 0 (the state layout is unchanged from dc20745db).
- The DDES ledger region W[16384..32768) is currently unwritten by the generic driver; this is the honest boundary noted for W3/W9, not a gap in Stage 0.

## Honest ceiling

Stage 0 proves freezability of the harness, not generality of the cognition. The interface is deliberately thin: it cannot drive the causal core generically, it cannot select actions, and it adds no linguistic or planning machinery. Those are the predicted W3/W6/W7/W8/W9 failure points from protocol section 8, unchanged by this work.

## Files committed (owned pathspec only)

- core_freeze/stage0/NAMECHECK.md (Step 0 record)
- core_freeze/stage0/INTERFACE.md (interface spec)
- core_freeze/stage0/REGIONS.md (region declaration)
- core_freeze/stage0/STAGE0_RESULT.md (this file)
- core_freeze/stage0/world_learn.zag (candidate + interface)
- core_freeze/stage0/world_learn_bin (Stage 0 binary)
- core_freeze/stage0/build.err (build log)
- core_freeze/stage0/null_world.txt (empty world spec)
- core_freeze/stage0/null_out_1.txt (null-world stdout, representative)
- core_freeze/stage0/null_state.bin (recorded initial state)
