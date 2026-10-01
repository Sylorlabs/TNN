# NAMECHECK.md: H3-Lite Prereg Freezer

## Step 0: Toolchain guard (mandatory)

- Safebin activated: `export PATH="$HOME/safebin"` run at session start.
- `which python3 python` returned nothing (verified: output was only "guard-check-done").
- Zero forbidden executables invoked. This worker used only: git, shell builtins, file reads/writes.
- Pure-Zag rule: no computation was performed by this worker (freeze only, no code, no builds, no experiments).

## Scope

Freeze the H3-lite preregistration per Micah's 2026-10-01 07:18 PDT authorization.
Freeze ONLY. No implementation. No source changes.
Owned path: `docs/lab/research-lead/overnight-20260928/h3lite_prereg/` only.

## Freeze authorization (from Micah, 2026-10-01)

"Freeze H3-lite as the next diagnostic experiment unless H2 produces evidence that directly invalidates its assumptions."

H2 evaluation is running in parallel and has produced no results as of this freeze. The invalidation condition is NOT triggered. This freeze proceeds.

If H2 later produces evidence directly invalidating H3-lite assumptions, that will be recorded as a separate superseding note. This freeze remains the valid preregistration for the experiment as designed.

## Input provenance (read-only, nothing modified)

- H3-lite draft: commit `dab50dd68`, `h3lite_prereg/H3LITE_PREREG_DRAFT.md` (187 lines, DRAFT-NOT-FROZEN).
- Protected-core brief: commit `092566072` (Alternative C chosen by Micah 2026-10-01).
- Micah's rulings 2026-10-01: APPROVE H3-lite preregistration; Alternative C; structural ops DEFERRED; scope constraints; K-H3 6-element audit; standing metric fields; freeze authorization 07:18 PDT.

## Verification of draft completeness

All required elements confirmed present in `dab50dd68` before freezing:

1. Three policy nodes (trial order, guide template, repair dispatcher), each with: decision moved, learner-state fields, production read path, production write path, triggering experience, discrimination test.
2. K-H3 write-path audit: Micah's 6 elements (decision; fields; read path; write path; triggering experience; sealed behavioral variation) plus 4 failure conditions (a: source literal; b: read-only theater; c: unreachable write path; d: test encodes decision) plus theater rule.
3. Explicit non-claims (6): not learner-authored procedures; not SUF; not L3; no frozen-battery improvement predicted; not inquiry discrimination; not H1.
4. Alternative C boundary: structural opcodes DEFERRED; no ALLOC/LINK/KILL; Alt A rejected; Alt D rejected; Alt B banked.
5. Sealed adversary protocol: independent adversary designs worlds after freeze; one per node minimum; frozen predictions; 3 byte-identical runs; white-box requirement.
6. Standing architectural metric: all 12 fields as reporting requirements.

No required element was missing. No weakening. Only status lines changed (DRAFT-NOT-FROZEN to FROZEN, section 8 updated to freeze record).

## Freeze ordering

H3-lite implementation may NOT begin until this freeze commit exists. This commit strictly precedes any implementation commit.

## Constraints honored

- Freeze ONLY: no implementation, no source changes, no binary built, no TNN-2 modification.
- Zero em dashes (byte-verified before commit).
- Paper untouched: `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md` not read or modified.
- No sealed contents inspected (FW/GW/H2 worlds).
- Nothing pushed. Local commit on `tnn-native-lab` only.

## Verdict discipline

H3LITE-PREREG-FROZEN on commit. The preregistration is FROZEN and governs H3-lite implementation and evaluation.
