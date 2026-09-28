# Round 6 report — qualitative craft fixes on the round-4 champion (D-IMG-1)

Date: 2026-09-22. Base: `r4_alien.zag` (head-to-head champion: beat R3 3–2,
beat R5 4–1). Method: qualitative craft fixes BY EYE against the judges'
reward list (crispness, contact shadows, surface texture, inter-plane haze,
one unified light). NO quantitative tell-death metrics — round 5's lesson
("measures clean but reads worse") was honored throughout.

## Deliverables

- `img/r6_alien.zag` — pure-Zag canonical generator (no RNG anywhere)
- `img/r6_alien_1024.bmp` — 1024×1024 24-bit canonical artifact
- `img/r6_alien_1024.png` — lossless Python re-encode, preview only
- `img/ROUND6_REPORT.md` — this file

## What changed and why (by eye, referencing judge comments)

**1. Pinstripe mountains — root-caused, not metric-chased.** A diagnostic
render with far-range gullies disabled showed the vertical striping
UNCHANGED: the stripes were never the gullies. They were the *lighting
term* — the ±6px gradient of the ridged heightfield sampled the sharp
ridge creases and printed each as a light/dark vertical stripe pair
(the "pinstripe-extrusion" / "organ-pipe" tell named by R4-J4, R5-J1/2/5).
Fix: far range lit from a ±24px wide-baseline gradient of the same
heightfield (broad massif slopes, creases averaged out); mid hills lit
from a ±18px baseline of the smooth profile (round 4's ±6px "palisade
fix" was incomplete — the base ridge still creased). The crag terms
still roughen both silhouettes, so crispness is kept. The gullies were
also reworked (low-frequency x-warp breaks regular spacing, per-channel
downslope lean, patchiness breaks full-height stripes) and the mid-hill
lip term had a mismatched v-scale that printed decorrelated bright
stripes — fixed to match the channel field.

**2. Decal boulders.** The round-4 rocks were near-perfect discs
("floating disc-rocks", R4-J3; "decal boulders", R4-J4). Now: two-scale
edge wobble (big asymmetric lobes + fine crag, per-rock seeds), squashed
bases so each boulder settles into the ground instead of perching, and a
noise-broken burial blend at the foot — the lower flank dissolves into
the dirt with a talus line. The hero boulder reads as one lumpy,
weighty rock; contact darkening and cast shadows retained.

**3. Feathered planet limb.** Tighter 2px anti-aliased limb and a thinner
rim wash (was 3px + heavy extinction feather). The giant now reads as a
solid body with a haze line; the defined terminator judges rewarded in
R4 is kept.

**4. Inter-plane haze.** A thin haze lift at the mid-hill crests —
atmosphere *between* the mid hills and the far range, never fog over
everything (the R5 failure mode).

**Kept from R4:** crisp silhouettes, embedded rock shadows, surface
texture at every scale, one unified sun, dusk composition, hash dither.

## Frozen bars (PREREG.md)

| Bar | Result |
|---|---|
| D-RES 1024×1024 24-bit | PASS |
| D-SHARP ≥ 1.20 | PASS — grad(O)=3.749, grad(B)=1.487, ratio=**2.522** |
| D-DET clean reruns byte-identical | PASS — 3 independent runs, sha256 `9335bc8c…19859` ×3 |
| D-COMP anti-template audit | PASS — zero axis-aligned filled-primitive placement tokens |
| Pure Zag canonical path | PASS — Python only re-encodes/verifies |
| Zero randomness | PASS — integer hash noise, no RNG |
| No znc slice > 2^25 B | PASS — one ~3.15 MB RGB buffer |

SHA-256:
- `r6_alien_1024.bmp`: `9335bc8c736e5410e275f105fd46dda2d1055c529c25c5405dc32666fbf19859`
- `r6_alien_1024.png`: `d77416c76b8ec35c20b8b052abae85aee9ce598ee02f9d49f99282081b04f038`
- `r6_alien.zag`: `b49fdd1c7e6abe6ef906894f891082527c48cfc041b317f2bf7ab6731a759c60`

Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(`--no-zagd --no-analyze`); render ~3.5 s at 1024². Binary emitted to
`/tmp` only; no binaries, `.zagd`, or `.zag-cache` committed.

## Iteration log (honest)

- Pass 1 (gully-only rework): mountains still striped → diagnostic render
  with gullies disabled proved stripes were the lighting term, not the
  gullies. This is why the brief says diagnose, don't metric-chase.
- Pass 2 (wide-baseline lighting): far-range pinstripes gone; mid hills
  still picket-fence → second diagnostic (mid gullies disabled) proved
  the mid stripes were also the lighting term (incomplete R4 palisade
  fix). Wide-baseline fix applied; fence gone.
- Pass 3 (mid lip v-scale match + gentler channels + 2D mottle):
  final. Stopped here by eye — further work risked the R5 over-working
  trap.

## Honest limitations

- D-BLIND is the separate judge crew's gate; nothing here claims
  aesthetic success, only that the three named tells were addressed by
  eye and R4's rewarded qualities kept.
- The far range keeps mild vertical texture on its right third; it reads
  as erosion, but a judge may still name it.
- Rock crack patterns remain ridge-noise, not stress-fracture geometry.
- 2048² untested (prereg minimum is 1024²).

## Reproduce

```
cd imagination_discovery/img
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 r6_alien.zag --no-zagd --no-analyze -o /tmp/r6_alien
/tmp/r6_alien /tmp/r6out 1024
python3 verify_bars.py /tmp/r6out/r6_alien_1024.bmp
```
