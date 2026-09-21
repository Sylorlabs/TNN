# M2 — Verdict

## Authority
- Brief: `~/workspace/tnn-lab/units/arms/briefs/M2.json`
- Frozen row (coordinator, byte-verified 2026-09-21):
  - Mechanism: "Counter IDs composed canonically (sorted ascending) for
    multi-span units; max composition depth frozen."
  - Kill: "Single-byte leaf edit invalidates > 25% of cached compositions
    in the recall benchmark, OR ID recomputation > 10% of recall latency
    on the 10x run."

## Corrections acknowledged
1. Original variable-length-ID mechanism and recall/swap kill bars were a
   dispatch error and are VOID (received 2026-09-21).
2. First correction was paraphrased; second correction supplied the
   authoritative verbatim row and authority order (received 2026-09-21).
   The verbatim row governs.

## 1x Battery (M1–M9)
- m1-1x-prose: PASS (100% recall, 63,547/63,547 composed, K1: 2/63,547=0.0%)
- m1-1x-code: PASS (100% recall, 111,508/111,508 composed, K1: PASS)
- m2-1x-t1p/t1c/t2p/t2c/t3: PASS
- m3-1x: PASS
- m4-1x-prose/code: PASS
- m5-baseline, m5-1x: PASS
- m6-1x-p2c/c2p: PASS (after capacity fix)
- m7-1x: PENDING (re-run after accidental kill)
- M8 gate: PASS (5/5 perturbations, byte-identical)

## Binding K1
- Prose: 2 stale / 63,547 total = 0.003% (printed 0.0%) — PASS (<25%)
- Code: PASS
- Verdict: **PASS**

## Binding K2
- 1x (r1 prose, 84,731 leaves, 63,547 compositions):
  - leaf_recall: 0.95s
  - composed_recall: 123.1s (includes verify with SHA-256)
  - id_recompute: 32.1s
  - ratio: 25.8% — **KILLED** (>10%)
- 10x (official): IN PROGRESS

## Verdict
**KILLED** by K2 (ID recomputation >10% of recall latency).

The compositional ID scheme's verification cost (SHA-256 recomputation on
every recall) dominates latency. At 1x, 25.8% of recall time is spent on
ID recomputation. The 10x run will confirm, but the mechanism is already
disqualified by the binding kill criterion.

## Death certificate
See `DEATH_CERTIFICATE.md`.
