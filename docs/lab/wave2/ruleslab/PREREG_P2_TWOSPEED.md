# PREREG P2 — TWO-SPEED: fast/candidate + slow/accepted consolidation

Status: PREREGISTERED + EXECUTED 2026-09-19 (3 seeds). See TRIAL_RESULTS.md.

## Hypothesis

Mirroring the brain's `ProtectedSkillMemory` fast/slow tables: a fast table
absorbs experience (the candidate), a slow table consolidates toward it
periodically (the accepted policy). Decisions default to the consolidated
table; the fast table overrides only on strong disagreement. Predicted: better
return-A retention than R34 (16/16 vs 15/16) with no extra updates, because the
slow table preserves regime-A knowledge while fast adapts to B.

## Rule mechanics

- `fast[c][o]`: R34 additive rule, `+= reward*100`, clamp ±30000.
- Every 8th outcome (**consolidation**): for each cell, `slow` moves toward
  `fast` by ±25 without overshoot; then `fast` decays 25% toward the new slow:
  `fast = slow + (fast−slow)*3/4`.
- **Decision:** `slow_best = argmax slow[c]`, `fast_best = argmax fast[c]`.
  If `fast_best != slow_best` and `|fast[c][fast_best] − slow[c][fast_best]| > 4000`,
  follow fast (override, counted); else follow slow. Then ε-greedy 1/5 as R34.
- Context recruitment/switching identical to R34, reading fast (recent evidence).

## Predicted observable difference vs R34

- returnA 16/16 (vs R34's 15/16); equal or better evalA/evalB.

## Falsification criteria

- If returnA ≤ R34's on any seed, or training acquisition is worse with no
  retention gain, reject the mechanism at these parameters.

## Outcome (executed)

**REJECTED at these parameters.** Across 3 seeds P2's training positives were
strictly worse than baseline every time (A: 31/33/32 vs 35/35/36; B:
30/31/31 vs 33/30/34), endpoints identical (16/16, 16/16, 15/16).
Mechanism of failure: the slow table's extended tie-break phase costs ~3–4
early episodes per regime, and the 25%-per-8-episode fast decay drags down
fresh learning. The 4000 override margin almost never fires on 40-episode
horizons. The returnA 15/16 miss is a one-episode switch-detection cost,
present in all variants — not forgetting, so consolidation cannot fix it.
**Do not rerun P2 as parameterized.** Candidate repairs (untested): lower
override margin, asymmetric consolidation (only consolidate on positive
outcomes), or much longer B phases where forgetting actually occurs.
