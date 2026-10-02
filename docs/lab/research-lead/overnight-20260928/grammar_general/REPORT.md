# REPORT: Grammar Generalization Worker

## Verdict: GRAMMAR-GENERAL-COMPLETE

## Claim tested

Micah Priority B: Grammar induction was 11/11 on EXL. Does the SAME
induction machinery generalize to a new formal system, and where are
its boundaries? The induction mechanism (gi_induce) is FROZEN
byte-identical from the prior wave. No modifications.

## Method

Four tests, one binary, pure Zag, pinned znc, safebin.

### Test A: EXL2 (new formal system)

A genuinely different formal system from EXL:
- Operators: ADD (41) and SUB (42). EXL used ADD/MUL.
- Licensor relations: DADD=46, DSUB=47. EXL used 43/44.
  These IDs are DISCOVERED by the frozen gi_induce, never hardcoded.
- Literals: 0..7. EXL used 0..9.
- BUILD=45 and pair encoding P(a,b)=a*16+b are structural requirements
  of the frozen mechanism (gi_induce hardcodes the BUILD relation ID
  and the pair decoding).

Teaching (examples only):
- Eval: (P(a,b),41,a+b) and (P(a,b),42,a-b) for a,b in 0..7.
- Decomp: (T,46,P) and (T,47,P).
- BUILD: 6 canonical examples covering both licensors.

Arms: INDUCE (frozen gi_induce + frozen gi_trial_build2), ABLATE
(induce then delete), FRESH (no induction). 9 TEST targets, none in
TRAIN. New classifier gg2_classify2 mirrors the EXL rubric for 46/47
and range 0..7.

### Test B: Nested constraints

BUILD examples where the ONLY licensor is 2-step: (T,44,M) and
(M,43,P), with no single fact (T,r2,P). The frozen gi_induce searches
only single facts. Expected: induction returns 0.

### Test C1: Wrong-licensor noise

8 clean BUILD examples (licensors 43/44) + 2 with licensor 46.
The distinct licensor set becomes {43,44,46} (nlic=3), triggering the
`nlic>2` rejection. Expected: induction returns 0.

### Test C2: Missing-licensor noise

8 clean BUILD examples + 2 with NO licensor fact at all
(P(1,1) for T=28: 1+1=2, 1*1=1, neither is 28; P(2,2) for T=30:
sums/products are 4, not 30). Expected: induction returns 0 via the
`found==0` path.

## Results (3/3 byte-identical, SHA-256 215af50e...)

### Test A: PASS

- Induction: SUCCESS. Discovered `nlic=2 lic=47,46 a=[0,7] b=[0,7]`.
  The NEW licensor IDs (46/47) and the NEW range ([0,7]) were found
  from data. The source contains no 46/47 literals in the induction
  or construction path.
- INDUCE arm: 9/9 valid (all class=1).
- ABLATE arm: 0/9 valid (errors return; causal proof preserved).
- FRESH arm: 0/9 valid (induction necessary).

The frozen mechanism generalized to different operators, different
licensor IDs, and a different literal range with zero changes.

### Test B: PASS (honest boundary)

- GG-B-INDUCED 0. The mechanism cannot induce nested (multi-step)
  licensors. It searches single facts only. This is an architectural
  limitation, not a bug: the induction procedure assumes atomic
  licensors.

### Test C1: PASS

- GG-C1-INDUCED 0. The `nlic>2` cap rejects inconsistent licensor
  sets. The mechanism does not silently pick a majority.

### Test C2: PASS

- GG-C2-INDUCED 0. A single BUILD example without a licensor kills
  the entire induction (`ok=0`). The mechanism has ZERO noise
  tolerance by construction.

## Interpretation

1. **Generalization confirmed (Test A).** The induction LOGIC (find
   licensor relations by scanning BUILD facts for shared
   subject/object with a different relation; ground literal ranges
   in licensor-relation experience) transfers to a new formal system
   with different operators, different relation IDs, and different
   ranges. The discovery is data-driven, not EXL-specific.

2. **Boundary 1: atomicity (Test B).** Nested constraints are out of
   scope. A future mechanism would need to induce licensor PATHS,
   not just licensor relations.

3. **Boundary 2: brittleness (Test C).** The mechanism is all-or-nothing.
   One bad example voids the induction. There is no majority vote,
   no confidence weighting, no revision. This matches the prior
   wave's follow-up note: "Grammar revision: if counterexamples
   arrive, can the induced grammar be revised?" Answer: not with
   this mechanism.

4. **What remains researcher-owned.** The induction PROCEDURE
   (gi_induce code) is still researcher-written, as is the BUILD=45
   convention and the pair encoding. What is learner-owned: the
   specific licensor set, the literal ranges, the semantic values.
   Test A shows the learner-owned portion transfers; the
   researcher-owned scaffold does not yet learn itself.

## Architecture accounting

- New cognition lines: gg_driver.zag (~250 lines, driver/test only).
- Frozen: gg_patch_frozen.zag (byte-identical to gi_patch.zag).
- Modes/bridges/handlers/semantic cases: 0.
- Base modifications: 0.

## Constraints observed

Pure Zag. Safebin active. `which python3 python` empty. Zero em/en
dashes (byte-verified). Paper untouched. Nothing pushed.
