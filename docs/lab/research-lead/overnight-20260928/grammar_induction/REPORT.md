# REPORT: Grammar Induction Worker

## Verdict: GRAMMAR-INDUCTION-COMPLETE

## Claim tested

Micah Priority 2: TNN LEARNS grammar/semantics/constraints from
experience. Those learned constraints become causally active in
construction. Invalid structures become impossible or explicitly
rejected. Do not permanently hardcode grammar restriction. Induce it
from examples. Then ablate the learned constraint and verify errors
return.

## Method

EXL formal system taught via EXAMPLES only (no grammar rules):
- Eval: all (P(a,b),ADD,a+b) and (P(a,b),MUL,a*b) for a,b in 0..9.
- Decomp: (T,DADD,P) and (T,DMUL,P) for many targets.
- BUILD: 8 canonical examples (T,BUILD,P) for TRAIN targets only.
  No BUILD facts for the 11 TEST targets.

Induction (gi_induce) discovers from learner state:
1. FORM: For each BUILD example (T,45,P), find licensor facts
   (T,r2,P) with r2 != 45 (same subject/object, different relation).
   Collect distinct r2. Result: {43,44} (DADD, DMUL). Discovered,
   not hardcoded. The code never mentions 43 or 44.
2. LITERALS: Scan all facts with induced licensor relations; decode
   pair objects to (a,b); track ranges. Result: [0,9]x[0,9]. Grounded
   in full decomp experience, not overfitted from 8 examples.
3. ATOMICITY: Licensors are single facts, so candidates must be
   single facts (path length 2).

The induced grammar is stored in learner state (type-70 node) and
guides gi_trial_build2: candidates must be atomic facts with induced
licensor relations; outputs must decode within induced ranges and
verify against TNN's own eval knowledge (either op).

## Results (3/3 byte-identical, SHA-256 1d997322...)

Induced grammar: nbuild=8 nlic=2 lic=43,44 a=[0,9] b=[0,9] maxlinks=1

### INDUCE arm (W1): 11/11 valid

All 11 TEST targets constructed valid single-dep DADD/DMUL pairs:
10=P(1,9), 11=P(2,9), 12=P(3,9), 13=P(4,9), 14=P(5,9), 15=P(6,9),
28=P(4,7), 30=P(5,6), 42=P(6,7), 45=P(5,9), 63=P(7,9).
Each verifies against TNN's own eval knowledge.

### ABLATE arm (W2): 0/11 valid (errors return)

Grammar induced, then DELETED via gi_ablate. Base trial produces
0/11 valid (all class 2 multi-dep invalid forms, same as prior
control). The induced constraint was causally necessary: remove it,
errors return.

### HARDCODE arm (W3): 11/11 valid

Prior treatment (researcher-authored DADD/DMUL restriction):
11/11. Induced matches hardcoded performance exactly.

### FRESH arm (W4): 0/11 valid

No induction, base trial: 0/11. Induction is necessary.

## Causal proof

The ablation is the causal test Micah required:
- With induced grammar: 11/11 valid.
- Without (ablated): 0/11 valid.
- The ONLY difference is the presence/absence of the induced
  grammar record. Errors return when it is removed.

## Induced vs hardcoded

Both achieve 11/11. The difference is authority:
- Hardcoded: researcher wrote `fr==43 || fr==44` in the source.
- Induced: TNN discovered {43,44} by scanning its own BUILD facts.
  The source contains no 43/44 literals in the induction or
  construction path.

## Researcher-owned vs learner-owned

Researcher-owned: EXL definition, pair encoding, teach order,
TRAIN/TEST split, classification rubric, the induction procedure
itself (gi_induce code).
Learner-owned: all eval/decomp/BUILD facts, the induced licensor
set {43,44}, the induced literal ranges [0,9], the semantic
verification values, the promoted MAPs.

The induction procedure is researcher-written, but its OUTPUT
(the specific grammar: which relations, which ranges) is
learner-derived from data. If the world had different licensing
relations, it would discover those.

## Architectural finding: node field overflow

During development, the grammar node (type 70) was corrupted by
trial allocations: field 40 overwritten with 902 (frame type).
Root cause: MY bug, not base. Node size is 40 bytes (noff(n) =
64+n*40). I used fields 40,44,48,52,56,60 which overflow into the
next node. Field 40 of node 368 IS field 0 of node 369. When
t2_exec allocated node 369 as a frame (type 902), it overwrote my
field 40.

Fixed: use fields within 0..32 (0=type, 4=nlic, 8=lic0, 12=lic1,
16=min_a, 20=max_a, 24=min_b, 28=max_b, 32=nbuild; 36=liveness).
Also added buffer workaround (read once after induction) for
robustness.

Lesson: custom node types must respect the 40-byte node size.
Fields 0,4,8,12,16,20,24,28,32 are safe; 36 is liveness; 40+
overflow.

## Metrics

- Cognition lines added: ~250 (gi_patch.zag new fns only).
- Modes/bridges/handlers: 0. Semantic cases: 0.
- Base modifications: 0 (gi_base.zag is byte copy).
- Determinism: 3/3 byte-identical.
- Induction success rate: 8/8 BUILD examples yielded consistent
  grammar (100%). Construction: 11/11 novel targets valid.

## Follow-ups

1. The induction procedure (gi_induce) is researcher-written. A
   stronger test: can TNN decide WHEN to induce (not just how)?
2. Grammar revision: if counterexamples arrive (e.g., a new
   operator), can the induced grammar be revised?
3. The 40-byte node limit constrains learner-created structure.
   A general mechanism for larger learner structures is needed.
