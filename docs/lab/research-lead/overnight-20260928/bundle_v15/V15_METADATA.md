# Bundle v15 Metadata

**Date:** 2026-09-30
**Verdict:** BUNDLE-V15-COMPLETE

## Bundle specifications

- **File:** `~/workspace/tnn-native-lab-20260930-v15.bundle`
- **Size:** 2.0G
- **SHA-256:** `226a50bf01281e7fd67b38236eefb374eca109eed292fad4c0413cf72bf281fb`
- **HEAD captured:** `10a9b2d0dc44e6fd67b3c4a6c65b6e0ea557aa41`
- **Branch:** `tnn-native-lab`
- **Refs:** 69
- **Commits on HEAD:** 3303
- **Verification:** `git bundle verify` confirms complete history
- **Supersedes:** v14 (`d5e3222b6`, 3279 commits)

## Work captured since v14

23 commits since v14 HEAD (`d5e3222b6`):

### Ledger and governance
- `aada2ada7` Ledger cycle 14: C134-C142 appended (142 claims; zero new SURVIVES; L3 zero)
- `f4198107d` Ledger cycle 14 prep draft
- `dd704acd8` Ledger cycle 15 prep draft (C143-C152 proposed)
- `e28682159` Ledger 15 draft updated (C146 to frozen MUL Rung B commit)
- `1c84f8116` Inquiry NAMECHECK correction (9th incident acknowledged)
- `7604f2e5e` Ledger 14 NAMECHECK correction (12th incident acknowledged)

### TNN-1 follow-up
- `f51a3df0e` TNN-1 independent reproduction (REPRO-PASS; byte-identical binary; 35/35 x3)
- `6c40f4238` TNN-1 cognition-line remeasurement (641 lines; 49pct reduction; R_test 5.46)
- `86518edc4` F-INT4 disposition (narrow XCAP claim; no MAP-to-guide mechanism exists)
- `5a3ab340d` F-INT4 Level 1 strengthening (PASS; real MAP node; 2/2; byte-identical)
- `4b36f0c1e` ACT coverage assessment (3/16 covered; 11 missing; recommend 24/24 port)
- `10a9b2d0d` ACT remediation prereg accepted as frozen

### EXECUTE boundary
- `55a7356f2` EXECUTE boundary evidence package (breach documented; reliance map corrected)
- `13f9adac6` EXECUTE placement red team (F-A through F-J all ATTACK-PASS)

### MUL Rung B
- `5924bbdae` MUL Rung B prereg draft (two-level construction)
- `0f7034567` Rung B freeze verification (INCOMPLETE; needs review disposition)
- `3ce154801` MUL Rung B prereg frozen (K1 anchor for implementation)

### DEVINT-CLA2
- `2ed45875d` Unimplemented-elements triage (E6 pairing induction ranked first)
- `d5ec6f6e2` E6 prereg amendment draft
- `8ab5abbdb` E6 prereg amendment frozen (K1 anchor for implementation)

### Process
- `af82536c4` COMP-1 prereg amendment (157-line actual documented)
- `669aeb56b` Python incident audit 3 (10th, 11th, 12th incidents; all self-disclosed)
- `6d2d54d79` Safebin rollout (mandatory restricted PATH for builder workers)

## Process notes

- Working tree verified clean (zero modified tracked files) before each bundle creation.
- Bundle was recreated three times because concurrent workers landed new commits
  mid-task. Final bundle HEAD (`10a9b2d0d`) matches repo HEAD at creation time
  (verified via list-heads comparison).
- The 10th, 11th, and 12th Python incidents all occurred during this window;
  all self-disclosed, zero scientific contamination. The safebin rollout
  (`6d2d54d79`) makes restricted PATH mandatory for builder workers going forward.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` zero-diff verified.
- No sealed FW1-FW9 files accessed during this task.
- The bundle file itself is not committed to the repo (lives in `~/workspace/`).
