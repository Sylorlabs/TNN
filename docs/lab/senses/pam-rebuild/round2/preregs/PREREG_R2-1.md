# PREREG R2-1 — Executable out-of-span warrant (A-HC-1)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_A_contract_property.md` §16 HC-1 (commit 45ec1912). Hypothesis text below is copied verbatim from the debate.

## 1. Hypothesis under test (verbatim from DEBATE_A §16 HC-1)

> **HC-1 — Executable out-of-span warrant (P3+P9).**
> *Rule:* INSTALL only if a bounded deterministic test program derived from the percept PASSES every test, including ≥1 test executed on evidence disjoint from the percept's formation evidence (later time window, second occurrence, or different modality). FAIL or UNRESOLVED on the disjoint test → WITHHOLD. The program, its tests, and the disjoint evidence spans are ledger-bound.
> *Sketched kill bar (frozen, ≥10,000 trials, ≥30% adversarial):* false permanent installs ≤2%; true-install recall ≥80%; ablate the disjoint-evidence requirement → false installs must rise by ≥5× (load-bearing proof); byte-identical reruns. Dies if the gate's safety comes from anything other than the disjoint test.

## 2. What is built

- Pure-Zag percept pipeline producing bounded deterministic percept programs: observations, relational tests, predicted_consequences, result ∈ {PASS, FAIL, UNRESOLVED}, exact source evidence spans, fixed instruction budget, ledger-bound.
- The MEMORY CONTRACT as executable code: INSTALL only if the program's bounded tests ALL pass, including ≥1 test executed on evidence disjoint from formation evidence (declared per task per `R2_FIXTURE_SET.md` disjoint-span declarations). FAIL or UNRESOLVED on the disjoint test → WITHHOLD. All programs, tests, and disjoint evidence spans ledger-bound (hash-chained).
- A `sense` CLI: fixture bytes in → percept records + install/withhold dispositions out, with hash-chained ledger.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials (5,000 normal + 5,000 adversarial, ≥30% deliberately misleading high-confidence inputs).
- All 18 attack families exercised; KB4-relevant: signature-collision families (R2A-SHP-1 occlusion-bar, R2A-TMB-2 harmonic-boost) and fooled-predictor families (R2A-MOT-1 reversed-video, R2A-MOT-2 flicker/two-motion).
- The disjoint-evidence spans named in the contract are the declared spans in `R2_FIXTURE_SET.md` ("Disjoint-span declarations per task"), frozen before the build.
- The load-bearing ablation (disjoint-evidence requirement removed) runs on the identical 10,000 trials.

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60% (the bar that killed B).
- **B2 vs Approach A:** head-to-head judgment-accuracy delta R2-1 − A on identical fixtures; reported (no bar direction claimed in advance).
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured, not asserted).
- **B4 memory-contract proof (LOAD-BEARING HARD KILL):** ablate the contract — run the same percepts through a contract-less install gate. PASSES only if the contract changes install/withhold decisions on ≥10% of adversarial fixtures AND reduces false installs vs the ablated run. Contract-as-decoration → FAIL.
- **B5 KB4:** adversarial false-install rate ≤ 2% (hypothesis's own tighter bar, §5); the round-1 10% bar is superseded by the tighter one.
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance — one idea doing the work of many, judged against the hypothesis's own beauty claim ("every percept carries its own falsification experiment"); (ii) output quality — **PENDING-MICAH: this prereg produces no sensory artifacts**; no artifact half of B7 runs. If artifacts are produced later, they ship with the brief under Debate C's protocol.

## 5. Kill criteria

The hypothesis's own kill bar from DEBATE_A §16 HC-1, applied verbatim and HARDENED:
1. False permanent installs ≤ 2% on the frozen 10,000 trials (≥30% adversarial). Any exceedance kills.
2. True-install recall ≥ 80% (denominator: all correct percepts).
3. Ablate the disjoint-evidence requirement (same-evidence tests only): false installs must rise by ≥ 5× vs the full gate — load-bearing proof that the disjoint test does the work. Dies if the gate's safety comes from anything other than the disjoint test.
4. B4 and B6 are HARD KILLS regardless: fails B4 (contract is decoration) → dies; fails B6 (non-determinism) → dies.
5. **No retroactive bar changes after results.** These numbers were frozen before the build; they do not move when the evidence lands. Amendments go to Micah, never into the analysis.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-1.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-1/`: PREREG_R2-1.md (copy), src/, evidence/, LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
