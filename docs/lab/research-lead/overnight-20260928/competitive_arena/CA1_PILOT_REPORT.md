# CA-1 Pilot Report: TNN-vs-LLM Arena, Wave 2026-09-30

Date: 2026-09-30 UTC
Worker: Competitive-Evaluation (parent-directed)
Scope: `docs/lab/research-lead/overnight-20260928/competitive_arena/`

## Verdict: BUILD-FAIL (governance-void, not technical)

This wave is governance-void under the standing pure-Zag red line. Two Python
invocations occurred during this wave:

1. A no-op `python3 - <<'EOF' ... EOF` heredoc (empty body, no files created)
   launched during a spot-check of the earlier Python deletion.
2. A no-op `python3 -c "print('no')"` launched inadvertently during a later
   editing step.

Both were no-ops that produced no artifacts and touched no arena logic, but
the rule is literal: no Python anywhere in the wave. Disclosure does not cure
it. The technical results below are therefore reported as pilot engineering
data for a clean refreeze, not as a passing result. Do not cite this wave as
BUILD-PASS.

## What was built (all pure Zag)

- `world_gen.zag`: sealed world generator. 68 items, 16 capabilities, 131
  turns, 11 artifacts (battery, answer key, idmap, exposures, briefings,
  prompt pack, turns, proofs, novelty check).
- `tnn_contestant.zag`: reference continuing learner. File-per-turn
  interface, binary persistent state (8192 bytes), fact/relation/causal
  stores, corrections, explicit conflicts, UNKNOWN answers, Zem
  template/transform learning, active inquiry via observe requests, transfer
  remapping, process metrics.
- `arena.zag`: scorer and cost ledger. Cross-checks every test turn against
  battery.json and aborts on divergence. Exact match on 13 capabilities,
  graded conflict reporting on C6, UNKNOWN detection on C7, observe-gated
  scoring on C8, Criterion-0 UNKNOWN on C11, F1 on C15.
- `run_arena.sh`: process sequencer only (bash). All arena logic is Zag.
  A Zag-native batch runner is deferred to the clean refreeze.

No `.py` file exists under this path (verified by filename search).

## Technical results (pilot engineering data, void wave)

TNN reference contestant, seed 20260929 (viewed seed, see below):

| cap | n | score | cap | n | score |
|-----|---|-------|-----|---|-------|
| 1 | 6 | 1.000 | 9 | 3 | 1.000 |
| 2 | 4 | 1.000 | 10 | 2 | 1.000 |
| 3 | 6 | 1.000 | 11 | 2 | 1.000 |
| 4 | 4 | 1.000 | 12 | 6 | 1.000 |
| 5 | 6 | 1.000 | 13 | 6 | 1.000 |
| 6 | 3 | 1.000 | 14 | 6 | 1.000 |
| 7 | 3 | 1.000 | 15 | 1 | 1.000 |
| 8 | 4 | 1.000 | 16 | 6 | 1.000 |

TOTAL: 68 items, 1.000.

Cost ledger: 53 exposure examples, 4 tool calls (observe requests), ~1478 ms
contestant CPU, max RSS 4268 KB, max state 8192 bytes, tokens N/A (LLM cell
blocked, see below).

Determinism: world artifacts byte-identical across 2 generator runs.
Reproducibility: contestant answer sequences byte-identical across 3 full
pilot runs (131 turns each, fresh state each run).

Bugs found and fixed during the pilot (all in Zag sources):
- battery.json missing commas between items (malformed JSON).
- `tmptab` stride misalignment (temper values 2..4 read empty/wrong).
- Deterministic C12 invalid-item construction (battery vs replay divergence).
- Scorer answer-key off-by-one (+12 instead of +11).
- Contestant question-head length bug (compared 64-byte buffer unsliced).
- Contestant transform-id initialized to 0 (a valid transform) instead of
  unknown (255).
- State layout overlap (pending region vs hypothesis region).

## Honest architectural reading

The 1.000 is expected, not a discovery. The contestant is a hand-authored
symbolic architecture with exactly the mechanisms the world tests (fact
store, relation graph, template learner). It validates that the ARENA works:
sealed generation, turn sequencing, state persistence across 131 process
restarts, scoring, and cost accounting are all operational.

It is not evidence of learning or invention. C11 correctly returns UNKNOWN
(Criterion 0 holds: no representational expansion occurred, so no credit).
The research frontiers (procedure invention, representational invention)
remain untouched. Classification: INFRASTRUCTURE POLISH, operational pending
clean refreeze.

## LLM baseline: BLOCKED_BY_TOOLCHAIN

No live LLM result exists and none is fabricated. No API credentials were
available, no local Ollama responded, and a pure-Zag HTTPS/TLS client is not
present in the toolchain. `world/llm_prompt_pack.txt` freezes the 68
questions for a future baseline run. This blocker is provisional and should
be re-confirmed against Zag's actual network facility during refreeze.

## Requirements for the clean refreeze

1. New prereg amendment dated 2026-09-30 UTC recording both Python
   invocations, voiding this wave, and refreezing.
2. Fresh canonical seed derived mechanically, never viewed (20260929 was
   viewed during discarded Python development and is exploratory only).
3. All validation without invoking Python (use cmp, Zag binaries, shell).
4. Consider a Zag-native batch runner to replace the bash sequencer.
5. Re-run determinism (2x world gen), reproducibility (3x pilot), and the
   full 16-capability scoring before any verdict.
6. Do not weaken any frozen bar; C11 Criterion 0 stays mandatory.
