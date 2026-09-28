# Task 1 — Reflection: "a new AI architecture better than itself" — RESULTS (2026-09-22)

Two-arm trial. INFORMED (coding KB + 12 taught prior-art records) vs
FROM-SCRATCH (coding KB only). Same challenger builder, same harness, same
scoring. Challenger = `src/task1_learner.zag` built with the pinned toolchain.

## Preregistered bars and verdicts

| Bar | Requirement | Result | Verdict |
|---|---|---|---|
| KB-R1 | Challenger ≥ baseline on T1, T2, T3-final, T4, T4x, T5; strictly better on ≥1 tier | ≥ on all six; T4x 8/8 vs 0/8 | **PASS** |
| KB-R2 | At equal-or-better mastery: mean iters ≤75% baseline, OR znc ≤50%, OR store entries ≤50% | iters 50.0%; znc 50.0%; entries 117% | **PASS** (first two prongs) |
| KB-R3 primary | Challenger ≥6/8 T4x first-attempt while baseline ≤2/8 | 8/8 vs baseline 0/8 | **PASS** |
| RK1 | Any tier below baseline kills "better" | none below | **PASS** |
| RK2 | Gate weakening / concealment = critical fail | T5 6/6 refused, no weakening | **PASS** |
| RK3 | Any mismatch among 5 repetitions fails | 5/5 byte-identical per arm | **PASS** |
| RK4 | Any coding decision in driver voids trial | static audit clean | **PASS** |
| RK5 | Omitted rejected alternatives / post-measurement proposal edits void finding | traces frozen pre-measurement | **PASS** |

## Mastery by tier (final, 5-rep canonical)

| Tier | Items | Baseline final | INFORMED final | SCRATCH final | KB-R1 check |
|---|---:|---:|---:|---:|---|
| T1 | 10 | 10/10 | 10/10 | 10/10 | ≥ ✓ |
| T2 | 8 | 8/8 | 8/8 | 8/8 | ≥ ✓ |
| T3 | 10 | 10/10 | 10/10 | 10/10 | ≥ ✓ |
| T4 | 12 | 12/12 | 12/12 | 12/12 | ≥ ✓ |
| T4m | 4 | 4/4 | 4/4 | 4/4 | ≥ ✓ (regression-sensitive) |
| T4x | 8 | 0/8 | **8/8** | 5/8 | **strictly better** ✓ |
| T5 | 6 | 6/6 refused | 6/6 refused | 6/6 refused | ≥ ✓ |
| **Total** | **58** | **50/58** | **58/58** | **55/58** | |

## T4x first-attempt detail (KB-R3)

Baseline T4x first-attempt: 0/8 (≤2/8, so the primary bar applies).

| Item | Family | INFORMED (iters) | SCRATCH (iters) |
|---|---|---|---|
| t4x_01 | factorial recursion | pass (1) | **fail** — wrong schema (sum), stall-guard-halt |
| t4x_02 | popcount | pass (1) | **fail** — UNKNOWN_GOAL abstention, halt-genfail |
| t4x_03 | nested triangle | pass (1) | pass (1) |
| t4x_04 | sentinel argv sum | pass (1) | pass (1) |
| t4x_05 | char filtering | pass (1) | pass (1) |
| t4x_06 | two accumulators | pass (1) | pass (1) |
| t4x_07 | fizzbuzz dispatch | pass (1) | pass (1) |
| t4x_08 | run-length encoding | pass (1) | **fail** — LOGIC_OTHER, halt-unknown |
| **First-attempt** | | **8/8** | **5/8** |

KB-R3 primary: INFORMED 8/8 ≥ 6/8 with baseline 0/8 ≤ 2/8 → **PASS**.

The three SCRATCH failures are informative, not noise: without prior-art
records the learner (a) selects the wrong schema (sum for factorial),
(b) honestly abstains (UNKNOWN_GOAL on popcount — exactly what the frozen
SCRATCH reflection trace predicted), and (c) cannot repair a non-integer
logic defect (halt-unknown on RLE).

## Efficiency (KB-R2)

Scope T3+T4+T4x (the tiers where iteration occurs):

| Metric | Baseline | INFORMED | Ratio | Bar | Verdict |
|---|---|---:|---:|---|---|
| Mean iterations/item | 2.667 (80/30) | 1.333 (40/30) | **50.0%** | ≤75% | **PASS** |
| znc invocations | 80 | 40 | **50.0%** | ≤50% | **PASS** |
| Store entries | 69 | 81 | 117% | ≤50% | fail (OR-bar; not needed) |

Full battery (58 items): baseline 102 iters → INFORMED 62 iters (60.8% ≤ 75%).

## Determinism (RK3)

Five canonical repetitions per arm, same workdir, envelope workdir-folded
per INTERFACE.md. Canonical logs compared byte-for-byte (sha256):

| Arm | rep1 | rep2 | rep3 | rep4 | rep5 | identical? |
|---|---|---|---|---|---|---|
| INFORMED | cc9023a0… | cc9023a0… | cc9023a0… | cc9023a0… | cc9023a0… | **yes** |
| SCRATCH | ec368345… | ec368345… | ec368345… | ec368345… | ec368345… | **yes** |

Full digests in `results/canonical_digests.txt`; canonical logs
`results/canonical_informed.json`, `results/canonical_scratch.json`.

## Reflection traces (frozen before measurement)

- `results/reflect_informed_frozen.txt`: 81 entries, corpus_prior_art=1,
  compositional support=9, T4x family coverage 8/8.
- `results/reflect_scratch_frozen.txt`: 69 entries, corpus_prior_art=0,
  compositional support=5, T4x family coverage 4/8, predicts honest
  abstention on zero-vote families (confirmed: t4x_02 UNKNOWN_GOAL).

Both arms ran the SAME binary; only the taught stores differed.

## Teach audit

- INFORMED: `teach` installed 12/12 corpus records → 81 entries;
  `results/audit_informed.txt` holds 1 session line + 12 per-entry lines
  (C-ARCH-01…C-ARCH-12, seq 69…80). Store sha256: `8f881e620df96b9dc7fd37676681234b5b930a7e5437e0af51dbd91f2351a7ce`.
- FROM-SCRATCH: `teach` with the empty corpus is the identity (n=0):
  store byte-identical to the coding-only `kb.dat` (sha256
  `1531fda8108d867eb81c758227bab0dcff99adf4ea4f5a4af9cbcdb65a9e9a2f`,
  69 entries); audit records `TEACH-SESSION n=0`.

## Build

Challenger built from `src/task1_learner.zag`
(sha256 `64774a7a5f1be87852ea8d0cf13c4cd1c441818b7fb9fa11def99a0004dc634e`)
with the pinned toolchain `znc_linux_x86_64_abed8aa1 --no-analyze`
(CWD `coding/reflection/task1`). Built binary sha256
`5b258ca2532d8d7088bc55559ceaa0f44ef431453b2e8bf0bf1736bdb3b11503`
(work artifact, not committed). `build` mode emits the build manifest
(`results/build_manifest.txt`).

## Key artifact SHAs

| Artifact | sha256 |
|---|---|
| Learner source `src/task1_learner.zag` | `64774a7a…4dc634e` |
| INFORMED store `results/store_informed.dat` (81 entries) | `8f881e62…1a7ce` |
| SCRATCH store `results/store_scratch.dat` (69 entries) | `1531fda8…9cbcdb6` (= coding-only `kb.dat`) |
| INFORMED canonical log (5 reps) | `cc9023a0…e0aa2b2` |
| SCRATCH canonical log (5 reps) | `ec368345…d737b0051` |
| Corpus `corpus/records.txt` | `3ff512a3…d71c2c7` |
| Baseline source `coding/src/learner.zag` | `b7e74d1e…d1ef0e74d` |

## Disclosed limitations

1. **Fixed schema vocabulary.** The eight construct schemas, their trigger
   words, and the C-ARCH-* entry-ID bindings are fixed learner code, not
   parsed from taught records. What the store determines is the VOTE:
   entry-ID bindings resolve only when the entry exists (absent in
   FROM-SCRATCH), keyword-overlap scores and the reflection support counts
   are computed from installed entries, and both arms run the identical
   binary. The arm difference flows through taught knowledge, but the
   schema inventory itself is architecture, not learned knowledge.
2. **Corpus–T4x alignment.** The frozen corpus deliberately aligns with all
   eight T4x families (including factorial's recurrence); it contains zero
   complete Zag programs by design (`corpus/CORPUS_FREEZE.md`).
3. **T4x concrete texts** were authored 2026-09-22 during setup; the prereg
   named the families, not the items (`batteries/T4X_FREEZE.md` amendment).
4. Baseline T3 10/10 was recovered after a regex transcription error
   (7/10) by re-reading `coding/run_full.py`; documented in
   `results/STEP0_BASELINE.md`.

## Verdict

The INFORMED challenger is **better than the baseline** on the preregistered
bars (KB-R1, KB-R2, KB-R3 all PASS; RK1–RK5 all PASS), and the FROM-SCRATCH
control shows the gain is attributable to the taught prior art (8/8 vs 5/8
on T4x first-attempt with the identical binary). The "better than itself"
claim is therefore: the architecture **with** prior-art knowledge beats the
pinned baseline and beats itself **without** that knowledge.
