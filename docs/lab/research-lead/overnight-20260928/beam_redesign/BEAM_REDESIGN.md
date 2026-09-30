# Beam Redesign: diversity-preserving search for compositional reuse

Status: DESIGN. Not a preregistration. A future builder must write its
own preregistration (prereg-first rule) before implementing anything
here. No implementation exists at this commit. No .zag written.

Date: 2026-09-30. Worker: Beam Search Redesigner.
Parent task: Q4 R3 failed (023b4f84a, Q4R3_RESULT.md). Arm 2
(compositional embedding E = (D AND Y4) OR ((NOT D) AND Y5)) failed:
reuse reached 53/64, never 64/64, in 24 IVs. The revival conjunction
(R1 and R2 and R3 and R4) is dead; this design targets bounded-L2
reuse robustness only. It does not revive Q4 and does not touch L3
or Criterion 0.

## 1. Problem restatement (grounded numbers)

From the committed R3 result (3/3 byte-identical, md5
7ed09fda269b59cdbbf75e0df720661c, pure Zag):

- A2-REUSE: hit_iv = 24 (budget exhausted), final_true = 53/64,
  HAS_D = 1. Bar required 64/64. A2-PASS = 0.
- Diagnostic replay (non-governing, /tmp only): from round 6 onward
  the beam top is a 3-op expression containing D that fits up to
  29/32 evidence but generalizes to 53/64. The true 4-op E was never
  generated in 25 beam extensions.
- Score arithmetic (per the reported numbers): score =
  10000 * (fit / 32) - 200 * opc. The 3-op overfitter at full
  evidence fit scores 10000 - 600 = 9400. The true 4-op E at full
  fit scores 10000 - 800 = 9200.
- E_SANITY 64/64: target and installed D signature verified. No
  harness defect. F-R3-SEAL never fired.

## 2. Root cause: the two-fold trap

Fold 1: the tax ceiling (absorbing states). At equal evidence fit,
a fewer-op expression always wins by 200 per op. A 3-op expression
that fully fits the 32 evidence points scores 9400, permanently
above any fully-fitting 4-op expression at 9200. Once a simpler
expression reaches full evidence fit, no more complex expression
can outscore it on evidence alone. Escape is possible only through
refuting evidence: new observations on which the overfitter is
wrong, dropping its fit below full.

Fold 2: the monoculture (no refuting evidence arrives). The beam
keeps the global top 32 by score. After the overfitter locks in,
all 32 are overfitter variants. The IV policy selects interventions
to maximize disagreement among the top 8 hypotheses. Eight
overfitter variants agree with each other, so no disagreement
exists, so no informative IV is selected, so no refuting evidence
arrives, so the overfitter keeps full fit, so Fold 1 holds it on
top forever. The true E is additionally never generated, because
every generation builds on overfitter parents.

The 200/opc tax is not wrong by itself. It is the same tax that
found the minimal D in Phase 1. The defect is the interaction of a
fixed tax with greedy monoculture selection: premature commitment
to a simpler evidence-fitting expression that permanently blocks
the true compositional form.

## 3. Candidate fixes evaluated

A. Niching (diversity-preserving beam). Partition the beam into
species by a generic structural signature and keep top-k per
species instead of a global top 32. Fixes Fold 2 directly: the
compositional building blocks (AND(D,Y4), NOT D, AND(~D,Y5)) each
survive in their own species, E can be generated, and the IV
hypothesis set becomes diverse so disagreement-driven IVs target
distinguishing combos and produce refuting evidence. Generic
search machinery: the signature is computed from the expression
tree with no knowledge of the target, family, or D. Risk: the
signature granularity is a new hyperparameter. Too fine splits the
beam into singletons (no selection pressure within species); too
coarse re-creates the monoculture.

B. Tax annealing. Start the tax at 0 and ramp to 200/opc over the
extension rounds. Lets complex candidates establish evidence fit
before the minimality preference bites. Generic schedule change,
no semantic content. Weakness on its own: at the final full tax,
the overfitter still beats E at equal full fit (9400 > 9200), so
annealing without refuting evidence only delays the trap. It is a
complement to A, not a substitute.

C. Explicit compositional construction operators. Rejected as the
primary fix. The demonstrated bottleneck is selection, not the
operator alphabet: E was never generated because parents were all
overfitters, not because no operator could form it. Adding
researcher-authored compositional operators risks drifting toward
dedicated semantic cases. Allowed only as a fallback if A+B is
built, preregistered, and still fails, and then only as generic
moves (e.g. embed a kept-library terminal as a subexpression),
never as target-shaped templates.

D. Diverse hypothesis set for IV selection (companion to A). Build
the IV disagreement set as the top 1 hypothesis per species (up to
8) instead of the global top 8. Same disagreement machinery,
diverse inputs. Without D, niching the beam but keeping a
monoculture IV set would preserve Fold 2.

Recommendation: A + B + D, conjunctive. C stays rejected unless
A+B+D is honestly built and fails.

## 4. Frozen design parameters

A future builder's prereg must adopt these or transparently amend
them before implementation. Defaults:

- Beam width: 32 total, unchanged (same compute order as the frozen
  beam).
- Species signature: (tree depth, sorted operator multiset),
  computed generically from each candidate expression tree. No
  target, family, or library knowledge enters the signature.
- Keep rule: top 4 per species, at most 8 species (4 x 8 = 32). If
  more than 8 species are non-empty, merge the two smallest
  (fewest members, tie broken by lower best score). If fewer than
  8, fill remaining slots from the global score ranking.
- IV hypothesis set: top 1 per species, up to 8 hypotheses. The
  existing disagreement-driven IV selection is otherwise unchanged.
- Tax schedule: tax(t) = round(200 * t / 25) for extension round t
  in 0..24. Early rounds explore; late rounds decide under the full
  minimality preference. The keep/score formula is otherwise
  unchanged.
- Compute guard: per-round candidate simulations must not exceed
  the old beam's per-round count by more than 10 percent.
  Niching bookkeeping is O(beam) and carries no simulation cost.

## 5. Why this addresses the root cause (trap trace)

With species kept, AND(D,Y4) survives in its own species even
while the overfitter leads globally. Cross-species parents let the
search generate E. Once E exists, it disagrees with the overfitter
on some input combos; both enter the per-species IV set;
disagreement-driven IVs target those combos; the resulting
evidence refutes the overfitter (its fit drops below 32/32);
under the late full tax, E at full fit (9200) now beats the
refuted overfitter (below 9400 and falling). Annealing gives the
4-op chain room to form in early rounds instead of being taxed
out at birth. Each fold of the trap is met by a specific
mechanism: Fold 1 by refuting evidence plus the late full tax,
Fold 2 by niching plus the diverse IV set.

## 6. Builder protocol (for the future worker)

1. Write a preregistration adopting or amending section 4, with
   kill bars, before any implementation. Prereg commit strictly
   precedes implementation (commit-order self-check).
2. Control first: reproduce R3-FAIL on the frozen old code
   (023b4f84a) to confirm the baseline still fails identically.
3. Implement the fix in a copy; the frozen learner source stays
   untouched.
4. Run Arms 1 and 2 under the R3 prereg bars (64/64 and reuse
   ratio). Arm 1 must not regress. Arm 3 stays DEFERRED.
5. Pure Zag at every stage, 3/3 byte-identical, zero Python,
   zero em/en dash bytes in loop documentation.

## 7. Falsifiers for this design

- F-DIVERSE-FAIL: Arm 2 still fails after a faithful build of
  sections 4-5. The design is wrong, not just unbuilt.
- F-REGRESS: Arm 1 passes before and fails after. The fix breaks
  what worked.
- F-BLOAT: the compute guard in section 4 is violated. Diversity
  must not be bought with an unbounded simulation budget.
- F-CASE: any fix component keys on target, family, or library
  identity. Generic machinery only; a dedicated semantic case
  kills the design on the spot.

## 8. Honest scope

This is a design document, not a result. No implementation, no
measurement, no claim beyond the trap analysis in section 2,
which rests on committed R3 evidence. If built and passing, the
outcome is bounded-L2 reuse robustness for one compositional
form, not L3, not Criterion 0, and not a Q4 revival (the
conjunction is dead: R1-FAIL, R3-FAIL, R4-FAIL). The defined next
target from the R3 result is met at the design level: a search
mechanism in which a simpler evidence-fitting expression cannot
permanently block the true compositional form.

## Kill bars (this design task)

- K1 (design complete): this document, committed below.
- K2 (addresses root cause): sections 2 and 5 trace both folds of
  the trap to specific mechanisms.
- K3 (no implementation): prose only. No .zag written or
  modified, no binaries, no runs.
