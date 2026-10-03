# REPORT: Grammar Transfer Worker

## Verdict: GRAMMAR-TRANSFER-COMPLETE

## Claim tested

The grammar induction machinery (commit 62c6a7734) transfers to a
second formal system with different operators and a different
constraint shape, with the induction code byte-identical. Only the
example stream differs.

## EXL2: the second formal system

Literals 0..9, pair encoding P(a,b) = a*16+b (same world encoding
convention as EXL; researcher-owned, taught via examples).

| EXL            | EXL2                 |
|----------------|----------------------|
| ADD=41, MUL=42 | SUB=41, DIV=42       |
| DADD=43, DMUL=44 | DSUB=43, DDIV=44   |
| BUILD=45       | BUILD=45             |
| constraint: value < 64 (upper bound) | constraint: SUB result >= 0 (lower bound); DIV exact only, b > 0 (divisibility) |

Taught via examples only, never as rules:
- Eval: (P(a,b),41,a-b) for a>=b; (P(a,b),42,a/b) for b>0 and a/b exact.
- Decomp: (t,43,P) for a-b==t; (t,44,P) for exact a/b==t; all t in 0..9.
- BUILD: 4 canonical examples for TRAIN targets {1,3,5,7}, alternating
  DIV-first/SUB-first so both licensor relations appear in the stream.
  No BUILD facts for the 6 TEST targets {0,2,4,6,8,9}.

Battery size note: SUB/DIV on literals 0..9 admits exactly 10 target
values, so TRAIN/TEST must partition them. EXL2 uses 4 TRAIN examples
and 6 novel TEST targets (disjoint), the maximum the domain allows.
The bar is per-target validity and ablation causality, not the EXL
count of 11.

## Machinery-identity proof

- gt_base.zag SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  identical to gi_base.zag.
- gt_patch.zag SHA-256 ae94800e0167d72aaba3879216699c3be2fbdc5d7c60eeea62428594c3db50d3,
  identical to gi_patch.zag. This file holds ALL induction,
  construction, ablation, and classification logic. Zero bytes changed.
- Driver: gi_report_grammar, gi_arm_induce, gi_arm_base,
  gi_arm_hardcode verified byte-identical to gi_driver.zag with cmp.
  The driver diff is confined to: teaching functions
  (gi_dadd/gi_dmul -> gt_dsub/gt_ddiv, canon/teach fns), the
  world-specific test battery (gi_test_targets), and main, which adds
  the W5a/W5b contradiction arms.

Design decision (documented, not a machinery change): EXL2 reuses the
relation-id labels 41/42/43/44/45. Ids are the world's arbitrary
labels; every operator semantic (SUB vs ADD tables, non-negativity,
exact divisibility) comes from the example stream. The induction path
never hardcodes licensor ids; it discovered {44,43} from the 4 EXL2
BUILD examples.

Honest accounting of what the byte-identical machinery assumes about
a world (unchanged from EXL, now explicit): (1) the verification
lookup gi_trial_build2 references eval relations 41/42; (2) the rubric
gi_classify references decomp ids 43/44 and literal range 0..9;
(3) pair decoding assumes P(a,b) = a*16+b with components in 0..15.
A future generalization would induce the eval relations and the
encoding too. None of these were touched; EXL2 was shaped to fit the
machinery's stated assumptions, and the induction still had to
discover the grammar from examples.

## Results (3/3 byte-identical, SHA-256 ed1cce40...)

Induced grammar: nbuild=4 nlic=2 lic=44,43 a=[0,9] b=[0,9] maxlinks=1.
The licensor set {44,43} (DDIV, DSUB) was discovered, not hardcoded.

### INDUCE arm (W1): 6/6 valid

All 6 novel TEST targets constructed valid single-dep DSUB/DDIV pairs:
0=P(1,1) via 1-1=0, 2=P(2,0), 4=P(4,0), 6=P(6,0), 8=P(8,0),
9=P(9,0), each verified against TNN's own SUB/DIV eval knowledge.

### ABLATE arm (W2): 0/6 valid (errors return)

Grammar induced, then DELETED via gi_ablate. Base trial produces 0/6
valid (all class 2 multi-dep invalid forms, the same failure mode as
the EXL control). The induced constraint was causally necessary:
remove it, errors return.

### HARDCODE arm (W3): 6/6 valid

Researcher-authored restriction: 6/6. Induced matches hardcoded
performance exactly.

### FRESH arm (W4): 0/6 valid

No induction, base trial: 0/6. Induction is necessary.

### CONTRADICT arms (W5a/W5b): fail-closed, no collapse

- W5a: one deceptive BUILD fact (2,45,P(9,9)) labeled valid, with no
  licensor (T,r,P) anywhere in learner state. gi_induce returns 0;
  no grammar node written; construction reports NOGRAMMAR.
- W5b: deceptive teacher adds bogus decomp relation 46 licensing
  (3,45,P(4,1)) alongside true DSUB 43. Distinct licensor count
  reaches 3, exceeding the nlic<=2 guard; gi_induce returns 0;
  no grammar node written.

Induction degrades by refusing to induce (fail-closed) rather than
hallucinating a permissive or corrupted grammar. It does not exclude
the outlier and keep going; any inconsistency voids the whole
induction. That is the current graceful-degradation behavior, and its
limit: one bad example poisons the batch.

## Researcher-owned vs learner-owned

Researcher-owned: EXL2 definition, pair encoding, teach order,
TRAIN/TEST split, classification rubric, the induction procedure.
Learner-owned: all SUB/DIV eval facts, all DSUB/DDIV decomp facts,
the 4 BUILD facts, the induced licensor set {44,43}, the induced
literal ranges [0,9], the semantic verification values, the promoted
MAPs. The same researcher-written procedure produced a correct
grammar for a different operator set with a different constraint
shape, from examples alone.

## Metrics

- Cognition lines added: 0 to patch/base (byte copies). Driver:
  teaching section rewritten (~90 added lines, all example-stream);
  arms byte-identical.
- Modes/bridges/handlers: 0. New semantic cases: 0. Base
  modifications: 0.
- Determinism: 3/3 byte-identical runs.
- Induction success: 4/4 BUILD examples yielded consistent grammar.
  Construction: 6/6 novel targets valid; ablation 0/6; fresh 0/6.
- Contradiction: 2/2 fail-closed refusals, 0 corrupted grammars.

## Follow-ups

1. The machinery's world assumptions (eval ids 41/42, pair encoding
   /16, rubric range 0..9) are now explicit. Test a third system that
   breaks one assumption (e.g., ternary ops, different encoding) and
   record exactly which assumption breaks first.
2. Contradiction handling is fail-closed on the whole batch. An
   outlier-excluding induction variant is a possible next mechanism,
   but it must itself be tested for adversary exploitability (a
   teacher could smuggle bad examples past a naive excluder).
3. The nlic<=2 guard is a fixed researcher constant in the machinery;
   EXL2 happened to have 2 licensors. A system with 3 genuine
   licensors would be refused; generalizing the guard without opening
   a hole is open work.
