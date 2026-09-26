# Crash fix: `seg_fill_holes` stack overflow → clean refusal on degenerate inputs

Date: 2026-09-26. Applies to `video-fusion-step5` and `video-fusion-step6-neck`
(identical function in both trees). Pure Zag, zero RNG. No behavior change on
valid inputs (proven byte-identical below).

## 1. Root cause (red-team kill, commit `eed1281b1`)

`seg_fill_holes` (in `src/chunks/fz1.zag`) flood-fills the background through an
N-entry stack (`N = W*H`), but marked pixels `seen` only when POPPED. A pixel
could therefore be pushed up to 4x (once per neighbor) before its first pop.
On an empty (all-zero) 320x240 mask the stack depth reached 77,357 against
76,800 slots → `panic: slice index out of bounds`, process abort.

Any frame whose segmentation mask comes out empty hits this: uniform-gray
inputs, and frames where the dark subject covers ≥20% (the probe's dark
quintile threshold), because the dark-component mask ends up empty.

## 2. The fix

Mark `seen` **at push** — at all 8 push sites (4 border seeds + 4 neighbors) —
and remove the pop-side `seen`-check/`continue`. Each pixel then enters the
stack at most once, so the N-slot allocation provably cannot overflow
(`sp <= N` always).

Two subtleties found by testing (not by reasoning alone):

1. **Pop-side `continue` must go, not stay.** With mark-at-push the `continue`
   fires on every pop — including seed pixels that have not expanded yet —
   which starves the flood: on real frames the dark component vanished
   (`area=0`, `vr=-781`) while the buggy binary reported `area=6529`.
   The pop loop now expands unconditionally; with mark-at-push every pop is a
   fresh pixel by construction.
2. **Seed pushes need the `seen` guard too.** At corners (and whenever `H==1`
   or `W==1`) two seeds address the same pixel; pushing it twice overflows the
   stack on tiny masks (1x1: 2 pushes into a 1-slot stack → panic). The
   committed pure-Zag regression test caught this.

The flood's reachable set is unchanged: a pixel is visited iff it is a zero
connected to the border. Hole-filling semantics are identical.

## 3. Regression evidence

### 3a. Pure-Zag regression test (committed)

`tests/test_segfill.zag` + `tests/build_segfill_test.sh`. Assembles the REAL
`chunks/fz1.zag` (not a copy) with the real prelude and diffs `seg_fill_holes`
pixel-for-pixel against an independent sweep-to-fixpoint reference
implementation. 56 cases: 8 sizes (1x1, 2x2, 3x5, 8x8, 16x16, 32x24, 64x48,
320x240) x 7 patterns (empty mask, full mask, enclosed box hole, centered
blob, single interior zero, comb bars, ring maze). The empty-mask cases are the
original crasher (would panic before the fix).

Result: `cases=56, total_bad_px=0, SEG_FILL_REGRESSION_PASS`, exit 0.

### 3b. Uniform gray (320x240, 24 frames, gray 128) — end to end

Buggy binary: `panic: slice index out of bounds`, process rc=1.
Fixed binary `dumpanat`: `vr=-781` (no dark component — clean refusal), rc=0.
Fixed binary `fuse4`: `fuse4_rc=1` (refused: no valid head split), rc=0.
No panic on any path.

### 3c. Large dark subject (320x240, 24 frames, dark rectangle = 25% of frame)

Buggy binary: `panic: slice index out of bounds`, process rc=1.
Fixed binary `dumpanat`: `vr=-781`, rc=0. No panic.

### 3d. Empty mask

Covered by 3a (8 empty-mask sizes incl. 320x240, no panic, output all-zero =
unchanged, matching the reference).

## 4. Valid-input behavior is byte-identical

Fixed vs buggy binary on the real step-5 fixtures
(`video-composer/runs/ingest_pig_A` + `ingest_bunny_A`, the committed
`instr/merge.txt`):

| Check | Result |
|---|---|
| `dumpanat` pig frame 12 | `vr=1 snout=63,220 donor_c=103,140 area=6529` — identical in both binaries, and identical to the red-team's pre-fix evidence |
| Full `fuse4` battery, 24 frames | All 24 `frame_XX.ppm` byte-identical buggy vs fixed |
| `trace_fuse4.txt` buggy vs fixed | Byte-identical |
| `trace_fuse4.txt` fixed vs committed `evidence/trace_fuse4.txt` | Byte-identical |
| `fuse4` exit code on battery | `fuse4_rc=0` in both |
| Step-6-neck `dumpanat` pig frame 12, buggy vs fixed | Identical (`vr=1`, same geometry) |
| Step-6-neck `fuse4` on step-5 fixtures, buggy vs fixed | Identical (`fuse4_rc=-621` in both — the step-6 neck gate refuses these fixtures before fusion; same refusal both ways) |
| `selftest` | rc=0 in both fixed binaries |

The intermediate (broken) variant A is documented in §2 as a caution: the
first mark-at-push attempt kept the pop-side `continue` and broke real frames;
the differential test against the buggy binary caught it before commit.

## 5. Files changed

- `src/chunks/fz1.zag` — the fix (both trees; function byte-identical between them).
- `src/fusion4.zag` — reassembled from chunks with the fixed `fz1.zag` (both trees).
- `tests/test_segfill.zag`, `tests/build_segfill_test.sh` — new regression test (step-5 tree; tests the shared function).
- `evidence/CRASHFIX_SEGFILL_2026-09-26.md` — this file.

## 6. Refusal codes

- `vr=-781`: no dark component found (empty mask after segmentation) — the
  clean-refusal path for uniform-gray and large-dark inputs.
- `fuse4_rc=1`: battery refused, no valid head split on any frame.
- `fuse4_rc=-621` (step-6-neck only): neck-gate refusal on fixtures that lack
  the step-6 neck-anchor geometry; identical in buggy and fixed binaries.
