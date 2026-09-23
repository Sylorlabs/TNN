# Round 5 report — composed paradigm, all four killers dead

Date: 2026-09-22. Task: continue the composed paradigm (Round-4 winner, 3–2,
but 1/5 on the absolute blind bar) and kill the four recurring tells while
preserving Round-3 strengths (layered haze, unified warm/cool light,
foreground/midground/background depth order).

## Deliverables

- `img/r5_alien.zag` — pure-Zag canonical generator (no RNG anywhere)
- `img/r5_alien_1024.bmp` — 1024×1024 24-bit canonical artifact
- `img/r5_alien_1024.png` — lossless Python re-encode, preview only
- `img/verify_r5.py` — dedicated Round-5 killer/light verifier (Python, verify only)
- `img/r5_layout.txt` — SUN/PLANET/MOON/ROCK layout printed by the binary

## Frozen bars (PREREG.md)

| Bar | Result |
|---|---|
| D-RES 1024×1024 24-bit | PASS (`1024x1024`, 24-bit BMP) |
| D-SHARP ≥ 1.20 | PASS — grad(O)=3.305, grad(B)=1.219, ratio=**2.710** |
| D-DET two clean reruns byte-identical | PASS — 3 independent runs, sha256 `fb3a011a…748fc` ×3 |
| Pure Zag canonical path | PASS — Python only re-encodes/verifies |
| Zero randomness | PASS — integer hash noise, no RNG |
| No znc slice > 2^25 B | PASS — one ~3.15 MB RGB buffer |
| D-COMP anti-template audit | PASS — zero axis-aligned filled-primitive placement tokens |

SHA-256:
- `r5_alien_1024.bmp`: `fb3a011a6e83ee06f8bc687a2f382b3dd7cc435c429ce1c89b908bee20f748fc`
- `r5_alien_1024.png`: `9beff28ecb37aaa84db38ef97025c9a9b8f75f88950d00e4cc154e1a3768347d`
- `r5_alien.zag`: `0cd829312d11a16ed8ab00a37e85b21d485ca27a43304f89bd83694158cf1ba8`
- `verify_r5.py`: `e48267058e9391cd4c27847f20baf87ec2c00bc92c14af50caa430fcc7f8ad3b`

Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Binary was emitted to `/tmp` only; no binaries, `.zagd`, or `.zag-cache`
are committed.

## Light self-check (K4 — one sun), `verify_r5.py`

Shared sun vector `SUN = (-930, -140, 340)` → screen azimuth 188.6°.
Implied azimuth sampled from lit-centroid asymmetry of the rendered pixels:

| Element | Implied az | |Δ vs SUN| | Verdict |
|---|---|---|---|
| planet | 183.5° | 5.1° | PASS |
| moon | 218.3° | 29.8° | PASS |
| hero rock | 191.8° | 3.2° | PASS |
| hero-rock shadow | 17.6° (expect sun+180=8.6°) | 9.0° | PASS |

All four agree with the single numerical sun vector (bars: ≤30° for bodies,
≤45° for the shadow). Round-4's rock-normal bug (lateral normal negated,
rocks lit from the wrong side vs their shadows) is fixed: physical outward
normals dotted directly against the shared sun.

## Per-killer evidence

**K1 — pasted-disc planet.** The giant is now small (r≈0.105w vs R4's
0.156w), heavily extincted, with a turbulent soft limb and cirrus drifting in
front of its lower-left limb; the terminator uses the shared sun vector.
Measured on the render: limb 15–85% blend width **26.0px** over 14 spokes
(need ≥2.5); limb radius std **1.69px** (need ≥1.2 — not a perfect circle);
|edge−sky|/|center−sky| = **0.18** (need <0.55 — the limb dissolves into sky).

**K2 — repeating/template mountains.** Four separate profile functions
(ghost / far asymmetric summit / mid canyon-gully / near rolling foothills),
distinct palettes, strata directions, gully treatments, haze amounts; summits
noise-roughened; patchy 2D bump lighting dominates the 1D slope term; gullies
fade toward row bases. The verifier reimplements the Zag integer noise in
Python (validated against the binary's own rock layout: 6/6 ground-line
predictions match to <1px) and checks the heightfields: no narrow
autocorrelation spike >0.35 at any repeat lag 150–500px for any row (a stamped
peak train would imprint one); the far row's two summits measure 136px/131px
wide vs 119px/79px wide (different mountains, not stamps); detrended pairwise
row cross-correlations all ≤0.21 (need <0.35).

**K3 — floating rocks.** Six irregular squat domes (seeded lean + wobble,
never spheres), perspective-staged sizes with depth offsets, buried bases,
contact-AO crescents, and long soft cast shadows along the sun azimuth.
Per-rock measurements (all 6 PASS): AO darkest-quartile / local-plain ratio
0.42–0.80 (need <0.92); foot pixel dirt-tinted vs crown (burial blend);
dome top-height/radius 0.67–0.75 (need 0.55–0.90 — squat, never 1.0);
near-field shadow-core / flanking-ground ratio 0.83–0.93 (need <0.95).
Two real defects were found and fixed during verification: (a) shadows+AO
were gated on the plain only, so the three far boulders (which sit high in
frame, against the hills) had their shadows/AO silently unpainted — now
applied to all ground; (b) the shadow fade stopped at 38% strength at the
wedge end, printing a straight edge on the ground — now fades to zero.

**K4 — inconsistent lighting.** See table above: four independent elements
agree with the one sun vector. (Round-4 failure mode — negated rock normals —
was caught by code review and is covered by the hero-rock centroid check.)

## Honest limitations

- The moon's implied azimuth (29.8°) only just clears the 30° bar — it is a
  22px disc, so the centroid is noisy; the margin is thin.
- The far-row silhouette keeps a mild vertical banding read at the summit
  crags (much reduced from R4, but not fully gone); the 2D relief lighting
  only partially breaks the extruded look.
- The mid row's teeth are still somewhat regularly spaced (ridge at /75);
  silhouette variety comes mostly from the differing row profiles.
- Ground mottling (±25 luma) is stronger than the far-field shadow signal,
  so small-rock shadows read mainly in the near field; the verifier's shadow
  bar (0.95) is correspondingly lenient.
- Blind judging is pending with the separate crew; nothing here claims
  aesthetic success, only that the four mechanical tells are dead.

## Reproduce

```
cd imagination_discovery/img
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 r5_alien.zag --no-zagd --no-analyze -o /tmp/r5_alien
/tmp/r5_alien /tmp/r5out 1024        # writes r5_alien_1024.bmp + R5LAYOUT to stdout
python3 verify_bars.py r5_alien_1024.bmp
python3 verify_r5.py r5_alien_1024.bmp r5_layout.txt
```
