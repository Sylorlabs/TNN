# CLAIM COMPARISON WORKSHEETS — human claims enumerated from sealed H-* files.
# TNN claims to be filled from T-* outputs after runs complete.
# Verdicts: MATCH / MISS (withheld) / HALLUCINATION (false positive).

## A1 thunderstorm (H-A1)
| # | Human claim | TNN claim | Verdict |
|---|-------------|-----------|---------|
| A1.1 | Two loud broadband burst events (~0.8-3s, ~15-17.5s) | "102 distinct transient events" (bursts shredded into 20ms-scale triggers) | MISS (no burst-level grouping; 2 events -> 102) |
| A1.2 | Continuous lower-level broadband bed throughout | "LAYERS transient events over a noise-like bed" | MATCH |
| A1.3 | Energy concentrated at low frequencies (<~1kHz) | band_low 0.513 but "SPECTRUM broadband..." (0.55 threshold) | WEAK MISS (plurality low, sentence coarse) |
| A1.4 | NO tonal/pitched content | "no stable pitch detected; inharmonic or noise-like (pitch structure withheld)" | MATCH (correctly withheld) |
| A1.5 | NO regular repetition (bursts irregular) | "ONSETS occur at irregular intervals" | MATCH |
| A1.6 | Large dynamic swings (~20-30dB burst vs bed) | dyn_ratio 5379 "large swings: loud events rise far above a quiet bed" | MATCH |
| A1.7 | Two layers: bursts over noisy bed | "transient events over a noise-like bed" | MATCH (coarse) |
| A1.X1 | (no human claim; TNN extra) "RHYTHM amplitude repeats on a cycle of about 0.100 seconds" | no rhythmic structure in human analysis | HALLUCINATION (lag-2 envelope-autocorr artifact) |

## A2 bell buoy (H-A2)
| # | Human claim | TNN claim | Verdict |
|---|-------------|-----------|---------|
| A2.1 | Bell strike groups at ~6,~16,~26,~35,~44s (~9-10s spacing) | "40 distinct transient events... irregular intervals" (intra-strike triggers dominate IOI) | MISS (group-level ~10s regularity invisible) |
| A2.2 | Most groups are double strikes ~1s apart; ~16s single | not reported | MISS (withheld) |
| A2.3 | Sharp attack, long ~8-10s decay per strike | "large swings" MATCH on dynamics; decay shape not described | PARTIAL (dynamics MATCH, decay MISS) |
| A2.4 | Rich partials to 8kHz, inharmonic (metallic) | "SPECTRUM energy concentrated below ~400 Hz" (band_low 0.73); peaks_med 1 | MISS (high partials at attacks unreported; coarse 250Hz bins) |
| A2.5 | Quiet water/wave bed between strikes | never mentioned; bed called "tonal" | MISS (withheld) |
| A2.6 | Strike groups repeat regularly (~9-10s); pitch steady, no glide | "PITCH stable, no strong overall glide" MATCH on glide; "~10s group period" missed (env autocorr maxlag 0.5s) | PARTIAL (glide MATCH, period MISS = method limit) |
| A2.7 | Two layers: bell + water | "LAYERS a tonal bed with irregular transient events over it" (inverts: bell strikes ARE the tonal events, water bed unmentioned) | MISS (layer split does not match true sources) |
| A2.X1 | (no human claim; TNN extra) "RHYTHM amplitude repeats on a cycle of about 0.100 seconds" | no such rhythm | HALLUCINATION (lag-2 artifact) |
| A2.X2 | (human: strikes decay) "PITCH predominantly tonal: a sustained pitched component near 246.1 Hz" | strikes decay over ~10s, not sustained | WEAK MISS ("sustained" overstates; 246 Hz plausible low partial) |

## A3 crickets (H-A3)
| # | Human claim | TNN claim | Verdict |
|---|-------------|-----------|---------|
| A3.1 | One high-pitched band ~4-4.8kHz, ~6.5s to ~39s | "pitched component near 2285.7 Hz" (method ceiling 4kHz; subharmonic alias of true ~4.4kHz band, near real ~2kHz secondary band) | MISS (band center wrong; honest method-ceiling boundary) |
| A3.2 | Strong amplitude modulation: rapid pulses ~3-5/s | "RHYTHM amplitude repeats on a cycle of about 0.300 seconds" (3.3Hz) | MATCH |
| A3.3 | Weaker energy ~2kHz and ~8kHz (harmonics) | not mentioned | MISS (withheld) |
| A3.4 | Steady level middle ~25s; gradual fade in/out | "large swings: loud events rise far above a quiet bed" (true range, but "events" misframes continuous chorus) | MISS (framing wrong; fades unreported) |
| A3.5 | Single dominant process; no separate transients | "179 distinct transient events" + "tonal bed with irregular transient events over it" (chirp pulses double-counted as separate layer) | HALLUCINATION (no separate transient layer exists) |
| A3.6 | No pitch glide | "PITCH stable, no strong overall glide" | MATCH |

## I1 frost (H-I1)
| # | Human claim | TNN claim | Verdict |
|---|-------------|-----------|---------|
| I1.1 | Branching fern-like dendritic crystals, white/clear, most of frame | "4 distinct color regions; largest 43%"; edges mixed/diagonal | MISS (no dendritic/branching concept; region count is coarse) |
| I1.2 | Dark near-black background in gaps, esp. corners/edges | "TONE mid-tone" (mean 71.6/255); no mention of dark background | MISS (withheld) |
| I1.3 | Fine intricate texture everywhere; no large smooth areas | "TEXTURE mostly smooth surfaces, little fine detail" | HALLUCINATION (claims smooth; fine crystal detail lost at 80x45 analysis scale) |
| I1.4 | Branching in MANY directions; no dominant orientation | "EDGES run in mixed/diagonal directions, no single dominant orientation" | MATCH |
| I1.5 | Denser/brighter crystal mass toward center-left | centroid_x 0.435 but "visual mass centered horizontally" | MISS (withheld; number leans left, sentence does not claim it) |
| I1.6 | Very high contrast; essentially monochrome white-on-black | no COLOR sentence (sat low); no high-contrast sentence (std 46<60) | MISS (withheld monochrome + contrast) |

## I2 terraces (H-I2)
| # | Human claim | TNN claim | Verdict |
|---|-------------|-----------|---------|
| I2.1 | Many thin CURVED contour bands following slopes, patchwork | "7 distinct color regions; largest 50%"; "EDGES run mostly horizontal" | MISS (no curvature concept; horizontal edges partly true of contours) |
| I2.2 | Varied greens/yellows/tans/browns; some pale blue-gray bands | "COLOR vivid, strongly saturated colors" | MATCH (vivid/varied; coarse, no hue names by design) |
| I2.3 | Winding river lower-left/center | not mentioned | MISS (withheld; no object concepts) |
| I2.4 | Small clusters of tiny rectangular buildings scattered | not mentioned | MISS (withheld; no object concepts) |
| I2.5 | Curvilinear everywhere; no straight lines/rectangles | "EDGES run mostly horizontal" | MISS (orientation stat cannot express curvature) |
| I2.6 | Highly detailed/textured; no large uniform areas | "TEXTURE mostly smooth surfaces, little fine detail" | HALLUCINATION (claims smooth; terrace detail lost at 80x45 scale) |

## V1 waves (H-V1)
| # | Human claim | TNN claim | Verdict |
|---|-------------|-----------|---------|
| V1.1 | Static dark foreground: railing-like bars (verticals + top/bottom horizontals) | not mentioned (no region/object description in video mode) | MISS (withheld) |
| V1.2 | Blue-green water surface visible through frame, middle band | not mentioned | MISS (withheld) |
| V1.3 | Water in continuous motion (waves); no cuts; one shot | "no abrupt scene cuts; one continuous shot" MATCH; "little consistent motion... near-static or chaotic" MISSES the wave motion | PARTIAL: cut claim MATCH, motion MISS |
| V1.4 | Motion is water texture, not frame | not separated | MISS (withheld) |
| V1.5 | Direction of wave travel WITHHELD (not resolved) | "little consistent frame-to-frame motion" (withholds direction) | MATCH (both withhold) |
| V1.6 | Overall brightness stable | "the scene brightens over time" (29.2->32.1) | WEAK MISS (numbers show mild rise; human judged it negligible) |
