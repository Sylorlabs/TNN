# RESULTS: Speaker attitudes from interaction history (delib_att.zag) — 2026-09-22

Frozen prereg: PREREG_ATTITUDE_HISTORY.md (committed alone first).
History: attitude_history.txt (12 episodes, 2 speakers).
Evidence: scored_evidence/att_{spk,spk_utt}_rep{1,2,3}.txt + .sha256.

## Bar table (all frozen, all must pass)

| Bar | Result | Detail |
|---|---|---|
| A1 ambiguity: 10/10 on s_spk from LEARNED attitudes | PASS | 5/5 ALIX WITHHOLD (reason K2, ATT=NEG), 5/5 BRAM ENDORSE (reason G2, ATT=POS) |
| A2 no-simulation | PASS | verify_att.py: no find_speaker_blob/dislike/blob in code, no ';' blob parsing |
| K-AT1 leakage/audit | PASS | ALIX 5 sarc/1 gen -> NEG, BRAM 1 sarc/5 gen -> POS, each count cites >=1 episode line; no episode utterance equals any test utterance |
| K-AT2 determinism | PASS | 3/3 reps byte-identical per cell, sha256 logged |
| A3 unlabeled control | PASS (as designed) | s_spk_utt (no speaker labels): 4/10 on the base path only — attitudes fire only when the speaker is known, no inflation |

## Verdict
H-AT1 SURVIVES: attitudes learned from logged interaction episodes
reproduce the 10/10 speaker-cell score with no simulated input. The
attitude table is auditable episode-by-episode (verify_att.py prints the
citations).
