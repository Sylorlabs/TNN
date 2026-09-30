# MUL Rung B Prereg Review Disposition

Date: 2026-09-30. Reviewer: Muse (research coordinator).
Prereg: `docs/lab/research-lead/overnight-20260928/mul_rungb_prereg/MUL_RUNGB_PREREG.md` @ `5924bbdae`.
Freeze check: `docs/lab/research-lead/overnight-20260928/mul_rungb_freeze/RUNGB_FREEZE_CHECK.md` @ `0f7034567`.

## Review

I have read the full 488-line prereg. It is substantively complete:

- K1-K4 kill bars defined with exact verification procedures.
- P-MULB1 through P-MULB6 predictions with frozen probe lists and pass thresholds.
- F-MULB1 through F-MULB5 falsifiers, each with a specific kill/downgrade verdict.
- C1-C4 controls including the single-level diagnostic arm and lookup baselines.
- Both-phase oracle audit with rerun sensitivity.
- Graph-property checklists for ADD and MUL with the two-level ablation procedure.
- Revision probes with the negative-Y boundary in scope.
- Frozen vocabulary (section 2), frozen curriculum (section 3) with exact exemplars.
- One-System Rule accounting (section 11).
- Zero TBD/TODO/XXX/FIXME. The only "draft" occurrences are the status line and verdict label.

The design is sound. The two-level construction (ADD from {MOVE, BRANCHEQ, INC, DEC}, then MUL on learner-built ADD via generic CALL) is a genuine new discovery demand over Rung A. The falsifiers are sharp, particularly F-MULB1 (core-ADD smuggling) and F-MULB3 (flat re-derivation). The K3 purity requirement (structural exclusion of core ADD) is the load-bearing constraint.

## Disposition: ACCEPT

The prereg is accepted as frozen. No amendments required.

Note on K4: the prereg is frozen against the current EXECUTE arrangement pending Micah's ruling. Per K4's own terms, if the ruling changes the boundary, the prereg is re-frozen by amendment. This does not block the freeze.

## K1 anchor

This disposition, committed with the status flip to PREREG-FROZEN, is the K1 anchor. The implementation's first commit must strictly follow this commit (verified by git merge-base --is-ancestor before results are examined).
