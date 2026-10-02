# C1-CLEAN VALIDITY AUDIT

Date: 2026-09-30
Wave: C1-CLEAN

## Knowledge criteria

- K1 (prereg before implementation): PASS. PREREG_C1CLEAN.md committed alone
  in 13e4b1ce3 before any implementation.
- K2 (contestant frozen before worlds): PASS. Freeze commit b8d38d9c8 with
  recorded hashes strictly precedes seed generation.
- K3 (new unseen worlds): PASS. 5 fresh /dev/urandom seeds generated after
  freeze. No old C1 world reused.
- K4 (no contestant modification after worlds): PASS. Post-evaluation hashes
  match frozen values exactly.
- K5 (raw transcripts preserved): PASS. All 15 run directories with
  replies.jsonl, scores.jsonl, state, and costs preserved.

## Validity criteria

- V1 (pure Zag, zero Python): PASS. No .py files under c1_clean/. Zero Python
  invoked for implementation, debugging, verification, or analysis.
- V2 (binary frozen and hash-recorded before world gen): PASS. contestant_bin
  hash 8c7ccf30... recorded in freeze commit before seeds.
- V3 (no binary modification after world gen): PASS. Post-eval hash identical.
- V4 (no Python despite prohibition): PASS. See V1.
- V5 (prereg strictly precedes implementation): PASS. Commit order verified.
- V6 (seeds from /dev/urandom, unseen): PASS. Values not viewed; only hashes
  recorded.
- V7 (worlds byte-identical on regen): PASS. All 5 worlds regenerated
  independently; turns.jsonl and key.json byte-identical.
- V8 (no em dashes in loop docs): PASS. Verified zero em-dash bytes.
- V9 (commits local, owned paths only): PASS. Explicit pathspecs; nothing
  pushed.
- V10 (3/3 byte-identical determinism): PASS. All 5 worlds 3/3 identical.
- V11 (canonical score from W0-W2 only): PASS. Hard worlds reported
  separately as exploratory.
- V12 (research paper untouched): PASS. TNN_RESEARCH_PAPER_20260929.md
  not modified.

## Disclosed issues

1. Hard-world denominator: prereg said 64, actual is 67. Reported as X/67
   with disclosure. Canonical unaffected (63 each).
2. H0 L3 law-revert miss: systematic, deterministic, world-dependent.
   Genuine mechanism boundary for future work.

## Verdict

**C1-CLEAN-PASS**
