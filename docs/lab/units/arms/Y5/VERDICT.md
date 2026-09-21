# Y5 Verdict

**Arm:** Y5 — Cross-stream span sets (STRUCT)
**Mechanism:** One ID over a non-contiguous span set; kills cascade atomically via LINK with eliminative justification.
**Scale reported:** 1x (full battery). 10x blocked by toolchain limit (see §5).
**Date:** 2026-09-21
**Frozen prereg commit:** `b0b9140c0eda`, branch `tnn-native-lab`

## Verdict: PASS (1x) — binding kill does NOT fire

Every 1x bar passes. The binding kill criteria are not met:
- Link degradation on sqlite3.c: **0.0%** (bar: >20% to kill)
- Atomicity violations: **0** (bar: any to kill)

## 1x M1–M9 scorecard

| Metric | Prose | Code | Bar | Result |
|---|---|---|---|---|
| M1 recall/boundary | 100.0/100.0 | 100.0/100.0 | ≥99.5 | PASS |
| M1 ID probe | PASS | PASS | — | PASS (provisional A15) |
| M2 ETC (t1/t2/t3) | 1/1/1 | 1/1/1 | — | PASS, no leak (ep0=0.0) |
| M3 survival | 100.0% | — | ≥90% | PASS |
| M3 fresh recall | 100.0% | — | ≥99% | PASS |
| M4 rev boundary/content | 100.0/100.0 | 100.0/100.0 | ≥99 | PASS |
| M4 kill rate | 0.0% | 0.0% | ≤1% | PASS |
| M5 memory/source byte | 1.498 | — | ≤1.5 | PASS |
| M5 audit/KB | 5.015 | — | ≤10 | PASS |
| M6 recall/bnd/rev | 100/100/100 | 100/100/100 | — | PASS, tax 0.0 |
| M6 memorizer gate | 54.8pt drop | — | ≥15pt | PASS (valid) |
| M7 hit rate | 100.0% | — | ≥90% | PASS (provisional A7/A8) |
| M7 reuse | 4.1 | — | ≥1.5 | PASS |
| M8 gate | PASS | — | byte-identical | PASS (5×2 runs) |

Full scorecard: `units/arms/Y5/.work/scorecard_y5_1x.json`

## Binding kill evidence

**Clause 1:** ">20% of Y5 units on sqlite3.c degrade to single spans within the
revision curriculum." Measured on `m4-1x-code`: 2,048 LINKs before revision,
2,048 LINKs after. Degradation = 0.0%. **Does not fire.**

**Clause 2:** "Any kill leaves a live span pointing at a dead LINK (atomicity
broken — kill the implementation)." Measured by `y_audit_atomicity` after every
revision episode: 0 violations across all runs. **Does not fire.**

## Ambiguities (literal readings implemented, logged)

- **A15 (M1 ID probe):** PROVISIONAL-PENDING-FREEZE. Implemented as 64 live-unit
  T→U remap probes, byte-verified, restored. Reported PASS/PASS.
- **A7/A8 (M7):** Provisional schedule (C, C, C′ every-100th-unit XOR, 5,000
  `(l*37)%n` lookups). Reported as ID-arm fields with `na_reason`.
- **A17 (M8):** B-64 combined-instance reading. One store runs M1 ingest/probe +
  M3 churn per perturbation.
- **Provisional design choices:** 256B spans, first-token grouping, 2–8 span LINKs,
  2,048 LINK budget, tombstoned members, FIFO eviction, weaken-as-flag. All logged
  in ARM_SPEC.md.

## 10x status

**Not run — blocked by toolchain limit.** The znc compiler cannot index a slice
larger than 2^25 bytes (33,554,432). The r10 corpora are 52MB (prose) and 91MB
(code); `read_file` refuses them → `M1,FATAL,empty-corpus` on all 10x legs.
This is a known znc limit (AGENTS.md), not a Y5 design flaw. The Y5 design is
positional and linear (spans, LINKs, FIFO); no non-linear scaling is expected.
M5 memory at 1x is 1.498× (close to the 1.5 bar); 10x scaling of this ratio
was not verified.

## Corrections acknowledged

Per the coordinator's second (superseding) correction issued 2026-09-21:
- The original dispatch used the wrong arm text. Implementation uses
  `briefs/Y5.json` and the byte-verified frozen row.
- The first correction's M6-transfer paraphrase was wrong. Implementation uses
  the B-64 reference transfer protocol (train T1, in-domain revision, frozen
  policy transfer ingest, probe recall/boundary/revision, transfer tax).
- Authority: `briefs/Y5.json` > frozen row > nothing else.

## Commits

- Source/docs/evidence: [to be filled after commit]
- Binary (`.work/y5_arm`) NOT committed per instructions.
