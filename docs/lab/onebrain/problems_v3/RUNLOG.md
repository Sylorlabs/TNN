# RUNLOG — onebrain Experiment 2 problem-set builder

All times UTC. Workdir: `~/workspace/onebrain/problems/`.

## 2026-09-27 ~06:17 — source retrieval

- Fetched frozen prereg via GitHub API: `docs/lab/onebrain/PREREG.md` @ commit
  `1ab40adceff78d71460b992b078508acea7e8abc` (branch `tnn-native-lab`).
  Saved raw JSON (`prereg_raw.json`) and the document (`PREREG_FROZEN.md`).
  GitHub blob SHA: `e0244fc509412ded57820657a3591b3ca50212fd`.
- Fetched `docs/lab/dialogue/round4/ROUND4_REPORT.md` for failure-mode inspiration
  (untaught predicates, role reversal/entity overlap, deletion/world-event
  ambiguity, dimension mismatch, correction-state handling). New cases were
  written from these patterns, not copied.
- A full shallow clone was attempted, ran ~133 s, then intentionally terminated
  (repo too large); API retrieval used instead. No partial clone dir remains.

## 2026-09-27 ~06:18 — generator v1 + freeze v1

- Wrote `gen_problems.py` (v1): 32 problems, 8 per category
  (entity/predicate/scope/correction), each with ≥2 readings, validated
  (unique ids, no tabs/newlines, separators unique, expected answer among readings,
  no duplicate answers, correct-reading position balanced 16 A / 16 B).
- Generated `problems.tsv`, `problems_redacted.tsv` (id/query only, for the
  implementer sibling), `answer_key.tsv` (local scoring key).
- FROZE v1: 2026-09-27 06:19:53 UTC,
  sha256=`133965b6e9a3f3c54436900a7de1cd269356baaa157d41b39e243a17cdd09a9e`.

## 2026-09-27 ~06:19–06:21 — baseline build (design fixed before first scored run)

- Wrote `baseline.zag`: pure Zag, zero RNG. Fixed integer score per reading:
  3×(distinct reading/context content-word overlap)
  + 5×(distinct reading/query content-word overlap)
  + 4×(recency hit: reading names latest-turn entity)
  + 6×(correction-marker/response agreement)
  − (content-word-count / 16). Argmax; ties → lowest reading id.
  Reads readings only; never `expected_answer`.
- Initial raw `write(2)` output helper returned -9; corrected to `_zag_print`
  BEFORE the first completed measurement. (Scratch probes `scratch_hello.*`,
  `scratch_write.*` removed afterward.)
- Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Build via `build_baseline.sh` → `baseline_bin`. (Analyzer emitted a
  false-positive loop warning for the discarded raw-write helper; clean after fix.)
- Design documented in `BASELINE.md` before any scored run.

## 2026-09-27 06:21 — v1 measurement (superseded)

- Three runs of `baseline_bin problems.tsv`: byte-identical,
  output sha256=`3187e9487210e3a8ba30fd3a4644cb42dd72601611a7acd5bf1b38f4c8b77d38`
  (32 lines each).
- Accuracy: 26/32 = 81.25% (E 8/8, P 6/8, S 5/8, C 7/8).
  Misses: P05, P08, S02, S03, S08, C01.
- Verdict: TOO EASY for the prereg's "single deliberation is known to struggle"
  requirement. Triggered the task's explicit re-freeze mechanism (dated note).

## 2026-09-27 06:21:40 — re-freeze v2 (superseded)

- `gen_problems.py` rewritten (v2): readings only; ids/queries/answers/categories
  unchanged. Both readings made comparably substantive and plausible.
- problems.tsv sha256=`fa9624ecf2e2cb565118acc538d1282c9f1db5f7e28018e776562cb0f581277a`.
- Baseline binary/code UNCHANGED; no v2 run before the freeze entry.
- Three runs byte-identical. Accuracy: 28/32 = 87.5% (E 8/8, P 6/8, S 6/8, C 8/8).
  Misses: P02, P03, S03, S08.
- Verdict: STILL TOO EASY — wrong readings still argued a different fact with
  visibly different vocabulary, so bag-of-words overlap favored the correct reading.
  Second dated re-freeze.

## 2026-09-27 06:22:49 — re-freeze v3 (CURRENT)

- `gen_problems.py` rewritten (v3) under a new principle: BOTH readings walk the
  SAME taught facts and differ ONLY in the final inferential step (role order,
  predicate taught-ness, scope of negation/correction/quantifier, dimension word,
  aside-reversion). Lexical overlap is therefore nearly uninformative by
  construction; the disambiguating information is structural. Each reading states
  its inferential step explicitly, so answers remain determinable by careful
  readers. Ids, queries, expected answers, categories unchanged.
- problems.tsv sha256=`2d4d2ea41efa62877f493a92b399371ca6fd0060e2bab9424d9ed98b50e07b0e`.
- Baseline binary/code UNCHANGED; no v3 run before the freeze entry.
  Final redesign; no further iterations before the freeze.
- Three runs byte-identical,
  output sha256=`ee1e138b5d097f49c4ff2eb104c94c5d502b5a7c937c7b36086044b27f5c2240`
  (32 lines each).
- Accuracy: 18/32 = 56.2% (E 3/8 = 37.5%, P 4/8 = 50.0%, S 4/8 = 50.0%,
  C 7/8 = 87.5%). Misses: E02, E03, E04, E05, E07, P01, P04, P06, P08,
  S04, S05, S06, S08, C02.
- Recorded in `baseline_accuracy.md`. This is the FINAL measurement.

## 2026-09-27 ~06:23 — post-measurement verification + cleanup

- Verified current `problems.tsv` SHA matches the v3 FREEZE.txt entry: PASS.
- Verified `problems_redacted.tsv` contains id/query only (no answers): PASS.
- Cleaned scratch: `scratch_hello.zag`, `scratch_hello_bin`, `scratch_write.zag`,
  `scratch_write_bin`, `tiny.tsv`, `run1.err`, `err1.txt`, `.zag-cache/`,
  `.zagd.semantic-ready`.
- Kept: `baseline_bin` (regenerable via `build_baseline.sh`; remove before any
  repo commit per standing rule — no commit is in flight), `baseline.zag`,
  `build_baseline.sh`, `BASELINE.md`, `FREEZE.txt`, `baseline_accuracy.md`,
  this RUNLOG, `gen_problems.py`, `problems.tsv`, `problems_redacted.tsv`,
  `answer_key.tsv`, source-retrieval files (`PREREG_FROZEN.md`, `prereg_raw.json`,
  `ROUND4_REPORT.md`, `kb_round4.txt`).

## Deviations from the task letter

1. The task said "Freeze problems.tsv ... before running the baseline." The
   initial v1 freeze did precede its baseline run. v2 and v3 used the task's own
   explicit restart mechanism ("If you need to edit, restart the freeze with a
   dated note"), each logged in FREEZE.txt before any run on the new version.
2. v1 scored 81.25% and v2 87.5% — reported here, not hidden; they are
   superseded, not final. The v3 set is the frozen deliverable.
3. v1/v2 `baseline_run*.txt` files were overwritten by each re-freeze's runs;
   their SHAs and accuracies are preserved in this log and FREEZE.txt.
4. No `/tmp` was used for scratch (Lab VM /tmp is a shared 512MB tmpfs);
   all scratch stayed in the workdir and was removed.
5. Expected-answer-bearing files (`problems.tsv`, `answer_key.tsv`) were never
   exposed to the implementer sibling path; only `problems_redacted.tsv`
   (id/query) is sibling-safe.
