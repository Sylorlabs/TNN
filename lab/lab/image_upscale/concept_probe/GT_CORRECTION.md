# GT Correction — what the upscale eval actually measures

## Micah's question (2026-09-26)

"If GT is TNN's own [output], the current step is fine" — i.e., is the
ground truth in the upscale eval something TNN itself produced?

## Finding: GT is a held real photograph, not TNN's output

- `stage/gt_512x184.bmp` is a **held-out 512×184 crop of a real photograph**:
  a brick bridge over a river / European cityscape.
- SHA-256: `4ee3414bddd289ca7c9544a91ec39b8885f8dcde96fa0ffa0d56aebc38da1b00`.
- TNN sees only `stage/input_256x92.bmp`, produced by 2×2 box downsampling
  (round-half-up) of that photograph.
- Both TNN and the bicubic baseline construct 512×184 from the same input
  and are scored against the held photograph. This is the standard,
  fair super-resolution protocol.

## Correction to prior docs

Prior trace/design prose could be read as implying the eval target was
TNN-internal. It is not. Any document claiming or implying GT is TNN's own
output is wrong; the numbers that matter are all measured against the held
real photograph.

## Consequence for the "current step"

Micah's conditional ("if GT is TNN's own, current step is fine") does not
trigger: GT is external and held. The pixely-lines problem stands as a
genuine defect (crew-designed LINES operator re-rasterizing doubled
Bresenham chords), and the concept probe (DESIGN.md) was the required
gate before further photo work.
