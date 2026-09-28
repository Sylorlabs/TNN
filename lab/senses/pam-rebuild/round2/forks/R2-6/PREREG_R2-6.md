# PREREG R2-6 — Disjoint-corroboration PASS (B-HC-3)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_B_self_flagging.md` §7 HC-3 (commit e0458ace). Hypothesis text below is copied verbatim from the debate.
**Purpose:** informational head-to-head vs R2-4 — tests whether the H2 repair and H1's corroboration contract are the same mechanism in different clothes (cross-fork convergence, Debate B §7).

## 1. Hypothesis under test (verbatim from DEBATE_B §7 HC-3)

> **HC-3 — "Disjoint-corroboration PASS" (cross-fork convergence)**
> PASS requires two disjoint spans (or two modalities) to produce the *same normalized program structure* — the (g) requirement strengthened to structural agreement. Note the convergence: this is H1's corroboration requirement (§(c).5) expressed in H2's machinery. *What it tests:* whether the H2 repair and the H1 contract are the same mechanism in different clothes. **Kill bar:** RK-1..RK-7, plus an informational head-to-head vs HC-1 on compute and recall.

**Frozen definition of "same normalized program structure":** two programs are the same iff their test lists are identical after (a) sorting tests by canonical name, (b) replacing evidence-span literals with the span's role tag (formation/holdout), and (c) normalizing numeric thresholds to the frozen per-task EPS values committed with the build. The normalization function is frozen with this prereg's build design (before results), not after.

## 2. What is built

- Pure-Zag: percept program construction as in R2-4, but the PASS rule is strengthened: PASS requires the program constructed on the verdict-producing span and the program constructed on the DISJOINT span (or second modality) to be the *same normalized program structure* per the frozen definition above. Structural disagreement → UNRESOLVED (withhold), never FAIL.
- The MEMORY CONTRACT as executable code with the strengthened PASS rule; the gate dispositions install/withhold/escalate.
- A `sense` CLI: fixture bytes in → both programs + normalized-structure comparison + dispositions out, hash-chained ledger.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials (5,000 normal + 5,000 adversarial). Identical subset to R2-4, so the head-to-head is fixture-identical.
- Adversarial families most relevant to structural agreement: R2A-SHP-1 (occlusion-bar), R2A-SHP-2 (distractor-blob), R2A-MOT-2 (flicker/two-motion), R2A-COL-1 (metamer-pairs) — the traps that change program structure across spans.

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured) — the two-program construction cost is the head-to-head's compute axis vs R2-4.
- **B4 memory-contract proof (LOAD-BEARING HARD KILL):** contract-less ablation → contract must change decisions on ≥10% of adversarial fixtures AND reduce false installs. Contract-as-decoration → FAIL.
- **B5 KB4:** false permanent installs ≤ 3% (RK-1).
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance vs the hypothesis's own beauty claim (structural agreement — corroboration expressed as program identity); (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria (DEBATE_B §7 HC-3, hardened)

1. RK-1 through RK-7 (DEBATE_B §6.3), same thresholds as R2-4: RK-1 ≤ 0.03 false installs / 10,000; RK-2 ≤ 1% wrong-high-conf installed (denominator: all wrong percepts at confidence ≥ 700); RK-3 ≥ 85% correct-high-conf PASS-and-install; RK-4 ≥ 100 installs in the contract-less ablation; RK-5 ≥ 90% wrong-high-conf reach FAIL/UNRESOLVED over independent evidence (this hypothesis claims structural self-consistency, so RK-5 binds); RK-6 ≤ 5% escalations AND p95 ops ≤ 40% of Approach A; RK-7 byte-identical.
2. **Informational head-to-head vs R2-4 (preregistered):** on identical fixtures report compute (ops/trial, bytes/percept) and recall (true-install recall, RK-3 analog). If R2-6 matches R2-4's safety at equal-or-lower compute with equal-or-higher recall, the convergence claim stands (the H2 repair and H1 corroboration are the same mechanism); if it costs more for equal safety, the mechanisms are distinct and the extra cost is measured, not assumed.
3. B4 and B6 are HARD KILLS: fails B4 → dies; fails B6 → dies.
4. **No retroactive bar changes after results.** Frozen before the build; amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-6.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-6/`: PREREG copy, src/, evidence/, LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
