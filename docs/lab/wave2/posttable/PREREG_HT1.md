# PREREG_HT1 — Verified context switching under a randomized curriculum (BUILT 2026-09-19)

## Hypothesis

A context mechanism with **no score table** — contexts as declared memory
partitions, switching as a deliberate operation with **intrinsic
corroboration** (`CTX_SWITCH` refuses unless the target shows recorded
majority-positive evidence AND the active partition shows recorded
majority-negative evidence) — survives a randomized regime-switching
curriculum with 15% evidence noise, where the R34 v3 score-table learner
(the toy) breaks. Micah's acceptance test: *"if I randomly switch up on
TNN it shouldn't fail."*

## The exact toy failure being replaced

LH-5: the toy's switch rule (`reward<0 && old>0 → switch`, single
uncorroborated negative sample) explodes switches 19→181 at 10%
corruption and collapses whole probe blocks to 0/16. The replacement is
not a patched switch rule — there is no score, no `reward<0` trigger, no
accumulator anywhere in CTX. The trigger is gone; the mechanism is
different (CTX_DESIGN.md §3).

## Mechanics (native Zag, `ctx/`)

**Shared curriculum (both arms, identical):**
- 48 episodes. True regime starts 0; each episode flips with p=1/6 via a
  seeded LCG (dedicated stream, generated up front — both arms see the
  same regime sequence).
- Learning channel noise 15% (seeded, independent streams per arm):
  above the toy's 10% fragility knee (LH-5).
- Every 8 episodes: a 16-probe **measurement block**, uncorrupted,
  read-only (never feeds learning — H-07 evaluator separation).
- Settle phase after the 48: 8 episodes fixed regime 0, then 8 fixed
  regime 1, then 16 uncorrupted probes per regime on the settled
  active partition/context.

**CTX arm** (mechanism under test):
- 4 partition slots `{live, label, hits, total, bad_streak, step_created}`,
  one `active` index, fixed audit ledger (every op AND refusal audited).
- Ops: `CTX_PROPOSE(label)`, `CTX_RECORD(slot,hits,total)` (replaces the
  evidence window — observations, never accumulated), `CTX_SWITCH(target)`
  with the intrinsic corroboration rule (target majority-positive AND
  active majority-negative, else `REFUSED_UNVERIFIED` — structural, in
  the op implementation).
- Policy (protocol-fixed in the harness — honest boundary, same as MA1's
  fixed values): boot `PROPOSE(0)`; per episode, 16 noisy evidence probes
  on the active partition → `RECORD`; one majority-negative batch sets
  `bad_streak` (information, not a switch); verify mode probes every other
  live partition and `SWITCH`es to the first majority-positive one, else
  `PROPOSE`s the alternate label, probes, switches if verified.

**Toy arm** (R34 v3 learner core, unmodified — expected-negative control):
- Per episode: 16 training accepts (`choose` explore-disabled; reward
  +1 iff chosen==true regime else −1, 15% sign flips; `learn=1`,
  `allow_switch=1`).
- Measurement blocks: 16 chooses, `learn=0`, `allow_switch=0`,
  uncorrupted; count correct.

**Determinism:** seeded LCGs, documented seeds; the runner executes the
binary twice and requires byte-identical stdout.

## Pass / fail criteria

CTX arm PASSES iff ALL hold:
1. **No collapse:** zero measurement blocks ≤4/16 during the random
   phase (the toy's LH-5 signature was 0/16 blocks).
2. **Bounded switching:** `ctx_switches ≤ 2 × true_flips` (no
   switch-storm; the toy's switches exploded 19→181).
3. **Both regimes retained:** settle-phase endpoints `≥12/16` in regime 0
   AND regime 1 (per-regime reporting per the E51AJ law — never
   aggregate-only).
4. **Corroboration is real:** audit scan proves every committed
   `CTX_SWITCH` had target majority-positive AND old-active
   majority-negative evidence at commit time; every `REFUSED_UNVERIFIED`
   left state untouched; ledger replay from genesis == exact live state.
5. **Structural:** ≥2 live partitions with distinct declared labels at
   endpoint (it maintains separate contexts — not one relabeled slot).

Toy arm (control): expect ≥1 collapsed block OR `toy_switches >
3×true_flips` OR an endpoint regime ≤8/16. **If the toy passes all five
CTX criteria, the comparison is inconclusive** (curriculum too easy) —
report honestly, claim no win.

## Falsification

- FAIL the CTX mechanism if any criterion 1–5 fails.
- FAIL the trial design (not the mechanism) if the toy control passes
  everything — the curriculum didn't stress the difference.

## What it does NOT show

That the learner chooses *when* to probe or *which* label to propose on
its own — the policy is protocol-fixed in the harness. HT1 proves the
*mechanism* (verified switching) survives random switching + noise that
breaks the table. Learner-driven probe/switch timing is HT2.
