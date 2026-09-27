# EVIDENCE.md — Experiment 1: Invent-to-Survive

## Primary results (median survival ticks over 12 variants)

| Arm | Median | Values |
|-----|--------|--------|
| P (positive control) | 600 | 600×12 |
| Z (random baseline) | 143.5 | 4, 23, 41, 52, 130, 132, 155, 160, 190, 220, 243, 250 |
| R (recall-only) | 160 | 130, 160×7, 190×2, 220 |
| I-survive | 220 | 190×2, 215, 220×4, 248, 250×4 |
| I-invent | 220 | 190×3, 220×4, 242, 246, 250×3 |

## Determinism
- All 60 runs executed twice.
- SHA-256 of results.tsv (both reruns): `6d20bebee0b40f466aea796cef6343436c82face0b262be6021291dbdcc1c6da`
- Byte-identical across reruns. ✓

## Key findings
1. **C1/C2 met:** P=600 (solvable), Z=143.5 (not trivial).
2. **C3 not met:** Only ward-turtle reaches 360+. World is one-trick.
3. **K1/K2/K3 not fired:** I (220) beats R (160) and Z (143.5); P=600 (not VOID).
4. **No genuine invention:** A1 finds no coherent novel strategy in I's traces.
   I explores systematically but does not build WARDs or compose a working strategy.
5. **Novelty weakly causal:** A2 shows removing novelty drops median 250→232
   (7%); K6 supported.
6. **H2 not supported:** I-survive and I-invent both 220; goal string makes no difference.

## Files
- `src/`: world.zag, agent_r.zag, agent_z.zag, agent_p.zag, agent_i.zag, run_all.py
- `kb/`: kb.txt, p_addition.txt
- `worlds/`: v00.txt … v11.txt (33 ints each, fixed parameters)
- `runs/`: results.tsv, traces.tsv, results.sha256 (rerun 1 and rerun 2)
- `evidence/`: A1_sketches.md, A2_ablation.md, A3_task1_comparison.md,
  BAR_RESULTS.md, EVIDENCE.md (this file)

## Prereg friction (implementer notes)
1. **Exile:** Motes respawn at fixed cells beyond the void (prereg-compliant:
   "fixed per-mote cell" does not fix the side). Required for calibration
   (stationary motes give R=600, making K1 fire trivially).
2. **Windowed mean:** §4 says "mean observed ΔE". Implemented as sliding-window
   mean (last 8) because the world is non-stationary by (1); a lifetime mean
   is pathologically sticky. Documented as implementer refinement.
3. **Novelty bonus values:** §4 does not fix magnitudes. I-survive NOV=30,
   I-invent NOV=60 (parametrized by goal string only; machinery identical).
4. **Safety layer:** I uses the KB heuristics as hard safety constraints
   (void/storm/starvation) and deliberates only when safe. Justified by
   "Same KB, same reflexes" + invention machinery as the only difference.
5. **C3:** Not met; reported honestly. Did not retune prereg's fixed numbers.
