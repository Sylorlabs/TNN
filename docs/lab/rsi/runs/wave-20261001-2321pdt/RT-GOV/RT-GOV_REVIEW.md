# RT-GOV REVIEW: TNN3-SUBSTRATE DESIGN-COMPLETE proposal

Reviewer: RT-GOV (architecture and protected-core boundary review).
Wave: wave-20261001-2321pdt. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Read-only toward the lane dir; no lane artifacts modified.
Toolchain: safebin active, `which python3` and `which python` both return nothing (Step 0 recorded in NAMECHECK.md). No Python invoked by this reviewer at any point.

## Provenance and evidence base

- Prereg: docs/lab/rsi/runs/wave-20261001-2321pdt/TNN3-SUBSTRATE/SUBSTRATE_PREREG.md, frozen alone at commit be112b78f (2026-10-02 06:34:35 UTC).
- Prototype: same dir, substrate_proto.zag + dev_checks.zag + build_proto.sh + proto_run.log, committed at a11dde4b9 (2026-10-02 06:40:31 UTC).
- Adoption recommendation: ADOPTION_RECOMMENDATION.md (commit f77b7c7d5). Judge brief: JUDGE_BRIEF.md (same commit).
- Frozen baseline: docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, 1591 lines.

## Mechanical verification (all by shell tools, byte-level)

1. Commit order: `git merge-base --is-ancestor be112b78f a11dde4b9` passes; be112b78f (06:34:35 UTC) strictly precedes a11dde4b9 (06:40:31 UTC). Prereg frozen before implementation. HOLDS.
2. PKG byte-identity: sed-extracted PKG-BEGIN to PKG-END from the working-copy prereg and the working-copy prototype are byte-identical (cmp clean), 197 lines each, sha256 be4e5867ac305ba8ebe190922f7741f6a4c053729f99064354606c146affdff8. The same 197-line block with the same hash is in both files as committed at a11dde4b9. HOLDS.
3. Frozen baseline untouched: sha256 of tnn2.zag is a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd, matching the prereg's recorded hash character for character. HOLDS.
4. Line count: 197 exactly, comments and blank lines included. Honest. HOLDS.
5. Determinism: re-running the committed substrate_proto binary reproduces the committed proto_run.log byte-identically (TOTAL 46/46, PROTO-REGRESSION PASS, V1-PASS, V2-PASS, V3-PASS, SUBSTRATE-VERIFY ALL-PASS). HOLDS.
6. Lane docs pass the no em-dash check (check_no_dash.sh exit 0 on all four lane docs).

## AXIS 1: ONE-SYSTEM RULE. Verdict: HOLDS.

I read the PKG block (PKG lines 1-197) line by line. Findings:

- No modes: no function branches on a mode flag or task identifier. Every conditional is on structural vocabulary: node type 904 (PKG lines 56, 71, 75, 132, 160), operation codes -41/-43/-44 (lines 132, 146, 160, 173), frozen ISA tags 101-104 (lines 57, 84), the documented operand-spec encoding (lines 98-107: >=1000 frame-slot, <0 back-reference, else literal), the LS_NONE sentinel for record presence (lines 194-195), and allocation bounds (e<4096, nst<64, np<64).
- The "ticket" admission filter in lb_run (lines 129-136) checks `ng(W,t,24)==-41 && ng(W,t,28)==0`: an operation-code plus pending-status filter, not a domain gate. It is the same class of filter as ISA tag acceptance in execute(): it gates on the package's own structural vocabulary, which is machinery, not a mode switch on ticket type. No branch ever conditions on ticket content.
- One generic service: lb_build_ticket (lines 69-121) is a single two-pass materializer for every ticket. There are no special-cased paths for BUILD vs REDERIVE vs assembler-shaped tickets. REDERIVE (-43) tickets are intentionally inert data (interpretation is H7R's hypothesis, prereg section 7); this is deferred capability, not a hidden mode.
- The three-way spec decode is a data-driven documented encoding, not task-specific admission logic: the builder writes spec values verbatim and performs no semantic validation (prereg section 4A states this; the code shows no conditioning on what the specs mean).
- lbid (lines 192-196) is a sentinel-composition, not a router: it returns a standing value where a record exists and the frozen bid() otherwise. It selects between two numbers by record presence; it never selects between subsystems. Not a router.
- No bridges, no routers, no new handlers: no new edge types are introduced. BUILD_ROOT/STAND_ROOT are type-2 GROUP nodes with ET_MEM(10) membership edges and ET_PRO(9) self-pins via `link_edge(W,r,9,r,hg(W,4))`, exactly the frozen conventions: ET_MEM(10) is the same edge POLICY_ROOT uses for guides (frozen tnn2.zag line 810: `link_edge(W,pr,10,g,0)`), and the self-pin matches frozen lines 301, 313, 761. The roots are registers in existing node-0 fields, not connectors between subsystems.
- Register and type claims in prereg section 3d re-verified: node type 904 has zero occurrences in the frozen source; node-0 fields 24 and 28 are never read or written there (only field 20 via pol_set); field-36 existence convention matches frozen usage. Type 902 appears in the frozen source (4 occurrences), so the builder's inline literal convention (`ns(W,ln,0,902)`, PKG line 105) copies existing practice.
- The adoption diff's four lbid call sites match the frozen bid() call sites exactly (frozen lines 145 activate, 259 evict_node, 872 and 884 ev_act; prototype lines 145, 259, 874, 886 with the +2 line shift from hook insertions). The test-battery sites keep `bid(` (prototype lines 956, 988, 1208, 1213, corresponding to frozen 954, 986, 1206, 1211). The three ev_observe returns each get `lb_run(W)` (prototype lines 843, 856, 858); the confirm branch gets `ls_bump(W,n,1)` (line 842) and the contradiction branch gets `lt_fire(W,n,nn); ls_bump(W,n,-1)` (line 855). The applied diff matches the prereg's specified diff mechanically.

## AXIS 2: PROTECTED-CORE ISA RULING. Verdict: HOLDS, with two disclosed residuals.

- Zero new protected-core ops: the PKG calls only pre-existing functions (alloc_node, write_node, link_edge, seq_link, seq_nx, ref_prot, z_alloc, set32, get32, ng, ns, eg, hg, bid; all confirmed present in the frozen source at lines 28-318). execute() is unmodified. The frozen 4-op ISA tags 101-104 are used verbatim; no new opcodes. The tag check in lb_step_add/lb_build_ticket is ISA-tag validation (machinery, same class as execute()'s tag acceptance), not a semantic case.
- Forbidden-class audit of all 14 functions and 5 constants: no function detects a target-domain regularity. lt_fire fires unconditionally on every fact contradiction (no threshold, no type check). lb_build_ticket materializes specs verbatim with no semantic validation. ls_bump applies fixed event polarities. No FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE, LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL, or equivalents, and no equivalent disguised as plumbing.
- Residual 1 (disclosed by the lane, still Micah's call): ls_bump's +1/-1 polarities are researcher constants. The prereg (section 4C) admits this and frames them as event polarities analogous to the existing ET_CFM/ET_CON self-edges; ADOPTION_RECOMMENDATION section 6 lists it as a residual risk with the H6R bars testing the trajectories. It is not a semantic case, but it is a researcher constant at the composition seam.
- Residual 2 (disclosed by the lane): lbid's record-wins-else-bid composition is the substrate default; H6R may need full replacement semantics (ADOPTION_RECOMMENDATION section 6). An honest scoping statement, not a hidden choice.
- Absence citations in prereg section 3 re-verified against the frozen source: the six cell constructors sit at lines 338-361; all call sites are within constructor bodies (347, 351, 355, 359), the assembler region (366-405, including the hardcoded slot-0 `t2_guard(W,0,lx)` that V1 discriminates against), and t2_revise_graph (725-726). None is reachable from ev_observe, ev_query, or ev_act. ev_observe (836-857) never calls mp_run or t2_trial (those calls sit at lines 827 and 670, outside ev_observe). bid() is at 237-248. Amendment 1's fail-closed convention matches the frozen ISA's documented behavior (frozen line 327: "A GUARD cell (BRANCHEQ) with no SEQ fallthrough fails closed").

## AXIS 3: GOVERNANCE. Verdict: HOLDS, with one process note (QUALIFY) and one documentation precision fix requested.

What the lane did right:

- The recommendation's scope is honest: it asks only for cognition-layer adoption of the 197-line package, explicitly requests NO protected-core change, and states plainly that the frozen-baseline change is Micah's decision, not the lane's. It lists non-goals (ticket authoring, REDERIVE interpretation, EXECUTE in ev_act, cross-type queries) and residual risks. It does not adopt anything. The JUDGE_BRIEF's escalation section matches: "No irreversible architecture commitment was made; the prototype touches only lane-local files."
- No irreversible commitment exists. The prototype is lane-local; the package is additive and reversible by reverting the specified diff. Nothing was pushed; commits are local on tnn-native-lab.

Process note (QUALIFY, does not change any verdict above):

- The frozen prereg at be112b78f contains the 198-line PKG and no amendment text. Amendments 1-2 were applied to the prereg in place and committed inside the prototype commit a11dde4b9. The amendment diff is exactly the one line claimed (`if(ng(W,c,0)==102){ns(W,c,16,get32(cells,(i+1)*4));}` deleted; 198 to 197 lines), the rationale is recorded in section 11, the kill bars were not changed, and all verification evidence (R0 46/46, V1/V2/V3, byte-identity) was produced against the amended design consistently. This is transparent amendment practice, but it is not a separate re-freeze: the amended prereg was never frozen alone before the prototype was built from it. Under Micah's rule ("if a prereg is broken, amend transparently and re-freeze rather than pretending the execution was valid"), the amendment half is satisfied; the re-freeze half is not, strictly speaking. Recommend Micah either accept this instance (evidence is internally consistent) or require future amendments to re-freeze alone before implementation. This is decision 5 below.

Documentation precision fix (requested before any adoption):

- ADOPTION_RECOMMENDATION.md section 2 says "Learner-state structures created: 904 ticket nodes (BUILD -41, REDERIVE -43, standing -44)". Read plainly, "904 ticket nodes" looks like a count; it is the node TYPE (904). Recommend changing to "type-904 ticket nodes" to avoid the count reading. No evidence is affected.

The one downstream coupling Micah must see:

- Re-attempt kill-bar precondition G1 requires each re-attempt to re-verify the package on the adopted build. If Micah adopts and the re-attempts freeze their bars against the adopted baseline, a later reversal would invalidate those bars under his bar-change rule. Adoption therefore carries a soft irreversibility: cheap to revert technically, expensive to revert scientifically once re-attempts freeze against it. This is stated in the recommendation's governance section; it belongs in the decision below verbatim.

## ESCALATION: exact governance decisions for Micah (verbatim-ready)

1. Adoption: "Adopt the 197-line TNN3-SUBSTRATE package (PKG-BEGIN to PKG-END, sha256 be4e5867ac305ba8ebe190922f7741f6a4c053729f99064354606c146affdff8) into the TNN-2 lineage's cognition layer, with the specified adoption diff (lb_run at ev_observe's three returns; ls_bump +1/-1 and lt_fire hooks; lbid at the four selector sites 145, 259, 872, 884), as the substrate for the H2R/H4R/H6R/H7R re-attempts? No protected-core change is requested."
2. Baseline: "Accept that this changes the frozen baseline six lanes verified against (frozen tnn2.zag a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd), with the pre-package baseline preserved in git history for the sealed SUBSTRATE-ABSENT findings? Note: once re-attempts freeze their kill bars against the adopted build, reversing the adoption invalidates those bars."
3. Standing composition: "Accept lbid's record-wins-else-bid composition as the substrate default, with H6R allowed to propose full replacement semantics under its own bars, or direct a different composition rule now?"
4. Polarities: "Accept the +1/-1 confirm/contradict polarities as fixed machinery (analogous to the existing ET_CFM/ET_CON self-edges), or require learner ownership of polarity magnitudes before H6R freezes its bars?"
5. Amendment discipline: "Accept Amendments 1-2 as committed inside the prototype commit (evidence is internally consistent; one-line deletion, bars unchanged), or require future prereg amendments to re-freeze alone before implementation?"

Informational (no decision needed): the EXECUTE placement ruling (amendments A-C) remains pending and still gates H4R's B4; this package does not ask for it. Documentation fix requested: "type-904 ticket nodes" instead of "904 ticket nodes" in ADOPTION_RECOMMENDATION.md section 2.
