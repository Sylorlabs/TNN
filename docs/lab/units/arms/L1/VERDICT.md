# VERDICT.md — L1: Absolute Position IDs (IDENT)

## Arm
**L1** — Absolute position IDs | IDENT
Mechanism: `ID = (stream, segment, offset); identity is WHERE, not what.`

> COORDINATOR CORRECTION (2026-09-21, acknowledged): The original dispatch
> ("Fixed-32B IDs on BPE chunks") was a coordinator dispatch error (spec text
> from a different taxonomy whose arm IDs overlapped). The true frozen §3 row
> for L1 — verified byte-identical between frozen commit
> `b0b9140c0edaf6fc678edea9e9fd4bf9cf485aca`, `ALPHABET_G-L.md`, and
> `units/arms/briefs/L1.json` — is the IDENT mechanism above. The original
> kill criteria are void. (A-CONF-1 resolved.)

## Verdict
**PASS** — L1 survives as a primary arm. No binding kill criterion fires.
All M1–M9 1x bars pass. M8 gate passes (10/10 byte-identical).

## M1–M9 1x Results (accepted final battery)

| Trial | Recall | Boundary | Detail |
|-------|--------|----------|--------|
| M1 prose | 100.0 | 100.0 | 84,731 units, probe=PASS [PROVISIONAL-PENDING-FREEZE: A15] |
| M1 code | 100.0 | 100.0 | 148,678 units, probe=PASS [PROVISIONAL-PENDING-FREEZE: A15] |
| M2 t1 prose | 100.0 | 100.0 | etc=1, uncensored |
| M2 t1 code | 100.0 | 100.0 | etc=1, uncensored |
| M2 t2 prose | 100.0 | 100.0 | etc=1, uncensored |
| M2 t2 code | 100.0 | 100.0 | etc=1, uncensored |
| M2 t3 | 100.0 | 100.0 | etc=1, M9=fast-then-flat |
| M3 | 0.0 surv | 100.0 fresh | FROZEN-UNDER-PRESSURE (1,000 valuable pinned) |
| M4 prose | 100.0 rev | 100.0 content | 0 eternity violations, frag_segs=7 |
| M4 code | 100.0 rev | 100.0 content | 0 eternity violations, frag_segs=11 |
| M5 | — | — | 233,409 units, 0.839 mem/byte (PASS <1.5x bar) |
| M6 p2c | 99.7 | 99.7 | 200/200 kills blocked, 0 leaks, tax=100.0 |
| M6 c2p | 99.8 | 99.8 | 200/200 kills blocked, 0 leaks, tax=100.0 |
| M6 memctrl | — | — | drop=54.8 (p2c), validity gate PASS |
| M7 | 100.0 hit | — | 5,000 lookups, PASS [PROVISIONAL] |
| M8 | — | — | M8GATE PASS (10/10 byte-identical) |

M9: shape=fast-then-flat, takeoff_ep=1, steepness=100.0, late_gain=0.0.

## Kill Criteria Evaluation

### (i) Store cost >3× K1 on corpus A with no recall-accuracy advantage
**UNEVALUABLE** — K1's store cost on corpus A is not available to this arm.
L1's M5: 0.839 memory bytes per source byte (slot table + RSS delta;
PASS on the 1.5x bar). Recall accuracy: 100.0% (M1). Cannot compare to K1
without K1 data. Reported honestly; coordinator to adjudicate.

### (ii) Any revision batch changes an existing position ID — dies outright
**PASS** (no kill) — M4 ran revision batches (100 boundary shifts + 100
content patches per corpus) with zero position-ID changes. The `eternal=0`
flag confirms no eternity violations. L1's append-only revision map preserves
position IDs by construction: revisions append corrected content under new
slots; the original position ID is never mutated.

### (iii) Mean segments touched per sequential recall >4 on corpus C
**UNEVALUABLE as frozen** — The battery has no corpus C. M4's informational
fragmentation probe: 7 distinct segments (prose), 11 (code) touched by
sequential recall passes over corpora A/B. This is not the frozen corpus-C
metric and is reported with that caveat.

## 10x Status
**NOT-RUN** — 10x runs only after every required 1x bar passes. All 1x bars
pass; 10x is pending coordinator scheduling.

## Determinism
- All 17 1x legs: byte-identical stdout across 2 reruns (run_metric.sh).
- M8: 10/10 byte-identical (5 perturbations × 2 reruns), M8GATE PASS via
  m8_compare.py.
- Zero RNG in AI decision paths. Pure Zag. Frozen compiler
  `znc_linux_x86_64_abed8aa1`.

## Provisional Items
- **A15**: 64 deterministic ID→content remappings. Returns remapped content
  or fails loudly. Labeled `PROVISIONAL-PENDING-FREEZE` in all M1/M7 output.
- **M7**: C′ edit + lookup schedule provisional. Reports actual hit rate
  (100.0%) with provisional label.

## Evidence
- Scorecard: `scorecard_r1_1x.json` (this directory)
- Raw battery log: `~/workspace/tnn-lab/work/l1/battery1x_v2.log`
- Per-leg fragments: `~/workspace/tnn-lab/work/l1/battery1x_v2/*/fragment.jsonl`
- M8 artifacts: `~/workspace/tnn-lab/work/l1/battery1x_v2/m8/*/run*/`
- M8 gate: `~/workspace/tnn-lab/work/l1/battery1x_v2/m8/GATE.txt`

## Commit Hashes
- `ac6c1442b39f522ef27bb6b7d26b0edd72594953` (tnn-native-lab, parent fdeb1b907839)
  — final 1x battery PASS, all source/docs/evidence. 8 files:
  cl/arm.zag, substrate/*.zag (2), ARM_SPEC.md, BUILD_LOG.md, VERDICT.md,
  scorecard_r1_1x.json, scorecard_l1.py.
