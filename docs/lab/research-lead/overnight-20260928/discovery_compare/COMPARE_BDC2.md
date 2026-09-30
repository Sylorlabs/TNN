# Discovery Comparator: B vs D vs C2 on Valley-Crossing

Date: 2026-09-30.
Status: ANALYSIS ONLY. No implementation. No new measurements.
Authority: compares committed results for B (`hyp_b/RESULT_HYPB.md`),
D (`hyp_d/HYPD_RESULT.md`), and the frozen C2 design (`hyp_c2/C2_DESIGN.md`)
plus C2 prereg (`hyp_c2_impl/PREREG_HYPC2.md`), against the frozen battery
(`discovery_battery/PREREG_BATTERY.md`, 425f7276d).

## 1. Task definitions (frozen battery)

- T0 2x+1: train x in 0..8 (9). Target 2x+1.
- T1 abs: train x in -8..8 (17). Target |x|.
- T2 x mod 3: train x in 0..16 (17).
- T3 parity: train a,b in 0..4 (25). Target 1 iff (a+b) even.
- T4 nested abs: train x in -6..6 (13). Target ||x|-2|.
- T5 fragment composition: train x in -4..8 (13). Target |x|+|x-2|.
- Budget per (hypothesis, task): 1M evaluations or 300s.
- SOLVE: exact integer equality on ALL train episodes.

## 2. Mechanism comparison (K1)

### Hypothesis B: semantic fragment induction

Routing: kink-driven. Kinked tasks go to the assembler (piecewise
construction from probe comparisons); unkinked tasks go to the base
(straight-line search). Composition route retrieves library fragments
by behavioral kink-subset match and emits CALLs.

Retention: a library of fragments, each carrying a semantic signature
(behavior on a probe set), kink set, generality verdict, and
input-agnosticism flag. Promotion requires passing a generality gate;
the gate refused a train-exact non-general conditional on T2.

Valley-crossing mechanism: PERSISTENT REUSABLE STRUCTURE. Induce the
ABS fragment once on T1 ([DUP,PUSH0,LT,JZ6,NEG,JMP6], conditional,
input-agnostic, generality ok), then retrieve it twice on T4
([IN0,CALL0,PUSH2,SUB,CALL0]) and twice on T5
([IN0,CALL0,IN0,PUSH2,SUB,CALL0,ADD]). The 1-CALL phase was
exhaustively shown insufficient (2380 candidates, none exact), so the
2-CALL composition is doing real work.

Causal evidence: the transfer pairs. T4 carried 13544 evals SOLVE vs
fresh 2189 evals FAIL; T5 carried 142018 evals SOLVE vs fresh 1686
evals FAIL. Carried solves, fresh fails, budget respected on all
tasks (max 142018 evals). This is the cleanest valley-crossing
evidence in the program: the library is isolated as the causal
contributor.

### Hypothesis D: MAP-Elites / novelty control

Mechanism: an archive of elites indexed by behavior-descriptor niche.
Mutation is single-op replace/insert/delete; a candidate enters the
archive if it improves its niche. No score-ranked population across
iterations, but thousands of elites are retained per task
(T0->654, T1->1790, T2->2988, T3->12068, T4->9980, T5->7064).

Valley-crossing mechanism: NONE DEMONSTRATED. T0 was solved by a
single-OP replace (PUSH -9 to PUSH 1) on a lucky parent; the predicted
deceptive-prefix construction never occurred (0 PREFIX_EVAL events in
4.4M evals), so the T0 mechanism is UNCONFIRMED per the battery rule
(outcome match without mechanism trace). T3, T4, T5 each exhausted the
1M evaluation budget. T1 was solved, but see section 3.

D is a VALID control (D-F1 and D-F2 did not fire): it shows what a
conventional MAP-Elites baseline achieves on this battery. It is not
a discovery advance.

### Hypothesis C2: counterexample-driven growth with non-myopic repair

Status: design complete (e658766bd), prereg frozen, implementation in
progress. Not yet tested.

Mechanism: single growing program, no population, no fragment
library. The driver is the counterexample set. Three remedies for
C1's falsified greedy repair: (a) lookahead repair appending op
sequences of length 1..3 with two-phase evaluation and argmax by
(pass count desc, length asc, lex asc); (b) net-progress criterion
(fix e AND strictly increase total pass count, replacing no-breakage);
(c) chronological backtracking with (prefix, extension) tabu, BMAX=6.
Split operator unchanged from C1 (frozen probe family), firing from
best_P on stagnation.

Valley-crossing mechanism (predicted): NON-MYOPIC REPAIR. Lookahead
finds multi-op fixes (PUSH 2 then MUL) that single-op repair cannot
see; backtracking retracts constant traps ([PUSH 1] on T0 episode
(0,1)); net-progress permits stepping stones that sacrifice passing
episodes for net gain. The design walkthrough predicts T0 SOLVE with
3 repairs and 1 backtrack.

### Side-by-side outcomes

Task | B | D | C2 (predicted)
T0 2x+1 | SOLVE base, 94 evals | SOLVE, 39082 evals, mechanism UNCONFIRMED | SOLVE, <=2 backtracks
T1 abs | SOLVE assembly + ABS fragment | SOLVE via MOD trick (see sec 3) | SOLVE via splits, <=4
T2 mod3 | SOLVE assembly, induction rejected | SOLVE, 134414 evals | SOLVE, 1 repair
T3 parity | SOLVE base, 17728 evals | FAIL, 1M evals | SOLVE, 1 repair, no splits
T4 nested | SOLVE composition, 2 CALLs | FAIL carried+fresh, 1M | SOLVE via nested splits, 0 CALLs
T5 fragcomp | SOLVE composition, 2 CALLs | FAIL carried+fresh, 1M | SOLVE via splits

Budget: B respected everywhere (max 142018). D hit 1M on T3/T4/T5.
C2 has the 1M budget with falsifier C2-F5.

Purity: B K4 VIOLATED (python3 twice, disclosed). D K4 VIOLATED
(python3 byte-check, disclosed). C2 prereg freezes pure Zag; K4 to be
verified on implementation.

## 3. D's major finding and its blast radius

D discovered [IN0 PUSH:-2 IN0 MUL MOD NEG NEG], a 7-op straight-line
program computing |x| exactly (17/17 train, 8/8 hidden) via
mod_nonneg(x, -2x) with truncated division. This overturns the
architecture review's load-bearing assumption that the GENEXEC2 op
alphabet has no comparison and that abs "matches the straight-line
limit." T1 does NOT discriminate conditional from straight-line
machinery.

Blast radius:

1. T1 is compromised as a conditional-structure discriminator for ALL
   hypotheses. B's T1 solve used genuine conditional machinery
   ([DUP,PUSH0,LT,JZ6,NEG,JMP6] with LT/JZ), so B's fragment claim
   survives, but any hypothesis solving T1 via the MOD trick has not
   demonstrated conditional structure.
2. T4 and T5 build on |x|. Since |x| is straight-line expressible in
   7 ops, T4/T5 may also be straight-line solvable (harder to find;
   D failed at 1M evals). The battery's discrimination matrix for
   T1/T4/T5 must be re-examined before T6. A battery redesign worker
   has been spawned for this.
3. C2's frozen T1 prediction ("SOLVE via splits") is now suspect.
   C2's lookahead repair uses argmax by pass count over length 1..3
   sequences. The MOD trick is 7 ops, longer than one repair step,
   but C2 grows incrementally: a partial MOD-trick prefix could
   accumulate pass count and be extended across multiple repairs
   without ever splitting. If C2 solves T1 via straight-line repair
   (MOD trick) rather than splits, the outcome matches but the
   mechanism is UNCONFIRMED per the battery confirmation rule, and
   the "split for conditionals" story is weakened. The C2
   implementer must log whether T1 solves via straight-line repair
   or via SPLIT events; this distinction is checkable in the trace.
4. C2's T4 prediction ("SOLVE via nested splits, 0 CALLs") faces the
   same hazard in reverse: if C2 finds a straight-line MOD-trick
   solution for ||x|-2|, that is outcome SOLVE with mechanism
   UNCONFIRMED against the frozen prediction, and it further erodes
   the battery rather than confirming C2.

None of this invalidates B's T4/T5 results: B's solutions contain
explicit CALLs to the induced ABS fragment with retrieval traces,
which is mechanism evidence independent of the MOD trick.

## 4. What C2 must show to advance beyond B and D (K2)

C2 is tested against frozen falsifiers C2-F1..F5. Advancement means:

1. T0 SOLVE with the predicted repair/backtrack trace (C2-F1, C2-F4).
   This is the core claim: greedy repair's valley defect is fixed by
   lookahead plus backtracking. D's T0 solve was luck (UNCONFIRMED
   mechanism); B's T0 solve was trivial base search (94 evals, no
   valley). C2 must show the valley actually crossed by repair:
   constant trap tried, retracted via BACKTRACK, structural sequence
   found via lookahead. If the trace shows degenerate splitting
   instead, C2-F3 fires and C2 has recreated C1's failure mode.
2. T4 SOLVE via nested SPLITs with 0 CALLs (C2-F2). This is the key
   discriminator against B: the same task B solved via fragment
   composition must be solved by a third distinct mechanism,
   counterexample-driven piecewise growth. If C2's T4 trace shows
   CALLs, C2-F2 fires. If it shows straight-line MOD-trick repair,
   the mechanism is UNCONFIRMED (section 3, item 4).
3. T3 SOLVE via single REPAIR [IN0, PUSH 2, MOD] with no splits.
   C1 memorized T3 with 24 splits; D failed T3 at 1M evals; B solved
   it via base search in 17728 evals. C2 must show argmax-by-count
   finding the general solution before splitting is considered.
   This tests whether the net-progress criterion plus lookahead
   avoids both C1's memorization trap and D's search failure.
4. Budget discipline on all tasks (C2-F5). B never exceeded 142k
   evals; D hit 1M three times. C2's per-fix search enumerates
   about 40k sequences; the design claims well under 100k
   evaluations per fix. If any task exceeds 1M, C2 is not a bounded
   discovery mechanism.

What would NOT count as advancement: solving T0-T5 with outcome
match but mechanism UNCONFIRMED on the load-bearing tasks (T0
repair/backtrack trace, T4 nested splits). The battery confirmation
rule is explicit: outcome without the predicted mechanism trace
neither confirms nor falsifies.

## 5. Architecture-review trigger (K3)

The frontier's treadmill watch (H-NEW-6) states: if B, D, and C2 all
plateau at budget-shaped depths, stop the lineage and open the
architecture review. This section makes that trigger operational.

Definitions. A mechanism has plateaued at budget-shaped depth when,
on the redesigned battery (tasks provably requiring conditional
structure, per the battery redesign worker), its max solvable valley
depth scales with the evaluation budget rather than showing a
mechanism-specific ceiling. Concretely: doubling the budget from 1M
to 2M evaluations doubles the crossable valley depth (measured in
the H-NEW-6 parameterized valley battery, depths 1..k). A
mechanism-specific ceiling is the opposite: depth stops increasing
while budget increases, with failures showing a characteristic
signature (B: kink-routing misfires; C2: backtrack exhaustion at
BMAX; D: archive saturation).

Trigger conditions (any one opens the review):

- T-A (mechanism convergence): on the redesigned battery, B, C2,
  and D all fail at the same valley depth k*, and k* moves with
  the budget. The three mechanisms are then budget-bound variants
  of one search process, not distinct discovery capabilities.
- T-B (C2 falsification): C2 fires C2-F1 (T0 fail), C2-F4 (T0 needs
  more than 6 backtracks), or C2-F3 (degenerate splits). The
  non-myopic repair lineage is then exhausted: greedy (C1)
  falsified, non-myopic (C2) falsified, and the remaining
  counterexample-driven growth idea has no live variant.
- T-C (battery exhaustion): the redesigned battery shows that every
  valley deeper than depth d* (for small d*, e.g. 2) is unsolvable
  by all three mechanisms within 10x budget, and the failures are
  all budget-shaped. The representation (GENEXEC2 straight-line
  plus splits plus fragments) is then the binding constraint, not
  any mechanism's search policy.

What the review must answer (per the standing architecture-review
trigger): "Is the current representation itself wrong?" Three
generations (C1 greedy, C2 non-myopic, plus B's fragment library as
the adjacent dimension) would then have repaired the search policy
while the representation stayed fixed. The review may not spawn a
C3/D2/B2 that keeps GENEXEC2 straight-line-plus-split as the
program form; it must examine whether the program representation,
the episode encoding, or the train/hidden split is the defect.

Sequencing note: the trigger is evaluated AFTER C2 results land AND
the battery redesign lands, using the H-NEW-6 valley-depth battery
(depths 1..k, max crossable depth per mechanism at fixed budget).
Do not open the review on C2's raw T0-T5 outcomes alone, because
D's MOD-trick finding means the current battery does not measure
what it claims to measure.

## 6. Honest scope

- B and D both violated K4 (Python use, disclosed). Neither
  implementation's logic may be adopted without a clean rerun, per
  the standing literal purity rule. The comparison above uses their
  reported traces as evidence about task structure (the MOD trick
  is verifiable from the committed program text), not as adoptable
  mechanisms.
- B's BUILD-FAIL includes K3 not met (T2 induction rejected). The
  generality gate's refusal is honest mechanism behavior, but it
  leaves B's periodic-structure handling unproven.
- C2 is untested; section 4 lists what its frozen predictions
  require. This document makes no claim about C2's outcomes.
- The battery redesign worker's output may change the task set;
  sections 3 and 5 are written to survive that change.

**Builder label: COMPARE-COMPLETE.**
