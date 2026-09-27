# Deliberation Fork-Divergence Repair Report — Round 2

**Date:** 2026-09-27  
**Branch:** `tnn-native-lab`  
**Task:** Repair `deliberate.zag` to incorporate all adopted round-4 dialogue behavior while preserving the ledger architecture (readings GEN → facts GEN → actions GEN → ELIM → ARGMAX).

**Provenance:** This is the second repair round. The first repair (commits `6e69b86b3`, `82bfa629e`) reached 33/38 on the adopted round-4 battery. An independent red team issued NO-GO on the report commit `c3f2261d6`. This round addresses the red-team findings and reaches the full proof bar.

**True characterization:** The remaining divergences were **gate-policy integration gaps** — repaired gates (G3, G6, clarify/withhold) that existed in the source but were not wired into the full deliberation policy (e.g., clarify considering only gate 2, correction falling back to a stale literal). They were not entity-retrieval edge cases.

## Proof battery results

Every battery was run twice; the two outputs were byte-identical. SHA-256 of the output is recorded.

| Battery | Score | Output SHA-256 | Bar |
|---|---:|---|---|
| Adopted round-4 (`round4/battery.txt`, 38 probes) | **38/38** | `61810b656f3691621f0fe927745eb25c3f0ef9dfd9a6a44eb6a2019182462272` | 38/38 met |
| Generality (8 probes vs adopted `gen_ref.out`) | **8/8** | `64f0e7d10f73ff8f36bebccb95caaf9e7551378f172010f32c594b645b8d3f7b` | 8/8 met |
| Round-3 answer-stream equivalence (23 probes) | **23/23** exact A-lines | `d8a9f004ab1032349a7fac6c691a6a6ec51d79c7542b6a3a01f9e1f37a3d8340` | 23/23 met |
| Heldout (`deliberation/heldout.txt`, 20 probes) | **20/20** | `96937cd04a6b72f9d73bb9711f64d05b6c2e1820042aa7cba3741ff7191b47dd` | 20/20 met |
| Round-2 F2 withhold battery (370 probes) | **355/370** | `b60971207af64035db84461c3bf85551726f54f195fc84e83a658202cc98af04` | no regression (floor 351/370) |
| Round-2 integrated battery (18 probes) | **15/18** | byte-identical runs; SHA recorded in manifest | matches adopted reference |

All six bars met. No bar missed: this is a GO.

### Round-2 F2 detail (355/370)

Failures: `101, 121, 141, 274, 279, 284, 289, 294, 299, 304, 309, 314, 319, 324, 329`.

- Probes 101/121/141 (ellipsis) are inherited from the pre-repair fork, unchanged.
- Probes 274–329 are the adopted round-4 reference's own known-miss region.
- The pre-repair fork failed 23 probes; this repair fixed 8 of them and introduced zero new failures.
- The adopted round-4 reference scores 351/370 on this battery with a different 19-failure set; the no-regression floor (351/370) is exceeded.

### Round-2 integrated detail (15/18)

The three misses are exactly the adopted reference's three legacy drifts (verified identical):
- Probe 6: expected `120`, actual `120 meters`
- Probe 14: expected no-joke response, actual composed joke
- Probe 18: expected short forget refusal, actual architectural explanation

### Generality adopted answers matched (8/8)

1. `1000 meters`
2. `4500 kilograms`
3. `45 degrees celsius`
4. `90 minutes`
5. `1690 meters`
6. `8519 meters`
7. `84 years`
8. Honest elephant/sauna incompatibility clarification

## The ten behavior changes vs the pre-repair fork

Verified by programmatic function-level diff of `deliberate.zag` against the pre-repair source. Only the listed functions changed; no other answer-stream changes exist.

1. **Correction `use_prev` fallback generalized** (`gen_correction`): any zero-entity correction reuses the previous resolved query shape, not just the literal "the other one".
2. **Correction second fallback** (`gen_correction` + new `qfocus_span`): reshapes the previous query by replacing its focus span with the correction remainder (e.g., "who wrote hamlet?" + "no, i meant the eiffel tower." → "who wrote the eiffel tower").
3. **Clarify gate set** (`gen_clarify`): considers withhold gates {2,3,6}, not just gate 2.
4. **Withhold gate set** (`gen_withhold`): considers gates {2,3,6}, not just gate 2.
5. **`pred_mismatch` pronoun allowance**: rejects only `ne4==0 && bn==0`; a bound pronoun (`bn>0`) may carry the clarification.
6. **Clarify/withhold `wpe` from bound pronoun**: when `ne4==0 && bn>0`, the withhold/clarify entity comes from the bound pronoun buffer.
7. **`diff_dim` "heavier"**: "how much heavier is X than Y?" recognized as a quantity-difference dimension (kilograms).
8. **`diff_dim` "hotter"**: "how much hotter is X than Y?" recognized as a quantity-difference dimension (degrees celsius).
9. **`grab_num_left` space skip**: skips spaces before reading a quantity, enabling text like "100 centimeters".
10. **`pron_class` "there" removal**: the pre-repair fork bound "there" as a class-3 pronoun; the adopted round-4 reference does not. Binding it over-enabled predicate clarification against a previously mentioned entity (observed: identical salience `[17:1, 19:1]`, fork produced `bn=1` vs reference `bn=0` for "how many people live there?", flipping the adopted "I don't know." into a clarification). Removed.

## Fresh behavioral neuter flips

See `probe_gaps.txt` for the full record. Three probes absent from every existing battery, each isolating one repaired mechanism:

1. **G3 ALL semantics** — "when was big ben dedicated?": pre-repair "I don't know." → repaired informative clarify with Big Ben's taught facts. G3 demands EVERY demand word be covered; "dedicat" is untaught for Big Ben, so the gate fires and the clarify path engages.
2. **F3 surname-only resolution** — "how much older is darwin than curie?": entities resolve via `cmp_scan` over the punctuation-stripped tail (instrumented: `ne_d=2`). The old `gaz_scan` path failed single names outright.
3. **Correction after withhold** — "who wrote dune?" → "no, i meant the martian.": pre-repair "The Martian was published in 2011." (wrong fact) → repaired "Andy Weir wrote The Martian." (matches adopted reference).

## Architecture preserved

- The 25-row GEN → ELIM → ARGMAX ledger is intact (verified: `gen_readings` emits 12 rows, `gen_fact_cands` 7, `gen_action_cands` 6; ELIM and ARGMAX unchanged).
- `docs/lab/epistemic_native/` does not import `deliberate.zag` (verified by grep; no dependency regression).
- Pure Zag, deterministic, zero RNG. No per-item hardcodes; all mechanisms are broad.

## Remaining misses

None against the assigned bars. The Round-2 F2 battery has 15 failures and the integrated battery 3, all documented above as inherited or adopted-reference-identical; the explicit no-regression floors are met.

## Files committed

- `docs/lab/dialogue/deliberation/deliberate.zag` — repaired source (212,223 bytes)
- `docs/lab/dialogue/deliberation/build/deliberate_frozen_r4repair2.zag` — frozen copy
- `docs/lab/dialogue/deliberation/probe_gaps.txt` — fresh neuter-flip probes
- `docs/lab/dialogue/deliberation/DIVERGENCE_REPAIR.md` — this report

No binaries, `.zagd` files, caches, or doubled paths are included.
