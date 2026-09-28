# A1 — Strategy sketches (novelty extraction)

## Method
For each variant where I-survive (or I-invent) beats R by ≥60 ticks, the action
trace was examined and an abstract strategy sketch was attempted.

## Result: NO coherent novel strategy found

I-survive beats R by ≥60 on 9 variants (v00, v01, v02, v03, v05, v06, v07, v08, v10).
I-invent beats R by ≥60 on 9 variants (similar set).

However, examination of the traces reveals that I does NOT execute a coherent
novel survival strategy. Instead, I's behavior is:

1. **Safety layer** (shared heuristics): flees storms, forages when E<40,
   avoids the void. This is NOT novel (it's the taught KB).
2. **Systematic exploration** (when safe): tries all 1-step actions, then all
   2-step combinations, then 3-step, etc., driven by the novelty bonus. The
   action distribution is roughly uniform across action types (not focused).
3. **No WARD built** (DISC 3@-1 on all variants). No shelter constructed.
4. **Occasional LAMP** built (v00, v04, v07, v10) but never effectively used
   (kept in inventory or dropped without benefit).

### Example: I-survive v00 (248 ticks vs R 160)
Trace begins: 0123456 01020203040506 00111213141516 101212223242526...
This is lexicographic enumeration of 1-step then 2-step plans, NOT a strategy.
Action counts: LEFT 68, RIGHT 28, EAT 29, TAKE 28, DROP 27, COMBINE 24, WAIT 44.
The agent explores systematically, eats opportunistically, and dies at t=248
from starvation (cause 1). There is no "strategy sketch" to extract — the
behavior is exploration, not a composed plan.

### Why I beats R (hypothesis)
R's heuristic "if two items and safe, try COMBINE" is HARMFUL: it builds
LAMPs (wasting crystal+mote) or SURGEs (with the -2/tick penalty) without
using them. I's deliberation, when safe, does NOT reflexively COMBINE; it
explores alternatives. I also has void-avoidance in its executor that R lacks.
The 60-tick gain appears to come from (a) avoiding R's harmful COMBINE and
(b) slightly better safety, NOT from a novel invented strategy.

### Conclusion for H1
I-survive median (220) > R median (160), so K1 does not fire. HOWEVER, the
requirement for "genuine invention" (§2: "composing discovered/known elements
into a novel working strategy") is NOT met. I does not compose elements into
a working strategy; it explores without converging on one. The novelty audit
(K4) will likely find no "key compositional steps" because there are none —
just exploration. The ablation (K6) will likely show the "novelty" (exploration)
is not causally responsible for a specific strategy, because no strategy exists.

This is reported honestly: the deliberation machinery, as specified in §4 and
implemented here, does NOT produce genuine invention in this world. It produces
exploration that modestly outperforms a flawed recall baseline.
