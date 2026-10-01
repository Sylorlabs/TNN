# Reuse-Rebinding Experiment: cross-domain structure reuse via structural rebinding

## Verdict: REBINDING-COMPLETE: PASS (chain family)

A learner that promoted chain-structured MAPs in World A answers a
structurally isomorphic World B query with 7 verification attempts versus
11 for a fresh learner (36% reduction), using only generic machinery:
shape read from learner-created graph topology, literals from B's own
facts, execution verification as arbiter. No hardcoded A to B
correspondence. No fixed similarity metric.

## Hypothesis

Learn structure in A, retrieve in structurally isomorphic B, rebind
literals/entities, invoke, reduce trials versus a fresh learner.

## Design

World A (treatment only):
- Decoy, promoted first (lower MAP id): facts (2,1,21),(21,1,22);
  query (2,51) expects 22. Trial promotes a plen-3 chain MAP.
- Main: facts (1,1,11),(11,1,12),(12,1,13),(13,1,14);
  query (1,50) expects 14. Trial promotes a plen-5 chain MAP.

World B (both arms): facts for an isomorphic chain
(101,1,111),(111,1,112),(112,1,113),(113,1,114), plus distractor paths:
two length-3, two length-4, one length-5 decoy path, all with different
surface literals. Query (101,50) expects 114.

The isomorphism is structural (chain topology, 4 links), not literal:
every subject id and literal value differs between A and B.

## Mechanism (unfrozen variant, rb_patch.zag)

On a miss, after activate fails and before the trial enumeration:

1. `rb_chain_plen`: walk each live MAP's graph root. If the cells form a
   pure chain (alternating BRANCHEQ guard / MOVE set, guard true-branch to
   set, set SEQ to next guard), return plen = guards+1. Else -1. The shape
   parameter comes from learner-created structure, never from the task.
2. `rebind_try`: gather local paths from the query subject (t2_gather).
   For each chain-shaped MAP, re-instantiate the chain on every local path
   whose length matches plen, using the frozen t2_asm_chain with B's own
   literals, and verify by execution (t2_try_verify). First verified
   rebound is promoted and returned.
3. Fallback: if no rebound verifies, the vanilla trial/bootstrap/inquire
   path runs unchanged.

What is generic: MAP scan order is node-id order (oldest first); no
A to B table exists anywhere; literal substitution is positional over
B's gathered paths; accept/reject is by execution against expected.
What is researcher-owned: the shape walker, the retrieve-then-verify
ordering, the splice point in ev_query.

## Results (3/3 byte-identical per arm)

| arm | B-MAIN ans | verifications (tried) | rejected |
|---|---|---|---|
| treatment (A + rebind) | 114 | 7 | 6 |
| control (fresh, no A) | 114 | 11 | 10 |
| ablation (A, no rebind) | 114 | 11 | 10 |

Treatment trace: rebound tried the decoy plen-3 shape against B's six
length-3 paths (6 rejections, all verified wrong by execution), then the
main plen-5 shape against B's length-5 paths (1 verification, success).
The blind trial never ran.

Control trace: full trial, 6 length-3 rejects, then 4 length-4 rejects,
then length-5 verify. 11 verifications.

Ablation trace (MAPs present, vanilla ev_query): 11 verifications,
identical to fresh control. The MAPs are inert without the retrieval
mechanism, consistent with the fossil census (nothing learner-driven
consults a MAP). The reduction comes from the rebind machinery, not
from A-phase facts priming the workspace.

Decomposition: oracle (known plen) = 1 verification; generic retrieval
over 2 MAPs = 7; blind trial = 11. The 6 decoy rejections are the honest
cost of generic retrieval without a shape prior.

A-phase sanity: A-DECOY answered 22 in 1 verification; A-MAIN answered
14 in 4 (1 rebound reject of the decoy shape against [1,11,12], then
3 trial: len-3 reject, len-4 reject, len-5 verify). Notably, the rebound
already exercised verification-driven shape rejection inside World A.

## Failure analysis (where genericity stops)

This pilot handles the chain family only. Count graphs
(102,101,103 repeating plus MOVE epilogue) and sum graphs (103 runs)
are not recognized by rb_chain_plen and fall back to trial. Extending
the shape walker to those topologies is mechanical (same walk, more
patterns), not architectural. A harder open problem, not attempted here:
rebinding when B's solution needs a *different* topology than any
learned MAP (genuinely new domain). That is STRONG K-LT-5 territory and
remains untested.

## Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: the rebinding procedure
  (shape walk, plen filter, positional re-instantiation, retrieve-before-
  trial ordering, splice point). 1 mechanism, ~70 cognition lines.
- LEARNER-OWNED STRUCTURAL DECISIONS: the two A-phase MAP graphs
  (created by trial + promote_graph from experience, not enumerated in
  source). The plen values read back are learner-created.
- SOURCE-ENUMERABLE FORMS: chain shapes of any plen (generic over
  length, not a fixed menu of answers).
- SUF DECISIONS: MAP scan order (node id), B-path order (BFS gather).
- LEARNER-INTERNAL CRITERIA: execution verification accepts/rejects
  every rebound candidate (7/7 decisions).
- REUSE EVENTS: 1 (MAP_main shape reused in B; MAP_decoy retrieved and
  rejected by verification).
- REVISION EVENTS: 0.
- COGNITION LINES: 106 (rb_patch.zag), of which the mechanism is ~70.
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## Constraints honored

Unfrozen variant only; frozen base read-only (SHA-256 verified
a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd).
Pure Zag via pinned znc. Safebin PATH, no python3/python. Zero em/en
dashes byte-verified. Paper untouched. No sealed worlds. Nothing pushed.

## Files

- NAMECHECK.md (Step 0 toolchain guard, scope, provenance)
- rb_base.zag (verbatim frozen copy, hash-verified)
- rb_patch.zag (rebinding mechanism + patched ev_query; treatment only)
- rb_noa.zag / rb_yesa.zag (phase_a_enabled stubs for control/ablation)
- rb_driver.zag (experiment driver)
- rb_full_treat.zag / rb_full_ctrl.zag / rb_full_abl.zag (assembled)
- rb_treat_bin / rb_ctrl_bin / rb_abl_bin
- rb_treat_run{1,2,3}.txt / rb_ctrl_run{1,2,3}.txt / rb_abl_run{1,2,3}.txt
  (3/3 byte-identical within each arm)
- REBINDING.md (this report)

## Follow-ups (for the parent, not decided here)

- Extend the shape walker to count/sum families (mechanical).
- Retrieval policy: recency or shape-frequency ordering to cut the
  decoy-rejection cost (still generic).
- Adversarial B worlds where the first-plen match is wrong and a later
  MAP is right (selection under ambiguity).
- The genuinely-new-topology case (STRONG K-LT-5) remains open.
