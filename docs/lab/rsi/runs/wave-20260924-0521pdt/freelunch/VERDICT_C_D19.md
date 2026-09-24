# VERDICT C-D19 - wave-20260924-0521pdt, Worker C free-lunch slot

Candidate: D19 focus-plane detail on the r8c substrate (fulfills frozen D14).
Prereg: PREREG_C_D19_0521.md, commit 35f81a256 (frozen before any D19 code existed).

## Verdict: DISCARD

Killing evidence: KB2-FOCUS = 11804 bp = 1.18x against the frozen bar
>= 1.30x (13000 bp). The focal detail mechanism underperforms its bar
by 0.12x, and the 1x crop confirms the F3 cluster is swallowed by the
focal region's haze and grain: no visible detail gain at (430,400).
The frozen mapping mandates DISCARD on any KB1..KB6 fail; the PARTIAL
narrowing clause (KB5-marginal or fringing) does not apply, and its
narrowing direction (cut alphas) would weaken the already-weak focal
effect. One miss is DISCARD.

## Bar table (measured vs frozen)

| Bar | Frozen | Measured | Result |
|---|---|---|---|
| KB1-DET 3/3 byte-identical | pass | sha256 30a9cd5c404c4b14393660cfc305064c56e6e19745e093b0b146feb013a x3 | PASS |
| KB2-FOCUS acutance ratio, 40 F3 points | >= 1.30 | 1.18 (11804 bp) | FAIL |
| KB3-STONE acutance ratio, 80 stone points | >= 1.20 | 1.90 (19027 bp) | PASS |
| KB4-SKY acutance ratio, 12 sky points | <= 1.10 | 1.00 (10000 bp) | PASS |
| KB5-NONREG mean \|dL\| full frame | <= 8.0 | 0.05 | PASS |
| KB6-COST dab budget == 208 | exact | 208, program-asserted and trace-logged | PASS |
| KB6-COST wall time <= 1.25x baseline | pass | 934 ms vs 979 ms (0.95x) | PASS |
| Baseline byte-identity gate | e4f65557... | e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d | PASS |
| VKB-EYE sealed pair | prepared iff bars pass | not prepared (bars failed) | N/A |

Static checks: no Python files, no interpreter invocations, no
rand/random/srand/time/clock calls in new sources (pure Zag, zero RNG).
Toolchain pinned: znc_linux_x86_64_abed8aa1 sha256 498abcb5...;
IO substrate pinned: e6379ddb... (Linux-ported blob from 72ef158fc,
vendored in-wave).

## Why it failed (mechanism, not measurement)

The 40-dab F3 cluster at the D14 focal point adds only 1.18x local
acutance because the peak-shoulder region is already textured (pass-3
light modeling, pass-4 fixations, D13 haze, pass-5 grain); the small
rad-2/3 accents do not register against it. KB3's 1.90x on the stones
is numerically real but visually negligible at 1024px scale. The
negative result stands: detail dabs at this scale do not move the
painting-vs-photo read on this substrate. See REDTEAM_C_D19.md.

## Sealed pair for Micah

None prepared. The candidate failed its frozen bars, so nothing is
ready for his eyes, and no blind pair was built. His existing judge
queue (R9, S11-IMG, S13, S14, C1, C2v3) is untouched by this wave.

## Commits

- Prereg: 35f81a256 (prereg-only commit, before any D19 code)
- Implementation + evidence: f26e277da
- This verdict SHA fill-in: <this commit>

## Follow-up note (not a claim)

A future wave may re-preregister a focus lever with a recalibrated KB2
or a stronger mechanism (larger accents, a different mark primitive,
or haze/grain-stack changes per the red-team program finding), but
that is a NEW prereg, not a revival of D19 as frozen. D19 as frozen
is dead.
