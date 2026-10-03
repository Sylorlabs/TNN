# Spec Errata: Build-Blocking Corrections and Frozen-Prereg Discrepancies

Status: COMPILATION ONLY. Nothing here has been fixed. This document collects
factual errors found in specification documents so the next build's
preregistration can correct them explicitly. Frozen-prereg discrepancies are
recorded, not amended: amendment of a frozen prereg is a banked Micah decision.

Conventions: E-numbers are errata (factual errors in a spec). G is a resolved
gap (an open question now closed, recorded so the build does not reopen it).
R-numbers are documented design risks (honest limits already stated in the
specs, not errors; included because a build that ignores them repeats a
known hazard).

## E1. BUILD_QUESTIONS Q1: splice-trace fields do not exist on the frozen layout

**Wrong spec:** `composition_build/BUILD_QUESTIONS.md`, section Q1 ("Splice
trace storage format"), commit `97b80383a`.

**What was wrong:** Q1 specified the per-SETREG rebound-vs-nulled trace as
"Field 12: n_trace" plus "Fields 40 + i, for i = 0 .. n_trace - 1: the cited
fact node id", and claimed the layout was "verified against the frozen base
source."

**What is correct:** The frozen node is 40 bytes with 10 fields (offsets
0-36). Fields 40 through 68 do not exist. Writing to field 40 of node n
would corrupt field 0 (the tag) of node n+1. The Q1 layout as written is not
implementable on the frozen node layout.

**Found by:** `fragment_record/FRAGMENT_RECORD.md` section 0, commit
`8b7b0f12a`. The same commit independently confirmed the error (also see E2
reporter `fragment_guard/FRAGMENT_GUARD.md` finding 5, which re-verified that
fields 40-68 do not exist in the frozen 40-byte layout).

**Resolution path (specified, not implemented):** FRAGMENT_RECORD.md section 2
declares a node enlargement from 40 to 72 bytes (18 fields, offsets 0-68),
which simultaneously validates Q1's intended layout. Until the build adopts
the enlarged node, Q1's fields 40-68 must not be used.

**Impact:** BUILD-BREAKING. Any build proceeding from BUILD_QUESTIONS.md as
written would corrupt memory (silent tag corruption of adjacent nodes), not
fail loudly.

**Required build-preregistration statement:** the node size (40 vs 72 bytes)
must be stated explicitly; Q1's layout is valid only under the enlargement.

## E2. FRAGMENT_RECORD section 1.2: guard location is dead code

**Wrong spec:** `fragment_record/FRAGMENT_RECORD.md`, section 1.2
("Production guard requirement"), commit `8b7b0f12a`.

**What was wrong:** Section 1.2 required a `ng(W,m,24) != -2` guard in "the
query path (`activate`, `ev_query`)" before any MAP-shaped read, and stated
that "no guard is needed" in `revise_on_contradict` (second bullet).

**What is correct:** `activate` (frozen base line 140) scans only tag-1 FACT
nodes; `ev_query` routes through `activate`, `t2_trial`/`t2_gather` (tag-1
only), `bootstrap_miss` (tag-1 only), and `miss_inquire` (no MAP scan). The
query path never enumerates tag-20 nodes and cannot mistake a fragment for a
MAP. The guard as specified would be dead code.

The actual vulnerable location is `revise_on_contradict` (frozen base line
690): the ONLY production function that enumerates tag-20 nodes, and it has
NO field-24 check. Fragments are safe there today only under a BUILD-TIME
INVARIANT (fragments never carry outbound type-1 prov edges, so the inner
`eg(W,e,4)==1` check skips them). If that invariant is ever violated,
`t2_revise_graph` would misread fragment fields (root read as topology,
s/r read as -1, answer read as F-shape signature) and `ns(W,m,28,out)` would
silently overwrite the F-shape signature, corrupting the fragment store and
breaking fragment dedupe. The invariant violation produces silent
corruption, not a crash.

**Found by:** `fragment_guard/FRAGMENT_GUARD.md` sections 6.1 and 6.2, commit
`0266321cc`.

**Recommended (defense in depth, negligible cost):** add
`&& ng(W,m,24)!=-2` to the enumeration condition at line 690. One field read
per live MAP per contradiction; contradictions are rare.

**Also flagged by the same verifier (not errors, completeness items):**
`map_standing` must be guarded if it ever becomes production (currently
test-only); `ev_act` enumerates candidates via POLICY_ROOT edges with no tag
filter (latent risk: fragments are not linked to POLICY_ROOT in the design,
but if they ever were, field 4 = -1 and field 20 = cell id would be misread
as relation/answer; the build must verify by inspection).

**Impact:** Not breaking (an unnecessary guard is harmless), but the build's
preregistration must correct the guard location, or the guard is absent where
it is needed and present where it can never fire.

## E3. Frozen H3-lite prereg `9084a7760` Section 3: initial trial order is factually incorrect

**Wrong spec:** frozen H3-lite prereg `9084a7760`, Section 3. NOT amended by
this document.

**What was wrong:** The prereg states: "Initialized to 2,1,0,3,4,5
(researcher's current literal order)" and describes the current order as
"chains k=4,3,2, then sum, then count, then single hop."

**What is correct:** The frozen source (`tnn2.zag` line 593) does
`let k:i32=2; while(k<=4 && ans==-2)`, trying k=2, then k=3, then k=4
(ascending): families 0,1,2 in that order, followed by sum (3), count (4),
single hop (5). Actual source order: 0,1,2,3,4,5.

**Found by:** `h3lite_node1/H3LITE_NODE1.md`, "Prereg discrepancy
(documented, not hidden)" section, commit `45c55ed83`. The Node 1
implementation initialized the policy node to the ACTUAL source order per
the prereg's own "copy-then-revise" bootstrap rule; copying the prereg's
incorrect description would have changed behavior on first use.

**Downstream consequence (active):** the frozen weak K-LT-5 prereg
(`weak_klt5/WEAK_KLT5_PREREG.md`) repeats the [2,1,0,3,4,5] initial order in
seven places (lines 64, 97, 120, 143, 155, 245, 255), including the Phase-B
reset procedure ("reset the trial-order policy node ... to initial values:
order fields [2,1,0,3,4,5]"). The sealed-world design
(`weak_klt5_world/WORLD_DESIGN.md` section on R1-R5, commit `94011d705`) used
the ACTUAL order [0,1,2,3,4,5] from the built implementation for its
predicted trajectories (E(A)=30, E(B)=20, R=1.50).

**Impact:** The frozen weak K-LT-5 prereg is internally consistent as written
(the reset procedure and the predicted trajectories both assume [2,1,0,3,4,5]
in the prereg text), but it does not match the built implementation's actual
initial order. An evaluator following the frozen reset procedure verbatim
would reset the policy node to [2,1,0,3,4,5], a permutation the
implementation never produces on its own; the predicted R=1.50 was computed
under the actual [0,1,2,3,4,5]. Resolution requires a transparent prereg
amendment, which is a banked Micah decision. This document does not amend.

## G1. Resolved gap: fragment record tag and F-utility field offsets

Not an erratum. BUILD_QUESTIONS.md Q3 identified an information gap: "the
design never specifies the fragment record's node tag or F-utility field
offsets; the build must specify these." FRAGMENT_RECORD.md (commit
`8b7b0f12a`) closed it: tag 20 (MAP), no new tag; F-utility invocations =
field 12, successes = field 16; full field layout in its section 3. Recorded
here so a future build does not treat the gap as still open.

## R1-R4. Documented design risks (not errata)

These are honest limits already stated in the specs. They are included
because ignoring them in a build repeats a known hazard.

- **R1. Discount threshold T=2 is a researcher magic number**
  (`discount/DISCOUNT.md` sections 3.2 and 5.3). Mitigation stated: fix once,
  report T=1/2/3 sensitivity, never tune per benchmark. Tuning T until a
  desired result appears is a treadmill surface.
- **R2. Discount is source-blind** (`discount/DISCOUNT.md` section 5.1, "the
  deep limit"). The W3 majority heuristic excludes minority evidence even
  when the minority is the only genuine observation; it fixes fragility by
  preserving a self-referential loop. Source provenance tags remain the
  actual fix. W3's majority heuristic punishes truth when the majority is
  wrong and is flagged for adversarial testing.
- **R3. Corruption detector attribution is world-granular, not event-granular**
  (`corruption_detector/CORRUPTION_DETECTOR.md` section 3). CORRUPTION events
  are emitted at boundary processing; the corruption occurred at some unknown
  point during the preceding world's stream. Measures must not treat the
  event as timestamped to the boundary tick.
- **R4. Zero CORRUPTION count is evidence of no detected corruption, not proof
  of none** (`corruption_detector/CORRUPTION_DETECTOR.md` section 11). The
  core check covers MAP roots only; interior guard-target and literal-operand
  corruption require the section 9 extensions.

## Standing note

E1 and E2 are eligible for correction inside the next build's
preregistration under normal copy-then-revise. E3 touches a frozen prereg
(`9084a7760`) and a second frozen prereg that depends on it (weak K-LT-5);
any amendment must be transparent and re-frozen per Micah's standing rule
(no silent reinterpretation of a frozen kill bar).
