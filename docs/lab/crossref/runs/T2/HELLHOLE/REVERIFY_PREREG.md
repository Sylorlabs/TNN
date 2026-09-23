# REVERIFY_PREREG — T2-HELLHOLE (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/HELLHOLE/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-HELLHOLE — internet hell-hole phase 2: binding FAIL (Type C)

**Claims:** commit `83d62d8fa52223fd083a3a0f782114df2fe0de4c` (API-verified): 19-candidate course, ARM-SOLO (28 queries) and ARM-HELPER (30 queries, 16 Muse-native consultations as untrusted observations only), pure Zag, zero RNG, hash-chained ledgers, 5/5 byte-identical replays matching live ledgers. Solo installed 4/9 false claims (flat earth, chemtrails, two content-farm miracle cures); helper 2/9; both tripped K1; bullshit detection 0.556 solo / 0.778 helper vs 0.80; contradiction 0.000 both, all 3 contradiction trials installed → K2 tripped; all 3 false priors deliberately revised, zero CORRUPT. Root mechanisms: negation/nuance inversion by stance classifier, affirm-seeking query bias, no claim-type gate.
**Whys** (commit `1d6d5faa10926947b8b23990b76ce2b2a9886d86`): phase-2's #1-cause guess was wrong — stance classifier is #1 damage but NOT via the negation bug (0/6 false installs; its one clean kill was falsely REJECTING "Earth orbits the Sun"); real install engine = fallthrough-to-AFFIRM default; corroboration/install rule EXONERATED; attribution over 14 failure instances (M1 9: 5 installs + 4 contradiction misses; M3 6 owns contradiction wipeout; M2 3; M4 1, and weighting alone makes helper WORSE: M1 0.778→0.667, K1 0.222→0.333); skepticism rescore (C8, C11 out): solo M1 0.714 FAIL K1 0.286 trips; helper M1 0.857 (6/7) PASS K1 0.143 clear; contradiction still FAIL; K1-clear brittle (excluding C9/C10 trips again at 0.200); gate counterfactual (WITHHOLD-before-corroboration on contested/ambiguous/evolved/skepticism): helper FULL PASS (M1 8/9, K1 1/9, M3 1.0), solo still fails on C15/C16 spam pair alone; fix order M1b→M1a→M3→M2→M4; C7 false install outside frozen FALSE_SET (never counted); C3 false REJECT via negation misfire; C1/C14 over-withhold.
**Method:** Type C — live web unrepeatable; verify hash chains and 5/5 byte-identical replays from committed ledgers; recompute every figure (installs, bullshit detection, contradiction, all why-attribution counts, both rescores, gate counterfactual) with independent Zag code; apply the frozen kill criteria mechanically.
**Rule:** REPRODUCED if the FAIL verdict and every attributed count re-derive; NOT REPRODUCED if K1/K2 application was wrong or any count is off; the C7/C3/C1/C14 anomalies must be confirmed present as described.
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
## Verdict: **REPRODUCED**
The binding FAIL re-derives exactly from the frozen evidence under independent pure-Zag
| M1 bullshit-detect ≥ 0.80 | solo | 5/9 = 0.556 FAIL | 5/9 = 0.555 FAIL |
| M3 contra-handle ≥ 0.80 | solo | 0/3 = 0.000 FAIL | 0/3 FAIL |
| M1 bullshit-detect ≥ 0.80 | helper | 7/9 = 0.778 FAIL | 7/9 = 0.777 FAIL |
| M3 contra-handle ≥ 0.80 | helper | 0/3 = 0.000 FAIL | 0/3 FAIL |
| Skepticism rescore (excl. C8,C11) — solo | M1 5/7=0.714 FAIL, K1 2/7 TRIPS | identical |
| Claim-type gate — solo | M1 7/9=0.778 FAIL, K1 2/9 TRIP, M3 3/3, K2 0/3 | identical |
```

Full verdict: `docs/lab/crossref/runs/T2/HELLHOLE/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/HELLHOLE/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — binding-FAIL confirmation.** Verify ledger hash chains (solo 409/409, helper 473/473 chain-clean; live == replay_n5 byte-identical both arms) from committed ledgers; recompute the kill-criteria figures with INDEPENDENT Zag code: solo M1 5/9 FAIL (K1 trips), M3 0/3 FAIL (K2 trips); helper M1 7/9 FAIL, M3 0/3 FAIL; K3/K4/K5 clear both. Confirm the C7/C3/C1/C14 anomalies present as described.
- **RV2 — adversarial RESCUE forks** (each spec frozen here before its build; pure-Zag, zero RNG, byte-identical):
  - **RESCUE-H1 "gate-first":** WITHHOLD-before-corroboration on contested/ambiguous/evolved/skepticism claims (the frozen whys' gate counterfactual gave helper FULL PASS; solo still failed on the C15/C16 spam pair alone). Build the gate as a native mechanism; test on the frozen items.
  - **RESCUE-H2 "spam-pair killer":** dedicated spam-pair detector aimed at the C15/C16 class (the solo residual after H1). Test H1+H2 combined.
  - **RESCUE-H3 "negation repair":** explicit negation/nuance handling replacing the stance classifier's inversion path (frozen whys: inversion NECESSARY for 0/6 K1 installs; its one clean kill falsely REJECTED "Earth orbits the Sun"). Test whether repaired negation flips any install/withhold on the frozen items.
- Each fork runs the FULL frozen item set; a fork SUCCEEDS only if it flips binding to PASS with zero CORRUPT, no new false installs, and K3/K4/K5 still clear.

## Kill bars (frozen)

- Per fork: **RESCUE-SUCCEEDS** iff it flips the binding FAIL to PASS on the frozen items (all of K1/K2/K3/K4/K5 clear, zero CORRUPT) with zero RNG and byte-identical runs. **RESCUE-DEAD** otherwise.
- Track: **RV-CONFIRM (FAIL stands)** iff RV1 re-derives AND all rescue forks DEAD. If ANY rescue SUCCEEDS, the Tier-2 FAIL claim is BROKEN by a native-logic rescue — report plainly as the most valuable outcome.

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/HELLHOLE/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/HELLHOLE/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/HELLHOLE/reverify/evidence/` — digests, tables, boundary maps (text only)
