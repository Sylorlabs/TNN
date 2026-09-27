# A1 Strategy Sketches (EXP1b)

For each variant where I-survive beats R by >= 60 ticks, the winning trace
is abstracted to a strategy sketch over primitive actions.

Variants qualifying: v1 (+284), v2 (+84), v4 (+95), v5 (+475), v7 (+349).

## v1 (I 600, R 316, +284)

I trace: begins L R E T D C W (len-1 plans in index order), then len-2
plans, then len-3. I executes many WAITs. Mote-on-cell reflex triggers
frequently (dense cluster near home). I survives via H1 eats and WAITs.

Sketch:
- Execute plans in index order (L, R, E, T, D, C, W, LL, LR, ...)
- When mote on cell: EAT (taught reflex)
- When energy < 25: move toward nearest mote (taught reflex)
- When storm: flee (taught reflex)
- Otherwise: continue plan (often WAIT, saving energy)

No compositional step. The advantage over R (which chases constantly,
burning 2/tick) is energy saved via WAITs.

## v2 (I 397, R 313, +84)

Similar. I's plans include WAITs; R's chase wastes movement. I eats via
H1 when motes wander onto its cell. No COMBINE succeeds.

Sketch: same as v1. Trivial.

## v4 (I 340, R 245, +95)

Same pattern. I's random plans happen to include enough WAITs and EATs
(via reflex) to outlast R's chase.

Sketch: same as v1. Trivial.

## v5 (I 600, R 125, +475)

Largest margin. v5 has a dense cluster (4 motes in 20..23). R chases
futilely and starves (125). I's WAITs conserve energy; H1 triggers often
enough to sustain. I never builds anything.

Sketch: same as v1. Trivial.

## v7 (I 600, R 251, +349)

Same. Dense cluster, I outlasts R via energy conservation.

Sketch: same as v1. Trivial.

## Conclusion

In all 5 variants, I's "strategy" is: execute random primitive plans in
index order, rely on taught reflexes (EAT on cell, flee storm, emergency
seek), and save energy via WAITs. There is no multi-step compositional
plan, no tool construction, no novel sequence. The behavior is a trivial
recombination of taught single-step reflexes and random actions.

This fires K4 (trivial recombination kills the invention claim).
