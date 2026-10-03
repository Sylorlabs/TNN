# JUDGE_BRIEF: TNN3-SUBSTRATE

## Provenance header

- RENDER_SHA: 8a2ca227d645409b9c3968811e6627f22437af5bad6923616a10609646e7822e (filled at render time; to verify, restore the value on this line to TBD and recompute sha256 over the file)
- FIRST_RENDERED_WAVE: wave-20261001-2321pdt
- COMPONENT_LINEAGE: 2021pdt TNN3-SYNTH synthesis ("TNN-3 needs additions, not
  compression") and its six SUBSTRATE-ABSENT findings: H2 inversion (no
  learner-reachable construction path), H3 procedure-as-operand (no
  graph-as-fact-operand path), H4 projection authoring (no learner cell
  authoring; EXECUTE unreachable from ev_act), H6 standing (no
  learner-updatable standing; no CONFIRM/CONTRADICT events), H7 re-derivation
  (no learner construction process; no contradiction-to-construction trigger),
  H10 unified workspace (no learner-addressable workspace); frozen substrate
  docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag (1591 lines,
  sha256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd).
- NEW_KNOWLEDGE_CLAIM: A 197-line, zero-new-opcode addition package (learner
  construction service plus contradiction trigger plus learner-writable
  standing) closes the three substrate gaps that stopped H2/H4/H6/H7, verified
  behavior-preserving on 46/46 frozen self-tests and content-neutral on sealed
  dev checks.

Documentation rule observed: no em-dashes in this document.

## Verdict

DESIGN-COMPLETE. All four deliverables landed: (1) SUBSTRATE_PREREG.md frozen
alone before implementation (commit be112b78f; Amendments 1-2 transparent);
(2) pure-Zag dev prototype with verification-first checks R0/V1/V2/V3 all
passing; (3) frozen kill bars KB-H2R, KB-H4R, KB-H6R, KB-H7R; (4) this
recommendation, which recommends but does not adopt.

## Evidence a judge can re-run

In docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE/:
sh build_proto.sh rebuilds substrate_proto from the frozen tnn2.zag plus the
prereg's PKG block (mechanical extraction, byte-verified identical) plus
dev_checks.zag; ./substrate_proto prints TOTAL 46/46, PROTO-REGRESSION PASS,
V1-PASS, V2-PASS, V3-PASS, SUBSTRATE-VERIFY ALL-PASS (proto_run.log). The frozen
tnn2.zag was never modified (hash re-verified at every build).

## Architecture accounting

197 cognition lines added; 0 hardcoded semantic cases; 0 modes; 0 bridges;
0 routers; 0 task-specific handlers; 0 protected-core ops. Learner-state
structures: 904 ticket nodes (-41 BUILD, -43 REDERIVE, -44 STAND),
topology-identified step nodes, BUILD_ROOT (node-0 field 24), STAND_ROOT
(node-0 field 28); all existing edge types.

## What this unblocks, and what stays gated

Unblocked: H2R (inversion), H6R (standing), H7R (re-derivation), and H4R's
construction half, each with frozen kill bars. Gated: H4R's closed loop waits
on Micah's pending EXECUTE placement ruling (amendments A-C); ticket authoring
by the learner and REDERIVE interpretation are the re-attempts' hypotheses, not
this package. Adoption into the TNN-2 lineage (and any protected-core change,
of which this package requests none) is Micah's governance decision.

## Escalations for Micah

None created by this lane beyond the standing ones: the pending EXECUTE
placement ruling (amendments A-C) still gates H4R's B4 bar, and the adoption
decision itself is his. No irreversible architecture commitment was made; the
prototype touches only lane-local files.
