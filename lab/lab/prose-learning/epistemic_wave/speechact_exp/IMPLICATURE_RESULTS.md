# RESULTS: Implicature with speaker / situation / goal / indirect-request
# context (delib_impl2.zag) — 2026-09-22

Frozen prereg: PREREG_IMPLICATURE_CONTEXT.md (committed alone first).
Context model: impl_situations.txt (12 situation records).
Battery: impl_ctx.txt (12 items, 6 same-utterance pairs).
Evidence: scored_evidence/impl_ctx_rep{1,2,3}.txt + .sha256.

## Bar table (all frozen, all must pass)

| Bar | Result | Detail |
|---|---|---|
| I1 indirect-request battery >= 10/12 | PASS | 12/12: 6 REQUEST (odd items, correct target object) + 6 LITERAL (even items) |
| I2 all 6 pairs discriminate | PASS | same utterance resolves REQUEST in the action-goal situation and LITERAL in the inform situation for all 6 pairs |
| K-IM1 no-hardcode | PASS | verify_impl.py: no battery utterance or >12-char substring in delib_impl2.zag; every REQUEST cites the matched situation slot + goal class |
| K-IM2 determinism | PASS | 3/3 reps byte-identical, sha256 logged |

## Verdict
H-IM1 SURVIVES: adding speaker + situation + goal + indirect-request
context resolves indirect requests via the context model, with identical
utterances resolving differently by context. No utterance patterns are
hardcoded — the situation records live in the context input, and the
deliberation is a fixed object/state-channel matcher over a general
state lexicon.
