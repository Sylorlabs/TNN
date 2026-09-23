# LH-2 — Horizon ×40 (≈1920 updates): RESULT

**Variant dir:** `variants/LH-2/` · **Evidence:** `EVIDENCE_20260919T221525Z/` · **Date:** 2026-09-19
**Seeds (fresh, documented):** learner `22002`, world/runtime `2202`, drift off
**Learner core:** byte-identical to canonical, isolation holds. Harness = LH-1 harness with `LH_BLOCKS=40`, `LH_STRICT_EVAL=0` (findings recorded, not failed).

## Hypothesis verdict: saturation YES, rigidity NO

The ±30000 clamp binds — but the saturated learner keeps discriminating perfectly.

### Saturation points (per cell, from per-block `LH_TRACE`)

| Cell | Role | Pins at | Total updates at pin | Per-cell accepts at pin |
|---|---|---|---|---|
| s00 (ctx0·obj0) | A-correct | **+30000 during block 16** (28400→30000) | 768–816 | n00 = 302 (≈300 net positive accepts) |
| s11 (ctx1·obj1) | B-correct | **+30000 during block 16** (28100→30000) | 768–816 | n11 = 300 |
| s01 (ctx0·obj1) | A-wrong | never pins | — | −21100 at end (block 39) |
| s10 (ctx1·obj0) | B-wrong | never pins | — | −20100 at end (block 39) |

So each correct cell saturates after ≈300 net positive accepts (~16 blocks); the wrong cells sink at only ~−500/block (touched solely on exploration flips and switch episodes) and would need ~60 blocks to pin.

### Post-saturation behavior (blocks 16–39, fully saturated correct cells)

- **ea=16/16, eb=16/16 on every post-saturation block.** Zero `LH_FINDING` lines in the whole run.
- Return-A: `ra=15/16`, zero weight updates, `active=0` — identical to the unsaturated baseline gate.
- Determinism: identical fingerprint `fp=758072` across two full 40-block runs; world bytes equal.
- `train_updates=1920` exact; `LH_FAILURES=0`; controls match baseline (disabled 12/24, scrambled 0/16).

## Mechanism note — why the clamp does not cause rigidity (for Agent F)

Discrimination in `r34v3_best` depends on **within-context ordering** (`s00>s01`, `s11>s10`), not absolute magnitudes. Saturation preserves the ordering because the correct cell pins at +30000 while the wrong cell keeps sinking — the margin *grows* after saturation (30000 vs −21000). The clamp discards overflow but the update machinery (counts, `updates`, switch rule) keeps working: the switch rule keys on reward sign and `old>0`, both intact. True rigidity (tie → `decisions%2` coin-flip) would require *both* cells of one context pinned at the *same* value, which the fixed reward mapping never produces. **Candidate rigidity trigger for future work: a regime reversal** (reward mapping flip) — but `world.zag` (`cw_change`) supports only regimes 0/1 with a fixed mapping, so it cannot be tested without a new world.

Cost: ~9.0M cpu_us, 2.0MB RSS.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The results in this document come from a training run
with `explore_enabled=1`, which engaged the hidden seeded LCG (`r34v3_rng`,
`(rng*997+7919) mod 1000003`) inside `r34_learner_core.zag`, driving 1-in-5
pseudo-random explore flips in `r34v3_choose` — hidden randomness in the AI's
decision path, violating the no-randomness law. This leg: LH-2, ≈1920 updates (40× horizon), learner seed `22002`; training ran explore=1 (same LH-1 harness).
Verified by the r34 RNG probe (workstream 2/8), investigation commits
`072f25aa` / `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE.
The run is reproducible engineering evidence (byte-identical reruns hold) but
**not law-compliant evidence**. The stability verdict below stands recorded
but may not be cited as canonical — including the 40×-horizon stability verdict (1920 updates, 16/16) and the saturation findings — until clean
reruns (deliberate or state-varying exploration, no LCG) reproduce it.
The original text above is left intact for the record.
