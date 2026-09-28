# BEAUTY MECHANISMS — r10, classification and verdicts

Date: 2026-09-22. Law (Micah): imagination means LOGIC — every visible
change must trace to a deliberated scene truth. Beauty that comes from
correct physics IS logic-derived. Cosmetic wins are reported as
COSMETIC, never as imagination. Flagship advances on logic-derived only.

Class definitions (from r9, kept):
- LOGIC-DERIVED: TNN deliberated a scene truth and derived the detail
  from that reasoning. The detail exists because the world model says
  it should.
- COSMETIC: a filter/tweak/hash/parameter that improves the look
  without scene reasoning behind it.

All mechanisms: zero RNG (integer hashes, fixed seeds), T1 sun
accessors byte-identical (generator asserts the T1 block unchanged),
D-COMP banned-token audit in the generator, byte-identical reruns
verified per final artifact.

## Mechanism table

| ID | Mechanism | Scene truth it derives from | Class | Targets | Verdict |
|----|-----------|----------------------------|-------|---------|---------|
| B-LAKE | T14: the graben floods — the far lowland becomes a real rift lake: water plane in the SDF where the *tapered* ground drops below WL=-9 beyond 360u, wave-normal field (3 deterministic scales, parallax-faded), fresnel sky reflection from the deliberated dome, half-vector sun-glitter toward the T1 sun (shadow-marched), dissolved by the shared fog pass (repaired 2026-09-22: pre-render source left water unfogged; see Honesty notes) | Rift valleys on basaltic worlds flood below the water table (Tanganyika analog); still water mirrors the sky, glitters toward the sun, dissolves into haze at distance. Reconception of the existing horizon band, not a new asset. | LOGIC-DERIVED | B1 (horizon slab) | PARTIAL-PASS 2026-09-23: left/center horizon is now honest water — glitter path, shoreline, fresnel, fog-dissolved (see compare_horizon). The graben mask does not extend to the right frame edge, so a remnant of the old gray band + hard edge survives at far right. The mechanism works where it applies; the mask extent is the documented limit. |
| B-FILL | Two-lobe hemisphere sky ambient: lobe 0 = sky in the normal direction, lobe 1 = sky at the sunward horizon (T1 ground-track azimuth), gains for 0.6 bar silicate dust | A ground point's sky hemisphere includes the bright sunward horizon band; the old single normal-direction sample threw that light away — the physical reason shadowed ground went black. Multiple scattering is generous in dusty air. | LOGIC-DERIVED | B2 (black foreground) | PASS 2026-09-23: foreground fully legible — warm textured dust, pebbles, angular rocks with shape (see compare_foreground). No black crush anywhere. The massif now models form instead of silhouetting. |
| B-GLINT | Microfacet fix: the power-~60 glint lobe amplitude fades as `1/(1+t/260)` — specular integrates over the pixel footprint | Rough-surface specular must widen/weaken with distance; sub-pixel normal variation firing a tight lobe is aliasing, not light. Near-field volcanic glass still glints. | LOGIC-DERIVED | B3 (waxy streaks, sparkle chains) | PASS 2026-09-23: sparkle chains on the ridge crest and isolated white speckles on the foreground are gone (compare_foreground, compare_horizon); no waxy smears on broad slopes; near volcanic glass retains tight glints. |
| B-AERIAL | Scatter coefficient `t*0.0011` → `t*0.0019` in the exponential fog, same azimuth-dependent horizon target | 0.6 bar of silicate dust scatters harder than the old coefficient admitted; far ranges must pale and lose contrast, and the far plane must dissolve, not end in an edge. | LOGIC-DERIVED | B4 (no perspective), B1 edge | PASS 2026-09-23: the far ridge pales and loses contrast against the mid-ground massif; the lake dissolves into haze at distance. The far plane no longer ends in an edge where the lake applies; the surviving right-edge band is the B-LAKE mask limit, not a fog failure. |
| B-MOON | Planetshine 0.34→0.52 (albedo-scaled, flat — earthshine is roughly uniform); terminator stays sharp, no limb glow | Earthshine/planetshine is real light transport; the old value was below display-size legibility so the disc read as a hole. Limb glow DECLINED: Cinder is deliberated airless (T3) — atmosphere glow would contradict the world. | LOGIC-DERIVED (partial; decline documented) | B5 (black balloon moon) | PASS 2026-09-23: the disc reads as a cratered world, not a hole (compare_moon); terminator razor-sharp, phase consistent with the one sun. |
| B-CLOUD | Silver lining: forward-scatter brightening on sunward cirrus edges, gated to `m*(1-m)`; r9 M-c wind-sheared filaments kept | Ice streaks between viewer and sun forward-scatter (Mie) — sunward edges silver. Filament shear follows the deliberated +x/-z upper-wind azimuth. | LOGIC-DERIVED (lining) / LOGIC-DERIVED (weak) (filaments) | B6 (flat clouds) | MARGINAL 2026-09-23: the mechanism fires (sunward edges brighten) but reads subtle at display size; the sky crop shows little change vs r8b. Honest: this tell is improved, not fixed. |
| B-STRATA | Flood-basalt flow banding: world-space y-band noise on steep faces (slope>0.55), subtle, distance-faded | A shield volcano stacks lava flows; strata show on steep faces. | LOGIC-DERIVED | B8 (clay slopes) | PASS 2026-09-23: flow banding visible on the right-ridge steep faces; slopes no longer read as smooth clay. |
| M-F | Rock angularity rev2 (r9): ridged broad-facet displacement, smin 3.0→0.8, per-rock mineral tint, fracture crackle | Jointed basalt breaks into angular blocks with planar fracture faces — never taffy. | LOGIC-DERIVED | B7 (taffy rocks) | SHIPPED = r9 WINNER (FINAL.md: PARTIAL — advances on silhouette; faces still smooth). Foreground rocks read as discrete angular blocks. |
| M-P | Cobbles rev3 (r9): hashed 9.0-unit grid, r 2.0–4.5, min-blended, per-cobble tint, contact shadows via existing march | Weathering/rockfall shed discrete stones that sit ON the ground as separate bodies. | LOGIC-DERIVED | B7 (no pebbles, no scale cues) | SHIPPED = r9 WINNER (FINAL.md: PARTIAL WIN — tint makes separate stones legible). Foreground cobbles read as separate stones with contact shadows — the distance relationship's near anchor. |
| M-D | Ejecta-sorted grain rev2 (r9): grain amplitude follows proximity-to-rock + dust-settling mask | Comminution + aeolian sorting: coarse near sources, fines where dust settles. | LOGIC-DERIVED | B7 (flat albedo) | SHIPPED = r9 WINNER (FINAL.md: WIN — ground reads as regolith, not wash). Foreground ground carries mineral grain at every scale. |
| M-b | Downslope striation (r9): two-scale streak noise in albedo, gated by slope, distance-faded | Wind/water carve gullies downhill along the fall line. | LOGIC-DERIVED | B8 (no fine erosion) | KNOWN LIMIT (FINAL.md: MISS — albedo-only, too subtle; rev2/rev3 FAIL). Shipped as spec'd; contributes little. r11 should drop it or carve geometrically. |
| M-e | Talus chips (r9): octahedron SDF, hashed scatter at rock bases, half-buried | Rockfall sheds angular fragments that accumulate at outcrop bases. | LOGIC-DERIVED | B7 (scale, talus) | KNOWN LIMIT (FINAL.md: rev1 MARGINAL — renders but doesn't read; rev2 M-E is the PARTIAL WIN winner and is NOT in this frame). Shipped as spec'd; r11 should swap to M-E rev2. |
| M-g | Shadow-side grain boost | NONE — excluded from r10. B-FILL answers the same tell (B2/D5) from scene truth instead. | COSMETIC (excluded) | — | EXCLUDED |

## Honesty notes

- B-LAKE's wave field is statistical (three noise scales), not a
  simulated water surface; the REFLECTION geometry (fresnel, mirror
  vector, glitter half-vector, fog) is analytic. The shoreline is a
  blend, not a surf zone. The mask reads the *tapered* field
  (b_hfull), so water and rendered ground always agree — an earlier
  rev read untapered b_hbase and left patchy dry/water disagreement;
  fixed before any committed render.
- An earlier b_wshade rev applied its own fog inside the shader and
  would have been fogged twice by the shared pass, erasing distant
  glitter; fixed (single shared fog) before any committed render.
  CORRECTION 2026-09-22 (resume crew): on review the "single shared fog"
  was not actually present in the pre-render source — the fog lived only
  inside b_tshade, so water would have rendered UNFOGGED to the far
  plane (glitter path + wave texture undissolved, a hard water/sky
  seam — B1's razor edge on the lake itself). Repaired in gen_beauty.py:
  b_wshade now applies the same fog formula as b_tshade (identical
  `1-exp(-t*0.0019)` and azimuth-dependent horizon target, same t);
  b_render applies no fog of its own, so this is the single shared
  pass — the shoreline blend mixes two identically-fogged values and
  stays consistent. The repair is byte-verified: the only src diff vs
  the pre-render file is this change.
- B-FILL's lobe gains (0.40/0.60) are set by deliberation about the
  dust load, not measured — the DIRECTION (hemisphere integration of
  the deliberated dome, lobe 1 on the T1 sun's ground-track azimuth)
  is the logic claim; the exact gains are the honest residual.
- B-MOON deliberately does NOT implement the brief's "limb glow":
  it would contradict T3's airless Cinder. Reported as a decline, not
  a silent skip.
- The r9 revs are included on the detail crew's own iteration
  evidence while their blind judging is still in flight; if the
  judges reject any, it comes out of the flagship.
- 2048² declined: the frozen raymarch costs ~2.8 hr per 1024² frame;
  2048² would be ~11–14 hr. The prereg minimum is 1024² and the bar
  is judged at display size.

## Resume repairs (2026-09-22, resume crew)

The prior crew's work was sound but died mid-render; the resume found
two things before the final render:

1. B-LAKE fog defect (FIXED): the pre-render source fogged terrain
   inside b_tshade but left water unfogged — the "single shared fog"
   the honesty notes claimed did not exist in the code. The lake would
   have rendered to the far plane undissolved. Repaired in
   gen_beauty.py: b_wshade applies the identical fog formula; only the
   intended diff changed; binary rebuilt; determinism re-proven.
2. r9 rev inventory (DOCUMENTED, not changed): the shipped talus is
   M-e rev1 (0.25–0.9u, judged MARGINAL by the r9 crew's own technical
   read; the M-E rev2 winner is not in this frame) and striation is
   M-b (judged MISS/too subtle). The mechanism table above said
   "pending r9 judging" — the r9 technical verdicts (r9/FINAL.md) now
   exist: FPEDc = M-F + M-P + M-E + M-D + M-c; blind judging still in
   flight. The r10 spec as written ships M-e and M-b; swapping to the
   judged winners would be a spec change, so it stays documented as a
   known limit rather than silently "fixed".

## Dropped / declined

- M-g (COSMETIC): excluded; B-FILL covers the tell from logic.
- Moon limb atmosphere glow: declined as world-contradicting (T3).
- Second low cloud deck: considered, skipped — the cirrus deck's
  horizon fade already reads as altitude structure; restraint over
  new elements.
