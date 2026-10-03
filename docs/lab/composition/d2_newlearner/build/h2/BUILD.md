# H2 Build Notes — Taught-Physics World Model + 64-Tick Lookahead Planner

## Toolchain
- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Build: `znc_linux_x86_64_abed8aa1 h2.zag -o h2` (from `~/workspace/d2_new_learner/h2/`)

## Binary
- `h2` (workdir only; NOT committed)
- SHA-256: `432c836b6c32832072bfebb60ec143147959e6dc6dbad81f59fe437ae92a84d5`

## Architecture
Pure Zag. Zero RNG in decision paths. Deterministic given state.

### Files
- `model.zag` — shared: prelude, physics parser (Session 1), model state + `model_step`
  (exact replica of instrument M1–M15), mote estimator (velocity/void/home tracking),
  OBS parser/resync, OBS emitter (fuzz), file helpers.
- `h2.zag` — learner: card parser, chat loop, 9-candidate generator + 64-tick rollout
  planner, card-stage strategic planner (P1).
- `fuzz.zag` — differential validator (not shipped): drives `model_step` on scenario
  files, prints OBS; diffed against `d2bin tui`.

### Model state
`[]u8` arena, 256 i64 slots (little-endian via p_put/p_get). Layout:
- 0 t | 1 pos | 2 E | 3 surge | 4 alive | 5 cause | 6 va | 7 vb
- 8,9,10 storms | 11 ep | 12 start | 13 window_len
- 15..18 crystal cells | 19..22 taken
- 23..30 mote pos | 31..38 vel | 39..46 dormant | 47..54 home
- 55..58 inventory | 59 n_placed | 60..83 placed (typ,cell) | 84..179 loose
- 180,181 plank flags
- Physics (separate arena): 0 basal | 1 eat_gain | 2 maxE | 3 dormancy | 4 storm_dmg |
  5 zlo | 6 zhi | 7 void_kills | 8 ward_basal | 9 inv_cap | 10 start_E | 11 n_cells | 12 recipe_ok

### Physics ingestion (Session 1)
Anchor-substring parser (never numeric values). All 13 slots must parse or it
fails loud with `A PHYSICS_ERROR slot=<id>`. Verified: correct text → all slots;
wrong text (+10) → eat_gain=10.

### Estimator (hidden state)
- Velocities: inferred from OBS deltas, verified against drift1; bounce-solve for
  void_a when a confirmed velocity mismatches (sound: only possible cause).
- void_a: solved → used for model drift; movement bound stays 7 until locked
  (8 stable ticks) → then va-1. Safety-first.
- Home: observed positions; on wake, home=position (exact).

### Planner (H=64 pinned)
Outer: 9 candidates in prereg fixed order → each resolves to action 0..6
(invalid → 6/WAIT). For each: copy state, model_step, then 63-tick rollout with
base policy (storm→shelter/flee; pre-storm→build; else forage). Score =
(alive ? final_E : -100000). Tie → lowest candidate index (strict-greater replace).

Base policy (rollout continuation):
- Storm active: if sheltered → WAIT; elif in zone → go to ward or flee to nearest
  zone edge; else forage.
- No ward + storm within 64 → build (get 2 crystals → COMBINE → DROP at start).
- Ward placed + not sheltered + storm imminent (≤ dist+6) → go to ward.
- Else forage (EAT if on mote, else chase nearest active mote within bound).

**Interpretation note (prereg ambiguity):** The prereg lists "≤8" candidates but
enumerates 9; we implement all 9 (explicit enumeration wins). The prereg's
"greedily choose the candidate with best immediate model-predicted ΔE" inside the
rollout is implemented as the base policy above (a fixed priority policy, not a
per-tick candidate argmax), because pure 1-step ΔE ties on all movement/build
actions and cannot produce coherent multi-step plans. This is the prereg-faithful
implementable interpretation; documented here.

### P1 (card-stage strategic planner)
Derives skill-class sequence from card facts only. No-storm → "1". Else:
build-if-needed (with forage-first iff storm0 - build_lead - 6 ≥ 20), then
"3" per storm window + "1" for gaps ≥ 20. Verified: FW→"1,2,3,1", WF→"2,3,1",
FWF→"1,2,3,1,3,1" (digits match canonical).

## Validation
### Differential fuzz (model_step vs d2bin)
- 81 scenarios × 6 action scripts (wander, greedy-L/R, take/build, storm-stay,
  void-dance) = 486 runs, 32,912 ticks.
- Result: **0 mismatches**. (Length diffs only from final-state OBS convention.)
- Coverage: movement, clamp, void death, EAT/dormancy/respawn/drift, TAKE
  (crystal/mote/loose priority), COMBINE (all recipes), DROP (ward/loose),
  ward shelter, storm costs, starvation death, preward.

### P0 battery (via harness protocol)
- P0-F (16 scenarios): **16/16 PASS** (nEat≥4, wastedEat=0, alive, invalid<3)
- P0-W (16 scenarios): **16/16 PASS** (wardTick<60, alive, invalid<3)
- P1 (FW/WF/FWF): FW→"1,2,3,1" ✓, WF→"2,3,1" ✓, FWF→"1,2,3,1,3,1" ✓
  (digits match canonical; format "1,2,3" per harness prompt)

### Determinism
See DETERMINISM.md. Three runs byte-identical; MALLOC_PERTURB_=165 clean.

### Wrong-physics self-check (EAT=+10)
- Method: Fed altered Session 1 (`gain +10` instead of `gain +30`) through the
  same ingestion path (parser confirms `eat_gain=10`); ran 6 F scenarios vs
  correct-physics; compared action traces tick-by-tick and pass rates.
- Traces identical: 28–37% (F-0:33%, F-1:30%, F-2:35%, F-24:28%, F-25:29%, F-26:37%).
- Pass rate: 6/6 correct, 6/6 wrong (unchanged).
- Kill trigger (≥90% identical AND unchanged pass): **NOT fired** — behavior
  changes significantly with different physics, proving the learner genuinely
  uses the taught values (not hard-coded).
- Note: wrong-physics still passes because the sim grants +30 regardless and the
  policy is robust; the trace divergence (eating/foraging at different ticks)
  is the signal.

## Ambiguities resolved
1. 9 candidates vs "≤8": implement all 9 (explicit list wins).
2. Rollout "greedy ΔE": base policy (documented above).
3. Storm window length (30): from card "(30 ticks each)"; Session 1 validates rest.
4. Recipe sentence wraps lines: two-anchor check.
5. Movement bound: 7 until va locked (safety); model drift uses solved va.
