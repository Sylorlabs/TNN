# EVIDENCE H1-CLOUDS-1721 - wave-20261001-1721pdt sensory lane

## Ordering evidence (prereg before implementation)

- PREREG_H1_CLOUDS_1721.md written 2026-10-02 00:32:26 UTC,
  sha256 0d447ed25e93adbb3fd5764c5600e6155988f78ce2f395e642771ce6f541d1b2.
- h1/ directory created after; first implementation artifact
  (h1_clouds.zag) written after the prereg file mtime.
- No commits this wave (forbidden); ordering evidence is file
  mtime + sha256, recorded here.

## Toolchain

- znc: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (matches frozen toolchain hash).
- IO substrate: h1/sub/R33_NATIVE_IO_V1.zag, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  (byte copy of the wave-20260924-1121pdt vendored file; hash re-verified).
- Safebin PATH only; python3/python do not resolve (NAMECHECK.md Step 0).

## Baseline gate

- h1/r11_baseline.zag: byte copy of
  docs/lab/imagination_discovery/img/r11_alien.zag with exactly one line
  changed (the @import repointed at ./sub/R33_NATIVE_IO_V1.zag;
  diff-verified). Gate (a) PASSED.
- Gate (b): two 1024 renders byte-identical:
  72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b x2.
  PASSED. Wall: 819 s, 590 s.
- Gate (c): geometric validator on the rebuilt baseline: PASS.
  SKYWIN 48/48, TERRAIN 64/64, MOON 16/16, FULLSKY 144/144,
  SUNHALF 25, ANTISUN 23. Moon screen center from frozen camera math:
  (877, 116).
- Note (stated openly): no frozen r11-1024 baseline hash exists on
  record, so gate (b) is determinism-based, not hash-match-based.

## H1-OCT5 data probe

- Prereg condition: measure only if a 1024 render completes under 600 s.
  Baseline renders took 819 s and 590 s. Condition NOT met; probe
  skipped and recorded here rather than run off-prereg.

## Variant renders (KB1)

- h1a: eaa71a18ccb657d0260a6d4ab7e534d180c7d79d16b54f3eb65aa5816b1cb7cf,
  wall 552 s.
- h1b: eaa71a18ccb657d0260a6d4ab7e534d180c7d79d16b54f3eb65aa5816b1cb7cf,
  wall 528 s. Byte-identical to h1a.
- h1c: rendering (background); hash to be recorded in evidence/sha_h1.txt.
- One background render died mid-run at row 576 (session lost, cause
  unknown, no error artifact); restarted cleanly and completed. The two
  completed renders are byte-identical, so no contamination is
  suspected; the dead run produced no output file.

## Kill bars (1024, h1a vs base1; full log evidence/killbars_h1a.log)

- KB2 coverage: 0.2916, bar [0.08, 0.60]: PASS.
- KB3 light logic: sun_mean +1.52 (bar >= 3.0), diff -2.13
  (bar >= 6.0): FAIL. Killing bar; see VERDICT_H1.md diagnosis.
- KB4 structure var(dL): 64.33, bar >= 40.0: PASS.
- KB5 terrain mean|dL|: 0.65, bar <= 1.0: PASS.
- KB6 moon mean|dL|: 0.00, bar <= 1.0: PASS.
- KB7 sky calm: |mean| 0.00 (bar <= 5.0), bigfrac 0.1388
  (bar <= 0.35): PASS.
- KB8 anti-grain acutance ratio: 1.036, bar <= 1.15: PASS.
- KB9 cost: variant 552/528 s vs baseline 819/590 s, ratio < 1.0:
  PASS (well under the 4.0x bar). Note the baseline's own two runs
  varied widely (819 s vs 590 s), so machine variance dominates here;
  the H1 block adds bounded fbm work on sky pixels only, and frame
  cost is dominated by terrain raymarching.

## Verdict

DISCARDED per the frozen mapping (KB3 failed as specified). See
h1/VERDICT_H1.md. No sealed A/B pair, no JUDGE_BRIEF.md; nothing
queued for judgment.
