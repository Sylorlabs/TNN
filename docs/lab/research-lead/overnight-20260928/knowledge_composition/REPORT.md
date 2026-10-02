# REPORT.md -- Knowledge Composition Experiment

## Verdict: KNOWLEDGE-COMPOSITION-COMPLETE

**TNN-2 does not compose independently-learned structures. It either
re-derives from scratch via trial (when trial can reach the answer) or
fails (when it cannot). The X/Y MAPs are causally inert for Z.**

## Design

Three X/Y/Z combinations. X and Y trained separately, never shown together.
Z requires X+Y. No paired examples. No "combine" hint.

- **C1**: X=r1 plen-3 chains, Y=r2 plen-3 chains, Z=mixed r1+r2 plen-5.
- **C2**: X=r1 plen-4 chains, Y=r2 plen-4 chains, Z=mixed r1+r2 plen-7.
- **C3**: X=r1 plen-3 chains, Y=r1 plen-4 chains, Z=r1 plen-5 chain.

Arms per combination: TREAT (X+Y trained), PAIRED (X+Y trained together),
ABL (X+Y trained, MAPs deleted before Z), FRESH (no X/Y training).
9 arms, 3/3 byte-identical (SHA-256 b21a0f4f...).

Base: persistent-connections variant (rebind + LINK14), unfrozen.
Pure Zag, safebin, pinned znc. Nothing pushed.

## Results

### C1: cross-relation, plen 5

| Arm | Z ans | Rebind | Trial verifies | ZMAP linked | Cost |
|-----|-------|--------|----------------|-------------|------|
| TREAT | 35 correct | 4 tried, 4 rejected | 3 tried, 2 rejected | 0 (trial-built) | 7 verifies |
| PAIRED | 35 correct | 1 tried, 0 rejected | - | 1 (LINK 121->68) | 1 verify |
| ABL | 35 correct | 0 (no MAPs) | 3 tried, 2 rejected | 0 | 3 verifies |
| FRESH | 35 correct | 0 (no MAPs) | 3 tried, 2 rejected | 0 | 3 verifies |

ZMAP DEP edges (TREAT): 4 Z facts only. Zero references to X/Y MAPs.

**Finding**: TREAT, ABL, and FRESH solve Z at IDENTICAL trial cost (3/2).
Deleting X/Y MAPs changes nothing. Never training X/Y changes nothing.
The X/Y structures are causally inert. TNN-2 re-derives Z from scratch.

**Stronger**: TREAT costs MORE than FRESH (7 vs 3 verifies) because rebind
wastes 4 attempts trying X/Y shapes that cannot verify. Prior structure is
not just unhelpful; the reuse mechanism burns compute on inapplicable shapes.

**Paired contrast**: When X+Y are trained together, Z reuses the mixed shape
via rebind (1 verify, LINK written). This is what structural reuse looks like,
and the treatment conspicuously lacks every signature of it.

### C2: cross-relation, plen 7 (beyond trial gather depth 5)

| Arm | X/Y competence | Z ans | Rebind | Trial |
|-----|----------------|-------|--------|-------|
| TREAT | 4/4 correct | -2 (miss) | 4 rejected | 5 rejected |
| FRESH | - | -2 (miss) | - | 5 rejected |

**Finding**: X and Y are solidly learned (all queries correct, rebind used
within X and within Y). But Z, requiring X-then-Y traversal (plen 7),
fails completely. No MAP promoted. There is no fallback to composition
when trial cannot reach the answer.

### C3: same-relation cross-length, plen 5

| Arm | Z ans | Rebind | Trial verifies | ZMAP linked |
|-----|-------|--------|----------------|-------------|
| TREAT | 95 correct | 4 rejected | 3 tried, 2 rejected | 0 |
| ABL | 95 correct | 0 | 3 tried, 2 rejected | 0 |
| FRESH | 95 correct | 0 | 3 tried, 2 rejected | 0 |

**Finding**: Identical pattern to C1. Rules out the objection that C1's
result is an artifact of cross-relation training. Even same-relation
length composition does not occur.

## Architectural reason

TNN-2 has exactly two learning mechanisms, neither of which composes:

1. **Trial** (t2_trial): monolithic gather->assemble->verify solver. It uses
   raw facts, never MAPs. Any Z within plen 5 is solved from scratch.
2. **Rebind** (rebind_try): whole-shape reuse via plen matching. It reuses
   one MAP's shape on new data. It cannot combine two shapes.

There is no mechanism to sequence, nest, or combine two MAP executions.
There is no way for Z's solution to structurally reference X's and Y's
internals. Composition is architecturally absent, not merely untested.

## Controls summary

- Paired (C1): establishes Z solvable and shows reuse signature (rebind+LINK).
- ABL (C1, C3): MAP deletion -> identical Z cost. Structures inert.
- FRESH (C1, C2, C3): no X/Y -> identical Z outcome. Training inert.
- Competence (C2): X/Y queries 4/4 correct. Failure is composition-specific.

## Honest limits

- Chain family only. Other capability pairs (chain+count, chain+sum) not tested.
- The plen-5/7 boundary is specific to t2_gather depth 4. A deeper gather
  would shift the boundary but not create composition.
- Builder-run worlds only; no independent adversary.
- Does not test whether a composition mechanism COULD be built; tests whether
  the current architecture composes (it does not).

## Standing metrics

- RESEARCHER-OWNED: all drivers, arm designs, ablation procedure.
- LEARNER-OWNED: X/Y/Z MAP graphs, LINK edges, trial verify outcomes.
- COGNITION LINES: 0 added (driver only, ~270 lines; base+patch verbatim).
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0.
- REUSE EVENTS: within-X and within-Y only; zero cross X+Y reuse in TREAT.
