# Hybrid v2 — three-piece specification

**Status:** implements the grok-4.7 attack battery's converged architecture
(`~/workspace/bytegen/grok47/ATTACKS.md`, 2026-09-23). Replaces the v1
"bounded single loop" design, which the battery proved incoherent.
**Source:** `src/render_hyb.zag` (pure Zag, pinned
`toolchain/bin/znc_linux_x86_64_abed8aa1`, zero RNG).
**Fixture:** `bytegen/fixture/plan_v1.txt` (23 events, 30 s @ 44.1 kHz).

## 0. The three pieces

| # | Piece | Default | State | Authority |
|---|-------|---------|-------|-----------|
| 1 | PAR motif path | **always** | zero carried state | all synthesis parameters, always |
| 2 | Exception detect-and-reassert | idle (fires only on fault) | stateless | re-render a corrupted block plan-pure, nothing else |
| 3 | RESPOND octave latch | idle (fires once per RESPOND) | one-shot | octave-correct a RESPOND's nominal pitch, nothing else |

There is **no continuous feedback loop**. The v1 per-block servo
(gain/brightness/vibrato chasing frozen targets) is **deleted, not bounded**
(see §6).

## 1. Piece 1 — PAR motif path (default)

Every sample is a pure function `s[t] = F(plan, t)`: `voice_q16`/`bed_q16`
ported verbatim from `fork_par/src/render_par.zag`. No phase accumulators,
no carried servo state, no measurement. Rendering is block-major
(1024-sample blocks) but integer adds commute, so output is bit-identical
to PAR's event-major order — proven empirically: hybrid clean WAV is
**byte-identical** to `fork_par/src/par_seq1.wav`.

Piece 1 is the SOLE authority over: event existence, timing, duration,
envelope, bed level, timbre, vibrato, and pitch of ordinary events.
Pieces 2 and 3 cannot alter any of these.

## 2. Piece 2 — exception detect-and-reassert (the region-scoped servo)

After each 1024-sample block renders, the block is analyzed
(`analyze`: ZCR Q6M, RMS Q16 FS, peak Q16) and compared against the
**plan-derived target** `T = K_PLAN · plan_rms(block)` (§5).

**Fault predicate** (integers, no floats):
- `peak > 8.0 FS` (Q16 `524288000`), or
- `T ≥ SILENCE_FLOOR (2000)` and (`rms > 2.5·T` or `rms < 0.35·T`).

On fault: the block is **re-rendered plan-pure** (overwrite, `render_block`),
restoring the exact bytes piece 1 produced. Detections are logged per block.

### Authority
Piece 2 may only replace a block's bytes with `F(plan, t)` for that block.
It cannot change parameters, invent content, or touch uncorrupted bytes.

### Contractivity (proof)
The correction map is `C(x) = plan_render(block)` — **constant in `x`**.
Hence Lipschitz constant `L = 0 < 1`: a contraction. It is idempotent,
`C(C(x)) = C(x)`, and converges in exactly one application. It cannot
2-cycle, rail-pin, or hold memory across blocks: there is no carried state
(silence carries nothing — Attack 4's "infinite memory" is structurally
impossible). A false positive is a **no-op**: re-rendering uncorrupted bytes
yields identical bytes, so the band edges carry no safety risk, only a
perf cost (~1 block re-render).

This replaces v1's update `g ↦ clamp(T/(g·S))`, which the battery exposed as
a neutrally stable **involution** (`f(f(g)) = g`, `f′(g*) = −1` at the fixed
point): rail pins and sustained 2-cycles constructible from plan text,
untunable by magnitude clamps. Forward gain correction is additionally
**causally wrong** for this fault model: it would distort clean future
audio to "compensate" already-rendered corruption. Re-assertion is the
only correction that heals the past.

### Fault model assumption
Detection must precede consumption (verified double-buffer): the block is
re-rendered before the mix is written out. Under this model healing is
exact — proven: 64-sample bit-flip, full-block dropout, and 1292-block
sustained corruption all recover to **0 differing samples** vs clean.

## 3. Piece 3 — RESPOND octave latch (discrete plan-level event)

RT-LONG as a **discrete event latch that re-enters as plan input**, not
carried audio state (Attack 11). Fires once, at the block containing the
RESPOND's onset, before that block renders, measuring only
already-rendered (and exception-healed) audio.

**Gates** (all must pass; else the plan nominal stands):
1. **Well-posedness** (plan-grounded): exactly one rendered voice overlaps
   the source window `[w0, min(w1, now)]` (self excluded). Polyphonic cues
   abstain — ZCR of a sum is nobody's f0 (Attack 3(iii)).
2. **Stationarity**: ZCR of the two window halves agrees within 12%.
3. **Band**: measured `f_m ∈ [40, 4000]` Hz.

**Octave rule.** The ZCR estimator carries a **~97-cent sharp bias** on
harmonic cues (measured: 456 Hz on a true 440 Hz cue; 465 Hz in the old
battery — Attack 3(v)). It is an **octave-error detector**, not a pitch
meter. Hence: `k = round(log2(f_m / f_nom))`; if `k ≠ 0` — i.e. the nominal
is more than **600 cents** off, safely above the bias — the response pitch
is set to **`f_nom · 2^k`: the plan's own octave-corrected value, never the
raw biased measurement**. A 440 Hz cue mislabeled 880 latches to exactly
440 (not 456/465). Sub-octave disagreements keep the nominal: with a
±97-cent-biased sensor, "correcting" a 4-semitone error would be
fabrication, and the honest move is abstention (Attack 2's settling test).

The nominal is preserved in field 11; the latch writes field 2 once and
clears kind. There is no loop, hence no stability question; the corrected
value is a pure function of (plan nominal, quantized octave offset).

## 4. Bounds summary

| Parameter | Bound | Enforced by |
|-----------|-------|-------------|
| Synthesis (piece 1) | = plan, always | construction (pure function) |
| Exception correction (piece 2) | re-render ≤ 1 block per detection; output bytes ∈ {plan-pure} | constant correction map (L=0) |
| RESPOND pitch (piece 3) | `f_nom · 2^k`, one-shot, `k≠0` only | octave quantization + gates |
| Detection band | `[0.35×, 2.5×]` plan-expected RMS, peak `< 8 FS` | integer predicate §2 |
| Estimator trust | octave-scale only (>600¢); sensor bias ±97¢ disclosed | gate, §3 |

## 5. Plan-derived targets (answers Attack 1)

`T(block) = K_PLAN · plan_rms(block)`, where `plan_rms` is analytic:
per-voice `amp · crest(timbre) · envelope(tr)` (crest from the normalized
1/h stack: `0.51 + 0.197/tim`; envelope replicates the renderer's
raised-cosine attack/release exactly), quarter-point power-averaged over
the block, plus the bed. **No fixture loudness constant**: on a quiet
ambient plan the target is that plan's own level — rail-pinning toward a
frozen 0.19 FS (Attack 1's settling-test prediction) is structurally
impossible.

`K_PLAN = 49585` (Q16; = 0.7566) maps the analytic model to this build's
synth output: measured 2026-09-24 as `median(measured_rms/analytic_rms)`
over all 1292 fixture blocks. Spread: min/median 0.57, max/median 1.43 —
all inside `[0.35, 2.5]` with margin. Re-calibration procedure: rebuild,
run mode `cal`, take the median ratio. `K` is an implementation calibration
(synth↔model bridge), not a musical judgment; the wide band absorbs model
error including coherent voice cross-terms the analytic cannot know.

## 6. What was removed and why

The v1 continuous servo (per-block AGC gain, brightness, vibrato chasing
`RMS 0.19 / ZCR 0.016`) is **deleted**:
- **Attack 1 (mistargeted):** the targets were literals measured from
  `plan_v1.txt` — on any other plan the loop permanently fights the plan
  toward constants the plan didn't author. The 9/9 gate pass was measured
  on the tuning plan: an overfitting check.
- **Attack 4 (non-contractive):** the update `g ↦ clamp(0.19/(g·S))` is an
  involution with `f′ = −1` — neutrally stable 2-cycles and rail pins are
  constructible from plan text alone; silence holds state (infinite
  memory). Magnitude clamps bound outputs, not history-dependence.
- **Attack 6/11 (structural):** motif renders identically iff servo entry
  states match — 0.74 was 946 blocks of state carry, untunable by clamps.
  No single loop can both remember 27 s (RT-LONG) and be history-independent
  (recurrence 1.0). The three pieces separate the two jobs.

What survives of AR is **exception-path correction** (fault/dropout),
not "the renderer discovers facts."

## 7. Revocation

There is no revocation mechanism, and none is needed:
- Piece 2 is stateless and idempotent — there is no authority to revoke;
  a false detection self-corrects to a no-op.
- Piece 3 fires once per RESPOND; a failed gate leaves the nominal
  untouched — the plan is never mutated speculatively.
- The v1 concepts (8-block revoke windows, 3-strike episode revocation)
  belonged to the deleted loop and are gone with it.

## 8. Honest limits (detection floor)

- Corruption must move a block's RMS outside `[0.35×, 2.5×]` of
  plan-expected or its peak above 8 FS. A 64-sample zeroing moves block
  RMS ×0.97 — **below the floor** (would need >899/1024 samples zeroed to
  trip the RMS edge); small low-bit corruptions are likewise invisible.
  Bit-flips are caught by the peak edge.
- The RESPOND sensor is octave-scale only; sub-octave plan errors are
  kept as nominal (abstention, not correction).
- The fault model assumes detection precedes consumption (§2).

## 9. Attack-battery mapping

| Attack | Verdict on v1 | v2 answer |
|--------|---------------|-----------|
| 1 frozen targets | REAL | targets derived from the plan under render (§5) |
| 2 plan authority | REAL (w/ corrections) | nominal preserved (field 11); latch is a pure predicate; sub-octave abstention |
| 3 ZCR sensor | REAL (all five) | polyphony gate, stationarity, 40–4000 Hz; octave-only trust (§3) |
| 4 non-contractive | REAL | loop deleted; correction map Lipschitz 0 (§2) |
| 5 PAR-default regimes | MIXED | out of offline-render scope; documented |
| 6 0.74 structural | REAL (theorem) | zero carried state → recurrence 1.000000 |
| 7 security | REAL | no sensor write-path into future rendering; parser gaps are PAR-shared |
| 8 fragility ranking | REAL | cents-honest RT-LONG claim (octave detection, not pitch measurement) |
| 9 H1/H2/H3 | H3 wins | built: PAR path + region servo + event latch |
| 10 CHOP-3 spikes | mechanism debunked | pure f(plan,t) is chop-invariant by construction |
| 11 one loop incoherent | REAL (deepest) | three pieces, two memories separated |
