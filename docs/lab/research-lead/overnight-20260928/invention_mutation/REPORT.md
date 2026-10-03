# REPORT.md -- Invention Hypothesis 1: structural mutation from failure

## Preregistration (frozen before implementation)

**H-MUT-1 (mutation creates the form).** On a plen-6 chain problem, with
only plen-3/4/5 MAPs in learner state, the mutate stage will extend the
plen-5 MAP by one cell, verify the extension against the goal, and
promote a new plen-6 MAP with DEP provenance to the plen-5 parent.
Predicted: TREAT T6 ans=306; new MAP plen=6 with exactly one DEP->MAP
edge to a plen-5 parent. ABL-MUT (mutation disabled) T6 ans=-2. FRESH
(no training) T6 ans=-2.
Kill bar: H-MUT-1 is KILLED if TREAT T6 != 306, or no plen-6 MAP is
promoted, or ABL-MUT T6 != -2, or FRESH T6 != -2.

**H-MUT-2 (the invented form is reusable).** On a fresh plen-6 problem in
the same workspace, the invented plen-6 MAP will be directly rebound (no
new mutation). Predicted: REUSE R6 ans=406 via rebind; no MUT-STAT detail
line fires.
Kill bar: H-MUT-2 is KILLED if R6 != 406, or R6 requires a new mutation.

**H-MUT-3 (open-ended iteration).** On a plen-7 problem, the plen-6
mutant itself will serve as mutation parent, producing a plen-7 MAP with
DEP provenance to the plen-6 mutant.
Predicted: ITERATE I7 ans=507; new MAP plen=7 with DEP->MAP to the plen-6
mutant.
Kill bar: H-MUT-3 is KILLED if I7 != 507, or the plen-7 MAP's MAP parent
is not the plen-6 mutant.

Determinism bar: 3/3 byte-identical runs.

## Method

Base: persistent-connections core (rebind + trial), unfrozen copy. Two
changes, both in the unfrozen layer: (1) gather depth 5 to 6 with a
non-overlapping path layout, so invented longer forms stay rebindable
(trial's construction bound is unchanged at plen<=5); (2) a new general
pipeline stage, mutate_try, after trial in ev_query.

mutate_try: for each chain MAP, longest plen first, stage it on the query
subject, execute to its endpoint, and check the "too short" signal:
facts continuing past the endpoint that no existing shape reaches. Each
continuing fact yields one extended chain (parent structure + 1 cell),
executed and verified; the first verifying extension is promoted with a
type-1 DEP edge to the parent. No MUTATE_MODE, no task label, no
plen-6 template anywhere in source.

## Results

TREAT (train plen-3/4/5, then plen-6 problem):
- TR3 ans=103, TR4 ans=114, TR5 ans=125 (all via trial). maps=3,
  bestplen=5.
- T6: RB-STAT tried=3 rejected=3 (all existing MAPs fail rebind).
  MUT-STAT parent=116 plen 5 -> 6 zmap=271. T6 ans=306.
- ZMAP id=271 plen=6, DEP->MAP 116 (plen=5), dep_facts=5, dep_maps=1.
- H-MUT-1: PASS.

REUSE (fresh plen-6 problem, same workspace):
- R6 ans=406. RB-STAT tried=4 rejected=3, no mutation detail line: the
  plen-6 MAP rebound directly.
- H-MUT-2: PASS.

ITERATE (plen-7 problem, same workspace):
- RB-STAT tried=5 rejected=5. MUT-STAT parent=271 plen 6 -> 7 zmap=549.
  I7 ans=507.
- ZMAP id=549 plen=7, DEP->MAP 271 (plen=6), dep_facts=6, dep_maps=1.
- Mutation lineage: 116 (plen 5, trial) -> 271 (plen 6, mutation) ->
  549 (plen 7, mutation of the mutant).
- H-MUT-3: PASS.

FRESH (no training): T6 ans=-2. No parents, trial rejects all 5.
ABL-MUT (mutation disabled, all else identical): T6 ans=-2.
RB-STAT tried=3 rejected=3, MUT-STAT tried=0 rejected=0, trial 5/5
rejected. The mutation stage is causal: identical system minus the
stage cannot solve the problem.

## Alternative explanations attacked

1. "Trial could reach plen-6." No: trial is bounded to k=2..4
   (plen<=5) by construction, and ABL-MUT keeps trial intact yet fails.
2. "Rebind could solve it." No: rebind stages exact shapes; the longest
   MAP is plen-5 and execution verifies wrong (305 != 306). The 3/3
   rejections are in the log.
3. "The gather-6 change did the work." No: ABL-MUT has gather-6 and
   still fails. Gather-6 is necessary for REUSE (rebinding plen-6) but
   not sufficient for T6.
4. "One lucky fact." The operator tried exactly the world's continuations
   (tried=1) and ITERATE repeats the success with a different parent and
   different facts. Deterministic across 3/3 runs.

## SUF analysis (source-underdetermined form)

Researcher-authored: the mutation operator itself (extend by one cell on
the "too short" signal, longest parent first, verify-then-promote).
Source-underdetermined: the final form. Which parent mutates depends on
the learner's history (here MAP 116, the plen-5 MAP from training); which
fact extends it depends on the world's data (here 305->306); whether the
extension survives depends on verification against the goal. Source
contains no plen-6 template, no plen-7 template, and no enumeration of
long forms. The operator is open-ended through iteration: every promoted
mutant becomes a parent, so reachable forms (plen 8, 9, ...) are
unbounded while source stays fixed.

Honest bound: this is L2 structural learning, not L3. The learner
constructs a genuinely new structure via a general mechanism, and the
exact structure did not exist in source; but the mutation strategy
(extend on "too short") is researcher-designed. The learner does not
invent the operator. The step toward L3 is learner-invented mutation
operators, not just learner-selected mutations.

Requirement check (Micah's 9): existing structures inadequate (all fail,
logged); learner creates new form (MAP 271/549); form
source-underdetermined (above); internally evaluated (t2_try_verify
before promote; rejections logged); useful (T6/I7 solved); persistent
(MAP nodes in learner state); reusable (R6 via direct rebind);
revisable (standard MAP layout with type-1 provenance, so the generic
revision machinery applies structurally; explicit revision test is
future work); transferable (mutant parents the next invention;
cross-subject reuse in R6).

## Verdict

INVENTION-MUTATION-COMPLETE. H-MUT-1 PASS, H-MUT-2 PASS, H-MUT-3 PASS,
3/3 deterministic, ablation causal, SUF analysis recorded.

## Follow-ups (not blocking)

- Explicit revision test on a mutant (contradict a licensing fact,
  verify generic revision updates the mutant).
- Learner-owned choice among mutation operators (extend vs shrink vs
  swap) from consequence records, replacing the researcher-fixed
  extend-only policy.
- Sealed test: a domain where the needed extension is not +1 chain
  length, to probe the operator's generality boundary.
