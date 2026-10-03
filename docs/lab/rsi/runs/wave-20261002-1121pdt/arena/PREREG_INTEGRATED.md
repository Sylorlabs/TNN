# PREREG_INTEGRATED.md: integrated contestant assembly (candidate a)

Wave: wave-20261002-1121pdt | Lane: ARENA | Date: 2026-10-02
Status: FROZEN. No implementation exists at freeze time. This file is
committed alone before contestant_int.zag is written.

## Change

Assemble contestant_int.zag = v6_base.zag + INQ delta + REMAP delta +
CAUSAL delta, where the deltas are the exact additive sections already
verified on the individual candidates:

- INQ: inq helpers (inq_emit, INQ_ASK_ON/OFF, inq_trace_ask/absorb),
  observe_result absorb block, inq_ask emission on unknown fact/fact2,
  "observe" field in the reply envelope.
- REMAP: trace1, parse_qsegs4, remap_prod/remap_class dispatch blocks.
- CAUSAL: do/do_out intervention tracking (W 15000..15028), interference
  tick exclusion, discrim handler.

Additive only. No mechanism logic is altered: each delta is copied
verbatim from its frozen lineage source (inq_contestant.zag,
remap_contestant.zag, causal_contestant.zag as extracted via git show
from their recorded commits). No new modes, bridges, handlers, opcodes,
or semantic cases. W offsets are disjoint by construction:
v6 core + zem/lex region (shared, 13120..13920, identical zem_store in
v6 and remap lineages) + causal region (15000..15028); INQ adds no new
W offsets (verified: no get32/set32 offset in inq_contestant.zag absent
from v6_base.zag).

## Metric

Per-capability scores on the fixrun2 world (68 items, 291 turns),
scored by arena_512 (cross-validated byte-identical vs the frozen
scorer). Also: total/68, stripped reply-stream sha256 per run,
tool_calls (observe requests), binary sha256 (built twice).

## Frozen kill bars

- I1 (no regression): for EVERY capability, integrated score >= the max
  of the four individual candidates' fixrun2 scores (v6 54/68 profile,
  INQ C8 4/4, REMAP C12 6/6, CAUSAL C9 3/3).
- I2 (gains preserved): C8 4/4, C9 3/3, C12 6/6.
- I3 (determinism): 3/3 runs, stripped reply streams byte-identical.
- I4 (purity): pure Zag under safebin; `which python3` empty; sources
  via `git show` from recorded lineage commits; binary rebuilt twice,
  byte-identical.
- I5 (architecture): no new modes/bridges/handlers/opcodes/semantic
  cases; accounting recorded; W-offset map documented disjoint.

Predicted outcome (honest, not a bar): 67/68 = 0.985, C15 0/1
(DEFRECALL is not integrated; its scope is bounded per ABSTENTION_TEST).
A PASS requires I1..I5. Any FAIL kills the assembly claim this wave;
the individual candidates stand unaffected.
