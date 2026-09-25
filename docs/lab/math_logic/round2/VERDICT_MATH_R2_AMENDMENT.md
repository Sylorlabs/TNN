# AMENDMENT to VERDICT_MATH_R2.md — corrected hypothesis judgments + KB4 results (2026-09-25)

## Why this amendment exists

The committed `VERDICT_MATH_R2.md` (commit `9f83fc3c`) reaches the correct
decision but judges the WRONG hypotheses in its "Hypotheses" section: it
labels H1 as "HYB long-chain", H2 as "REF-FIRST contradiction-blind", H3 as
"NFEE no-free-elimination", H4 as "LEARN-FORM learned formalizer", H5 as
"QUOT quota-bounded". Those are not the frozen hypotheses. The frozen
hypotheses are PREREG_MATH_R2.md §5:

- H1 contradiction-tolerance-is-the-value
- H2 interface-cost-always-loses
- H3 formalization-is-the-bottleneck
- H4 learned-formalization-beats-curated
- H5 hybrid-dominates

This amendment re-judges the FROZEN hypotheses from the raw evidence
(`results_formal.json`, `results_formal_all.json`, `results_b1n.json`,
direct wall-time re-measurement), adds the KB4 grader results, and confirms
the decision. The original verdict's decision, battery table, and primary-bar
tallies are UNCHANGED and correct.

## Corrected hypothesis verdicts (frozen bars)

**H1 contradiction-tolerance-is-the-value: FALSIFIED.**
Bar: a contradiction-tolerant engine (HYB, REF-FIRST, DUAL-R1) produces ≥50%
fewer incorrect conclusions than ONE-R1 on B5X (i.e. ≤18 vs ONE-R1's 36).
Measured B5X incorrect: ONE-R1 36 (all false_withheld), DUAL-R1 24
(false_derived), REF-FIRST 24 (false_derived), HYB 60, NFEE 60, LEARN-FORM 36.
Best tolerant improvement: 24 vs 36 = 33% fewer — below the 50% bar.
On multi-hop false rules, derive-through tolerance becomes gullibility
(24 false_derived) and withhold-everything becomes blindness (36 false_withheld);
neither discriminates. Round-1's KB5 result (tolerance wins on single-hop
false rules) does NOT generalize to multi-hop chains.

**H2 interface-cost-always-loses: FALSIFIED.**
Bar: an interfaced engine pays ≥2x wall time vs the fastest interface-free
engine at equal (±10%) derivation counts on B6X. Kill: matches within 1.5x.
DUAL-R1 (interfaced) vs ONE-R1 (interface-free): identical derivation counts
(121/112/105). Directly re-measured wall means, 3 runs each (cwd
`math_logic/`, binaries `one_b6x_bin`/`dual_b6x_bin`):
B6X_01 2.47s vs 2.03s (1.22x); B6X_02 2.74s vs 2.50s (1.10x);
B6X_03 2.78s vs 1.69s (1.65x).
Kill condition met on 2/3 problems (within 1.5x); the ≥2x prediction fails on
all three means. The interface cost is real but ~1.1–1.65x, not ≥2x.
(Round-1's 2.5x on 50-step B6 did not replicate at 100-step scale — the
interface overhead amortizes as derivations grow.)

**H3 formalization-is-the-bottleneck: SURVIVES.**
Bar (a): all engines solve ≤30% on B1N raw NL. Bar (b): each engine's
formal-analog-minus-NL gap exceeds the between-engine spread on formal analogs.
(a): ONE-R1/DUAL-R1/HYB/REF-FIRST/NFEE score 0/22 (exit 4 — no NL path).
LEARN-FORM: 10/22 DERIVED but **0/22 correct** — every derivation used the
single unfaithful P01 MP-template (`imp(p,q),p|-q`) stamped onto unrelated
content (P02 infinitude-of-primes, P11 pigeonhole geometry, P15 angle sums…);
the OPEN P05 (Goldbach) was falsely derived; even P01 (sqrt(2) irrationality,
a proof by contradiction) was misformalized as modus ponens.
(b): NL gaps are 80–100pp (formal ~100% → NL 0%) vs between-engine spread on
formal analogs ≤20pp (B4R 12/15 vs 15/15; B3R 9/10 vs 10/10).
Both conditions hold. H3 is the round's one surviving hypothesis: the engines
are mature on formal batteries; NL→formal is the wall.

**H4 learned-formalization-beats-curated: FALSIFIED.**
Bar: LEARN-FORM ≥70% schema-equivalence on B7F AND beats the curated baseline.
Measured: LEARN-FORM 2.5/100; curated baseline 47.9/100. Fails both conditions.
The 1-template learner abstains on 12/20 and scores 0–17 on the rest.

**H5 hybrid-dominates: FALSIFIED.**
Bar: HYB beats BOTH round-1 parents on ≥2 of the 3 primary bars.
Measured: PB1 0 pairwise wins (FAIL), PB2 PASS, PB3 60 incorrect vs 18 bar
(FAIL) → 1/3. HYB also misses B6X_03 (120-chain) and refutes everything on
B5X (0/60). The hybrid assembly does not deliver.

## KB4 audit coherence — MEASURED (no longer pending)

Three independent blinded grader subagents rated all 356 audit trails
(aliases A–F) 1–5 on circularity / unwarranted-steps / magic-knowledge.
No grader read the alias key; none ungradeable; each built an independent
mechanical step-verifier.

- **Inter-rater alpha (Krippendorff, ordinal): pooled 0.83 > 0.8 → bar MET.**
  Per-dimension: unwarranted 0.85, circularity 0.73, magic 0.45.
  The magic-dimension split is a genuine rubric-interpretation difference
  (does an elided-but-verifiable contradiction derivation count as "magic"?),
  not rater noise: all three graders independently flagged the SAME 5 broken
  trails (A069/A089/A118/A343/A356 — PBC subproofs whose first MP step cites
  the conclusion itself with a failed unification, then cite nonexistent
  statements C5 / C333–C433) and the SAME coarse-PBC families.
- **Prereg falsification check** ("any engine's mean exceeds DUAL-R1's by
  ≥1.0 → DUAL falsified as audit-hostile"): largest exceedance is NFEE over
  DUAL on unwarranted, +0.86 < 1.0. **DUAL-R1 NOT falsified as audit-hostile.**
- Cross-grader means (alias → engine):
  DUAL-R1 4.69 (circ 5.00 / unw 4.14 / magic 4.94),
  NFEE 5.00 (cleanest trails),
  ONE-R1 4.88, REF-FIRST 4.44 (unw 3.33 — coarsest: 78 single-step
  S_PBC_BWD trails elide the contradiction derivation, though two graders'
  provers confirmed the contradictions genuinely follow from cited premises),
  LEARN-FORM 4.88, HYB 4.95.
- The 5 broken subproofs sit under ONE-R1 (2), LEARN-FORM (2), HYB (1).

## Decision — CONFIRMED

**The round-1 DUAL verdict STANDS.** No new engine wins ≥2/3 primary bars
(PB1 pairwise wins ≥7/10; PB2 KB2 contrast; PB3 B5X incorrect ≤ half of worse
parent) against BOTH ONE-R1 and DUAL-R1. Best new engines (HYB, REF-FIRST,
LEARN-FORM) win exactly 1/3 (PB2). QUOT remains BLOCKED-WITH-EVIDENCE
(repair in progress at amendment time; lands as an addendum if it completes).

## Answer to the prereg question (unchanged, strengthened)

Was the engine space the limiting factor, or does the formalization bottleneck
dominate? **The formalization bottleneck dominates — and it is now the only
surviving hypothesis.** Inference engines are mature and nearly indistinguishable
on formal batteries; the multi-hop discrimination problem (B5X: no engine gets
both derivable and withholdable right) and the NL→formal wall (B1N: 0/22
correct for every engine; B7F: learned 2.5 vs curated 47.9) are where all
progress stopped. Micah's suspicion is confirmed in the strong form: the round
tested 7 engines and 5 hypotheses, and the binding constraint is not which
inference engine you pick — it is getting from raw language to a faithful
formal representation at all.
