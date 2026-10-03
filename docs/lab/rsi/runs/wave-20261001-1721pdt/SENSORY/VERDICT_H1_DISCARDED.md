# VERDICT: H1 LIT CLOUD DECK [NEW] - DISCARDED

Wave: wave-20261001-1721pdt. Lane: SENSORY. Slot: big-lever.
Frozen prereg: PREREG_H1_CLOUDS_1721.md (2026-10-01 17:40 PDT).
Ordering evidence: prereg mtime 2026-10-02 00:32:26 UTC predates every
H1 implementation artifact (h1_variant.zag 00:34:32, bin/h1_variant
00:34:37, h1_verify.zag 00:39:08, bin/h1_verify 00:39:14).
Toolchain: safebin only, znc pinned, sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
Zero Python invocations this wave (NAMECHECK Step 0/0b).

## Baseline gates (prereg-ordered)

(a) One-line diff: diff of r11_baseline.zag against
docs/lab/imagination_discovery/img/r11_alien.zag shows exactly one
differing line (the @import repoint to ./sub/R33_NATIVE_IO_V1.zag).
PASS.
(b) Two 1024 baseline renders byte-identical:
out/base1/r11_alien_1024.bmp and out/base2/r11_alien_1024.bmp both
sha256 72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b.
PASS.
(c) Geometric validator on the rebuilt baseline (prior worker's
h1_verify.zag, adopted after audit: b_trace, b_moonhit, b_hbase, b_fbm2
function bodies byte-identical to the baseline by md5; bar thresholds
match the prereg exactly): SKYWIN_KEPT 48 (>=36), SUNHALF 25 / ANTISUN
23 (>=12 each), TERRAIN_KEPT 64 (>=56), MOON_KEPT 16 (>=12),
FULLSKY_KEPT 144 (>=100). Moon screen center computed from the frozen
camera math: (877, 116). VALIDATOR: PASS.

## Kill bars (measured on final 1024 BMPs, base1 vs var1)

KB1-DET: three 1024 renders of the H1 variant are byte-identical:
eaa71a18ccb657d0260a6d4ab7e534d180c7d79d16b54f3eb65aa5816b1cb7cf
(var1, var2, var3; shas in evidence/sha_var1.txt, evidence/sha_var2.txt,
evidence/sha_var3.txt). PASS.
KB2-COVERAGE: 0.2916, inside [0.08, 0.60]. PASS.
KB3-LIGHTLOGIC: mean dL SUNHALF +1.52, mean dL ANTISUN +3.65,
difference -2.13. Bar requires difference >= 6.0 AND sun mean >= 3.0.
FAIL. This is the killing bar.
KB4-STRUCTURE: variance of dL over SKYWIN 64.33 >= 40.0. PASS.
KB5-NONREG-TERRAIN: mean |dL| 0.65 <= 1.0. PASS.
KB6-NONREG-MOON: mean |dL| 0.00 <= 1.0. PASS.
KB7-SKYCALM: |mean dL| 0.00 <= 5.0; fraction |dL|>12 is 0.1388 <= 0.35.
PASS.
KB8-ANTIGRAIN: acutance ratio variant/baseline 1.036 <= 1.15. PASS.
KB9-COST: variant 1024 wall 527.3 s (var2) vs baseline 1024 wall 590 s
(base2), ratio 0.89x <= 4.0x. PASS. (var1 took 969.6 s because it ran
under heavy CPU contention beside base1; the var2/base2 pair ran under
matched contention. Ratio passes under every pairing: 969.6/590 = 1.64
at worst.)
H1-OCT5 probe: NOT RUN. Prereg condition (a 1024 render completing in
under 600 s wall) was not met: var1 took 969.6 s.

Control: baseline-vs-baseline (base1 vs base2) through the same
verifier gives dL = 0.00 on every bar (KB8 ratio 1.000), confirming the
dL pipeline is clean and the KB3 numbers on the variant are real
signal, not measurement noise.

## Killing evidence

evidence/killbars_run1.log (full bar table), evidence/validator_baseline.log,
out/var1/h1_variant_1024.png and out/base1/r11_alien_1024.png (1024 PNGs
for the eye), evidence/sha_var1.txt, evidence/sha_base12.txt.

## Knowledge vs architecture (red-team clause)

The failure is mechanism geometry, not a code bug. The frozen block
marches the 2-tap self-shadow along the world sun azimuth
(-0.628, -0.778) applied directly in (px, pz) projective field space,
where px = dx/(dy+0.18)*1.4. That projection warps direction, so the
march direction is misaligned with the true sun direction across the
frame. Measured consequence: on the sun side, sight rays traverse
denser field toward the assumed-sun direction, so the self-shadow term
sh is systematically lower exactly where the light should be strongest,
darkening the sun side relative to the baseline's already-bright flat
cirrus; the silver lining (thin coverage band, sunAmt > 0.55) does not
compensate. Net: anti-sun dL (+3.65) exceeds sun-side dL (+1.52), the
wrong sign against the +6.0 bar. No constant was tuned and none will
be; the bar stands as frozen. Lesson for the next cloud attempt: a
sun march must transport the sun vector through the projection instead
of reusing the world azimuth in field space, and the self-shadow term
must be checked for sign against the baseline it replaces, not just
against clear sky.

## Verdict

H1 LIT CLOUD DECK is DISCARDED on frozen KB3-LIGHTLOGIC. It is not
queued, no sealed blind pair is prepared, h1/blind/ remains empty, and
nothing is surfaced to Micah. The 7 passing bars are recorded as
measured; they do not override the kill.
