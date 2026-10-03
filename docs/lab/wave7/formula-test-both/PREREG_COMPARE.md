# Comparison preregistration — nested vs independent wrongness

Date: 2026-09-20. Investigator: wave-7 formula-test-both.
Status: PREREGISTERED BEFORE COMPUTATION. Nothing below was computed yet.

## The question (Micah's ruling 1)

"Test both. Why are we forcing that to happen?" — should wrong-memories be
*forced* inside important-memories (nested), or should wrongness be
*independent* of importance?

## The two versions

- **VERSION N (nested, wave-6 recommendation):**
  `wrongN(m,v) = 1` iff `((3m + 7v + 9) mod 10 < 2)`.
  Fixed. Yield ~100/variant, P(important|wrong) = 1.0 by construction.
- **VERSION I (independent, designed here):**
  `wrongI(m,v) = 1` iff `((a·m + b·v + c) mod 10 < 3)`,
  with `a ∈ {1,3,7,9}` (coprime to 10, uniform residues), `b, c ∈ 0..9`
  chosen by the search below. Design target: P(important|wrong) ≈ 1/3
  ≈ P(important), exactly one shared residue per variant if achievable.

Importance (fixed, from prereg): `imp(m,v) = 1` iff
`((7m + 13v + 3) mod 10 < 3)` → per-variant residues v0:{1,4,7},
v1:{2,5,8}, v2:{3,6,9} (to be re-verified computationally, not trusted).

Horizon: m = 0..499, v ∈ {0,1,2} (S1 leg).

## Shared mechanics assumptions (same for both versions)

- A memory admitted at episode m with imp(m,v)=1 is revealed important
  25 episodes late and STRENGTHENed by the learner's own rule to 80–90.
- A memory with wrong(m,v)=1 receives contradiction revelations at
  m+25/+50/+75/+100 (wave-4/5 amendment), supplying the citations an
  80–90 erase requires.
- Therefore the **rigidity-test denominator** = #{m : wrong(m,v)=1 AND
  imp(m,v)=1} per variant: wrong memories that actually BECOME STRONG.
  (Matches wave-6 usage of R_wbs denominator.)

## Comparison criteria (pass/fail bars set now)

- **C1 Yield.** Per-variant wrong count in band 90–160. (Admits both by
  design: N≈100, I≈150. The comparison axis is correlation, not rate;
  raw counts reported.)
- **C2 Independence.** |P(important|wrong) − P(important)| ≤ 0.05 per
  variant required for I. N's value reported, not gated (it is nested
  by design).
- **C3 No starvation.** Rigidity denominator (wrong&important) ≥ 20 per
  variant for a version to be "usable". Rationale: the kill criterion is
  all-or-nothing (any single unrevised strong mistake kills Arm A), so
  20+ unanimous revisions is convincing; below 20 the test is thin.
- **C4 Blinding.** Period ≤ 10 for both (same predictability class as the
  importance signal). Report P(wrong|important) vs P(wrong): the leak
  through the importance-revelation channel.
- **C5 Hygiene.** Pressure-episode {100,200,300,400} and implant-episode
  {83,166,250,333,416} overlaps counted per variant (implant set carries
  the Defect-3 dependency — recompute if ruling 3 changes indexing).
  Flag any variant asymmetry.
- **C6 Verdict rule.** Recommend the version that (i) passes C3 in every
  variant, and (ii) gives the cleaner causal reading of "can TNN undo a
  strong mistake" — argued from the computed numbers, not pre-decided.
  Forcing (N) must justify its artificiality with test power; not
  forcing (I) must justify its smaller denominator as still decisive.

## VERSION I search procedure (deterministic, exhaustive)

Over a ∈ {1,3,7,9}, b ∈ 0..9, c ∈ 0..9, threshold < 3:
1. Require per-variant |wrongset ∩ imp(v)| == 1 exactly.
2. Require yield exactly 150/variant (follows from coprime slope).
3. Minimize total pressure-episode overlap, then total implant-episode
   overlap, then pick lexicographically smallest (a,b,c) — fully
   deterministic tie-break, no judgment calls.
If no candidate satisfies (1), report the failure honestly (negative
result) instead of relaxing the bar silently.
