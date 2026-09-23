# KB-RECALL — results (frozen battery, 2026-09-22)

**Prereg:** `PREREG-KB.md` (frozen before scored runs). **Toolchain:**
`znc_linux_x86_64_abed8aa1`. Full per-spec log: `hidden_files/recall_results.json`.

## Headline numbers (manual-free recall, first attempt, no repair loop)

| metric | result |
|---|---|
| install determinism (3 runs) | byte-identical kb.dat, identical digest — PASS |
| compile success rate | **24/24 (100%)** |
| test-pass rate | **23/24 (95.8%)** |
| gen determinism (3 runs × 24 specs) | 24/24 byte-identical — PASS |
| gate battery | 6/6 (4 REFUSE, 2 ALLOW) — PASS |

## Per-spec results

| id | family (famscore) | compile | verdict | note |
|----|-------------------|---------|---------|------|
| r1–r3 | E-STRREV | ok | PASS | incl. empty-string edge |
| c1–c3 | E-STRCOUNT | ok | PASS | incl. absent-byte → 0 |
| s1–s3 | E-ARRAYSUM | ok | PASS | incl. no-arg → 0, negatives |
| m1–m3 | E-ARRAYMAP | ok | PASS | incl. a=0, negative scale |
| o1 | E-SORT | ok | PASS | |
| **o2** | **E-STRREV (wrong)** | ok | **FAIL** | selection failure, see below |
| o3 | E-SORT | ok | PASS | negatives + duplicates |
| h1–h3 | E-HASH | ok | PASS | incl. empty → offset basis |
| w1–w3 | E-FILEWRITE | ok | PASS | stdout byte count + file bytes verified |
| f1–f3 | E-FILEREAD | ok | PASS | incl. 0B and 100000B |

## Kill bars

| Bar | Rule | Result |
|-----|------|--------|
| KR-C1 viable recall | < 50% compile-correct → FAIL | 23/24 = 95.8% → **PASS** |
| KR-C2 determinism | any install/gen rerun differs → FAIL | all identical → **PASS** |
| KR-C3 gate | any wrong REFUSE/ALLOW → FAIL (critical) | 6/6 → **PASS** |
| KR-C4 no-guess | unfilled `{{slot}}` or silent substitution → FAIL | none; A2 proves KB-MISS path → **PASS** |

## Ablations (knowledge-flow evidence)

| leg | change | outcome |
|-----|--------|---------|
| A1 | kb.dat minus E-FILEWRITE, gen w1 spec | selected nearest family E-FILEREAD, emitted a compiling wrong-task program — **no refusal, no KB-MISS** |
| A2 | kb.dat minus L-SYSCALL-NUMS, gen w1 spec | `KB-MISS: required auxiliary entry absent for E-FILEWRITE` — **no hallucinated syscall numbers** |

A2 is the load-bearing result: syscall numbers/flags exist ONLY in the
L-SYSCALL-NUMS entry, and without it the learner refuses rather than
inventing values. Knowledge flows from the KB, not the learner binary.

## Honest gaps

1. **o2 selection failure (the 1 miss).** Spec "order integers from smallest
   to largest" scored E-SORT=1 ("order") vs E-STRREV=1 ("order"); the
   lowest-index tie-break picked E-STRREV and emitted a string reverser.
   Word-sense ambiguity ("order" as verb vs noun) defeats single-term keyword
   overlap. The spec was NOT re-worded and the KB was NOT retuned after the
   freeze — the miss stands as recorded. Fix direction (future): phrase-level
   scoring or sense-disambiguating entries, validated on a fresh battery.
2. **A1 shows the fallback is nearest-neighbor, not refusal.** Removing a
   family degrades to the closest surviving family and does the wrong task
   confidently. For safety-relevant families this wants an explicit
   coverage check (a "none of the above" outcome), which does not exist yet.
3. **Recall surface = installed families.** The battery measures recall within
   the 8 installed EMIT families. Anything outside them (graphs, hash maps,
   DP, processes) is KB-MISS by design — correct behavior for Phase 1, but
   the "coding knowledge" claim is bounded by the MANIFEST inventory.
4. **Templates are trainer-authored.** Phase 1 measures recall/application of
   installed knowledge, not de-novo invention of algorithms. The
   INFORMED vs FROM-SCRATCH arms (workstream tasks 1–4) are where invention
   gets tested.
5. **Selection is keyword overlap, not understanding.** `plan` traces show
   sensible support entries, but the mechanism is substring matching over
   `K:` fields. It is deterministic and auditable; it is not comprehension.
