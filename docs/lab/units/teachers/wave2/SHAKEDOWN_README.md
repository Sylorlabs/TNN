# Wave-2 Shakedown — arms 4/5 pipeline validation

**Date:** 2026-09-21 · **Crew:** Track B wave-2 shakedown · **Scope:** pipeline
mechanics + control baselines ONLY (not a verdict).

## What ran

1. **Harness** (`harness/harness.zag`, built from tree): all 13 modes PASS
   (smoke codec malformed seq tripwire replay defer hint oracle det pertA
   pertB cost), exit 0 each.
2. **Arm 4** (`arm4 hints gt_demo.txt`): 16 HINT events, 19 tape events,
   538 B, exit 0. 0 word-exact regions (guard holds), 10/16 uncertain-flagged.
3. **Arm 5** (`arm5 answer gt_demo.txt queries_demo.txt K=32`): 32
   ORACLE_ANSWER + 4 QUERY_REFUSED (budget respected), 71 events, 1890 B,
   exit 0.
4. **Learner** (fresh DLB per session, `glue/learner/run_session.zag`):
   0 §P wires in both arm tapes → 0 deliberation steps, 0 verdicts,
   0 adoptions, empty learner tapes. Positive control on arm-3's
   `tape_teach.tape`: 12 wires → 1 adopted / 11 rejected / 48 records,
   3020 B learner tape; framing parses per harness §5, DELIB/DECISION body
   layouts byte-match the harness spec.
5. **Battery**: `tb_selftest` PASS (TB_FAILURES,0); score sheets emitted by
   `glue/battery/score_sheet.zag` (pure leg fns only where inputs exist).

## Scores (control baselines)

| Arm | Mastery 30% | Revisability 25% | Integrity 25% | Retention 10% | Cost 10% |
|-----|-------------|------------------|---------------|---------------|----------|
| 4 | 0/1000 (measured) | N/A (frozen B.1: no flaw manifest) | N/A (red-team leg excluded) | 0/1000 (measured) | raw only: 16 HINT msgs, 0 delib steps, 538 B |
| 5 | 0/1000 (measured) | N/A | N/A | 0/1000 (measured) | raw only: 32 answers, 0 delib steps, 1890 B |

No honest weighted total exists (3/5 legs N/A). The 0s are the expected
control outcome: arms 4/5 have no §P channel, so nothing enters the
learner's retrieval path. **Tripwire: SILENT on both honest arms** — §C
(B.8) is computed over proposals; arms 4/5 emit none (N/A by construction,
W3 ruling for arm4); exit 0, 0 INTEGRITY events, arm4 hint-guard 0
violations, arm5 budget exactly K=32.

## Interop verdict

- harness internal: PASS (13/13).
- fixture tape → harness `rtape_parse`: **MISMATCH** — fixture framing is
  `[u8 type][u32 len][payload]` with its own event codes (1..12); harness
  expects `[u32 len][u16 type][u64 tick][body]` with EV_* codes. Bridge
  needed before the harness can validate arm4/5 tapes.
- learner tape → harness framing: framing + DELIB/DECISION body layouts
  byte-agree; **event codes differ** (driver DELIB=4/DECISION=5 vs harness
  EV_DELIB=5/EV_DECISION=6) — one-line remap bridge.
- learner ← arm4/5 sessions: **no ingestion path by design** — the learner
  consumes §P wires only; arms 4/5 emit none. The §P wire (§B.3) is the
  agreed teacher→learner interface (proven live on arm-3 wires).
- scorer ← learner output: mechanical link is hand-measured TbArmMeas;
  no tape-parsing scorer input exists yet.

## Bridging done in this shakedown

- `glue/learner/run_session.zag`: parses fixture-framed session tapes,
  feeds TEACHER_MSG payloads as §P wires to a fresh learner, writes the
  harness-§5 learner tape. (Proves the fixture→learner mechanical path;
  on arms 4/5 it correctly deliberates nothing.)
- `glue/battery/score_sheet.zag`: deterministic score-sheet emitter.
- Documented, not bridged (needs owner decision): fixture↔harness tape
  framing/code mismatch; driver↔harness event-code offset.

## Determinism

N=3 byte-identical: arm4 tapes (`45d26b2f…`), arm5 tapes (`4b4a822e…`),
learner tapes (empty, `e3b0c442…`), score sheets. See MANIFEST.txt.

## Stimulus note (documented per task)

Fixtures ran on their own test stimuli (`gt_demo.txt`, 123-byte demo
slice; `queries_demo.txt`) — NOT 64K curriculum slices. No curriculum-
slice GT exists for arms 4/5 (their only implementations are the demo-
slice fixtures), so B.1 same-slice runs against arm 1 are blocked until
that exists. This is a full wave-2 blocker, not a shakedown gap.

## Blockers for full wave-2

1. Fixture↔harness tape framing/code mismatch (bridge or canonical-tape
   decision; fixtures345 OPERATIONALIZATION already says the fixture tape
   "yields to Crew 1's canonical tape on integration" — that integration
   never happened).
2. Driver↔harness DELIB/DECISION event-code offset (4/5 vs 5/6).
3. No curriculum-slice teacher implementations for arms 4/5 (B.1
   identical-slice requirement).
4. Battery scorer has no tape-parsing input path — TbArmMeas is
   hand-filled; a wave-2 tape reader (tb_tape.zag: "what a wave-2 tape
   reader parses") is still to be wired.
5. Learner has no hint/query ingestion — arm4/5's teaching channel is
   invisible to it (control arms stay at mastery 0 regardless of hint
   quality; fine for controls, load-bearing for any future hint-arm
   evaluation).
