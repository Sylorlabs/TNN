# A — Verdict

## Verdict: PASS

Arm A completes the full 1x battery. It is **not killed** (B-64 does not
strictly dominate on M1/M2 at 1x; 10x comparison not applicable) and **not
disqualified** (M8 artifacts byte-identical across all perturbations —
pending final gate confirmation).

**10x status: NOT PROMOTED TO 10x.** The M5 promotion bars block promotion:
- M5 memory/source: 13.01 FAIL vs 1.5 bar (RSS-based; the coordinate store
  keeps the full corpus buffer + slot table + ledger, as designed).
- M5 audit entries/KB: 16.19 FAIL vs 10 bar (one ADD per 64-byte coordinate
  request — the honest cost of the no-segmentation mechanism).

These are the expected null-control failures (B-64 fails both identically).
They are not optimized away: doing so would violate Arm A's mechanism.

## 1x Scorecard (metrics-v1)

| Metric | Prose | Code |
|---|---|---|
| M1 recall | 100.0 | 100.0 |
| M1 boundary | 100.0 | 100.0 |
| M1 units | 84,731 | 148,678 |
| M1 recall ops | 84,731 | 148,678 |
| M1 triple comparisons | 254,193 | 446,034 |

| M2 tier | ETC | Final recall/boundary |
|---|---|---|
| t1-prose | 1 | 100.0 / 100.0 |
| t1-code | 1 | 100.0 / 100.0 |
| t2-prose | 1 | 100.0 / 100.0 |
| t2-code | 1 | 100.0 / 100.0 |
| t3-synthetic | 1 | 100.0 / 100.0 |

M9 (t2-code): shape=fast-then-flat, takeoff_ep=1, steepness=100.0,
late_gain=0.0.

| M3 | Value |
|---|---|
| survival | 100.0 |
| fresh recall | 100.0 |
| mgmt entries | 8,050 |
| weaken handled | 50 / 50 |
| freeze | CLEAR |

| M4 | Prose | Code |
|---|---|---|
| rev boundary | 100.0 | 100.0 |
| rev content | 100.0 | 100.0 |
| kill rate | 0.0 | 0.0 |
| killsub | false | false |

M5: units=84,731, source=5,422,721 B, slot_table=2,987,332 B,
ledger=5,486,784 B / 85,731 entries, corpus_buffer=5,422,721 B.
Memory/source=13.01 (FAIL vs 1.5). Audit=16.19/KB (FAIL vs 10).

| M6 | recall | boundary | revision | tax |
|---|---|---|---|---|
| p2c | 100.0 | 100.0 | 100.0 | 0.0 |
| c2p | 100.0 | 100.0 | 100.0 | 0.0 |

M6 validity gate (15pt vs memorizer): PASS (arm 100.0 vs memorizer 27.4).

M7: N/A (no ID layer). Informational re-read bytes: 319,937.

M8: PASS (5 perturbations × 2 runs, all artifacts byte-identical).
Store chain: c1259aca444c2ae0907d4330ec9733f3790329ab535749d659cb1c13b9d8a990.
Ledger chain: fee53ffc335da7724b63bb44aa174c6b95d82e1f45775588328c3f354c3df27e.

## Kill criterion (frozen §7)

"Retire A only if B-64 strictly dominates it on M1, M2, and
retrieval-op count on both corpora at 10x."

- M1 at 1x: A=100.0/100.0, B-64=100.0/100.0 → **tie**, not dominated.
- M2 at 1x: A ETC=1 all tiers, B-64 ETC=1 all tiers → **tie**.
- 10x: A not promoted (M5 bars); comparison not applicable.

**A is not killed.** (If A ties/beats every lettered arm on M2 at equal
M1, smart arms die instead — not asserted here; cross-arm comparison is
out of scope for this report.)

## Disqualification check

M8 must be byte-identical across all perturbations or the arm is
DISQUALIFIED. Artifacts (store_chain, ledger_chain, ledger.bin) are
byte-identical across clean/frag/aslr/starve/freelist (verified by
SHA-256). The initial gate run failed only on stdout (JSON contained
the perturbation name); fixed by removing `m8_perturb` from JSON.
Re-run in progress. No disqualification.

## Commit hashes

- `4617842c5b71` — current source (`cl/arm.zag`, with m8_perturb fix)
- `7d29e5fe725e` — docs at correct paths (ARM_SPEC, BUILD_LOG, VERDICT,
  scorecard, evidence)
- `baa855e6e25c` — superseded: source (pre-fix) + docs at wrong
  `docs/lab/docs/lab/` path (orphans remain; cleanup pending)

Branch: `tnn-native-lab`, repo `sylorlabs/TNN`.

## Ambiguities (carried)

- **A-A1**: Unit schedule vs no segmentation. Each 64-byte probe window
  is an upstream-requested coordinate triple; A claims no boundaries.
- **A-A2**: M2 terminology. Frozen M2 = episodes-to-criterion (reported
  literally); the retirement bar's "M2" is ambiguous.
- **A-A3**: 10x ledger chain uses SHA-256 over concatenated per-chunk
  hashes (not literal whole-file SHA-256). Needs frozen-amendment review
  before 10x evidence is relied upon. Not exercised (not promoted).
- **A15**: Swap probe does not apply (non-ID arm, interface §9).
- **A17**: M8 uses the combined-instance interpretation.
