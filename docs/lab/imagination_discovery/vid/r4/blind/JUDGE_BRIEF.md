# Blind Judging Package — D-VID-1 Round 4

## Brief for the judge

You are judging an alien ocean render. The baseline (R3) was judged
"doesn't look realistic — it looks Minecraft" (2026-09-22). The candidate
(R4) applies eight mechanism variants to kill the blocky read.

**Your task:** Score the CANDIDATE images below. Do not try to guess which
mechanism is which; judge what you see.

## Images

- `candidate_full.png` — full frame (512² preview of 1024² render)
- `candidate_fg.png` — foreground crop (near-camera water, 2×)
- `candidate_mid.png` — mid-field crop (2×)
- `candidate_spire.png` — spire/waterline crop (2×)

## Scores (1–10 each)

1. **Blockiness:** Does the water look like rectangular tiles/blocks?
   (1 = obvious Minecraft tiles, 10 = no block structure at all)
2. **Realism:** Does it look like real water / could it pass as a photo?
   (1 = obvious CG, 10 = indistinguishable from real vision)
3. **Foam naturalness:** Does the foam look like real sea foam?
   (1 = artificial speckle/dashes, 10 = natural foam)

## Mechanism attribution

The candidate combines these LOGIC-DERIVED mechanisms (no cosmetic ones
survived to the final):
- Mg: per-pixel shading from interpolated surface (kills march banding)
- Ma: micro-chop normal detail (capillary waves)
- Mb: fine foam breakup (lace, not blocks)
- Mc: spire waterline spume breakup
- Md: capillary specular jitter
- Mh: spire cone-normal shading
- Mq: fractional world coords for noise (kills near-field quantization)
- Mb5: mid-field coarse foam patches

**Question:** Which mechanisms, in your judgment, are responsible for
killing the blocky read? Are they the logic-derived ones above, or would
you attribute it to something else?

## Verdict

- Does the candidate kill the "Minecraft" verdict? (yes/no)
- What remains artificial?
