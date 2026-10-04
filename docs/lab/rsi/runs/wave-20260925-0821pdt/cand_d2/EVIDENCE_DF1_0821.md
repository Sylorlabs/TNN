# EVIDENCE DF-1 - wave-20260925-0821pdt, cand_d2

Implementation worker report (Phase 2). The frozen prereg
docs/lab/rsi/runs/wave-20260925-0821pdt/cand_d2/PREREG_D2_0821.md was
committed alone at 0d977b976 before any DF-1 source, verifier, scratch,
or render existed. Commit order is clean: prereg strictly precedes
implementation. This worker wrote no commits; only the coordinator
commits.

## Provenance header (machine-checkable)

RENDER_SHA: 6155ae844814167eb9e41d79e41806e8859354a10f6e615ef6f6658d0cda2e50
FIRST_RENDERED_WAVE: wave-20260925-0821pdt
COMPONENT_LINEAGE: r8c_alien.zag(committed,395663d4; baseline BMP e4f65557); R9:QUEUED-UNJUDGED (2026-09-23, not stacked, plain baseline used); C1:QUEUED-UNJUDGED (2026-09-23); C2v3:QUEUED-UNJUDGED (2026-09-23); S11-IMG:QUEUED-UNJUDGED (2026-09-23); C12:QUEUED-UNJUDGED (2026-09-23); S11-AUD:QUEUED-UNJUDGED (2026-09-23); S13:QUEUED-UNJUDGED (2026-09-24); S14:QUEUED-UNJUDGED (2026-09-24); whirlpool-planform:QUEUED-UNJUDGED (2026-09-24); D19:DISCARDED (wave-20260924-0521pdt, opposite mechanism, not stacked); ST-1:UNVERIFIABLE (wave-20260925-0521pdt, audio lane, untouched); E3:REJECTED by Micah 2026-09-23; G1:STAND-DOWN; D-VID-1 V3:DEAD (wave-20260925-0221pdt, video lane, stands down)
NEW_KNOWLEDGE_CLAIM: A frozen-radius separable integer box blur applied only to the r8c foreground tier with a 12 px feather at the plain horizon gives the render a lens depth of field (near field defocused, giant and focus plane bit-identical) at negligible cost.
Tag: [NEW]. This is not a re-certification. No pending queue item is
re-surfaced or re-presented here; they are listed only as lineage so
the judge queue stays honest.

## Artifact inventory (all under cand_d2/, uncommitted)

- R33_NATIVE_IO_V1.zag: vendored IO substrate, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  (byte-identical to the frozen freelunch/sub copy).
- r8c_alien_dry.zag: byte copy of docs/lab/imagination_discovery/img/r8c_alien.zag
  (sha256 395663d473b8f1190181300e307f224d0d256ec002ed435d03603cfb4d3c4452)
  with ONLY the @import line repointed (line 46); diff against the
  baseline shows exactly one changed line.
- r8c_alien_df1.zag: dry source plus the frozen mechanism. Diff dry->df1 is
  a pure addition of 121 lines: the new pass block (r8c_df1_w12 mask fn,
  r8c_pass6_defocus) inserted after r8c_pass5, plus the two call-site lines
  after the r8c_pass5 call in main (before the trace is closed, so the
  DF-1 decision lines land in the trace). Passes 1-5 are byte-identical.
- df1_pass_block.txt: the authored pass block, kept as the splice source.
- df1_geom.zag: geometry functions extracted VERBATIM from the baseline
  source (lines 95-146 and 304-313, diff-verified); used by the verifier
  to recompute the frozen mask independently.
- df1_verify.zag / bin/bin_verify: pure-Zag verifier for KB2, KB3, KB4, KB7.
- df1_probe.zag / bin/bin_probe: pure-Zag diagnostic probe for the KB4 miss.
- bin/bin_dry, bin/bin_df1: binaries built with the pinned toolchain.
- out/dry_baseline.bmp: the gated dry rebuild.
- out/df1_1.bmp, out/df1_2.bmp, out/df1_3.bmp: three variant renders.
- out/dry_trace.md, out/df1_trace_1..3.md, out/verify_out.txt, out/df1_stdout_1..3.txt.

Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
verified with sha256sum before every compile in this session.

## Dry rebuild gate (re-verified this implementation)

bin_dry rendered out/dry_baseline.bmp in 959 ms with sha256
e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
byte-identical to the committed r8c baseline (S14 record) and to the
prereg's frozen gate value. The gate holds; work proceeded.

## Implementation (frozen mechanism, exactly as preregistered)

r8c_pass6_defocus runs after pass5 finish and before the BMP write:

- Mask: w12(x,y) from the frozen substrate functions r8c_plain_y and
  r8c_arch_open. w12 = 0 for y <= py (sky, range, giant, moon, focus
  plane); w12 = 12 for y >= py + 12 (full defocus); w12 = y - py in the
  12 px feather band; w12 = 0 inside the arch opening (far rim stays
  sharp).
- Blur: separable integer box blur, R = 7 (15x15), over a scratch buffer.
  Horizontal pass then vertical pass, sums in i64, each 1D pass divides
  by 15 with rounding (add 7 before divide).
- Blend: out = (sharp * (12 - w12) + blurred * w12 + 6) / 12 per channel.
  Pixels with w12 == 0 are never written.
- Trace decision lines (from out/df1_trace_1.md):
  DF1: blur-zone pixel count=257803
  DF1: carve-out pixel count=5229
  The verifier recomputed both counts from the verbatim geometry and got
  257803 and 5229 exactly: mask_blur_n=257803, mask_carve_n=5229.
- No RNG, no new samples, no clock, no outside input. Deterministic by
  construction.

## Kill bar readings

KB1 determinism: PASS. Three variant renders byte-identical:
6155ae844814167eb9e41d79e41806e8859354a10f6e615ef6f6658d0cda2e50
x3. Render wall times 1363 ms, 1856 ms, 1741 ms.

KB2 background integrity: PASS. Verifier diffed the full frame against
the dry baseline with the independently recomputed mask:
KB2_outside_mask_diff_px=0 over KB2_sharp_px_checked=790773 w12==0
pixels. Sky, giant, moon, focus plane, and arch opening are
bit-identical to baseline.

KB3 defocus efficacy: PASS. Over the w12==12 zone (KB3_zone_n=246539):
mean |variant - baseline| luma = 6.594 levels (>= 1.5 required;
KB3_mean_diff_milli=6594). Neighbor-difference HF power ratio
variant/baseline = 0.002 (<= 0.7 required; KB3_hf_ratio_milli=2,
KB3_hf_power_base=57647182, KB3_hf_power_var=151875, KB3_hf_n=245104).
The blur is measurable and crushes high-frequency content; not a no-op.

KB4 E3 grain guard: FAIL. KB4_max_luma_diff=48 (bar: <= 24 everywhere);
KB4_max_ch_diff=55. Killing evidence below.

KB5 purity: PASS. Pinned znc hash 498abcb5... verified before every
compile. Zero Python contact: no .py files anywhere under cand_d2/,
and the session used only shell coreutils, git, sha256sum, the pinned
znc, and the compiled Zag binaries (command log in
shell_history_0821.txt). Token grep (case-insensitive) for
rand/srand/random/time/clock over the authored sources
(df1_pass_block.txt, df1_verify.zag, df1_probe.zag, df1_geom.zag)
returns 0 hits. The vendored copies (r8c_alien_dry.zag,
r8c_alien_df1.zag, R33_NATIVE_IO_V1.zag) inherit the baseline's own
purity comments mentioning "clock" (lines 19/353 of the baseline) and
the substrate's "No Python" line 17; they are covered by their pinned
hashes (395663d4..., e6379ddb...), D19 precedent.

KB6 cost: PASS. Variant render wall times 1363 ms, 1856 ms, 1741 ms,
all <= 2000 ms (dry baseline 959 ms this session).

KB7 anti-halo: PASS. The verifier reimplemented the separable box blur
independently on the baseline BMP and checked every feather-band pixel
(0 < w12 < 12): KB7_feather_checks=33792, KB7_overshoot_px=0. Every
final channel lies between its sharp and fully-blurred endpoints; the
blend is a true convex combination with no seam overshoot.

## KB4 killing evidence

The bar requires |variant - baseline| <= 24 luma levels for every pixel
in the frame. The variant shifts one pixel by 48 luma levels (55 in a
single channel), so the bar fails as frozen.

The pure-Zag probe (df1_probe.zag) localized the miss:

- gt24_count=203 of 1048576 pixels (0.019%).
- Bounding box: x 249..267, y 790..887. The max-diff pixel is (258,806)
  with diff 48.
- 166 of the 203 lie inside the arch body rects (left pillar:
  x 256..288, y 786..900); all 203 lie in the stone band (y 786..986).
- Luma-diff histogram over the frame: 0..8: 959991; 9..16: 87714;
  17..24: 668; 25..32: 146; 33..48: 57; 49+: 0.

Interpretation: the 203 hot pixels sit exactly on the hardest edge in
the blur zone, the lit edge of the left arch pillar against the dark
field. A genuine R=7 defocus across a ~100-level step must move edge
pixels toward the neighborhood mean by up to roughly half the step;
48 luma levels there is the mechanism behaving as a lens would, not
pathological amplification (nothing reaches 49, the tail is tiny and
fully localized, and KB7 proves the blend never overshoots). The frozen
KB4 bar was written on the premise that a blur only ever nudges pixels
by small amounts; on this substrate's hard foreground edges that
premise is false for any real R=7 blur. The bar cannot be satisfied
without weakening it (forbidden) or shrinking R (not the frozen
mechanism). The candidate dies on its own bar, honestly.

## Red-team structured self-review

This worker runs at depth 2/2 and cannot spawn an independent
red-team reviewer. What follows is a structured adversarial
self-review, disclosed as non-independent.

1. Knowledge vs architecture. The KB4 miss is neither a code bug nor a
   wrong depth story. Cross-checks rule out implementation error: the
   verifier's independently recomputed mask counts match the generator
   trace exactly (257803/5229), KB2 shows zero writes outside the mask,
   and KB7's independent blur reimplementation shows a clean convex
   blend with zero overshoot across 33792 feather checks. The miss is
   bar-vs-physics: the frozen KB4 bound (<= 24 everywhere) is
   incompatible with any genuine radius-7 defocus on a substrate whose
   foreground contains ~100-level hard edges. No knowledge claim is
   salvaged by re-framing; the mechanism did what the prereg said it
   would do.

2. Metric gaming. No constant was tuned after seeing results: R=7 and
   the 12 px feather are the frozen values, implemented before the
   first render. KB3's zone-interior HF definition follows the frozen
   spec verbatim. KB4 was measured on luma because the bar says "luma
   levels"; the per-channel max (55) was also reported, and it also
   exceeds 24, so the luma-vs-channel reading does not change the
   verdict. Nothing was re-run until it passed: the first verifier run
   is the reported run.

3. Weak bars, stated plainly. KB6 (2.0 s) passed with the worst run at
   1.856 s; KB3 passed by 4x on efficacy and ~350x on the HF ratio;
   KB2 and KB7 passed with zero violations. The bars that passed were
   not close calls, and the one that failed was failed by the
   mechanism's honest behavior, which is exactly what a kill bar is
   for. No bar was near a boundary in a way that would reward
   re-interpretation, and none was re-interpreted.

4. Lineage honesty. Tag [NEW] stands: grep over docs/lab and every run
   dir found zero prior art for defocus/blur/bokeh (per the prereg
   survey), and this is the first render of DF-1. It dies on KB4 in its
   first wave; nothing is recycled, nothing is re-presented.

5. Residual risk the bars do not cover. The blind-judge question the
   bars cannot answer, whether a defocused near field actually reads
   as more real to Micah's eyes, is moot: the candidate is DEAD on KB4
   and no pair is queued.

## Verdict: DEAD

Per the frozen verdict mapping, one failed bar maps to DEAD with
killing evidence. Killing bar: KB4 (max luma shift 48 > 24, localized
on the arch pillar edge; probe evidence above). The candidate is not
adopted, not queued, and no sealed blind pair was prepared.

## Sealed pair

NOT prepared. The frozen sealing plan permits a pair only on a clean
pass of every bar. KB4 failed, so no baseline/variant BMPs were copied
under blind/ and no mapping file was written.

## Purity attestation

Pure Zag throughout: generator, verifier, probe, analysis, and /tmp
scratch (none used). Shell coreutils, git, sha256sum, and the pinned
znc only for orchestration. Zero Python contact with any wave
artifact. Token greps clean as reported under KB5. No em-dashes in
this file (checked with grep before writing completed). Nothing was
committed, merged, pushed, reset, or rebased by this worker. Google
Drive untouched.
