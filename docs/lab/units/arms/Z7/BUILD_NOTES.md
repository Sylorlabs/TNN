# Z7 — Provenance cuts: crew build notes

Arm crew Z7 (replacement crew), 2026-09-21. Frozen spec: prereg §3 row
(commit `b0b9140c0eda`), brief `units/arms/briefs/Z7.json` — verified
byte-identical in mechanism and kill criterion before building. Authority
order honored: brief = row; no conflicts found.

## Mechanism as built

Cut at trust-tier boundaries; every chunk carries its trust tier; recall
returns the tier with the bytes (consumers never receive bytes without their
trust label); tier upgrades re-cut with audited `derived_from` lineage.
One native binary, pure Zag, zero randomness in any decision path.

## Crew literal-reading decisions

**D1 — Tier-assignment rule (resolves open item A-57, value + rule).**
Tier is a pure, frozen function of corpus id, compiled into the arm; no
human judgment per chunk:
- `prose.bin`, `code.bin` → tier 0 PROVEN (protocol-fixed training fixtures)
- `t1_prose.bin`, `t1_code.bin` → tier 1 CORROBORATED (novel tier)
- `t2_prose.bin`, `t2_code.bin` → tier 2 SINGLE-SOURCE (third corpus)
- `t3.bin`, `churn_fresh.bin` → tier 3 UNTRUSTED (synthetic deterministic)
- corpus 11 (spoof stream) → frozen per-offset schedule `[0,3,0,3]` per
  4096-byte segment (proven / adversarial channels alternating)

Every assignment is auditable: the tier rides in each ADD ledger entry
(`a1`; `a2` = `derived_from` on upgrade re-cuts), in the per-slot tier array
(which is part of the M8 store image), and is re-verified on every recall
probe (`tierbad` counters on M1/M2/M6/M8 stdout; all must be 0). The second
kill clause ("tier assignment cannot be made deterministic/auditable without
human judgment per chunk → collapse to arm O") does not fire: assignment is
deterministic (byte-identical reruns, M8-gated) and fully audited.

**D2 — Segmentation granularity (deviation from "maximal", documented).**
The frozen mechanism says "maximal single-provenance spans". On the frozen
fixtures each corpus is a single provenance at a single tier, so literal
maximal spans would be whole-file chunks (1–2 units per corpus). That makes
M3/M4/M6 vacuous (no capacity pressure, defects collapsing onto one unit)
while reporting 100s — honest measurement forbids reporting vacuous passes
as results (the design doc itself lists enormous spans as a weakness,
RISKS.md R3). Decision, following sibling-arm precedent (Z5 keeps the
harness 64B grid and layers its mechanism on top): the arm cuts the
*ingested extent* at trust-tier boundaries and each tier-run becomes one
maximal chunk. The harness legs ingest 64B extents (the harness address
quantum), so standard-leg chunks are 64B and tier-homogeneous — every
standard leg measures real behavior. The spoof battery ingests one 16384B
mixed-tier extent, exercising true tier-boundary cutting (1 extent → 4
maximal chunks, verified). No chunk may span a tier boundary (structural;
a tier change always starts a new chunk). Cross-ingest-call merging is not
implemented: each deliberate ingest call is its own provenance episode.

**D3 — ID-layer declaration: non-ID (crew-confirmed override).**
Chunk ID = `(tier<<28)|(corpus<<24)|(start_off/64)`: a pure deterministic
function of (corpus, offset) under the frozen tier rule — positional
arithmetic, no arm-maintained ID→storage translation structure. Same
standing as b64. M1 swap probe: N/A (no ID layer). M7: N/A + re-read bytes.
(The §9 provisional list marks z1–z8 as ID arms "subject to crew
confirmation"; this is the confirmation: override to non-ID.)

**D4 — Ledger conventions (frozen opcode namespace; aux fields arm-defined).**
- `ADD_UNIT`: `a1` = tier, `a2` = `derived_from` (0, or superseded unit id on
  an upgrade re-cut); `b5` = unit id; `d1` = chunk index.
- `KILL_UNIT`: `d1` = reason (1 churn, 2 mini-pressure, 10 recut-superseded).
- `REFUSE` reason 201 = tier-upgrade refused (world record did not corroborate).
- `REVISE_UNIT`, `TRAINER_*`, `PIN/WEAKEN/EVICT` as in the harness validator.

**D5 — Spoof battery (PROVISIONAL per A-57).** Mode `spoof-1x`. Two-source
prototype corpus per the design doc ("prototype on a two-source corpus, one
proven, one adversarial"): corpus-11 stream, 16384B, schedule [0,3,0,3];
seg1 = `prose[0:4096] XOR 0xA5` (deterministic fabricated observations on the
adversarial channel); seg3 = genuine bytes on the adversarial channel (the
honest-observation control). Probe A (containment): recall each chunk;
bytes vs independently-derived expectations, tier vs schedule;
`contamination` and `spoof_labeled_proven` (spoofed bytes recalled with a
proven-tier label — the exact binding probe). Probe B (upgrade re-cut):
upgrade of the spoofed chunk against the genuine world-record hash must
REFUSE (audited, tier unchanged); upgrade of the honest-untrusted chunk must
re-cut to tier 1 with `derived_from` lineage and the old id must fail
loudly. Kill rule: `contamination > 0` OR `spoof_labeled_proven > 0` →
"kill the claim, keep the labeling".

**D6 — Upgrade semantics.** `z_upgrade` grants a tier change only on
world-record corroboration (native sha256 of the chunk's current bytes vs
the provided record hash — deterministic stand-in for the
corroborated-elimination defense, provisional). Re-cut = KILL(reason 10) +
ADD(new tier, `a2` = old id). Tier is otherwise immutable.

## What was NOT built

- Maximal whole-file spans (see D2).
- The wave9 corroborated-elimination defense itself (35/35): the upgrade
  path uses a world-record hash check as its deterministic corroboration
  gate (provisional, D6).
- M7 ID machinery (non-ID arm, D3).

## Determinism

Zero RNG in any decision path (the only seeded generator in the pipeline is
T3's corpus builder — environment input per RULE-3). No wall-clock,
addresses, or PIDs in the ledger, store image, allocator trace, or stdout.
M8 gate: 5 perturbations × 2 reruns, byte-identical artifacts required.
