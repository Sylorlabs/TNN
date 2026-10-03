# TNN-2 Construction Red Team Report

Date: 2026-09-30. Target: `tnn2.zag` @ `f4de7ff46` (frozen, read-only).
Scope: Change 1, the `t2_trial` miss-policy trial loop (lines 581-672).

## Verdict: CONSTRUCTION-ATTACK-SUCCESS

The trial loop does not construct open executable structure. It performs
generate-and-test over a finite, researcher-authored family of exactly
three linear graph templates (two reachable in production), with every
bound, wiring choice, slot assignment, search order, and the verification
criterion fixed by the researcher. Per Micah's criterion, this is not L3:
the final structures are effectively enumerable from a complete
researcher-written family.

## 1. The candidate grammar (complete)

`t2_trial` calls exactly three assemblers. `promote_graph` has exactly
four call sites, all inside `t2_trial` (lines 605, 628, 644, 659). No
other code path creates executable graphs. The constructible space is:

**Family A: chain graphs** (`t2_asm_chain`, lines 363-378). A linear
sequence of k (GUARD -> SETREG) pairs. Each guard is BRANCHEQ testing
frame slot0 against a literal; on match, slot0 is set to the next
literal. Guards link via ET_SEQ; each guard's true-target (field12) is
its paired set cell. Assembled from BFS paths gathered by `t2_gather`
(depth 1..4 hops, 96-path cap, cycle-free, any relation except -999).
Tried in fixed order k=2,3,4, then single hops (k=1) last.

**Family B: sum graphs** (`t2_asm_sum`, lines 398-413). An unrolled chain
of exactly T INC(slot0) cells, where T is the sum of one non-empty
subset of at most 12 direct values of the subject. Subsets enumerated by
descending bitmask grouped by popcount (at most 4095). Declined unless
0 < T <= 900.

**Family C: count graphs** (`t2_asm_count`, lines 379-397). A linear
chain of (GUARD -> SETREG -> INC slot1) per link, plus a final
MOVE(slot0 <- slot1) epilogue. Assembled from per-relation value chains
(`t2_chain`, at most 16 links via first-match fact lookup).

That is the entire space. No branching beyond the fixed guard->set
pairs. No nesting. No loops except unrolled INC runs. No subroutine
calls: promoted graphs are never reused as components (no CALL, no
reading of MAP/graph nodes during assembly). DEC (tag 104) is never
emitted by any assembler; construction uses 3 of the 4 ISA ops.

## 2. What the researcher fixed vs what the data supplies

Researcher-fixed (in source, not learned):
- The three families, their exact wirings, and their cell tags.
- Slot assignments: slot0 = subject/output, slot1 = counter. Only
  slots 0 and 1 are ever initialized (`t2_exec`, line 421-422).
- Guards always test slot0; sets always write slot0.
- Search order, hardcoded with the comment "composition-preserving":
  chains k=2..4, then sums, then counts, then single hops.
- All bounds: chain depth 4, 96 BFS paths, 12 sum values, 4095
  subsets, total <= 900, 16 count links, 32-cell signature walk.
- The frame layout and the verifier semantics (below).

Data-supplied (not researcher-enumerated):
- Literal values, which come from observed facts.
- Which paths, subsets, and relations exist in the workspace.
- Which candidate verifies first (order-dependent, data-dependent).

Fair acknowledgment: the promoted graph is genuinely new persistent
learner state with provenance DEP edges, not a retrieved template
instance, and failed guards count as genuine rejections. The mechanism
does compose parts at runtime, and T2-CHAIN4 (4-hop) genuinely exceeds
the old 3-template ceiling. But the new ceiling (4 hops) is equally
hard, and "composed at runtime from parts" where the parts, the
composition rules, the bounds, and the acceptance test are all
researcher-fixed is a larger finite menu, not open construction. This
matches Micah's excluded category: fitting parameters (here, literals
and wirings drawn from data) of a supplied template.

## 3. The verification oracle

`t2_try_verify` (lines 497-510): in unmasked mode, a candidate is
accepted iff its executed output `v` equals `expected`. The `expected`
value arrives as a parameter of `ev_query(W,s,r,expected,flags)` and, in
the freeze protocol, is parsed directly from the world's QUERY event
(`QUERY s r e` -> `ev_query(W,subj,rel,exp,0)` in `shim_driver2.zag`,
line 91; flags=0 always, so masked mode never engages in the freeze).

The trial loop therefore does not discover the answer from the world.
It is given the answer and searches its fixed grammar for the first
member whose output matches. The honest characterization is
feedback-driven structure search over a fixed grammar: legitimate as a
learning-from-feedback setup, but the "construction" step contains no
discovery beyond enumerating the researcher's family in the
researcher's order until the oracle says yes.

## 4. The sum family is dead in production (test-gated)

Family B is additionally gated by `comb_present(W) >= 0` (line 613),
which requires a type-8 node in the workspace. The only type-8
creation site in the entire source is line 1106, inside test function
`t_p2`. No cognitive path (`ev_observe`, `ev_query`, `ev_teach`,
`miss_inquire`, revision) ever creates one. In any fresh world,
including the sealed freeze, the sum branch is unreachable. The
effective production construction space is two families: chains and
counts.

## 5. Boundary probes (frozen `freeze_shim2_bin`, novel worlds)

All probes use subjects/relations with no direct stored fact, forcing
the miss path (direct retrieval short-circuits otherwise):

- 2-hop chain (miss): OBSERVE (10,5,11),(11,5,12); QUERY (10,9,12)
  -> ANSWER 10 9 12. In-family construction works.
- 5-hop chain (miss): 5-link chain on relation 5; QUERY (20,9,25)
  -> ANSWER 20 9 -2. Correctly refused: hard depth-4 bound confirmed
  behaviorally. A 5-hop structure is unrepresentable, not merely
  undiscovered.
- Subset sum (miss): OBSERVE (30,7,3),(30,7,4); QUERY (30,9,7)
  -> ANSWER 30 9 -2. Sum not attempted: no type-8 marker exists,
  confirming the test-gating finding behaviorally.
- Count (miss): 3-link chain on relation 21; QUERY (50,43,3)
  -> ANSWER 50 43 3. In-family construction works.

Note: `t2_gather` does not filter by the query relation (line 452
checks relation != -999 only), so chain/count candidates freely mix
relations; the query relation plays no role in construction. This is a
researcher choice, documented here, not a separate falsifier.

## 6. Explicit finite bound

For a workspace with P BFS paths (P <= 96), V direct subject values
(V <= 12), and R relations of the subject, the total candidate count is
at most P (chains) + (2^V - 1) (sums; zero in production) + R
(counts), each tried once in fixed order, each a linear graph of
bounded size. The family is completely enumerable from the source plus
the fact set. Nothing in the mechanism can produce a graph outside
these three linear forms.

## 7. What would change this verdict

- A proposal generator whose graph topologies are not drawn from a
  fixed finite set of researcher-written assemblers (e.g., recursive
  composition of previously promoted graphs, which MUL Rung B
  demonstrated standalone but which `t2_trial` does not use).
- Verification against world feedback rather than an environment-
  supplied expected answer on the query path.
- Removal of the hard depth/shape caps with the bound emerging from
  learner state (e.g., a budget the learner manages) rather than
  literals in researcher code.

## 8. Relation to the other two mechanisms

Out of scope for this report (sibling red teams): whether the inquiry
loop's UNCERTAINTY -> guide -> POLICY_ROOT chain is learner-driven,
and whether `t2_revise_graph`'s tombstone/insert/rewire procedure is a
researcher-authored repair script. This report covers construction
only. Note for those teams: the revision operator edits graphs that
this finite family produced; its generality should be judged
independently.

## Verdict restated: CONSTRUCTION-ATTACK-SUCCESS

TNN-2 Change 1 is generate-and-test over a finite researcher-authored
family of linear graph templates (effectively two in production), verified
against an environment-supplied answer. It is a genuine improvement over
three fixed templates, and a real L2 structural-learning mechanism, but
it is not open executable-structure construction and must not be called
L3.
