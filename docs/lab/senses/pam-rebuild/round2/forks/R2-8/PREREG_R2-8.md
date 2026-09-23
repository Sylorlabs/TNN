# PREREG R2-8 — Independent interventional program (A-HC-6, from Grok-4.6)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_A_contract_property.md` §16 HC-6 (commit 45ec1912), candidate from grok-4.6 verbatim in §14. Hypothesis text below is copied verbatim from the debate.

## 1. Hypothesis under test (verbatim from DEBATE_A §16 HC-6 / §14 Grok-4.6)

> **HC-6 — Independent interventional program (P3+P9+P11; from Grok-4.6).**
> *Rule:* INSTALL only if an executable program derived from the percept (i) predicts successfully on ≥1 held-out source whose raw measurements are informationally independent of percept formation (different sensor, later time, or different modality), AND (ii) produces a clear FAIL (residual > 3σ or hash mismatch) on ≥3 adversarial perturbations of that same independent source.
> *Sketched kill bar (frozen, 10,000 adversarial trials):* false-install <0.5%; ≥95% of high-confidence wrongs self-flag FAIL/UNRESOLVED; true-install recall ≥70% on two held-out tasks. Dies if the interventional leg adds no measurable safety over HC-1's observational out-of-span check (ablation decides).

**Frozen interventional leg (hardened):** for each trial the build selects ≥1 held-out source informationally independent of formation (per the R2A disjoint-span declarations); the program predicts on it (leg i), then the SAME independent source is subjected to ≥3 frozen adversarial perturbations drawn from the task's family list (leg ii) and the program must produce a clear FAIL (residual > 3σ under the frozen per-task noise model, or hash mismatch) on EACH of the ≥3. INSTALL only if leg (i) succeeds AND all leg-(ii) perturbations FAIL cleanly. The σ values are frozen per task with the build design, before results.

**Two held-out tasks (frozen):** the true-install recall ≥70% bar is measured on two tasks held out from the design of the interventional perturbations — frozen here as shapetrans and timbredisc. (The perturbation design may reference families from the other four tasks; the recall bar may not see shapetrans/timbredisc families in advance.)

## 2. What is built

- Pure-Zag: executable percept programs as in R2-1, PLUS the interventional leg: held-out independent source selection, leg-(i) prediction check, leg-(ii) ≥3 adversarial perturbations of that source with FAIL assertions (residual > 3σ or hash mismatch).
- The MEMORY CONTRACT as executable code: INSTALL only if leg (i) succeeds AND every leg-(ii) perturbation produces a clear FAIL. Ledger-bound leg outcomes.
- A `sense` CLI: fixture bytes in → program + leg outcomes + disposition out, hash-chained ledger.

## 3. Fixtures

- Frozen 10,000 adversarial trials: the R2A adversarial 5,000, each paired with its independent-source presentation and ≥3 perturbations of that source (the perturbations are frozen per fixture at suite-build time, not chosen at eval).
- The two held-out recall tasks (shapetrans, timbredisc): recall measured on the R2A normal fixtures of those tasks, with ground-truth installs.

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured) — the interventional leg's cost is reported separately from the observational leg.
- **B4 memory-contract proof (LOAD-BEARING HARD KILL):** contract-less ablation → contract must change decisions on ≥10% of adversarial fixtures AND reduce false installs. Contract-as-decoration → FAIL.
- **B5 KB4:** false-install < 0.5% on the frozen 10,000 adversarial trials.
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance vs the hypothesis's own beauty claim (intervention, not observation — the do-operator as the strongest out-of-span check); (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria (Grok-4.6's kill bar, DEBATE_A §14, hardened)

1. False-install < 0.5% on the frozen 10,000 adversarial trials. At-or-above kills.
2. ≥ 95% of high-confidence wrongs self-flag FAIL/UNRESOLVED (denominator: wrong percepts at confidence ≥ 700). Below kills.
3. True-install recall ≥ 70% on the two held-out tasks (shapetrans, timbredisc; denominator: correct percepts in those tasks). Below kills.
4. **Interventional-leg ablation (preregistered decider):** ablate leg (ii) — run the observational out-of-span check only (R2-1's rule). If the full two-leg gate does not measurably reduce false installs vs the leg-(i)-only gate (difference ≥ 0.2 percentage points on the 10,000 trials, in the full gate's favor), the interventional leg adds no measurable safety and dies — the hypothesis is falsified even if bars 1–3 pass.
5. B4 and B6 are HARD KILLS: fails B4 → dies; fails B6 → dies.
6. **No retroactive bar changes after results.** Frozen before the build; amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-8.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-8/`: PREREG copy, src/, evidence/, LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
