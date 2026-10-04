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

## Step 0b: Phase 2 implementation start (worker toolchain guard re-verified)

- Date/time: 2026-10-01 PDT, wave-20261001-2021pdt, lane ARENA, phase 2.
- Re-ran: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (exit 0). SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
  PATH=/home/hatch/safebin for all subsequent commands in this lane.
- Fresh-shell verification with PATH=/home/hatch/safebin:
  `which python3` prints NOTHING (exit 1); `which python` prints NOTHING
  (exit 1). `which znc` resolves to /home/hatch/safebin/znc (pinned).
- Prereg commit-order check: HEAD is 8f8663026
  (8f8663026f8574effe9330364f99e486e64ed513), whose message reads
  "FREEZE arena PROCEDURE prereg (writing-only, committed alone before any
  implementation)". All implementation files in this lane are created after
  this commit, so implementation timestamps strictly follow the prereg
  commit; ordering is verifiable from git history (UNVERIFIABLE ORDERING
  guard satisfied).
- PURE ZAG ONLY in this lane: all computation via Zag compiled with the
  pinned znc, or shell plus safebin coreutils. No python anywhere.
  Any forbidden executable invocation is automatic PROCESS-FAIL and will
  be reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
  No git commit, no push, no reset, no rebase in this lane (coordinator
  commits). Write scope: ONLY
  docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/.
- Documentation rule: zero em-dash bytes in lane docs and in implementation
  stdout/stderr text (colons, parentheses, and commas only).

## Step 3: Implementation complete (TCNP), dev/control testing done

- Date/time: 2026-10-01 PDT, wave-20261001-2021pdt, lane ARENA.
- Toolchain guard held for the whole turn: safebin PATH only; `which python3`
  prints nothing (re-verified at phase start); zero Python or other
  interpreter invocations; shell only sequenced pinned znc, built binaries,
  git read ops, and file copies. No PROCESS-FAIL event.
- Contestant `bin/tcn_p` sha256:
  71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b
  (v6 base sha256 c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89;
  585 lines added, 8 v6 lines changed at documented insertion points only).
- Dev battery (contaminated by construction, /tmp only, never sealed):
  dA 6/6, dB 6/6, dC 6/6, dD 6/6 via zero-trial rebind (proc=dA, trials=0),
  dE 0/6 with 6/6 abstain (0 confident wrong). A-D dev total 24/24.
  Dev logs in ARENA/dev_logs/.
- K7a ablation (`bin/tcn_p_ablated`, one-line source delta): 0/24 on dev
  A-D, all UNKNOWN. PASS.
- K7b memorization control (`bin/tcn_p_memctrl`): 0/24 on dev A-D
  (<=6/24 bar). PASS; dev battery not memorization-solvable.
- K4 no-regression: world_gen and arena rebuilt from committed sources,
  hashes match the refreeze record; turns.jsonl hash matches the sealed
  world; `bin/tcn_p` over all 131 turns scores per-capability byte-identical
  to the v6 baseline (54/68 = 0.794, same per-cap distribution); TCNP trace
  empty on this battery. PASS.
- Determinism: 3/3 byte-identical stripped reply streams
  (57eaec92e48ca0fbe24fc713fdaad84654bd3a47224cbd6577545275348710b2) and
  byte-identical stderr traces. Zero RNG in decision paths.
- Byte scan: zero em-dash bytes anywhere in the lane (exit 1 on grep).
- Delta accounting: 0 new modes, 0 bridges, 0 routers, 0 hardcoded semantic
  cases, 0 new task-specific handlers; learner state (procedure table,
  trial log, verdict ring) verified live in state.bin.
- Full record: ARENA/IMPLEMENTATION.md. No deviations from the frozen
  prereg beyond three documented concretizations (turn envelope reuse,
  verdict/fitter caps, table caps), all inside prereg latitude.
- Lane stops here per task. No sealed worlds seen. The coordinator runs
  sealed evaluation after the independent adversary commits worlds.
  IMPLEMENTATION COMPLETE; READY FOR SEALED EVALUATION; no blockers.
