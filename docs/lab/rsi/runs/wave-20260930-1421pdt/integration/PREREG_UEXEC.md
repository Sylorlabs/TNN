# PREREG_UEXEC: MAP bodies as executable ISA graphs (H-UEXEC)

Date: 2026-09-30. Worker: integration worker, wave-20260930-1421pdt.
Status: FROZEN before any implementation. No edits after this file exists
except an explicit amendment record. Implementation must follow this
document exactly.

## Hypothesis H-UEXEC

CAM-1's APPLY-time per-kind interpretation (eval_body's four-way branch on
body_kind in cam1.zag) can be replaced by compiling each promoted MAP into
a 4-op ISA executable graph of the exact type CLA-2's EXECUTE runs, with
APPLY = build frame + EXECUTE(graph root, frame) + read output. The causal
MAP and the learned procedure then share ONE executable graph type and
differ only in their evidence/lifecycle edges (SUPPORTS/CONTRADICTS,
standing threshold, exact-hit facts), per Micah's confirmed direction that
procedure and causal rule converge to the same executable graph type with
different evidence/lifecycle edges, not separate engines. ACT's signed-bid
selection generalizes to choosing among competing graphs.

## Background and information gap

- cam1.zag (818 lines, commit 371d20743) PROMOTE reifies verified
  candidates as MAP nodes (refs [trigger, 0, group, 0], payload
  [body_kind, in_a, in_b, literal]), but APPLY evaluates bodies through
  eval_body, a per-kind branch chain (B_LITERAL/B_COPY_A/B_DBL_A/B_ADD_AB).
  Those four apply-time semantic handlers are the information gap: the
  body semantics live in source, not learner state.
- cla2.zag (1419 lines, commit e639904f2) implements EXECUTE(root, frame)
  over the closed 4-op ISA {MOVE(101), BRANCHEQ(102), INC(103), DEC(104)}
  with cells chained by SEQ edges (etype 12), frame-slot operand encoding
  (>=1000), literal cells (node id, value in payload[0]), and output at
  the root cell's ref[0]. The op dispatch is the justified minimal fixed
  point (EXECUTE placement amendment A); it names no domain concept.
- act.zag (615 lines, commit f7d87938f) selects actions by signed evidence
  bid from learner-state edges only. This build generalizes that selector
  to MAP choice (select_map): signed bid, no graph-content inspection.

## Construction plan (frozen)

uexec.zag is built by copying cam1.zag VERBATIM, then applying exactly
these diffs:

1. Add the EXECUTE machinery ported from cla2.zag unchanged in semantics:
   OP tags 101-104, SEQ edge type 12, operand encoding (>=1000 frame slot,
   >=0 literal-cell node id, <0 absent), frame as a node with payload
   slots 0-3, frame_get/frame_set, resolve_op, seq_next, execute,
   execute_value, EBUDGET 1000. The op dispatch table is reused verbatim;
   zero new core ops.
2. Add compile_graph(ws, es, m, kind, in_a, in_b, literal) -> root cell.
   Called at PROMOTE time only (construction). Maps each body kind to an
   ISA graph of cells chained by SEQ edges:
   - LITERAL c: lit=T_CELL node pay0=c; root=MOVE(slot2, lit).
   - COPY_A: root=MOVE(slot2, slot0).
   - DBL_A: MOVE(ctr,slot0); MOVE(out,slot0); loop BRANCHEQ(ctr,zero,done,body);
     body: INC(out); DEC(ctr); back to branch; done=MOVE(out,out) terminal.
   - ADD_AB: same loop over slot1 instead of slot0.
   COPY_B/DBL_B reuse COPY_A/DBL_A shapes with slot1 as the source.
   Frame slots: 0=in_a value, 1=in_b value, 2=out, 3=counter.
   Zero cell: T_CELL node pay0=0, shared.
3. run_loop change: for each candidate, compile its graph FIRST, then
   VERIFY by EXECUTING the graph over every held-back triple (EQ compare
   to the held-back object; missing input fact or non-clean halt fails
   the candidate). PROMOTE links the MAP node's ref[3] to the verified
   graph root and writes SUPPORTS/INSTANCE edges exactly as before. The
   payload body_kind stays as a construction audit trail; the query path
   never reads it.
4. APPLY (query) change: exact-key lookup unchanged. On miss, select the
   highest-standing (signed bid from edges only) MAP with trigger==r and
   standing>=1; build a frame from the subject's input facts
   (slot0=(s,in_a), slot1=(s,in_b)); return execute_value(root, frame);
   non-clean halt or missing input fact means that MAP cannot apply
   (skip to next, else -2). eval_body is DELETED; no body-kind branch
   exists in the query path.
5. Add select_map (ACT-style): signed bid = SUPPORTS - CONTRADICTS from
   edges only, no graph-content inspection; highest bid wins; exact-hit
   priority preserved in query.
6. Tests: port all six CAM-1 tests verbatim (W2, W3, NEG, P6, P7, P4) plus
   three new ones:
   - T-BID: two competing MAPs for one trigger; higher standing applies;
     adding CONTRADICTS to flip standing flips the answer.
   - T-GRAPH-SHARE: a second MAP node with independent evidence edges
     reuses the first MAP's graph root; demoting the original (standing
     below threshold) still yields the executed answer through the new
     MAP. Demonstrates the graph is content, decoupled from lifecycle.
   - T-DUMP: white-box dump of every MAP's ISA graph; asserts each MAP
     with a trigger has root>=0 with >=1 reachable cell, all tags in
     {101..104} or T_CELL.

## Frozen fixtures

Self-designed synthetic fixtures identical to the CAM-1 build (W2:
8001..8008/801..805/9501..9505; W3: 9001..9010/601/602/600; NEG:
7001..7005/701/702; P6: 7101..7105/711/712; P7: 8001..8008/801;
P4: 1001/1002/101/102/999). Builders stay blind to sealed FW1-FW9;
no sealed file is accessed.

## Kill bars (frozen; never moved after implementation)

- K-U1 (commit-order self-check): this prereg strictly precedes
  uexec.zag. ORDER.txt records creation order; prereg is first.
- K-U2 (no semantic handlers in APPLY): the APPLY/query path contains
  zero body-kind branches. Audit: grep for B_LITERAL()/B_COPY_A()/
  B_COPY_B()/B_DBL_A()/B_DBL_B()/B_ADD_AB() in functions
  {query, select_map, execute, frame_get, frame_set, resolve_op,
  seq_next, execute_value} returns 0 hits. Kind references are allowed
  only in compile_graph and the candidate tuple (construction time).
- K-U3 (behavioral parity with CAM-1): W2 (1 group, 5 promoted, 5/5
  probes, exact-hit 9503), W3 (1 group, 1 promoted, probes 30 and 15,
  exact-hit 10), NEG (0 promoted, -2/-2), P6 (0 promoted with verify,
  >=1 without, wrong probe 6), P7 (9501 before, -2 after 2 contradicts),
  P4 (201, -2, -2). Any deviation fails the build.
- K-U4 (determinism): 3/3 runs byte-identical; sha256 recorded in the
  run log.
- K-U5 (graph inspectability): T-DUMP passes: every MAP with a trigger
  has root>=0, >=1 reachable cell, tags only in {101,102,103,104}
  or T_CELL.
- K-U6 (bid selection): T-BID passes: higher standing applies; the
  contradict flip changes the answer; selection reads edges only.
- K-U7 (governance): pure Zag; zero Python invocations (NAMECHECK Step 0
  recorded); docs dash-clean; pinned compiler
  src/tools/toolchain/znc_linux_x86_64_abed8aa1; FW1-FW9 untouched.
- K-U8 (One-System accounting): recorded in the result doc: cognition
  source lines added, new hardcoded semantic cases (must be 0), new
  modes (0), new bridges (0), new task-specific handlers (0), new core
  ops (0), learner-state structures created.

## Known boundaries (pre-registered, not post-hoc)

- The kind->template mapping in compile_graph is researcher-authored
  construction-time machinery (6 templates), honestly recorded. This
  build removes apply-time handlers; learner-authored construction of
  the templates themselves is future work (the L3B line), not claimed.
- ADD/DBL loop bodies assume non-negative inputs; a negative input
  exhausts the execution budget and is treated as cannot-apply (the
  same class as a missing input fact). All fixtures use non-negative
  values.
- No L3 claim of any kind. Templates are researcher-enumerated; the
  discovered regularities are bounded L2 trials. Verdict is
  BUILD-PASS/BUILD-FAIL only.

## Expected result

BUILD-PASS if all kill bars hold: CAM-1 behavioral parity with zero
apply-time body-kind branches, 3/3 byte-identical, bid-driven selection,
dumpable ISA graphs. Any kill bar failure is BUILD-FAIL with the killing
evidence recorded.
