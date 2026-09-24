# TIMBREDISC AUTOPSY — R2-16 CH-TBD-2 white-box defect

Autopsy crew report, 2026-09-23. Work dir `round2/forks/R2-16/`.
Scope: analysis + instrumentation only. No mechanism changed, no fork built.

## 0. The mechanism in 5 lines

1. The fixture audio is **16000 Hz** (`RATE=16000` in the R2FX builder; `SR=16000` in the
   frozen harness generator), but R2-16's Goertzel table was computed as
   `2cos(2π·440·m/32000)·1024` — correct only if the sample rate were 32000 Hz.
2. Every bin therefore sits at **half** the intended frequency: m=1→225 Hz, m=2→436 Hz
   (≈ the 440 Hz fundamental), m=3→658 Hz, instead of 440/880/1320 Hz.
3. So `p2` measures the fundamental's **peak** while `p1` measures **ramp-edge residue**
   at 225 Hz where no tone exists: `r2 = p2·1000/p1` is ~10^10, **seven orders of
   magnitude above the template scale** (max template value 2560).
4. The nearest-template decision is therefore **always d1** (it has the largest
   t2=1960; d1 wins whenever r2>1300; observed min r2 = 1.49×10^9). CH-TBD-2 as built
   is a **constant classifier** — the "ratio" carries no timbre information at all.
5. The mapping choice only re-labels the constant: theory (d1→BRIGHT) emits BRIGHT
   always; swapped (d1→RICH) emits RICH always. FI counts are just the formation's
   wrong-claim counts for those labels: **347** (BRIGHT) vs **52** (RICH) — reproduced
   exactly. The swap "worked" by betting on the formation's rarer error, not by
   measuring timbre.

## 1. The anomaly (as documented in BUILD_NOTES.md)

- Theoretically-correct mapping (d1(1960,2560)→BRIGHT, d3(640,384)→RICH, matching the
  generator's `TMB_TMPL`): **347/985** false installs.
- Empirically-optimal swapped mapping (d1→RICH, d3→BRIGHT): **52/985**.
- Builder's diagnosis: "systematic bias in Goertzel ratio vs generator templates",
  root cause unidentified. This autopsy identifies it.

## 2. Method: bit-exact white-box replication

- Replicated `tb_goertzel` / `tb_chal` / `tb_form` **bit-exactly**, including Zag i64
  semantics: `+,-,*` wrap mod 2^64, `/` truncates toward zero, `p<0 → 0` clamp.
  (The wrap matters: `s1·s2·coeff` overflows i64 — see §7.)
- Verified against the frozen binary `forks/R2-16/build/r216`: **32/32 fixtures**
  match on formation judgment AND challenge outcome (normal + adversarial).
- Built a C batch harness (`tbdump`, same arithmetic) and ran all **985** b_adv
  timbredisc fixtures from `R2-16/evidence/b_adv.list` under two coefficient tables:
  R2-16's (broken) and R2-14's (nominally "880·m").
- Cross-checked the corrected instrument with exact-DFT harmonic energies at the
  true bins (float64, no quantization).

## 3. Root cause #1: 2× sample-rate error (the "fix" that broke it)

Fixture chain sample rates (all 16000 Hz):
- `fixtures/gen_r2.py`: `SR = 16000`; `write_pcm` writes `rate=16000` in the header.
- `forks/R2-7/src/gen_r2a.py` (R2FX builder): `RATE = 16000`, `AU_N = 32000` = 2.0 s.

R2-16's `tb_coeff` comment: "EXACT coefficients for 440*m Hz, N=32000
`(2cos(2*pi*440*m/32000)*1024, rounded)`". The identity
`2cos(2π·f·N/(sr·N)) = 2cos(2πf/sr)` holds only for **sr=32000**. At the true
sr=16000, Goertzel bin `k=440m` of a 32000-DFT is `440m·16000/32000 = 220m` Hz.

Measured bin centers (from the quantized coefficients, N=32000, sr=16000):

| m | R2-16 coeff | true center | intended |
|---|------------|-------------|----------|
| 1 | 2040 | **225.2 Hz** | 440 Hz |
| 2 | 2018 | **436.4 Hz** | 880 Hz |
| 3 | 1980 | **658.0 Hz** | 1320 Hz |
| 4 | 1927 | 879.7 Hz | 1760 Hz |

So `p1` sits at 225 Hz (no tone energy — only 20 ms raised-cosine ramp-edge
residue), `p2` sits 3.6 Hz from the 440 Hz fundamental (**peak**), `p3` at 658 Hz
(residue between the 440/880 Hz tones).

**The R2-14 irony.** R2-14's table was `2cos(2π·880·m/32000)·1024` with the comment
"coeff x1024 for k=880*m" — the builder believed sr=32000 and thought it measured
880·m Hz ("off-by-one harmonic", per R2-16's notes). At the true sr=16000, bin
880m = **440m Hz — exactly the intended harmonics**. R2-14's "bug" was accidentally
correct; R2-16's "exact fix" halved every bin and introduced this defect. Residue of
the R2-14 error persists only as folklore: the 880m table was right for the wrong
reason.

## 4. Why the challenge is a constant classifier (numbers)

Broken-instrument measurements on normal fixtures (G span, bit-exact):

| truth | p1 @225Hz | p2 @436Hz | p3 @658Hz | r2 = p2·1000/p1 | r3 | nearest | theory→ | swapped→ |
|-------|-----------|-----------|-----------|-----------------|----|---------|---------|----------|
| PURE   | 1,053,301 | 11,619,605,827,377 | 373,097 | **11,031,609,983** | 354 | d1 | BRIGHT | RICH |
| BRIGHT | 10,399 | 220,833,926,968 | 2,794 | **21,236,073,369** | 268 | d1 | BRIGHT | RICH |
| DARK   | 796,725 | 7,927,076,819,855 | 218,684 | **9,949,577,106** | 274 | d1 | BRIGHT | RICH |
| RICH   | 249,560 | 2,314,034,772,294 | 4,714 | **9,272,458,616** | 18 | d1 | BRIGHT | RICH |

Template points: d0(0,0), d1(1960,2560), d2(78,6), d3(640,384).
d1 beats d3 iff `(r2−1960)² < (r2−640)²` iff **r2 > 1300**; beats d2 iff r2 > 1019;
beats d0 iff r2 > 980. Observed r2 range on 985 adv fixtures:
**min 1,486,407,376, p50 9,958,484,168, max 541,949,613,107**.
The r3 term can never compensate (bounded by ~r3·2176 against an r2-term gap ≥
2·r2·1320). Result on the full battery: **985/985 fixtures pick d1** under both
mappings. The challenge emits one constant label; the "ratio" is degenerate, not
biased — r2 sits ~7 orders of magnitude above template scale, so there is no
"bias vs the templates" to correct. The builder's diagnosis was wrong.

On the residue itself: p1 varies 100× across classes (10,399 BRIGHT … 1,053,301
PURE) because the 225 Hz response is ramp-edge + quantization residue whose shape
depends on harmonic content and (random) harmonic phases — but it is 6–9 orders of
magnitude below p2 in all cases, so it cannot rescue the ratio. Synthetic check:
an unramped 880-cycle tone gives p1=1,848,687,378 (quantization off-center 0.3
bins + hard edge); with the generator's 20 ms ramps p1=81,734 — the ramps
*suppress* the residue. Window-edge effects are real but are not the driver; the
driver is that the bin is tuned to a frequency where no tone exists.

There is **no second tone** in any timbredisc fixture (single 440 Hz tone; TMB-3
"distractors" are single tones with different harmonic profiles), so "spectral
leakage from the second tone" is ruled out. Frame alignment is exact (32000
samples = 2.0 s; the 440 Hz tone completes exactly 880 cycles).

## 5. Why swapping "helps": formation wrong-claim arithmetic

Support rule (R2-16): INSTALL iff challenge outcome == formation claim.
With a constant challenge C: FI = #{formation claims C **and** claim ≠ truth}.

The formation (`tb_form`) uses the same mistuned table: its even-m bins land on
true harmonics (m=2→436, m=4→880, m=6→1320 Hz) while odd-m bins see residue, so
its "centroid" ≈ 2× the true centroid (plus i64-wrap garbage — e.g. PURE normals
get cent=−474,256,640, which bins as PURE only by accident of the `<520` test).

Formation (claim × truth) on the 985 b_adv timbredisc fixtures (bit-exact):

| claim \ truth | BRIGHT | DARK | PURE | RICH |
|---------------|--------|------|------|------|
| BRIGHT | 21 ok | **78** | **47** | **222** |
| DARK   | 1 | 12 ok | 5 | 18 |
| PURE   | 30 | 90 | 89 ok | 259 |
| RICH   | **3** | **33** | **16** | 61 ok |

- Theory mapping (constant BRIGHT): FI = 78+47+222 = **347/985** ✓ reproduces anomaly.
- Swapped mapping (constant RICH): FI = 3+33+16 = **52/985** ✓ reproduces anomaly.

The swapped mapping does not measure timbre better — it cannot, the instrument is
degenerate. It wins by agreeing with the formation's *rarer* wrong answer (the
mistuned formation claims BRIGHT wrongly 347×, RICH wrongly 52×). This is a
surface patch over a broken instrument, exactly the kind Micah's law forbids.

## 6. Root cause #2: coefficient quantization (÷1024) — hits R2-14/R2-7 too

Running the same 985 fixtures under R2-14's table (nominally correct for
sr=16000): the challenge is **still constant** (985/985 → d1). Why: at N=32000,
one LSB of the ÷1024 coefficient moves the bin by ~14.5 bins near k=880
(d(bin)/dLSB = (N/2π)/(S·sin ω)). The exact value 2cos(2π·880/32000)·1024 =
2017.504 — **no integer** centers the bin; c=2018 → bin 872.8 (**7.2 bins**
below the 440 Hz tone), c=2017 → bin 887.3 (7.3 above). Measured attenuation of
p1: **0.000707 in power** (float-Goertzel check on a pure tone). So r2 is
inflated ~1400× for every class (observed: min 18,465, p50 341,816, max
13,241,334 — all > 1300 → d1 always). R2-14's front end was right in nominal
frequency but unusable in practice: the ÷1024 quantization cannot place a bin on
440 Hz at N=32000.

## 7. Root cause #3: i64 overflow in the Goertzel power formula (latent)

`p = s1*s1 + s2*s2 - s1*s2*coeff/1024`: for an on-bin tone at 12000 peak,
s1,s2 ~ 10^9, so `s1·s2·coeff` ~ 2.4×10^21 overflows i64 (max 9.2×10^18) and wraps
mod 2^64. The wrap quantum is 2^64/1024 = 2^54 ≈ 1.8×10^16 — **comparable to the
signal power itself** (float check on real fixtures: p_true/2^54 = 0.04…2.01;
one fixture had p_true=7.0×10^14 with a wrap term of −5.5×10^15, 8× the signal).
Any corrected CH-TBD-3 must rewrite this as
`p = s1*s1 + s2*s2 - (s1*s2/1024)*coeff` (divide before multiply; max
intermediate ~2×10^18, no overflow) or use wider arithmetic. In the R2-16 data
this defect is masked by root cause #1 (r2 stays astronomically large regardless),
but it would corrupt a fixed front end.

## 8. Knowledge vs machinery: verdict = MACHINERY

- **The theory was correct.** The generator's `TMB_TMPL` labels are arithmetically
  consistent with its `TMB_PROFILES`: DARK (0.28², 0.08²)·1000=(78,6) ✓,
  RICH (0.8², 0.62²)·1000=(640,384) ✓, BRIGHT ((0.7/0.5)²,(0.8/0.5)²)·1000=
  (1960,2560) ✓ (weak fundamental a1=0.5 correctly normalized). The builder's
  theory mapping d1→BRIGHT, d3→RICH was right.
- **Proof by corrected instrument:** exact-DFT harmonic energies at the true bins
  (880·h) with the THEORY mapping classify 8/8 normal fixtures with ratios landing
  *on* the templates — BRIGHT→(1959.8, 2559.8), DARK→(78.4, 6.4),
  RICH→(640.0, 384.4), PURE→(0,0) — and 20/20 TMB-3 adversarial distractors,
  including the weak-fundamental BRIGHT (r2=12251=(0.7/0.2)²·1000 ✓) that the
  template design was built for.
- **What failed was the instrument**, three times over: (1) 2× sample-rate error
  from assuming sr=32000 (the "exact" fix that broke R2-14's accidentally-correct
  table); (2) ÷1024 coefficient quantization unable to center 440 Hz at N=32000
  (±7 bins); (3) i64 overflow in the power formula with quantum ~ signal power.
- No knowledge gap: nobody misunderstood what the tones look like; the Goertzel
  was simply tuned to the wrong frequencies with unplaceable, overflowing
  arithmetic.

## 9. Cross-fork impact: the program's timbredisc story is largely front-end artifact

| Fork | Coeffs | Mapping | Timbredisc number | Assessment |
|------|--------|---------|-------------------|------------|
| R2-14 | "880m" = correct nominal @16000 | theory | **227/985 = 23.05%** FI | **Same artifact.** Reproduced exactly by this autopsy (constant challenge via quantization-inflated r2 + theory mapping → FI = formation wrong-BRIGHT = 227). Its postmortem blamed enumeration; the front end was the driver. |
| R2-7 | same as R2-14 | theory | **~158** FI (B5) | **Same artifact** (mechanism proven by shared code path; constant challenge; its margin≥20000 gate is vacuous at the quantization-inflated r2 scale, margin always ≫ 20000). Exact count UNVERIFIED on R2-7's own battery — mechanism-verified only. |
| R2-16 | "440m" = 2× mistuned | swapped | 52/985 FI (347 theory) | This autopsy. Constant challenge; swap bets on rarer formation error. |
| R2-8 | **different**: reads sr from .pcm header, f0-robust DFT at h·f0 | n/a | **0/720 = 0% recall** | **NOT this artifact.** Front end is correctly calibrated; the verdict explicitly attributes it to an overstrict gate ("withholds even when the percept is correct"). Gate story, stands as written. |

Net: three forks' timbredisc FI numbers (R2-7 ~158, R2-14 227, R2-16 52/347) are
dominated by the Goertzel front-end defects, not by gate discrimination. Only
R2-8's timbredisc result is a genuine gate story.

## 10. Prescription: what a corrected CH-TBD-3 would compute (analysis only)

1. **Sample rate**: use the true sr=16000 — read it from the fixture header
   (R2-8 already does: `t_get32(buf,0)`) or hardcode with an assertion. Target
   bin k = round(f·N/sr).
2. **Coefficient scale ≥ 2^20, not 1024**: `coeff = round(2cos(2πk/N)·2^20)`,
   divide by 2^20. At N=32000 this centers bins within ~0.03 bins (vs ±7.2 now).
3. **Overflow-free power**: `p = s1*s1 + s2*s2 - (s1*s2/SCALE)*coeff`
   (divide before the final multiply), or accumulate in 128-bit. Keep the
   `p<0 → 0` clamp only as a rounding guard, not as overflow concealment.
4. **Keep the THEORY mapping** d0(0,0)→PURE, d1(1960,2560)→BRIGHT, d2(78,6)→DARK,
   d3(640,384)→RICH — proven correct in §8. The swapped mapping must be reverted.
5. **Fix the formation identically** (`tb_form` shares `tb_coeff`; its
   520/950/1550 Hz bin boundaries assume true Hz).
6. **Unit test** (from §8): exact-DFT ratios on the 4 normal profiles must land
   within rounding of TMB_TMPL with the theory mapping — 8/8 normals, 20/20
   TMB-3 shown here.

## 11. Caveats / UNVERIFIED

- The i64 **wrap** (vs trap) model of znc arithmetic is assumed; it reproduces the
  frozen binary 32/32 on (judgment, outcome), but absolute `p` magnitudes were
  not read out of the binary (ledger exposes only bestd) — treat exact p values
  as model-verified, the mechanism conclusions as binary-verified.
- R2-7's ~158 FI: mechanism-verified via the shared coefficient table and the
  R2-14-coefficient run; the exact count on R2-7's own battery was not re-run —
  UNVERIFIED as a count, VERIFIED as a mechanism.
- The ÷1024 quantization analysis assumes the builder's documented formula; the
  7.2-bin offset and 0.000707 attenuation are measured, not assumed.

## 12. Provenance

- Bit-exact replication: `/home/hatch/workspace/tmp_autopsy/goertzel.py`
  (32/32 vs binary), batch harness `/home/hatch/workspace/tmp_autopsy/tbdump.c`.
- Fixture lists: `R2-16/evidence/b_adv.list` (985 timbredisc).
- Key sources: `forks/R2-16/src/r216.zag` (tb_coeff/tb_goertzel/tb_chal/tb_form),
  `forks/R2-7/src/gen_r2a.py` (`RATE=16000`, `TMB_TMPL`, `TMB_PROFILES`,
  `synth_tone`), `fixtures/gen_r2.py` (`SR=16000`, `TIMBRES`, `_tone_np`),
  `forks/R2-14/src/r213.zag` (880m table), `forks/R2-8/src/sense_r28.zag`
  (header-sr front end).
