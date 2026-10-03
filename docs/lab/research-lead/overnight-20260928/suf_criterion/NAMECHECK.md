# NAMECHECK: SUF Criterion Formalizer

## Step 0: Toolchain guard (mandatory, recorded first)

- Safebin activated: `export PATH="$HOME/safebin"` before all work.
- `which python3 python` returned nothing (verified 2026-10-01).
- 36 allowed tools only (coreutils, git, pinned znc). No python, no other interpreters.
- All operations in this wave: file reads (`git show`), text authoring, git add/commit.
- Zero forbidden executable invocations. This wave is not PROCESS-FAIL.

## Scope

Analysis ONLY. Formalize the Source-Underdetermined Form (SUF) entrance
criterion for future construction work, per Micah's 2026-10-01 ruling.

## Input provenance (read-only, character-exact identifiers)

- Micah's SUF ruling (2026-10-01, chat): "The entrance criterion for future
  construction work is Source-Underdetermined Form: At least one causal
  structural decision in the production path must be resolved by learner
  history such that the produced form cannot be completely enumerated from
  source alone. SUF is necessary, not sufficient. Future invention requires
  at minimum: SUF AND useful behavior AND learner-internal verification
  AND revisability AND cognitive reuse."
- PROPERTY_DEFINITION.md, commit `64eec921f` (proposal, not a frozen bar):
  formal SUF definition, 4-step operational test, necessity vs sufficiency.
- SUF_CHECK_TNN2.md, commit `8ef148a42`: white-box application to frozen
  TNN-2, all three mechanisms SUF-FAIL.
- H3LITE_PREREG_DRAFT.md, commit `dab50dd68`: H3-lite "does not establish
  SUF by itself. The policy value spaces ... are enumerable from source."
- Micah's continuous-learner clarification (2026-10-01): freeze means freeze
  researcher-authored architecture/source, NOT the learner. FROZEN
  RESEARCHER CODE + CONTINUOUSLY CHANGING LEARNER STATE.

## Constraints honored

- Analysis only. No implementation, no source edits, no binaries built.
- No sealed world contents inspected (hash references only, none needed).
- Frozen TNN-2 source read via `git show` (read-only); never modified.
- Paper untouched. Nothing pushed (local commits only).
- Zero em dashes in deliverables (byte-verified before commit).

## Output

- `SUF_CRITERION.md`: formalization, worked FAIL example (TNN-2
  construction), hypothetical PASS example, white-box evidence requirements.
- Committed with explicit pathspecs, owned path only.
