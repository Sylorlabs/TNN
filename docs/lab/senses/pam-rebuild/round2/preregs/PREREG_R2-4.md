# PREREG R2-4 — H2-gate + calibrated self-flagging (MERGE of B-HC-1 and A-HC-4)

**Status: FROZEN 2026-09-22. Committed alone — before any build output exists.**
**Source debates:** `../debates/DEBATE_B_self_flagging.md` §7 HC-1 (commit e0458ace) MERGED with `../debates/DEBATE_A_contract_property.md` §16 HC-4 (commit 45ec1912). Hypothesis texts below are copied verbatim from the debate docs.

Overlap resolution: B-HC-1 and A-HC-4 are the same mechanism (out-of-span self-result). This prereg keeps **the H2 gate unchanged**, computes the program's self-result **over disjoint evidence spans** (B's (g) cross-validation principle), uses **UNRESOLVED as the default** (B's (b)), and carries the **repaired kill set RK-1..RK-7** from Debate B §6.3. A-HC-4's kill-2 rematch is subsumed into RK-5. The round-1 kill-2 (38.9%) measurement is kept as a **reported diagnostic column**, not a kill — H2 stays dead under its frozen bar regardless; no HARKing.

## 1. Hypothesis under test (verbatim from DEBATE_B §7 HC-1)

> **HC-1 — "H2-gate + calibrated percept self-flagging" (primary)**
> H2's memory contract and gate unchanged. The change is all in *how the program's result field is computed*: PASS requires the program's tests to succeed on ≥ 1 evidence span **disjoint** from the verdict-producing span (temporal holdout, spatial holdout, or cross-modal span) — the (g) mechanism. Default UNRESOLVED; promotion by fresh evidence (b). The gate dispositions install/withhold/escalate (c+h); deliberation ratifies high-stakes promotions and resolves program conflicts (d triaged). Flagger predicates improvable only by deliberate audited revision with constitutional anti-gaming veto (f). **Kill bar:** RK-1 through RK-7. *What it tests:* whether independent-evidence flagging lifts program self-flagging from 38.9% toward 90% without the gate doing all the work.

(Verbatim from DEBATE_A §16 HC-4, merged here:)
> **HC-4 — Calibrated executable self-report (P3 rematch of H2's kill-2).**
> *Rule:* rerun H2's kill-2 bar with programs required to contain ≥1 out-of-span test: ≥90% of wrong high-confidence percepts must reach FAIL or UNRESOLVED *by their own programs*.
> *Sketched kill bar:* self-flag rate ≥90% on wrong high-confidence percepts (the exact bar that killed H2 at 38.9%); false permanent installs ≤3% on 10,000 trials; byte-identical reruns. Dies if executability still can't flag its own errors — which would kill P3 outright, composite included.

**Layer assignment (frozen, Debate B §4-clash-1 resolution):** the gate decides install/withhold/escalate; the program's result field is a triage signal (evidence to the gate, never the verdict); deliberation ratifies only high-stakes promotions and resolves program conflicts (≤5% of trials escalated).

## 2. What is built

- Pure-Zag: H2's memory contract and gate code path unchanged; new result-field computation: the program's tests are executed over ≥1 evidence span DISJOINT from the verdict-producing span (temporal holdout, spatial holdout, or cross-modal span per the frozen R2A disjoint-span declarations). Default result = UNRESOLVED; promotion to PASS only on fresh-evidence success.
- Deliberation-ratification step for high-stakes promotions and program conflicts (triaged ≤5% of trials).
- A `sense` CLI: fixture bytes in → program + self-result (PASS/FAIL/UNRESOLVED) + gate disposition out, hash-chained ledger. Kill-2's original same-evidence self-flag measurement reported as a diagnostic column on every report.

## 3. Fixtures

- Frozen suite R2A per `R2_FIXTURE_SET.md`: 10,000 trials (5,000 normal + 5,000 adversarial). All 18 attack families.
- The paired R2P set is available to the gate at evaluation (admission via R2-3).
- NEW suite requirement satisfied: R2A is the new adversarial fixture set (Debate B recommendation 1); its attack families differ from round-1's H2 families so no flagger can be a post-hoc fit to round-1 traps.

## 4. Bars (all preregistered, applied mechanically)

- **B1 viability:** mean primary accuracy on the frozen 370 harness primary ≥ 60%.
- **B2 vs Approach A:** head-to-head judgment-accuracy delta on identical fixtures; reported.
- **B3 efficiency:** ops and bytes per percept vs Approach A (measured).
- **B4 memory-contract proof (LOAD-BEARING HARD KILL):** contract-less ablation → contract must change decisions on ≥10% of adversarial fixtures AND reduce false installs. Contract-as-decoration → FAIL.
- **B5 KB4:** false permanent installs ≤ 3% on the 10,000 trials (RK-1) — the hypothesis's own bar; round-1's 10% superseded.
- **B6 determinism (HARD KILL):** ≥3 runs byte-identical, hash-chained ledger verified.
- **B7 beauty:** (i) mechanism elegance vs the hypothesis's own beauty claim ("every percept is a claim together with its own experiment"); (ii) **PENDING-MICAH — no sensory artifacts produced.**

## 5. Kill criteria — the repaired kill set RK-1..RK-7 (DEBATE_B §6.3, verbatim, hardened)

- **RK-1** (system safety): false permanent installs / 10,000 ≤ 0.03.
- **RK-2** (gate withholding — replaces kill-2 *as the safety kill*): wrong high-confidence percepts reaching permanent installation ≤ 1%; denominator = all wrong percepts at confidence ≥ 700. (H2's gate scored 0/108.)
- **RK-3** (anti-gaming pair for RK-2): correct high-confidence percepts reaching PASS-and-install ≥ 85%; denominator = all correct percepts at confidence ≥ 700. Withhold-everything dies here.
- **RK-4** (gate load-bearing — from Grok): the identical suite run contract-less must produce ≥ 100 permanent installs. Proves the *gate* does the filtering, not an absence of candidates.
- **RK-5** (program-signal calibration): ≥ 90% of wrong high-conf percepts reach FAIL/UNRESOLVED **computed over independent evidence**, paired with RK-3. (A hypothesis may drop RK-5 only by dropping the self-flagging claim — R2-4 claims it, so RK-5 is binding.)
- **RK-6** (triage/compute): deliberation escalations ≤ 5% of trials AND p95 ops ≤ 40% of Approach A.
- **RK-7** (determinism): byte-identical rerun — subsumed by B6; both must hold.
- Kill-2's original same-evidence self-flag measurement (the 38.9%) stays in the battery as a **reported diagnostic** (not a kill): the 38.9% → ? trajectory is how we tell whether the independent-evidence mechanism worked.
- B4 and B6 are HARD KILLS regardless: fails B4 → dies; fails B6 → dies.
- **No retroactive bar changes after results.** RK-1..RK-7 were frozen before the build; they do not move when the evidence lands. H2 stays dead under its own frozen bar — this prereg tests a NEW hypothesis, not a resurrection. Amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-4.md` (committed ALONE — no src, no evidence).
- Build output (later, separate commits): `senses/pam-rebuild/round2/forks/R2-4/`: PREREG copy, src/, evidence/, LEDGER.md.
- Shared fixtures: `senses/pam-rebuild/round2/preregs/R2_FIXTURE_SET.md`.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Commit via `~/workspace/commit_racefree.py`, lab-relative paths, TMPDIR=`~/workspace/tmp_commit`. No binaries, no .zagd. Verify via GitHub API, report SHAs.

**Laws:** pure Zag, zero RNG in any decision path, byte-identical reruns required, plain language, max-risk posture.
