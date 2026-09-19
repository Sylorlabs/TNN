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
