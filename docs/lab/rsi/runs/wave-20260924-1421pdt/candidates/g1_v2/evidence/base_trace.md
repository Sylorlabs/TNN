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
The interest map: contrast x novelty x nearness to the focal anchor.
Recomputed from the canvas every 20 fixations; visited places fade.
F0: (497,435) far rim - clarify the rim crest against the sky
F1: (365,435) far rim - strata lines on the old crater wall
F2: (390,341) far rim - strata lines on the old crater wall
F3: (327,362) far rim - strata lines on the old crater wall
F4: (172,136) moon - a bright crater ray on the moon
F5: (556,310) sky - deepen the blue hour overhead
F6: (375,487) far rim - strata lines on the old crater wall
F7: (457,530) far rim - the far slope falls into dusk
F8: (302,309) sky - the sun's glow gathers below the horizon line
F9: (299,437) far rim - the far slope falls into dusk
F10: (368,265) sky - another cirrus streak, drawn along the wind
F11: (495,295) sky - a thin place in the clouds - let the sun through
F12: (617,392) sky - another cirrus streak, drawn along the wind
F13: (628,339) gas giant - a bright zone swath on the giant
F14: (236,441) far rim - the far slope falls into dusk
F15: (498,370) far rim - strata lines on the old crater wall
F16: (441,177) sky - a thin place in the clouds - let the sun through
F17: (526,496) far rim - the far slope falls into dusk
F18: (564,431) far rim - clarify the rim crest against the sky
F19: (391,555) far rim - the far slope falls into dusk
-- interest map recomputed from the canvas after fixation 20 --
F20: (497,431) far rim - strata lines on the old crater wall
F21: (366,439) far rim - clarify the rim crest against the sky
F22: (408,336) far rim - clarify the rim crest against the sky
F23: (337,368) far rim - strata lines on the old crater wall
F24: (463,522) far rim - clarify the rim crest against the sky
F25: (170,148) sky - a thin place in the clouds - let the sun through
F26: (362,502) far rim - the far slope falls into dusk
F27: (302,310) sky - another cirrus streak, drawn along the wind
F28: (519,306) sky - the sun's glow gathers below the horizon line
F29: (302,426) far rim - clarify the rim crest against the sky
F30: (375,277) sky - a thin place in the clouds - let the sun through
F31: (623,395) sky - the sun's glow gathers below the horizon line
F32: (618,336) gas giant - the limb darkens toward the edge
F33: (233,438) far rim - strata lines on the old crater wall
F34: (527,490) far rim - clarify the rim crest against the sky
F35: (497,369) far rim - clarify the rim crest against the sky
F36: (432,176) sky - another cirrus streak, drawn along the wind
F37: (398,560) far rim - strata lines on the old crater wall
F38: (565,428) far rim - clarify the rim crest against the sky
F39: (214,338) far rim - the far slope falls into dusk
-- interest map recomputed from the canvas after fixation 40 --
F40: (498,437) far rim - clarify the rim crest against the sky
F41: (362,426) far rim - clarify the rim crest against the sky
F42: (400,344) far rim - clarify the rim crest against the sky
F43: (335,360) far rim - clarify the rim crest against the sky
F44: (366,500) far rim - strata lines on the old crater wall
F45: (459,521) far rim - strata lines on the old crater wall
F46: (304,308) sky - the sun's glow gathers below the horizon line
F47: (528,342) sky - another cirrus streak, drawn along the wind
F48: (569,275) gas giant - turbulence in the zones
F49: (296,430) far rim - strata lines on the old crater wall
F50: (377,277) sky - another cirrus streak, drawn along the wind
F51: (185,139) moon - a bright crater ray on the moon
F52: (617,409) sky - another cirrus streak, drawn along the wind
F53: (617,329) gas giant - turbulence in the zones
F54: (247,432) far rim - the far slope falls into dusk
F55: (436,175) sky - another cirrus streak, drawn along the wind
F56: (527,503) far rim - clarify the rim crest against the sky
F57: (400,562) far rim - strata lines on the old crater wall
F58: (552,429) far rim - clarify the rim crest against the sky
F59: (299,232) sky - a thin place in the clouds - let the sun through
-- interest map recomputed from the canvas after fixation 60 --
F60: (502,424) far rim - strata lines on the old crater wall
F61: (369,433) far rim - strata lines on the old crater wall
F62: (369,312) sky - another cirrus streak, drawn along the wind
F63: (302,295) sky - another cirrus streak, drawn along the wind
F64: (331,364) far rim - strata lines on the old crater wall
F65: (367,497) far rim - clarify the rim crest against the sky
F66: (530,345) sky - another cirrus streak, drawn along the wind
F67: (465,520) far rim - clarify the rim crest against the sky
F68: (394,361) far rim - strata lines on the old crater wall
F69: (300,438) far rim - clarify the rim crest against the sky
F70: (560,280) gas giant - the limb darkens toward the edge
F71: (630,392) sky - the sun's glow gathers below the horizon line
F72: (185,152) sky - another cirrus streak, drawn along the wind
F73: (625,340) gas giant - the limb darkens toward the edge
F74: (431,185) sky - the sun's glow gathers below the horizon line
F75: (231,432) far rim - strata lines on the old crater wall
F76: (520,490) far rim - clarify the rim crest against the sky
F77: (407,565) far rim - strata lines on the old crater wall
F78: (558,432) far rim - clarify the rim crest against the sky
F79: (297,240) sky - another cirrus streak, drawn along the wind
-- interest map recomputed from the canvas after fixation 80 --
F80: (490,432) far rim - strata lines on the old crater wall
F81: (359,441) far rim - clarify the rim crest against the sky
F82: (363,311) sky - the sun's glow gathers below the horizon line
F83: (298,304) sky - the sun's glow gathers below the horizon line
F84: (531,340) sky - the sun's glow gathers below the horizon line
F85: (337,373) far rim - clarify the rim crest against the sky
F86: (373,490) far rim - strata lines on the old crater wall
F87: (471,531) far rim - clarify the rim crest against the sky
F88: (401,375) far rim - clarify the rim crest against the sky
F89: (297,441) far rim - clarify the rim crest against the sky
F90: (557,271) gas giant - turbulence in the zones
F91: (173,148) sky - another cirrus streak, drawn along the wind
F92: (619,399) sky - another cirrus streak, drawn along the wind
F93: (627,334) gas giant - turbulence in the zones
F94: (434,171) sky - another cirrus streak, drawn along the wind
F95: (242,423) far rim - clarify the rim crest against the sky
F96: (533,500) far rim - clarify the rim crest against the sky
F97: (302,233) sky - another cirrus streak, drawn along the wind
F98: (399,564) far rim - strata lines on the old crater wall
F99: (551,430) far rim - strata lines on the old crater wall
-- interest map recomputed from the canvas after fixation 100 --
F100: (374,296) sky - the sun's glow gathers below the horizon line
F101: (487,436) far rim - clarify the rim crest against the sky
F102: (373,432) far rim - strata lines on the old crater wall
F103: (526,334) sky - another cirrus streak, drawn along the wind
F104: (313,306) sky - the sun's glow gathers below the horizon line
F105: (331,368) far rim - strata lines on the old crater wall
F106: (368,489) far rim - strata lines on the old crater wall
F107: (473,534) far rim - strata lines on the old crater wall
F108: (392,362) far rim - clarify the rim crest against the sky
F109: (299,427) far rim - clarify the rim crest against the sky
F110: (632,337) gas giant - turbulence in the zones
F111: (566,272) gas giant - turbulence in the zones
F112: (618,392) sky - the sun's glow gathers below the horizon line
F113: (179,146) sky - deepen the blue hour overhead
F114: (430,178) sky - another cirrus streak, drawn along the wind
F115: (243,433) far rim - clarify the rim crest against the sky
F116: (521,505) far rim - strata lines on the old crater wall
F117: (302,236) sky - another cirrus streak, drawn along the wind
F118: (391,565) far rim - strata lines on the old crater wall
F119: (563,437) far rim - clarify the rim crest against the sky
-- interest map recomputed from the canvas after fixation 120 --
F120: (491,425) far rim - clarify the rim crest against the sky
F121: (374,439) far rim - clarify the rim crest against the sky
F122: (359,297) sky - the sun's glow gathers below the horizon line
F123: (307,308) sky - the sun's glow gathers below the horizon line
F124: (525,336) sky - another cirrus streak, drawn along the wind
F125: (331,369) far rim - strata lines on the old crater wall
F126: (375,493) far rim - clarify the rim crest against the sky
F127: (455,536) far rim - clarify the rim crest against the sky
F128: (400,359) far rim - clarify the rim crest against the sky
F129: (625,340) gas giant - turbulence in the zones
F130: (304,433) far rim - clarify the rim crest against the sky
F131: (568,274) gas giant - turbulence in the zones
F132: (629,409) sky - another cirrus streak, drawn along the wind
F133: (430,167) sky - the sun's glow gathers below the horizon line
F134: (243,423) far rim - clarify the rim crest against the sky
F135: (171,143) moon - a bright crater ray on the moon
F136: (307,241) sky - the sun's glow gathers below the horizon line
F137: (537,494) far rim - clarify the rim crest against the sky
F138: (391,561) far rim - strata lines on the old crater wall
F139: (560,423) far rim - clarify the rim crest against the sky
-- interest map recomputed from the canvas after fixation 140 --
F140: (489,441) far rim - clarify the rim crest against the sky
F141: (366,428) far rim - strata lines on the old crater wall
F142: (364,311) sky - deepen the blue hour overhead
F143: (300,302) sky - another cirrus streak, drawn along the wind
F144: (336,365) far rim - clarify the rim crest against the sky
F145: (536,340) sky - the sun's glow gathers below the horizon line
F146: (367,491) far rim - clarify the rim crest against the sky
F147: (470,531) far rim - clarify the rim crest against the sky
F148: (409,370) far rim - strata lines on the old crater wall
F149: (623,341) gas giant - turbulence in the zones
F150: (299,436) far rim - clarify the rim crest against the sky
F151: (555,272) gas giant - the limb darkens toward the edge
F152: (627,391) sky - the sun's glow gathers below the horizon line
F153: (428,173) sky - the sun's glow gathers below the horizon line
F154: (240,431) far rim - strata lines on the old crater wall
F155: (520,494) far rim - clarify the rim crest against the sky
F156: (301,240) sky - the sun's glow gathers below the horizon line
F157: (404,555) far rim - clarify the rim crest against the sky
F158: (168,138) moon - a bright crater ray on the moon
F159: (569,433) far rim - clarify the rim crest against the sky
-- interest map recomputed from the canvas after fixation 160 --
F160: (496,437) far rim - clarify the rim crest against the sky
F161: (362,432) far rim - the far slope falls into dusk
F162: (409,336) far rim - strata lines on the old crater wall
F163: (309,296) sky - the sun's glow gathers below the horizon line
F164: (532,345) sky - deepen the blue hour overhead
F165: (331,373) far rim - clarify the rim crest against the sky
F166: (626,336) gas giant - the limb darkens toward the edge
F167: (377,503) far rim - clarify the rim crest against the sky
F168: (472,528) far rim - strata lines on the old crater wall
F169: (304,436) far rim - strata lines on the old crater wall
F170: (569,264) gas giant - the limb darkens toward the edge
F171: (370,267) sky - the sun's glow gathers below the horizon line
F172: (620,407) sky - deepen the blue hour overhead
F173: (431,177) sky - the sun's glow gathers below the horizon line
F174: (239,424) far rim - strata lines on the old crater wall
F175: (537,499) far rim - strata lines on the old crater wall
F176: (307,236) sky - the sun's glow gathers below the horizon line
F177: (400,556) far rim - strata lines on the old crater wall
F178: (180,144) sky - another cirrus streak, drawn along the wind
F179: (557,430) far rim - strata lines on the old crater wall
-- interest map recomputed from the canvas after fixation 180 --
F180: (370,426) far rim - strata lines on the old crater wall
F181: (493,441) far rim - strata lines on the old crater wall
F182: (405,330) far rim - clarify the rim crest against the sky
F183: (298,306) sky - deepen the blue hour overhead
F184: (343,366) far rim - strata lines on the old crater wall
F185: (498,310) sky - another cirrus streak, drawn along the wind
F186: (366,505) far rim - strata lines on the old crater wall
F187: (629,330) gas giant - the limb darkens toward the edge
F188: (455,524) far rim - clarify the rim crest against the sky
F189: (569,298) gas giant - the limb darkens toward the edge
F190: (297,430) far rim - strata lines on the old crater wall
F191: (369,272) sky - the sun's glow gathers below the horizon line
F192: (623,400) sky - the sun's glow gathers below the horizon line
F193: (437,172) sky - the sun's glow gathers below the horizon line
F194: (248,432) far rim - strata lines on the old crater wall
F195: (553,374) far rim - the far slope falls into dusk
F196: (520,501) far rim - clarify the rim crest against the sky
F197: (500,360) far rim - clarify the rim crest against the sky
F198: (406,561) far rim - the far slope falls into dusk
F199: (562,432) far rim - clarify the rim crest against the sky
-- interest map recomputed from the canvas after fixation 200 --
F200: (373,426) far rim - strata lines on the old crater wall
F201: (500,438) far rim - clarify the rim crest against the sky
F202: (399,343) far rim - strata lines on the old crater wall
F203: (519,336) sky - the sun's glow gathers below the horizon line
F204: (343,361) far rim - strata lines on the old crater wall
F205: (310,304) sky - another cirrus streak, drawn along the wind
F206: (362,501) far rim - clarify the rim crest against the sky
F207: (628,327) gas giant - turbulence in the zones
F208: (474,528) far rim - clarify the rim crest against the sky
F209: (307,433) far rim - strata lines on the old crater wall
F210: (556,267) gas giant - turbulence in the zones
F211: (375,279) sky - another cirrus streak, drawn along the wind
F212: (630,399) sky - another cirrus streak, drawn along the wind
F213: (239,439) far rim - strata lines on the old crater wall
F214: (437,178) sky - deepen the blue hour overhead
F215: (524,505) far rim - strata lines on the old crater wall
F216: (400,561) far rim - clarify the rim crest against the sky
F217: (551,435) far rim - strata lines on the old crater wall
F218: (303,234) sky - the sun's glow gathers below the horizon line
F219: (456,247) sky - a thin place in the clouds - let the sun through
-- interest map recomputed from the canvas after fixation 220 --
F220: (359,432) far rim - strata lines on the old crater wall
F221: (490,424) far rim - strata lines on the old crater wall
F222: (407,344) far rim - clarify the rim crest against the sky
F223: (497,312) sky - another cirrus streak, drawn along the wind
F224: (336,368) far rim - the far slope falls into dusk
F225: (366,502) far rim - strata lines on the old crater wall
F226: (627,332) gas giant - turbulence in the zones
F227: (464,537) far rim - strata lines on the old crater wall
F228: (313,312) sky - the sun's glow gathers below the horizon line
F229: (298,427) far rim - strata lines on the old crater wall
F230: (557,278) gas giant - turbulence in the zones
F231: (359,265) sky - another cirrus streak, drawn along the wind
F232: (625,408) sky - another cirrus streak, drawn along the wind
F233: (239,424) far rim - clarify the rim crest against the sky
F234: (432,174) sky - another cirrus streak, drawn along the wind
F235: (564,377) far rim - the far slope falls into dusk
F236: (520,501) far rim - strata lines on the old crater wall
F237: (397,560) far rim - strata lines on the old crater wall
F238: (494,376) far rim - strata lines on the old crater wall
F239: (567,434) far rim - strata lines on the old crater wall

## PASS 5 - FINISH (vignette and grain)
V1: vignette - the eye's attention falls off toward the frame edge,
    so the image does too. Quiet, not heavy.
V2: grain - a whisper of hash grain, +/-14, so no gradient is ever
    perfectly smooth. The world is not a gradient.

## Decision count
Pass 1: 5 gist decisions. Pass 2: 14 big decisions. Pass 3: 8 light
decisions. Pass 4: 240 fixations. Pass 5: 2 finish decisions.
Total: 269 deliberate decisions. No RNG. Byte-identical reruns.
