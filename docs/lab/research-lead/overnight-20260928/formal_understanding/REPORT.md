# REPORT: Formal Understanding Worker

## Verdict: FORMAL-UNDERSTANDING-COMPLETE

## Claim tested

Constitutional claim (Section 8): Once TNN has complete operational
knowledge of a formal system, certain elementary mistakes should
disappear. Concretely: after TNN demonstrably masters a tiny expression
language (grammar, semantics, constraints, composition), novel
construction tasks should yield syntactically valid, semantically valid,
constraint-satisfying expressions, not impossible forms.

## Formal system: EXL

- Literals 0..9. Operators ADD (+), MUL (*).
- Grammar: E := ADD(lit,lit) | MUL(lit,lit) (one binary level).
- Constraint: every value < 64; operators only ADD/MUL.
- Semantics: standard arithmetic.
- Encoding: P(a,b) = a*16+b (injective for a,b in 0..15).
- Relations: ADD=41, MUL=42, DADD=43, DMUL=44, BUILD=45, SUB=46.

Taught (deterministic order, via ev_teach_in):
- Eval: all (P(a,b),ADD,a+b) and (P(a,b),MUL,a*b) for a,b in 0..9
  with value < 64. About 196 facts. This is the semantics.
- Decomp: (T,DADD,P(a,b)) for a+b==T, (T,DMUL,P(a,b)) for a*b==T,
  for T in 2..9, TRAIN targets, TEST targets, and collision probes.
  About 162 facts. This is the grammar (what decompositions exist).
- BUILD: canonical (T,BUILD,P(a0,b0)) for 8 TRAIN targets only.
  No BUILD facts for TEST targets (novelty).

TEST targets (11): 10,11,12,13,14,15,28,30,42,45,63.
Chosen so (T mod 16) > 9: they never collide with a taught
pair-encoding subject, isolating the construction mechanism from
encoding accidents. All are decomposable within the taught grammar.

## Results (3/3 byte-identical runs, SHA-256 27774ec8...)

### Mastery: 10/10 (both states)

M1 (P(2,3),ADD)=5. M2 (P(4,5),MUL)=20. M3 (P(7,8),MUL)=56.
M4 (16,DADD)=121=P(7,9), 7+9=16. M5 (21,DMUL)=55=P(3,7), 3*7=21.
M6 (16,BUILD)=121, valid decomposition. M7 (P(2,3),SUB)=-2 (miss).
M8 (P(10,10),ADD)=-2 (miss, literals out of range).
M9 (81,DADD)=-2 (miss, untaught target). M10 (P(0,5),MUL)=0.
The 10/10 bar is met; the experiment is valid.

### Novel construction, control arm (base t2_trial, masked): 0/11 valid

Every construction was classified INVALID (class 2, multi-dep).
Representative outputs:
- T=10 produced 9, via chain [10, P(1,9), 9]: decompose 10 into
  (1,9), then evaluate 1+9=9. The "expression" is 9, not a pair.
- T=42 produced 13, via [42, P(6,7), 13]: 6+7=13. Not a pair.
- T=63 produced 16, via [63, P(7,9), 16]: 7+9=16. Not a pair.

The trial prefers longer chains (k=2..4 before the len-2 fallback),
and the len-3 decomp-then-eval paths are always executable, so the
masked trial accepts the first one. The result is a VALUE, not an
EXPRESSION. Syntactic validity: 0%. Semantic validity: 0% (the outputs
do not denote decompositions of T). Constraint satisfaction: the
outputs violate the grammar (BUILD must yield a pair).

Collision probes (T=48=P(3,0), T=54=P(3,6)): both class 2.
T=48 produced 0 via [(48,ADD,3),(3,MUL,0)]: the pair-encoding collision
let the eval fact (48,ADD,3) hijack the search before any DMUL fact
was considered. Documented as predicted.

### Novel construction, treatment arm (fu_trial_build): 11/11 valid

All 11 classified VALID (class 1): single DADD/DMUL dep, pair decodes
to a,b in 0..9, TNN's own eval knowledge confirms op(a,b)==T.
- 10=P(1,9), 11=P(2,9), 12=P(3,9), 13=P(4,9), 14=P(5,9), 15=P(6,9),
  28=P(4,7), 30=P(5,6), 42=P(6,7), 45=P(5,9), 63=P(7,9).
Syntactic validity 100%, semantic validity 100%, constraints 100%.

### Two-level recursive probe: 3/3

Driver-recursed, TNN decomposition at each step:
36=(0+9)*(0+4), 48=(0+6)*(0+8), 30=(0+5)*(0+6). All validated.

## Architectural analysis

### Why mastery does not constrain construction

The constitutional claim is FALSIFIED for the base architecture and
CONFIRMED for the treatment. TNN-2 scores 10/10 on mastery yet its
native construction mechanism produces impossible forms on 11/11 novel
targets. The architectural reasons:

1. Grammar-blind search. t2_trial gathers BFS paths over ALL relations
   and assembles executable chains with no notion of what BUILD means.
   It does not know that a BUILD answer must be a pair licensed by a
   single DADD/DMUL fact. The knowledge (decomp facts) exists in the
   store, but nothing in the trial consults the GRAMMAR of the task.

2. Length preference over validity. The k=2..4 loop tries longer chains
   first. The len-3 decomp-then-eval paths are always executable, so
   they are always accepted before the len-2 fallback that would have
   produced a valid pair. The search order is composition-preserving in
   intent but validity-destroying in effect for construction tasks.

3. Masked acceptance cannot see form. With masked=1, any executable
   output is accepted. There is no check that the output has the right
   FORM (a pair), only that the chain ran.

### What closes the gap (treatment)

fu_trial_build adds two things:
- A grammar restriction: only single-link candidates licensed by
  DADD/DMUL facts. RESEARCHER-AUTHORED. This encodes BUILD's grammar.
  It is the piece TNN-2 cannot supply itself.
- Learner-owned semantic verification: each candidate pair is checked
  against TNN's OWN eval knowledge (fu_eval_known). The VALUES are
  learner-owned; only the lookup procedure is driver code.

Result: 11/11 valid. The grammar restriction is doing the heavy
lifting; the semantic check is a backstop that never fired (all first
candidates passed).

### The honest accounting

The treatment does NOT show TNN learning the grammar. It shows that
IF the grammar is enforced (by the researcher) AND the semantics are
in TNN's own state, THEN construction is perfect. The composition
worker's negative (TNN-2 does not compose) is consistent: TNN-2 has no
mechanism to derive or enforce a task grammar from its knowledge.

### Additional architectural finding: node leak on rejected trial

While building this experiment, a pathological behavior was found:
t2_trial permanently allocates ~13 nodes per candidate chain, including
REJECTED candidates. A non-masked miss query gathering 96 paths burns
through the 1024-node store and never finishes (observed: 14+ minutes,
root node ids climbing past 1000). This forced the mastery miss probes
(M7/M8/M9) to use direct retrieval (activate) instead of the full
query path. The leak means TNN-2's trial has no search budget and no
cleanup; every failed construction permanently consumes capacity.
This is independent of the formal-understanding claim but material to
any future construction work.

## Researcher-owned vs learner-owned

- Researcher-owned: EXL definition, pair encoding, relation ids,
  teach order, TEST/TRAIN split, the grammar restriction in
  fu_trial_build (only DADD/DMUL single links), the classification
  rubric, the two-level probe recursion.
- Learner-owned: all eval/decomp/BUILD facts (in TNN state), the
  semantic verification values (fu_eval_known reads TNN state),
  the promoted MAPs and their DEP edges.
- The treatment's 11/11 does not transfer grammar authority to the
  learner. A future experiment should test whether TNN can DERIVE the
  grammar restriction from the BUILD examples (TRAIN) and apply it to
  TEST. That is the natural next step.

## Metrics

- Cognition lines added: 0 (no base modifications). New files only.
- Modes/bridges/handlers: 0. Semantic cases: 0.
- Determinism: 3/3 byte-identical.
- Source: fu_base.zag (byte copy), fu_patch.zag (new fu_ fns),
  fu_driver.zag, fu_build.sh. Binary: fu_bin.

## Follow-ups

1. Grammar induction: can TNN derive the BUILD grammar from TRAIN
   examples without the researcher hardcoding DADD/DMUL? This is the
   missing piece for a full formal-understanding claim.
2. Trial node budget: the leak-on-reject pathology needs a general
   fix (scratch space for candidates, or a search budget), or all
   future construction experiments will hit it.
3. Toward real Zag: EXL is one binary level. The next formal system
   should have nesting (expressions as subexpressions), which requires
   the recursive construction the probe only simulated via the driver.
