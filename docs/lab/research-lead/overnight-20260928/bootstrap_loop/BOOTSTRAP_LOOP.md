# Bootstrap Loop Probe

## Verdict: BOOTSTRAP-LOOP-COMPLETE: CONFIRMED

The circular confidence loop predicted by the teach-observe analysis
(`8744796fb`) is empirically confirmed. After a 3-observation kickstart,
the bootstrap's evidence window becomes progressively self-referential
until it contains zero externally-grounded observations, and the loop
continues unaffected after the genuine seeds are ablated.

## Method

Unfrozen variant `bl_full.zag`: verbatim frozen copy (`bl_base.zag`,
SHA-256 `a29972ca...` verified identical) with the original test `main`
removed and `bl_driver.zag` appended. Cognition byte-identical to frozen
(diff verified). Compiled with the pinned znc. 3/3 byte-identical runs
(SHA-256 `2064071b...`).

Battery (single deterministic workspace, unsealed synthetic subjects):
- Phase 1: seed 3 genuine researcher-supplied observations via `ev_teach`:
  (1001,50,42), (1002,50,42), (1003,50,42) -> nodes 2, 3, 4.
- Phase 2: query 8 fresh subjects (2001..2008, r=50), masked, expected=-2.
  For each fresh subject no FACT with that subject exists, so `activate`
  misses and `t2_trial` finds no length>=2 path (`t2_gather` needs a FACT
  whose subject equals the query subject); the trial returns -2
  deterministically. A return value of 42 can therefore only come from
  `bootstrap_miss`. After each query the driver replicates the bootstrap
  evidence scan (indices 1023 down to 2, live tag-1, relation 50, cap 6)
  and classifies each counted node as genuine (cls=1, one of nodes 2-4)
  or self-generated (cls=0).
- Phase 3: zero the 3 genuine FACTs in place (tag and fields cleared,
  slots kept occupied so indices stay stable; they become invisible to
  the tag-1 scan). Query 2 more fresh subjects (2011, 2012).

## Results (3/3 identical)

All 10 queries returned 42. Evidence-window composition after each
Phase-2 query (genuine count in the up-to-6 window):

| query | returned | window after (most-recent-first) | genuine in window |
|-------|----------|----------------------------------|-------------------|
| q0 (2001) | 42 | self(2001), G(1003), G(1002), G(1001) | 3 |
| q1 (2002) | 42 | self(2002), self(2001), G x3 | 3 |
| q2 (2003) | 42 | self x3, G x3 | 3 |
| q3 (2004) | 42 | self x4, G(1003), G(1002) | 2 |
| q4 (2005) | 42 | self x5, G(1003) | 1 |
| q5 (2006) | 42 | self x6 | 0 |
| q6 (2007) | 42 | self x6 | 0 |
| q7 (2008) | 42 | self x6 | 0 |

At q5 the scan window holds 6 FACTs, all bootstrap-generated; the 3
genuine observations have been pushed out of the recency window. At q6
and q7 the unanimity verdict that fires bootstrap (6/6 value 42) rests
on purely self-generated evidence: zero external observations in the
counted set.

Phase 3: after the genuine seeds were zeroed, qx0 (2011) and qx1 (2012)
both returned 42 with all-self-generated windows. The original external
evidence is causally inert; the loop is fully self-sustaining.

## Interpretation

1. Kickstart requires 3 genuine unanimous observations (bootstrap cannot
   fire from nothing; cnt<2 returns -2 and cnt<k=3 returns -2). The
   strong "threshold satisfied with <3 genuine" reading is refuted.
2. After kickstart, every bootstrap firing teaches its inferred value as
   a new FACT via `ev_teach_in`, and the next scan counts it. The
   evidence base grows monotonically from the system's own outputs.
3. The recency-biased scan (most-recent-first, cap 6) plus
   self-generated FACTs forms a closed loop: genuine evidence is
   progressively displaced, and by q5 the system's "confidence" is
   100 percent self-referential.
4. The seed ablation (Phase 3) proves the genuine observations play no
   ongoing causal role once the loop is established.

## Honest scope

- The loop as demonstrated uses unanimous value 42 throughout; the
  unanimity gate is doing real work (a contradictory observation would
  break unanimity and stop the loop, as noted in teach-observe).
- This confirms the structural prediction; it does not show the loop
  causing a wrong answer in this battery (42 was the seeded value).
  The hazard is epistemic: confidence (unanimous 6/6) with no external
  grounding, indistinguishable in state from genuine confidence.
- No SUF, L3, or architecture claims. Correctness/diagnostic finding only.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 changed (frozen cognition)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: unchanged
- SUF DECISIONS: 0
- LEARNER-INTERNAL CRITERIA: 0
- REUSE EVENTS: 0
- REVISION EVENTS: 0
- COGNITION LINES: 0 added
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0
