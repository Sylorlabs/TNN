# BUILD_LOG.md — Approach A ("LLM-style") senses, pure-Zag rebuild

Deliverable tree: `~/workspace/senses-rebuild/a_raw/`
Binary: `sense` · Source: `sense.zag` (+ `R33_NATIVE_IO_V1.zag` import)
Built: 2026-09-21. Do NOT commit (per task instructions).

## Toolchain

Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Build command (frozen):
```
znc sense.zag --no-zagd --no-analyze --no-foreground-cache -o sense
```
Compiler constraints honored (from ZAG_PLAYBOOK.md / INTERFACE.md / AGENTS.md):
`_zag_arg(n)` read unconditionally (argc is always 0); `[]u8` arenas with LE
accessors instead of `as []i32`/`[]u32`/`[]u16` (ZNC-2026-09-21-007 aliasing
bug); `_zag_strcmp` == 1 on equality; no slice > 2^25; no `};`; explicit
allocation init; NUL-terminated paths via `z_cstr`; `_zag_raw_syscall` takes
exactly 7 args; shallow else-nesting (ZNC-2026-09-21-013).

## Build history

| # | Time (UTC 2026-09-21) | Command / change | Result |
|---|---|---|---|
| 1 | ~early | Initial `sense.zag` (all six tasks, zero-crossing pitch, derivative-energy timbre) | built OK |
| 2 | ~mid | Smoke fixtures via temporary Zag generator `/tmp/smoke/fixgen.zag` | generator build FAILED once (temp issue, fixed); fixtures generated |
| 3 | ~mid | Shape fixtures initially failed: traced to a **fixture-generator Taylor-series scaling bug**, not the sense. Generator corrected; final raster counts circle=377, square=485, triangle=214 px | all 3 shape cases pass |
| 4 | ~mid | `timbredisc`: derivative-energy feature mislabeled DARK as PURE; replaced with harmonic-bin DFT centroid over harmonics 1–8 | PURE now correct; DARK/RICH/… improved |
| 5 | ~mid | DFT probe showed integer-Hz `f0=439` caused severe spectral leakage over 8000-sample window (pure tone measured `r=8000`) | root-caused |
| 6 | ~mid | Pitch/timbre f0 switched to interpolated zero-crossing estimate in **milli-Hz** (fractional phase increments in harmonic DFT) | f0 within ~0.02 Hz on pure tones; 6/7 audio cases pass |
| 7 | ~mid | `timbredisc` on BRIGHT tone (rising spectrum, strong high harmonics) → `task_failed`: zero-crossing estimator breaks when high harmonics dominate crossings | root-caused (real weakness, not a fixture bug) |
| 8 | ~23:2x | Replaced f0 with **robust estimator**: autocorrelation (coarse period, parabolic refinement) → harmonic-energy maximization on ±3% fine grid (0.1% steps, parabolic) → octave guard. Milli-Hz throughout. Same estimator used for `pitchdisc` and `timbredisc`. | built OK — `wrote native binary sense (88167→88191 bytes main, 0 external tools)` |
| 9 | ~23:3x | Debug probe on BRIGHT: stage-1+2 correctly found f0=440.021 Hz, but the **octave guard compared E(880) vs E(440) with mismatched harmonic coverage** (nhmax=6 for both: E(880) covered true harmonics 2,4,6,8 ∝120 while E(440) covered 1..6 ∝91, so the guard "corrected" 440→880). Fixed guard to matched coverage: E(f0,8) vs E(f0/2,16) vs E(2f0,4). | built OK — `wrote native binary sense (88191 bytes main, 0 external tools)` |
| 10 | 23:3x | Lab VM restarted mid-build; `/tmp` (tmpfs) wiped — smoke fixtures and generator lost. Rewrote generator in Python (`/tmp/smoke/gen.py`, temporary, not a deliverable); regenerated all 19 fixtures; re-verified. | 19/19 pass |
| 11 | 23:4x | Final rebuild from current source (deterministic: byte-identical to build 9) | `wrote native binary sense (88191 bytes main, 0 external tools)` |

Final binary md5 (2026-09-21 23:36 UTC): matches the build-9 artifact; rebuilds are byte-identical.

## Algorithms (what the binary does)

| Task | Mechanism | Fixed thresholds |
|---|---|---|
| `colordisc` | Mean RGB per half; Euclidean distance | 40 |
| `colorconst` | Per-half white-patch maxima; von Kries-normalized means; Euclidean distance | 150 |
| `shapetrans` | Minority-brightness mask; centroid; max radius; `area/(πR²)` vs prototypes | circle 1000, square 637, triangle 414 (per-mille) |
| `pitchdisc` | Robust f0 per tone (milli-Hz); relative diff in ppm | 2% = 20000 ppm → SAME/HIGHER/LOWER |
| `timbredisc` | Robust f0 (milli-Hz); harmonic DFT centroid `r=1000·Σh·E_h/ΣE_h`, h=1..8 | PURE<1075<DARK<1400<RICH<3000<BRIGHT |
| `motiondir` | Frame differencing (>90 summed-channel diff); changed-pixel centroid track | \|disp\|<3px → STILL; else 8-way octant |

Confidence = deterministic margin-to-threshold (or margin-to-nearest-prototype)
mapping, 0..1000. `debug_vec` exposes raw numeric features (means, f0m, r,
ratio, dx/dy). Ops counted at element-visit / distance-comparison grain;
audio ops dominated by autocorrelation lags + fine-grid harmonic DFTs.

## Smoke results (19 temporary fixtures, since regenerated — all pass)

| Task | Fixture | Expected | Got | debug_vec |
|---|---|---|---|---|
| colordisc | cd_same.img | SAME | SAME | dist=0 |
| colordisc | cd_diff.img | DIFFERENT | DIFFERENT | dist=212 |
| colordisc | cd_near.img | SAME | SAME | dist=8 |
| colorconst | cc_same.img | SAME_SURFACE | SAME_SURFACE | dist=2 |
| colorconst | cc_diff.img | DIFFERENT | DIFFERENT | dist=347 |
| shapetrans | sh_circle.img | CIRCLE | CIRCLE | ratio=991 area=377 |
| shapetrans | sh_square.img | SQUARE | SQUARE | ratio=640 area=485 |
| shapetrans | sh_triangle.img | TRIANGLE | TRIANGLE | ratio=432 area=201 |
| pitchdisc | pd_same.pcm | SAME | SAME | fam=439999 fbm=439999 dppm=0 |
| pitchdisc | pd_higher.pcm | HIGHER | HIGHER | fam=439999 fbm=554003 dppm=259100 |
| pitchdisc | pd_lower.pcm | LOWER | LOWER | fam=439999 fbm=329994 dppm=250011 |
| timbredisc | tb_pure.pcm | PURE | PURE | f0m=439999 r=1000 nh=8 |
| timbredisc | tb_dark.pcm | DARK | DARK | f0m=440000 r=1137 nh=8 |
| timbredisc | tb_rich.pcm | RICH | RICH | f0m=440007 r=1779 nh=8 |
| timbredisc | tb_bright.pcm | BRIGHT | BRIGHT | f0m=440021 r=6351 nh=8 |
| motiondir | mv_e.vid | E | E | dx=12 dy=0 mag=12 |
| motiondir | mv_n.vid | N | N | dx=0 dy=-12 mag=12 |
| motiondir | mv_sw.vid | SW | SW | dx=-12 dy=12 mag=16 |
| motiondir | mv_still.vid | STILL | STILL | dx=0 dy=0 mag=0 |

**19/19 pass.** Timbre centroids match theory to the digit:
pure 1000 (exact), dark 1137 vs 1138 theory, rich 1779 vs 1779 theory,
bright 6351 vs 6351 theory. f0 within 0.021 Hz on all four timbres.

Error paths: unknown task → `error=bad_task`, exit 1; missing/unreadable
fixture → `error=read_failed`, exit 1. Contract keys `approach=A task=
judgment= confidence= debug_vec= ops=` present on every success; confidence
in 0..1000.

Representative ops: colordisc 2049, colorconst 2049, shapetrans 3075,
pitchdisc 3942949, timbredisc 2012442, motiondir 7170.

## Determinism (3 runs each, SHA-256 of stdout — h1=h2=h3 for all six)

| Task | Fixture | SHA-256 (all 3 runs identical) |
|---|---|---|
| colordisc | cd_diff.img | 64dc0714b5120572aaef705476f72a3662ac7e14583e2715c607df886a8a936f |
| colorconst | cc_same.img | 38691295bf118e6dc51a3c82c9209cdfacb419d1be13f9876d5311eb0cec27b9 |
| shapetrans | sh_square.img | 5eb9f7cd901558dca50398fa9b9d2b4375e7efcd500a899052d83feb6e62f14d |
| pitchdisc | pd_higher.pcm | 9d3ee52792baa3649e7ea6fb15bcc37785d61ee1256c747170d6de8cde3135ef |
| timbredisc | tb_rich.pcm | 2e878fda5bebebd42e52aad579a10eef7f2b6929ab442f6534a7ce7735f991b1 |
| motiondir | mv_sw.vid | 87792ed0c9e367971f52b022b07e928a6c66c4631227fed378c992fdb4212a40 |

Zero RNG anywhere; no wall-clock; no uninitialized reads. Rebuilds of the
binary from the same source are byte-identical (deterministic compiler).

## Known limitations / weak spots (honest)

1. **Timbre class boundaries are hand-fixed** (1075/1400/3000) and tuned
   against 4 synthetic timbres. The PURE/DARK boundary is inherently tight —
   a mellow tone with weak low harmonics is spectrally close to a sine.
   Real-harness timbres may need boundary evidence; this is the weakest task.
2. **f0 range is 50–2000 Hz** (autocorrelation lag range). Tones outside it
   → `task_failed`. Documented, not silent.
3. **Octave guard assumes harmonic tones with odd-harmonic energy.** Tones
   with only even harmonics keep the doubled f0 (genuine psychoacoustic
   ambiguity); inharmonic/percussive timbres are out of scope.
4. **colorconst white-patch degenerates on perfectly uniform halves** (each
   normalizes to ~(1000,1000,1000)); needs surface texture/highlight
   variation. Smoke fixtures include texture; dist=2 vs 347 shows headroom.
5. **Shape ratio assumes clean foreground/background brightness separation**
   (minority mask); camouflage/noise will break it. Rotated square/triangle
   pass (ratios 640/432 vs prototypes 637/414).
6. **Motion uses changed-region centroids**; symmetric leading/trailing edges
   or distractor motion can confuse direction. Still threshold 3 px.
7. **pitchdisc assumes the two tones share timbre** (same estimator both
   halves; complex timbres are handled by the robust estimator, but the
   2% threshold was validated on pure tones only).
8. Audio ops are ~2–4M per fixture (autocorrelation + fine-grid DFTs) —
   fine for a test harness, not for realtime.

## Deliverable tree contents (final)

- `sense.zag` — Approach A source
- `R33_NATIVE_IO_V1.zag` — native IO import (required to build)
- `sense` — compiled binary (88191 bytes)
- `BUILD_LOG.md` — this file
- `DONE` — completion marker
- No `.zagd`, `.zag-cache`, fixtures, or extra binaries in the tree.
  (Smoke apparatus lives in `/tmp/smoke/`, outside the deliverable.)
