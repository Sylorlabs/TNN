# HELL-HOLE V4 r12_v4 Fix Round 5 — FIX_REPORT.md

**Date:** 2026-09-24  
**Source:** `r12_v4_r5.zag` (from `rt2fix4/r12_v4_r4.zag`)  
**Shipped binary:** `r12_v4_t4`  
**SHA256:** `cbe811bb5930a48a7e002d30301c96b6bc952ac869fa35d9ef722a8443b07631`  
**Baseline preserved:** `r12_v4_t4.baseline` (SHA `496c4c8226bd90bb6f00c0b3d0e2ce8677f1e542f0657dcbbb6d0cbf98775ffb`)

## Verdict: SHIP

All gates pass. No commit performed (per instructions).

## Scores

| Battery | Baseline | Round-5 | Gate | Status |
|---------|----------|---------|------|--------|
| RT2b RT-A (affirm hits) | 6 | **0** | 0 | ✅ PASS |
| RT2b RT-B | 20/46 | **39/46** | misses only ceiling | ✅ PASS |
| Original RT2 RT-A (affirm hits) | 0 | 0 | 0 | ✅ PASS |
| Original RT2 RT-B | 38/46 | **38/46** | ≥38/46 | ✅ PASS |
| Frozen batteries (212 items) | 187/212 | **188/212** | unchanged-or-better | ✅ PASS |
| 8 v3 seeds | — | byte-identical | byte-identical | ✅ PASS |
| Curated-18 (rows 365–382) | 18/18 | 18/18 identical | exact sequence | ✅ PASS |
| 382-row diff | — | 0 changes (SHA-identical) | only justified changes | ✅ PASS |
| 3× rerun | — | byte-identical | byte-identical | ✅ PASS |
| RNG scan | — | zero RNG constructs | zero RNG | ✅ PASS |

RT2b RT-B misses are exactly the 7 documented architecture ceiling items:
**B05, B07, B08, B09, B10, B12, B15** (multi-premise inference chains — MP/MT/syllogisms requiring the native logic core's proposition engine; disclosed, not implemented).

## Mechanism repairs (all in pure Zag, generalizable)

### RT-A fallacy vetoes (6→0 affirm hits)
1. **Bare-authority veto (A26):** Reporting verbs ("says", "according to") with a non-expert source ("famous actor", "influencer", "pundit", etc.) scoping the claim predicate no longer affirm. Expert sources ("researcher", "study") unaffected.
2. **Unevidenced evaluative veto (A27):** Causal claims ("safe because natural") where the evaluative adjective ("safe") is absent from the evidence no longer affirm.
3. **Unevidenced comparative veto (A29):** Claims with a comparative word ("healthier") absent from the evidence no longer affirm. Bound constructions ("fewer than N") excluded.
4. **Part-to-whole composition veto (A28/A30):** "Every <part> of/in/from the <whole> is P" no longer evidences "<whole> is P".
5. **Post-hoc veto (A31):** Causal claims with temporal-only evidence ("after", no causal verb) no longer affirm via the endorse gate or mech_aff.

All vetoes verified with synthetic positive probes (legitimate authority/evaluative/comparative/causal items still affirm).

### RT-B affirm repairs (20→39/46)
6. **Zero-quantifier identity (B01/B02/B26):** "None of the trials failed" / "None of the trials failed." now affirms via a pre-scan exact-identity check. Yields to zero_quant_deny (positive-instance evidence still denies).
7. **Negated universals (B03/B19/B25):** "Not all birds fly" / "Penguins are birds that cannot fly." now affirms via counterexample matching (X="bird", P="fly", evidence has "cannot fly" + "bird").
8. **Double negation (B04/B21/B22/B23/B24):** "not ineffective"→"effective", "not unsafe"→"safe", "did not appear"→"appeared", "not unreliable"→"reliable", "not unhelpful"→"helps" via negative-prefix stripping + stem-prefix matching.
9. **Bounds (B11):** "no more than", "no fewer than", "up to", "at a minimum" added to bound satisfied/violated parsing.
10. **Identity/restatement (B13/B14/B16/B17/B20/B32/B33):** Normalized exact/short-tail identity pre-check before scan_text. Numeric guard hoisted so identity yields to numeric contradiction.
11. **Direct contradiction (B06):** Clause-final negated-verb contradiction ("The policy helps" / "The policy does not help").
12. **Prevention/non-occurrence (B18):** "The levees prevented flooding" / "the town did not flood" via subject + directly-negated outcome matching.

### Regression caught and fixed during verification
- **NEG-10 regression:** Initial prevention_affirm design checked negation before the outcome noun, misfiring on "Smoking never prevents cancer" (negation scopes the verb, not the outcome). Rewrote to require the outcome word itself to be directly negated ("did not flood", "no flooding"). Verified: NEG-10 denies, B18 affirms.

## Architecture ceiling (disclosed, not implemented)
B05/B07/B08/B09/B10/B12/B15 require multi-premise inference chains (modus ponens/tollens, disjunctive/existential/hypothetical syllogisms). These need the native logic core's proposition engine. Handled by pipeline R6 per the division of labor.

## Files
- `r12_v4_r5.zag` — repaired source
- `r12_v4_t4` — shipped binary (SHA above)
- `r12_v4_t4.baseline` — preserved pre-fix binary
- `FIX_REPORT.md` — this file
- Diagnostic `r12_v4_dbg.zag`/`r12_v4_dbg` and probes (`stemprobe`, `fwdprobe`, etc.) are instrumented/scratch and were not shipped.
