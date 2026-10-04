# VERDICT_H1.md - H1 LIT CLOUD DECK, wave-20261001-1721pdt

Verdict: DISCARD

Frozen verdict mapping applied: a clean pass requires every frozen kill
bar KB1..KB9 to pass as specified; any bar failed maps to DISCARD. KB3
failed as frozen. No bar was weakened, narrowed, or re-interpreted to
force a pass. No sealed A/B pair and no JUDGE_BRIEF.md were prepared
(those exist only on a clean pass). Nothing enters the judge queue.

## What was built (implementation order per prereg)

1. Prereg frozen and written first: SENSORY/PREREG_H1_CLOUDS_1721.md,
   sha256 0d447ed25e93adbb3fd5764c5600e6155988f78ce2f395e642771ce6f541d1b2,
   mtime 2026-10-02 00:32:26 UTC, predating every H1 implementation
   artifact. (Commits forbidden this wave; ordering evidence is file
   mtime + sha256.)
2. IO substrate: h1/sub/R33_NATIVE_IO_V1.zag, byte copy of the
   wave-20260924-1121pdt vendored file, sha256
   e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8,
   re-verified.
3. Baseline FIRST: h1/r11_baseline.zag is a byte copy of
   docs/lab/imagination_discovery/img/r11_alien.zag with only the
   @import line repointed (diff-verified: exactly one line differs).
   Two 1024 renders byte-identical:
   72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b x2.
   Gate PASSED. No substitution. (Stated openly: no frozen r11-1024
   baseline hash exists on record, so the gate is determinism-based.)
4. H1 mechanism: h1/h1_clouds.zag. The baseline's flat cirrus mix block
   inside b_sky replaced with the frozen lit-cloud-layer block verbatim
   (h1_dens with frozen seeds 601/602, coverage 0.52/0.14, thickness fbm
   604, forward-difference density gradient, shade = 0.62 + 1.2*slope*th
   clamped [0.05,1.35], 2-tap self-shadow march toward the frozen sun
   azimuth (-0.628,-0.778), warm tops / dust-glow underlight bases,
   silver lining on thin sun-side edges, coverage alpha composite).
   Output names changed to h1_clouds_*.bmp (bookkeeping only).
   Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
   sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
   verified before use.
5. Verifier: h1/h1_verify.zag (pure Zag), world model copied verbatim
   from the baseline (camera basis, b_trace, b_moonhit), frozen point
   sets per prereg. Geometric validator ran on the rebuilt baseline
   BEFORE the variant rendered: SKYWIN 48/48, TERRAIN 64/64, MOON 16/16,
   FULLSKY 144/144, SUNHALF 25, ANTISUN 23. All asserts passed.
6. Lane infrastructure (not candidate machinery): h1/tools/bmp2png.zag,
   a pure-Zag 24-bit BMP to PNG converter (stored deflate blocks,
   table-free CRC32), used to view renders and package pairs. Reusable.

## Per-bar results (1024, h1a vs base1)

| Bar | Measured | Frozen bar | Result |
|-----|----------|------------|--------|
| KB1 determinism | h1a == h1b byte-identical; h1c pending (moot, see below) | 3x identical | MOOT |
| KB2 coverage | 0.2916 | [0.08, 0.60] | PASS |
| KB3 light logic | sun_mean +1.52, diff -2.13 | diff >= 6.0 and sun_mean >= 3.0 | FAIL |
| KB4 structure var(dL) | 64.33 | >= 40.0 | PASS |
| KB5 terrain mean\|dL\| | 0.65 | <= 1.0 | PASS |
| KB6 moon mean\|dL\| | 0.00 | <= 1.0 | PASS |
| KB7 sky calm | mean 0.00, bigfrac 0.1388 | \|mean\| <= 5.0, frac <= 0.35 | PASS |
| KB8 anti-grain acutance ratio | 1.036 | <= 1.15 | PASS |
| KB9 cost | h1a 552 s vs base 819/590 s | <= 4.0x | OBSERVED PASS |

## Killing evidence

KB3 as frozen: mean(dL over SUNHALF kept) = +1.52 luma steps (bar
requires >= 3.0); SUNHALF minus ANTISUN = -2.13 (bar requires >= 6.0).
The anti-sun side brightened MORE than the sun side in
variant-minus-baseline terms (+3.65 vs +1.52).

## Diagnosis: prereg-spec defect (G1-v1 class), not a mechanism misfire

The mechanism is directionally correct: the 1024 render shows warm
amber lit clouds on the sun side (left) and dark violet cloud masses
on the anti-sun side (right), with structured tops, dark bases, and
no grain, banding, or artifacts (KB8 1.036, KB7 clean, KB5/KB6
non-regression holds). KB4 (var 64.33) confirms strong structure, not
wash.

KB3 failed because it measured dL asymmetry, which was dominated by
baseline headroom, not by the mechanism's light logic. The baseline's
sun-side cirrus was ALREADY bright warm (mix toward (1.0,0.72,0.55) at
0.55 alpha), leaving little headroom for dL; its anti-sun cirrus was
dim (mix toward (0.55,0.42,0.48)), leaving large headroom. The
variant's anti-sun cloud palette (tops 0.62..0.73 even at low sunAmt)
is brighter than the baseline's dim anti-sun cirrus, and coverage is
higher (no 0.55 cap), so anti-sun dL exceeded sun-side dL. The frozen
prediction ("anti-sun clouds take the dim dust-glow base") was wrong
about the baseline-relative direction because lk on the anti-sun side
sits at 0.1..0.5, not near zero.

A correct directional bar would be variant-side (e.g. variant
sun-side vs anti-sun-side cloud luminance ratio, as G1's KB2 did),
not dL-based. That bar belongs in a FUTURE prereg, not in this wave:
the frozen bar failed as written, and the verdict mapping is
mechanical. This is the same defect class as G1 v1 (bar specified
without validating what it measures against the baseline), one step
later in the pipeline.

## Red-team notes (knowledge vs architecture)

- Cotton-ball look: the H1 clouds read as discrete puffy masses
  rather than wind-streaked dusk cirrus. Cause: the density field's
  roughly isotropic fbm blobs plus a coverage threshold that isolates
  masses. This is a field-design (knowledge) choice, not a substrate
  flaw; a future mechanism could stretch the field along the frozen
  wind or layer it.
- Right-side clouds are heavy/dark: the self-shadow plus low lk makes
  anti-sun masses read stormy. Knowledge choice; the underlight gain
  (0.85) could be revisited in a future prereg.
- No dropout, flicker, grain, banding, or NaN specks observed.
  Terrain and moon pixels are untouched by construction (KB5 0.65 is
  dither-rounding on cloud-adjacent pixels; KB6 exactly 0.00).

## Determinism observation (KB1, non-decision)

h1a: eaa71a18ccb657d0260a6d4ab7e534d180c7d79d16b54f3eb65aa5816b1cb7cf.
h1b: identical hash (2/2). h1c render pending at verdict time; hash to
be recorded in evidence/sha_h1.txt. KB1 is moot: KB3 already killed
the candidate, and the mapping does not require completing moot bars.

## Standing consequences

- H1 LIT CLOUD DECK: DISCARDED. Not queued for judgment.
- The sensory image lane returns to stand-down; the next cloud attempt
  needs a fresh prereg with a variant-side directional bar and a
  wind-stretched density field, not a re-aim of this one.
- Reusable: h1/tools/bmp2png.zag (pure-Zag BMP to PNG) and the
  h1_verify.zag world-model-copy verifier pattern.
