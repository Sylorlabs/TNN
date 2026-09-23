# PREREG R2-5 — Withholding-first ablation (B-HC-2)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_B_self_flagging.md` §7 HC-2 (commit e0458ace). Hypothesis text below is copied verbatim from the debate.
**Purpose:** the ablation deciding whether the self-result field carries any load. If R2-5 matches R2-4's safety with less machinery, the field is decorative — kill it.

## 1. Hypothesis under test (verbatim from DEBATE_B §7 HC-2)

> **HC-2 — "Withholding-first with deliberated promotion" (the self-result ablation)**
> Every percept enters UNRESOLVED and **the program result field is removed entirely** — no self-flagging at all. Promotion to PASS requires either (i) a successful prediction outside the source span, or (ii) deliberation ratification citing the warrant. **Kill bar:** promotion precision ≥ 95% (denominator: promoted percepts); promotion recall ≥ 80% (denominator: correct high-conf percepts); escalation ≤ 5%; RK-1, RK-4, RK-7. *What it tests:* whether the self-result field carries any load. If HC-2 matches HC-1's safety with less machinery, the field is decorative — kill it.

## 2. What is built

- Pure-Zag percept pipeline WITHOUT the program result field: every percept enters UNRESOLVED; the field is absent from the data format (not merely ignored — removed, so no path can read it).
- The MEMORY CONTRACT as executable code: promotion to PASS requires (i) a successful prediction outside the source span, or (ii) deliberation ratification citing the warrant. Promotion decisions ledger-bound with the cited warrant.
- A `sense` CLI: fixture bytes in → percept records + promote/withhold dispositions out, hash-chained ledger.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials (5,000 normal + 5,000 adversarial). Same subset as R2-4, so the head-to-head is on identical fixtures.
- Head-to-head comparison vs R2-4's results on the identical 10,000 trials is preregistered as the informational decider.

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured). The removed field's cost saving is reported explicitly.
- **B4 memory-contract proof (LOAD-BEARING HARD KILL):** contract-less ablation → promotion gate must change decisions on ≥10% of adversarial fixtures AND reduce false installs. Contract-as-decoration → FAIL.
- **B5 KB4:** false permanent installs ≤ 3% (RK-1).
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance vs the hypothesis's own beauty claim (less machinery, same safety — "the field was decorative"); (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria (DEBATE_B §7 HC-2, hardened)

1. Promotion precision ≥ 95% (denominator: promoted percepts). Below kills.
2. Promotion recall ≥ 80% (denominator: correct high-conf percepts). Below kills.
3. Deliberation escalation ≤ 5% of trials. Above kills.
4. RK-1: false permanent installs / 10,000 ≤ 0.03. RK-4: contract-less ablation of the identical suite must produce ≥ 100 permanent installs. RK-7: byte-identical rerun (subsumed by B6; both hold).
5. **Decider rule (preregistered):** if R2-5 matches or beats R2-4 on RK-1, RK-3's analog (promotion recall ≥ 80%), and B4 with strictly less machinery (no result field, no self-flag computation), the self-result field is declared decorative and R2-4's RK-5 claim is closed as load-free. If R2-5 underperforms R2-4 on safety or recall, the field carries load and survives.
6. B4 and B6 are HARD KILLS: fails B4 → dies; fails B6 → dies.
7. **No retroactive bar changes after results.** Frozen before the build; amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-5.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-5/`: PREREG copy, src/, evidence/, LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
