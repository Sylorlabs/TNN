# Upscale Concept Probe — DESIGN.md

## 1. Why this probe exists

On 2026-09-26 Micah observed the TNN upscale line "drew some weird pixely
lines" instead of upscaling, and ordered: **verify TNN knows what upscaling
IS before more code is written.** The existing `azupscale.zag` pipeline used
crew-designed construction operators (a 50/50 nearest/bilinear SHAPES blend;
a LINES operator that doubles endpoints and re-rasterizes Bresenham chords —
the source of the pixely lines). TNN deliberated over which operators to use
and when to commit/revert, but it never constructed or selected any
construction operator itself. The pipeline therefore demonstrated
*operator selection*, not *upscaling understanding*.

This probe tests the concept behaviorally, through TNN's own intake, before
any real-photo work continues.

## 2. What "knowing what upscaling is" means here (C1–C4)

- **C1 — Resolution change.** Construct a 192×192 image from a 96×96 input
  (true 2× geometry, not a redraw at the same scale).
- **C2 — Observation anchoring.** Even positions of the construction are the
  observed low-res pixels, bit-exact (zero mismatches). The probe enforces
  this by protocol and verifies it independently; it is not claimed as
  learned.
- **C3 — Measured coarse→fine knowledge.**
  - C3a: TNN commits ≥1 upscale atom from paired low/high examples,
    gated by the standing commit bar (G ≥ 9·N, measured gain per value).
  - C3b: On held-out examples, ≥90% of edge *detail* pixels (edge-region
    pixels whose true 2×2 differs from flat replication, measured from the
    held high-res during scoring only) are constructed from committed atoms.
  - C3c: Held-out odd-pixel SSE ≤ 75% of pure bilinear on edge regions, and
    ≤ 95% of pure bilinear overall.
  - C3d: Zero INVENTED pixels (every constructed pixel is KNOWN,
    CONSTRUCTED-ATOM, or honestly labeled CONSTRUCTED-GENERIC).
- **C4 — No drawing.** Construction uses only: atom-stamp (measured
  coarse→fine deltas), replication, bilinear. No Bresenham, no
  re-rasterization, no doubled endpoints. Verified by static audit of the
  construction loop (crew audit, documented here — not a TNN decision).

## 3. Protocol

Synthetic paired fixtures (the "world"), generated in-fixture:

**Teach** (96×96 low / 192×192 high, six texture classes):
FLAT 110 · GRAD-H 40→220 · GRAD-V 40→220 · CHECKER 4×4 (8×8 high) 60/200 ·
EDGE-D1 diagonal (qx+qy<32) 60/200 · EDGE-D2 diagonal (qx<qy) 60/200.

**Test** (held out — permuted layout, shifted edges, phase-flipped checker,
new gradient ranges): EDGE-D1 at qx+qy<40 · CHECKER phase-flip · GRAD-H
60→200 · EDGE-D2 at qx−qy<8 · FLAT 170 · GRAD-V 60→200.

TNN's measurement primitive: for each low-res pixel, a 3×3 context
signature = (gradient-magnitude class × ternary 3×3 contrast pattern).
For each signature observed in the teach pair, TNN measures the four
sub-pixel coarse→fine deltas (true 2× sampling, NOT replication — the
diagonals are doubled in position so replication staircases) and commits
the atom only if it beats both generic replication and generic bilinear
by G ≥ 9·N. The held high-res is used ONLY in scoring, never construction.

**BEFORE mode:** vocabulary empty → default generic (bilinear).
**AFTER mode:** committed atoms where they exist; teach-selected generic
(replication or bilinear, per-signature winner) elsewhere.

## 4. Signature design (and two instructive failures)

The signature must give different atoms to pixels whose true sub-pixel
patterns differ. Two coarser designs failed honestly at the commit bar:

1. Orientation bins (8 gradient-orientation bins) mushed D1/D2 diagonal
   straddlers with axis-aligned boundary pixels → atoms averaged to
   ~[0,0,0,±70] instead of [0,0,0,±140].
2. Axis-vs-diagonal contrast dominance still collided D1 straddlers with
   D2 shoulders (both "axis-dominant").

The working signature is the **ternary 3×3 contrast pattern**: each of the
8 neighbors quantized to −1/0/+1 by sign of (n−c) when |n−c|>30 (crew-chosen
measurement quantization; the atom VALUES under each pattern are measured,
never crew-supplied). sig = class·6561 + pattern (26,244 signatures).
This gave exact atoms: D1 straddler [0,0,0,140] (n=30), D2 straddler
[0,0,−140,0] (n=30).

## 5. Results

| | BEFORE (no teaching) | AFTER (taught) |
|---|---|---|
| C1 | PASS | PASS |
| C2 | PASS (0/9216) | PASS (0/9216) |
| C3a | FAIL (0 atoms) | PASS (6 atoms) |
| C3b | FAIL (0/48) | PASS (47/48 = 97.9%) |
| C3c edge | FAIL (1000/1000) | PASS (23/1000 = 2.3%) |
| C3c overall | FAIL (1000/1000) | PASS (4/1000 = 0.4%) |
| C3d | PASS | PASS |
| C4 | PASS (audit) | PASS (audit) |
| **VERDICT** | **CONCEPT NOT HELD** | **CONCEPT HELD** |

Byte-identical reruns ×2 verified (SHA-256 over all traces, atoms.bin,
BMPs, reports).

## 6. Epistemic labels

- `[CREW]` — protocol framing, fixture design, bar definitions, C4 audit.
  Crew-authored, predicate-guarded, never presented as TNN's reasoning.
- `[MEASURED]` — numbers computed by TNN's measurement from the fixtures
  (signature counts, SSE values, gains, atom deltas).
- `[DECISION]` — bar-gated commits and the pre-registered verdict. The bars
  are crew-set; the PASS/FAIL outcomes are computed from measurements.

Per-pixel output labels: 0=KNOWN (even positions, observed), 1=CONSTRUCTED-
ATOM (built from a committed measured atom), 2=CONSTRUCTED-GENERIC (honest
fallback: teach-selected replication/bilinear), 3=INVENTED (none occurred).

## 7. What this does and does not establish

ESTABLISHES: TNN can acquire, commit, and apply coarse→fine upscaling
knowledge from paired examples through its own intake, beating generic
interpolation on held-out examples of the same texture classes, with no
drawing operators.

DOES NOT ESTABLISH: real-photo upscaling (synthetic textures only);
cross-domain transfer (teach on synthetic → test on photos untested);
that the atoms are optimal (6 committed; 4 are single-observation corner
patterns). Phase 3 (real-photo path) must re-run this protocol on photo
data before any photo claim.
