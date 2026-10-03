# NAMECHECK: arena_igl language lane (wave-20261001-1421pdt)

Worker: arena IGL language-lane worker (subagent d66d8956)
Lane: LANGUAGE (C16 synthetic language acquisition). Inquiry has a completed
prereg plus BUILD-PASS (arena_inquiry, v5, 0.735); per task preference rule
(inquiry preferred only if no prereg exists) the lane is LANGUAGE, which has
no arena-lane prereg (only standalone SYNLANG mechanism work).

## Step 0: Toolchain guard (MANDATORY FIRST STEP)

Executed before any other work:

```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3   -> prints nothing (exit 1)
```

Result recorded 2026-10-01:
- safebin: /home/hatch/safebin, 36 tools linked
- znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- verify: python3 absent from safebin PATH (OK)
- verify: python absent from safebin PATH (OK)
- which python3 -> no output, exit code 1

Toolchain guard: SATISFIED. All computation in this lane is pure Zag via the
pinned znc. No Python in programs, glue, analysis, verifiers, or harnesses.
Bash is used only to sequence process invocations (same pattern as the
committed run_arena.sh).

## Step 1: Lane selection record

- Located arena records: docs/lab/research-lead/overnight-20260928/competitive_arena/
  (ARENA_PREREG.md + amendments, arena.zag scorer, world_gen.zag, run_arena.sh)
- v4 contestant: docs/lab/research-lead/overnight-20260928/arena_conflict/devint1_contestant_v4.zag
  (0.676, 46/68, 7/7 kill bars per ARENA_CONFLICT_REPORT.md)
- Inquiry lane: already has PREREG_ARENA_INQUIRY.md and ARENA_INQUIRY_REPORT.md
  (BUILD-PASS, v5, C8 1.000). Not re-done in this lane.
- Goal (C15) and language (C16) have no arena-lane prereg. Selected LANGUAGE:
  6 scored items (vs 1 for C15), and the mechanism (morphological rule induction
  from labeled word examples) is a genuine learning capability rather than
  enumeration.

## Step 2: Prereg ordering

- PREREG_LANGUAGE.md written BEFORE any implementation work (writing-only first).
- Implementation file devint1_contestant_v6.zag created after the prereg file.
- No git commit performed (task forbids commit/push/checkout/branch changes);
  ordering is evidenced by file mtimes, recorded in RESULT_LANGUAGE.md.
