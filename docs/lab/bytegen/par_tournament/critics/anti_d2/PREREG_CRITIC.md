# CRITIC 2 (anti-D2) — preregistration (2026-09-24)

Coordinator: parent orchestrator. Stance: D2 PLANREF's overthrow is hollow —
"0¢ vs the plan's declaration" is a tautology (the latch copies the plan's
declared f0 Q16 verbatim; the metric compares against the plan's declared
f0 — the 0¢ is guaranteed by the mechanism, not discovered by measurement),
and plan-provenance is a fatal trust-root flaw (a lying or mistyped plan
owns D2 completely; crew_d measured: typo plan `plan_adv_f0lie.txt`
declares 466.16 for intended 440 → D2 latches 466.16 exactly, 99.99¢ vs
intent). Mandate: DO SOMETHING — beat D2 with something genuinely better,
or falsify the overthrow with measured evidence. Not argument — experiments.

Frozen law: `docs/lab/bytegen/par_dive/PREREG_PAR_DIVE.md` (§2 battery,
§5 red team, §6 adoption bars). Pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Pure Zag,
zero RNG in decision/render paths. Byte-identical reruns proven by
`cmp`/SHA-256. Audio analyzer-first: no listening claims; every audio claim
via Python waveform analysis (spectra/ZCR/autocorr) + SHA-256 identity.

Champion numbers under attack (crew_d, tournament synthesis §2a):
- D2: DET 4/4 byte-identical; fixture output bit-identical to NATIVE
  (9/9 bars, CHOP, coherence = NATIVE).
- RT-LONG honest-cents: D2 **0¢ / 0¢** (original LATCHED f0q=28835840 =
  440×65536 exact; near-miss 460 → same latch) vs NATIVE measured
  **1200¢ / 76.96¢** (renders nominal 880 / 460).
- RT-CASCADE 0/64/0; sustained ABSTAIN code=3; RT-EDGE bit-identical to
  NATIVE; order permutation bit-identical; §5: 5 adversarial plans survive.
- Caveat (measured): f0lie → LATCHED f0q=30550261 = 466.16×65536 exact —
  0¢ vs declaration, 99.99¢ vs trainer intent.

Warning heeded: crew_c's C-gate/rg tried output-sensing as a fix and it was
a preregistered no-op (falsified). Track A below is NOT that rerun: it is a
different mechanism (autocorrelation pitch meter on the cue window, wired as
a full D2+sensor challenger) built to TEST the impossibility thesis with
measurement — predicted to fail for information-theoretic reasons, and the
failure itself is the experiment.

## Verification leg V0 (before tracks; independent reproduction)

V0a. Build `render_d2.zag` + `render_native.zag` from the committed
tournament sources with the pinned znc; verify source SHAs against
`crew_d/results/sources.sha256`.
V0b. D2-C1: fixture `bytegen/fixture/plan_v1.txt` → D2 mix bit-identical
to NATIVE mix (`cmp`).
V0c. RT-LONG original (`crew_c/tests/plan_long.txt`: cue 440 @1–2 s,
RESPOND nominal 880 @28 s) → D2 trace `LATCHED f0q=28835840`; near-miss
(`crew_d/plans/plan_long_near.txt`, nominal 460) → same latch; NATIVE
renders nominal 880 / 460 (ZCR-confirmed).
V0d. f0lie (`crew_d/plans/plan_adv_f0lie.txt`) → D2 `LATCHED f0q=30550261`.
If any V0 leg fails, that is itself the finding (champion numbers not
reproducible) and tracks are re-scoped.

## TRACK A — challenger: absolute honesty via independent sensing

**Design.** `render_d2sense.zag`: D2's three phases unchanged, except the
Phase-B latch sets f0 := SENSOR reading (not the plan's declared f0).
Sensor: autocorrelation pitch meter on the phase-A cue-window mix
[w0,w1), DC-removed, lags 36..1102 samples (40..1225 Hz), parabolic
interpolation at the peak, output Q16. This is a genuine best-effort
independent sensor: it never reads plan pitch text (only w0/w1 window
bounds and sample audio). Rationale for expecting failure: the cue audio
IS f(plan-declared f0) — every world with the same plan text renders
byte-identical audio, so no function of (plan text, audio) can recover
trainer intent when text ≠ intent. The sensor can at best re-measure the
declaration, with strictly more noise than D2's exact copy (vibrato
15¢ depth + 110 Hz bed under the cue + harmonic stack + integer
rendering). crew_c's falsified C-gate/rg is consistent with this wall;
this track measures the wall rather than re-arguing it.

**Fixtures.** RT-LONG original + near-miss (clean), f0lie (typo 466.16),
plus declared-cue sweep plans (same skeleton, cue declares 415.30,
466.16, 220, 880, 523.25; nominal 880; w0=1.0, w1=2.0).

**Preregistered predictions.**
- P-A1a (self-consistency): on EVERY fixture, |sensor − declared| < 50¢;
  specifically on f0lie the sensor reads ≈466.16 (the typo), NOT 440
  (intent). The sensor re-measures the declaration; it has no channel to
  intent.
- P-A1b (strictly noisier): on clean fixtures |sensor − declared| > 0 —
  measured RMS error reported; sources decomposed (vibrato/bed).
- P-A1c (challenger loses): D2+sensor intent-grounded cents ≥ D2's on all
  fixtures (strictly worse on clean via sensor noise; identical on typo
  fixtures since both read the typo). D2+sensor therefore cannot beat D2.

**Kill bar (Track A BEATS D2):** the sensor recovers trainer intent on
typo fixtures within 50¢ (e.g. reads ≈440 on f0lie) while matching D2
elsewhere (0¢ clean RT-LONG, 9/9 bars, bit-identical non-RESPOND output,
byte-identical reruns, §5 survival). **Predicted: FAIL** — Track A is
expected to falsify itself by measurement, which PROVES the
information-theoretic ceiling: no renderer in this architecture (plan text
+ f(plan) audio as the only channels) can be "absolutely honest" vs intent;
D2's relative honesty (exact fidelity to the plan's cue declaration) is the
achievable maximum. A clean Track A failure RAISES confidence in D2.

## TRACK B — falsification: realistic typo families, intent-grounded cost

**Metric.** Intent-grounded honest-cents: 1200·log2(rendered_f0 / 440),
where 440 Hz is the trainer's intent (the battery's true cue). The frozen
battery metric (vs plan-declared) is ALSO reported per fixture to show the
tautology explicitly (D2 ≡ 0¢ by construction on every latch).

**B1 — typo family (human plan-authoring errors).** Base plan = RT-LONG
original skeleton (BED 110 Hz; EVENT cue @1–2 s declares C_decl; RESPOND
@28 s, w0=1.0, w1=2.0, nominal 880). C_decl ∈ {440 (clean), 466.16,
415.30 (semitone slips ±100¢), 404, 446 (digit slips), 220, 880 (octave
slips ±1200¢), 1760 (+2400¢), 4400 (extra-zero +3986¢), 44.0 (decimal slip
−3986¢)}. Render each with fresh D2 + NATIVE builds; record latched /
rendered f0 from traces + ZCR/autocorr confirmation on the response
window.
Predictions:
- P-B1a: D2 latches C_decl exactly (f0q = C_decl×65536) on all 10 — gates
  1–2 pass everywhere (audio is self-consistent; the typo is IN the plan).
- P-B1b: NATIVE renders 880 on all 10 → 1200¢ intent error throughout.
- P-B1c (loss-region map): D2 intent error < 1200¢ for |typo| < 1200¢;
  D2 intent error > 1200¢ (worse than NATIVE) for |typo| > 1200¢ (1760,
  4400, 44.0). Crossover exactly at |C_decl − 440| = 1200¢. This MAPS —
  with numbers — where D2's confident-wrong latch is worse than NATIVE's
  nominal render. (On the frozen battery metric D2 still scores 0¢ on all
  10 — the tautology made visible.)

**B2 — expected cost at realistic rates.** Typo model (documented
assumption, swept): per-RESPOND cue-field typo probability p ∈ {0.01,
0.05}; conditional on typo: semitone 50% (100¢), digit 20% (≈86¢ mean of
404/446), octave 20% (1200¢), extreme 10% (≈3457¢ mean of 1760/4400/44.0).
E[D2 intent-¢] = p·(0.5·100 + 0.2·86 + 0.2·1200 + 0.1·3457) ≈ p·653¢;
E[NATIVE] = 1200¢ constant.
Prediction P-B2: measured family-weighted mean intent error: D2 ≈ 6.5¢
(p=0.01) / ≈ 32.7¢ (p=0.05) vs NATIVE 1200¢ — D2's failure mode is
>10× cheaper at realistic rates.
**Falsification criterion (Track B FALSIFIES the overthrow):** measured
E_D2[intent-¢] EXCEEDS E_NATIVE = 1200¢ at p ≤ 0.05. Predicted: NOT met.

**B3 — machine-error boundary probe (planner Q16 units bug).** Plan with
cue declaring 0.00671 Hz (what a planner emitting raw Hz instead of Q16
would write for intended 440). Prediction P-B3: D2 latches f0q=440 →
renders ≈0.0067 Hz (≈DC/silence — catastrophic confident-wrong);
NATIVE renders 880 (1200¢ off but a real tone). Documents that D2 carries
NO range sanity check on the latch (contrast B-gate's 40–4000 Hz pitch
gate). Labeled as boundary probe (bug rates are not well-defined), not a
falsification leg.

**B4 — semantic note (diagnostic, challenges the battery, not the
verdict).** Under the alternative semantics "nominal = intended response"
(e.g. musical call-and-response at a different pitch), NATIVE trivially
wins intent-¢. This restates that D2's overthrow is CONDITIONAL on the
frozen battery's echo-the-cue semantics ("the frozen battery defines 460
as a lie"). No experiment can settle which semantics is "right" — the
trainer's intent is external. Reported as context; changing the semantics
needs Micah's word (frozen law).

## What counts as what

- **BEAT (Track A):** per kill bar above — sensor recovers intent ≤50¢ on
  typo fixtures with no regression elsewhere. Tournament verdict changes.
- **FALSIFIED (Track B):** per falsification criterion above —
  E_D2 > E_NATIVE at realistic p. Overthrow verdict falsified, stated
  with numbers.
- **FAILED-genuine:** Track A confirms P-A1a/b/c (impossibility measured);
  Track B confirms P-B1a/b/c + P-B2 (D2 cheaper at realistic rates; loss
  region mapped to the |typo|>1200¢ tail). Confidence in D2 RAISED; the
  caveat is quantified, not removed.
- **PARTIAL:** any leg's prediction fails in a way that opens a new attack
  (documented with numbers).

## Ground rules compliance

Pure Zag (renderers + sensor); Python only for plan generation and
waveform analysis (analyzer-first). Zero RNG anywhere in decision paths —
the typo "family" is a fixed enumerated set, no sampling. Pinned znc.
Byte-identical reruns proven by cmp/SHA-256 (2 runs per render leg).
Rendered artifacts stay local, never shown to Micah. No synthesis-doc /
crew-evidence / parked-item modifications. Scratch:
`~/workspace/par_critics/anti_d2/`.
