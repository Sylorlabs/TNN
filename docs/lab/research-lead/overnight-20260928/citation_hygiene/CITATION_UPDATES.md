# CITATION UPDATES: GEN-STRESS S1/S2/S4 (C410) -> GEN-REDIM (C434)

**Worker:** CITATION-HYGIENE (follow-up on DEFECT-AUDIT C447).
**Date:** 2026-10-03.
**Scope:** Documentation only; no code. No scientific conclusions altered.

## Governing rule

DEFECT-AUDIT (C447), recommendations 1-2:
- The frozen pre-redimensioning GEN base is superseded for all work registering more than 4 MAPs; GEN-REDIM (C434) is the canonical GEN base.
- 6/8-structure GEN composition behavior must be cited from GEN-REDIM (C434), never from the GEN-STRESS K2/K3/K5 corrupted runs. The corrupted outputs remain valuable only as the defect's empirical signature.

Canonical GEN-REDIM values (C434, CLEAN-REPRODUCTION-PASS, from gen_redim/REPORT.md C5/C6/C8):
- S1 (6 structures): ANS=2, TRIES=29, no WIDEN
- S2 (6 structures): ANS=219, TRIES=43, no WIDEN (GEN-STRESS prereg TRIES=48 carried four hand-derivation errors, corrected transparently in the GEN-REDIM prereg)
- S4 (8 structures): ANS=-2, TRIES=48, zero WIDEN=1 lines, clean decline

Method: repo-wide grep for `GEN-STRESS` across all `*.md` in the tnn-rsi worktree (10 files hit); each hit inspected for whether it cites 6/8-structure GEN *composition behavior* from the corrupted C410 runs.

## Changed citations (2)

### 1. gen_nm10/PREREG.md (prediction derivation, B1)

Before: "the expected outcome is a clean decline exactly like GEN-STRESS S4 at nm=8."
After: "the expected outcome is a clean decline exactly like GEN-REDIM S4 (C434) at nm=8."

Why: GEN-STRESS S4 at nm=8 did not exhibit a clean decline; its actual result was `panic: slice index out of bounds` (K5 FAIL). The clean decline at nm=8 was empirically established only by GEN-REDIM S4 (ANS=-2 TRIES=48, zero WIDEN=1). The prediction content ("clean decline") is unchanged; only the citation target changed.

### 2. gen_nm10/REPORT.md (Section 1, substantive findings)

Before: "The binding limit at 10+ is the 6-round cap for deep chains (B1), exactly as at nm=8 (GEN-STRESS S4)."
After: "The binding limit at 10+ is the 6-round cap for deep chains (B1), exactly as at nm=8 (GEN-REDIM S4, C434)."

Why: same as (1). This is a results-section interpretation citing 8-structure GEN behavior; the empirical source is GEN-REDIM S4 (C434), not the corrupted GEN-STRESS run. Numbers and conclusions unchanged.

## Canonical-base note added (1)

### 3. composition_synthesis/COMPOSITION_SYNTHESIS.md (Section 7, Caveats and ledger hygiene)

Added bullet:
"Canonical GEN base (DEFECT-AUDIT C447, recommendations 1-2): the frozen pre-redimensioning GEN base is superseded for all work registering more than 4 MAPs; GEN-REDIM (C434) is the canonical GEN base. Citation rule: 6/8-structure GEN composition behavior must be cited from GEN-REDIM (C434: S1 ANS=2 TRIES=29, S2 ANS=219 TRIES=43, S4 ANS=-2 TRIES=48 clean decline), never from the GEN-STRESS K2/K3/K5 corrupted runs. The corrupted outputs remain valuable only as the defect's empirical signature."

Why: the synthesis already recorded GEN-REDIM as canonical (C434) and carried the C429-exploratory caveat, but did not state the explicit canonical-base rule or the citation rule from the defect audit. This note closes that gap. No verdict or priority changed.

## Reviewed and left unchanged (with reason)

- **gen_stress/PREREG.md, NAMECHECK.md, REPORT.md**: the primary records of the GEN-STRESS experiment itself. The corrupted S1/S2/S4 runs are the defect's empirical signature, which the audit explicitly preserves as valuable. REPORT.md already carries the standing warning that the frozen artifact's addressable MAP count is 4.
- **gen_redim/PREREG.md, NAMECHECK.md**: cite GEN-STRESS only for the S1-S5 *predictions* being re-run, the frozen setup reuse, and the S2 hand-derivation errors. These are legitimate historical references, not citations of corrupted results as composition behavior.
- **gen_redim/REPORT.md**: cites GEN-STRESS for the original predictions, the S2 TRIES=48 correction, and "as characterized by GEN-STRESS" (defect characterization). Legitimate.
- **defect_audit/DEFECT_AUDIT.md**: the source of the citation rule itself. Unchanged.
- **composition_synthesis/COMPOSITION_SYNTHESIS.md** other GEN-STRESS mentions (C410 entry, gap 7 "5+ structure wall"): cite C410 only for the boundary/defect characterization, which the audit explicitly permits. Unchanged.

## Governance notes

- The frozen GEN-NM10 prereg commit (a256719a1) retains its original text in git history; the working-copy change above is a citation-target correction per DEFECT-AUDIT recommendation 2, applied transparently. Prediction content, kill bars, and verdicts are untouched.
- No file outside the citation-hygiene lane, gen_nm10/, and composition_synthesis/ was modified.
- Canonical base going forward: GEN-REDIM (C434). The frozen GEN base remains superseded for any future battery registering more than 4 MAPs.
