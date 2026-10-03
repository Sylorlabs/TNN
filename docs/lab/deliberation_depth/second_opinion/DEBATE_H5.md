# H5 Second Opinion — grok-4.7 vs gpt-5.6-sol (with adjudication)

Date: 2026-09-24. Coordinator task from Micah: undecided on H5, wants sol +
grok to weigh in on (1) the knee finding, (2) the confidence sensor,
(3) the single most valuable follow-up. Same frozen prompt sent to both
models independently (`../` — prompt text in this run's working notes).

## gpt-5.6-sol: NO OPINION — provider outage (evidence preserved)

Four attempts, two interfaces (`unorouter.py chat` x3, `sol.py` x1), over
~15 minutes. Every attempt returned the identical provider-side signature:

```json
{"id": "chatcmpl-Tpp5l5kiQ6drqi5f", "model": "gpt-5.6-sol",
 "object": "chat.completion", "created": 1790225062,
 "choices": null,
 "usage": {"prompt_tokens": 1349, "completion_tokens": 0, "total_tokens": 1349,
  "completion_tokens_details": {"text_tokens": 0, "audio_tokens": 0,
   "reasoning_tokens": 0}}}
```

The provider backend accepted the prompt (1349 tokens) and generated zero
completion tokens, four times in a row. This is the documented AGENTS.md
sol failure mode (`choices:null` with 0 completion tokens, provider-side,
not a prompt problem) and matches the earlier H7 debate where "Sol flaked
on 3 openings." Sol is declared unavailable for this round. Raw response
preserved in working notes (`sol_diag.txt`).

## grok-4.7: full opinion (verbatim, 1 attempt, ~84s)

**1. The knee is mostly a misread, and neither 4 nor 16 should be law.**

The table and the parenthetical disagree. Trap accuracy is 0.961 at d4 and
1.000 at both d8 and deep16, so d4→d8 is +3.9 points and d8→d16 is +0.0.
The claim that "8→16 still gained 3.9pts" labels the wrong interval.
Applied to the table, the frozen rule's "smallest depth whose arriving
doubling is <1pt and every later one is too" is d8 on the pooled numbers
(+0.6 then 0) and d16 on traps only because the doubling that *arrives
at* d8 is still 3.9 points. Knee=16 is an off-by-one against a point
that is already saturated: trap mean rounds at d8 and deep16 are
identical (3.81). Cap 16 does nothing.

The curvature claim is the other misread. Dividing +0.039 by four
*nominal* rounds (0.010/round, "two orders of magnitude") treats unused
cap as compute. Actual trap rounds go 3.48→3.81, about +0.33 rounds,
~0.12 accuracy per round actually spent, to fix 5/127 items. That is not
a collapsed return.

What the data support: four batteries are ceilinged at depth 1 (pooled d1
= 750/877 = 0.855 exactly when every trap item is wrong), so a pooled
knee is not a system property. On the only battery with a curve, accuracy
saturates once the cap reaches 8, at ~4 rounds, and the live tradeoff is
cap 4 vs cap 8: ~5 items, ~40 extra item-rounds on that battery. Do not
enshrine 4. Enshrine "cap 8, expect ~4 rounds, d16 is a null," and treat
the 1pt-per-doubling rule as mis-specified because its denominator is
the log cap, not rounds consumed. Also do not promote this to
architectural law: the d4→d8 contrast is five items.

**2. The sensor is a bad quantity, but it is not why traps don't
early-stop.**

§6 saved nothing on traps because corrective evidence kept moving the
margin until the stream ended (0/127 early stops; adaptive rounds =
deep16 rounds). A stability rule *should* refuse to stop there. "Run
until evidence exhaustion" is the right policy for finite,
conflict-bearing streams. A tighter epsilon or a smoother confidence
score would not create safe early exits if the margin is still honestly
moving; it would only add premature stops.

What is wrong with the sensor:

- Clamped leader−runner-up is not a belief. ε=0.02 is in incomparable
  score units, so "stable" ≠ "correct" and ≠ "calibrated."
- On the four verdict-anchored batteries, stability is immediate, so §6
  looks smart where depth never mattered.
- k=3 cannot tell a mid-stream plateau from exhaustion. This design never
  contained a plateau-then-flip, so the rule was not tested, only
  untriggered.

Replace the stopping rule with a residual-flip bound: stop only if the
stream is exhausted, or if remaining unprocessed evidence cannot change
the leader under a stated bound. Keep processing whenever premises still
conflict. Recalibration is worth doing so that thresholds mean
something; it is not a substitute for that bound.

**3. The follow-up that can actually change the verdict**

Build one battery of delayed-disconfirmation items: a ≥3-round margin
plateau while the running answer is wrong, then a late premise that
flips it, plus a matched set where extra rounds after a correct early
answer flip it to wrong (overthinking), with the same n and the same
frozen §6. Preregister item-level stop round, whether the stop fell
inside the plateau, and accuracy against an oracle that reads the full
stream.

If §6 stops in the plateau, ADAPTIVE-WINS is an artifact of traps whose
scores never flatten early. If extra depth flips correct items, deeper
caps are not monotone and knee=8 is unsafe. If neither happens,
evidence-exhaustion really is the right trap policy and the confidence
sensor is only a cost heuristic for easy items. Secondary, not instead:
a reliability check of clamped margin, and a misleading-premise dose
curve (0/1/2/6) to see whether rounds track residual conflict. More
ceilinged batteries will not change anything.

## Adjudication (coordinator)

Verified grok's arithmetic against `results_v2/RESULTS_H5.md` before
adjudicating — every check held:

- The handoff's "8→16 still gained 3.9pts" is indeed an off-by-one. Trap
  d8 = 1.000, deep16 = 1.000 → d8→d16 = +0.000; the +3.9pts is d4→d8,
  arriving AT d8. The frozen rule mechanically yields knee=16 on traps
  only because it tests the doubling *arriving at* p, labeling
  saturation one doubling late. Pooled d1 = 750/877 = 0.855 exactly when
  all 127 trap items are wrong — the pooled curve is the trap curve
  diluted; a "pooled knee" is not a system property.
- The "two orders of magnitude per round" rhetoric divides by nominal
  rounds. In rounds actually spent, d4→d8 is +0.039 on ~0.33 rounds ≈
  0.12 accuracy/round vs +0.315/round earlier — a real decline (~2.7×)
  but not the 100× the file's rhetoric implies. The absolute return
  still collapses (3.9pts vs 63pts), and the entire d4→d8 gain is 5
  wason items.
- Trap mean rounds d8 = deep16 = 3.81 exactly: cap 16 is a null on this
  distribution. Nothing in the sweep ever hit the cap (0/877).

**Rulings:**

1. **Knee.** Neither 4, 8, nor 16 should become architectural law. The
   data support an operating envelope, not a constant: saturation at
   cap 8, ~3.8 mean trap rounds, d4 reaching 96.1% on traps, and the
   d4-vs-d8 choice decided by exactly 5 wason items. The frozen
   per-doubling rule is mis-specified two ways (denominator = log cap
   instead of rounds consumed; off-by-one labeling of saturation).
   Recommend a prereg amendment: replace the rule with one denominated
   in rounds actually spent, or keep the mechanical 16 as a
   conservative cap with the off-by-one documented — but do not present
   any of these numbers as a property of deliberation in general.
   The results file's own §8.3 already concedes the knee may not
   generalize beyond this harness's score mechanics.
2. **Sensor.** Grok is right on both halves, and they point in different
   directions: (a) clamped margin is a bad quantity — uncalibrated,
   epsilon in incomparable units, "stable" ≠ "correct"; recalibration
   is worth doing so thresholds mean something. (b) But the sensor is
   NOT why traps didn't early-stop — a stability rule *correctly*
   refused to stop while the margin was honestly moving. The finding
   stands: on conflict-bearing finite streams, "run until evidence
   exhaustion" is the right policy, and §6 is vacuous there by design
   correctness, not by sensor failure. Adopt grok's residual-flip bound
   as the stopping rule for conflict streams (stop only on exhaustion
   or when remaining evidence provably cannot flip the leader); keep
   §6 as a cost heuristic for the easy batteries.
3. **Follow-up.** Grok's delayed-disconfirmation battery is the single
   most valuable experiment: it is the one input class the frozen
   design never contained (plateau-then-flip), and it simultaneously
   tests whether ADAPTIVE-WINS is an artifact of never-plateauing
   traps AND whether deeper caps are monotone (the overthinking
   matched set). If §6 stops inside a wrong plateau, the adaptive
   verdict needs revision; if extra depth flips correct items,
   knee=8/cap-16 thinking is unsafe. Recommend building it with the
   same frozen §6 and preregistered item-level stop rounds.
   Secondary: misleading-premise dose curve (0/1/2/6) to check whether
   rounds track residual conflict.

**Net change to the H5 verdict:** ADAPTIVE-WINS stands (pooled), the
knee numbers do not graduate to law, the sensor needs recalibration
plus a residual-flip bound for conflict streams, and the next battery
must contain plateau-then-flip items before any architectural claim
about stopping rules is frozen.
