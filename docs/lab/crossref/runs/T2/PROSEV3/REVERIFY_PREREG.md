# REVERIFY_PREREG — T2-PROSEV3 (deeper adversarial re-verification)

**Coordinator:** re-verification coordinator (Wave-2 crossref Tier-2 re-verification track)
**Date frozen:** 2026-09-23 (PDT)
**Frozen prereg:** `docs/lab/crossref/PREREG_TIER2.md` @ `7b2100d09911c5c10252c5756c7def288e70bd1f` (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`, SHA-verified via API)
**Tier-2 verdict under re-verification:** see extract below (from `docs/lab/crossref/runs/T2/PROSEV3/VERDICT.md`)

## 1. Frozen prereg section — byte-verbatim from PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f

> The section below was sliced programmatically from the frozen document. It was NOT transcribed.

```
## T2-PROSEV3 — prose v3: KB3-VIABLE FAIL (2/4), v1 pinned (Type A)

**Claims:** commit `4be6b0cf128d` (API-verified): verdict KB3-VIABLE FAIL (2/4), v1 pinned. Honest prereg deviation: implementation expanded the coreference trigger beyond the preregistered order change; 6/11 fixed CORE items came from the unregistered expansion (C2 attribution confounded); frozen A0/A1 comparisons → no scored headline result changed; tier-3 tolerant fallback carried essentially all recovery but raised wrong-value verdicts 8→30/912 while converting ~463 unknowns into values.
**Method:** rerun the v3 battery from committed sources in clean checkout; verify the FAIL (2/4) and reproduce the deviation's quantitative footprint (6/11 CORE, 8→30/912 wrong-value).
**Rule:** REPRODUCED if FAIL (2/4) holds and the deviation footprint matches; PARTIAL if the deviation's impact differs from recorded (name it).
```

## 2. Tier-2 verdict being re-verified (extracted programmatically from the crew VERDICT.md)

```
## Verdict: REPRODUCED
The preregistered claim — **KB3-VIABLE FAIL (2/4)** with the documented
`REPRODUCED` iff FAIL 2/4 **and** the deviation footprint match;
`PARTIAL` if the deviation impact differs. Both conjuncts hold.
| Evidence commit (prereg-named) | `4be6b0cf128d5a443c9e67486f63520816535cca` (API-verified, 2026-09-22T03:28:39Z; message states `KB3-VIABLE FAILS (2/4)`) |
## Headline: KB3-VIABLE FAIL (2/4) — reproduced
**2/4 → KB3-VIABLE FAILS**. The frozen A0/A1 baselines are unchanged, so no
**REPRODUCED.** KB3-VIABLE FAIL (2/4), and the full deviation footprint —
```

Full verdict: `docs/lab/crossref/runs/T2/PROSEV3/VERDICT.md`; run log: `docs/lab/crossref/runs/T2/PROSEV3/RUNLOG.md`.

## 3. Re-verification scope for this family

This track does NOT redo Tier-2. It performs INDEPENDENT re-derivations (different code/method than the Tier-2 crew where possible) and FRESH adversarial red teams designed to BREAK the Tier-2 claim. A break is the most valuable outcome and is reported plainly, never buried.

## Re-verification plan (fresh work)

- **RV1 — independent FAIL re-derivation.** Build a NEW pure-Zag verifier (different code than the T2 crew's 17-assertion verifier): A3 grok 183/228, sol 204/228, step 208/228, muse-native 227/228 vs frozen v1 189/204...; expect KB3-VIABLE FAIL (2/4: step + muse-native only). Reproduce the deviation footprint: 6/11 CORE from the unregistered expansion, wrong-value 8->30/912.
- **RV2 — adversarial challenge forks on the 2/4 boundary** (each frozen before build):
  - **CHAL-P1 "deviationectomy":** re-score with the 6 unregistered-expansion CORE items EXCLUDED — does FAIL deepen (1/4, 0/4) or soften (3/4)?
  - **CHAL-P2 "v1-side attack":** adversarial item sets targeting the 2 passing comparisons (step, muse-native) — can harder items flip them to FAIL?
  - **CHAL-P3 "wrong-value counterfactual":** cap/repair the 8->30/912 wrong-value verdicts — is the wrong-value increase the load-bearing cause of FAIL? If repairing it flips 2/4 -> 3/4+, the FAIL's mechanism is identified (still FAIL, but explained).

## Kill bars (frozen)

- **RV-CONFIRM** iff FAIL (2/4) holds under the independent verifier AND no challenge fork flips viability to PASS.
- **RV-BROKE** (report plainly) iff any fork flips the verdict to KB3-VIABLE PASS.

## Protocol (binding for this track)

- Pure Zag for all mechanisms / learners / verification code. Python glue/analysis only (statistics, parsing, plotting) — never in a decision path.
- ZERO randomness in any decision path. Every run byte-identical; prove with SHA-256 digests, >=3 reps unless the plan says otherwise.
- Slices and indexable structures under 2^25 bytes each.
- No full git clones on this VM (SIGKILL/OOM under load). Use blob-filtered single-commit fetches, sparse checkouts, or per-file SHA-verified API fetches.
- Commits to `sylorlabs/TNN`, branch `tnn-native-lab`, ONLY via `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`; lab-relative paths NOT starting with `docs/lab/` (never double-prefix). Never commit binaries or `.zagd`.
- This prereg is frozen at its commit: no implementation work before the prereg commit lands. Any deviation is recorded in RUNLOG.md and flagged.
- If a Tier-2 claim BREAKS under this probing, that is the most valuable outcome: report it plainly with evidence. Verdicts that survive get stronger; verdicts that break get reported, not buried.

## Deliverables

- `docs/lab/crossref/runs/T2/PROSEV3/reverify/VERIFY.md` — per-leg results, digests, red-team outcomes
- `docs/lab/crossref/runs/T2/PROSEV3/reverify/RUNLOG.md` — timestamped run log
- `docs/lab/crossref/runs/T2/PROSEV3/reverify/evidence/` — digests, tables, boundary maps (text only)
