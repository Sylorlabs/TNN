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

## Step 0b: Phase 2 implementation start (worker toolchain guard re-verified)

- Date/time: 2026-10-01 PDT, wave-20261001-2321pdt, lane ARENA, phase 2.
- Re-ran: sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (exit 0). SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
  PATH=/home/hatch/safebin for all subsequent commands in this lane.
- Fresh-shell verification with PATH=/home/hatch/safebin:
  `which python3` prints NOTHING (exit 1); `which python` prints NOTHING
  (exit 1). `which znc` resolves to /home/hatch/safebin/znc (pinned).
- Prereg commit-order check: HEAD was 1156add31
  (1156add3114bc9079b93cebdb3fd7604c757e0c0), whose message reads
  "FREEZE arena INQUIRY prereg (writing-only, committed alone before any
  implementation)". The implementation commit 0ddb5e9ce
  (0ddb5e9cec6b0b506eb50bd35f215595d2362d95, 2026-10-02 06:31:59 UTC) has
  1156add31 as an ancestor (verified by git merge-base --is-ancestor);
  ordering is verifiable from git history. A concurrent lane commit
  (9db334bd4) landed between them; it does not touch this lane.
- PURE ZAG ONLY in this lane: all computation via Zag compiled with the
  pinned znc, or shell plus safebin coreutils. No python anywhere.
  Any forbidden executable invocation is automatic PROCESS-FAIL and will
  be reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
  No git push, no git reset --hard, no rebase in this lane. Commits local
  only, under docs/lab/rsi/runs/wave-20261001-2321pdt/ARENA/. Retried on
  git races (none encountered; one concurrent commit observed, no conflict).
- Documentation rule: zero em-dash bytes in lane docs (verified by
  check_no_dash.sh before each commit).

## Step 3: Implementation and sealed evaluation complete (INQ)

- Date/time: 2026-10-01 PDT, wave-20261001-2321pdt, lane ARENA.
- Toolchain guard held for the whole lane: safebin PATH only; `which python3`
  prints nothing at lane start and lane end; zero Python or other
  interpreter invocations; shell only sequenced pinned znc, built binaries,
  git read/commit ops, and file copies. No PROCESS-FAIL event.
- Implementation: inq_contestant.zag (1204 lines; v6 base
  c6dbc20cf447dce7ab506576b42557a0542065e170bee6516558ecfb435d1e89 plus
  the marked INQ section and two surgical edits; diff +69/-3, ASCII-only).
  Built on the v6 base, not on the TCNP candidate binary; candidate
  integration is a separate later decision (recorded in SEALED_EVAL.md).
- Contestant binary bin/inq sha256:
  09f59dcbee0fcd443a911f2bf24bff883960f457d0ce9acd59506d3c38339b1d
  (rebuild from committed source byte-identical; build deterministic).
- Dev smoke test (/tmp/inqdev, hand-crafted turn streams, never sealed):
  request-on-unknown, absorb-on-observe_result, answer-on-reask,
  no-request-on-known, and C7-style unknowable (request + UNKNOWN reply)
  all behave per spec. PASS.
- Sealed evaluation (frozen protocol, prereg section 6): world_gen and
  arena rebuilt from committed sources, hashes match the refreeze record;
  turns.jsonl regenerated byte-identical to the sealed world
  (0fc3edb0e2fe0d4b68e1d51a63c8cac243c8faefcd800122b2d9c1c97bcb2469,
  131 turns, 68 items); pre-run key hash recorded, key never opened.
- Scores (3/3 runs identical): C8 4/4 = 1.000 (was 0.000); C1-C7 and
  C9-C16 byte-identical to the v6 refreeze record; TOTAL 58/68 = 0.853
  (was 54/68 = 0.794). Zero regressions on all 15 non-target capabilities.
- K3 determinism: 3/3 byte-identical stripped reply streams
  (3b1911236a81c742204f0800da14933ac713ed1e23c9905cf05bc4693dcbb46d) and
  byte-identical stderr traces
  (d664b9eb600250e5fb5a8f7a1ee98b9f2710cc416305bfd5e59d7e6d8be76488).
- K6a ablation (ask off, one-line delta): C8 0/4, total 54/68. K6b
  ablation (absorb off, one-line delta): C8 0/4, total 54/68. Both halves
  causal; both ablations reproduce the v6 baseline exactly.
- K5: zero C8 oracle strings in mechanism source (grep audit). K7: C7
  reply fields exactly "UNKNOWN" in all runs. K8: 0 new modes/bridges/
  routers/handlers/semantic cases; learner state = absorbed facts in the
  general fact store. K9: L3 explicitly disclaimed (fails C0-A through
  C0-D; L1/L2 fact-acquisition infrastructure, not representational
  invention).
- Verdict: BUILD-PASS (K1 through K9 all PASS). Full record:
  ARENA/SEALED_EVAL.md. Remaining zeros: C9 causal, C12 transfer, C15 goal.
  Lane stops here per task.
