# ELABORATION TRACE - r8c_alien (Fork C: mind's-eye elaboration)

This image is the residue of 269 deliberate decisions in five passes,
the way a mind's eye comes into focus: vague gist first, then big
decisions, then light logic, then hundreds of small attentional
fixations, then finish. This file was written by the program
r8c_alien.zag AS IT DECIDED - every line below corresponds to a
decision the program executed.

## Determinism, and where surprise comes from
Every decision is a pure function of (pass, index, canvas state).
No RNG, no clock, no outside input: the same run always writes
this exact file and this exact image. Yet fixation N+1's target is
chosen by READING THE CANVAS after fixation N - so the sequence
cannot be predicted without running the elaboration. Surprise
comes from feedback, not dice.

## World commitments (the world is invented first; pixels follow)
- ONE sun, low at the left horizon, below the frame. (-880,-260,+390)
- ONE wind, left-to-right, slightly toward the viewer. Cloud streaks,
  dust tails, dune ripples all obey it.
- The far tier is an ancient crater rim, breached right of center;
  a glacier of dust pours through the breach.
- A gas giant hangs upper right, half in shadow; it lends a faint
  teal secondary glow to the cloud undersides (same sun, second story).
- The foreground is a ventifact field: wind-carved sailstones, every
  dust tail pointing downwind. One wind-carved arch, lower-left third,
  with light coming through its opening.

## PASS 1 - GIST (the vague impression)
G1: first impression - a dusk vista, indigo-teal sky, the sun already
    below the left horizon. Nothing is decided except mood.
G2: three land tiers, still vague - a far violet mass, a warmer middle
    tier, a dark foreground. Edges deliberately soft.
G3: something huge hangs in the upper right sky. I do not know what
    yet - only that the sky needs weight there. A pale unresolved glow.
G4: the air is dusty; the far tier will sit behind air, not pasted on it.
G5: gist done - 576 large soft dabs, one wash. Everything is soft;
    nothing is decided except mood and masses.

## PASS 2 - BIG DECISIONS (the world gets specific)
D1 sun: I put the sun low and to the left, just below the horizon.
    From here on, every shadow must agree with it. (-880,-260,+390)
D2 sky: dusk indigo-teal, deeper overhead - the day is leaving upward.
D3 rim: the far tier is an ancient crater rim - a long escarpment
    bowing away at the edges, violet in the dusk.
D4 peak: one peak stands tallest, left of center - the eye needs
    an anchor.
D5 breach: the rim is breached right of center - a broad soft glacier
    of dust pours through the gap. Specific, committed.
D6 hills: a warmer, closer tier - rust-colored hills in front of the rim.
D7 plain: dark umber foreground - the ground I stand on.
D8 stones: the foreground is a ventifact field - wind-carved sailstones,
    each trailing dust downwind. Forty stones; every tail points the
    same way, because there is only one wind.
D9 arch: one wind-carved arch in the lower-left third - light comes
    through the opening. Something near, something to touch. I paint
    it as a dark silhouette: the dusk is behind it, not on it. The
    opening holds the hazed far rim, dimmed by the arch's own shadow;
    the low sun rims its left edges with warm light.
D10 giant: the huge thing in the sky is a gas giant - zones of teal
     and gold, half in shadow. It will catch the last sunlight and
     throw a faint teal glow on the cloud undersides.
D11 moon: a small cratered moon, high left - balancing the giant.
D12 clouds: thin cirrus, stretched along the wind, lit from below-left.
     The wind draws every streak; none crosses it.
D13 haze: dust in the air between the tiers - the far rim sits BEHIND
     atmosphere, not pasted onto it.
D14 focal: my eye lands on the lit shoulder of the great peak, just
     left of the dust breach, at (430,400). Detail will gather there.

## PASS 3 - LIGHT LOGIC (one sun, one wind)
L1: sun vector committed: (-880,-260,+390). One sun. No second light.
    Every shadow painted from here must agree with its azimuth.
L2: I imagine the relief first - rim, hills, plain, arch, stones -
    a 128x128 height grid the mind's eye holds before shading.
L3: normals from the relief. Faces toward the sun warm; faces away
    cool. Flat ground gets weak light - the sun is low, correctly.
L4: cast shadows - I march each ray back toward the sun; where the
    relief blocks it, shadow. The arch throws one long shadow right.
    Tier heights are capped (a cliff has a finite height) and the
    shadow map is softened - dusk shadows are broad, not pillars.
L5: the giant's terminator crosses its disc from the same sun; its
    night side keeps faint zone structure, never flat black.
L6: the giant lends a faint teal secondary glow to cloud undersides -
    a second light story, but it comes from the same sun.
L7: aerial perspective - each tier washed toward the dusty horizon
    color by its distance.
L8: light logic done. Every shadow now agrees with one sun, one wind.

## PASS 4 - FIXATIONS (the mind's eye looks around)
Each fixation: I scan the canvas for the most interesting unresolved
place (contrast x novelty x nearness to the focal anchor), look there,
and lay pigment for a stated reason. 240 fixations follow.

## G1 SUNSHAFTS - crepuscular shafts (new pass, after light logic)
G1.1: the light stops at the clouds in the substrate; in real dusk
    photographs the low sun throws visible shafts through cloud gaps.
G1.2: a frozen cloud-deck density field D(x,y), wind-stretched fbm
    seed 9131: shaft machinery only, never rendered as visible cloud.
G1.3: each sky pixel marches N steps screen-space toward the frozen
    D1 sun at (82,532); deterministic hash jitter (seeds 9132+k,
    9133+k) keeps the march from banding.
G1.4: transmittance T = mean(1024 - D) over the march; lift
    L = max(0, T-400)*90/624, so gaps glow and the deck stays.
G1.5: lift applied in sun color (255,172,112), clamped at 255;
    terrain skipped by construction (tier_at != 0).
G1.6: N=12 sky_px=325786
G1.7: ops: 1048576 density fbm evals, 3909432 march steps.
The interest map: contrast x novelty x nearness to the focal anchor.
Recomputed from the canvas every 20 fixations; visited places fade.
F0: (561,307) sky - deepen the blue hour overhead
F1: (493,435) far rim - strata lines on the old crater wall
F2: (166,149) sky - another cirrus streak, drawn along the wind
F3: (359,426) far rim - strata lines on the old crater wall
F4: (396,328) far rim - clarify the rim crest against the sky
F5: (332,374) far rim - strata lines on the old crater wall
F6: (375,487) far rim - strata lines on the old crater wall
F7: (777,370) gas giant - a bright zone swath on the giant
F8: (462,533) far rim - the far slope falls into dusk
F9: (299,437) far rim - the far slope falls into dusk
F10: (368,265) sky - another cirrus streak, drawn along the wind
F11: (303,295) sky - the sun's glow gathers below the horizon line
F12: (489,296) sky - another cirrus streak, drawn along the wind
F13: (628,403) sky - the sun's glow gathers below the horizon line
F14: (620,345) gas giant - a bright zone swath on the giant
F15: (242,434) far rim - the far slope falls into dusk
F16: (505,369) far rim - strata lines on the old crater wall
F17: (558,368) sky - another cirrus streak, drawn along the wind
F18: (436,175) sky - the sun's glow gathers below the horizon line
F19: (519,491) far rim - the far slope falls into dusk
-- interest map recomputed from the canvas after fixation 20 --
F20: (497,431) far rim - strata lines on the old crater wall
F21: (558,311) sky - deepen the blue hour overhead
F22: (376,432) far rim - clarify the rim crest against the sky
F23: (177,144) moon - a bright crater ray on the moon
F24: (399,330) far rim - clarify the rim crest against the sky
F25: (330,372) far rim - strata lines on the old crater wall
F26: (362,502) far rim - the far slope falls into dusk
F27: (462,534) far rim - strata lines on the old crater wall
F28: (295,434) far rim - clarify the rim crest against the sky
F29: (366,266) sky - the sun's glow gathers below the horizon line
F30: (311,309) sky - the sun's glow gathers below the horizon line
F31: (495,299) sky - the sun's glow gathers below the horizon line
F32: (618,400) sky - the sun's glow gathers below the horizon line
F33: (617,342) gas giant - turbulence in the zones
F34: (239,426) far rim - clarify the rim crest against the sky
F35: (561,369) sky - the sun's glow gathers below the horizon line
F36: (784,368) gas giant - a bright zone swath on the giant
F37: (526,496) far rim - strata lines on the old crater wall
F38: (501,364) far rim - clarify the rim crest against the sky
F39: (438,178) sky - the sun's glow gathers below the horizon line
-- interest map recomputed from the canvas after fixation 40 --
F40: (466,405) far rim - clarify the rim crest against the sky
F41: (362,426) far rim - clarify the rim crest against the sky
F42: (528,344) sky - the sun's glow gathers below the horizon line
F43: (399,328) far rim - clarify the rim crest against the sky
F44: (334,372) far rim - strata lines on the old crater wall
F45: (363,489) far rim - strata lines on the old crater wall
F46: (464,532) far rim - clarify the rim crest against the sky
F47: (304,438) far rim - strata lines on the old crater wall
F48: (569,275) gas giant - turbulence in the zones
F49: (360,270) sky - another cirrus streak, drawn along the wind
F50: (633,405) sky - another cirrus streak, drawn along the wind
F51: (185,139) moon - a bright crater ray on the moon
F52: (297,313) sky - another cirrus streak, drawn along the wind
F53: (617,329) gas giant - a bright zone swath on the giant
F54: (247,432) far rim - strata lines on the old crater wall
F55: (532,495) far rim - strata lines on the old crater wall
F56: (463,471) far rim - clarify the rim crest against the sky
F57: (816,338) gas giant - a bright zone swath on the giant
F58: (424,173) sky - the sun's glow gathers below the horizon line
F59: (555,424) far rim - strata lines on the old crater wall
-- interest map recomputed from the canvas after fixation 60 --
F60: (470,392) far rim - strata lines on the old crater wall
F61: (369,433) far rim - strata lines on the old crater wall
F62: (401,344) far rim - strata lines on the old crater wall
F63: (558,295) gas giant - turbulence in the zones
F64: (331,364) far rim - strata lines on the old crater wall
F65: (367,497) far rim - clarify the rim crest against the sky
F66: (466,537) far rim - strata lines on the old crater wall
F67: (625,328) gas giant - the limb darkens toward the edge
F68: (298,425) far rim - strata lines on the old crater wall
F69: (364,278) sky - the sun's glow gathers below the horizon line
F70: (496,312) sky - deepen the blue hour overhead
F71: (310,296) sky - the sun's glow gathers below the horizon line
F72: (185,152) sky - another cirrus streak, drawn along the wind
F73: (625,404) sky - the sun's glow gathers below the horizon line
F74: (239,441) far rim - clarify the rim crest against the sky
F75: (551,368) far rim - strata lines on the old crater wall
F76: (520,490) far rim - clarify the rim crest against the sky
F77: (471,469) far rim - strata lines on the old crater wall
F78: (430,176) sky - deepen the blue hour overhead
F79: (553,432) far rim - strata lines on the old crater wall
-- interest map recomputed from the canvas after fixation 80 --
F80: (458,400) far rim - strata lines on the old crater wall
F81: (359,441) far rim - clarify the rim crest against the sky
F82: (395,343) far rim - clarify the rim crest against the sky
F83: (522,336) sky - deepen the blue hour overhead
F84: (339,372) far rim - clarify the rim crest against the sky
F85: (369,501) far rim - clarify the rim crest against the sky
F86: (469,522) far rim - strata lines on the old crater wall
F87: (631,339) gas giant - the limb darkens toward the edge
F88: (305,439) far rim - clarify the rim crest against the sky
F89: (361,281) sky - the sun's glow gathers below the horizon line
F90: (557,271) gas giant - turbulence in the zones
F91: (173,148) sky - another cirrus streak, drawn along the wind
F92: (299,303) sky - another cirrus streak, drawn along the wind
F93: (627,398) sky - another cirrus streak, drawn along the wind
F94: (242,427) far rim - strata lines on the old crater wall
F95: (530,487) far rim - clarify the rim crest against the sky
F96: (469,468) far rim - clarify the rim crest against the sky
F97: (430,169) sky - another cirrus streak, drawn along the wind
F98: (559,436) far rim - strata lines on the old crater wall
F99: (391,558) far rim - the far slope falls into dusk
-- interest map recomputed from the canvas after fixation 100 --
F100: (470,392) far rim - clarify the rim crest against the sky
F101: (359,436) far rim - clarify the rim crest against the sky
F102: (405,336) far rim - strata lines on the old crater wall
F103: (558,302) sky - deepen the blue hour overhead
F104: (345,370) far rim - clarify the rim crest against the sky
F105: (363,496) far rim - strata lines on the old crater wall
F106: (464,521) far rim - strata lines on the old crater wall
F107: (633,342) gas giant - turbulence in the zones
F108: (296,426) far rim - clarify the rim crest against the sky
F109: (363,267) sky - the sun's glow gathers below the horizon line
F110: (504,305) sky - another cirrus streak, drawn along the wind
F111: (310,304) sky - deepen the blue hour overhead
F112: (618,392) sky - the sun's glow gathers below the horizon line
F113: (179,146) sky - deepen the blue hour overhead
F114: (238,434) far rim - strata lines on the old crater wall
F115: (563,369) sky - the sun's glow gathers below the horizon line
F116: (521,505) far rim - strata lines on the old crater wall
F117: (462,460) far rim - strata lines on the old crater wall
F118: (423,181) sky - another cirrus streak, drawn along the wind
F119: (403,565) far rim - clarify the rim crest against the sky
-- interest map recomputed from the canvas after fixation 120 --
F120: (459,393) far rim - clarify the rim crest against the sky
F121: (374,439) far rim - clarify the rim crest against the sky
F122: (391,329) far rim - clarify the rim crest against the sky
F123: (531,340) sky - the sun's glow gathers below the horizon line
F124: (333,368) far rim - strata lines on the old crater wall
F125: (363,497) far rim - strata lines on the old crater wall
F126: (471,525) far rim - clarify the rim crest against the sky
F127: (615,344) gas giant - the limb darkens toward the edge
F128: (304,423) far rim - clarify the rim crest against the sky
F129: (369,276) sky - deepen the blue hour overhead
F130: (560,273) gas giant - the limb darkens toward the edge
F131: (312,306) sky - another cirrus streak, drawn along the wind
F132: (629,409) sky - deepen the blue hour overhead
F133: (238,423) far rim - clarify the rim crest against the sky
F134: (179,135) moon - a bright crater ray on the moon
F135: (523,495) far rim - clarify the rim crest against the sky
F136: (467,465) far rim - clarify the rim crest against the sky
F137: (409,558) far rim - clarify the rim crest against the sky
F138: (551,433) far rim - strata lines on the old crater wall
F139: (432,167) sky - the sun's glow gathers below the horizon line
-- interest map recomputed from the canvas after fixation 140 --
F140: (457,409) far rim - clarify the rim crest against the sky
F141: (366,428) far rim - strata lines on the old crater wall
F142: (396,343) far rim - strata lines on the old crater wall
F143: (524,334) sky - another cirrus streak, drawn along the wind
F144: (336,365) far rim - clarify the rim crest against the sky
F145: (376,500) far rim - clarify the rim crest against the sky
F146: (463,523) far rim - clarify the rim crest against the sky
F147: (630,339) gas giant - the limb darkens toward the edge
F148: (313,434) far rim - strata lines on the old crater wall
F149: (367,277) sky - another cirrus streak, drawn along the wind
F150: (555,276) gas giant - the limb darkens toward the edge
F151: (299,304) sky - the sun's glow gathers below the horizon line
F152: (627,391) sky - the sun's glow gathers below the horizon line
F153: (236,429) far rim - clarify the rim crest against the sky
F154: (176,143) moon - a bright crater ray on the moon
F155: (520,494) far rim - clarify the rim crest against the sky
F156: (461,464) far rim - clarify the rim crest against the sky
F157: (564,427) far rim - clarify the rim crest against the sky
F158: (392,554) far rim - strata lines on the old crater wall
F159: (441,177) sky - deepen the blue hour overhead
-- interest map recomputed from the canvas after fixation 160 --
F160: (464,405) far rim - clarify the rim crest against the sky
F161: (362,432) far rim - strata lines on the old crater wall
F162: (409,336) far rim - strata lines on the old crater wall
F163: (533,328) sky - the sun's glow gathers below the horizon line
F164: (340,377) far rim - clarify the rim crest against the sky
F165: (363,501) far rim - clarify the rim crest against the sky
F166: (466,528) far rim - clarify the rim crest against the sky
F167: (633,343) gas giant - the limb darkens toward the edge
F168: (312,432) far rim - strata lines on the old crater wall
F169: (368,276) sky - another cirrus streak, drawn along the wind
F170: (569,264) gas giant - the limb darkens toward the edge
F171: (306,299) sky - the sun's glow gathers below the horizon line
F172: (620,407) sky - another cirrus streak, drawn along the wind
F173: (239,433) far rim - clarify the rim crest against the sky
F174: (527,488) far rim - strata lines on the old crater wall
F175: (473,467) far rim - strata lines on the old crater wall
F176: (563,428) far rim - clarify the rim crest against the sky
F177: (432,172) sky - another cirrus streak, drawn along the wind
F178: (404,560) far rim - strata lines on the old crater wall
F179: (845,270) gas giant - a bright zone swath on the giant
-- interest map recomputed from the canvas after fixation 180 --
F180: (466,394) far rim - strata lines on the old crater wall
F181: (365,441) far rim - strata lines on the old crater wall
F182: (405,330) far rim - clarify the rim crest against the sky
F183: (522,338) sky - deepen the blue hour overhead
F184: (311,334) far rim - the far slope falls into dusk
F185: (370,502) far rim - strata lines on the old crater wall
F186: (462,537) far rim - strata lines on the old crater wall
F187: (309,426) far rim - clarify the rim crest against the sky
F188: (615,332) gas giant - the limb darkens toward the edge
F189: (377,266) sky - the sun's glow gathers below the horizon line
F190: (553,270) gas giant - turbulence in the zones
F191: (625,400) sky - the sun's glow gathers below the horizon line
F192: (239,432) far rim - clarify the rim crest against the sky
F193: (533,492) far rim - clarify the rim crest against the sky
F194: (472,464) far rim - strata lines on the old crater wall
F195: (553,438) far rim - clarify the rim crest against the sky
F196: (392,565) far rim - clarify the rim crest against the sky
F197: (436,168) sky - the sun's glow gathers below the horizon line
F198: (310,241) sky - the sun's glow gathers below the horizon line
F199: (466,240) sky - the sun's glow gathers below the horizon line
-- interest map recomputed from the canvas after fixation 200 --
F200: (469,394) far rim - strata lines on the old crater wall
F201: (372,438) far rim - clarify the rim crest against the sky
F202: (399,343) far rim - strata lines on the old crater wall
F203: (327,368) far rim - clarify the rim crest against the sky
F204: (375,489) far rim - strata lines on the old crater wall
F205: (566,304) gas giant - turbulence in the zones
F206: (458,533) far rim - clarify the rim crest against the sky
F207: (628,327) gas giant - turbulence in the zones
F208: (314,432) far rim - clarify the rim crest against the sky
F209: (371,273) sky - deepen the blue hour overhead
F210: (492,299) sky - another cirrus streak, drawn along the wind
F211: (311,311) sky - deepen the blue hour overhead
F212: (630,399) sky - another cirrus streak, drawn along the wind
F213: (239,439) far rim - strata lines on the old crater wall
F214: (565,370) sky - deepen the blue hour overhead
F215: (524,505) far rim - strata lines on the old crater wall
F216: (464,465) far rim - the far slope falls into dusk
F217: (551,435) far rim - strata lines on the old crater wall
F218: (431,170) sky - the sun's glow gathers below the horizon line
F219: (392,567) far rim - strata lines on the old crater wall
-- interest map recomputed from the canvas after fixation 220 --
F220: (455,400) far rim - strata lines on the old crater wall
F221: (362,424) far rim - strata lines on the old crater wall
F222: (407,344) far rim - the far slope falls into dusk
F223: (337,376) far rim - strata lines on the old crater wall
F224: (368,496) far rim - strata lines on the old crater wall
F225: (462,534) far rim - strata lines on the old crater wall
F226: (563,300) gas giant - turbulence in the zones
F227: (624,345) gas giant - turbulence in the zones
F228: (313,440) far rim - clarify the rim crest against the sky
F229: (490,299) sky - deepen the blue hour overhead
F230: (365,278) sky - another cirrus streak, drawn along the wind
F231: (295,297) sky - another cirrus streak, drawn along the wind
F232: (625,408) sky - deepen the blue hour overhead
F233: (239,424) far rim - clarify the rim crest against the sky
F234: (528,494) far rim - strata lines on the old crater wall
F235: (468,473) far rim - clarify the rim crest against the sky
F236: (552,437) far rim - strata lines on the old crater wall
F237: (557,368) sky - another cirrus streak, drawn along the wind
F238: (430,184) sky - deepen the blue hour overhead
F239: (407,562) far rim - strata lines on the old crater wall

## PASS 5 - FINISH (vignette and grain)
V1: vignette - the eye's attention falls off toward the frame edge,
    so the image does too. Quiet, not heavy.
V2: grain - a whisper of hash grain, +/-14, so no gradient is ever
    perfectly smooth. The world is not a gradient.

## Decision count
Pass 1: 5 gist decisions. Pass 2: 14 big decisions. Pass 3: 8 light
decisions. Pass 4: 240 fixations. Pass 5: 2 finish decisions.
Total: 269 deliberate decisions. No RNG. Byte-identical reruns.
