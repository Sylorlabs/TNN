# Blind judgments — ROUND 5 (2026-09-22)

5 NEW fresh judges. A = round-5 alien planet (r5_alien_1024.png, built
with quantitative per-killer death criteria), B = round-4 alien planet
(r4_alien_1024.png, current head-to-head champion).

## Part 1 — absolute bar on A

| Judge | Verdict | Tells named |
|---|---|---|
| R5-J1 | Yes | vertical scan-line striping on mesas, smeared foreground, stamped crack textures, marble planet, sharp moon terminator |
| R5-J2 | Yes | pasted disc-boulders, vertical smear banding in peaks, hard-ringed planet highlight, flat two-tone moon |
| R5-J3 | No (procedural art, not diffusion) | vertical banding, decal boulders, marbled planet, two-tone moon |
| R5-J4 | Unsure (leans procedural) | vertical banding, sticker rocks, smeary ground, smudged clouds |
| R5-J5 | Yes | columnar striping, contour-ring artifacts, identical marble swirl on every rock AND the planet, flat gray horizon band, pasted planet with hard edge |
| **"not AI"/unsure** | **2/5** | tells named by all 5 |

**D-IMG-1 round 5: FAIL** on the absolute bar (2/5).

## Part 2 — head-to-head A (round 5) vs B (round 4)

| Judge | Pick | Reason (one line) |
|---|---|---|
| R5-J1 | A | softer unified lighting, better depth layering, one light source |
| R5-J2 | B | B's rocks embedded with occlusion, crisp ridgelines; A's mountains smear vertically |
| R5-J3 | B | B's rocks embedded with consistent shading; A's boulders pasted with mismatched lighting |
| R5-J4 | B | B's rocks have contact shading and weight, crisp layered ridgelines; A is a hazy flat backdrop with stickers |
| R5-J5 | B | B has crisper silhouettes, real ground shadows, visible surface texture, defined planet terminator; A is buried in fog/striping/softness |

**Head-to-head: B (round 4) wins 4–1.** Round 5 lost.

## The meta-lesson (important)

Round 5 optimized against the tell list with QUANTITATIVE death criteria
(limb blend width, radius variance, autocorrelation, AO measurements) —
and produced an image that measures clean but reads WORSE to human eyes:
"a 1990s fractal-terrain demo... buried in fog, striping, and softness."
The tell list is a diagnostic, not an objective function. Metric-driven
killer-fixing over-fit: it killed the measurements while regressing the
aesthetics (crispness, embedded rocks, defined terminator) that judges
actually reward.

## What judges consistently reward (stable preference signal)

Crisp silhouettes, real ground/contact shadows, visible surface texture,
atmospheric haze BETWEEN depth planes (not fog over everything), one
coherent light, objects embedded in terrain with occlusion. What they
punish: softness/smear, vertical banding, pasted discs, floating objects,
flat horizon bands.

## Direction for round 6

Round 4 is the champion base. Round 6 = round 4's craft + qualitative
(not metric-driven) fixes for its real weaknesses: pinstripe-mountain
texture, decal boulders, feathered planet limb. Keep R4's crispness,
embedded rocks, and defined terminator. No numeric tell criteria — the
crew judges by eye against the "reward" list above, then blind judges
decide.
