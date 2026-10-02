# NAMECHECK: Arena inquiry-lane worker (wave-20261001-2321pdt)

Wave: wave-20261001-2321pdt
Lane: docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/
Worker role: Arena capability worker (active inquiry, C8). No child subagents
(depth 2/2, can_spawn=no).

## Step 0: Worker toolchain guard (mandatory, first)

- Ran: sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (exit 0). Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python);
  znc OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- export PATH="$HOME/safebin" for all subsequent commands in this lane.
- Fresh-shell verification with PATH=/home/hatch/safebin:
  `which python3` prints NOTHING (exit 1); `which python` prints NOTHING
  (exit 1). `which znc` resolves to /home/hatch/safebin/znc (pinned toolchain).
- PURE ZAG ONLY for this lane: all computational research work uses Zag
  compiled with the pinned znc, or shell plus safebin coreutils. No python
  for glue, analysis, verifiers, harnesses, or fixture provisioning.
  Any forbidden executable invocation is automatic PROCESS-FAIL and will be
  reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab,
  HEAD c5ea959d4 at lane start (wave skeleton commit; local only, never pushed).
- Write scope: ONLY docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/.
- No git push, no git reset --hard, no rebase in this lane. Commits local
  only, under this lane directory. Retry on git races.
- Documentation rule: zero em-dash bytes in anything written in this lane
  (colons, parentheses, and commas only). Every doc checked with
  sh docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  before commit.

## Step 1: Prior arena material re-derived (from files, not memory)

Sources read:
- docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/NAMECHECK.md (capability map,
  TCNP BUILD-PASS record, v6 refreeze confirmation)
- docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/SEALED_EVAL.md (K1-K9 bars,
  determinism protocol, architecture accounting)
- docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/IMPLEMENTATION.md (TCNP wire
  protocol, reply envelope, K4 no-regression method)
- docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/refreeze/REFREEZE_RECORD.md
  (v6 refreeze protocol, per-capability table, binary hashes)
- docs/lab/research-lead/overnight-20260928/competitive_arena/ARENA_PREREG.md
  (16 capability definitions)
- docs/lab/research-lead/overnight-20260928/competitive_arena/world_gen.zag
  (C8 operationalization: items 64..67, test -> observe_result -> re-ask)
- docs/lab/research-lead/overnight-20260928/competitive_arena/arena.zag
  (C8 scoring rule: last test reply exact match AND first reply contains
  "observe":[; per-capability aggregation)

Capability map (sealed 68-item battery, per REFREEZE_RECORD.md):
v6 scores 1.000 on C1, C2, C3, C4, C5, C6, C7, C10, C11, C13, C14, C16
(12 capabilities nonzero); 0.000 on C8 (inquiry), C9 (causal), C12 (transfer),
C15 (goal). Total 54/68 = 0.794 CONFIRMED. Canonical clean score stays 0.573.

Zero capabilities available this wave: C8 inquiry, C9 causal, C12 transfer,
C15 goal. (Procedure got the TCNP candidate in 2021pdt; language C16 is
candidate-only, not clean.)

Battery count note: the parent task says "15 capabilities" and "the other 14".
The sealed records show 16 capabilities and 68 items (16 - 1 target = 15
others). The count does not reproduce, so it is flagged here and in the
prereg rather than asserted. The frozen no-regression bar covers all 15
non-target capabilities.

## Step 2: Chosen capability

INQUIRY (C8), per the recommended ranking. Rationale recorded in the prereg
(section 2). Phase 1 deliverable: PREREG_ARENA_INQUIRY.md (frozen prereg,
written and committed alone before any implementation file exists).
