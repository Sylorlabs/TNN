# PREREG — FE1 novel-family formation audit (R3-2)

**Date:** 2026-09-24. **Crew:** FE1 novel-family formation audit crew (self-contained, no build).
**Parent hypothesis:** R3-2 (FE1), `docs/lab/senses/pam-rebuild/round2/debates/HYPOTHESES_R3.md`.
**Branch:** `tnn-native-lab`, repo `sylorlabs/TNN`.

## 1. Question

The R2-4 sense scores 53% on the 12 sealed novel adversarial families
(PTC-4/5, TMB-4/5, COL-4/5, CCN-3/4, SHP-4/5, MOT-4/5) and reaches its own
install bar on only 44/288 trials. Hardening ruled the remaining failures
front-end, not gate. Per family: **is there a ≥80%-accurate separator on the
frozen data, or is the truth byte-level unobservable** (MOT-1 class)?

## 2. Frozen inputs (verified live 2026-09-24)

- Generator: `docs/lab/senses/pam-rebuild/v2/redteam/src/rt_gen.zag`
  (pure Zag, zero RNG; `rt_draw` stateless hash chain). Read live; family
  semantics in §4 are quoted from it.
- Fixtures: `docs/lab/senses/pam-rebuild/v2/redteam/fixtures/sealed/` —
  288 fixtures + 288 `.truth` sidecars, 24 per family.
- Manifest: `MANIFEST.sha256`, digest
  `c140013e76c520e3e04ca2f3d4283f56a3e8184cbac01d4e5509ff5fb4f56b9d`
  — **verified**: recomputed manifest sha256 matches exactly; all 576
  per-file sha256 match the manifest (0 mismatches).
- File contracts (frozen R2A): `.img` = u32LE w,h + w·h·3 RGB;
  `.pcm` = u32LE rate(16000), u32LE nsamples, i16LE samples;
  `.vid` = u32LE nframes, u32LE w,h + frames of w·h·3 RGB;
  `.truth` = `truth=<VALUE>\n`.
- Kill-bar source: KB-FE1 in HYPOTHESES_R3.md (R3-2), quoted verbatim in §6.
- Unobservability template: `v2/MOT1_PREMISE_FLAW.md` (generator inspection
  + independent byte measurement + scope/limits).

## 3. Audit protocol (frozen)

For each of the 12 families, in family order:

1. **Separator attempt.** Implement the family's specified separator (§4)
   as a deterministic algorithm over the fixture bytes (integer arithmetic;
   f64 only where the frozen generator itself uses f64, replicating its op
   order exactly; correlator banks are bounded multiply-accumulate loops —
   directly portable to pure Zag, no RNG, no external data). The audit's
   reference evaluator is a frozen deterministic script (numpy only as a
   vectorized MAC evaluator — same arithmetic, zero RNG); the FE2 handoff
   is the algorithm spec, not the evaluator.
2. **Measure.** Run the separator over the family's 24 frozen fixtures;
   prediction vs `.truth` sidecar. Accuracy = matches / 24.
   **Separator bar: ≥ 20/24 (≥80%).** PASS → verdict SEPARATOR, record the
   accuracy and the full per-fixture prediction list.
3. **Unobservability attempt (only if the separator scores < 20/24).**
   Produce a byte-level unobservability proof per the MOT-1 template:
   (a) generator inspection — cite the exact generator branch and show the
   truth-determining operation leaves no record in the emitted bytes;
   (b) independent byte measurement on the frozen fixtures (no generator
   internals) showing the depicted/apparent signal is uninformative about
   or opposite to the truth label; (c) scope and limits. PASS → verdict
   UNOBSERVABLE with the proof.
4. **Otherwise** → verdict DEFENSE-SCOPE with the honest reason (explicit,
   not silent). Per KB-FE1 the "sense can learn this family" claim is then
   KILLED; the family becomes a refuse-by-construction (defense) target,
   not a front-end target.

**Determinism bar.** Zero RNG anywhere. The audit script is run 3 times;
sha256 of the per-fixture predictions file must be identical across runs —
any mismatch VOIDs the run. All evidence (predictions, digests) is committed.

**No threshold tuning on the verdict set beyond §4.** Decision thresholds in
§4 are frozen here, chosen from generator constants (class gaps), not from
fixture peeking. The audit reports the full per-fixture score distribution
so any threshold fragility is visible.

## 4. Per-family separator specifications (frozen)

Notation: `C(f, seg) = (Σ s·cos(2πfi/16000))² + (Σ s·sin(2πfi/16000))²`
over i16 samples s (correlator bank, 0.5 Hz steps unless stated).

### PTC-4 — detune-beats (pitchdisc). Truth ∈ {SAME, HIGHER, LOWER}.
Generator: segA pure fA (300–499 Hz); segB = (fB−det)+(fB+det) equal
partials, det ∈ [3,6] Hz; fB = fA (1/6 of draws) else fA±df, df ∈ [5,19].
- fA = argmax C(f, segA), f ∈ [280,540].
- segB: f1 = argmax C(f, segB); f2 = argmax C(f, segB) over |f−f1| ≥ 2 Hz;
  fB = (f1+f2)/2.
- Δ = fB−fA: |Δ| < 2.5 → SAME; Δ > 0 → HIGHER; else LOWER.
- Basis: the beat partials are symmetric about fB; 6–12 Hz spacing resolves
  in a 0.5 s window; the 2.5 Hz threshold sits in the empty gap between the
  SAME cluster (Δ=0) and the df ≥ 5 cluster.

### PTC-5 — gap-tone (pitchdisc). Truth ∈ {SAME, HIGHER, LOWER}.
Generator: segA pure fA; segB pure fB with a 60 ms (960-sample) silence gap
at segB samples [3520,4480); fB = fA (1/10 of draws) else fA±df, df ∈ [6,20].
- fA = argmax C(f, segA), f ∈ [280,540].
- fB = argmax C(f, segB_valid), segB_valid = segB samples with t2 ∉ [3400,4600)
  (known gap location plus guard band).
- Same decision rule as PTC-4 (|Δ| < 2.5 → SAME …).

### TMB-4 — env-reversal (timbredisc). Truth ∈ {BRIGHT, DARK, RICH}.
Generator: harmonic stack (f0, 4 harmonics); classes differ ONLY in f0 and
relative harmonic amplitudes — BRIGHT (f0 520–639; 1.0/0.7/0.5/0.3), DARK
(f0 300–399; 1.0/0.25/0.08/0.02), RICH (f0 400–499; 1.0/0.6/0.45/0.1).
The lure (envelope normal vs time-reversed) is time-domain only.
- f0 = argmax over f ∈ [280,660] of harmonic-sum Σ_{k=1..4} √C(k·f, full).
- Ak = √C(k·f0, full), k = 1..4; r2 = A2/A1.
- r2 < 0.42 → DARK; r2 > 0.65 → BRIGHT; else RICH.
- Basis: class a2/a1 centers are 0.25 / 0.6 / 0.7; thresholds are midpoints.
  Time-reversal of a real signal preserves |X(f)| exactly, so a
  magnitude-spectrum separator is provably immune to the lure.

### TMB-5 — formant-twin (timbredisc). Truth ∈ {BRIGHT, DARK}.
Generator: f0 350–499 Hz, 8 harmonics with Lorentzian amplitudes around
formant ff (bw 400): BRIGHT ff ∈ [2400,2799]; DARK ff ∈ [700,899].
- Full-signal magnitude spectrum (FFT, deterministic); spectral centroid
  = Σ f·|X(f)| / Σ |X(f)|, f ∈ [0,8000] Hz.
- centroid < 1600 → DARK else BRIGHT.
- Basis: class centroids sit near the formants (~800 vs ~2600 Hz); the
  1600 Hz threshold is mid-gap.

### COL-4 — adapt-ramp (colordisc). Truth ∈ {SAME, DIFFERENT}.
Generator: 128×64; left panel surface under neutral; right panel SAME surface
or surface+(30,−20,+15) under a SPATIAL illuminant ramp that is neutral at
the panel's left edge (t=0) and drifts to ±(40,10,30) at the right edge.
- L = mean RGB of left panel (x ∈ [0,64)); R = mean RGB of right-panel
  columns x ∈ [64,68) (ramp parameter t ≤ 4/63 ≈ 0.06, near-neutral).
- d = |Lr−Rr| + |Lg−Rg| + |Lb−Rb|; d > 25 → DIFFERENT else SAME.
- Basis: at t=0 the ramp is exactly neutral, so the panel edge compares
  surfaces directly: DIFFERENT → d ≈ 65; SAME → ramp residue ≈ 7.

### COL-5 — drift-metamer (colordisc). Truth ∈ {SAME, DIFFERENT}.
Generator: left panel flat (br,bg,bb); right panel flat S2·D/255 where
S2 = S1 (+(18,−12,+9) if DIFFERENT) and D is a UNIFORM drift
D_c = S1_c·255/S2_c + jit with ONE shared integer jit ∈ [−5,5] per fixture
(k=4 draw). The drift is chosen to make S2 metameric to S1.
- Read (br,bg,bb) from the left panel, (rr,gg,bb2) from the right panel.
- Replicate the generator's f64 drift math exactly (op order preserved):
  pred(S2c, j, S1c) = int(S2c·(S1c·255.0/S2c + j)/255.0) (truncation = Zag `as i64`).
- SAME-consistent ⟺ ∃ j ∈ [−5,5]: pred agrees on all 3 channels with S2=S1.
  DIFF-consistent ⟺ ∃ j ∈ [−5,5]: pred agrees on all 3 channels with
  S2 = (br+18, bg−12, bb+9).
- SAME-only → SAME; DIFF-only → DIFFERENT; both/neither → MISS.
- Basis: the shared integer jitter leaves a 3-channel rounding signature;
  the two hypotheses predict different signatures.
- KNOWN RISK (not a verdict): jit=0 makes SAME and DIFFERENT fixtures
  byte-identical on the right panel (right = left exactly, up to f64
  rounding) — those fixtures are provably unobservable. If the separator
  clears 20/24 it still passes; residual misses must be shown to be the
  jit=0 sub-case.

### CCN-3 — checker-illuminant (colorconst). Truth ∈ {SAME_SURFACE, DIFFERENT}.
Generator: 128×64; left panel texture sv=0 under neutral; right panel texture
sv ∈ {0,1} under a 2×2 warm/cool checkerboard (32×32 quadrants;
warm (255,220,180), cool (180,210,255)); surface tint (1, 0.9, 0.8).
- Per-quadrant von-Kries inversion with the known illuminants:
  v̂ = round(obs·255/I) per channel; invert the tint ((v·9)/10, (v·8)/10)
  from G and B; average the three v̂ estimates.
- MAD = mean |v̂(x,y) − L(x,y)| over the 64×64 panel (L = left R channel).
- MAD < 4 → SAME_SURFACE else DIFFERENT.
- Basis: same surface → inversion recovers the texture to ±2 LSB
  (truncation rounding); different surface → different texture phases →
  MAD in the tens.

### CCN-4 — exposure-flicker (colorconst). Truth ∈ {SAME_SURFACE, DIFFERENT}.
Generator: as CCN-3 but the right panel is split into 3 horizontal exposure
bands (band = y/22; middle band ×0.55) instead of a checkerboard.
- Per-band inversion: v̂ = round(obs/0.55) in band 1 (with tint inversion as
  in CCN-3), v̂ = obs elsewhere; average channels.
- MAD vs left texture; MAD < 4 → SAME_SURFACE else DIFFERENT.

### SHP-4 — shadow-decoy (shapetrans). Truth ∈ {CIRCLE, SQUARE, TRIANGLE}.
Generator: 96×96; shadow (a DIFFERENT shape, gray (95,95,100)) drawn FIRST at
(70,66) s=24; target drawn LAST at (48,48) s=26 in saturated blue (30,90,160).
- Blue mask M = {(b−r) > 50 ∧ (b−g) > 30}.
- Templates T_sh = the generator's `draw_shape` rasterization replicated
  bit-exact at (48,48), s=26, for sh ∈ {0,1,2}.
- Predict argmax IoU(M, T_sh). Self-check: the winning IoU must be 1.0
  (target drawn last ⇒ mask is exactly the target shape).
- Basis: the shadow is painted UNDER the target; color keying isolates the
  target regardless of the decoy.

### SHP-5 — tile-scramble (shapetrans). Truth ∈ {CIRCLE, SQUARE, TRIANGLE}.
Generator: shape drawn at (48,48) s=30 in (160,40,40); then 2×2 tiles
displaced by fixed offsets ((6,−4), (−6,5), (5,6), (−5,−5)) with in-order
overwrite on overlaps.
- Red mask M = {(r−b) > 50}.
- Forward templates: replicate the generator's tile displacement EXACTLY
  (offsets, order, clipping) applied to draw_shape(sh, 48, 48, 30);
  take each template's red mask.
- Predict argmax IoU(M, mask(F_sh)). Self-check: winning IoU == 1.0.
- Basis: forward rendering is bit-identical to the generator; the true
  shape's template matches exactly.

### MOT-4 — strobe-alias (motiondir). Truth ∈ {E,W,S,N,SE,SW,NE,NW}.
Generator: 8 frames 64×64; dot steps ±40 px/frame (cardinal) or ±36
(diagonal) with wraparound — nearest-neighbor differencing reads the
ALIASED (reversed) direction. A 12-dot comet tail (brightness 188→56) is
drawn BEHIND the head along the TRUE direction; head (240,240,240) rad 4.
- Frame 0 (head at (32,32), no wraparound): H = centroid of pixels with
  R ≥ 220; tail pixels = R ∈ [40,200) within Chebyshev distance ≤ 16 of H;
  T = their centroid; d = H − T.
- Predict the nearest of the 8 unit vectors
  (E=(1,0), W=(−1,0), S=(0,1), N=(0,−1), SE/SW/NE/NW diagonals; +y = S)
  by max cosine similarity.
- Basis: the tail grounds the truth in the stimulus (the generator's own
  comment); frame 0 avoids all wraparound.

### MOT-5 — induced-motion (motiondir). Truth ∈ {STILL, E, W, S, N}.
Generator: 8 frames 64×64; vertical-stripe surround translates ±6 px/frame;
target dot (240,240,240) is STILL at (32,32) or moves 10 px/frame
(clamped to [4,59]).
- D_f = centroid of pixels with R ≥ 220 per frame (dot is the unique
  brightest object; stripes ≤ 90).
- Δ = D_7 − D_0: |Δx|+|Δy| < 3 → STILL; elif |Δx| > |Δy| → E/W by sign(Δx);
  else S/N by sign(Δy).
- Basis: absolute dot position is truth; the moving surround is the lure
  and is ignored by construction.

## 5. Evidence and determinism

- The audit script reads the 576 verified files, emits
  `predictions.csv` (fixture, truth, prediction, per-family score detail)
  and prints sha256 digests. Run 3×; all three prediction-file digests
  must match or the run is VOID.
- Zero RNG: no random module, no time/entropy inputs; fixture order sorted.
- Committed evidence: the audit script, `predictions.csv`, and the digest
  log. No binaries, no `.zagd` files.

## 6. Kill bars (frozen)

- **KB-FE1 (per family**, HYPOTHESES_R3.md R3-2 verbatim): "per family, KILL
  the 'sense can learn this family' claim if neither a ≥80% separator nor
  an unobservability proof is produced — the family is then defense-scope,
  not a front-end target."
- **Program-level** (R3-2 verbatim): "KILL the audit's usefulness if fewer
  than 4 of 12 families resolve to (a) or (b) with byte-level evidence."
- A family scoring 19/24 (79.2%) does NOT pass — the bar is ≥20/24.
- Families recorded DEFENSE-SCOPE are explicit verdicts with reasons, not
  silent drops. No fixture is relabeled or excluded on this crew's
  authority — any relabel/exclusion recommendation goes to Micah as a
  prereg amendment with the proof as evidence (per the MOT-1 precedent).

## 7. Commit plan

1. This prereg commits ALONE to
   `docs/lab/senses/pam-rebuild/round2/fe1_audit/PREREG_FE1_AUDIT.md`.
2. After the audit: `VERDICT_FE1.md` (12-row table) + audit script +
   predictions + digests, one commit, no binaries.
