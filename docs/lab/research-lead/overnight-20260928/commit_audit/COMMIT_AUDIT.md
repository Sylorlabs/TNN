# Commit Audit: Mixed and Swept Commits

## Verdict: AUDIT-COMPLETE

All 12 commits audited. Commit order (prereg before implementation) is preserved in all cases where it applies. No commit requires voiding. Recommendations are annotate or keep; history is not rewritten.

## Method

For each commit: listed files via `git show --stat`, compared commit message against file contents, verified prereg-before-implementation order via `git log` on relevant paths where implementations are present. Audit only; no files modified except this report. No Python used. No em dashes.

## Findings

### 1. 9cef7f9d4 — MIXED (message incomplete)

- Message: "Segmentation architecture review: four hypotheses compared, H4 recommended."
- Files: 43 files under `f2_ood/` (F2 OOD results, binaries, logs) plus `seg_review/SEG_REVIEW.md`.
- Issue: The commit contains two distinct work products (F2 OOD evaluation and segmentation review) but the message names only the segmentation review.
- Order: Not applicable (both are results/reviews; no prereg/impl pair split across this boundary).
- Recommendation: ANNOTATE. Do not rewrite history. Future agents should cite the F2 OOD result and the segmentation review as co-located in this commit.

### 2. 4f0811349 — MIXED (message incomplete)

- Message: "A2 prereg: simpler-explanation attacks on H-CAUSALEXP-CONSTRUCT (frozen before implementation)."
- Files: `adv_simpler/PREREG_A2.md` and `machine_native/PREREG_MNSTRESS1.md`.
- Issue: Two unrelated preregs in one commit; message names only the first.
- Order: Both files are preregs; no implementation in this commit. The mnstress1 implementation (`mnstress1.zag`) landed later in 49270b38a, so prereg-before-implementation holds for that pair.
- Recommendation: ANNOTATE. Both preregs are validly frozen; the message should have named both.

### 3. 49270b38a — MIXED (paper log plus unrelated implementation)

- Message: "Paper: Q3 recruitment logged (internal log)."
- Files: paper edit (2 lines) plus `machine_native/HUMAN_PROTOCOL.md` and `machine_native/mnstress1.zag` (1985 lines).
- Issue: A paper-log commit swept in an unrelated implementation and protocol doc.
- Order: VERIFIED. The mnstress1 prereg (`PREREG_MNSTRESS1.md`) is in 4f0811349, which strictly precedes this commit. Prereg-before-implementation is preserved.
- Recommendation: KEEP with annotation. The paper itself is already treated as a contaminated internal log per standing order; no further action on the paper edit. The implementation's governance is intact.

### 4. 87de47c1c — MIXED (paper log plus adversary result)

- Message: "Paper: H-INTENT-UNIFIED7 SURVIVES (8/8)."
- Files: paper edit plus `seg6_adversary/SEG6_ADV_RESULT.md`.
- Issue: Paper log swept in an unrelated adversary result document.
- Order: Not applicable (result doc, no implementation).
- Recommendation: ANNOTATE. No governance impact on the result itself.

### 5. bd883d969 — FALSE CLAIM in message ("alone")

- Message: "Prereg H-CAUSALEXP1 FROZEN (alone, before implementation): active causal discovery frontier. K-CX-1..7 frozen. Pure Zag."
- Files: `causalexp_frontier/PREREG_CAUSALEXP1.md` AND `proclang_frontier/PREREG_PROCLANG1.md`.
- Issue: The message claims the prereg was committed "alone" but the commit contains two preregs. The claim is false.
- Order: Both files are preregs; no implementation in this commit. No order violation.
- Recommendation: CORRECT the record via this audit (done here). Do not rewrite history. Both preregs remain validly frozen; the "alone" claim is retracted.

### 6. bbcd6eca8 — MIXED (paper log plus unrelated prereg)

- Message: "Paper: H-CAUSALEXP-CONSTRUCT step 9 TRANSFER-PARTIAL logged (internal log)."
- Files: paper edit plus `arena_composition/PREREG_ARENA_COMPOSITION.md`.
- Issue: Paper log swept in an unrelated prereg.
- Order: The swept file is a prereg; no implementation in this commit. No order violation.
- Recommendation: ANNOTATE. The arena-composition prereg is validly frozen.

### 7. d42294620 — MIXED (message incomplete)

- Message: "Race contestant frozen: race_tnn.zag (Program 1 TNN entry)."
- Files: `ddes/PREREG_DDES.md` and `lifetime_race/race_tnn.zag`.
- Issue: A DDES prereg is co-committed with the race contestant; message names only the contestant.
- Order: The DDES prereg here precedes the DDES implementation work; no inversion found. The race contestant freeze is a freeze, not a prereg/impl pair.
- Recommendation: ANNOTATE. Both artifacts are valid.

### 8. 17c97a2cd — MIXED (paper log plus full implementation)

- Message: "Paper: Schema persistence SCHEMA-WINS logged (internal log)."
- Files: paper edit plus `ddes_repair/` (result doc, `ddesr.zag` 636 lines, 3 run logs).
- Issue: A paper-log commit swept in a complete implementation and its results.
- Order: VERIFIED. The DDES repair prereg (`0f10fd0f2`, "Prereg: DDES t*=0 soundness repair frozen. No implementation yet.") strictly precedes this commit. Prereg-before-implementation is preserved.
- Recommendation: KEEP with annotation. Implementation governance is intact.

### 9. 83ead74cb — MIXED (two workstreams)

- Message: "Step D: merged DEVINT1+DEVINT2 curricula, STEP-D-COMPLETE (6/6 kill bars)."
- Files: `arena_inquiry/` (report, scores, contestant) plus `integration_step_d/` (result, merged curriculum).
- Issue: Two unrelated workstreams (arena inquiry and integration step D) in one commit.
- Order: Both are results; no prereg/impl pair split here.
- Recommendation: ANNOTATE. No governance impact on either result.

### 10. f2f6688b5 — MIXED (paper log plus implementation)

- Message: "Paper: F2 ablation logged (internal log)."
- Files: paper edit plus `p1_redesign/` (result doc, `p1proto.zag` 451 lines).
- Issue: A paper-log commit swept in a P1 redesign implementation and result.
- Order: VERIFIED. The P1 redesign prereg (`b236b28ff`) strictly precedes this commit. Prereg-before-implementation is preserved.
- Recommendation: KEEP with annotation. Implementation governance is intact.

### 11. be49e8267 — MIXED (paper log plus binary deletion; attribution impurity)

- Message: "Paper: synergy logged (internal log)."
- Files: paper edit plus `hyp_pop/hyppop_bin` (binary, 72170 bytes deleted).
- Issue: A binary artifact was deleted inside a paper-log commit. The binary belonged to the hypothesis-population work (`e150624a9`), not to the synergy paper log. This is the reported attribution impurity: the deletion is unattributed to any cleanup rationale in the message.
- Order: Not applicable (deletion, no prereg/impl pair).
- Recommendation: ANNOTATE. The binary is confirmed absent from the tree after this commit and was not referenced by later work. Do not restore it without cause. Record here that the deletion occurred in this commit so future provenance queries resolve correctly.

### 12. 69730b4ab — SWEPT (wrong files for the message)

- Message: "Q4 alternative-explanation attack: implementation and results (ATTACK-COMPLETE)." (with a detailed Q4 attack summary in the body)
- Files: `hyp_b/` only (`RESULT_HYPB.md`, `hyp_b.zag`, 3 run logs). No Q4 files.
- Issue: The B worker's files were swept into a broad-stage commit carrying a Q4 message. The proper Q4 attack commit is `73d9637a2`, which contains the actual `q4_altexp/` files and precedes this commit.
- Order: VERIFIED per the B worker's own check (reported to parent): file contents match the worker's final source exactly (md5), and the B prereg (`9e2fbd134`) is a strict ancestor of this commit. Prereg-before-implementation is preserved for hypothesis B.
- Recommendation: ANNOTATE, do not rewrite history. The message is misleading, but the B worker verified content integrity and commit order, and chose not to re-commit to avoid duplication. Cite hyp_b results as committed in 69730b4ab with the message discrepancy noted here.

## Kill bars

- K1 PASS: All 12 commits audited (11 listed plus the swept 69730b4ab).
- K2 PASS: Prereg-before-implementation order verified for every commit containing an implementation (49270b38a, 17c97a2cd, f2f6688b5, 69730b4ab). No inversions found.
- K3 PASS: Recommendations made per commit (annotate in 9 cases, keep-with-annotation in 3 cases, record-correction for the false "alone" claim in bd883d969). No commit is voided; no history rewrite is recommended.

## Notes for the parent

1. The dominant pattern is paper-log commits sweeping unrelated files (6 of 12). This stopped being possible after the standing order to halt direct paper editing, but the historical commits remain.
2. The single false claim is bd883d969's "(alone)". It is retracted here; both preregs in that commit remain validly frozen.
3. The binary deletion in be49e8267 is the only destructive operation in the set. It is annotated, not reversed.
4. No Python was used in this audit. No em dashes in this file.
