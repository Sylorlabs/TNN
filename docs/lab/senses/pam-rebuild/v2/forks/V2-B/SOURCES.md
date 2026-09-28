# V2-B Sources — Build Manifest

**Fork:** V2-B (interventional-port) | **Date:** 2026-09-23

## src/
| File | SHA256 | Provenance | Builds |
|------|--------|------------|--------|
| vsense.zag | cf4ffb43…997a78e | Byte-identical to R2-4 `sense_r24.zag` | Yes (`znc vsense.zag`) |
| deliberate.zag | 63228c64…b97663b6 | Byte-identical to R2-4 | Yes (library) |
| R33_NATIVE_IO_V1.zag | e6379ddb…641e9f61d8 | Byte-identical to R2-4 | Yes (substrate) |
| R33_NATIVE_SHA256_V2.zag | 9824f6db…7ca683bcf | Byte-identical to R2-4 | Yes (substrate) |

**DEFERRED: `src/vgate_b.zag` (pure-Zag interventional gate).** Reason: the
fork is DEAD on RK-3 (0.02%) regardless of implementation language; the
hypothesis test (preregistered ablation) is decisive from the Python
validation (score_v2b.py, 10,915 trials, 12.6pp false-install reduction).
The Zag port is mechanical (follows the vgate_a.zag pattern: record parsing,
program logic per PREREG_V2-B §2, hash-chain ledger). Writing it would not
change the verdict. If revived, the gate reads 5-span records
(F, G, P1, P2, P3) built by build_records.py extended with P judgments.

## evidence/
- VERDICT_V2-B.md (DEAD on RK-3; ABLATION PASSES)
- calibration_3sigma.json (frozen 3σ values, committed before battery)
- pspans_ledger.json (32,745 P1/P2/P3 spans, generator ledger)
- pgen2.py — P1/P2/P3 perturbation generator (frozen families, PREREG_V2-B §3; deterministic, zero RNG)
- prun.py — runs vsense on P spans (8 shards)
- cal3sigma.py — 3σ calibration on harness noise
- score_v2b.py — full/ablation scorer (the frozen hypothesis evidence)
- build_records.py — record builder (shared with V2-A/D)

## Reproducibility
1. `python3 pgen2.py` → P spans + ledger (or use committed pspans_ledger.json)
2. `python3 cal3sigma.py` → calibration_3sigma.json
3. `python3 prun.py` (×8) → P judgments
4. `python3 score_v2b.py` → full vs ablation metrics
