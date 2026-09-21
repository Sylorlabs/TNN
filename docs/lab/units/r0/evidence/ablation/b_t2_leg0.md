# B-T2 causal ablation — leg 0 evidence (crew B-ABLDOSE)

Prereg: R0 §2 R0.1 battery 2 (causal ablation of retrieval routes).
Manifest: `docs/lab/units/r0/evidence/ablation/MANIFEST_BT2_BT3.md`
(frozen pre-execution; amendment 2026-09-21 scopes the 24/24 promotion
assertion to leg 0). Binary `b_t2.zag`, pure Zag, seed 20260921
(environment inputs only, never an AI decision). Expected-value readback
probe: `BT_PROBE,fails=0`. Golden mini-run passed inside the binary.
Leg 0: recovered parameters.

## Training

- units=400, observed spans=204547, promoted=700,
  live=700, vocab_check=24/24
- trust updates every 10th unit: w_chunk=1350, w_raw=2000

## Hard-grounding battery (200 occurrences, label-3 per R-1)

| route | hard score (/1000) | label-3 | n |
|---|---|---|---|
| raw_active | 950 | 190 | 200 |
| chunk_active | 550 | 110 | 200 |
| dual_active | 950 | 190 | 200 |

- Per-route recall: raw=1000/1000, chunk=600/1000;
  consistent occurrences=190/200 (10 inconsistent-span
  occurrences excluded from label-3 by b=0).
- dual−raw delta: 0/1000 (abs 0).

## Near-twin set (192 trials, reference-only, no bar)

| route | score (/1000) | correct |
|---|---|---|
| raw_active | 609 | 117 |
| chunk_active | 468 | 90 |
| dual_active | 468 | 90 |

## Compression (dual indexing layer)

- source=30821 bytes, stored=21740 bytes
  (live chunk payload + 4 bytes per chunk-index reference + literal bytes),
  ratio=1417/1000, live payload=5237.
- The raw route re-reads the external source; the ratio does not imply
  deletion of raw evidence.

## Ledger

- entries=2048, FNV-1a hash=948767623 (compact ledger commitment
  printed per run; full 2048-entry dumps omitted by design).

## M8 adversarial-allocation battery (N=5 + repeated baseline)

| perturb | mode | rc |
|---|---|---|
| 0 | baseline | 0 |
| 1 | heap pre-fragmentation | 0 |
| 2 | held 64KiB ASLR-equivalent offset | 0 |
| 3 | entropy/clock canary | 0 |
| 4 | free-list reversal + mid-run churn | 0 |
| 0r | repeat baseline | 0 |

stdout/stderr byte-identical across all 6 runs: YES (sha256-verified by the
evidence generator). Runner attestation: M8_IDENTICAL + _RC=0 in runner status.
Expected-readback probe + golden mini-run passed in every invocation.

## Bar verdict

- chunk < dual: 1 | chunk < raw: 1 |
  ratio > 1.0: 1
- R-3 formal numeric ε and minimum compression ratio: **PENDING-MICAH-AMENDMENT**
  (proposed |dual−raw| ≤ 25/1000, ratio ≥ 1.2).
- Descriptive bar verdict: **PASS**
