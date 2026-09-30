# Beam Design Reconciliation

Date: 2026-09-30. Worker: Beam Design Reconciler.
Status: DESIGN ONLY. No implementation. No code written or modified.

## Source designs

- Design 1: `BEAM_REDESIGN.md`, commit `27a8fd108` (niching + tax annealing + diverse IV set, sections A/B/D; C rejected).
- Design 2: `BEAM_EVIDENCE_DESIGN.md`, commit `e37b04c47` (Pareto-diverse beam, D1-D5).

Both commits verified in ancestry of `tnn-native-lab` via `git merge-base --is-ancestor`.

Design 1 was written against R3 Arm 2 (`023b4f84a`): the beam locks onto a
3-op overfitter and the true 4-op E is never generated. Design 2 was written
against R1 (`e40cb1b51`) plus R3: evidence fit never reaches 32/32
(24-31/32), tax-off ties on 3/5 seeds (TAXOFF_UNIQ=0), and the same
compositional blocking.

## 1. Overlaps (what both designs agree on)

1. The same score arithmetic: `sc = 10000 * (fit/32) - 200 * opc`. A 3-op
   overfitter at full evidence fit scores 9400; the true 4-op E at full fit
   scores 9200. The simpler evidence-fitting expression permanently wins on
   evidence alone.
2. The same escape condition: only refuting evidence (new observations on
   which the overfitter is wrong) can drop it below full fit. Both designs
   therefore route through IV diversity: the disagreement-driven IV selector
   must be fed diverse hypotheses so it can target distinguishing combos.
3. The same honesty: at full fit, the overfitter still beats E on the
   simplicity preference. Neither design claims to make E win without
   refuting evidence. Both are bounded-L2 search improvements; neither
   claims L3, Criterion 0, or a Q4 revival.
4. Both reject dedicated semantic cases and researcher-authored
   compositional operators as the primary fix (Design 1 C rejected;
   Design 2 "no new semantic cases").
5. Both require no regression on what already works (Design 1 F-REGRESS;
   Design 2 F-NOREGRESS), control-first builds, prereg-first, pure Zag,
   3/3 byte-identical determinism.

## 2. Conflicts (where the designs differ)

| # | Design 1 (niching) | Design 2 (Pareto) |
|---|--------------------|--------------------|
| W | Beam width 32, explicit compute guard (per-round sims within 10 percent of frozen beam) | Beam width 64, no compute guard |
| R | Retention: scalar score within species (top 4 per species) | Retention: global Pareto dominance (non-dominated kept, cap 64) |
| T | Tax: linear annealing, `tax(t) = round(200*t/25)` over 25 rounds | Tax: binary two-phase (rounds 1-16 accuracy only; 17-24 accuracy then opc tie-break) |
| B | Tie-breaking: unaddressed (node-ID arbitrariness remains) | Tie-breaking redesigned: disagreement distance, operator-histogram novelty, recency |
| V | IV set: redesigned (top 1 per species, up to 8) | IV set: unchanged selector (relies on beam content) |
| F | Diversity: hard species partitions (depth, sorted op multiset), max 8 species | Diversity: soft floor (8 of 64 slots for novelty, acc >= 50 percent) |
| P | Tie reporting: unaddressed (R1 TAXOFF_UNIQ issue untouched) | Tie reporting: UNDERDETERMINED(N_tie, opc_range) vs DEFECT only for syntactic duplicates |

## 3. The decisive complementarity

Pareto retention and niching are not redundant. They fix different defects.

Pareto fixes the exploration defect (Design 2 Defect 1, the R1 evidence-fit
failure). With niching-plus-scalar-score, a 5-op intermediate at 28/32
(score 7750) can still be pushed out of its species by a 3-op expression at
30/32 (score 8775), even when the 5-op is on the path to the true solution.
Pareto never prunes a higher-accuracy candidate for a lower-accuracy one, so
the max-accuracy path survives exploration. Niching alone does not guarantee
this.

Niching fixes the compositional defect (Design 1 Fold 1, the R3 failure).
Under pure global Pareto, once the overfitter reaches full fit it strictly
dominates E: equal accuracy (32/32), strictly fewer ops (3 < 4). A pure
Pareto beam would prune E at exactly the moment E matters most. Per-species
retention keeps E alive in its own species even when globally dominated,
because retention is per-species rather than global. Pareto alone does not
guarantee this.

Conclusion: a correct fix needs both. Pareto protects the accuracy path
during exploration; niching protects the compositional form at and after
full overfitter fit. Neither subsumes the other.

## 4. Recommended unified design (U1-U7)

Recommendation: build the unified design below, not either source design
alone. The builder preregisters against this document.

- U1 Pareto retention within species (from Design 2 D1). Within each
  species, retain non-dominated candidates (accuracy >= and opc <=, one
  strict); never prune a higher-accuracy candidate for a lower-accuracy one.
- U2 Niching (from Design 1 A). Species signature: (tree depth, sorted
  operator multiset), computed generically, no target/family/library
  knowledge. Top 4 per species, at most 8 species, total cap 32 (Design 1
  compute guard retained; Design 2's width 64 rejected to keep per-round
  simulations within 10 percent of the frozen beam).
- U3 Two-phase tax schedule (from Design 2 D2, chosen over Design 1 B).
  Rounds 1-16: rank by accuracy alone (tax computed, ignored). Rounds
  17-24: rank by accuracy, break ties by lower opc. The linear annealing
  schedule is recorded as an allowed builder variant only via transparent
  prereg amendment; two-phase is the default because it is explicit and
  auditable, and both schedules share the honest property that at full fit
  the overfitter still wins on opc absent refuting evidence.
- U4 Diverse IV hypothesis set (from Design 1 D). Top 1 per species, up to
  8 hypotheses, into the otherwise unchanged disagreement-driven IV
  selector.
- U5 Principled tie-breaking (from Design 2 D3). Within-species ties:
  (a) evidence-disagreement distance from beam consensus, (b) operator
  histogram novelty, (c) recency. Replaces node-ID arbitrariness (Design
  1's gap; addresses the R1 TAXOFF_UNIQ signal).
- U6 Reduced diversity floor (from Design 2 D4, resized for width 32).
  Reserve 4 of 32 slots for structurally novel candidates (acc >= 50
  percent) regardless of species rank. Rationale: niching covers the steady
  state, but in early rounds the beam can collapse to 1-2 species (all
  expressions simple), where niching provides no diversity. The floor
  protects those rounds.
- U7 Honest tie reporting (from Design 2 D5, adopted verbatim). Replace
  the binary taxoff_unique diagnostic with UNDERDETERMINED(N_tie,
  opc_range) when multiple beam members share max accuracy; report DEFECT
  only when all tied expressions are syntactically identical. (Design 1's
  gap.)

Retired: the scalar score formula for retention (kept implicitly only as
the final accuracy-then-opc pick); Design 2's beam width 64; Design 1's
annealing as default; explicit compositional operators (still rejected).

## 5. Trap trace for the unified design

R3 Arm 2: the 3-op overfitter and 4-op partials coexist (U1 keeps both as
non-dominated while the overfitter is below full fit). E's components
survive in their own species (U2) even after the overfitter reaches full
fit, where Pareto alone would prune them. E gets generated; E and the
overfitter both enter the per-species IV set (U4); disagreement-driven IVs
target distinguishing combos; refuting evidence drops the overfitter below
full fit; under the consolidation-phase tax (U3), E at full fit now beats
the refuted overfitter. U5 keeps the tie-breaking informative; U6 keeps
early rounds diverse; U7 reports genuine underdetermination honestly.

R1 F-PARCOND: Pareto retention (U1) preserves the max-accuracy path that
the scalar score pruned, so the beam can reach 32/32 fit where a fitting
expression is reachable by the candidate generator. U5 removes the
arbitrary node-ID tie-breaking behind the TAXOFF_UNIQ=0 signal; U7
replaces the binary defect flag with an honest underdetermination report.

## 6. Falsifiers for the future builder (union, deduplicated)

- F-DIVERSE-FAIL (Design 1): Arm 2 still fails after a faithful build of
  U1-U7. The design is wrong, not just unbuilt.
- F-FIT (Design 2): on a task where a 32/32-fitting expression is in the
  reachable candidate space, EVFIT must equal 32/32.
- F-NODOM (Design 2, scoped to species): instrument retention; assert no
  pruned candidate was non-dominated within its species at prune time.
- F-TIE-HONEST (Design 2): on a task with known underdetermination, the
  report must say UNDERDETERMINED with correct N_tie, not DEFECT.
- F-REGRESS (merged): Arm 1 (R3) and Phase-1 64/64 tasks must not regress.
- F-BLOAT (Design 1): per-round candidate simulations must not exceed the
  frozen beam's per-round count by more than 10 percent.
- F-CASE (Design 1): any component keying on target, family, or library
  identity kills the design. Generic machinery only.

## 7. Builder protocol (both designs agree; adopted unchanged)

1. Preregistration adopting or amending section 4, with kill bars, before
   any implementation. Prereg commit strictly precedes implementation
   (commit-order self-check).
2. Control first: reproduce R3-FAIL on the frozen old code (`023b4f84a`)
   and R1-FAIL on the frozen R1 code (`e40cb1b51`) to confirm baselines.
3. Implement in a copy; frozen learner sources stay untouched.
4. Run R1 F-PARCOND seeds and R3 Arms 1 and 2 under the frozen bars.
   Arm 1 must not regress. Arm 3 stays DEFERRED.
5. Pure Zag at every stage, 3/3 byte-identical, zero Python, zero em/en
   dash bytes in loop documentation.

## 8. Honest scope

Design only, no result. If built and passing, the outcome is bounded-L2
search robustness for compositional reuse and evidence fitting: not L3,
not Criterion 0, and not a Q4 revival (the conjunction is dead: R1-FAIL,
R3-FAIL, R4-FAIL). Fitting 32/32 does not imply 64/64 generalization;
generalization still depends on the evidence being representative.

## Kill bars (this reconciliation task)

- K1 (reconciliation complete): this document compares both designs
  (sections 1-2), identifies the decisive complementarity (section 3),
  and specifies the unified design (sections 4-7).
- K2 (recommendation made): section 4 recommends the unified U1-U7
  design over either source design alone, with explicit adopt/reject
  decisions for every conflicting component.
- K3 (no implementation): prose only. No .zag written or modified, no
  binaries, no runs. Zero Python used at every stage (shell, git, and the
  shell-only check_no_dash.sh snippet for dash verification).

## Governance notes

- Observed during this task: untracked `beam_impl/` run outputs exist in
  the worktree (a Design-1 builder is in flight). This reconciliation does
  not touch those files. The parent should decide whether to redirect that
  builder to the unified design or let it complete as a Design-1 control
  run; either outcome is informative (a Design-1 build doubles as the
  U-minus-Pareto ablation).
- The contaminated research paper was not touched. Other workers' staged
  and untracked files were not touched.
