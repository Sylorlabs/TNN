# LH-3 — Horizon ×100 (≈4800 updates) + slow regime drift: RESULT

**Variant dir:** `variants/LH-3/` · **Evidence:** `EVIDENCE_20260919T221548Z/` · **Date:** 2026-09-19
**Seeds (fresh, documented):** learner `33003`, world/runtime `3303`, drift RNG `333`
**Learner core:** byte-identical to canonical, isolation holds. Harness = LH-1 harness with `LH_BLOCKS=100`, `LH_DRIFT_SEED=333`, `LH_STRICT_EVAL=0`.

## Recorded constraint (world regimes)

`world.zag` `cw_change` accepts **only regimes 0/1** (`regime>1` → `cl_bad()`), and the delayed reward is hardcoded to **+3 ticks** from the touch with value/action independent of the harness poll schedule — so there is **no learner-visible reward-timing handle** at harness level. Per the prereg fallback, drift is implemented as **seeded perturbation of the regime presentation schedule** (documented, no world modification):

- mode 0: A(24)→B(24) (normal order)
- mode 1: B(24)→A(24) (swapped order)
- mode 2: interleaved A/B in 6-episode chunks ×4 (rapid alternation)

Seeded decile schedule (drawn at each decile start from drift seed 333):

| Blocks | 0–9 | 10–19 | 20–29 | 30–39 | 40–49 | 50–59 | 60–69 | 70–79 | 80–89 | 90–99 |
|---|---|---|---|---|---|---|---|---|---|---|
| Mode | 1 | 1 | 2 | 0 | 0 | 2 | 1 | 2 | 2 | 1 |

## Hypothesis verdict: STABLE (behaviorally), under drift and full saturation

| Check | Result |
|---|---|
| `train_updates == 4800` | 4800 == 4800 ✓, one lineage, no restarts |
| Determinism | identical fingerprint `fp=875695` across two full 100-block runs |
| Per-decile eval | blocked deciles (modes 0/1): **16/16 both regimes, every block**; interleaved deciles (mode 2): eb=16/16, **ea=15/16** |
| Return-A | **ra=16/16**, zero weight updates |
| Campaign failures | `LH_FAILURES=0` |

### The ea=15/16 in mode-2 deciles is a probe artifact, not learning loss

In mode 2 the block ends on a B-chunk (`active=0`); `eval_A` runs with `allow_switch=1, learn=0`, so its first episode is consumed re-engaging context 1 — the remaining 15 are correct. Switch counts confirm the accounting: +8 switches per mode-2 block (7 chunk-boundary switches + 1 eval-A switch) vs +2/block in blocked modes. The router works 4× harder under rapid alternation with no performance cost.

### Representation finding: first-decile mode mirror-assigns the contexts — permanently

Because decile 0 ran mode 1 (B-first), context 0 claimed the **B** mapping and context 1 the **A** mapping — the mirror image of LH-1/LH-2:

- b=0: `s01=+1500` (ctx0·B-correct), `s10=+1800` (ctx1·A-correct); `s00=−900`, `s11=−600`
- b=99: `s00=−30000, s01=+30000, s10=+30000, s11=−30000`

The assignment, once set, **never changed across 100 blocks and 4 schedule perturbations**. Behavior stayed 16/16 throughout. Context→regime assignment is path-dependent (first regime trained claims context 0) but behaviorally equivalent.

### Saturation under drift

Correct cells pinned +30000 at **block 16** (s01, s10 — same ≈300-accept pinning as LH-2); wrong cells pinned −30000 at **block ≈51** (s00) and **≈59** (s11). The table was fully saturated from block ~59 onward — 40 more blocks of perfect discrimination on a fully pinned table.

### Return gate nuance

`ra=16/16` with `active=1` (recorded as `LH_FINDING,return_active=1`): under the mirror assignment, context 1 *is* the A-context, so no switch was needed — better than the baseline's 15/16, which was itself a switch-cost artifact. This confirms the baseline 15 was probe mechanics, not retention loss.

## What Agent F should know

1. **No rigidity mechanism found up to 100× horizon**, even fully saturated and under schedule drift. The clamp is behaviorally inert here: ordering-based discrimination + sign-based switching survive pinning.
2. The interesting stress the apparatus *cannot* express: a true contingency reversal (reward mapping flip). `world.zag` fixes the mapping; testing post-saturation adaptability needs a new world, not a new harness.
3. Probe design matters more than horizon: the two "imperfections" in this run (LH-1's ea=0/16 ordering bug, LH-3's ea=15/16 switch cost) were both measurement artifacts of context-relative evals, caught by the trace, not by aggregates. Per-block/per-regime reporting (E51 law) is what made them visible.
4. Compute is a non-issue: 100 blocks + full determinism rerun + controls = ~22M cpu_us (~25 s wall), 1.9 MB RSS.

## Per-decile eval positives (endpoint retention, E51 law)

Every block: modes 0/1 → A 16/16, B 16/16; mode 2 → A 15/16, B 16/16. No block below 15/16 in either regime across 100 blocks. No collapse, no oscillation — classification: **stable**.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The results in this document come from a training run
with `explore_enabled=1`, which engaged the hidden seeded LCG (`r34v3_rng`,
`(rng*997+7919) mod 1000003`) inside `r34_learner_core.zag`, driving 1-in-5
pseudo-random explore flips in `r34v3_choose` — hidden randomness in the AI's
decision path, violating the no-randomness law. This leg: LH-3, ≈4800 updates (100× horizon) with seeded regime drift, learner seed `33003`; training ran explore=1 (same LH-1 harness).
Verified by the r34 RNG probe (workstream 2/8), investigation commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE.
The run is reproducible engineering evidence (byte-identical reruns hold) but
**not law-compliant evidence**. The stability verdict below stands recorded
but may not be cited as canonical — including the "delayed-credit rule is stable at 100× horizon" verdict (4800 updates, 16/16) — until clean
reruns (deliberate or state-varying exploration, no LCG) reproduce it.
The original text above is left intact for the record.
