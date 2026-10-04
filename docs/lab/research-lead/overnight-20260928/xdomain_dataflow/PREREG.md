# PREREG.md -- XDOMAIN-DATAFLOW (H3: Generic Dataflow Graph)

Frozen before implementation. Commit this file alone first.

## Hypothesis

Cross-domain composition can be achieved via a GENERIC DATAFLOW GRAPH.
The goal is represented as dataflow nodes (learned procedures) connected
by data dependencies. X and Y are subgraphs. Composition wires X's output
port to Y's input port. The wiring is DISCOVERED from goal fact
connectivity, not from a template. The dataflow machinery does not know
"chain" or "count"; it only knows procedures with input subjects and
output values.

This competes with H1 (typed I/O contracts) and H2 (value-level f(g(x))).

## World

Same as composition_xdomain (verified port):

- X (navigation): chain-following, r=81 facts, plen-4 chains. Queries
  (s,91) -> endpoint. X MAPs are guard/set chains.
- Y (aggregation): count queries, r=82 facts. Queries (s,92) -> link
  count. Y MAPs are count graphs (INC cells + MOV epilogue).
- Z (chain-then-count): facts (31,81,32),(32,81,33),(33,81,34) then
  (34,82,35),(35,82,36). Query (31,93) -> 2.

30-fact interference gap between training and Z facts. Fresh literals.
Query rel 93 is new.

## Mechanism (unfrozen patch)

1. **Procedure registry** (learner-owned): after training, each learned
   MAP is registered as a procedure with (map_id, in_rel, fact_rel).
   in_rel is the query relation it answers (91, 92). fact_rel is the
   fact relation it consumes (81, 82), extracted from the MAP's relseq
   or training context.

2. **df_discover(W,s)**: given goal subject s, find a two-stage wiring:
   - Stage 1: find proc P with facts (s, P.fact_rel, *).
   - Execute P on s (black box via rebind) to get mid.
   - Stage 2: find proc Q != P with facts (mid, Q.fact_rel, *).
   - Return wiring (P, mid, Q) or none.

3. **df_execute**: run P on s to get mid, run Q on mid to get ans.
   Procedures are black boxes; the dataflow only wires output to input.

4. **df_try hook** in ev_query, after compose_try, before trial.
   Recursion guard via workspace depth counter.

5. **Promotion**: on success, promote a dataflow record for r=93 so a
   later Z' query reuses the wiring directly.

## Arms

- TREAT: X+Y trained, dataflow on. Expect Z=2.
- ABL-X: r=91 MAPs deleted. Expect Z=-2 (no stage-1 proc).
- ABL-Y: r=92 MAPs deleted. Expect Z=-2 (no stage-2 proc).
- FRESH: no training. Expect Z=-2.
- NO-DF: dataflow disabled (one-line flip). Expect Z=-2 (proves causal).
- Z-REUSE: after TREAT solves Z, new facts (41,81,42),(42,81,43),
  (43,82,44),(44,82,45),(45,82,46), query (41,93) -> 3 via promoted
  dataflow record. Expect Z'=3.

## Kill bars (frozen)

- K1: TREAT Z ans=2. (discovery + execution work)
- K2: ABL-X Z ans=-2. (X causally necessary)
- K3: ABL-Y Z ans=-2. (Y causally necessary)
- K4: FRESH Z ans=-2. (training necessary)
- K5: NO-DF Z ans=-2. (dataflow mechanism causal, not trial luck)
- K6: 3/3 byte-identical runs per arm. (determinism)
- K7: No 93-specific or chain/count-specific literals in df_patch.zag
  (grep audit). Wiring discovered from facts, not template.
- K8: Z-REUSE ans=3 via promoted dataflow record (reuse, not re-discovery).

Verdict XDOMAIN-DATAFLOW-COMPLETE requires K1-K8 all PASS.
Any FAIL -> verdict records which bar failed and why.

## Baselines

- A/B/C all scored Z=-2 on this world (composition_xdomain report).
  Dataflow must do strictly better (K1) to claim progress.
- NO-DF arm isolates the dataflow contribution vs base trial.

## Researcher-owned vs learner-owned

Researcher-owned: world facts, registry extraction procedure, discovery
algorithm, execution via rebind, kill bars.
Learner-owned: X/Y MAP graphs, registry entries (from training), the
discovered wiring (P, mid, Q), the promoted dataflow record, all verify
outcomes.

The wiring (which proc feeds which, and the mid value 34) is NOT in
source. It is computed from goal facts at query time.
