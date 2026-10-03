# Contradiction Break Probe

## Verdict: CONTRADICTION-BREAK-COMPLETE: CONFIRMED

A single contradicting observation breaks the confirmed bootstrap loop,
and the break is permanent without external intervention. The learner has
no mechanism to resolve the disagreement, discount the outlier, or resume
inference on its own. Recovery required six externally-taught observations
to push the contradiction out of the recency window. The hazard is worse
than epistemic: the bootstrap mechanism is fragile, not just ungrounded.

## Method

Unfrozen variant `cb_full.zag`: verbatim frozen copy (`cb_base.zag`,
SHA-256 `a29972ca...` verified identical) with the original test `main`
removed and `cb_driver.zag` appended. Cognition byte-identical to frozen
(diff verified). Compiled with the pinned znc. 3/3 byte-identical runs
(SHA-256 `b15078a0...`).

Battery (single deterministic workspace, unsealed synthetic subjects):
- Phase 1: seed 3 genuine observations via `ev_teach`:
  (1001,50,42), (1002,50,42), (1003,50,42).
- Phase 2: query 4 fresh subjects (2001..2004, r=50), masked, expected=-2.
  Establishes the self-referential loop (replicates `ee7815de8`).
- Phase 3: CONTRADICTION via `ev_teach(3001,50,99)`. A conflicting
  observation for the same relation. Becomes the most-recent scan entry.
- Phase 4: query 4 fresh subjects (2005..2008). Tests if the loop breaks.
- Phase 5: query 2 more fresh subjects (2009,2010). Tests persistence.
- Phase 6: RECOVERY. Externally teach six 42-facts (4001..4006, r=50,42).
  Query 2 fresh subjects (2011,2012). Tests what recovery requires.
- Phase 7: SECOND CONTRADICTION via `ev_observe(2001,50,99)` on a subject
  with an existing self-generated 42-fact. Routes through
  `revise_on_contradict`. Query 1 fresh subject (2013).

## Results (3/3 identical)

### Phase 2: loop established

q0..q3 all returned 42. Window accumulated self-generated 42-facts.
Replicates the confirmed bootstrap loop.

### Phase 3: contradiction taught

`ev_teach(3001,50,99)` returned idx14. Scan window for r=50:
`[99(3001), 42, 42, 42, 42, 42]`. The contradiction is the most-recent
entry (highest index, scanned first).

### Phase 4: loop breaks

b0, b1, b2, b3 ALL returned -2. The unanimity gate fires correctly:
v0=99, subsequent values are 42, inv=0, return -2. No new FACT is taught
on a failed bootstrap, so the window is unchanged across all four queries.

### Phase 5: break is persistent

p0, p1 both returned -2. Window r70 still shows 99 at the top. The system
has no mechanism to remove, discount, or work around the contradiction
on its own. Failed bootstraps teach nothing, so the contradiction stays
at the top of the recency-ordered window indefinitely.

### Phase 6: recovery requires external teaching

Six externally-taught 42-facts (4001..4006, idx28..33) pushed 99 out of
the cap-6 window. Window r80: six 42s, zero 99s. Then r0=42, r1=42:
bootstrap FIRES AGAIN. The loop recovered, but ONLY because of external
intervention. The learner contributed nothing to its own recovery.

### Phase 7: observe-path contradiction also breaks

`ev_observe(2001,50,99)` returned 0 (contradiction path: the existing
(2001,50,42) fact did not match). This invoked `revise_on_contradict`
and taught (2001,50,99) at idx39. Window r100:
`[99(2001), 42, 42, 42, 42, 42]`. Query f0 (subject 2013) returned -2.
The revision machinery did not prevent the new 99-fact from entering the
bootstrap evidence window and breaking unanimity.

Note: the system now holds two live contradictory facts about (2001,50):
idx7 says 42, idx39 says 99. No resolution mechanism exists. They coexist.

## Interpretation

1. **The unanimity gate works as designed.** A single conflicting
   observation correctly stops the bootstrap from inferring. This is not
   a bug in the gate.
2. **The break is permanent without external help.** The architecture has
   no disagreement-resolution machinery: no outlier discounting, no
   evidence-base revision, no confidence-weighted voting, no path from
   "stop" to "resume." The three-stops analysis (`48cb843e5`) identified
   decline, abandonment, and forgetting as missing; this probe shows that
   even the first stop (decline) has no exit.
3. **Recovery is entirely external.** Six taught 42-facts were needed to
   displace one 99-fact from the cap-6 window. The 6:1 ratio is an
   artifact of the recency window size, not a principled confidence
   mechanism. The learner cannot generate its own recovering evidence
   because failed bootstraps teach nothing.
4. **The revision machinery does not protect bootstrap.** Phase 7 shows
   `revise_on_contradict` runs on the observe path but operates on MAPs
   and graphs, not on the bootstrap evidence base. The FACT-level
   contradiction still poisons the scan window.
5. **Contradictory facts accumulate without resolution.** After Phase 7,
   (2001,50) has two live facts with different values. The teach/observe
   conflation (`8744796fb`) means there is no "current belief" vs
   "superseded belief" distinction that bootstrap respects.

## Honest scope

- This probe confirms the structural prediction that contradiction breaks
  the loop. It does not show the loop causing a wrong answer; the hazard
  demonstrated here is fragility (permanent disablement), not incorrectness.
- The 6:1 recovery ratio depends on the cap-6 window and the single-99
  setup. Different contradiction multiplicities were not tested.
- No SUF, L3, or architecture claims. Correctness/diagnostic finding only.
- The probe used `ev_teach` (researcher-supplied) for the contradiction.
  A naturally-occurring contradictory observation would enter via
  `ev_observe`; Phase 7 covers that path with the same breaking result.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 changed (frozen cognition)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: unchanged
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 1 (revise_on_contradict invoked in Phase 7; no MAPs
  present to revise, so no structural effect)
- COGNITION LINES: 0 added
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
