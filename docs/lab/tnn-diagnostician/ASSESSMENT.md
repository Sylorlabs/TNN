# TNN as Image-Issue Diagnostician — Assessment

**Order:** Micah 2026-09-26: "try putting TNN onto the image issues, see if TNN helped out in any way with solving image issues. See if it can find logically what's wrong."

**What was built:** `tnn_diag.zag` (pure Zag, zero RNG). TNN is trained on 8 diagnostic patterns extracted from committed evidence (upscale rectangle diagnosis f67e9893, generation audit dee44ecb6f8b, pig-front 22px find ce15343fb955). TNN's intake VALIDATES each pattern by recomputing its key quantitative claim (all 8 PASS). TNN then diagnoses 8 issues by computed explanatory gain (sum of severities of matching symptoms), selecting the argmax or honestly outputting NO PATTERN FITS. Full trace in DIAG_TRACE.txt. Two runs byte-identical.

## Results

| Issue | TNN verdict | Confidence | Correct? |
|---|---|---|---|
| I1 upscale generation path | P8 NO-SYNTHESIS | 100% | Yes |
| I2 operator-level drawing | P2 OPERATOR-DRAW | 100% | Yes |
| I3 hardcoded-constant class | P3 HARDCODED-CONSTANT | 100% | Yes |
| N1 outpaint seam (novel) | P4 MIXED-REGIMES (runner-up P8) | 79% | Yes |
| N2 ear scale factor (novel) | P3 HARDCODED-CONSTANT | 100% | Yes |
| N3 jagged lines (novel) | P2 OPERATOR-DRAW (runner-up P5) | 75% | Yes |
| N4 label speckles (novel, matches none) | NO PATTERN FITS | — | Yes |
| C1 compound (novel) | P4, runner-up P2 | 62% | Partial |

## Honest assessment: did TNN help?

**What TNN genuinely did:**
- Generalized to novel surface details. N1-N3 were new descriptions TNN never saw in training; it matched them to the right deep patterns by computed gain, not memorization. N1 is the strongest: it weighed P4 (23) against P8 (6) and correctly prioritized the mixed-regime diagnosis over the no-synthesis one.
- Honestly abstained on N4. It did not force a match where none fit — the "no atom fits" behavior working as designed.
- Discriminated competing patterns. N3 had symptoms pulling toward both P2 and P5; TNN computed 15 vs 5 and chose correctly.

**What TNN did NOT do:**
- It discovered no new mechanism. All 8 patterns are the crews' findings; TNN applied them.
- It proposed no fix direction beyond the crews' templates. The "fix direction" output selects a crew-authored template; the instantiation is limited to citing supporting symptoms.
- On the compound C1, it picked only the dominant pattern (P4). A real diagnostician would say "both P4 and P2." The runner-up is visible in the trace but TNN does not explicitly diagnose compounds.

**The one potentially novel contribution:**
N1 suggests the outpaint seam is FIRST a mixed-regime problem (feather the boundary) and only secondarily a no-synthesis problem. The crews framed outpaint as "no model of beyond-frame"; TNN's weighing says the visible defect is the regime seam. This is a prioritization the crews hadn't explicitly made. Caveat: I coded N1's symptoms, so this is suggestive, not proven.

**The deeper limitation (the real finding):**
TNN matched crew-coded (symptom, severity) pairs to crew-extracted patterns. It did not extract symptoms from raw evidence itself. True "TNN finding what's wrong" — reading the upscale source and spotting the Bresenham calls on its own, or reading a verdict doc and extracting the mechanism — is the next wall. What was tested here is applied diagnostic reasoning, not diagnostic discovery.

**Verdict on Micah's question:**
TNN's logic works correctly on the diagnostic task it was given: it goes with the best-supported pattern, weighs competing explanations, and abstains honestly. It did not solve anything the crews hadn't already solved, but it validated that the patterns capture real structure (they generalize to novel cases rather than overfitting the training instances). The N1 prioritization is worth the crews' attention. The next step toward genuine TNN-led diagnosis is symptom extraction from raw evidence, not pre-coded features.
