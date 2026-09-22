# BUILD_LOG.md — Approach B ("human-style") build record

All work 2026-09-21. Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Flags on every build: `--no-zagd --no-analyze --no-foreground-cache`.

## 1. Standalone percept compile (boundary proof)

```
znc check percept.zag --no-zagd --no-analyze --no-foreground-cache
→ znc: OK — all capability claims proven
```

`percept.zag` has no `@import`s, reads no fixtures, performs no
arithmetic on raw sensory values. Re-verified after all transducer
edits; the result is unchanged. A reviewer can delete the
transducer's numeric code and this file still compiles.

## 2. Full build

```
znc sense.zag --no-zagd --no-analyze --no-foreground-cache -o sense
→ znc: wrote native binary sense (94129 bytes main, 0 external tools)
```

Binary on disk: 101807 bytes, md5 `e6c98d091bbb0f90f54936b46bf849d8`.
Two consecutive rebuilds from identical sources are byte-identical
(same md5), so the build itself is deterministic.

Deliverables in `~/workspace/senses-rebuild/b_percept/`:
`transducer.zag`, `percept.zag`, `sense.zag`, `sense` (binary),
`PERCEPT_DESIGN.md`, `BUILD_LOG.md` (this file), `DONE`.
Nothing committed (per task instructions).

## 3. Smoke fixtures (temporary, since removed)

A Zag-only generator (`gen.zag`, kept OUTSIDE the deliverable dir)
wrote 18 deterministic fixtures: 4 color, 4 shape, 3 pitch,
4 timbre, 3 motion. Generator and fixtures deleted after testing
(see §7).

## 4. Smoke results (final binary, all exit 0)

| Task | Fixture | percept | percept2 | Judgment | Conf | ops |
|---|---|---|---|---|---|---:|
| colordisc | cd_same.img | 1005 | 1005 | SAME | 950 | 9217 |
| colordisc | cd_diff.img | 1005 | 1053 | DIFFERENT | 950 | 9217 |
| colorconst | cc_same.img | 1003 | 1003 | SAME_SURFACE | 950 | 15265 |
| colorconst | cc_diff.img | 1003 | 1047 | DIFFERENT | 950 | 15265 |
| shapetrans | sh_circle.img | 3000 | — | CIRCLE | 950 | 10363 |
| shapetrans | sh_triangle.img | 3001 | — | TRIANGLE | 700 | 10205 |
| shapetrans | sh_square.img | 3002 | — | SQUARE | 950 | 10275 |
| shapetrans | sh_square_rot.img | 3002 | — | SQUARE | 950 | 10283 |
| pitchdisc | pd_same.pcm | 4024 | 4024 | SAME | 950 | 8844001 |
| pitchdisc | pd_higher.pcm | 4024 | 4027 | HIGHER | 900 | 8844001 |
| pitchdisc | pd_lower.pcm | 4027 | 4024 | LOWER | 900 | 8844001 |
| timbredisc | tb_pure.pcm | 5000 | — | PURE | 750 | 4437999 |
| timbredisc | tb_bright.pcm | 5001 | — | BRIGHT | 950 | 4437999 |
| timbredisc | tb_dark.pcm | 5002 | — | DARK | 950 | 4437999 |
| timbredisc | tb_rich.pcm | 5003 | — | RICH | 950 | 4437999 |
| motiondir | mo_still.vid | 6000 | — | STILL | 900 | 20480 |
| motiondir | mo_e.vid | 6003 | — | E | 800 | 20480 |
| motiondir | mo_n.vid | mo_n: 6001 | — | N | 800 | 20480 |

18/18 correct, including rotation invariance (rotated square →
SQUARE) and the isosceles triangle (2/3 tuple vote → TRIANGLE,
conf 700 — honest degraded confidence, still correct).

Ops semantics: one per fixture element visit + one per
vocabulary/distance comparison. Spot checks: colordisc 9217 =
9216 pixel visits + 1; colorconst 15265 = 2×(4608 border-scan +
3024 inset-scan) + 1; timbredisc 4437999 = 4422000 autocorr +
15999 feature-loop + …; all consistent with the counting rule.

## 5. Determinism (byte-identical stdout × 3)

Five representative tasks (pitch, color, timbre, motion, shape)
run 3× each, outputs concatenated and hashed:

```
a47ee80b31decdee9a244e1018108fad267d175392518a0accb65f1798b60f8a  run1
a47ee80b31decdee9a244e1018108fad267d175392518a0accb65f1798b60f8a  run2
a47ee80b31decdee9a244e1018108fad267d175392518a0accb65f1798b60f8a  run3
```

3/3 byte-identical. Zero RNG anywhere in the build.

## 6. Error paths (all exit 1, one-line errors)

- no args → `error=no-task-arg`
- unknown task → `error=unknown-task`
- missing fixture → `error=open-fixture`
- truncated fixture → `error=short-pixels`

## 7. Bugs found and fixed during the build (honest record)

1. **pitchdisc direction inverted** (sense.zag): `pc_pitch_cmp(p1,p2)<0`
   means p2 is higher, but the code emitted LOWER. Fixed by swapping
   the HIGHER/LOWER arms. Caught by the pd_higher/pd_lower smoke pair.
2. **Autocorrelation peak-picking locked onto period multiples.**
   The "smallest lag within 99% of max" rule picked 2×/3× the true
   period for sawtooth/square (their jump discontinuities misalign by
   a fraction of a sample at the true period, scoring ~0.94, while a
   luckier-aligned multiple scored higher). Replaced with first
   prominent local maximum (≥50% of global max); 99%-rule kept as
   fallback. Pitch bins and timbre brightness now use the fundamental.
3. **Triangle "DARK" fixture was conceptually wrong, then the
   classifier.** A sine+sub-octave mix is NOT darker than a sine by
   f0-normalized brightness (a sine is the minimum). Rethought the
   4-way: sine→PURE, sawtooth→BRIGHT, square→RICH, triangle→DARK,
   adding FORM FACTOR (peak/mean|s|: sine 1571, triangle 2000) as the
   sine-vs-triangle cue. All four classify correctly with margins.
4. **znc miscompile in the fixture generator (NOT in the
   deliverable):** `(ic as i64)*512` compiled to `*1024` inside the
   large generator main (correct in a minimal probe), writing one
   full-scale spike per triangle period. Worked around with `*500` /
   peak 32000. Filed in `~/AGENTS.md` as candidate ZNC-2026-09-21-015.
   The deliverable's own sources were probed for the same pattern;
   the deliverable's arithmetic was verified correct by feature
   probes (sine≈(9,1416,1573), triangle≈(11,1733,2001) vs theory).
5. **`/tmp` was wiped mid-build** by the environment (512 MB tmpfs
   cleaner), taking the first generator and fixtures. Regenerated
   under `~/workspace/senses-rebuild/.genwork/`; removed afterwards.
6. **Ops anomaly (unresolved, documented):** one intermediate `sense`
   binary reported `ops=2049` for colordisc where the counting rule
   gives 9217. A clean rebuild from the then-current sources
   reported the correct 9217, and two further rebuilds are
   byte-identical to it. The counting code (`ops.* = ops.* + 1` per
   pixel visit) was verified correct by a standalone probe
   (4608/9216). No source change explains the 2049; treated as a
   one-off toolchain artifact, recorded here rather than hidden.

## 8. Unsupported paths

None. All six INTERFACE.md tasks are implemented and smoke-tested:
colordisc, colorconst, shapetrans, pitchdisc, timbredisc, motiondir.

## 9. Cleanup

Removed: `~/workspace/senses-rebuild/.genwork/` (generator +
fixtures), probe sources/binaries (`probe.zag`, `tprobe.zag`,
`oprobe.zag` + binaries), `.zag-cache/`, `.zagd.semantic-ready`,
`/tmp/det*.txt`, `/tmp/trunc.img`. Deliverable dir contains only
the six deliverables + `DONE`.

---

# REMATCH APPENDIX (2026-09-21, senses-rematch crew)

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
Flags: `--no-zagd --no-analyze --no-foreground-cache`.

## What changed vs round-1 sources (instrumentation ONLY)

Prereg amendment §"INSTRUMENTATION (B only, judgment path untouched)":

- `percept.zag`: `TimbreT` gains `crest, bright, form` (i64); `MotionT`
  gains `mcount, dx, dy` (i64). No decision code touched.
- `transducer.zag`: `td_timbre` stores its three per-mille features in
  the returned struct; `td_motion` accumulates total changed-pixel
  count (`mcount`) across frames and returns `(mcount, dx, dy)` on
  every path (including the STILL paths). Decision logic identical.
- `sense.zag`: `sn_timbredisc` emits `timbre_crest`, `timbre_bright`,
  `timbre_form` lines; `sn_motiondir` emits `motion_mcount`,
  `motion_dx`, `motion_dy` lines. All judgment/confidence/percept/ops
  lines unchanged.

`znc check percept.zag` still → "OK — all capability claims proven".

## Build

```
znc sense.zag --no-zagd --no-analyze --no-foreground-cache -o sense
→ znc: wrote native binary sense (95752 bytes main, 0 external tools)
```
md5 `7bf5598ecdac8dcdcc030cfeaeebd0f4`.

## VALIDATION GATE (passed, before any fitting)

`validate_gate.py`: instrumented binary vs original round-1 binary on
all 925 round-1 fixtures — every non-instrument key byte-identical:
**925/925 checked, 0 mismatches.** Instrument lines present on all
150 timbredisc and 150 motiondir fixtures.

## Relation-table verification (passed, before any fitting)

`verify_relations.py`: Python reimplementation of `pc_color_dist`,
pitch handles, shape prototypes/vote, timbre thresholds reproduces the
binary's judgments at hand-tuned values on all 925 round-1 fixtures:
**0 mismatches** (colordisc, colorconst, shapetrans, pitchdisc,
timbredisc). Motion at hand t=200 agrees on 141/150 — expected
divergence (CALIBRATION.md correction 1: the binary's actual still
rule is centroid-based, not mcount<200).
