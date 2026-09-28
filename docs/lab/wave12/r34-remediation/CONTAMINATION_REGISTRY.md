# R34 hidden-randomness contamination registry

**Date opened:** 2026-09-20 · **Owner:** Micah · **Worker:** DOCS (r34 remediation)
**Ruling:** REMEDIATE — R34 v3 stays quarantined until clean evidence exists.

## The contamination (verified)

`r34_learner_core.zag` contains a seeded LCG —
`r34v3_rng`: `(rng*997+7919) mod 1000003` — consumed inside the learner's
action-decision function `r34v3_choose`: when `explore_enabled==1`, a 1-in-5
pseudo-random flip of the greedy action. The explore decision is made by a
dice-like stream, not by learner judgment: a violation of the no-randomness
law ("no random exploration"). The stream is seeded (fixed constants, no
entropy source), so runs are byte-identical and reproducible — this is an
engineering-law violation, not a determinism failure.

**Investigation (workstream 2/8), branch `tnn-native-lab`:**

- `072f25aa49766ca27fcf4718a758adb6f7b1dde7` — "r34 RNG probe: INVESTIGATION.md"
  (full mechanism trace; 2026-09-20)
- `4976cbf5ce07302b21af5eff01b80458d23bd731` — "r34 RNG probe: VERDICT.md"
  (verdict: PROBLEM-REQUIRING-ACTION; 2026-09-20)

## Tainted runs

Every run below trained with `explore_enabled=1` and is **QUARANTINED**:

| Run | What it was | Taint detail | Status |
|---|---|---|---|
| R34 v3 qualification campaign | `train_A`/`train_B` (24+24), `scramble_train` control, `deterministic_learner` replay; learner seed `7331` | train phases explore=1 | QUARANTINED |
| LH-1 | 10× horizon, ≈480 updates, 16/16 per block; seed `11001` | `lh_train_regime` passes explore=1 | QUARANTINED |
| LH-2 | 40× horizon, ≈1920 updates, 16/16, saturation findings; seed `22002` | same LH-1 harness, explore=1 | QUARANTINED |
| LH-3 | 100× horizon, ≈4800 updates, 16/16 + regime drift; seed `33003` | same LH-1 harness, explore=1 | QUARANTINED |
| LH-4 | multi-return curriculum, 12 visits; seeds `47111`/`271` | every training visit explore=1 | QUARANTINED |
| LH-5 | 480-update runs under LH-1 protocol, reward-corruption ramp | train explore=1 (LH-1 protocol) | QUARANTINED |
| LH-7 | rapid-alternation interference, 480 train updates | updates always on, explore=1 | QUARANTINED |
| ruleslab baseline arm | R34 rule head-to-head baseline (seeds 7331/999/…) | explore=1 (5/6, 4/5, … exploratory episodes per phase) | QUARANTINED |
| ruleslab P2 arm | "explores identically to baseline by construction: fixed 1/5 rate, same rng consumption" | same LCG stream as baseline | QUARANTINED |

**Partially implicated (comparison baseline tainted):**

| Run | Detail | Status |
|---|---|---|
| LH-P3 | Own core (`r34_p3_learner_core.zag`); adaptive exploration is a preregistered mechanism under test, not hidden. But all head-to-heads compare against the tainted R34 baseline. | comparisons QUARANTINED; P3 mechanism standing needs Micah's ruling separately |
| ruleslab P3 arm | Own seeded adaptive rule (preregistered mechanism); margins vs tainted baseline/P2 | comparisons QUARANTINED |

**Investigated and NOT tainted by this contamination:**

| Run/doc | Reason |
|---|---|
| Eval / return-eval phases of all R34/LH runs | `explore=0` — pure greedy |
| HT1 / HT2 toy arms (R34 v3, unmodified) | ran with `choose` explore-disabled per prereg; 357-switch storm reproduced without exploration |
| Whitebox tests (`wb_whitebox_tests.zag`) | `r34v3_rng` used only as benign fixture (seed-sensitivity / serialization checks); drives `r34v3_accept` directly |
| MA3 (memory agency) | runs on `r34_memory_lifecycle_v1`, not the R34 v3 explore learner |
| World/harness side | RNG is learner-side only; structural isolation claims hold |

## Tainted claims (suspended until clean reruns)

1. "Delayed-credit learning rule is stable at 10×/40×/100× horizon" (480/1920/4800 updates, 16/16 throughout) — LH-1/LH-2/LH-3.
2. "Stable at 100× but fragile to noisy reward — knee between 0% and 10% corruption, regime switches exploding 19→181" — LH-5.
3. R34 v3 campaign endpoints (trained A 16/16, trained B 16/16, return A 15/16, exactly 48 updates) — qualification campaign.
4. ruleslab P2/P3-vs-baseline margins (incl. "P3 cuts exploration ~53%", "adopt P3 as the default") — tainted baseline.
5. LH-4 multi-return retention and LH-7 rapid-alternation results.

Note: the "LH-5 signature" *phenomenon* (switch-storm under noise) is descriptively
valid — it was independently reproduced under explore-disabled conditions
(HT1/HT2). Only the tainted quantitative claims above are suspended.

## Documents annotated (2026-09-20)

Each carries an appended, clearly-marked contamination note; original text intact.

**Primary evidence:**
- `docs/lab/toolchain/r34v3/CLOSURE_20260917.md`
- `docs/lab/toolchain/r34v3/PREREGISTRATION.md`
- `docs/lab/toolchain/r34v3/WORKLOG_20260916.md`
- `docs/lab/toolchain/r34v3/README.md`
- `docs/lab/toolchain/ZAG_PLAYBOOK.md` (§6 Linux-port campaign results)
- `docs/lab/wave1/README.md`
- `docs/lab/wave2/longhorizon/PREREG.md`
- `docs/lab/wave2/longhorizon/variants/LH-1/RESULT.md`
- `docs/lab/wave2/longhorizon/variants/LH-2/RESULT.md`
- `docs/lab/wave2/longhorizon/variants/LH-3/RESULT.md`
- `docs/lab/wave2/longhorizon/variants/LH-4/RESULT.md`
- `docs/lab/wave2/longhorizon/variants/LH-5/RESULT.md`
- `docs/lab/wave2/longhorizon/variants/LH-7/RESULT.md`
- `docs/lab/wave2/longhorizon/variants/LH-6/BLOCKED.md`
- `docs/lab/wave2/longhorizon/variants/LH-P3/RESULT.md`
- `docs/lab/wave2/ruleslab/TRIAL_RESULTS.md`
- `docs/lab/wave2/ruleslab/RULES_SURVEY.md` (already marked "(quarantined)" inline; now dated and grounded)
- `docs/lab/wave2/ruleslab/PREREG_P1_STRUCT_PROMOTE.md`
- `docs/lab/wave2/ruleslab/PREREG_P2_TWOSPEED.md`
- `docs/lab/wave2/ruleslab/PREREG_P3_ADAPTIVE_EPS.md`
- `docs/lab/wave2/whitebox/WHITEBOX_TESTS.md` (clarifying note: tests clean, referenced campaign checks quarantined)

**Downstream citations:**
- `docs/lab/wave2/posttable/POST_TABLE.md`
- `docs/lab/wave2/posttable/CTX_DESIGN.md`
- `docs/lab/wave2/posttable/PREREG_HT1.md`
- `docs/lab/wave2/posttable/TRIAL_RESULTS_HT1.md`
- `docs/lab/wave3/developmental-curriculum/CURRICULUM.md`
- `docs/lab/wave3/developmental-curriculum/PREREG.md`
- `docs/lab/wave3/developmental-curriculum/PILOT_RESULTS.md`
- `docs/lab/wave3/non-toy-evaluation/EVALUATION_PROTOCOL.md`
- `docs/lab/wave4/scaffold-release/PREREG.md`
- `docs/lab/wave4/rl-redteam/PREREG.md`
- `docs/lab/wave4/cheat-traps/TRAP_SUITE.md`
- `docs/lab/wave4/cheat-traps/curriculum/family_c_loopholes.md`
- `docs/lab/wave11/t4-curricula/findings/10-noise-incompleteness.md`
- `docs/lab/history/WHAT_TNN_IS_NOT.md`

**Archival mirrors (byte-identical copies of the annotated toolchain docs — covered by the same notes, not individually annotated):**
- `docs/lab/wave2/longhorizon/variants/{LH-1,LH-2,LH-3,LH-4,LH-5,LH-7,LH-P3}/toolchain/r34v3/{README,PREREGISTRATION,WORKLOG_20260916,CLOSURE_20260917}.md`
- `docs/lab/wave12/senses/doc-sweep/docs_local/` and `drive-inventory/docs/` contain Drive-archive mirrors of R34-era documents (e.g. `0311_TNN_R34_V3_QUALIFICATION_CHECKLIST.md`, `0691_CLOSURE_20260917.md`, `0621_WORKLOG_20260916.md`); these are catalogued copies of the same tainted campaign — same quarantine applies.

## Quarantine status

- R34 v3 (all variants) may not be cited as canonical evidence until clean reruns exist.
- Clean rerun requirement: exploration replaced by a deliberate or state-varying
  (non-dice) mechanism, then re-qualification of the campaign and LH legs.
- Alternative path (needs Micah's dated approval): prereg amendment explicitly
  ruling seeded deterministic PRNG exploration law-compliant, closing the
  exploration-undeclared prereg gap (0302_PREREGISTRATION.md never mentions it).

## Memory-file items flagged for the parent (memory is read-only for this worker)

`~/MEMORY.md` repeats tainted claims verbatim in two fact entries; the parent
should update them:
1. "the delayed-credit learning rule is stable at 100x horizon (480/1920/4800
   updates, 16/16 throughout)" — from the 2026-09-19 session record.
2. "fragile to noisy reward — the knee is between 0% and 10% reward corruption,
   with regime switches exploding 19 to 181" — same entry.
Both should be marked QUARANTINED pending clean reruns (see above).
