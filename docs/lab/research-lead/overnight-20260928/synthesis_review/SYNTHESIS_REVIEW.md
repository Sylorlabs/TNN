# Synthesis Review: TNN3_DESIGN_SYNTHESIS.md

**Verdict: SYNTHESIS-REVIEW-COMPLETE.** Reviewed commit `a01128de5` (132 lines of synthesis + 48 lines NAMECHECK). Review only; the synthesis was not edited.

## Input coverage check (all six declared inputs verified against git history)

| # | Input | Commit (verified exists) | Covered in synthesis | Complete? |
|---|---|---|---|---|
| 1 | Floor spec, 7 capabilities | `f383dd11c` | Section 1: F1/F2/F3 freeze + G1/G2/G3 GW, thresholds, NOT-floor list, 4 breaking criteria incl. anti-gaming clause | YES |
| 2 | Treadmill guard | `1646b9732` | Section 2: definition, 8 warning signs, 5 checks with dispositions, per-capability analyses, 3 guard-gaming modes | YES |
| 3 | SUF implications | `b1835dec6` (plus supporting `64eec921f`, `8ef148a42`) | Section 3: property definition, entrance-gate argument, zero-to-one recipe, per-mechanism (b) candidates cheapest-first, non-moves, do-not-do list | YES |
| 4 | Bar priority + roadmap with bars | `20d810d4b` (+ roadmap-with-bars in `bbe79ddf1`) | Section 4: 24 bars, phases P0-P4+PX, critical path, future-bar triggers, audit-bar placement | YES |
| 5 | Revision bug report | `8b58c4104` (sourced from boundary map `8d763d766`) | Section 5: what/why/impact, 3 fixes, regression test, compounding findings (Surprise 2, E5) | YES |
| 6 | Reading order + open items | (none, synthesis author) | Section 6: reading order, open items for preregistration, governance scope | YES |

Supporting citations spot-checked: re-clustering `ed2357141` (generality check), GW eval `881fbb3d4` (G1-G3 provenance), boundary map `8d763d766` (bug provenance), SUF definition `64eec921f`, SUF check `8ef148a42` (entrance gate). All exist on `tnn-native-lab`.

## Nothing missing from the declared scope

- Each of the six inputs has a dedicated section with full transcription of its load-bearing content.
- The synthesis invents nothing: explicitly statused as DRAFT, governs nothing until a frozen preregistration references the sources.
- Section 1 preserves the NOT-floor list (FW3/FW7/FW8/FW9, FW6 contingency, GW6 retirement, GW8 rev2/revert, GW3 phases 3-4, GW4/GW5, depth ceiling, DAG bound) so failure modes are not preserved.
- Section 3 carries the banked protected-core caveat for inquiry (I-a) and revision (R-a) without making the decision.
- Section 6 lists open items without resolving them (Step 4 enumeration E, H3-lite Step 4 clearance, banked structural-ops decision, K-STATE-RET placement, six kill-bar questions, floor battery placement).
- Zero em dashes in the synthesis (byte-verified).

## Observations (informational, not findings)

1. The copy-and-commit revision advice (commit `5a009ff87`) and guard-integration spec (commit `abe3d32e5`) postdate the synthesis inputs and are therefore absent. This is expected: they were never declared as inputs. A future synthesis pass could reference them.
2. Section 4's phase table cites the roadmap-with-bars as "in `bbe79ddf1`" (a swept commit); content was verified by the roadmap-update worker as byte-identical. No action needed.
3. The synthesis repeats the floor spec's "7 capabilities" count consistently; the guard-integration draft's "seven" in one insertion-point text refers to floor capabilities and was separately verified as consistent (the floor spec has 7: F1/F2/F3 + G1/G2/G3). No contradiction.

## Conclusion

The synthesis covers all six declared inputs completely, accurately transcribes their load-bearing content, invents nothing, makes no banked decisions, and correctly scopes itself as DRAFT. No gaps found within declared scope.
