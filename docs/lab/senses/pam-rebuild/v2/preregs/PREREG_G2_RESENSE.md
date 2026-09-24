# PREREG — Hypothesis G2: Judgment-Blind Deliberate Re-Sense

**Status:** FROZEN — committed alone before any G2 code or formal run.
**Date frozen:** 2026-09-24
**Hypothesis:** A second sense organ that reads the SAME raw evidence through a
DIFFERENT mechanism — never the first organ's judgment, confidence, margin, or
any derived verdict — provides genuine independent corroboration. An install is
legitimate only if the second organ, reading attended raw bytes through its own
mechanism, emits the same label the first organ did.

**Install rule (frozen):** A candidate installs iff the second organ emits the
same label string as the first organ's logged judgment, where the second organ
reads ONLY the frozen attended neighborhoods of the raw F payload (plus the
8-byte fixture header for sample/pixel geometry). Two full-frame PASSes with no
second-organ confirmation = no install. Label equality is exact string equality.

**Order from Micah:** "no more debate — the tests decide." Five parts, run in
order. If any part kills G2, write the KILL verdict with the numbers, commit
source + evidence + verdict, report, and STOP. No rescue missions.

---

## 0. Reconnaissance disclosure (pre-prereg activity)

Before freezing this prereg, the following reconnaissance was performed. No G2
code was written and no formal G2 run was executed.

1. Counted `DISP=ACCEPT_INSTALL` rows in
   `v2/redteam/evidence/ledger_d_withhold.txt`: **43**.
2. Categorized by comparing the ledger's judgment field to its truth field
   (positional fields 8 and 13; an earlier named-field reading was wrong and is
   discarded — the ledger is positional, verified 2026-09-24):
   **9 false, 34 true**, exactly as the task stated.
   - False (judgment vs truth): 8× TMB-5 `RICH` vs `DARK`; 1× COL-4
     `DIFFERENT` vs `SAME`.
   - True: 12× COL-4 `DIFFERENT`, 16× PTC `HIGHER`/`LOWER`, 6× TMB-5 `BRIGHT`.
3. Inspected the frozen first organ (`v2/forks/V2-D/src/vsense.zag`), the V2-D
   gate (`vgate_d.zag`), the ceiling test, the trial generator
   (`v2/redteam/src/rt_trials.zag`), and the R2-4 sweep/fixtures.
4. Discovered the task's stated fixture path (`redteam/fixtures/sealed/rt4_*`)
   is wrong: sealed/ holds only the original `rt3_*` payloads. The `rt4_*`
   dual-span trials are deterministically regenerable from sealed `rt3_*` via
   `v2/redteam/src/rt_trials.zag`; existing verification records the regenerated
   `TRIALS.sha256` as
   `319f45e3aaf0f5d38569974b9b027770ac6344bcaa618fd835fdd7737dea6cb0`
   (byte-identical across independent regenerations).
5. Read V2-D baseline metrics (`v2/forks/V2-D/evidence/metrics.json`):
   RK-3 = 88.48%, ACCEPT_INSTALL = 934, false installs = 7/11,840.
6. Read the full RK-3 case record (`v2/diagnostics/case_r24_rk3.txt`, 11,840 rows)
   and the R2-4 sweep (`round2/forks/R2-4/evidence/clean/sweep.jsonl`:
   10,915 r2a + 925 harness).

The headline 43/9/34 counts and the Part 1 subset below were known before
freezing. The five kill bars below are the task's bars, frozen verbatim in
meaning; all mechanism/procedure detail needed to run them is frozen here.

---

## 1. The frozen 43

Source: `v2/redteam/evidence/ledger_d_withhold.txt`, lines containing
`DISP=ACCEPT_INSTALL` (positional: field5=fixture, field8=judgment,
field9=conf, field13=truth). Exactly 43 lines. Frozen 2026-09-24.

### 1a. The 9 FALSE installs (judgment != truth)

| # | fixture | judgment | truth | conf |
|---|---------|----------|-------|------|
| 1 | rt4_COL-4_0000.r24 | DIFFERENT | SAME | 763 |
| 2 | rt4_TMB-5_0000.r24 | RICH | DARK | 788 |
| 3 | rt4_TMB-5_0006.r24 | RICH | DARK | 764 |
| 4 | rt4_TMB-5_0008.r24 | RICH | DARK | 819 |
| 5 | rt4_TMB-5_0011.r24 | RICH | DARK | 806 |
| 6 | rt4_TMB-5_0013.r24 | RICH | DARK | 806 |
| 7 | rt4_TMB-5_0014.r24 | RICH | DARK | 774 |
| 8 | rt4_TMB-5_0016.r24 | RICH | DARK | 832 |
| 9 | rt4_TMB-5_0021.r24 | RICH | DARK | 799 |

### 1b. The 34 TRUE installs (judgment == truth)

COL-4 DIFFERENT (12): rt4_COL-4_0001, _0002, _0004, _0007, _0009, _0012, _0014,
_0015, _0017, _0019, _0020, _0022.
PTC-4 (4): rt4_PTC-4_0000 HIGHER, _0012 HIGHER, _0013 LOWER, _0020 HIGHER.
PTC-5 (12): _0001 HIGHER, _0002 LOWER, _0005 LOWER, _0006 HIGHER, _0009 HIGHER,
_0011 HIGHER, _0012 LOWER, _0013 HIGHER, _0014 HIGHER, _0017 LOWER, _0021 HIGHER,
_0023 LOWER.
TMB-5 BRIGHT (6): rt4_TMB-5_0004, _0005, _0007, _0012, _0015, _0017.

### 1c. Part 1 subset (frozen)

The six TMB-5 falses with the lowest fixture index (the task's "lowest seq";
fixture generation order is the trial order):
**rt4_TMB-5_0000, rt4_TMB-5_0006, rt4_TMB-5_0008, rt4_TMB-5_0011,
rt4_TMB-5_0013, rt4_TMB-5_0014.**
All are logged `RICH` (truth `DARK`). Part 1 asks: does the second organ,
reading only its attended neighborhoods, also emit `RICH`?

---

## 2. Architecture (frozen)

### 2a. First organ (frozen, vendored — not re-derived)

`organ1.zag` = `v2/forks/V2-D/src/vsense.zag` minus `main`, plus the shared
substrate files it imports (`R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag`,
`lut.zag`, `gcheck.zag`) copied verbatim. The six task functions
(`task_colordisc`, `task_colorconst`, `task_shapetrans`, `task_timbredisc`,
`task_pitchdisc`, `task_motiondir`), the LUT builders, and the byte-access
helpers are vendored UNCHANGED (verified by diff against the V2-D source at
build time; the diff must be empty apart from the removed `main`).

The first organ is deliberately NOT re-run to produce judgments for Parts 1–4:
the logged ledger judgments are the frozen first-organ outputs. The vendored
organ 1 is used ONLY for:
- (i) Part 4: re-judging PERTURBED F bytes (to test whether organ 1's judgment
  holds the perturbation fixed);
- (ii) Part 5: G-as-F re-sensing to recompute (jG, confG) for the V2-D detector
  replay (the V2-D evidence does not persist per-trial (jG, confG)).
Build verification (not a battery part): the vendored organ 1 must reproduce
the 43 logged judgments on unperturbed F spans byte-for-byte (label and conf).
If it does not, the vendoring is wrong and work stops until it is fixed.

### 2b. Attention map (frozen)

Pure function of the raw F payload length N (samples for audio, pixels for
image/video). NEVER of any judgment, confidence, margin, task outcome, or
program verdict. Exactly 64 offsets:

- If N >= 64: `off[k] = ((2*k+1) * N) / 128` for k = 0..63 (uniformly spaced
  segment midpoints; integer division). Depends only on N.
- If N < 64: offsets are 0..N-1 (all bytes). (Does not occur for our fixtures;
  N = 16000 audio, 16384 image, 4096 video.)

Frozen neighborhoods (the "attended span" = union of the 64 neighborhoods):
- Audio (tcode 3,4): samples `[off-48, off+48]` clamped to `[0, cnt)`
  (97-sample window; 64×97 = 6208/16000 ≈ 39%; windows do not overlap).
- Image (tcode 0,1,2): 5×5 pixel patch centered at `(off%w, off/w)`, clamped to
  `[0,w)×[0,h)` (64×25 = 1600/16384 ≈ 10%; no overlap).
- Video (tcode 5): 5×5 patch (same as image) read in frames 0 and 3
  (the fixture's motion interval).

The second organ reads ONLY these neighborhoods plus the 8-byte fixture header
(needed for sample/pixel geometry: sr/cnt or w/h). It never scans the full
payload. The map is stable under outside-edits by construction (it depends only
on N, which edits preserve).

### 2c. Second organ (frozen design; thresholds via frozen calibration)

A generic local byte-texture classifier, deliberately architecturally distant
from the first organ. It uses NONE of: autocorrelation, harmonic-grid pitch,
harmonic spectral centroid, CIELAB, shape prototypes (area/perimeter/circularity
moments), or 1-D projection motion profiles. Per task:

- **timbredisc**: For each attended 97-sample window, Goertzel energies at fixed
  octave bands 250/500/1000/2000/4000/8000 Hz (NOT f0-relative). Feature
  `r = 1000*(E4000+E8000)/sum(E)`. Label = median `r` over the 64 windows vs
  frozen boundaries B1<B2<B3: PURE / DARK / RICH / BRIGHT. (No f0 estimation;
  no autocorrelation; no harmonic anything.)
- **pitchdisc**: Dual-tone layout from header (`tone = cnt*10/22`,
  `gap = cnt-2*tone`; this is fixture geometry, also used by organ 1's harness).
  For each attended window, rising-zero-crossing f0 (NOT autocorrelation, NOT
  harmonic grid). `fA` = median f0 over windows with `off < tone`;
  `fB` = median f0 over windows with `off >= tone+gap`. If either has no valid
  estimate: `SAME`. Else `d = |fB-fA|*1000000/max(fA,fB)` (relative difference
  in per-million): HIGHER if fB>fA and d>=5000, LOWER if fA>fB and d>=5000,
  else SAME. (The 5000 = 0.5% is a FIXED a priori constant, not learned.)
- **colordisc**: For each attended 5×5 patch, mean RGB. Accumulate patch means
  into left (`x<64`) / right (`x>=64`) halves (w=128). `dist = isqrt(dr²+dg²+db²)`
  on the half-means. DIFFERENT iff `dist >= T_col` (frozen calibrated
  threshold), else SAME. (RGB means, NOT CIELAB.)
- **colorconst**: Same patches; per-half RGB means → per-mille chromaticity
  `(r,g,b)*1000/(r+g+b)` (sum=0 → (0,0,0)). `dist` = isqrt of squared
  chromaticity difference. DIFFERENT iff `dist >= T_cc`, else SAME_SURFACE.
- **shapetrans**: For each attended 5×5 patch, foreground = pixels with
  `r+g+b > 400`; bounding box + count over all 64 patches.
  `fill = 1000*count/bbox_area` (count=0 → label CIRCLE, documented fallback).
  Nearest of frozen prototypes {CIRCLE:785, SQUARE:1000, TRIANGLE:500} by |.|;
  ties → CIRCLE < SQUARE < TRIANGLE. (Fill-ratio, NOT organ 1's moments.)
- **motiondir**: For each attended pixel, 5×5 patch in frame 0 vs frame 3;
  2-D SSD over shifts dx,dy ∈ [-8,8] (NOT 1-D projection profiles); pick min SSD
  (ties → smallest |dx|+|dy|, then smallest dx, then dy). Median (dx,dy) over
  64. STILL iff |dx|<=1 and |dy|<=1, else 8-direction by angle using organ 1's
  label codec (0=STILL,1=N,2=NE,3=E,4=SE,5=S,6=SW,7=W,8=NW).

Label strings are EXACTLY organ 1's (`jstr`): pitchdisc HIGHER/LOWER/SAME;
timbredisc PURE/DARK/RICH/BRIGHT; colordisc SAME/DIFFERENT;
colorconst SAME_SURFACE/DIFFERENT; shapetrans CIRCLE/SQUARE/TRIANGLE; motiondir
STILL/N/NE/E/SE/S/SW/W/NW.

### 2d. Separate training (frozen procedure — the ONLY data-derived step)

Boundaries B1/B2/B3 (timbre), T_col, T_cc are learned in pure Zag by
`calibrate.zag`, which @imports organ 2's feature functions (NOT its label
functions, NOT organ 1, NOT the gate):

- Training set: ALL r2a fixtures of the task present on disk with a readable
  `.r24.truth` sidecar (`round2/forks/R2-4/fixtures/r2a_<task>_*.r24`), reading
  ONLY (seq/task/fixture/truth). NEVER first-organ judgment, confidence,
  margin, program verdict, or agreement. (Sweep r2a counts: timbredisc 1410,
  colordisc 2230, colorconst 1400. The driver uses the on-disk intersection and
  logs the exact N used.)
- Features: organ 2's exact feature (`r` / `dist`) on each fixture's F span
  (extracted from the dual-span .r24 via the length prefix).
- timbredisc: coarse-to-fine exhaustive grid search maximizing train accuracy;
  coarse step 20 over [0,1000], refine ±20 at step 2 around the best; ties →
  lexicographically smallest (B1,B2,B3).
- colordisc / colorconst: exhaustive single threshold over sorted unique
  feature values maximizing train accuracy; ties → smallest threshold.
- The resulting boundaries are PRINTED by the calibration run, recorded in the
  evidence log, and passed as ARGV to the battery/replay drivers (organ2.zag
  takes boundaries as parameters — no post-calibration source edit).
- pitchdisc/shapetrans/motiondir have NO learned parameters (fixed 0.5%,
  fixed prototypes, fixed mapping — documented above).

The calibration run is deterministic (pure Zag, zero RNG) and is itself run 3×
with SHA comparison; its printed boundaries must be byte-identical.

---

## 3. The five parts (frozen procedures and kill bars)

Deterministic trial bytes: the 43 `rt4_*.r24` files do not exist on disk under
`redteam/fixtures/sealed/` (only the original `rt3_*` sealed payloads are
there). Before ANY battery run, regenerate the full rt4 trial tree with the
frozen generator `v2/redteam/src/rt_trials.zag` from sealed `rt3_*` into a
scratch dir (NOT committed), and verify the regenerated `TRIALS.sha256`
byte-identical against the frozen manifest
`v2/redteam/evidence/TRIALS.sha256`
(digest `319f45e3aaf0f5d38569974b9b027770ac6344bcaa618fd835fdd7737dea6cb0`).
If the digest mismatches, STOP and report — the battery cannot run on wrong
bytes. The 43 battery trials are the regenerated files named in §1; F spans are
extracted via the .r24 length prefix (`r24_flen`).

All parts: pure Zag, zero RNG, each part run 3× with byte-identical SHA-256
comparison of the full evidence output. Pinned compiler:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Run order is sequential; the FIRST kill ends the arm (write VERDICT_G2.md with
the numbers, commit source+evidence+verdict, report, stop).

Notation: for trial i, `J1[i]` = frozen ledger judgment (§1), `T[i]` = truth,
`O2(F)` = second-organ label on (possibly edited) F bytes with the frozen map.

### Part 1 — wrong-kill (does the second organ corroborate known falses?)

- Trials: the six of §1c. For each: `o = O2(F)`. Wrong-corroboration iff
  `o == J1[i]` (i.e. organ 2 also emits `RICH` on its attended read).
- **KILL BAR: kill iff ≥2/6 wrong-corroborations.** Report k/6 and the SHAs.

### Part 2 — span-edit (is the second organ's read independent of the outside?)

Trials: all 9 falses of §1a. Deterministic byte-noise (frozen):
`noisebyte(pos,seq,salt) = ((pos*1103515245 + seq*40503 + salt*987643211 + 12345) mod 2^64) mod 256`
(u64 arithmetic; `seq` = fixture index, e.g. 0 for rt4_TMB-5_0000).

- **Edit A (outside edit):** preserve the 8-byte fixture header and every byte
  in the attended union; replace every other F-payload byte with
  `noisebyte(pos,seq,1)`. (For audio the noise is per byte of the i16 stream —
  full-scale white noise; for image per channel byte.)
- **Edit B (reverse edit):** preserve the header and every byte OUTSIDE the
  attended union; replace every attended byte with `noisebyte(pos,seq,2)`.
- For each edited trial: `o = O2(F_edited)`. False-install-preserved iff
  `o == J1[i]`.
- **KILL BAR: kill iff Edit-A false-install-preserved rate > 2/9** (i.e. ≥3/9).
  Edit B is a manipulation check and is REPORTED (destroyed = `o != J1[i]`);
  if Edit B preserves ≥3/9, the organ is not reading its input — report as a
  mechanism failure alongside (it does not need its own bar; it invalidates
  any Part 2 pass).

### Part 3 — correct-retention (does the second organ confirm true installs?)

- Trials: the 34 of §1b, UNEDITED F. `o = O2(F)`. Retained iff `o == J1[i]`.
- **KILL BAR: kill iff retention < 26/34.** Report k/34 and per-task
  retention (COL/PTC/TMB).

### Part 4 — judgment-blindness (does organ 2 move when bytes move, judgment fixed?)

Trials: all 9 falses of §1a. Frozen perturbation levels applied to the
ATTENDED union only (outside bytes and header preserved). `seq` = fixture index.

- **Level A (deterministic ±32):**
  `delta(pos,seq) = ((pos*7919 + seq*104729 + 7) mod 65) - 32` ∈ [-32,32];
  audio: `s = clamp(s+delta,-32768,32767)` per sample; image: per channel byte
  `clamp(c+delta,0,255)`.
- **Level B (donor replacement):** copy donor F bytes over the attended union
  at identical byte ranges. Donors (frozen, opposite-truth, size-matched):
  TMB truth DARK (8 falses) → donor rt4_TMB-5_0004.r24 F (truth BRIGHT);
  COL truth SAME (rt4_COL-4_0000) → donor = sealed `rt3_COL-4_0000.img` bytes
  (truth DIFFERENT; verified 24584 bytes, same geometry).
- **Level B-half:** Level B applied to the 32 attended neighborhoods with the
  LARGEST offsets only (deterministic subset).
- **Level C (constant):** audio: attended samples = 0; image: attended pixels =
  (128,128,128).
- Baseline `b[i] = O2(F)` (unedited). For each level L: FIRST run the vendored
  organ 1 on the perturbed F; let `j1 = ` its judgment. If `j1 != J1[i]`,
  level L is DISCARDED for trial i (judgment not held fixed — the probe is
  vacuous there). Otherwise `o = O2(F_perturbed)`; record whether `o == b[i]`.
- **KILL BAR: kill iff ∃ trial i with (held ∩ {B,B-half,C} ≠ ∅) such that
  `o == b[i]` on EVERY held level** — i.e. the second organ's output is
  invariant across all strong byte changes while organ 1's judgment is fixed.
  (Level A is weak by design and is reported but cannot trigger the bar alone;
  it is included to characterize sensitivity.)
- Report per trial: baseline, per-level (discarded / moved / invariant).

### Part 5 — RK-3 no-regression (does gating V2-D installs on the second organ hold the line?)

- **Baseline (frozen):** V2-D metrics: RK-3 = **88.48%** (975/1102 HC installed
  correct), ACCEPT_INSTALL = 934, false installs = 7/11,840.
- **Replay driver** (`g2_replay.zag`, pure Zag): replays the FULL 11,840-trial
  RK-3 case record with the V2-D gate logic vendored verbatim (operating on
  judgment STRINGS — equality-preserving vs the original jcodes) in two modes:
  (a) baseline mode (G2 disabled) — must reproduce RK-3 = 88.48% within ±0.05pp
  and ACCEPT_INSTALL = 934 ±2, else the replay is unfaithful and work stops;
  (b) G2 mode — every V2-D ACCEPT_INSTALL candidate additionally requires
  `O2(G-as-F attended read) == jG` (the recomputed G-span judgment); H2-path
  (non-detector) installs are unchanged.
  - Case input: a TSV derived from `v2/diagnostics/case_r24_rk3.txt` +
    `round2/forks/R2-4/evidence/clean/sweep.jsonl` (derivation script + input SHA
    committed; columns: seq, tcode, fixture, judgment, conf, prog, pred,
    measure, truth, src). Harness-src trials have no G span and are never
    detector candidates (as in V2-D).
  - G-as-F: the vendored organ 1 judges the G-span bytes exactly as the V2-D
    detector did (same task fn, same `(buf,n,ob,pos,op,empty_gbuf,0)` call
    shape); (jG, confG) are re-derived, NOT read from any record.
- Metric: RK-3_G2 = (HC trials installed correct under G2 mode) / 1102,
  where HC trials are the frozen 1,102 high-confidence trials of the case
  record and "installed" uses the G2 install rule (§2 head).
- **KILL BAR: kill iff RK-3_G2 < 85.48%** (more than 3.0pp below 88.48%).
  Report RK-3_G2, the delta, per-task install deltas, and run SHAs.

---

## 4. Determinism and build rules (frozen)

- Pure Zag for the second organ, attention map, calibration, and all five
  battery/replay drivers. **Zero RNG** anywhere (no `rand`, no time/addr seeds).
- Each part (and calibration) run **3×**; the full stdout+evidence bytes of the
  three runs are SHA-256-compared and must be **byte-identical**. Any
  divergence is a build defect: stop, root-cause, fix, re-run 3×.
- Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Known znc hazards respected: no indexed `as []i32`/`as []u32`/`as []u16`
  (use []u8 arenas + explicit little-endian accessors); no slice > 2^25 bytes;
  `.*` only on actual pointers; `@import` paths relative to build cwd;
  no `};`; no bare `{}` blocks; no identifier named `try`/`zalloc`.
- Commit via `~/workspace/commit_racefree.py` (message files under
  `~/workspace/tmp_commit/`, never /tmp). This prereg is committed ALONE,
  before any G2 source or evidence. Never commit binaries, `.zagd`, or
  `.zag-cache`; trial scratch bytes are never committed.

## 5. File layout

```
v2/g2_resense/
  src/            organ1.zag (+ verbatim substrate), organ2.zag, attn folded in,
                  calibrate.zag, g2_battery.zag (parts 1-4), g2_replay.zag (part 5)
  evidence/       calibration log+boundaries, per-part run logs, SHAs,
                  VERDICT_G2.md
  scratch/        regenerated rt4 trials (NOT committed)
v2/preregs/PREREG_G2_RESENSE.md   (this file)
```

## 6. Residual risks (stated honestly)

- Shared error may live in the RAW BYTES (both organs read the same physics).
  Part 4 tests judgment-side smuggling (organ 2 ignoring bytes), NOT byte-side
  correlation. If all five parts pass, the remaining risk — both organs fooled
  by the same bytes — belongs to the senses rebuild, not to G2.
- The second organ is deliberately WEAKER than the first (sparse attended read,
  simpler features). Part 3 guards against a degenerate organ, but a weak
  organ that passes Part 3 on easy trues could still add little in Part 5.
- Calibration uses r2a programs (TMB-1..4, COL-1..3) while the battery uses
  rt4 programs (TMB-5, COL-4, PTC-4/5); transfer is assumed and is tested by
  Parts 1–3 themselves.
- Part 5's replay re-derives (jG, confG); if baseline mode does not reproduce
  88.48% ± 0.05pp, the replay — not G2 — is at fault, and Part 5 cannot run.

---

**Frozen by:** G2 arm (subagent), 2026-09-24. Awaiting commit-alone, then build.
