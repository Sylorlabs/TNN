# QUOT ADDENDUM to the MATH R2 verdict (2026-09-25)

Engine (d) QUOT ("admissible-support quotient") was BLOCKED-WITH-EVIDENCE at
verdict time and is judged here under the decision rule of the frozen
PREREG_MATH_R2.md §6, as corrected by VERDICT_MATH_R2_AMENDMENT.md:

> The round-1 verdict (DUAL wins) STANDS unless a new engine wins >=2 of the
> 3 primary bars against BOTH ONE-R1 and DUAL-R1.

Primary bars: PB1 = KB1X pairwise wins vs each round-1 parent (>=7/10);
PB2 = KB2 contrast sub-bar appropriate to the engine's confidence model;
PB3 = B5X incorrect conclusions <= half of the worse round-1 parent's count.

QUOT is not one of the frozen H1–H5 hypotheses (the amendment notes it enters
only via the decision rule). This addendum judges QUOT on the decision rule
alone.

## Engine

QUOT runs ONE forward match-and-bind pass to fixpoint; every claim carries a
support bitset of the contingent store items it depends on. Conflict = two
supports proving P and ¬P; a support is tainted iff it covers a conflict,
and tainted supports commit nothing. The commit decision additionally applies
a specificity rule (more-specific exception defeats the general rule), per
SPEC_QUOT.md §4. No referee object, no numeric confidence (confidence is
non-zero iff DERIVED), no NL formalizer (exits 4 on raw NL input).

Sources verified byte-identical (git blob SHA) to repair commit
`6574167232e22790af999a67f3b8cf78a4511526`; built with pinned toolchain
`znc_linux_x86_64_abed8aa1`. Repair-crew validation reproduced: penguin
specificity trace (penguin(tweety)->DERIVED, not(flies(tweety))->DERIVED,
flies(tweety)->WITHHOLD), B2 smoke OK, sealed guard exits 3 on all probe
vectors, zero-RNG grep clean, 3x byte-identical reruns with zero divergence
on every non-timeout problem. Full validation record:
`evidence/r2/quot_validation.md`.

## Battery results (QUOT)

Formal batteries (3 reruns/problem, byte-identical SHA across r0/r1/r2,
zero divergence on every completed problem; binary
`d4adc432c558b75c89461fc1ab1b957068842354a968e13c75157c1bf0003f7f`):

| Battery | Solved | Incorrect (false-derived / false-withheld) | Notes |
|---|---|---|---|
| B2R | 12/12 | 0 (0 / 0) | wall 172.3s |
| B3R | 9/10 | 1 (0 / 1) | miss B3_03 (withheld, sealed DERIVED); wall 88.3s |
| B4R | 15/15 | 0 (0 / 0) | wall 88.6s |
| B4X | 0/15 | 0 (engine failure, not scored) | all 15 EXIT_4: "universe failed" — term universe exceeds the 65,536-term table cap during `q_universe` (~2-3.5 min each); deterministic |
| B5X | 36/60 | 24 (24 / 0) | all 24 misses are sealed-WITHHELD problems with injected false rules, which QUOT derives from (misses: _04,_05,_09,_10,_14,_15,_19,_20 at each of L2/L3/L4); wall 142.7s |
| B6X | 1/2 scored | 1 (0 / 1) | B6X_01: rc=1 panic (slice index out of bounds), unscored; B6X_02 DERIVED correct; B6X_03 WITHHOLD vs sealed DERIVED; wall 7.0s |
| KB2 | 19/20 dual-wins | — | only loss pair 13 (B3_03); conf=1 iff DERIVED |
| B1N | 0/22 (abstain) | — | all 22 raw NL inputs exit rc=4 ("bad .form"): no NL formalizer |
| B7F | — (abstain) | — | 0 produced forms; score null (not scoreable, not zero) |

QUOT-native derivation counters (aggregates over ok problems; see
`evidence/r2/results_formal_quot.json` `deriv`/`deriv_totals`):

| Battery | committed facts | inserts | enq/pop | subproofs | conflicts |
|---|---|---|---|---|---|
| B2R | 2,704 | 13,663 | 5,489 | 0 | 0 |
| B3R | 2,423 | 12,151 | 4,843 | 0 | 0 |
| B4R | 1,494 | 7,509 | 2,980 | 0 | 0 |
| B5X | 11,280 | 81,860 | 2,540 | 0 | 60 |
| B6X | 776 | 10,436 | 7,443 | 0 | 0 |

(B5X's 60 conflicts = the injected false rules clashing with the honest
store on every problem; QUOT commits through them rather than withholding.)

## Primary bars vs the round-1 parents

Parent numbers (amendment / results_formal_all.json):
- B3R: ONE-R1 10/10, DUAL-R1 10/10 (both perfect).
- B5X incorrect: ONE-R1 36 (all false_withheld), DUAL-R1 24 (all
  false_derived). Worse parent = ONE-R1 -> PB3 bar = <=18.
- KB2: ONE-R1 20/20 + ONE-bar allpass; DUAL-R1 20/20.

**PB1** (KB1X pairwise wins >=7/10 on B3R): FAIL vs both parents. QUOT
solves 9/10; ONE-R1 and DUAL-R1 each solve 10/10, so QUOT has 0 pairwise
wins against each (and 1 pairwise loss, B3_03, against each). Bar not met.

**PB2** (KB2 contrast): PASS. 19/20 dual-wins (conf(solvable)=1 >
conf(open)=0 on 19 pairs; the DUAL-bar >=18/20 applied, same bar as every
other engine). Only loss is pair 13 (B3_03: QUOT withholds the solvable
form). ONE-R1 and DUAL-R1 each pass 20/20; QUOT passes the bar.

**PB3** (B5X incorrect <= 18): FAIL. QUOT incorrect = 24, all
false-derived: on every sealed-WITHHELD problem carrying an injected false
rule (24/60), QUOT derives a conclusion from the false rule instead of
withholding. (DUAL-R1 shows the identical 24-false-derived profile;
ONE-R1's 36 incorrect are all false-withheld.) 24 > 18: bar not met.

## Decision

The round-1 verdict (DUAL wins) STANDS. QUOT wins 1 of the 3 primary bars
(PB2 only) against each parent; the frozen decision rule requires >=2 of 3
against BOTH ONE-R1 and DUAL-R1 to overturn. QUOT does not overturn.

In plain terms: QUOT is a strong, honest formal engine on clean problems
(B2R/B4R perfect, B3R one safe withhold, KB2 contrast pass), but it has two
load-bearing limitations the round-2 stress batteries expose: (1) it cannot
build the term universe for B4X-scale stores (0/15, deterministic
universe-table exhaustion), and (2) it trusts injected false rules instead
of withholding (B5X 24 false-derived, failing PB3). Neither limitation is a
scoring artifact; both are deterministic engine properties.
