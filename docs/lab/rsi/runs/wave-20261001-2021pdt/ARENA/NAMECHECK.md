# NAMECHECK: Arena procedure-lane worker (wave-20261001-2021pdt)

Wave: wave-20261001-2021pdt
Lane: docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/
Worker role: Arena capability worker (procedure invention prereg, phase 1).
No child subagents (depth 2/2, can_spawn=no).

## Step 0: Worker toolchain guard (mandatory)

- Ran: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (exit 0). Output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python);
  znc OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- PATH set to /home/hatch/safebin for all subsequent commands in this lane.
- Verification in a fresh shell with PATH=/home/hatch/safebin:
  `which python3` prints NOTHING (exit 1); `which python` prints NOTHING (exit 1).
  `which znc` resolves to /home/hatch/safebin/znc (pinned toolchain).
- PURE ZAG ONLY for this lane: all computational research work uses Zag
  compiled with the pinned znc, or shell plus safebin coreutils. No python
  for glue, analysis, verifiers, harnesses, or fixture provisioning.
  Any forbidden executable invocation is automatic PROCESS-FAIL and will be
  reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab,
  HEAD 57aac4b81da99792f42a94b15d9e15ed6d3bb6d1 (matches wave tip at lane start).
- No git commit, no git push, no git reset, no rebase in this lane.
  The coordinator commits the prereg alone at wave end (commit-order rule).
- Write scope: ONLY docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/.
- Documentation rule: zero em-dash bytes in anything written in this lane
  (colons, parentheses, and commas only).

## Step 1: Prior arena material re-derived (from files, not memory)

Sources read:
- docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/NAMECHECK.md
- docs/lab/rsi/runs/wave-20261001-1721pdt/ARENA/refreeze/REFREEZE_RECORD.md
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/PREREG_LANGUAGE.md
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_igl/PREREG_LANGUAGE_AMEND1.md
- docs/lab/research-lead/overnight-20260928/competitive_arena/ARENA_PREREG.md
- docs/lab/research-lead/overnight-20260928/competitive_arena/world_gen.zag
- docs/lab/research-lead/overnight-20260928/baseline_arena/BASELINE_ARENA_DESIGN.md
- docs/lab/rsi/runs/wave-20261001-1421pdt/arena_transfer/NAMECHECK.md

Capability map (sealed 16-cap battery, per REFREEZE_RECORD.md refreeze table):
v6 scores 1.000 on C1, C2, C3, C4, C5, C6, C7, C10, C11, C13, C14, C16
(12 capabilities nonzero); 0.000 on C8 (inquiry), C9 (causal), C12 (transfer),
C15 (goal). Total 54/68 = 0.794, CONFIRMED on 3 fresh sealed runs, 8/8 bars
PASS, as a CANDIDATE confirmation [RE-CERT]. Canonical clean score stays
0.573 (only a clean refreeze reproducing composition without contamination
can move it).

Critical finding for this lane (PREREG_LANGUAGE_AMEND1.md plus world_gen.zag
line 514): the sealed battery's C10 items are operationally identical to the
C16 zemprod items ("C10 procedure invention (2): novel A-words -> B-form").
The CA-1 prereg text described C10 as a rotation-rule procedure battery with
a DSL exhaustion proof; that battery was never implemented in world_gen.zag.
Therefore v6's C10 1.000 is answered by the language morphology mechanism,
not by any procedure invention mechanism. Genuine procedure invention is
untested in the sealed battery: effectively zero, with no valid battery at
all. C16 language is candidate-only (not clean). The six named zero
capabilities (inquiry C8, causal C9, procedure, transfer C12, goal C15,
language C16-clean) are unambiguous in the records. Note: the parent task
states "9 of 15"; that exact count does not reproduce from the sealed
records read here (12 of 16 nonzero in the refreeze table), so it is flagged
rather than asserted. The zero list itself is what this lane acts on.

## Step 2: Chosen capability

PROCEDURE (genuine procedure invention), per the recommended ranking.
Rationale recorded in the prereg (section 2). Phase 1 deliverable:
PREREG_ARENA_PROCEDURE.md (frozen prereg, written before any implementation).
Phase 1 ends at PREREG READY; no implementation in this turn.
