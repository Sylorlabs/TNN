# REDTEAM C-D19 - red-team attack on the frozen confound list

Wave wave-20260924-0521pdt. Worker C. Date 2026-09-24.
Target: D19 focus-plane detail (s19_focus.zag) vs r8c baseline.

## Confound 1: detail is disguised grain (the E3 line)

Attack: the F1/F2/F3 accents are small high-frequency marks; if they
scatter energy uniformly they are grain by another name, and Micah
already rejected grain.
Result: COUNTERED. KB4-SKY = 10000 bp = 1.0000x, bar <= 1.10. Zero
sky dabs exist in the mechanism, and the 12 frozen sky sample points
are bit-identical in acutance between arms. No uniform HF lift.

## Confound 2: sharpening halos

Attack: dark accents on light ground (or light ticks on dark ground)
produce visible fringes.
Result: COUNTERED (moot). The 256px focal crop at 1x shows no fringing;
the accents are too weak to fringe. The crop comparison
(base vs variant) is nearly indistinguishable, which is itself the
KB2 story, not a halo story.

## Confound 3: metric gaming by point selection

Attack: sample points chosen after seeing renders would inflate ratios.
Result: COUNTERED. All 132 sample points were frozen in PREREG_C_D19_0521.md
before any D19 code existed: 40 F3 centers and 80 stone points from the
frozen hash formulas, 12 fixed sky coordinates. The verifier
recomputes them from the same formulas; no post-hoc selection.

## Confound 4: baseline mismatch

Attack: the variant is compared against the wrong baseline.
Result: COUNTERED. The in-wave baseline rebuild reproduces the
committed r8c BMP byte-identically
(sha256 e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d).
The blind-pair baseline arm would have been this rebuild.

## Confound 5: program-level critique (another r8c dab iteration)

Attack: this is one more micro-lever on the 09-22 r8c substrate; the
red-team program finding says that lane is exhausted.
Result: SUSTAINED, and the numbers agree with the critique. D19 was
designed as a global focus mechanism, but 208 small dabs do not move
the 1024px read: the full-frame variant is indistinguishable from the
baseline at normal viewing scale. The binding constraint appears to be
the substrate's own softness stack (soft dab primitive, 50 uniform haze
dabs, per-pixel pass-5 grain), not a lack of detail marks. Negative
result of record: detail dabs at this scale do not change the
painting-vs-photo read. A future focus lever must change the
mark-making primitive or the haze/grain stack, not add more dabs.

## Confound 6: knowledge vs architecture

Attack: the gain comes from the verifier knowing dab positions.
Result: COUNTERED. Position knowledge is measurement only; the renders
carry no position information, and no blind pair is being presented,
so there is no channel for it to leak into a judgment.

## Extra red-team finding: KB2 shortfall is genuine, not a metric artifact

KB2-FOCUS = 11804 bp = 1.18x vs frozen bar >= 1.30. Cross-checked:
the painter and verifier use identical hash formulas (verified by
inspection); the 208-dab budget is program-asserted and trace-logged;
the focal crop at 1x shows the F3 cluster swallowed by the region's
haze and grain. The bar miss is a mechanism shortfall (focal accents
too small/subtle against the textured peak shoulder), not a broken
ruler. KB3-STONE = 1.90x is real but visually negligible at scale,
which corroborates: the dab primitive at this size does not register
perceptually.
