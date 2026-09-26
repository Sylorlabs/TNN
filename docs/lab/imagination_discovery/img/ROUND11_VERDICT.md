# Round 11 — VERDICT

Date: 2026-09-26. Branch target: `tnn-native-lab`. Pure Zag, zero RNG.
Champion test: R11 (dusk, hemisphere ambient T14) vs R4 (standing champion, bright day).

## Verdict: R11 TAKES THE CHAMPIONSHIP

R11 is a genuine perceptual improvement over R4. T14 fixed the defect it
was built to fix — the shadowed foreground no longer reads as void — and
nothing in the sunlit look, sky, or moon moved. Judged as a picture with
normal vision, full frame (1024×1024), both images viewed whole.

## What got better (r4 → r11)

- Sky: r4's flat blue day sky vs r11's gradient dusk with pink dust-glow
  clouds at the horizon ring. More atmospheric, more light logic.
- Moon/crescent: r4's big planet is vivid but stylized; r11's dark planet
  with the deliberated 19%-lit crescent reads physically — lit limb,
  dark limb, no pastel wash (the rejected gamma-2.0 fork would have
  collapsed this; r11 keeps it).
- Mountains: r4's range is spiky and cutout-flat; r11's read as distant
  silhouettes with rim light from the dusk sun. Depth reads.
- Foreground (the T14 target): r8b's bottom-35% band mean luminance 27.78,
  void-dark; r11's 34.13 (~+23%), rock forms and hillside shading visible.
  Not "re-lit" — it reads as ambient-lit, consistent with the scene.
  (Numbers are secondary; the eyes confirm the band went from void to
  readable.)
- Mood: r11's dusk scene has coherent alien atmosphere; r4 is a bright
  procedural diorama. As concept art, r11 is the stronger image.
- Nothing regressed in the sky/moon/mountains/lake between r8b and r11 —
  same-scene before/after confirms the change was confined to the dusk
  fill, as designed.

## What got worse / stayed behind

- Absolute foreground detail: r4's boulder field (day scene, band mean
  80.93) is still more readable than r11's dim dusk foreground (34.13).
  R11's foreground is no longer void, but it remains a dark zone.
- Overall brightness/punch: r4 pops; r11 is deliberately dark. A viewer
  wanting a bright scene still prefers r4's scene, not its rendering.

## Caveat (recorded openly)

r4 and r11 are different scenes (day vs dusk), so this is not a
same-scene relit comparison — it compares the rendering machinery's
output quality. The same-scene T14 before/after (r8b → r11, bottom-35%
defect) is included as supporting evidence that the claimed fix is real
and confined.

## Judging method

Full-eyes: the complete 1024×1024 r11 render and the 1024×1024 r4
champion were each inspected whole (no thumbnails, no crops), plus the
r8b same-scene parent. Normal vision, no horror-biased defaults.
Secondary numbers (band luminance) recorded after the eye call, never
as the decision.

## Determinism

- Source: `r11_alien.zag` (in this dir), built with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (`znc r11_alien.zag --no-zagd --no-analyze`), import layout mirrored in
  a scratch dir (this znc resolves `@import` relative to the source
  file's directory).
- Original render (2026-09-26 05:28): SHA-256
  `72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b`
- Fresh rerun (2026-09-26): SHA-256
  `72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b`
- Result: BYTE-IDENTICAL. Determinism holds.

## Delivery

- `~/workspace/your_files/image_r11/NEW_r11_alien_1024.png` — full-res R11
- `~/workspace/your_files/image_r11/NEW_r4_champion_1024.png` — full-res champion
- `~/workspace/your_files/image_r11/NEW_r11_vs_r4_champion_sidebyside_2048.png`
- `~/workspace/your_files/image_r11/NEW_r11_vs_r8b_T14_before_after_2048.png`
  (supporting: same-scene T14 before/after)

## Commit

Committed to `tnn-native-lab`: r11_alien.zag, VERDICT.md, ROUND11_REPORT.md,
plus 256px verdict-evidence renders. Binary (r11_alien, r11_alien_rerun),
`.zag-cache/`, and scratch build trees excluded per repo content standard.
Commit SHA: `<TBD>`
