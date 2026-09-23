# PREREG R2-7 — Independent discriminative challenge contract (A-HC-5, from Sol)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_A_contract_property.md` §16 HC-5 (commit 45ec1912), candidate from gpt-5.6-sol verbatim in §14. Hypothesis text below is copied verbatim from the debate.

## 1. Hypothesis under test (verbatim from DEBATE_A §16 HC-5 / §14 Sol)

> **HC-5 — Independent discriminative challenge contract (P9+P10; from Sol).**
> *Rule:* INSTALL only if a preregistered challenge, selected to distinguish the claim from its strongest plausible alternative, succeeds using evidence not used to form or select the percept. The challenge must come from a different measurement path or a controlled intervention; re-running the front end does not count. UNRESOLVED or non-discriminating challenges → WITHHOLD.
> *Sketched kill bar (frozen, ≥10,000 adversarial + ≥2,000 true controls):* false permanent installs ≤1% overall and ≤2% in every attack family; true-claim recall ≥80%; ≥90% of wrong high-confidence percepts flagged or left unresolved; no attack family may pass by reusing, transforming, or selecting the original evidence. Dies on any bar — and specifically dies if the challenge separates "looks independent" from "actually discriminates."

Sol's original wording (§14):
> **Independent discriminative challenge contract:** Install a claim only if a preregistered challenge, selected to distinguish it from its strongest plausible alternative, succeeds using evidence not used to form or select the percept. The challenge must be generated through a different measurement path or a controlled intervention; a re-run of the front end does not count. Unresolved or non-discriminating challenges withhold installation.

**Frozen challenge registry (per task — the challenges are preregistered here, not invented at eval):** each task's challenge must name (a) the strongest plausible alternative claim, (b) the predicted outcome under the claim, (c) the predicted DIFFERENT outcome under the alternative, (d) the evidence path (different measurement path or controlled intervention). Example registry entries (the build commits the full registry; the registry is frozen before results): colordisc → alternative "different surface" predicts RGB-split under the neutral-illuminant token (G-span) while the claim "same surface" predicts match; shapetrans → alternative "occluder is the object" predicts contour-closure failure on the unoccluded quadrant (G-span) while the claim predicts closure; motiondir → alternative "reverse direction" predicts phase-inversion on frames 51–100 while the claim predicts phase continuity. **A challenge whose two predicted outcomes do not differ is non-discriminating and is rejected at registry time.**

## 2. What is built

- Pure-Zag: percept pipeline + the frozen challenge registry above + the challenge runner: for each percept, select the preregistered challenge for its task, execute it on evidence disjoint from formation evidence, compare the outcome to the claim's and the alternative's predictions. Succeeds → PASS; matches the alternative's prediction or is non-discriminating → WITHHOLD (UNRESOLVED).
- The MEMORY CONTRACT as executable code: INSTALL only on a successful discriminative challenge; everything else withholds. Ledger-bound challenge outcomes.
- A `sense` CLI: fixture bytes in → claim + selected challenge + outcome + disposition out, hash-chained ledger.

## 3. Fixtures

- Frozen: ≥10,000 adversarially misleading percepts (the R2A adversarial 5,000, each run twice under two challenge-selection variants? NO — variants are not invented; instead: the 5,000 adversarial R2A fixtures plus the 5,000 adversarial-equivalent second presentation under a disjoint corruption of the same family = 10,000 adversarial trials) + 2,000 true controls (2,000 of the R2A normal fixtures with ground-truth claims).
- Per-attack-family false-install ≤2% is measured over the 18 frozen families (no family may pass by reusing, transforming, or selecting the original evidence — audited per family).

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured).
- **B4 memory-contract proof (LOAD-BEARING HARD KILL):** challenge-less ablation (install on claim alone) → the challenge contract must change decisions on ≥10% of adversarial fixtures AND reduce false installs. Contract-as-decoration → FAIL.
- **B5 KB4:** false permanent installs ≤ 1% overall on the 10,000 adversarial trials; ≤ 2% in every attack family.
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance vs the hypothesis's own beauty claim (discrimination, not support — "supporting evidence is cheap; discriminating evidence is the property"); (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria (Sol's kill bar, DEBATE_A §14, hardened)

1. False permanent installs ≤ 1% overall AND ≤ 2% in every attack family, on the frozen 10,000 adversarial trials. Any exceedance kills.
2. True-claim recall ≥ 80% (denominator: the 2,000 true controls). Below kills.
3. ≥ 90% of wrong high-confidence percepts flagged or left unresolved (denominator: wrong percepts at confidence ≥ 700). Below kills.
4. No attack family may pass by reusing, transforming, or selecting the original evidence — per-family evidence-audit; a family that passes on non-disjoint evidence kills.
5. Dies specifically if the challenge separates "looks independent" from "actually discriminates" — i.e., if the challenge registry contains a non-discriminating challenge that the runner failed to reject, the hypothesis is falsified by construction.
6. B4 and B6 are HARD KILLS: fails B4 → dies; fails B6 → dies.
7. **No retroactive bar changes after results.** Frozen before the build; amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-7.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-7/`: PREREG copy, src/ (incl. the frozen challenge registry), evidence/, LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
