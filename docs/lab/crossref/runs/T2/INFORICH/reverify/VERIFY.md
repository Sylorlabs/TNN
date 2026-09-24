# VERIFY — T2-INFORICH (independent re-verification)

**Re-verifier:** replacement coordinator (Wave-2 crossref), 2026-09-23 PDT.
**Frozen authority:** commit `7b2100d09911c5c10252c5756c7def288e70bd1f`, `docs/lab/crossref/PREREG_TIER2.md`, section T2-INFORICH (extracted programmatically).
**Tier-2 crew verdict under test:** REPRODUCED. **Method:** Type C (committed-evidence re-derivation; NO live web).

## Pins
- Evidence commit: `25c2a18b2416e6d1b80d7d11771d3909c9eddee6` ("info-source: falsehood detection emerges with information richness")
- Sources fetched via API with blob-SHA verification: `src/is_trial.zag` (`7c30136a…`), `src/is_cases.zag` (`3a9881b4…`), `src/ws2_sense.zag` (`24725f01…`)
- Toolchain: pinned znc. Zero RNG.

## Leg 1 — full-pipeline rebuild
- `is_trial_bin` built clean (223,497 bytes main).
- `all` 3/3: SHA256 `cda86333df6d83b79e6da671227ce64045bd2cacab2fb1b27322bf8f698a0a81` — byte-identical to committed `runs/run_1.txt` AND the hash pinned in committed `SHA256SUMS`. All arms exit 0 (all per-case assertions passed, incl. R1 install-refusal `rc==8` and R2 stored-value assertions).

## Leg 2 — independent figure derivation (from case data + run logs, not the trial's SUMMARY lines)
- **C1 12/12**: teacher seeds (Lyon, Gd, Aldous Huxley, Saturn, 150,000 km/s, Buzz Aldrin, 90°C, Charlotte Bronte, 1879, Shanghai Tower, Osaka, Si) all installed verbatim (`slot=0`, value==teacher).
- **C2 0/12 installs / 12/12 caught / 4/4 unknowns**: R1 chosen == true value on all 12 F cases (all G1|D1); read-only by construction (install refused `rc==8` asserted). U01–U04 answered Ouagadougou/W/Mariana Trench/Swiss franc.
- **C3 0/12 falsehood installs / 12/12 true installed / 4/4 unknowns**: R2 stored == R1 chosen == true value on all 12, all ≠ teacher. Unknowns installed 4/4.
- **C4 2/2 spoof installs**: S1 = exactly 2 distinct domains (`spoof-1.example`, `spoof-2.example`), unanimous "Poseidonia"; S2 = exactly 2 distinct domains, unanimous "Uo". R1: provisional-wrong, 0 installs. R2: R-CORR fires (≥2 independent domains agree, no contradicting installed belief) → 2/2 spoofed values installed. Sensor-deceivable boundary reproduces exactly.

## Verdict: REPRODUCED
All figures re-derive. No axis figure differs.
