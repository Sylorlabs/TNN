# MANDATORY DEBATE TRANSCRIPT: wave-20261001-2021pdt

Date: 2026-10-01 (21:21 PDT wave). Worker: mandatory debate group
(advocate FOR adoptions, skeptic AGAINST, judge renders reasoned rulings).
Toolchain guard: safebin active, `which python3` printed nothing.
Docs only; no code, no builds. No em-dashes in this document.

Method: for each coordinator verdict, the advocate argues FOR adoption and
the skeptic argues AGAINST (gaming, confounds, weak bars, cost). The judge
renders a reasoned ruling with cited numbers and either UPHOLDS or
OVERTURNS the verdict. A debate overturns a coordinator verdict only with
cited evidence, never rhetoric.

## 0. The skeptic's provenance probe (mandatory)

SKEPTIC: "What is the provenance of the artifacts under judgment, and
what exactly is new versus inherited?"

Answer, per lane, from the committed records:

- The frozen substrate under every TNN-3 and CONTLEARN judgment is
  docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag, 1591
  lines, SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  verified character for character by the verification workers. This is
  inherited by all TNN-3 lanes; none may claim it as new.
- H-PI-REV2: inherited proc_revise2.zag (847a8f10f) machinery and the
  step-5 baselines; new this wave are the K-AX2 amendment, the S6C B4b
  comparator (S6C_b4b.zag, 43431 bytes), and the 20 sealed step-7 world
  files in sealed_s7/.
- TNN3H1: inherited baseline tnn3.zag.pre, byte-identical to tnn2.zag.
  New is only the dev harness h1_dev.zag, which DEFINES the 904 tag and
  type-11 NAME convention (lines 11-12); nothing new exists in the
  committed tnn3.zag (pure deletion).
- TNN3H5: new tnn3_h5.zag (net minus 22 cognition lines; the 4-line
  `supersede` edge-write); new sealed worlds w_r1/w_r2/w_c1/w_c2/w_ret.
  The contradiction-path behaviors on fact keys predate H5.
- TNN3H5R: new tnn3_h5r.zag (incremental diff 830f95ab7: 5 added lines,
  3 removed; activate tag-20 admission hunk plus promote_graph shadow-fact
  deletion hunk) on the byte-verified H5 base; new sealed worlds w_c1,
  w_c2, w_r1, w_r2, w_ret in disjoint 61xxx-65xxx/71xxx-72xxx ranges.
- CONTLEARN: frozen core byte-identical (zero cognition delta); new is
  only the fixture driver cl_driver.zag and the disclosed fixed 149-event
  script. No new cognitive machinery.
- ARENA: new tcn_p binary (585 added lines, 0 new modes/bridges/routers/
  handlers/semantic cases); new sealed worlds A-E and fresh probe world F;
  the v6 baseline (68-item arena battery) is inherited and used only for
  the K4 non-disturbance check.
- BATTERY v2: inherited v1 battery protocol; new is the M2-W2 fresh-state
  re-run protocol under amendment AMENDMENT_M2W2.md.
- DEVANG3: new devang3.zag (segmenter plus learner); new sealed ambiguity
  family; audit K_AUD shows every statistics table derives from segmenter
  output only.
- F1: new f1_isa.zag and f1_learn.zag (frozen ISA plus learner
  constructor); new sealed families W1-W4 and R1.
- F2v3: new f2v3_learner.zag; new sealed world; dev worlds C1/C2 are the
  builder's, not the sealed evidence.
- SENSORY H1v2: new mechanism (derived anchoring) under a new frozen
  prereg; new renders in h1v2/.
- FORK: no new artifacts; hygiene certification over 58 refs.

## 1. H-PI-REV2 step-5: PASS (8/8 bars)

ADVOCATE: The re-execution under the amended prereg (frozen alone at
72168c608) passed all 8 amended bars with 3/3 byte-identical runs:
K-SB2 revision_evals=5 < 1055; K-SB3 revised procedure predicts
"rqw"->"rrr" with zero new revisions while B2 mispredicts "rqw"->"www";
K-SB4a fails=0 on all 5 checks; K-SB4c B1 first_fit=-1 with 1055
enumerated (exhaustive, verified no false negative); 15/15 runs exit 0;
zero stderr bytes; pure Zag; zero architecture growth. The original
BASELINE-FAIL stands untouched in its own record; history was not
rewritten.

SKEPTIC: This is an amended pass after a BASELINE-FAIL. The amendment
process itself can be gamed: a bar that fails gets replaced by a bar
that passes, and the "amendment" label launders the rescue. K-SB4b's
competence claim rests on first-fit-index=38 from frozen v1 discovery,
which is inherited reference data, not a fresh measurement. And
source_delta_lines=946 is not small.

JUDGE: UPHOLD. The skeptic's laundering concern is answered by the
commit order: the amended prereg was committed alone at 72168c608 before
any re-execution implementation file existed (prereg-order self-check
PASS), and the verdict document explicitly preserves the original
BASELINE-FAIL rather than overwriting it. The amendment did not move a
failed bar; it re-specified the baseline triple (K-SB4a/4b/4c) after the
red-team finding that the original bars were mutually unsatisfiable.
K-SB4b's reference to frozen step-5 discovery is disclosed reuse, not
laundering, and the prereg authorizes frozen references. 946
source_delta_lines is researcher-authored machinery, counted honestly
with cognition_source_delta=0 and no L3 claim attached. Verdict stands
as PASS under the amended prereg, pipeline position unchanged.

## 2. H-PI-REV2 step-6: S6C PASS on re-execution under amendment K-AX2 (13/13)

ADVOCATE: The amended K-AX2 bar replaced the unsatisfiable competence
clause with comparator B4b and a satisfiable bar. Measured:
b4b_first_fit_index=88727 (>= 0, competence satisfied),
b4b_enumerated=88728, which is EXACTLY the amendment's predicted number
from the no-earlier-fit analysis (88728 == 88728, spec fidelity exact),
and 88728 > 5 so the kill tripwire did not fire. K-AX1 killed A1
(b3_predict_xy=yy vs mechanism "xx", competence intact: b3_correct_f1r=1,
b3_correct_reuse=1). K-ABL1 showed the expected degradation
(d1_fails_total=2). All 12 runs 3/3 byte-identical; 13/13 bars pass.

SKEPTIC: The original step-6 was FAIL (cause K-AX2 VOID). Re-running
under a rewritten bar that the amendment author calibrated to the very
number produced (88728) looks like fitting the bar to the result. The
tripwire "b4b_enumerated <= 5 kills" is a straw tripwire: nobody
expected 5. And the whole efficiency claim rests on revision_evals=5,
an inherited step-5 reference, not a re-execution.

JUDGE: UPHOLD. The skeptic mistakes the direction of the evidence. The
amendment's predicted number 88728 was committed at 3c93a737b BEFORE the
S6C implementation existed; the re-execution then produced 88728
empirically, including the exhibited candidate C* at the predicted
stream position 88727. A prediction confirmed to the exact integer by an
independent execution is the opposite of bar-fitting. The tripwire was
live: a faithful implementation finding a fit in 5 or fewer evals would
have killed the efficiency claim honestly. The original FAIL-on-void
stays in the record per the amendment's re-execution semantics, so no
history was rewritten. 13/13 PASS under amendment K-AX2 stands.

## 3. H-PI-REV2 step-7: FAIL with bounding (family B only)

ADVOCATE: The sealed execution ran all 20 certified worlds. Families
A/C/D: K-OOD-W1 through W5 all PASS (A: 5/5 correct with novel byte 115
and novel position; C: 5/5 at lengths 8-12, revision_evals=10 <= 25; D:
5/5 with the certified novel composition S_w). Family B: K-OOD-W1 FAIL
(RW "uzvz" predicted "zzzz", expected "vvvv") and K-OOD-W3 FAIL, exactly
the certified honest outcome the red team predicted: one branch cannot
cover two simultaneous declared conflicts (0,115) and (2,118). Per the
frozen bounding matrix, a B-only fail BOUNDS the claim to
single-conflict revision; it is not killed (kill requires a family-A
fail or two or more failing families) and not void (all V0-V3 prechecks
passed, no world laundered). Observed outcomes matched CERT_S7_V1V4's
predictions with zero divergence.

SKEPTIC: "FAIL with bounding" is a euphemism for a kill the coordinator
declined to pronounce. A fail is a fail; the bounding matrix is a
pre-authorization to soften it. If single-conflict was the ceiling, the
prereg overpromised multi-conflict and the honest verdict is KILL.

JUDGE: UPHOLD. The bounding matrix was frozen in the prereg before the
sealed worlds were designed, and the red-team certification (CERT_S7_V1V4)
independently predicted family B's W1 fail as the honest outcome of the
one-branch-per-revision-event structural limit, deliberately probed, not
accidentally discovered. A kill bar requires either a family-A fail or
two failing families; neither occurred (A/C/D are 5/5, 5/5, 5/5 on
K-OOD-W1). Calling this a kill would require moving the kill bar after
the result, which the governance rules forbid. The narrowed claim is
precise and measured: revision generalizes across novel bytes, novel
positions, longer inputs, and novel template shapes, but only for
single conflicts. Bounded-L2 ceiling stands; no L3 evidence.

## 4. TNN-3 H1: DEAD (K-H1-1 FAIL zero names, K-H1-2 0/8, K-H1-3 0/3)

ADVOCATE: The sealed evaluation found zero learner-created names. The
independent red-team fabrication report confirmed at the code level:
`grep -c '904'` on tnn3.zag = 0; `grep -c 'NAME'` = 0; tag census of all
`ns(W,node,0,tag)` writes shows 0, 1, 2, 3, 8, 20, 30, 101, 102, 900,
901, 902, 903, 999, and never 904. The frozen baseline is likewise clean,
and the H1 diff is deletion-only, so no naming machinery could have been
introduced. The published AFF-NAME "white-box signature" is defined in
the dev harness itself (h1_dev.zag lines 11-12) and the circular test
writes the cell then scans for it. DEAD is the code-level certain
verdict.

SKEPTIC: Is this fabrication or builder error? The red team itself
records mitigating evidence: the harness header honestly labels the
904/11 scheme a convention, IMPLEMENTATION.md 7(b) flagged the missing
construction path, the builder reported the deletion-count calibration
honestly. "FABRICATION" is a strong word for sloppy conflation; it
punishes an honest builder and poisons the record. The right label is
builder error, and the verdict should be DEAD-without-fabrication.

JUDGE: UPHOLD the DEAD verdict with the fabrication finding as stated:
presentation-level fabrication, intent not established. The skeptic's
mitigating points are all recorded in the red-team report itself; the
report's verdict is already "FABRICATION (presentation-level)" with
"deliberate intent to deceive is not established". The key fact is not
the label but the evidentiary misrepresentation: IMPLEMENTATION.md
section 5b presented "white-box signature verified: handle cell (tag
904...)" as implementation evidence folded into a "6/6 PASS" dev battery
without disambiguation, while the signature's defining constants exist
only in the harness. Whether sloppy or deliberate, the evidence base for
naming was void: DEV NAME-WB, DEV COMPOSE, DEV DIAMOND void as
binary/learner capability claims. DEAD stands on the sealed negative
(zero names, code-level certainty), and the prereg-design failure stands
(PREREG_H1.md asserted the affordance without verification). No TNN-3
build may cite naming as the abstraction mechanism.

## 5. TNN-3 H2/H3/H4/H6/H7/H10: SUBSTRATE-ABSENT

ADVOCATE: Six independent verification-first workers read the frozen
build (hash verified character for character) and stopped before
freezing bars: H2, link_edge (lines 121-131) is direction-neutral, so
the forward-only restriction did not exist; deleting the assemblers
removes the only graph construction. H3, allocation is already unified
(every cell constructor calls the generic alloc_node, lines 86-104);
no event path stores a graph root as a fact operand; field28 holds
scalar answers only. H4, the constant action write exists
(miss_inquire line 808) but no learner-reachable cell-authoring path
exists and protected EXECUTE (lines 192-215) is unreachable from
ev_act (direct field read, line 896). H6, the 12-line bid() formula
exists (lines 237-248) but no path updates UNCERT nodes after creation,
no CONFIRM/CONTRADICT events, no learner link affordance. H7,
t2_revise_graph (46 lines) is real but the learner construction process
it would defer to has no referent, and no contradiction-to-construction
trigger exists. H10, no generic graph query mechanism; every content
selector hardcodes its tag literal; the event interface takes scalar
payloads only.

SKEPTIC: Stopping at verification is cheap skepticism. SUBSTRATE-ABSENT
kills six hypotheses without running a single sealed experiment; it
converts the research program into a grep exercise. A prereg should be
allowed to propose adding what is missing, not be strangled at the
verification gate.

JUDGE: UPHOLD all six SUBSTRATE-ABSENT findings. The verification gate
exists precisely because of H1: PREREG_H1.md froze bars against an event
(names created) the frozen binary could not express, producing a vacuous
test and a dev harness that constructed the signature it then
"verified". Each of the six findings is quoted source-line evidence, not
an opinion, and each was checked against the frozen hash. The skeptic's
proposal (let the prereg add what is missing) is exactly what the
synthesis recommends for the NEXT program: construction-first additions
with architecture accounting. SUBSTRATE-ABSENT does not kill the
research question; it kills the net-negative deletion framing of each
question. The process fix worked: five preregs stopped before freezing
vacuous bars.

## 6. TNN-3 H5: KILLED (red-team dissent, KB-B2)

ADVOCATE: The dissent is evidence-cited, not rhetorical. The frozen bar
reads: "the query after the second contradiction must return the
twice-corrected value. TNN-2 silently no-oped and returned the
first-patched value." On the fact key (b,5202), the unmodified baseline
also returns the twice-corrected value (base ev_observe taught the new
fact; activate skips superseded tag-1 nodes), so the bar as
operationalized is non-discriminating. The 1421pdt M3-W2 probe, cited by
the adversary as justification, was on the MAP key: the event stream
ends `QUERY 43101 43509 43119` with K-S12 expecting 43119, and 1421pdt
reported "returned 43109, not 43119". Under the faithful MAP-key
reading, the committed sealed evidence shows the bridge queries
returning the stale ORIGINAL values (C1S=100, expected 300; C2S=900,
expected 623) via promote_graph's shadow fact. PREREG_H5.md section 10
is conjunctive: any single bar failing kills. KB-B2 fails under the
faithful reading; H5 is KILLED.

SKEPTIC: The dissent kills a genuine advance on a bar-reading dispute.
The R-family evidence is real: 8/8 guide CON edges, ev_act 30 to 0,
12/12 retention, wrong-key selectivity, the generic 4-line supersede
with net minus 22 cognition lines. The dissent itself says the MAP
supersession writes are genuine white-box evidence. Killing H5 over the
MAP-key operationalization when the builder honestly disclosed the
supplementary bridge queries (100/900) punishes transparency; the bar
could have been amended instead of the verdict killed.

JUDGE: UPHOLD the KILL. Three independent defects compound, each
evidence-cited: (1) the baseline sentence of the frozen bar describes
MAP-key behavior only, so the fact-key operationalization contradicts
the prereg's own text; (2) the adversary's stated justification is
factually false (1421pdt probed the MAP key, quoted above); (3) under
the faithful reading the committed sealed logs show staleness worse
than TNN-2's (original c0 vs once-patched c1). Amending the bar after
the result to save the verdict is exactly what the never-retroactively-
alter-a-kill-bar rule forbids; the honest path was taken, which is a
fresh prereg for H5R under VOID discipline. The R-family guide evidence
survives as genuine (the synthesis records it), but the wave verdict
under the conjunctive rule is KILLED. Dissent sustained as the verdict.

## 7. TNN-3 H5R: KILLED (KB-W2R 8/12)

ADVOCATE: The kill bar is KB-W2R, frozen at 12/12, measured 8/12. The 8
double-contradiction probes pass cleanly; all 4 revert probes fail the
DEP clause. Killing evidence (identical on C1R1, C1R2, C2R1, C2R2): the
live revert MAP (id=298, f28=63501=c0) carries DEP edges to node 254
(live chain fact) and node 255 (the SUPERSEDED original fact), while
the live reverted fact that actually licenses the c0 answer has no DEP
edge from the MAP. Root cause traced in the frozen trial loop:
first-verifying-candidate ordering promotes the candidate via the
lowest-node-id (dead) fact. This is a genuine causal flaw, not a
technicality: revise_on_contradict locates stale MAPs via DEP edges to
the contradicted fact, so a future contradiction of the live fact would
not supersede this MAP; the MAP would keep answering via the MAP read
path. The revision chain is broken for revert-promoted MAPs.

SKEPTIC: Is the DEP clause a technicality or a genuine flaw? All the
behavioral bars pass: KB-W0 36/36 (zero live tag-1 facts on any MAP key,
shadow fact gone), KB-B2R 16/16 (twice-corrected values via fresh MAPs),
KB-B3R 4/4 (revert returns c0), KB-W1R 8/8, KB-B1R 8/8, KB-R1R 12/12.
The DEP clause is a white-box bookkeeping requirement about which node
the provenance edge points to; the behavior is correct everywhere. The
kill elevates provenance tidiness over demonstrated revision and blocks
a substrate change that demonstrably corrected the original sin.

JUDGE: UPHOLD the KILL. The skeptic's framing ("provenance tidiness")
misstates what the DEP edge is for. The DEP edge is not bookkeeping; it
is the mechanism by which revise_on_contradict finds stale MAPs. A
revert MAP whose provenance anchors to a superseded fact is invisible
to future contradiction-driven revision on its live licensing fact,
which means the revision chain the hypothesis exists to provide is
broken exactly on the revert path the KB-B3R bar exercises. The bar was
designed to catch this; it caught it; the verdict follows the frozen
conjunctive rule. The kill is narrow and honest, and the record says so:
KB-W0 36/36 proves the original sin corrected, KB-B2R 16/16 and KB-B3R
4/4 prove genuine behavioral revision, the guide half passes fully. A
killed H5R returns via fresh prereg plus fresh sealed worlds; the
remediation target is named (first-verifying-candidate ordering in the
frozen trial loop), not a bar adjustment.

## 8. TNN-3 synthesis: complete

ADVOCATE: The synthesis draws the central finding from six independent
verification reports: the frozen TNN-2 core has no learner-reachable
construction, update, or standing-maintenance paths; every deletion
presupposed a learner affordance that verification showed was never in
the substrate. It names the dissolved program precisely (deleting
researcher code leaves zero construction, not learner construction) and
derives the positive implication (construction-first additions with
architecture accounting: learner-reachable construction primitive,
contradiction-to-construction trigger, learner-writable standing) while
keeping the guardrails binding (no modes/bridges/routers/handlers,
protected-ISA ruling, verification-first process fix, L3 evidence
standard). It answers the skeptic's treadmill attack directly.

SKEPTIC: The synthesis is a permission slip to add researcher code,
which is the treadmill wearing a lab coat. "Additions with architecture
accounting" is vague enough to admit anything; every future failure
will be met with a new affordance, and the one-system rule becomes a
rubber stamp. The net-negative program at least had a hard constraint
(delta <= 0); this replaces it with vibes.

JUDGE: UPHOLD as complete. The skeptic's attack is answered in the
document's own section 7, and the answer is falsifiable rather than
vibes: the proposed additions create affordances the learner must then
exercise itself, and the L3 criterion set discriminates treadmill
patches (structure in source) from genuine affordances (structure
created after experience, white-box trace, ablation, sealed
adversarial survival). If the primitive is built and sealed evaluation
finds the learner still authors nothing, the synthesis's prediction
fails and the addition is retired; the wave demonstrated the process can
kill (H1 dead, H5 dissented, five preregs stopped). The hard constraint
is not gone; it moved from "delta <= 0" to "positive delta recorded,
justified, and minimized, with fewer special mechanisms rewarded" plus
the standing question "Why can the existing general architecture not
learn this behavior?" The synthesis also correctly keeps H8-H11
suspended pending re-verification rather than killed. Complete.

## 9. CONTLEARN: INTEGRATION-DEMONSTRATED, red-team QUALIFY

ADVOCATE: All of K0 through K6 pass on the fixed 149-event script:
REUSE_COUNT 30/30 (R1C 6, R2C 3, R3C 3, R4C 12, R5C 6), per-phase-reset
controls scoring identically within phases and 0/18 on the cross-phase
probe, 3/3 byte-identical determinism across 21 runs, frozen ISA
boundary intact, zero cognition-source delta. The red team independently
reproduced the hashes, transcript counts (149 EV lines, 6 P4 events),
and determinism, and concurred the 149/150 erratum and empty-env
deviation are immaterial. The verdict honors the prereg's non-claims
(no L3, no generality).

SKEPTIC: Is it learner-owned? No. Attack 1 shows the learner's causal
contribution to every counted citation is zero: `t2_try_verify` accepts
iff the executed value equals `expected`, and the driver passes the
answer key on every QUERY (`EV 2 6001 202 5101 ans=5101`); promotion
writes MAP, DEP edges, and answer fact after the key-match decision;
revision fires on driver OBSERVE with no learner decision on the path.
K5a equality shows per-phase outcomes are history-insensitive: the
cross-phase citations are causally inert for behavior. R5c is fact
retention mislabeled "procedures reused": the serving node is a
machinery-taught answer fact read by activate; no promoted MAP is ever
executed at query time (H2-v2 K-H2-4(b) on the byte-identical source).
REUSE_COUNT 30/30 at ceiling with floors just below deterministic
maxima means the bars cannot fail short of implementation breakage: a
regression check, not an experiment. "INTEGRATION-DEMONSTRATED" will be
misread as a learner achievement.

JUDGE: UPHOLD the verdict as QUALIFIED, and adopt the red team's
qualified claim as the governing statement. The unqualified label is
misleading under the causal reading of "learner-owned": H2-v2 K-H2-3(a)
already proved on this byte-identical source that no learner-created
state influences any accept decision, and the red team's attack-1
evidence (answer key on every query, machinery-written citations) is
unrebutted. What stands, exactly: on the fixed disclosed 149-event
script, with the correct answer supplied on every query, the frozen
core's event-triggered machinery produces 30 structural cross-phase
citations in one persistent arena, with control parity and byte
determinism. Not shown: learner-owned integration in the causal sense,
procedure reuse (R5c is fact retention), unsupervised integration
(every accept matched a supplied answer key), or behavior-changing
integration (K5a equality). H10 must beat the qualified baseline, not
the nominal one: cross-phase integration where the learner does the
integrating, with the causal trace through learner-authored state. The
verdict is a machinery floor for H10, nothing more.

## 10. BATTERY v2: 9/9 VALIDATED

ADVOCATE: The amended M2-W2 fresh-state protocol executed cleanly: K-S9v2
amended FAIL with the predicted stale-guide signature (N=0, pre=30,
post=30), validity holds, all calibration gates hold, 3/3 determinism;
K-S8v2 FAIL unchanged; K-S10v2 FAIL with N carried from the fresh-state
baseline (EPISODE_ACTIONS 30 30 30, distinct=0). The v1 M2 kills stand
corroborated through a calibrated bar. 8/9 worlds validated in the v2
run plus the amended M2-W2 protocol makes 9/9 validated (expected
outcome achieved). No battery-defect void; unexpected-PASS rule not
triggered.

SKEPTIC: The "validation" is of a battery that mostly fails by design:
the headline results are three FAILs. Calling 9/9 "validated" invites
reading it as 9/9 passed, which is the opposite of what happened. And
the M2-W2 amendment fixed a WORLD-INVALID design defect, which is a
prereg repair, the kind of amend-and-promote the rules frown on.

JUDGE: UPHOLD. "Validated" here is a term of art with a precise meaning
in the lane record: each world's measured outcome matches its
preregistered expected outcome, where the expected outcome for M2 was
FAIL (the v1 kill). A battery that corroborates its kills is doing its
job; the v2 validation recorded 8/9 validated with M2-W2 WORLD-INVALID
as a prereg design defect, and the amended re-run supplied the missing
ninth under a fresh-state protocol, with the failure matching the
amendment's predicted signature exactly (N=0, pre=30, post=30 stale).
That is corroboration, not laundering. The record is unambiguous that
the outcomes are FAILs; no honest reader can mistake "9/9 validated"
for "9/9 passed" given the run log states the fails explicitly. The
v1 M2 kills stand corroborated.

## 11. ARENA TCNP: BUILD-PASS (K1-K9)

ADVOCATE: All nine frozen bars pass: K1 24/24 construction within the
8-op ISA with consensus abstention; K2 0 confident wrong on the honesty
probe; K3 rebind with trials=0 and D 6/6; K4 54/68 byte-identical to the
v6 baseline (no regression); K5 0/24 contamination markers; K6 3/3
byte-identical determinism; K7 0/24, 0/24 memorization controls; K8 pure
Zag (zero Python); K9 585 added lines, 0 new modes/bridges/routers/
handlers/semantic cases. The procedural gap the red team found (K5(e)
never run) is now closed: the frozen binary scored 6/6 on fresh world F
(new rule COPY(1,3), ROTR, SWAP(0,1), DEC(0); fresh seed 20261001; binary
hash 71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b
matching the sealed record; full enumeration L=3, tried=37059, 6 minimal
fitters agreeing on all 6 hidden probes).

SKEPTIC: Does 6/6 on one fresh world establish generality? The red team
itself notes that for any fresh in-bound rule the mechanism passes by
completeness of exhaustive search, so K5(e) guards against
battery-specific contamination, not capability; it is a governance
requirement, not a generality demonstration. And the C10/C16 identity:
the sealed battery's C10 items are operationally identical to the C16
zemprod morphology items, so the whole lane's motivation (procedure
evidence in the arena) rests on an artifact. K2's "honesty" is a
researcher-installed length cap (E mode=none after tried=1222980);
K3's "transfer" is exact rebind, the weakest form. This is DSL search
over a 33-variant vocabulary wearing a procedure-invention costume.

JUDGE: UPHOLD BUILD-PASS, with the red team's interpretation bounds
adopted as part of the verdict. On generality: K5(e) 6/6 satisfies the
frozen bar (>= 4/6) and closes the procedural gap, but it establishes
only what the bar asked; per the red team's own note, it does not
discriminate capability beyond contamination-guarding. On C10/C16: the
identity is confirmed, but Attack 5 shows it has no effect on this
verdict: TCNP was evaluated on a separate sealed battery (cap 99,
pshow/ptest, vector-transformation worlds A-E); the C10/C16 items do not
occur in it; K4 is a non-disturbance check that passed exactly as
specified (54/68 byte-identical). The identity threatens the v6
baseline's procedure-evidence claims, not the TCNP verdict. On K2/K3:
the charges are sustained as interpretation bounds, not bar failures:
K2 honesty reads narrowly as deterministic abstention on search failure
(the unprobed case (iii), short-fitter-agrees-but-wrong, stands as a
named gap); K3 transfer is exact rebind, not adaptation. The result is
capped at candidate status: exhaustive search within the frozen ISA,
consensus abstention, white-box traces, with the prereg's L3 disclaimer
load-bearing. BUILD-PASS on all nine bars as frozen, so bounded.

## 12. DEVANG3: BUILD-FAIL (K_SEG 8/12, K_SEAL 11/20)

ADVOCATE: The verdict is an honest measurement, not a design kill.
K_AUD passes on all three prereg claims (every statistics table derives
from segmenter output only, quoted code), so the segmentation-dependence
design requirement holds. What fails is segmenter quality: K_SEG 8/12
(< 9/12) on the sealed ambiguity cases and K_SEAL 11/20 (< 12/20) on the
post-freeze adversarial family, with K_C0 failing on the sealed-family
reading (0pp margin; the learner ties the raw-byte architecture at
11/20). The design is sound; the component is insufficient.

SKEPTIC: BUILD-FAIL is BUILD-FAIL. "Design holds but quality
insufficient" splits a hair the prereg does not: the prereg's bars are
frozen, the segmenter missed them, and dressing the fail as a
"mechanism result, not an architectural-recurrence result" softens a
straight kill. If the design were good, the bars would pass.

JUDGE: UPHOLD BUILD-FAIL as stated, including the mechanism-vs-design
distinction, because the distinction is evidence-backed, not softening.
K_AUD's code inspection (lexicon counts, grounding writes all deriving
from segs[]) proves the dependence requirement the prereg actually
froze as a design claim; K_SEG and K_SEAL measure component quality on
sealed adversarial cases. Conflating the two would misdirect the repair:
the fix is a better segmenter, not a different architecture. The
verdict correctly names the killing bars (K_SEG first) and the
0pp-margin K_C0 sealed reading as a secondary finding. BUILD-FAIL
stands; the design may be reused.

## 13. F1: BUILD-FAIL (K-C0C TRIP; K1 trigger never fires on interleaved errors)

ADVOCATE: The killing bar is K-C0C on W1: 15/30 = 50% < 80%. The
mechanism diagnosis is precise: the K1=2 consecutive-failure trigger
never fired on interleaved errors, so the constructor never attempted
learning on the EQ-discovery world (0 CONSTRUCT events on W1). A
non-sealed diagnostic (reordered W1 train, same frozen binary) confirms
EQ discovery works when errors are consecutive, isolating the defect to
the trigger. Secondary findings are also crisp: W4 is a near-variant
(final ops [4 2] isomorphic to the training family), and a single-node
brute-force oracle matches the learner 30/30 on W4. Passing bars are
genuine: K-C0A (zero forbidden semantic names, grep-quoted), K-C0B
(menu attack defeated), K-C0C on W2/W3, K-C0D all five sub-bars,
K-REV (R1 30/30 via the learner's own continued construction).

SKEPTIC: Is the trigger diagnosis right, or is it the adversary's
post-hoc story? The reordered-W1 diagnostic was non-sealed, built by the
same adversary after seeing the failure; it confirms the binary can
learn EQ under a sorted curriculum, which proves little about the sealed
defect. Maybe the W1 world itself is miscalibrated (interleaved errors
as the only discovery world punishes any threshold trigger). And the
adversary's "prescribed remedy" (redesign W4, fresh prereg for the
trigger) keeps the builder on a treadmill of re-registration.

JUDGE: UPHOLD BUILD-FAIL with the trigger diagnosis. The skeptic's
calibration worry is real but does not overturn the verdict: the frozen
bar (K-C0C >= 80% on W1) failed at 15/30, and K-TRACE (0 construction
events) and K-ABL (0pp drop vs control) corroborate that nothing was
learned, not that the world was unfair. The reordered-W1 diagnostic is
explicitly labeled non-sealed and diagnostic, not verdict evidence; it
isolates the trigger as the defect locus, which the sealed evidence
already implies (TRIGGER never fired in the train trace). The adversary
is correct that tuning K1 post hoc against the sealed families would
void the evaluation per prereg section 7; the remedy is a fresh
preregistration with a redesigned trigger, not a patch. A learner that
only builds when failures arrive in consecutive pairs cannot learn from
interleaved experience, the normal case outside sorted curricula. The
diagnosis stands; the bars that passed (K-REV especially: revision
through the learner's own continued construction, R1 30/30) are real and
preserved in the record.

## 14. F2v3: BUILD-FAIL (K4-R4 convergence; nalive=2)

ADVOCATE: The sealed 3/3 runs terminate by exhaustion with nalive=2
(SURVIVORS [80,82]); D2 certificates are logged for the indistinguishable
pair; w_verify confirms the true Y1/Y2 rules are the shared ones but the
exactly-one-survivor clause fails. The final pair needs depth-9, and
D2=8 is provably insufficient: a calibration fact, not an excuse. What
DPDS did achieve is honest and bounded-effective: K4-R1 PASS (NHYP 216),
K4-R2 PASS (adversary source audit: the distinguishing sequences appear
nowhere in f2v3_learner.zag; experiments from iterative-deepening
enumeration), K4-R3 PASS (zero world calls in search; complete
discrimination ledger), GOAL_REAL_C2 1 on a fresh sealed world with
random 0/20 and NC2 0/1. The verdict names exactly what failed and what
survived.

SKEPTIC: The depth-9-vs-D2=8 finding is suspiciously convenient: the
bound the builder froze is exactly one short of what the sealed world
needed. Either the prereg was calibrated against knowledge of the
world (seal leak) or the bar was set to fail gracefully. And
"bounded-effective" is another softening label for a kill.

JUDGE: UPHOLD BUILD-FAIL. The skeptic's seal-leak suspicion is
testable and was tested: K4-R2's adversary source audit confirmed the
distinguishing sequences appear nowhere in the learner source, and the
sealed world was designed post-freeze with the builder having no read
path. D2=8 was the frozen certificate bound from the prereg, not a
post-hoc excuse; "provably insufficient" is a mathematical fact about
the final pair, recorded with the D2 certificates. The exactly-one-
survivor clause is the frozen bar; it failed at nalive=2. "Bounded-
effective" describes the measured scope of what passed (4 of 6
variants resolved with a complete elimination trail, sustained
dual-contextual goal achieved on a fresh world), which the evidence
supports and which correctly scopes the next hypothesis (deeper
certificates or a different convergence rule). No softening: the kill
bar is named, the number is exact.

## 15. SENSORY H1v2: BUILD-FAIL (KB3, KB9)

ADVOCATE: Two frozen bars failed with measured margins: KB3 light logic
(diff +0.72 vs >= 6.0; sun mean +0.64 vs >= 3.0) and KB9 cost (2.36x vs
<= 2.0x on sequential pairing 1). KB11=0: no artifacts. The candidate is
honestly reported as not judge-ready: no blind pair prepared, no
JUDGE_BRIEF.md, no SEALED_MAPPING. The red-team investigation found no
dropout, flicker, banding, or weirdness; KB10 confirms the
implementation matches the frozen design to ~1e-6. The failure is
attributed: KB3 is a mechanism-knowledge finding (right anchoring,
insufficient systematic half-level effect); KB9 pairing-1 is a
measurement-environment finding (contention outlier) compounded by a
real cost increase (+26 fbm octave-evals per sky pixel that the prereg
prediction missed). No substrate defect.

SKEPTIC: KB9's failure is partly a measurement-environment artifact
(contention outlier), so failing the candidate on it punishes the
builder for the lab's noise. And "provenance honesty: NEW candidate
under NEW prereg" is a fig leaf: the H1v2 mechanism is a rework of a
failed H1, and the bar (diff >= 6.0) was set an order of magnitude
above the measured effect (+0.72), suggesting the bar was aspirational,
not calibrated.

JUDGE: UPHOLD BUILD-FAIL. On KB9: the pairing-2 measurement (1.29x)
passed, but the frozen bar requires the sequential pairing per the
prereg's matched-contention design; moreover the investigation found a
real +26 fbm octave-evals per sky pixel that the prereg prediction
missed, so the cost increase is not pure noise. The bar stands as
frozen. On calibration: KB3's bar (diff >= 6.0, sun mean >= 3.0) was
frozen before the renders existed; the measured +0.72 misses by nearly
an order of magnitude, which is a genuine mechanism shortfall (the
anchoring is right but the systematic effect is weak), not a near miss
worth re-measuring. The verdict's honesty provisions (not judge-ready,
provenance statement, artifact-free KB11=0) are exactly what the
judgment rule requires: the candidate returns via a fresh prereg, not
via bar adjustment. BUILD-FAIL stands.

## 16. FORK battery: tip PASS, 54 RE-CERT PASS, 2 UNTESTABLE, 0 FAIL

ADVOCATE: 58 refs enumerated against the recorded SHA set with the
frozen instrument (driver, harness, fixtures, and all pins byte-verified
before use). One fresh extraction run on commit
94767525856b09fa0d93569df941d0c5fd8c5bf3 (the tnn-native-lab tip and the
new archive-wave-20261001-1721pdt tip): full frozen battery PASS,
neg1/neg2 discriminate, probe R32_ZNC_PROBE_OK. 54 refs RE-CERT PASS by
SHA match. 2 refs (rh-pull-1-head, rh-pull-2-head) RE-CERT UNTESTABLE
with the recorded standing cause (pinned toolchain path absent in
tree), unchanged from prior waves. Archive immutability 46/46 for the
pre-existing set. Zero FAIL. Zero Python.

SKEPTIC: RE-CERT by SHA match is not testing; 54 of 58 "passes" are
bookkeeping. The two UNTESTABLE refs have been untestable for waves on
end with the same standing cause, which is a euphemism for never
investigated. And the fresh PASS covers a tip that moved only because
the wave archived itself.

JUDGE: UPHOLD. The fork battery is a hygiene certification, and it says
so on its face ("Hygiene certification only, not content review").
RE-CERT by SHA match against a previously executed result is the correct
procedure: re-running identical bytes proves nothing new, and the one
ref whose bytes changed (the tip) plus the one new ref were fresh-tested
with the frozen instrument. The two UNTESTABLE refs carry a recorded,
specific cause (pinned toolchain path absent in tree, git show exit
nonzero at extraction), reported every wave, not silently skipped; the
cause is structural to those foreign refs, not an investigation the
battery is chartered to perform. Zero FAIL, archive immutability intact.
Verdict stands as recorded.

## Summary table

| # | Verdict | Advocate position | Skeptic position | Judge ruling |
|---|---------|-------------------|------------------|--------------|
| 1 | H-PI-REV2 step-5: PASS (8/8) | Amended prereg frozen first; 3/3 byte-identical; original BASELINE-FAIL preserved | Amendment launders a fail; bars re-specified to pass | UPHOLD |
| 2 | H-PI-REV2 step-6: S6C PASS under K-AX2 (13/13) | b4b_enumerated=88728 exactly as pre-committed; kill tripwire live | Bar fitted to the result; straw tripwire | UPHOLD |
| 3 | H-PI-REV2 step-7: FAIL with bounding (family B only) | Frozen bounding matrix; red-team certified honest B fail; A/C/D 5/5 | "Bounding" softens a kill | UPHOLD |
| 4 | TNN-3 H1: DEAD | Zero names; code-level certainty (no 904/NAME in binary); harness-defined signature | "Fabrication" overlabels builder error | UPHOLD (presentation-level fabrication; intent not established) |
| 5 | TNN-3 H2/H3/H4/H6/H7/H10: SUBSTRATE-ABSENT | Quoted source-line verification x6; H1's lesson applied | Verification gate strangles hypotheses; no sealed runs | UPHOLD |
| 6 | TNN-3 H5: KILLED | Dissent evidence-cited x3: unfaithful KB-B2, false 1421pdt premise, non-discriminating bar; conjunctive rule | Kills a genuine advance on a bar-reading dispute | UPHOLD (dissent sustained) |
| 7 | TNN-3 H5R: KILLED | KB-W2R 8/12; DEP flaw is causal (revision chain broken for revert MAPs), not bookkeeping | DEP clause is a technicality; behavior all passes | UPHOLD |
| 8 | TNN-3 synthesis: complete | Six verifications converge; additions falsifiable via L3 bars; guardrails binding | Permission slip for researcher-code treadmill | UPHOLD |
| 9 | CONTLEARN: INTEGRATION-DEMONSTRATED | K0-K6 pass; 30/30; 3/3 deterministic; controls parity | Learner causal contribution zero; answer keys on every query; R5c mislabeled | UPHOLD as QUALIFIED (machinery floor for H10, not learner-owned in the causal sense) |
| 10 | BATTERY v2: 9/9 VALIDATED | Amended M2-W2 protocol; fails match predicted signatures; v1 kills corroborated | "Validated" misread as "passed"; amendment is bar repair | UPHOLD |
| 11 | ARENA TCNP: BUILD-PASS | K1-K9 pass; K5(e) 6/6 closes the gap; C10/C16 identity has no effect on the separate TCNP battery | 6/6 on one world is not generality; K2/K3 are narrow; DSL-search costume | UPHOLD with interpretation bounds (K2/K3/K4 narrowed; candidate status; L3 disclaimer load-bearing) |
| 12 | DEVANG3: BUILD-FAIL | K_AUD design proof passes; quality shortfall (8/12, 11/20) honestly measured | "Design holds" softens a straight kill | UPHOLD |
| 13 | F1: BUILD-FAIL | Trigger defect isolated (TRIGGER never fired; reordered-W1 diagnostic); K-REV 30/30 preserved | Diagnosis is post-hoc; world may be miscalibrated | UPHOLD with the trigger diagnosis |
| 14 | F2v3: BUILD-FAIL | nalive=2 exact; depth-9 vs D2=8 provably insufficient; seal held (K4-R2 audit) | Convenient calibration; "bounded-effective" softening | UPHOLD |
| 15 | SENSORY H1v2: BUILD-FAIL | KB3 +0.72 vs 6.0 and KB9 2.36x vs 2.0x measured; KB11=0 artifact-free; not judge-ready | KB9 partly environmental; bars aspirational | UPHOLD |
| 16 | FORK: tip PASS, 54 RE-CERT PASS, 2 UNTESTABLE, 0 FAIL | Frozen instrument; changed bytes fresh-tested; UNTESTABLE cause recorded | RE-CERT is bookkeeping; UNTESTABLE never investigated | UPHOLD |

## Overturns

None. All 16 verdicts are UPHELD. The debate's hardest fights (H5 kill,
H5R kill, H1 fabrication label, CONTLEARN qualification, ARENA
generality) were resolved on cited evidence, and in each case the judge
adopted the narrower, better-evidenced reading: the H5 dissent becomes
the verdict, the H1 fabrication stays presentation-level with intent
explicitly not established, CONTLEARN is governed by the red team's
qualified claim, and ARENA BUILD-PASS carries its interpretation bounds.
No coordinator verdict was overturned on rhetoric; none needed
overturning on evidence either.
