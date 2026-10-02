# ADOPTION_RECOMMENDATION: TNN3-SUBSTRATE package

Lane: TNN3-SUBSTRATE, wave-20261001-2321pdt.
Prereg: SUBSTRATE_PREREG.md (frozen be112b78f; Amendments 1-2 recorded transparently).
Prototype: substrate_proto.zag (dev harness; frozen tnn2.zag never modified).
Documentation rule observed: no em-dashes in this document.

## 1. Evidence summary

The 2021pdt synthesis proved the H2/H4/H6/H7 re-attempts cannot proceed on the
frozen substrate: no learner-reachable construction, no contradiction trigger, no
learner-writable standing (six SUBSTRATE-ABSENT findings, re-verified by grep in
the prereg section 3). This lane designed the minimal addition package closing
those three gaps as generic machinery and verified it on a dev prototype:

- R0 REGRESSION: all 46 frozen self-tests pass 46/46 with the hooks in place.
  The hooks (standing bumps, contradiction trigger, pending-ticket scan, lbid at
  four selector sites) are behavior-preserving at cold start and under the
  self-tests' own contradiction/confirm traffic.
- V1 CONSTRUCTION: a BUILD ticket authored with guard slot 1 (inverted relative
  to the assemblers' fixed slot 0) builds through one generic service, executes
  correctly on the frozen ISA, and fails closed on guard-false exactly like
  researcher-built graphs. An assembler-shaped ticket builds through the same
  code path, proving content-neutrality: the service imposes no schema.
- V2 TRIGGER: every ev_observe contradiction yields exactly one REDERIVE ticket
  linking the superseded and the new fact; confirms and pure teaches yield none.
- V3 STANDING: confirm/contradict events accumulate (+1/-1) on per-node records;
  values persist unchanged across queries; lbid is identical to bid where no
  record exists.
- INTEGRITY: the prototype's package code is byte-identical to the prereg's PKG
  block (mechanical extraction, cmp-verified); the frozen tnn2.zag is untouched
  (sha256 re-verified); two prototype runs are byte-identical output.

## 2. Architecture accounting (final)

- Cognition source lines added: 197 (PKG-BEGIN..PKG-END, comments and blanks
  included; 14 functions + 5 constants).
- New hardcoded semantic cases: 0. New modes: 0. New bridges: 0. New routers: 0.
- New task-specific handlers: 0. Protected-core operations added: 0.
  execute(), the 4-op ISA, alloc_node, link_edge, ng/ns/eg/es: unmodified.
- Learner-state structures created: 904 ticket nodes (BUILD -41, REDERIVE -43,
  standing -44), topology-identified step nodes, BUILD_ROOT (node-0 field 24),
  STAND_ROOT (node-0 field 28), all on existing node/edge types.

## 3. Recommendation

Adopt the package into the TNN-2 lineage's cognition layer (the same layer as the
assemblers and trial loop) as the substrate for the H2R/H4R/H6R/H7R re-attempts,
which are blocked without it. Do not place any of it in the protected core: the
package is machinery around the ISA, not ISA, and the ISA ruling's freeze holds.

## 4. Explicit governance statement

Adopting anything into the protected core is a GOVERNANCE DECISION for Micah
(protected-core boundary change). This package requests no protected-core change
and this recommendation does not ask for one. Separately, landing this package in
the frozen TNN-2 lineage changes the frozen baseline that six lanes verified
against; that baseline change is likewise Micah's decision, not this lane's.
This lane recommends; it does not adopt.

## 5. What the package does not do (re-attempts' burden)

Ticket authoring by the learner, REDERIVE-ticket interpretation, EXECUTE wired
into ev_act (blocked on the pending placement ruling, amendments A-C), and generic
cross-type queries (H10 follow-on) are all out of scope by design. A re-attempt
whose sealed driver hand-authors ticket content fails its L3 novelty bars by
construction; the frozen kill bars (prereg section 8) enforce this.

## 6. Residual risks

- Standing composition (lbid = standing where a record exists, else bid) is the
  substrate default; H6R may need full replacement semantics, which its bars cover.
- ls_bump's +1/-1 polarities are researcher constants; the H6R bars test whether
  trajectories built from them discriminate, which is the actual claim.
- The BEQ fail-closed convention (Amendment 1) matches the assemblers but cannot
  express else-branches; a re-attempt needing them must propose the extension.
