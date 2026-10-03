# EXP1c Attempt 4: Red-team self-review

Wave: wave-20260928-0221pdt. Written after milestone 3, before any
adoption. The reviewer is the implementer; per binding K5 this
self-review does NOT certify anything. It hunts for the failure modes
the loop has hit before.

## 1. Knowledge versus architecture

The I arm learns only from experienced delta-energy of executed
sketches plus the B0/(1+n) novelty bonus. Nothing in M1-M4 reads the
taught KB texts. The P and R arms read only the taught strategies.
The K4 audit (taught vs learned behavior) is CANNOT-CONFIRM by
construction: no such audit was attempted, and the implementer cannot
self-certify one. The attempt-4 K6 ablation excludes COMBINE-containing
sketches from selection but does not teach anything; it is a
capability removal, not knowledge transfer.

## 2. Metric gaming

Median survival ticks is the outcome. Could the I arm game it?
Survival to 1200 requires actually staying alive; the world, not the
agent, scores ticks. The enumeration machinery burns ticks on
exploration, which is why I medians (431, 282) sit far below R (1200):
exploration is costly, not gamed. The ablation arms (1200, 1068)
survive longer precisely because excluding COMBINE sketches cuts the
riskiest exploration. No reward shaping exists beyond the frozen M3.

## 3. M3 fidelity

Verified from source `x1c4_agents.zag`, function `xi_score`:
`mean + (st.b0 / (1 + (tried as i32))) as i64`. Integer division on
the bonus, B0=40 for I-survive (arm 3), B0=120 for I-invent (arm 4).
`xi_pick` uses strict `s > bv` so the lex-earlier (lower-index) sketch
wins ties, and selects over all 399 sketches. Untried sketch:
tried=0, mean=0, score=B0. No extra bonuses, no tie-breaking jitter,
no RNG in any I decision path. Matches the frozen M3 verbatim.

## 4. M4 fidelity

`xi_act` contains exactly three preempting reflexes: (a) storm-active
and in-zone and unsheltered flees via `w_reflex_storm`; (b) energy
below 25 runs `w_reflex_emergency`; (c) `xi_h9` gates every step about
to be taken, refusing steps onto unplanked void cells. Both (a) and
(b) abort the running plan and record partial delta-energy as one try.
No other reflex exists. The P arm's 25-tick storm anticipation is
verbatim taught text from kb_p_exp1c.txt, not an added reflex; the P
arm is the taught strategy, not part of M4.

## 5. K6 cleanliness

Frozen operationalization (M1): all 399 sketches retained, scoring,
selection, plan lengths, and enumeration machinery identical; only
COMBINE-containing sketches excluded from `xi_pick` on the ablation
arm. This fixed the 2321pdt confound (old ablation shrank 399 to 258
sketches AND changed risk profile). Residual confound, recorded in the
evidence note: excluding COMBINE sketches changes both the invention
channel and the exploration-risk profile; the observed survival gain
(abl 1200 vs 431; abl 1068 vs 282) is fully explained by reduced
exploration risk. The ablation medians are measurements from a voided
run, never evidence about invention. Adoption of the ablation is
blocked: attempt 4 is VOID on K7, so nothing may be adopted.

## 6. C3 discrimination

Per the binding 2026-09-28 ruling, the "qualitatively distinct"
gloss is STRUCK. What the calibration actually measured: f0=1200,
f1=1200, f2=1200 medians (all at ceiling), per-variant (ticks,e_end)
vector diffs d01=11, d02=12, d12=12. These diffs are end-energy-only
differences at the 1200 ceiling and discriminate nothing about
survival capability. C3 PASSED on its measurable gate (all three
scripted strategies median >= 720). The f2 patrol differs at code
level (open-loop oscillation, no target seeking, eats only active
motes, storms home, energy-gated emergency reflex), documented from
source reading only, claimed as nothing more.

## 7. K7 precedence

Measured: I-survive post-enumeration selections 0, learned 0;
I-invent post-enumeration selections 56, learned 0. K7 requires
learned fraction >= 0.50; measured 0/0 and 0/56. Verdict: VOID.
K7 is structural: a void run cannot kill the hypothesis. The K1 and
K6 firings (I-survive 431 <= R 1200; ablation medians above I
medians) are recorded as literal measurements from a voided run with
no adoption and no hypothesis-level reading. The old attempt-3
findings (0/13, 0/94) remain uncertified history, unadopted and
uncurable.

## Verdict

Attempt 4 is VOID on K7. No adoption. The structural pattern across
attempts is stable: enumeration completes rarely (5 of 48 I-arm runs
here), and when it does, post-enumeration selections never show
learned dominance (bonus always contributes >= 10%). The next queue
item is a redesign of the exploration/exploitation balance, not a
retune of the variant family: the novelty bonus as specified
structurally prevents learned dominance within 1200 ticks.
