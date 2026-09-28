# CRITIC 2 (anti-D2) — RUNLOG (2026-09-24)

Scratch: `~/workspace/par_critics/anti_d2/`. Pinned znc
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`. Pure Zag
renderers; Python only for plan generation + waveform analysis
(analyzer-first). Zero RNG — the typo "family" is a fixed enumerated set.

## 13:30 PDT — context + prereg
- Read tournament synthesis §2a, crew_d VERDICT/PREREG_D, frozen
  PREREG_PAR_DIVE, render_d2.zag (full source).
- Sparse-cloned `docs/lab/bytegen/{par_dive,par_tournament,fixture,fork_par,hybrid}`
  from tnn-native-lab for local fixture access.
- Wrote `PREREG_CRITIC.md` (Tracks A+B, falsifiable kill bars, V0
  verification leg, B1/B2/B3/B4 definitions). Committed BEFORE any
  experiment: `718415d847277a2600801067064c01791e142383`
  (`docs/lab/bytegen/par_tournament/critics/anti_d2/PREREG_CRITIC.md`).

## V0 — independent reproduction of champion numbers
- V0a: `src/render_d2.zag` SHA `5199cd1d…` and `src/render_native.zag`
  SHA `4f50187c…` match `crew_d/results/sources.sha256`. Built both with
  pinned znc (warnings only, no errors).
- V0b: fixture `plan_v1.txt` → D2 mix `cmp`-identical to NATIVE mix
  (SHA `a30c6577…`).
- V0c: RT-LONG original → `LATCHED f0q=28835840`; near-miss (460) → same;
  FFT on response windows: NATIVE 880.00 Hz / 460.00 Hz (0.00¢),
  D2 440.00 Hz / 440.00 Hz (0.00¢).
- V0d: f0lie → `LATCHED f0q=30550261` (= 466.16×65536 exact).
- V0: all champion numbers reproduce. Tracks proceed as preregistered.

## Track A — D2+sensor challenger
- Analyzer note: naive autocorr pitch meter locks onto the 110 Hz bed
  (bed period 401 samples ≈ 8× the 880 period — they reinforce); FFT
  spectral peak-pick works on response windows (880.00/460.00/440.00/
  466.15 Hz measured, ≤0.03¢). On cue windows the raw FFT peak-pick hits
  a renderer quirk (see below); autocorrelation (global max) reads the cue
  at 439.44 Hz (−2.2¢) and 465.63 Hz (−2.0¢) on 440/466.16 cues.
- **Renderer quirk found (documented, not attacked):** the cue's vibrato
  (nominal "15¢") is implemented as PM with index 4.37 rad (the Q15
  `vs/32768` scaling makes `beta=df/vibhz` land as cycles, not radians);
  J0(4.37)≈−0.34 vs J3(4.37)≈0.36 — the carrier is suppressed and the
  3rd sideband (+16.5 Hz, +60¢) is the strongest spectral peak. A pure
  peak-picker reads +60¢ on cue windows. Autocorrelation is immune (PM
  preserves periodicity). This is why the Zag sensor uses autocorr.
- Built `src/render_d2sense.zag`: D2's three phases + gates unchanged;
  the latch sets f0 := `sense_f0()` (autocorr on the bed-subtracted cue
  window, lags 36..1102, DC-removed, parabolic interpolation, Q16 out)
  instead of the plan's declared f0. The sensor reads only w0/w1 window
  bounds + BED spec (interferer cancellation) + audio — never plan pitch
  text. Fixed one i64 overflow in parabolic interpolation
  (`32768*(r0-r2)` needs the 2^10 downscale; ratio is scale-invariant).
- Results:
  - Clean RT-LONG: `D2SENSE cue_declared_q16=28835840` →
    `LATCHED f0q=28615223` (436.63 Hz, −13.3¢ vs declared). Rendered
    response FFT: 436.65 Hz (−13.2¢ vs true 440). D2: 440.00 (0¢).
  - f0lie: declared 30550261 → `LATCHED f0q=30422501` (464.21 Hz,
    −7.3¢ vs declared 466.16, **+92.8¢ vs intent 440**). Rendered:
    464.23 Hz (+92.8¢ vs intent).
  - Determinism: rerun `cmp`-identical.
- P-A1a CONFIRMED (|sensor−declared| = 13.3¢/7.3¢ < 50¢; reads the typo,
  not intent). P-A1b CONFIRMED (strictly noisier than D2's exact 0¢).
  P-A1c CONFIRMED (D2+sensor ≥ D2 on intent-¢ everywhere; the 7¢ edge on
  f0lie is sensor noise toward 440, not intent recovery).
- **Kill bar (recover intent ≤50¢ on typo): measured +92.8¢. TRACK A FAILS.**

## Track B — typo family, intent-grounded cost
- B1: 11 plans (fixed set, no RNG): clean 440; semi ±100¢; digit
  404/446; octave 220/880; 1760; 4400 (extra-zero); 44.0 (decimal slip);
  0.00671 (planner Q16-units bug). Rendered each with D2 + NATIVE.
  - P-B1a CONFIRMED: D2 latches declared×65536 exactly on all 11
    (28835840, 30550261, 27217100, 26476544, 29229056, 14417920,
    57671680, 115343360, 288358400, 2883584, 439) — gates pass everywhere;
    the typo is self-consistent audio.
  - P-B1b CONFIRMED: NATIVE renders 880 on all 11 → 1200¢ intent error.
  - P-B1c CONFIRMED — loss-region map (intent-¢, |.|):
    D2 wins: clean 0, semi_up 100, semi_dn 101, digit1 149, digit2 24
    (NATIVE 1200 throughout).
    TIE at |typo|=1200¢: oct_dn (D2 −1200 vs NATIVE +1200), oct_up
    (both render 880).
    NATIVE wins: oct2_up 2400, xzero 3986, dec_slip 3996, q16bug
    catastrophic (D2 renders ≈DC/silence).
    Crossover exactly at |C_decl−440| = 1200¢, as predicted.
  - Frozen-metric scoreboard (explicit tautology): D2 ≡ 0.0¢ vs declared
    on all 10 numeric fixtures; NATIVE 0–5186¢.
  - Determinism: reruns `cmp`-identical (D2 + NATIVE).
- B2: family-weighted E[intent-¢] with p(typo)∈{0.01,0.05}, conditional
  {semitone 50%, digit 20%, octave 20%, extreme 10%}:
  E[D2] = p×653.8¢ → **6.5¢ (p=0.01) / 32.7¢ (p=0.05)** vs NATIVE 1200¢.
  Ratios: 183× / 36.7×. P-B2 CONFIRMED (>10× cheaper).
  Note: E[D2] at p=1.0 is 653¢ < 1200¢ — D2 wins in expectation even if
  EVERY cue is mistyped under this distribution.
- **Falsification criterion (E_D2 > 1200¢ at p≤0.05): measured 32.7¢.
  NOT met. TRACK B DOES NOT FALSIFY.**
- B3: q16bug (0.00671 Hz): D2 latches f0q=439 → renders ≈0.0067 Hz
  (≈DC; response window RMS confirms near-silence vs NATIVE's full
  880 tone). P-B3 CONFIRMED — D2 carries no range sanity check on the
  latch (contrast B-gate's 40–4000 Hz pitch gate). Boundary probe,
  labeled as such (bug rates not well-defined).
- B4: semantic note — under "nominal = intended response" (musical
  call-and-response at a different pitch), NATIVE trivially wins
  intent-¢. This restates that D2's overthrow is CONDITIONAL on the
  frozen battery's echo-the-cue semantics. No experiment can settle which
  semantics is right (intent is external); changing it needs Micah's word.

## Artifacts (local only, never for Micah)
- `src/render_d2sense.zag` (challenger), `build/` binaries (uncommitted).
- `plans/b1_*.txt` (11 typo plans), `runs/` (mixes + traces), `results/`
  (empty — scores inline in VERDICT).
- `analyze.py` (FFT/autocorr meter), `b1_score.py` (family scoreboard).
