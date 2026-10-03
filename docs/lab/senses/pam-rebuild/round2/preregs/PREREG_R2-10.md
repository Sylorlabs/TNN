# PREREG R2-10 — Emission-Gated Install (C-EC2)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_C_sensory_output.md` §9 EC2 (commit 891f4dae). Hypothesis text and KB-E6 below are copied verbatim from the debate.
**The strong form of "ears outrank metrics":** the install gate is disciplined by human emission verdicts.

## 1. Hypothesis under test (verbatim from DEBATE_C §9 EC2)

> **EC2 — Emission-Gated Install (the strong form of "ears outrank metrics")**
>
> **The hypothesis.** EC1 plus: the install gate is disciplined by human emission verdicts. On the frozen human-judged sample, the fork's install/withhold decisions must agree with the human "witnessed correctly" verdict on ≥90% of trials. This is what it means, literally, for ears to outrank metrics — the human verdict disciplines the memory contract, not just the artifact.
>
> **Kill bars:** all EC1 bars, plus **KB-E6 — gate agreement (human, frozen sample):** install/withhold decisions agree with the human witnessed-correctly verdict ≥90%. Below the bar, the fork dies — its contract does not track what a human recognizes as witnessing.
>
> **Cost note:** this is the expensive, high-information bar. It is proposed as one fork, not the default — EC1 is the default emitting fork; EC2 tests whether human-disciplined installation is worth its cost.

## 2. What is built

- Everything in R2-9 (witness-emission PAM with read-only replay emission), PLUS a human-disciplined install gate: the gate is trained (deliberate audited revision, zero RNG, constitutional veto — same rules as R2-12's revision loop) against human "witnessed correctly" verdicts on a TRAINING sample, then frozen; KB-E6 is measured on the separate frozen EVAL sample. Training sample and eval sample are disjoint and both frozen before the build.
- A `sense` CLI: fixture bytes in → percept records + emission artifacts + human-disciplined dispositions out, hash-chained ledger.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials for mechanical bars (KB-E1/E2/E5) and B5.
- Frozen human TRAINING sample: 200 trials (100 clean / 100 adversarial, disjoint from the eval sample) for disciplining the gate — frozen before the build.
- Frozen human EVAL sample: 200 trials (100 clean / 100 adversarial, disjoint from the training sample) for KB-E6 — frozen before the build. The fork's training never sees the eval sample.

## 4. Bars (all preregistered; mechanical unless marked human)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured); human-trial cost reported as a separate line item (the cost question is part of the verdict).
- **B4 no-interference (LOAD-BEARING HARD KILL):** KB-E5 — percepts and dispositions byte-identical with emission on vs. off. Any difference kills immediately.
- **B5 KB4:** false permanent installs ≤ 3% on the 10,000 trials.
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty — EXERCISED:**
  - (i) mechanism elegance vs the hypothesis's own beauty claim: the human verdict disciplining the contract, not just the artifact — one loop doing the work of verification and beauty;
  - (ii) human verdict per the shared protocol: KB-E3 (≥90% audio / ≥80% visual), KB-E4 (≥90% spoof-catch), and KB-E6 (≥90% gate agreement with "witnessed correctly" on the eval sample). Below any threshold kills.

## 5. Kill criteria (EC1 bars + KB-E6, hardened)

1. All R2-9 kill criteria (KB-E1..KB-E5) apply — any failure kills.
2. KB-E6: install/withhold decisions agree with the human "witnessed correctly" verdict on ≥90% of the frozen eval sample → below kills. The human verdict disciplines the gate; disagreement means the contract does not track what a human recognizes as witnessing.
3. Shared human-verdict protocol applies (see R2-9 §5; same 8 rules — frozen sample, mechanical-first, pre-delivery consistency gate, artifact+brief, double-blind, batching, verdict outranks metrics on the sample, verbatim records).
4. B4 and B6 are HARD KILLS: fails B4 → dies; fails B6 → dies.
5. **No retroactive bar changes after results.** Frozen before the build; amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-10.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-10/`: PREREG copy, src/, evidence/ (incl. artifacts, briefs, human-verdict records, gate-discipline ledger), LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
