# F1 AUTOPILOT — conscious-perception control fork

Pure-Zag representative perception pipeline. F1 is the **non-killable control**:
sensing runs automatically, deliberation receives percepts, the conscious gate
admits. This fork declares its sampling policy up front, states what evidence
that policy can destroy, and is measured honestly on the frozen 26-fixture
shared battery — including its home-turf losses.

## Control behavior

1. **Sensing (automatic).** Every fixture in the manifest is routed to a fixed
   perceptual pipeline with no deliberative choice: `.pcm` → pitch/timbre,
   `.img` → color discrimination/constancy, `.vid` → motion.
2. **Deliberation receives percepts.** Each pipeline emits one percept string
   plus a confidence (0–1000) and scalar details.
3. **Conscious gate admits.** F1 installs every routed percept (26/26 installed).
   The gate is trivially open by design — this is the control against which
   selective forks are measured.

## Declared sampling policy (frozen 2026-09-23)

| Task | Policy |
|---|---|
| PITCH | Halves A=[0:8192), B=[8192:16384); only the **first 2048 samples** of each half are examined. Frequency = interpolated zero-crossing estimate. `rel_ppm = \|fB−fA\|·10⁶/fA`. SAME iff rel_ppm < 20000, else HIGHER/LOWER. |
| TIMBRE | Only the **first 2048 samples**. `hp1000 = 1000·Σ\|x[i]−x[i−1]\|/Σ\|x\|`. PURE ≤67< DARK ≤82< RICH ≤110< BRIGHT (midpoints of calibrated 62/72/93/166). |
| COLORDISC | 64×64 image split into left/right 32×64 halves; mean RGB per half; integer Euclidean distance of the means. SAME iff dist < 40. |
| COLORCONST | White-patch illuminant = per-half max RGB; discounted channel = 255·mean/max. SAME_SURFACE iff max channel discounted difference < 8. |
| MOTION | **Frames 0 and 7 only** (6 of 8 discarded). Brightness-weighted global centroid (b>16), displacement in Q6 subpixels. STILL iff max(\|dx\|,\|dy\|) < 128, else 8-way by dominant axis. |
| ROUTER | `.pcm` n=16384→PITCH, n=8192→TIMBRE, else UNKNOWN; `.img` per-half variance→COLORDISC (flat) / COLORCONST (textured); `.vid`→MOTION. |

## Declared loss bounds (what the policy can destroy)

- **PITCH:** pitch events confined to samples [2048:8192) of either half are
  invisible (late-onset omission); sub-2% pitch differences destroyed by the
  20000 ppm gate.
- **TIMBRE:** timbre changes after sample 2048 are invisible; the hp1000 bands
  quantize the timbre continuum.
- **COLORDISC:** color differences < 40 units destroyed by the gate.
- **COLORCONST:** a single-pixel max-RGB spike corrupts the whole-panel
  illuminant estimate; discount-identical surfaces under different absolute
  levels collide after normalization.
- **MOTION:** small-target motion is invisible to the global centroid; the
  centroid follows the brightest mass (distractor capture).
- **ROUTER:** unsupported `.pcm` lengths install nothing.

## Build

Pinned toolchain only, no cache/daemon:

```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 f1.zag \
  --no-zagd --no-analyze --no-foreground-cache -o f1
```

`@import("substrate/R33_NATIVE_SHA256_V2.zag")` resolves relative to the build
cwd; the vendored SHA-256's own import was rewritten to
`@import("substrate/R33_NATIVE_IO_V1.zag")` for the same reason.

## Run

```
./f1 <manifest> <fixtures-root> <ledger-out>
```

- `<manifest>`: text file, one fixture path per line, paths relative to
  `<fixtures-root>`. This fork's manifest is `battery_all.txt` (26 frozen
  fixtures, `find test train -type f ! -name '*.truth' | sort` order).
- stdout: one machine-readable `RESULT` line per episode plus a final
  `SUMMARY` line. No timing data — canonical stdout is fully deterministic.
- `<ledger-out>`: hash-chained ledger (see below).

Full protocol (3 timed runs + byte-identity proof + aggregates):

```
./run_f1.sh            # writes results/stdout_run{1,2,3}.txt, results/ledger_run{1,2,3}.txt
python3 verify_ledger.py results/ledger_run1.txt
```

## Ledger

`GENESIS entry = sha256(0x00³² ‖ header-bytes)`; each episode appends
`EPISODE / STEP / PERCEPT` lines and a `CHAIN prev=<prev> entry=<entry>` line
with `entry = sha256(prev ‖ episode-body)`. The header binds the manifest
path+sha256 and the full POLICY/LOSS declarations above. Verified independently
by `verify_ledger.py` (recomputes every link from ledger bytes alone).

## Results (frozen battery, 26 fixtures)

- Installed percepts: **26/26** (gate open by design)
- Correct: **11** · Wrong: **15** · False-install rate: **15/26 = 57.6%**
- Total deterministic ops: **155,645** · mean **5,986 ops/episode**
- Wall time: **≈6.2 s per 26-episode run** (≈238 ms/episode; pure-Zag SHA-256
  of fixture/ledger bytes dominates, not the perceptual ops)
- Determinism: **6/6 runs byte-identical** stdout
  (`78de7cb3…0ca4`) and ledger (`48baf360…c7e`); chain head
  `cb31a9fe…4c5`, independently re-verified.

### The 15 misses, by declared loss mode (zero surprise misses)

- **Late-onset omission (6):** om_p1, om_p2, tr_om_p1, tr_om_p2 (pitch change
  in half B after the 2048-sample window); om_t1, tr_om_t1 (timbre turns
  BRIGHT after sample 2048).
- **White-patch corruption (2):** il_c1, tr_il_c1 — a single saturated-pixel
  spike corrupts the illuminant estimate; truth is SAME_SURFACE, F1 installs
  DIFFERENT at conf=1000.
- **Discount-identical collision (2):** il_c2, tr_il_c2 — different absolute
  levels, identical discounted means.
- **Distractor capture (3):** ib_m1, tr_ib_m1, tr_ib_m2 — big dim distractor
  dominates the global centroid; the small bright target's motion is lost.
- **Red-team boundary (2):** rt_c1 (dist=39, one unit under the gate),
  rt_p1 (rel_ppm=18181, under the 20000 gate).

### Honesty note

An earlier build of this binary miscompiled two color-constancy episodes
(`maxdisc=0` instead of 41) and scored a spurious 13/26. The independent
Python oracle (`gen/ref_f1.py`, integer-exact reference for the declared
algorithms) caught the divergence on re-check; the current binary matches the
oracle field-by-field (task, percept, conf, ops, detail) on all 26 fixtures.
The 11/26 figure above is the verified one.

## Files

- `f1.zag` — the pipeline (sources of truth)
- `substrate/` — vendored SHA-256 + IO substrate
- `gen/ref_f1.py` — integer-exact Python oracle for the declared algorithms
- `battery_all.txt` — run manifest (26 fixtures)
- `run_f1.sh` — 3-run timed protocol with determinism proof
- `verify_ledger.py` — independent ledger-chain verifier
- `results/` — stdout_run{1,2,3}.txt, ledger_run{1,2,3}.txt, run_log.txt,
  results.csv

## Limits

- 64×64 images and ≤16384-sample PCM only (router installs nothing otherwise).
- Integer arithmetic throughout; perceptual quality is deliberately crude —
  F1 is the control, not the champion.
