# VERDICT: TNN-on-Placement (scaffold-and-release, Micah order 2026-09-26)

## Order
"we need to have TNN on it — the crew can scaffold and release as well as train as they need, and see if it helps."

## What scaffold-and-release means here (honest framing)
The previous crew's `deliberate_headx()` in pigfront.zag is crew-authored Zag
code: the D1/D2/D3 reasoning steps are fixed crew prose with computed numbers
plugged in. The choice is computed, but the reasoning is the crew's, not TNN's.
Scaffold-and-release puts TNN's ACTUAL native deliberation machinery on the
placement problem: the dialogue system with reasoning traces from chat round 3
(retrieval + F2 withhold gate + F1 comparison engine + F3 difference engine,
binary `dialogue_bin_trace`). The crew built ONLY the scaffold — a KB of
measured facts, a gazetteer, and a question battery. TNN's machinery made every
decision below; the traces are genuine machine output, not crew prose.

## Training (through the machinery's real intake, kb_install)
10 facts taught. 9 are measurements from knowledge.txt (head center x=161,
left/right ear x, ear-mid x=163, snout x=186, the two offsets 2px/25px,
ear-line y=39, frame 320x240). 1 is honest negative knowledge: "TNN did not
measure the pig head center y in the teaching frame." (true: the KNOW record
has no head-cy field).
Deliberately NOT taught: any layout principle ("the ear midpoint marks the
head center", "ears are symmetric"). Those are the hypotheses under test;
teaching them would smuggle the answer.

## TNN's deliberation (genuine traces, P1 taught branch)
1. "which is shorter, the ear midpoint offset or the snout offset?"
   `TR compare e1=ear midpoint offset v1=2 e2=snout offset v2=25 tall=1 dmin=1`
   -> "ear midpoint offset is shorter." The native comparison engine weighed
   the two measured offsets and chose the ear-mid estimator. TNN's choice.
2. "how much smaller is it?"
   `TR f3 ddim=1 d1=ear midpoint offset v1=2 d2=snout offset v2=25 diff=23`
   -> "23". Genuine native subtraction.
3. "what y marks the pig head center?"
   Before the negative fact was taught: emitted the x-measurement fact —
   the round-3 predicate hole reproduced live in this domain (entity-known +
   predicate-unknown -> confabulation). After teaching the honest negative
   fact: `branch=default fid=9 withhold=0` ->
   "TNN did not measure the pig head center y in the teaching frame."
   Epistemically correct.
4. "where is the pig torso in the front view?"
   `branch=default fid=0 withhold=1` -> "I don't know." No fabrication.
5. "what x did TNN measure for the pig head center?" -> fact 0 verbatim.
   TNN distinguishes the direct measurement (161) from the chosen estimator.

## P2 (untaught branch — KB holds only side views, no frontal knowledge)
1. "where is the pig head in the front view?"
   -> "TNN never saw the pig front view." The honest native replacement for
   the crew's (160,82) untaught prior (hardcode #4).
2. "where should the pig torso be drawn?"
   -> "TNN saw 24 side views of the pig." Predicate hole again: irrelevant
   but true; crucially, NO coordinates fabricated.

## TNN's placement rule (scaffold translation, documented as scaffold)
- head-x: use TNN's chosen estimator (ear-mid) -> 163. dx=19 vs truth (182).
- head-y: TNN declines ("did not measure") -> NO placement.
- torso / facezone / untaught geometry: TNN abstains -> do not draw.

## Measurement: did putting TNN on it help?
| | Crew's deliberated rule | TNN's native deliberation |
|---|---|---|
| head-x | 163 (dx=19) | 163 (dx=19) — same choice, via genuine machinery trace |
| head-y | 123 (dy=11, confident, wrong) | declines — epistemically correct |
| hardcodes eliminated | 3 (#1,2,3) | +3: #4 untaught prior, #6 facezone ratios, #7 torso geometry — all become honest abstention |
| new discovery | — | none |

Honest assessment: TNN validated the head-x estimator choice through its own
machinery — the comparison is real deliberation, not crew prose with numbers.
Its abstention on head-y is strictly better than the crew's confident-but-wrong
123: had TNN been on the problem first, the 11px head-y regression would never
have happened. Three more hardcodes die by abstention instead of extrapolation.
But TNN discovered nothing new — no better estimator, no better placement.
What the crew's D3 did (judging method quality: "band mask is suspect, clean
blobs are better") has no native equivalent in the machinery.

## Machinery limits mapped by this experiment
1. Predicate hole is real and domain-general: without the negative fact,
   a y-question gets the x-fact. Teaching honest negative knowledge fixes it.
2. No multiply/divide in native arithmetic: the crew's scale-corrected head-y
   (39*172/179) is impossible for the machinery; it cannot do that step at all.
3. The assertion branch checks discourse consistency only; it cannot reject a
   hypothesis (e.g. "snout marks the midline") from measurement evidence.

## Determinism
Two full runs byte-identical (sha256) on stdout AND stderr traces.
Pure Zag binary, zero RNG. KB/gazetteer/battery/traces committed below.
