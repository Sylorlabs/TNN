# JUDGE2_ROBUSTNESS_FIX.md — bands-arena overflow on dense-text images

Date: 2026-09-24. Binary: `build/v2/judge2` (rebuilt from fixed `judge2.zag`
with the pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`).

## Symptom

`judge2 judge` panicked with `panic: slice index out of bounds` (exit 1,
empty stdout) on exactly one image:
`~/workspace/code-ui/b2-bads/bad02_clutter_dashboard.img`
(1280x800 RGB, well-formed: 8 + 1280*800*3 = 3072008 bytes). All other
fixtures judged normally.

## Root cause

`compute_metrics` (judge2.zag) keeps per-text-band records in a `[]u8` arena:

```zag
let bands:[]u8 = nio_alloc(2560);   // <-- 2560 bytes
...
if(nb < 64) {                        // <-- guard allows 64 records
    t_put32(bands, nb * 64, btop as i64);   // <-- stride 64 bytes
    ...
}
```

Band records are stored at a **64-byte stride** (`nb * 64`, fields at
+0/+4/+8/+12/+16/+20/+24/+32), and the close-band guards allow **up to 64**
bands — but the arena held only **2560 / 64 = 40 records**. Any image whose
low-threshold (|dL|>12) band scan produces >= 40 text bands writes record 40
at offset 2560 == arena length -> out-of-bounds panic. The stale comment said
"band record (40 bytes)"; the record layout had since grown to a 64-byte
stride without the allocation being updated.

`bad02` is a dense clutter dashboard: the fixed binary reports `m_bands=51`
— the 41st band record (offset 2560) is exactly where the old binary died.
No other fixture in the dev/calibration sets reaches 40 bands, which is why
only this one image panicked.

Verified with a minimal Zag reproducer (`/tmp` scratch, not committed):
`nio_alloc(2560)` + `t_put32(b, 40*64, 1)` panics with the identical
`panic: slice index out of bounds`; the same write into a 4096-byte arena
succeeds.

## Fix (minimal, metric-preserving)

`judge2.zag` (`compute_metrics`, band-scan section):

```zag
let bands:[]u8 = nio_alloc(4096);   // 64 records x 64-byte stride
```

64 records matches the `nb < 64` guards' documented intent. The fix changes
nothing for any image with nb < 40 (the arena contents are identical), and
for nb in 40..63 it records the true band count instead of crashing.
Capping nb at 40 was rejected: it would silently truncate the measurement
(m_bands, gap_cv, hero_ratio, align_k, body_contrast all consume the band
table), whereas the density metric already saturates honestly at 1000 for
nb >= 18 via `dev_abs(mi==4)`. The metric still measures what it claims.

Also corrected the stale comment: "band record (40 bytes)" -> "(64 bytes)".

## Verification

- Rebuilt with the pinned toolchain from `build/v2/` (cwd, so the
  `@import("R33_NATIVE_IO_V1.zag")` resolves). `build/v2/judge2.zag` kept
  byte-identical to the workdir source.
- **Determinism:** 3x runs byte-identical (sha256) in both `metrics` and
  `judge` modes.
- **bad02 now judges:** `judgment=BAD score=536 confidence=160`
  `defects=DENSITY_CLUTTER` (`defect_sev_DENSITY_CLUTTER=1000`;
  `HIERARCHY_FLAT=388` below the 600 fire bar). Key metrics: `m_bands=51`
  (confirms the >= 40-band diagnosis), `m_body_contrast=4157` (>= 3000 bar,
  readable), `m_contrast=2480`, `best_ref=vercel1`, `ops=3112800`.
- **Regression sweep (old vs new binary):** all 24 dev fixtures
  (`calibration/fixtures/*.img` x14 + `calibration/html_fixtures/*.img` x10)
  x 2 modes (`metrics`, `judge`) = 48 outputs **byte-identical** old vs new;
  the only 2 differences are bad02 (`metrics` and `judge`), which panicked
  pre-fix. No score, defect, or metric changed on any other fixture.
- **Calibration still 14/14:** full `driver2.py` rerun over the 14-fixture
  set (both representations, frozen sense binaries) reproduces
  `calibration/after_v2.tsv` exactly — verdicts, scores, defects,
  confidence all identical; bad_* -> BAD (10/10), good_* -> GOOD (4/4).

## Lesson for the codebase

When an arena's record stride and its record-count guard are defined in
different places, the allocation must be audited against both. A cheap
static check: every `nio_alloc(N)` feeding indexed writes should carry a
comment naming the record size x max records, and the guard constant should
appear once. (Related znc lesson already in AGENTS.md: slices > 2^25 bytes
panic on any index — not the cause here, but the same "know your arena
bounds" discipline.)
