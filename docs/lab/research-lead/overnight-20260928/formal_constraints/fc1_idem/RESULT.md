# RESULT_FC1: learned idempotence constrains planning

Verdict: FC-1 PASS on all six frozen bars (K-FC-1, K-FC-2, K-FC-3,
K-FC-4, K-FC-5, K-FC-6). Prereg PREREG.md (with Amendments 1-2)
was committed before any implementation existed; commit-order
self-check holds (prereg e4e8b85f2, amendment a229a87d9, both
strictly before this implementation commit).

## Frozen predictions vs observed

| Bar | Frozen prediction | Observed | Match |
|---|---|---|---|
| K-FC-1 beliefs run 1 | [1,0,0] for ops [2,5,7] | BELIEF 2 1, BELIEF 5 0, BELIEF 7 0 | yes |
| K-FC-2 beliefs run 2 permuted | [0,0,1] | BELIEF 2 0, BELIEF 5 0, BELIEF 7 1 | yes |
| K-FC-3 EXP T1 | exactly [2,5] | [2,5], REACH 1, DBL2 0 | yes |
| K-FC-3 EXP T2 | REACH 1, DBL2 0 (predicted [2,5,2,5,2,5,2,7]) | [2,5,2,5,2,5,2,7], REACH 1, DBL2 0 | yes, exact |
| K-FC-3 EXP T3 | exactly [2] | [2], REACH 1, DBL2 0 | yes |
| K-FC-3 EXP T4 | REACH 1, DBL2 0 (predicted [2,5,2,5,2,5,2,5]) | [2,5,2,5,2,5,2,5], REACH 1, DBL2 0 | yes, exact |
| K-FC-4 CTL T1 | exactly [2,2,2,2,2,2,2,5] | [2,2,2,2,2,2,2,5], REACH 1, DBL2 6 | yes |
| K-FC-4 CTL T2 | exactly [2,2,2,2,2,2,2,7] | [2,2,2,2,2,2,2,7], REACH 1, DBL2 6 | yes |
| K-FC-4 CTL T3 | exactly [2] | [2], REACH 1, DBL2 0 | yes |
| K-FC-4 CTL T4 | REACH 1, DBL2 >= 1 (predicted [2,2,2,2,5,5,5,5]) | [2,2,2,2,2,7,2,5], REACH 1, DBL2 4 | property yes, exact plan differed (see note) |
| K-FC-5 revision | BELIEF 2 0; T3B exactly [2,2,2] | BELIEF 2 0; [2,2,2], REACH 1, DBL2 2 | yes |
| K-FC-6 determinism | 3/3 byte-identical, exit 0, zero FAIL | cmp clean, exits 0 0 0, zero FAIL | yes |

3/3 runs byte-identical (sha256
b3d5d9222928848d9c9064aa0472f60c4ea52bc1a33e09e627a9863ef5d9dcf9).

## What the result shows

1. The property is LEARNED, not hardcoded. Six fixed trials per
   op; the SELF_STABLE bit is set exactly for the idempotent op
   in Run 1 (op 2) and tracks the FUNCTION under permutation in
   Run 2 (op 7). Nothing in the learner is tied to an op id.
2. The learned property CONSTRAINS behavior. The experimental
   planner cannot extend a prefix ending in op 2 with another
   op 2, so the redundant-double error is impossible for it:
   zero (2,2) pairs across all four Phase-2 plans, and every
   plan still reaches its goal (pruning never broke
   correctness).
3. The control makes the error. Without the property, the
   identical planner emits plans containing (2,2) on T1
   (six pairs), T2 (six pairs), and T4 (four pairs). T3 is the
   sanity case: no redundancy is reachable, both groups return
   the clean [2].
4. The constraint is the LIVE belief, not a frozen rule. After
   the world change (op 2 becomes increment) and disconfirming
   trials, belief[2] flips 1 -> 0, and the experimental planner
   immediately emits [2,2,2] on T3B: the error reappears once
   the property is unlearned. Behavior follows the belief,
   which follows evidence.

Supporting (not barred): world simulation calls during
planning, experimental total 84 vs control total 339. The
acquired property prunes search roughly fourfold while
preserving goal-reaching.

## Note on the T4 control plan

The hand derivation predicted [2,2,2,2,5,5,5,5]; execution
returned [2,2,2,2,2,7,2,5] (states 5,5,5,5,5,10,8,9, reaches
9). The derivation missed the [2]^5,7 branch: [2]^5,7,2 is
length 7 (not a leaf), and its child [2]^5,7,2,5 reaches 9 at
length 8, enumerated before the [2]^4,5 subtree. The bar was
property-level (REACH 1, DBL2 >= 1) precisely to contain this
class of hand-tracing risk, and it passes: DBL2 = 4. The
scientific claim (control exhibits the redundancy error) is
unaffected; the exact-plan miss is recorded here, not hidden.

## What this does NOT claim

- Not a generality claim: one formal property (idempotence),
  one op family, one planner. Inverses, commutativity, and
  other properties are future work.
- The trial procedure (6 trials, unanimity, fixed states) and
  the generic no-effect prune rule are authored machinery. The
  experiment's load-bearing assumption is the
  machinery/content split stated in PREREG.md section 10(c);
  it is open to red-team review.
- No L2/L3 classification claim. This is a mechanisms test of
  whether learned knowledge constrains behavior.
- One deterministic world family; no broad transfer claim.

## Relation to the prior lane result

The 2026-10-02 worker found the learner could build constraint
CONTENT but not the wiring (channel/ABI/consultation stayed
researcher-defined; removing it left generation unconstrained).
FC-1 narrows the wiring to a domain-neutral rule (skip actions
the current model predicts are effectless) and adds the
revision probe: the constraint here is a live belief that
flips on counterevidence, with behavior flipping in step.
The honest boundary carries over: the prune rule itself is
authored generic machinery, not learner-invented.

## Process notes

- Pure Zag; safebin mandatory. `which python3` empty at
  session start and throughout; binary built by
  /home/hatch/safebin/znc. No forbidden executable invoked.
- No em dashes in deliverables or source comments.
- Commits local only; nothing pushed. Binary built to /tmp
  (never committed). Explicit pathspecs for all commits.
- K-FC-6 verified by the build harness (build_fc1.sh) per
  Amendment 2: three runs, cmp, sha256, exit codes, FAIL grep.
