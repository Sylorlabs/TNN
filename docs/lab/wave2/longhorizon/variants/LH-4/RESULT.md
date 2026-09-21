# LH-4 — Multi-return curriculum (A→B→A→B…) — RESULT

**Date:** 2026-09-19 · **Agent:** E2 (curriculum & interference) · **Apparatus:** R34 v3 continual learner, Linux port
**Evidence:** [EVIDENCE_20260919T221437Z](EVIDENCE_20260919T221437Z/) (`failures=0`, RECEIPT.txt)

## Config (as preregistered)

- 12 visits, alternating A/B starting with A, 24 train episodes per visit (learn=1, allow_switch=1, explore=1).
- After every visit: 16-episode probe with updates DISABLED. A-return probes mirror the
  baseline return_A gate (learn=0, allow_switch=1); B probes mirror eval_B (allow_switch=0);
  visit 0 mirrors eval_A (allow_switch=0). Zero weight updates during probes asserted every visit.
- One lineage, no restarts. **Fresh documented seeds: learner 47111, world 271.**
- `r34_learner_core.zag` unmodified (md5 `cf823bedd7afe300ae3da382a9e78aab`, isolation=true).

## Per-return / per-visit endpoint counts (E51 law: every point reported, none aggregated)

| visit | regime | train_pos/24 | probe_pos/16 | return-to-A gate (≥15/16) |
|------:|--------|-------------|-------------|---------------------------|
| 0 | A | 21 | 16 | — (acquisition) |
| 1 | B | 13 | 16 | — |
| 2 | A | 20 | **16** | **pass** |
| 3 | B | 20 | 16 | — |
| 4 | A | 17 | **16** | **pass** |
| 5 | B | 17 | 16 | — |
| 6 | A | 19 | **16** | **pass** |
| 7 | B | 21 | 16 | — |
| 8 | A | 19 | **16** | **pass** |
| 9 | B | 21 | 16 | — |
| 10 | A | 18 | **16** | **pass** |
| 11 | B | 20 | 16 | — |

- All 5 returns to A: **16/16** (gate ≥15/16 — passed with one point of headroom each).
- All 6 B visits: 16/16 on the disabled-update probe. A acquisition visit 0: 16/16.
- Train-phase positives (13–21/24) are below probe levels as expected: training runs with
  1-in-5 exploration and pays the one context-switch episode per visit.
- Endpoint state: `updates=288` (= 12×24 exactly), `contexts=3`, `switches=11`
  (one per regime change), fp=354681, pending=0.

## Determinism & controls

- Two same-seed runs → byte-identical stdout (`determinism_same_seed=true`).
- Matched control: original R34 v3 campaign recompiled with the same compiler in this
  variant tree → `R34V3_FAILURES,0` (baseline reproduces).

## Hypothesis verdict

**Confirmed.** The 3-context capacity supports repeated returns: A-retention stayed at
16/16 (≥15/16 gate) after every one of 5 returns across 12 alternations / 288 updates,
and B acquisition was undamaged by interleaved A visits. The context-switch mechanism
re-settles within a single visit; retention does not decay with alternation count.

## Notes for Agent F

- Every return beat the baseline's return_A gate (15/16) by landing 16/16. The 15 vs 16
  gap in the baseline appears to be a property of the single return transition (one
  exploratory/switch episode), not of horizon: it does not widen with more alternations.
- Train-phase positives are noisy (13–21/24); only disabled-update probes are retention
  evidence — consistent with evaluator discipline.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The results in this document come from a training run
with `explore_enabled=1`, which engaged the hidden seeded LCG (`r34v3_rng`,
`(rng*997+7919) mod 1000003`) inside `r34_learner_core.zag`, driving 1-in-5
pseudo-random explore flips in `r34v3_choose` — hidden randomness in the AI's
decision path, violating the no-randomness law. This leg: LH-4, multi-return curriculum, every training visit ran explore=1 (learner seed `47111`, world seed `271`).
Verified by the r34 RNG probe (workstream 2/8), investigation commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE.
The run is reproducible engineering evidence (byte-identical reruns hold) but
**not law-compliant evidence**. The stability verdict below stands recorded
but may not be cited as canonical — including the multi-return curriculum retention results — until clean
reruns (deliberate or state-varying exploration, no LCG) reproduce it.
The original text above is left intact for the record.
