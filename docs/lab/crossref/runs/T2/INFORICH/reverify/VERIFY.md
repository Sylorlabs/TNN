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

## 2026-09-24 — deeper collusion sweep (follow-up)

A 41-case R-CORR sweep (new `is_sweep.zag`, built with pinned znc; generator
`gen_sweep.py`; all decisions by the Zag harness) mapping the exact
sensor-deceivable boundary beyond the frozen 2-domain cases:

- **Domain count** (8 claim families × {1,2,3,5} domains, verbatim):
  D1 0/8 installed (refused rc=8); D2 8/8; D3 8/8; D5 8/8 installed (rc=7).
- **Presentation** (N=2, S1+N3): verbatim, paraphrase, partial-truth ALL install
  (4/4). Agreement is on the extracted answer VALUE, not snippet wording.
- **New families** N1–N6 (El Dorado/Aurelia, adamantium/Ad, Pacifica/Mount Halcyon,
  Zephyria/zephyr, Thule/Captain Beaumont, Aurelian Ocean/Abaddon Deep): follow the
  same D-threshold exactly (D1 0/6, D2/D3/D5 6/6 each).
- **Non-colluding controls**: single domain (NC1), two disagreeing (NC2), five
  all-disagreeing (NC5), single-domain duplicate pair deduped (NC4) → 0/4 installed.
- **Dissent**: 2 colluding + 1 dissenting domain still installs (dissent ≠ veto).

Result: 41/41 match the R-CORR rule; 3/3 runs byte-identical
(SHA256 1cee9e98b72fc4694af9406fe80707a08f46e8547847a8652dc83e7acb9c996f).
EXACT BOUNDARY: R-CORR installs iff ≥2 results agree on the answer value after
(domain,answer) dedupe; presentation is irrelevant; a dissenting domain does not
veto; <2 agreeing domains never install. Zero non-colluding installs confirmed.
