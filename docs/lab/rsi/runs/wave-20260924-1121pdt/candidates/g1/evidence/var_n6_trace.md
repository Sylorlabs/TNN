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
G1.6: N=6 sky_px=325786
G1.7: ops: 1048576 density fbm evals, 1954716 march steps.
The interest map: contrast x novelty x nearness to the focal anchor.
Recomputed from the canvas every 20 fixations; visited places fade.
F0: (561,307) sky - deepen the blue hour overhead
F1: (173,147) sky - another cirrus streak, drawn along the wind
F2: (486,437) far rim - strata lines on the old crater wall
F3: (359,426) far rim - strata lines on the old crater wall
F4: (396,328) far rim - clarify the rim crest against the sky
F5: (780,374) gas giant - a bright zone swath on the giant
F6: (343,359) far rim - strata lines on the old crater wall
F7: (297,306) sky - the sun's glow gathers below the horizon line
F8: (366,501) far rim - clarify the rim crest against the sky
F9: (459,533) far rim - the far slope falls into dusk
F10: (304,425) far rim - the far slope falls into dusk
F11: (367,263) sky - the sun's glow gathers below the horizon line
F12: (489,296) sky - another cirrus streak, drawn along the wind
F13: (628,403) sky - the sun's glow gathers below the horizon line
F14: (620,345) gas giant - a bright zone swath on the giant
F15: (242,434) far rim - the far slope falls into dusk
F16: (569,369) sky - another cirrus streak, drawn along the wind
F17: (494,368) far rim - strata lines on the old crater wall
F18: (596,143) gas giant - a bright zone swath on the giant
F19: (839,267) gas giant - a bright zone swath on the giant
-- interest map recomputed from the canvas after fixation 20 --
F20: (561,303) gas giant - turbulence in the zones
F21: (494,439) far rim - clarify the rim crest against the sky
F22: (376,432) far rim - clarify the rim crest against the sky
F23: (177,144) moon - a bright crater ray on the moon
F24: (399,330) far rim - clarify the rim crest against the sky
F25: (330,372) far rim - strata lines on the old crater wall
F26: (362,502) far rim - the far slope falls into dusk
F27: (462,534) far rim - strata lines on the old crater wall
F28: (295,306) sky - the sun's glow gathers below the horizon line
F29: (302,426) far rim - clarify the rim crest against the sky
F30: (375,277) sky - the sun's glow gathers below the horizon line
F31: (495,299) sky - deepen the blue hour overhead
F32: (618,400) sky - the sun's glow gathers below the horizon line
F33: (777,374) gas giant - a bright zone swath on the giant
F34: (623,330) gas giant - a bright zone swath on the giant
F35: (561,369) sky - deepen the blue hour overhead
F36: (240,432) far rim - strata lines on the old crater wall
F37: (494,368) far rim - strata lines on the old crater wall
F38: (437,172) sky - the sun's glow gathers below the horizon line
F39: (310,242) sky - the sun's glow gathers below the horizon line
-- interest map recomputed from the canvas after fixation 40 --
F40: (498,437) far rim - clarify the rim crest against the sky
F41: (522,330) sky - deepen the blue hour overhead
F42: (368,440) far rim - clarify the rim crest against the sky
F43: (399,328) far rim - clarify the rim crest against the sky
F44: (334,372) far rim - strata lines on the old crater wall
F45: (363,489) far rim - strata lines on the old crater wall
F46: (464,532) far rim - clarify the rim crest against the sky
F47: (304,438) far rim - strata lines on the old crater wall
F48: (313,307) sky - another cirrus streak, drawn along the wind
F49: (552,270) gas giant - a bright zone swath on the giant
F50: (377,277) sky - another cirrus streak, drawn along the wind
F51: (633,331) gas giant - turbulence in the zones
F52: (169,153) sky - another cirrus streak, drawn along the wind
F53: (617,393) sky - another cirrus streak, drawn along the wind
F54: (823,336) sky - deepen the blue hour overhead
F55: (244,431) far rim - strata lines on the old crater wall
F56: (303,247) sky - the sun's glow gathers below the horizon line
F57: (432,178) sky - deepen the blue hour overhead
F58: (520,493) far rim - the far slope falls into dusk
F59: (555,424) far rim - strata lines on the old crater wall
-- interest map recomputed from the canvas after fixation 60 --
F60: (502,424) far rim - strata lines on the old crater wall
F61: (369,433) far rim - strata lines on the old crater wall
F62: (529,344) sky - another cirrus streak, drawn along the wind
F63: (398,327) far rim - the far slope falls into dusk
F64: (331,364) far rim - strata lines on the old crater wall
F65: (367,497) far rim - clarify the rim crest against the sky
F66: (466,537) far rim - strata lines on the old crater wall
F67: (305,296) sky - the sun's glow gathers below the horizon line
F68: (298,425) far rim - strata lines on the old crater wall
F69: (620,342) gas giant - the limb darkens toward the edge
F70: (176,152) sky - the sun's glow gathers below the horizon line
F71: (374,264) sky - the sun's glow gathers below the horizon line
F72: (633,408) sky - another cirrus streak, drawn along the wind
F73: (561,276) gas giant - the limb darkens toward the edge
F74: (239,441) far rim - clarify the rim crest against the sky
F75: (519,496) far rim - strata lines on the old crater wall
F76: (296,234) sky - the sun's glow gathers below the horizon line
F77: (439,181) sky - another cirrus streak, drawn along the wind
F78: (782,368) gas giant - a bright zone swath on the giant
F79: (553,432) far rim - strata lines on the old crater wall
-- interest map recomputed from the canvas after fixation 80 --
F80: (490,432) far rim - strata lines on the old crater wall
F81: (391,345) far rim - clarify the rim crest against the sky
F82: (363,439) far rim - clarify the rim crest against the sky
F83: (554,304) sky - deepen the blue hour overhead
F84: (339,372) far rim - clarify the rim crest against the sky
F85: (369,501) far rim - clarify the rim crest against the sky
F86: (469,522) far rim - strata lines on the old crater wall
F87: (311,307) sky - deepen the blue hour overhead
F88: (305,439) far rim - clarify the rim crest against the sky
F89: (617,345) gas giant - the limb darkens toward the edge
F90: (173,143) moon - a bright crater ray on the moon
F91: (365,276) sky - deepen the blue hour overhead
F92: (491,303) sky - another cirrus streak, drawn along the wind
F93: (627,398) sky - another cirrus streak, drawn along the wind
F94: (242,427) far rim - strata lines on the old crater wall
F95: (562,359) sky - the sun's glow gathers below the horizon line
F96: (533,500) far rim - clarify the rim crest against the sky
F97: (494,361) far rim - strata lines on the old crater wall
F98: (431,180) sky - another cirrus streak, drawn along the wind
F99: (295,238) sky - another cirrus streak, drawn along the wind
-- interest map recomputed from the canvas after fixation 100 --
F100: (502,424) far rim - clarify the rim crest against the sky
F101: (391,340) far rim - clarify the rim crest against the sky
F102: (373,432) far rim - strata lines on the old crater wall
F103: (526,334) sky - another cirrus streak, drawn along the wind
F104: (345,370) far rim - clarify the rim crest against the sky
F105: (363,496) far rim - strata lines on the old crater wall
F106: (464,521) far rim - strata lines on the old crater wall
F107: (313,438) far rim - strata lines on the old crater wall
F108: (616,330) gas giant - the limb darkens toward the edge
F109: (363,267) sky - the sun's glow gathers below the horizon line
F110: (312,305) sky - another cirrus streak, drawn along the wind
F111: (630,400) sky - another cirrus streak, drawn along the wind
F112: (554,264) gas giant - the limb darkens toward the edge
F113: (243,434) far rim - clarify the rim crest against the sky
F114: (174,146) sky - deepen the blue hour overhead
F115: (531,497) far rim - clarify the rim crest against the sky
F116: (425,185) sky - another cirrus streak, drawn along the wind
F117: (558,428) far rim - strata lines on the old crater wall
F118: (295,245) sky - another cirrus streak, drawn along the wind
F119: (403,565) far rim - the far slope falls into dusk
-- interest map recomputed from the canvas after fixation 120 --
F120: (491,425) far rim - clarify the rim crest against the sky
F121: (406,343) far rim - clarify the rim crest against the sky
F122: (359,425) far rim - clarify the rim crest against the sky
F123: (531,340) sky - deepen the blue hour overhead
F124: (333,368) far rim - strata lines on the old crater wall
F125: (363,497) far rim - strata lines on the old crater wall
F126: (471,525) far rim - clarify the rim crest against the sky
F127: (295,440) far rim - the far slope falls into dusk
F128: (304,295) sky - the sun's glow gathers below the horizon line
F129: (625,340) gas giant - turbulence in the zones
F130: (368,273) sky - the sun's glow gathers below the horizon line
F131: (632,402) sky - deepen the blue hour overhead
F132: (565,281) gas giant - turbulence in the zones
F133: (238,423) far rim - clarify the rim crest against the sky
F134: (179,135) moon - a bright crater ray on the moon
F135: (523,495) far rim - clarify the rim crest against the sky
F136: (435,177) sky - deepen the blue hour overhead
F137: (569,430) far rim - clarify the rim crest against the sky
F138: (391,561) far rim - strata lines on the old crater wall
F139: (464,231) sky - deepen the blue hour overhead
-- interest map recomputed from the canvas after fixation 140 --
F140: (489,441) far rim - clarify the rim crest against the sky
F141: (398,332) far rim - strata lines on the old crater wall
F142: (364,439) far rim - strata lines on the old crater wall
F143: (556,302) sky - deepen the blue hour overhead
F144: (304,333) far rim - the far slope falls into dusk
F145: (376,500) far rim - clarify the rim crest against the sky
F146: (463,523) far rim - clarify the rim crest against the sky
F147: (310,435) far rim - clarify the rim crest against the sky
F148: (633,338) gas giant - turbulence in the zones
F149: (367,277) sky - deepen the blue hour overhead
F150: (491,308) sky - the sun's glow gathers below the horizon line
F151: (619,400) sky - the sun's glow gathers below the horizon line
F152: (243,423) far rim - clarify the rim crest against the sky
F153: (172,141) moon - a bright crater ray on the moon
F154: (528,495) far rim - strata lines on the old crater wall
F155: (488,366) far rim - clarify the rim crest against the sky
F156: (557,368) sky - the sun's glow gathers below the horizon line
F157: (436,171) sky - the sun's glow gathers below the horizon line
F158: (552,426) far rim - strata lines on the old crater wall
F159: (409,561) far rim - clarify the rim crest against the sky
-- interest map recomputed from the canvas after fixation 160 --
F160: (496,437) far rim - clarify the rim crest against the sky
F161: (394,336) far rim - strata lines on the old crater wall
F162: (377,432) far rim - the far slope falls into dusk
F163: (533,328) sky - the sun's glow gathers below the horizon line
F164: (340,377) far rim - clarify the rim crest against the sky
F165: (363,501) far rim - clarify the rim crest against the sky
F166: (466,528) far rim - clarify the rim crest against the sky
F167: (633,343) gas giant - the limb darkens toward the edge
F168: (312,432) far rim - strata lines on the old crater wall
F169: (368,276) sky - another cirrus streak, drawn along the wind
F170: (313,296) sky - the sun's glow gathers below the horizon line
F171: (626,395) sky - the sun's glow gathers below the horizon line
F172: (556,279) gas giant - turbulence in the zones
F173: (239,433) far rim - clarify the rim crest against the sky
F174: (527,488) far rim - strata lines on the old crater wall
F175: (441,179) sky - deepen the blue hour overhead
F176: (563,428) far rim - clarify the rim crest against the sky
F177: (176,140) moon - a bright crater ray on the moon
F178: (404,560) far rim - strata lines on the old crater wall
F179: (813,334) gas giant - a bright zone swath on the giant
-- interest map recomputed from the canvas after fixation 180 --
F180: (498,426) far rim - strata lines on the old crater wall
F181: (397,345) far rim - strata lines on the old crater wall
F182: (373,426) far rim - clarify the rim crest against the sky
F183: (522,338) sky - the sun's glow gathers below the horizon line
F184: (343,366) far rim - strata lines on the old crater wall
F185: (370,502) far rim - strata lines on the old crater wall
F186: (462,537) far rim - strata lines on the old crater wall
F187: (629,330) gas giant - the limb darkens toward the edge
F188: (295,428) far rim - clarify the rim crest against the sky
F189: (313,298) sky - the sun's glow gathers below the horizon line
F190: (361,270) sky - another cirrus streak, drawn along the wind
F191: (561,272) gas giant - the limb darkens toward the edge
F192: (623,400) sky - the sun's glow gathers below the horizon line
F193: (245,428) far rim - clarify the rim crest against the sky
F194: (536,496) far rim - the far slope falls into dusk
F195: (553,438) far rim - clarify the rim crest against the sky
F196: (424,181) sky - the sun's glow gathers below the horizon line
F197: (404,552) far rim - clarify the rim crest against the sky
F198: (310,241) sky - the sun's glow gathers below the horizon line
F199: (594,144) gas giant - the limb darkens toward the edge
-- interest map recomputed from the canvas after fixation 200 --
F200: (501,426) far rim - strata lines on the old crater wall
F201: (404,342) far rim - clarify the rim crest against the sky
F202: (367,439) far rim - strata lines on the old crater wall
F203: (519,336) sky - deepen the blue hour overhead
F204: (343,361) far rim - strata lines on the old crater wall
F205: (374,496) far rim - strata lines on the old crater wall
F206: (458,533) far rim - clarify the rim crest against the sky
F207: (628,327) gas giant - turbulence in the zones
F208: (314,432) far rim - clarify the rim crest against the sky
F209: (371,273) sky - another cirrus streak, drawn along the wind
F210: (300,299) sky - deepen the blue hour overhead
F211: (631,407) sky - deepen the blue hour overhead
F212: (566,271) gas giant - turbulence in the zones
F213: (239,439) far rim - strata lines on the old crater wall
F214: (533,498) far rim - clarify the rim crest against the sky
F215: (428,185) sky - another cirrus streak, drawn along the wind
F216: (560,433) far rim - clarify the rim crest against the sky
F217: (391,563) far rim - strata lines on the old crater wall
F218: (303,234) sky - the sun's glow gathers below the horizon line
F219: (456,247) sky - another cirrus streak, drawn along the wind
-- interest map recomputed from the canvas after fixation 220 --
F220: (487,432) far rim - strata lines on the old crater wall
F221: (394,328) far rim - strata lines on the old crater wall
F222: (375,440) far rim - clarify the rim crest against the sky
F223: (369,504) far rim - strata lines on the old crater wall
F224: (336,368) far rim - strata lines on the old crater wall
F225: (462,534) far rim - strata lines on the old crater wall
F226: (627,332) gas giant - turbulence in the zones
F227: (304,441) far rim - strata lines on the old crater wall
F228: (569,312) gas giant - the limb darkens toward the edge
F229: (362,267) sky - another cirrus streak, drawn along the wind
F230: (493,310) sky - deepen the blue hour overhead
F231: (295,297) sky - another cirrus streak, drawn along the wind
F232: (625,408) sky - another cirrus streak, drawn along the wind
F233: (239,424) far rim - clarify the rim crest against the sky
F234: (528,494) far rim - strata lines on the old crater wall
F235: (564,377) far rim - the far slope falls into dusk
F236: (424,181) sky - deepen the blue hour overhead
F237: (493,368) far rim - strata lines on the old crater wall
F238: (558,440) far rim - strata lines on the old crater wall
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
