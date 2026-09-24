# CREW A — §5 red team, fresh runs 2026-09-24

Binary: `src/render_a` (+ `src/form_par` for formation-side probes).
All probes rerun on current builds; no RNG anywhere.

## R1. Event-order permutation (render path)
`render_a plan_v1 out.mix evperm+mix` vs `seq+mix` → `cmp` clean,
**bit-identical**. Visit order cannot leak into the mix. PASS.

## R2. Sustained 1292-block corruption + recovery
- Corrupted all 1,323,000 samples in 1024 consecutive 1292-sample blocks
  with a deterministic per-sample XOR pattern (no RNG).
- Re-render from the plan → **byte-identical to clean** (`cmp` clean).
- Recovery story holds: generation never reads the mix, so any mix-level
  corruption is exactly the corruption — no cascade, exact regeneration.
  PASS.

## R3. Plan-text adversarial (9 cases, from par_dive/redteam/plans)
empty, negative duration, nonnumeric tokens, short event, rail amp,
rail freq, rail dur, bad bed, 20 k-event flood — **no crash, no hang,
rc=0 on all 9**. Renderer degrades permissively (documented behavior —
counts as a known weakness vs strict rejection, not a bar failure). PASS.

## R4. Formation lies (form_par)
- Sub-octave nominal 220, vibrato cue, glide cue → all resolve **440 Hz**.
  Cue shape / nominal octave never confuses the resolver. PASS.

## R5. Fault-family (see BASE_BATTERY.md RT-CASCADE)
Zero post-fault differences on all four models — the generation path
provably never reads the mix. PASS.

## R6. Truncation (see BASE_BATTERY.md RT-EDGE)
No illegitimate diffs at the cut under either truncation interpretation.
PASS.

## §5 verdict: A survives the full red-team battery.
Known non-bar weaknesses confirmed: permissive malformed-plan handling,
no RESPOND→RESPOND chaining, fixed caps, dense-polyphony clipping
(see A_POLY.md), single-core cost (see BASE_BATTERY.md COST).
