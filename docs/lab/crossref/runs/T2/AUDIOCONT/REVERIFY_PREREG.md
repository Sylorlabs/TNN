# REVERIFY_PREREG — T2-AUDIOCONT (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/AUDIOCONT/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-AUDIOCONT — audio continuity round 2: hypotheses killed/refined (Type A/C)

**Claims:** test head `070c94cb46084c204433bf1d6d3567b4ebf574b3`, red-team head `f2c7b85e8f4e5ab3fc222d09832d1584e2fe0a6c`: six preregistered Sol/Grok-4.6 hypotheses tested in pure Zag, zero RNG, byte-identical — Sol-H2 bridge seams and Grok-G3 density stress KILLED; Sol-H3 frozen-bed material VOID/INDETERMINATE (test changed arrangement not material; corpus too small); Sol-H1, Grok-G1, Grok-G2 REFINED with claimed mechanisms contradicted despite letter-level survival; no hypothesis warranted v4 recomposition; B-β/B-γ v3 flagship scans: no missed unintended cutouts; longest sub-floor runs were the scored/preserved endings; H1 990ms runs only in variant seeds. Recorded defect (excluded from the verdict, tracked separately): the three blinded ear packages structurally deviate from the frozen prereg and must be rebuilt before presentation.
**Method:** rerun the six hypothesis tests from committed sources in clean checkout (Type A); Type C re-derivation of the flagship-scan no-missed-cutouts claim from committed scan records.
**Rule:** REPRODUCED if all six dispositions match; NOT REPRODUCED if any KILLED hypothesis survives or any REFINED mechanism is confirmed.
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
# VERDICT — T2-AUDIOCONT (replacement crew)
> **Rule:** REPRODUCED if all six dispositions match; NOT REPRODUCED if any KILLED hypothesis survives or any REFINED mechanism is confirmed.
## VERDICT: REPRODUCED
```

Full verdict: `docs/lab/crossref/runs/T2/AUDIOCONT/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/AUDIOCONT/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — independent re-measurement.** Fetch committed sources (`redscan.zag` IS committed; scan records committed). Rebuild the measurement path in a clean workdir; re-measure flagship scans B-beta (590ms @28.71s) and B-gamma (1300ms @28.70s) from committed scan records. Expect byte-identical to committed scan records. Instrument cross-check (independent implementation of the measurement).
- **RV2 — exact statistical re-derivation of the six dispositions** via an INDEPENDENT implementation path (different code than the T2 crew's; cross-check the Zag numbers with an independent exact-test implementation): sol-H2 KILLED (299/300 edges; 3/4 measures oppose, p~0.98-1.00 against); grok46-G3 KILLED (Wilcoxon one-sided p=0.1875 -> 0.19 exact); sol-H3 VOID/INDETERMINATE; sol-H1 REFINED (sign-test p 0.942340/0.868412 exact); grok46-G1 REFINED (ratios 0.71-2.16 <2.4); grok46-G2 REFINED (min ratio 1.19 <2.7, no monotonic decline).
- **RV3 — replication-strength boundary map.** Enumerate every re-derived figure and mark its dependency class: (a) re-executable from committed sources; (b) re-derivable from committed records only; (c) requires the uncommitted raw Type-A render battery (r2g.zag/r2b harness, patch/analysis scripts, renders). Quantify exactly how far replication extends without the battery — which claims are fully re-executable vs record-bound.

## Kill bars (frozen)

- **RV-CONFIRM** iff all six dispositions re-derive exactly AND flagship scans re-measure byte-identical AND the RV3 boundary map is complete (every figure classified).
- **RV-BROKE** iff any disposition flips, or any scan record fails to re-measure, or a figure claimed re-executable requires the missing battery.

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/AUDIOCONT/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/AUDIOCONT/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/AUDIOCONT/reverify/evidence/` — digests, tables, boundary maps (text only)
