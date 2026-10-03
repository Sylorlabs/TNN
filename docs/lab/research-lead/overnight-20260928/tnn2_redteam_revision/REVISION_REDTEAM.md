# TNN-2 Revision Red Team Report

Date: 2026-09-30. Target: `tnn2.zag` at `f4de7ff46` (frozen, read-only).
Focus: `revise_on_contradict` (line 685), `t2_revise_graph` (line 706).
Verdict: **REVISION-ATTACK-SUCCESS**.

## 1. What the operator actually does (source trace)

`revise_on_contradict(W, factn, new_o)` (685):
- Reads the old output from the fact node (687).
- Scans all MAP nodes (tag 20); for each with a type-1 (ET_DEP) edge to
  `factn`, calls `t2_revise_graph` (688-700).

`t2_revise_graph(W, m, factn, old_o, new_o)` (706) executes exactly one
repair schema, with no branches over alternatives:

1. Find the stale step (711-717): scan edges for a type-1 edge to `factn`;
   the source cell must be active with tag 101. Line 713:
   `if(ng(W,c,36)==1 && ng(W,c,0)==101){stale=c;}`
   Note: the loop overwrites `stale` on every match, so with multiple
   candidates the LAST in edge-index order wins. Arbitrary, not chosen.
2. Find the guard (719-724): scan cells for active tag 102 (BRANCHEQ)
   whose field 12 equals `stale`. If none, return 0. No repair.
3. Build the replacement (725-726):
   `let ly:i32=t2_lit(W,new_o);` then `let nst:i32=t2_set(W,0,ly);`
   Always a literal cell holding the just-observed value, wrapped in a
   SETREG of slot 0. No trial, no search, no alternatives considered.
4. Rewire (727-730): link new SETREG to the fact; repoint the guard's
   field 12 from `stale` to `nst`; SEQ-link `nst` to stale's successor;
   kill stale's old SEQ edge.
5. Tombstone (731): `ns(W,stale,0,0); ns(W,stale,36,0);` Always.
6. Re-execute (732): `let out:i32=t2_exec(W,root,s);`
   On failure (`-999999`), revert everything and return 0 (733-744).
7. Mark old facts contradicted, teach the new output, update the MAP
   answer (745-762). MAP standing untouched.

## 2. Repair-topology enumeration

The operator produces exactly **one** repair topology:

```
guard(102) -> NEW setreg(101, literal=new_o) -> succ
              OLD setreg(101) tombstoned (tag 0, inactive)
```

Probe results:

1. **Delete without inserting?** No. Lines 725-726 always create the
   literal and the SETREG. There is no code path that tombstones without
   inserting.
2. **Insert without tombstoning?** No. Line 731 always tombstones on the
   success path.
3. **Rewire a branch to a non-adjacent step?** No. Line 728
   (`ns(W,g,12,nst)`) always repoints the guard to the newly created
   cell, never to an existing step.
4. **Loop to straight-line or vice versa?** No. There is no loop
   manipulation anywhere in the operator. BRANCHEQ targets are repointed;
   loop structure is never created, removed, or altered.
5. **Revise a non-SETREG step?** No. Line 713 requires tag 101. An
   INC (103), DEC (104), or BRANCHEQ (102) step can never be `stale`;
   the operator returns 0. (A MOVE cell also carries tag 101 and would
   match, but it is then replaced by a literal SETREG, silently changing
   a register copy into a constant.)
6. **Revise the guard condition itself?** No. The guard's fields 4
   (tested slot) and 8 (comparison literal) are never touched. If the
   counterexample means "this branch should fire on a different value,"
   the operator cannot express that repair.
7. **Two steps needing revision?** Only one is fixed per call. `stale`
   is a single variable; one contradiction event revises one step. A
   second wrong step requires a second contradiction event against the
   already-revised graph, which may no longer be in a revisable shape.

## 3. What part of the repair topology was actually chosen by the learner?

Essentially none. Itemizing every degree of freedom:

| Decision | Chosen by | Evidence |
|---|---|---|
| Which MAP to revise | Deterministic lookup (contradicted fact) | 690-694 |
| Which cell is stale | Deterministic lookup via provenance; last-match-wins on ties | 711-717 |
| Which guard | Deterministic pointer chase (field 12) | 719-724 |
| Replacement cell type | Researcher: always SETREG (101) | 726 |
| Replacement value | The observed literal `new_o`; no search | 725 |
| Rewire targets | Researcher: always guard->new->succ | 727-730 |
| Tombstone vs keep | Researcher: always tombstone | 731 |

The trial loop `t2_trial` (line 586), TNN-2's genuine construction
machinery, is **never invoked** by the revision path. The operator does
not search a repair space; it executes a fixed procedure with
runtime-filled operands (which cell index, which literal value).

The honest characterization: the learner selects the *operands*
(which cell, what value); the researcher selected the *procedure*.
That is L1 parameter filling inside a researcher-authored repair
template, not L2 structural learning and not L3 invention.

## 4. The T2-REVISE trace (line 1275)

The test: teach (101,11,102) and (102,12,201); query builds a chain
graph yielding 201; then `ev_observe(W,102,12,999)` contradicts the
(102,12) fact; the test asserts the re-executed graph yields 999, the
graph signature changed, MAP standing is unchanged, and a fresh query
returns 999.

The space of possible repairs the operator considered: **one**.
The "corrected step" is `t2_lit(W, 999)`; a literal of the value just
supplied by the test harness. The revised graph does not compute 999;
it *stores* 999. After revision, the association (102,12)->999 is a
memorized constant behind the same guard shape. This is L0 storage
dressed as revision: the system records supplied information in a new
cell rather than restructuring a computation.

The test passes, and the mechanism is real (topology genuinely
changes; revert-on-failure works; standing is untouched). But it
demonstrates exactly one researcher-anticipated repair on one
researcher-built graph family.

## 5. Criterion 0 assessment

- **C0-A (runtime-defined semantics): FAIL.** The repair semantics;
  find SETREG via provenance, tombstone, insert literal SETREG, rewire
  guard target and SEQ; reside entirely in `t2_revise_graph` source
  (lines 706-763). Learner state supplies operands, not the procedure.
  A dedicated pre-written semantic case kills the claim, and this is
  one.
- **C0-B (open structural form): FAIL.** The output topology is always
  guard->new-SETREG(literal)->succ with the old SETREG tombstoned. The
  researcher enumerated a repair family with exactly one member. The
  final topology is not selected; it is the only thing the code can do.
- **C0-C (multiple unforeseen forms): FAIL.** A sealed world needing
  any other repair shape; change the guard predicate, insert a branch,
  convert INC to DEC, revise two steps, reroute around a step; receives
  return 0. The operator handles the demonstrated schema and nothing else.
- **C0-D (cognitive reuse): FAIL / not demonstrated.** The revised graph
  persists and answers follow-up queries, but no test shows the revised
  structure improving transfer, prediction, sample efficiency, or reuse
  in a new context. Continued functioning is not reuse.

No L3 claim survives. C0-A, C0-B, and C0-C fail outright; C0-D is
unestablished.

## 6. The bound, stated precisely

TNN-2's revision operator is a **single-schema literal-patch
procedure**: on contradiction of a fact licensed by a BRANCHEQ-guarded
SETREG in a chain/count-style graph, replace that SETREG's computed
value with the observed literal, preserving the surrounding topology.

It is genuine in what it does (real topology edit, real revert,
standing untouched) and it is not general. The gap between the claim
("generic revision operator over executable graphs") and the mechanism
("replace bad MAP step with observed constant") is the whole attack
surface, and the mechanism sits on the researcher-authored side of it.

## 7. What would count as an answer to this red team

- The revision path invokes the trial/search machinery (or equivalent)
  over a space of repair candidates with more than one member.
- Demonstrated repairs that differ structurally: at least two of
  (guard-predicate change, step insertion without deletion, branch
  rerouting to an existing step, loop/sequence conversion, multi-step
  coordinated repair).
- The corrected content is derived (computed, searched, or selected
  among alternatives), not the observed literal.
- A sealed-world repair the researcher did not pre-shape.

## Verdict: REVISION-ATTACK-SUCCESS

The "generic revision operator" is a hardcoded single-schema repair
procedure. The learner chooses operands; the researcher chose the
topology. C0-A, C0-B, C0-C fail; C0-D unestablished. No L3.
