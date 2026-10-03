# REPORT: corrupted SHA-256 typo sweep (queue item 16), wave-20261002-1121pdt

Lane: RECORDS. Branch: lane-records-20261002-1121pdt. Date: 2026-10-02.

Target string (corrupted, 79 hex chars, not a valid SHA-256):
`a29972ca8183b2857c0c7b262d004fce6e4547c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d`

## The three docs

1. `docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/LEARNER_MECH_ANALYSIS.md`
   FIXED LAST WAVE. Commit 59dc25ece (2026-10-02 09:41 UTC, "RECORDS: fix
   SHA-256 typo in LEARNER_MECH_ANALYSIS.md"). Both occurrences (lines 11,
   15) replaced with the true hash. Verified fixed: no corrupted string
   remains in the file at HEAD.

2. `docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/JUDGE_BRIEF.md`
   FIXED THIS WAVE. Line 82 asserted the corrupted string as the frozen
   TNN-2 core SHA-256 ("re-verified this lane; SHA-256
   `a29972ca...44064ec9d`"). Genuine typo: the string is presented as the
   hash, not quoted as evidence.
   - Old: `a29972ca8183b2857c0c7b262d004fce6e4547c12ff8c05f9ebd9152dddca9efeb2a3b44064ec9d` (79 chars)
   - New: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` (64 chars)
   - Verified independently: `git show
     f4de7ff46:docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag
     | sha256sum` returns exactly the new string; `git ls-tree f4de7ff46`
     confirms blob b226b223cb3ee0be742af673653fb8ea8605f281. Matches the
     fix-commit value and the C186 REPORT.md independent citation.
   - Post-fix grep: zero corrupted occurrences remain in the file.

3. `docs/lab/rsi/runs/wave-20261001-2321pdt/GAP-DOC/GAP_DOCUMENTATION.md`
   INTENTIONALLY LEFT UNCHANGED. Line 121 quotes the corrupted string as
   the subject of MECH-VERIFY transcription-error finding 1 ("Transcription
   errors found by MECH-VERIFY (recorded, none verdict-relevant) ... is 79
   characters long, not a valid 64-character SHA-256"). It is evidence of
   the documented error, and the true hash already appears in the same
   paragraph. Replacing the quote would make the sentence
   self-contradictory and falsify a faithful record.

## Out-of-scope note

The corrupted string also appears in
`docs/lab/rsi/runs/wave-20261002-0221pdt/RECORDS/SUPERSESSION_UPDATE.md`
(line 192) under "Old bytes" documenting the 59dc25ece fix itself.
Evidence quotation; left unchanged.

## Sweep coverage

Scanned every 2321pdt run dir present in the tree
(20260924, 20260926, 20260927, 20260928, 20260929, 20260930, 20261001) for
hex strings of length != 40 (git SHA) and != 64 (valid SHA-256).
wave-20260923-2321pdt does not exist in the tree (historical only; the
queue item's dir list was stale). No other malformed SHA-256 claims found.
One unrelated truncated hash surfaced: the D2_FW.txt frozen-hash line in
wave-20261001-2321pdt/HPIREV2/PREREG_PI_REV2_NARROWED.md (59-62 hex chars);
the red team already qualified it in RT-HPIREV2_REVIEW.md with the true
hash and a corrective. It is a frozen prereg, so no edit was made here.

## Commits

This wave: one pathspec-only commit on lane-records-20261002-1121pdt
covering the JUDGE_BRIEF.md fix, this REPORT.md, and the lane NAMECHECK.md.

No em-dashes anywhere (check_no_dash.sh rc=0). Pure shell text tools only;
python3 never invoked (safebin guard recorded in NAMECHECK.md Step 0).
