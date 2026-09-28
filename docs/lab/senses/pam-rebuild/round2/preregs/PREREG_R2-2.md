# PREREG R2-2 — Two-sided adversarially-distinctive signature (A-HC-2)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_A_contract_property.md` §16 HC-2 (commit 45ec1912). Hypothesis text below is copied verbatim from the debate.

## 1. Hypothesis under test (verbatim from DEBATE_A §16 HC-2)

> **HC-2 — Two-sided adversarially-distinctive signature (P4+P8).**
> *Rule:* INSTALL only if the percept's relational signature is nearer to enrolled true exemplars than to a frozen bank of known-false collision patterns, by a preregistered margin, on attack-aware features. Nearer to (or within margin of) a known-false pattern → WITHHOLD. The false bank grows with every caught attack across rounds.
> *Sketched kill bar:* false-install ≤1% under signature-targeted attacks (attacks designed to collide); retrieval accuracy ≥90%; every enrolled false pattern must withhold its own class (no self-collision installs). Dies if a novel collision class installs, or if answering the false-bank regress ("always one attack behind") fails measurably.

**Preregistered margin:** install requires dist(percept, nearest-true-exemplar) + M < dist(percept, nearest-known-false-pattern), M frozen at 0.15 in normalized signature distance units (frozen here; the frozen value is itself testable post-hoc only via amendment).

**False bank (frozen):** enrolled from round-1's caught attacks: G3's harmonic-boost ×1.15 timbre collision, G3's occlusion-bar CIRCLE→TRIANGLE collision, reversed-video block-match collisions, H1's flicker/metamer collisions. Each bank entry = (attack family ID, signature, class it falsely installed). The bank is read-only during evaluation — growth across rounds is a training-time claim, not an eval-time maneuver.

## 2. What is built

- Pure-Zag percept pipeline producing relational signatures on **attack-aware features**: features preregistered per task as the bands the frozen attack families target (harmonic structure for timbredisc, occlusion-robust shape features for shapetrans, direction-phase for motiondir, etc.). The feature list is frozen here, not selected post-hoc.
- The MEMORY CONTRACT as executable code: two-sided distinctiveness check per §1; WITHHOLD when nearer to (or within margin of) a known-false pattern. Ledger-bound distances.
- A `sense` CLI: fixture bytes in → signature + nearest-true/nearest-false distances + install/withhold dispositions out, hash-chained ledger.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials (5,000 normal + 5,000 adversarial).
- Signature-targeted subset (the hypothesis's primary kill surface): R2A-SHP-1 (occlusion-bar), R2A-TMB-2 (harmonic-boost), R2A-MOT-1 (reversed-video), R2A-COL-1 (metamer-pairs), R2A-SHP-2 (distractor-blob) — 2,000 fixtures; false-install ≤1% required on this subset.
- Novel-collision probe: R2A-PTC-2 (glide-through-threshold), R2A-CCN-2 (mixed-illuminant), R2A-MOT-2 (flicker/two-motion) — attack classes NOT represented in the frozen false bank; tests the "always one attack behind" regress directly. Any false install from a novel-collision class kills per §5(3).

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured). Signature bytes counted against G3's 36-byte datum.
- **B4 memory-contract proof (LOAD-BEARING HARD KILL):** contract-less ablation → contract must change decisions on ≥10% of adversarial fixtures AND reduce false installs. Contract-as-decoration → FAIL.
- **B5 KB4:** false-install ≤ 1% on the signature-targeted 2,000-fixture subset; ≤ 2% overall.
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance vs the hypothesis's own beauty claim (two-sided reference doing the work of one); (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria (DEBATE_A §16 HC-2, hardened)

1. False-install ≤ 1% under signature-targeted attacks (the 2,000-fixture subset). Exceedance kills.
2. Retrieval accuracy ≥ 90% (denominator: retrieved memories against ground truth). Below kills.
3. Every enrolled false pattern must withhold its own class — zero self-collision installs. A novel collision class that installs kills the hypothesis (the regress test is measurable).
4. B4 and B6 are HARD KILLS: fails B4 (contract is decoration) → dies; fails B6 (non-determinism) → dies.
5. **No retroactive bar changes after results.** Frozen before the build; amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-2.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-2/`: PREREG copy, src/, evidence/, LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
