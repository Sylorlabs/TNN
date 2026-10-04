# S1 run log — Phase A2 wiring (FINAL)

## Session
- Sealed session: `sessions/S1.txt` (16 episodes, commit e49b2a12).
- Binary: `session_run` (SHA `5513391538104bfb1049835e452b46a00b51427200511b5a0b7f3ae081ec6cad`), intent `survey`.
- Three modes: `live`, `ablate-constant`, `ablate-shuffle`.
- Runtime: ~390 s per full S1 (organ + low-band guard per frame, 16 eps).

## Live run (r1)
- Journal SHA-256: `b2234daba6fcdc2a8c6d97e94938f19a7e75312a206702c06cc3dee7f2105496`
- Actions: NOTE_NEW×1, ATTEND×2, CONTINUE×2, RECALL×11, QUERY×0.
- Prediction: 4 hits / 11 misses (pitch-class carryover).
- Behavior:
  - EP1 (kidc): NOTE_NEW (novel class, first episode).
  - EP2 (v1_human): ATTEND (deviation from baseline).
  - EP6–9,11 (novel clips): RECALL to nearest history entry (dist 2–39).
  - EP10,12–16 (exact repeats): RECALL with dist=0 to the correct turn
    (descriptors byte-identical across repeats — also a determinism signal).

## Ablations
- `ablate-constant`: 16/16 QUERY ("no-signal"). SHA `c3a521cf380a...`.
- `ablate-shuffle`: NOTE_NEW×1, ATTEND×1, RECALL×14. SHA `9cfbb54049e4...`.

## Scoring (frozen scorer_wiring.py, commit bcdd5b92)
```
K-W1: perm p=0.00010 (L1 obs=2.0000, 10000 perms) → PASS (bar p<0.01)
K-W2: differing episodes=16, sign agreement=1.000 → PASS (bar ≥0.70)
  ordinal diffs (const-live): [-2,-3,-1,-3,-1,-2×11] (all negative:
  silence ablation uniformly suppresses responsiveness)
shuffle supplementary: perm p=0.58244 (not significant — the fixed
  permutation preserves enough descriptor structure that actions barely move)
OVERALL: WIRING-WORKS
```

## Determinism (K-W4)
- Three consecutive full live runs (r1/r2/r3):
  - r1: `b2234daba6fcdc2a8c6d97e94938f19a7e75312a206702c06cc3dee7f2105496`
  - r2: `b2234daba6fcdc2a8c6d97e94938f19a7e75312a206702c06cc3dee7f2105496`
  - r3: `b2234daba6fcdc2a8c6d97e94938f19a7e75312a206702c06cc3dee7f2105496`
  - All three byte-identical. ✓
- Rendered WAVs: all 16 episodes byte-identical across r1/r2/r3 (SHA-compared
  per episode, 16/16 OK). ✓
- Ablation journals:
  - const: `c3a521cf380af1eeff3f57db1907ccd52a415510666820c67d000892ab5cf701`
  - shuf:  `9cfbb54049e40901e2a2a2daffdc462417c49b3ea8a9731f5fd850b62c1fa12e`

## Rendering
- `render_act` → 16 WAVs per journal (`runs/wav_live/`, `wav_const/`, `wav_shuf/`).
- Action→sound mapping verified against journal ACTION lines.
