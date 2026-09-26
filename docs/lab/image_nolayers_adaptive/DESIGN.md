# DESIGN.md — NO-LAYERS ADAPTIVE-SPLIT fork

Date: 2026-09-26. Order: Micah ~09:54 PDT: "yes I want the rigid grid
gone for no layers, for a real result."

Parent fork: `~/workspace/image_nolayers/` (commit
3a49b9c7031c51e81ab723c4dfbca14f246fe579 on tnn-native-lab):
29.27 dB / 0.9260 pre-residual, rigid nested dyadic grid (64→32→16→8→4).

## The question this fork answers

The rigid fork's own white-box analysis named the grid as the gap's
mechanical cause: a building edge at an arbitrary grid offset can only
match an exemplar whose edge sits at the same offset, so atoms mismatch
at content boundaries that don't align to the grid (mean abs error
identical to layered: 2.10 vs 2.12 — the errors just CONCENTRATE in the
town band). This fork kills the rigid grid while keeping everything
else identical: still one vocabulary, still one deliberative pass,
still no structure/edge/texture stages.

## The single mechanism, extended from scale to position

The rigid fork's decision machinery, unchanged in currency:

- Every region is evaluated against the **flat-mean baseline** e0
  (SSD of the region from its own mean).
- TAKE vs SPLIT is decided by **gain-per-byte**: (e0−ea)/ca vs
  (e0−es)/cs, exact integer cross-multiplication, ties → TAKE.
- Vocabulary selection converges on marginal **explained energy**
  tau_s = 9·3·s² (per-value 9, the v2 precedent). No motif-count caps.

The extension — a region now decides its own SPLIT POSITION from its
content:

1. **Regions are rectangles** (x0, y0, bw, bh), not dyadic squares.
   Entry is the whole image as one region — there is no grid at any
   level, not even a 64-entry-grid.

2. **Split-position criterion (CART rule, recorded per split).**
   For a region R, among candidate binary cuts, choose the cut that
   minimizes E_flat(child1) + E_flat(child2) — equivalently, the cut
   that MAXIMIZES the energy explained by allowing two means instead
   of one, measured against the same flat-mean baseline e0 the whole
   fork uses. This is the decision-tree (CART) splitting rule: the
   content boundary is where the two-piece flat fit beats the one-piece
   flat fit by the most. No thresholds, no tuned constants, no
   chasing the layered number.
   - Candidate cuts: every pixel position, vertical c ∈ [4, bw−4] and
     horizontal r ∈ [4, bh−4]. The ≥4 guard is the inherited floor:
     the smallest atom scale is 4, and a region thinner than 4 in any
     dimension cannot be tiled by the vocabulary (same floor as the
     rigid fork's 4×4 must-take, generalized to rectangles).
   - Tie-break (canonical, deterministic): strictly-less-than
     replacement while scanning → lowest position wins; vertical cuts
     scanned before horizontal → vertical wins ties.
   - E_flat of a segment is computed from per-column / per-row
     sufficient statistics (Σx, Σx² per channel) in the EXACT integer
     form of block_patch_sub (mean = Σx/n by integer division, then
     Σx² − 2·mean·Σx + n·mean²), so the criterion agrees bit-for-bit
     with the e0 used in the take/split decision.
   - A region with no valid cut (bw < 8 and bh < 8) MUST take.
     All regions satisfy min(bw,bh) ≥ 4 by construction (cuts keep
     ≥ 4 on the cut axis; the other axis is the parent's, ≥ 4).

3. **TAKE for rectangles: tile at fit scale.** A rectangle R takes the
   vocabulary at s* = the largest atom scale s ∈ {64,32,16,8,4} with
   s ≤ min(bw,bh), tiled on a regular grid anchored at R's top-left
   (row-major, canonical). Edge tiles are partial (clipped to R) and
   match the atom's top-left corner — the same partial-block rule the
   rigid fork already used for image-edge blocks. Each tile takes its
   best atom (min SSD, lowest index wins, NULL atom 0 always
   available) plus its own free mean. Cost ca = ntiles × 10 bytes
   (the actual region-record size — not tuned, it is the format).
   Each tile becomes a final region record (x, y, s, atom, r, g, b):
   the knowledge map format "TNNKNLM1" is UNCHANGED, and the emit
   path (path B) is byte-identical logic to the rigid fork.

4. **SPLIT deliberation, then DECIDE.** Given the CART-chosen cut,
   both children recurse (the single deliberation, unchanged in
   spirit). es/cs are the children's optimal error/cost. The parent
   takes iff (e0−ea)·cs ≥ (e0−es)·ca. Provisional child decisions and
   region records roll back on TAKE (same snapshot/restore pattern as
   the rigid fork). Recursion terminates: every split strictly
   shrinks both children, floor at min-dim 4.

5. **Recorded in the trace.** Every split records: rect, axis,
   position, E0(R), E0(c1)+E0(c2), explained energy. Every take
   records: rect, fit scale, tile count, ea, ca. The deliberation
   trace is the audit trail of where TNN put its boundaries and why.

## What did NOT change (deliberately)

- Vocabulary: one farthest-point pass per scale over full s×s
  candidate blocks, same tau_s, same NULL atom 0. Untouched.
- Survey: per-scale flat energies + total. Untouched.
- Residual: the same honest error channel, excluded from
  understanding metrics. Untouched.
- Render: pixel = clamp(atom_shape + tile_mean); white-box paths A
  (per-pixel via region-id map) and B (per-region stamping from the
  knowmap alone) must agree byte-identically. Untouched.
- Metrics: pre-residual PSNR/SSIM via the same metrics.py.
- Determinism: zero RNG; lowest-index tie-breaks; canonical orders.

## Why this is honest (Micah's bar)

- The split-position rule contains NO free parameter to tune: the
  argmin over cut positions of a quantity already in the design
  (flat-fit energy). There is no threshold, no weight, no constant
  chosen to close the 1.53 dB gap. If adaptive splitting closes the
  gap, it does so because content-aligned boundaries let atoms match
  — the recorded reason — not because a knob was turned.
- The take/split currency (gain-per-byte vs flat baseline) is the
  fork's own machinery, extended to position exactly as briefed.
- Failure is reportable: if adaptive loses or ties, the trace shows
  where the cuts went and the error map shows what the atoms still
  can't match. A clean negative stands.

## Falsifiable predictions (recorded before running)

- P1: adaptive closes part of the 1.53 dB gap vs layered zoom,
  because boundary-mismatch errors (the concentrated town-band
  errors) shrink when cuts sit on content edges.
- P2: the pentagon artifact stays eliminated — no polygonization
  step exists in this pipeline either (exemplar patches contain real
  curves; verified by re-render, not assumed).
- P3: the REMAINDER of the gap, if any, points at the vocabulary's
  remaining rigidity: atoms are still SQUARE and axis-aligned, and
  CART cuts are axis-aligned — diagonal boundaries (rooflines) still
  staircase. The error map will confirm or refute this.

## Standing rules honored

- Pure Zag; zero RNG; byte-identical reruns ×2 (knowmap, renders,
  trace; SHA-256).
- No arbitrary limits: cut positions span every valid pixel; floor 4
  inherits the vocabulary's smallest scale; region-record cap is
  sized from the pixel count (32768 ≥ 95744/16 worst case + margin),
  never a tuned bound.
- Commit target: tnn-native-lab, never main. Code + docs + verdict
  evidence only (no binaries, .zagd, BMP/PNG renders).

## Amendment 2026-09-26 (post-run-1)

Run 1 scored 21.42 dB / 0.7870 SSIM — far below the rigid 29.27 dB.
White-box diagnosis (trace + render): the root (512x187) TOOK at 64-scale
for the whole image (ea=137M), and the 512x109 town child TOOK at 64
(ea=300M). The greedy gain-per-byte, applied to a LARGE rect whose take
tiles N atoms, aggregates N tiles into one decision: smooth tiles' gains
drag complex tiles into a coarse take, and the myopic recursion never goes
deep. The rigid fork avoids this because it decides PER 64x64 block — no
aggregation. The inherited currency is sound per-tile; it fails per-rect.

Fix (structural, not a tuned threshold): a take matches ONE vocabulary
atom. If the rect is bigger than its fit-scale atom (bw > s or bh > s),
deliberation has not finished the structure — it MUST split via the CART
rule. Only an atom-sized rect (bw <= s and bh <= s, i.e. exactly s x s)
may deliberate take-vs-split by the inherited gain-per-byte. Floor (no
valid or no energy-reducing cut) falls back to the tiled take. This keeps
one mechanism and one pass; the CART rule still chooses every position.
