# RESULTS: Lie-catcher redesign (delib_f4.zag) — 2026-09-22

Frozen prereg: PREREG_LIECATCHER_REDESIGN.md (committed alone first).
Correction: LIECATCHER_CORRECTION.md.
Evidence: scored_evidence/f4_{falsehood,truth,unseen}_rep{1,2,3}.txt + .sha256.

## Bar table (all frozen, all must pass)

| Bar | Result | Detail |
|---|---|---|
| B1 falsehood: 12/12 b12_false -> WITHHOLD | PASS | 12/12 WITHHOLD, all reason F2 (contradiction with learned fact) |
| B2 truth: 12/12 b12_true -> ENDORSE | PASS | 12/12 ENDORSE, all reason T2 (fact consistency) |
| K-LC1 no-test-strings | PASS | verify_f4.py: no test-item string or >15-char substring in source or corpus; every corpus line textually differs from every test line; removed helpers absent |
| K-LC2 determinism | PASS | 3/3 reps byte-identical per cell, sha256 logged |
| K-LC3 abstention | PASS | unseen_keys: 3/3 no F2 (ENDORSE|D — honest abstain, default deliberation) |
| K-LC4 no-profile-regression | PASS | all 7 speech-act matchers byte-identical to delib_sa.zag |

## Verdict
H-LC1 SURVIVES: the falsehood leg passes with zero baked-in world
knowledge. The mechanism is an episodic fact ledger — claims parsed to
(sorted subject-key, numeric-claim), contradiction-checked against an
independently authored experience corpus. Corpus phrasing differs from
test phrasing; the normalized keys are what meet.
