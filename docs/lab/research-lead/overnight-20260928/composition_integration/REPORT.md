# REPORT: Composition Integration (H-COMPINTEG-1)

Verdict: COMPOSITION-INTEGRATION-COMPLETE (with integration
breakdown analysis, sections 5-6).
Date: 2026-10-02. Worker: Composition Integration Worker (subagent).
Prereg: PREREG.md (05d1b7a28) frozen and committed alone before
implementation. Amendments 1, 2, 3 each frozen and committed
before the redesigned implementation was run. Probe runs that
motivated the amendments were implementation tests, never verdict
runs. (An earlier probe-phase draft of this report existed; it is
superseded by the amended battery below.)

## 1. Question

C278 (EXTEND/TRUNCATE/SPECIALIZE), C279 (REBIND), C280
(learner-owned verification), C289 (learner self-wiring), and
C290/C291 (policy construction/revision/transfer) were validated
as separate pieces. Do they work TOGETHER in one learner? Where
does the integration break?

## 2. What was built

integ_patch.zag (157 cognition lines): compose_integ, the single
integrated learner operation taking NO researcher expected answer.
Flow: lv_setup prediction gate (C280; withholds at -3 when the
learner has no reliable prediction, and the L2 bracket never fires
on withhold) -> native learner-terminated DFS -> kind-dispatched
revision (adapt_revise2) else fresh EXTEND/TRUNCATE/SPECIALIZE ->
learner-terminated DFS over the augmented set -> execution
verification against the LEARNER prediction -> promotion with
learner-written self-wiring (LINK14 provenance, type-15 co-use,
type-16 adapted-from). Plus integ_explore, the ungated
experience-gathering counterpart (adapt, execute through live world
facts, observe with lv_observe, never promote). Plus
integ_tag_extend (kind-completion, section 5.4).

Build: cc_base + un_patch + adapt_patch + revise_patch + ts_patch
+ lvcomp_patch + integ_patch + integ_driver, compiled with the
pinned znc. All frozen sources sha256-verified against origins.

## 3. Results (3/3 byte-identical; sha256
8e73222767a21f5a89e5d35b13a7730e261ee47aabd281e5dacf2784f05797f1)

| arm | result |
|-----|--------|
| I1 extend+verify+wire | PASS: ans=108; adapted a=[70,70,70,2] type-16->MAP_X kind 1; MAP_Z LINK14->a; 2 live adapted MAPs; prediction 108 rel 3 |
| I2 truncate+verify+wire | PASS: ans=13; t=[70,70] type-16->MAP_X kind 2; MAP_Z LINK14->t |
| I6 specialize+verify+wire | PASS: ans=99; xs=[70,2] type-16->MAP_X kind 3; MAP_Z LINK14->xs |
| I4 withhold gates adaptation | PASS: ans=-3; zero type-16 edges; 1 live MAP; bracket never fired |
| I3 stale revise under verification | PASS: q1=108; world change; q2=-2; a retired; a2=[70,70,70,2] type-16->a; no LINK14->a2; stale FACT score still 3 |
| I5 recovery (diagnostic) | PASS: prediction flipped 108->140 in 4 explore cycles; q3=140; MAP_Z2 LINK14->a2 |

Kill bars: K1-K5 (arms) PASS; K6 (3/3 byte-identical) PASS;
K7 (zero em/en dashes byte-verified; `expected` absent from
integ_patch.zag; 0 modes/bridges/handlers) PASS; K8 (frozen
sha256) PASS. I5 reported as preregistered diagnostic, not gating.

Raw I3 revision trace:
REVISE2-STALE a=160 src=27 kind=1
REVISE-MK id=208 src=27 revises=160 len=4
INTEG-COMP-FAIL / I3-Q2=-2

I5 convergence trace: cycle1 pred=108 rel=0; cycle2 pred=140
rel=0; cycle3 pred=140 rel=2; cycle4 pred=140 rel=4; I5-Q3=140;
p1(conv10)=1 p2(q3140)=1 p3(z214a2)=1.

## 4. What the numbers establish

a) The three L2 operators compose with learner-owned verification
in one pipeline. In I1/I2/I6 the learner's own prediction (built
purely from its adapted executions, never handed by the harness)
gates adaptation, terminates the DFS, verifies the assembled
chain, and the learner wires the result to its own knowledge
(LINK14/type-16). No researcher answer is consulted anywhere in
the integrated path (grep audit).

b) Verification gates action. I4 shows the learner withholds (-3)
and creates zero structure when it has no reliable prediction.
Adaptation is not a reflex; it is a learner action taken under
a reliability threshold.

c) Structure revision works; prediction revision does not keep up.
I3 is the sharpest result: after the world change, adapt_revise2
correctly detects the stale adaptation, kind-dispatches (kind 1),
rebuilds a2=[70,70,70,2] via the new frontier fact with proper
revision provenance (type-16 a2->a), and retires a. But the
learner's prediction (108, rel 3) is stale, so the correctly
revised structure is REJECTED (q2=-2, nothing promoted). The
pipeline revises structure but has no prediction-revision path on
query failure. I5 shows the loop closes with 4 more explore
cycles (C181 supersession/score dynamics flip the prediction to
140), and then the revised structure is accepted and wired
(q3=140, MAP_Z2 LINK14->a2).

## 5. Integration breakdown analysis

This is the parent's core question. Five breaks/gaps, ordered by
severity. All were observed empirically, not theorized.

### 5.1 REBIND cannot join the integrated learner (architectural gap)

rebind_try's signature takes a researcher expected answer, and no
learner-verified rebind variant exists. It was excluded from
compose_integ by preregistered design. Consequence: an L2 operator
whose verification path is researcher-supervised cannot
participate in a learner-verified learner. A learner-verified
rebind (termination by learner prediction rather than expected)
is the missing piece; until it exists, cross-domain rebinding and
learner-owned verification are mutually exclusive in one
pipeline.

### 5.2 Stale predictions veto correct revisions (I3; the main break)

Even with all pieces working, structure-revision and
prediction-revision are not closed-loop. The learner rebuilt the
right structure (a2) and wired it correctly, then rejected it
because its own prediction was stale. The C280 machinery scores
predictions only on observation (lv_observe); compose_integ never
observes on failure, so a wrong prediction persists at rel 3
indefinitely while the world moves on. I5 proves recovery is
possible but costs fresh explore cycles; there is no
counterexample-driven prediction update inside the query path.
For a continuing learner this is the critical gap: every world
change pays full re-exploration cost for the prediction even when
the structural revision was already correct.

### 5.3 Prediction FACTs pollute adaptation operators (probe finding)

C280 stores predictions as FACTs in the shared fact store; C278's
adapt_specialize scans that store for alternative relations. The
first probe showed the interaction is real and dangerous: the
explore FACT (101,70,105) was picked up as a world alternative,
creating a 1-link self-referential [70] MAP (101->105 via the
learner's own FACT). In the stale regime this MAP stayed intact
after the world change and natively re-verified the stale
prediction: a degenerate self-fulfilling loop that immunizes the
learner against world changes. The battery designs around it by
construction (training X with the query relation, so prediction
FACTs carry r=R[j] and are skipped by the r_alt != R[j] scan;
Amendment 1), but the hazard is architectural: the substrate does
not distinguish world facts from learner predictions, so any
future operator scanning the fact store can bootstrap predictions
into self-verifying structures.

### 5.4 Latent kind-dispatch fault in ts_patch (found, contained)

adapt_extend predates Amendment 1 kind-recording, so its MAPs
carry field 12 = -1. ts_kind's relseq inference fails on stale
(unreadable) relseqs and falls through to kind 3, misdispatching
stale EXTEND adaptations to the specialize re-runner (which finds
nothing, retires the MAP, and leaves recovery to the fresh
fallback, losing revision provenance). integ_tag_extend completes
the kind convention in the integration layer (new code, frozen
files untouched). The frozen ts_patch fault remains for any
caller that does not tag.

### 5.5 Contract fallback reanimates stale composites (probe finding)

In the first I5 probe, Q3's native DFS selected the stale Q1
composite MAP_Z over the revised a2: un_satisfy's contract
fallback rebuilt a live path (101,102,103,104,140) through the
dead-licensed structure and terminated at the (by then correct)
prediction. The answer was right but the wiring bypassed the
revision. I5 retires the stale composite by harness isolation
(Amendment 3) to test the revision path; the fallback behavior
is legitimate learner machinery (mechanism A), but it means stale
composites are never truly dead while their contract shape
matches live facts. A continuing learner needs a staleness story
for composites, not just for adaptations.

## 6. Honest limitations

- Single-segment compositions only; the type-15 co-use promotion
  path is present but no arm exercises 2+ segments.
- The two probe-driven redesigns (Amendments 1-3) are disclosed
  in full; the original I1/I3 hand-derivations were factually
  wrong (EXTEND-ONE is single-link), not just unlucky.
- I6's explore creates a benign 1-link [74] MAP from the
  prediction FACT (shorter than [70,2], never selected); the
  5.3 hazard is contained, not eliminated.
- Toy scale; frozen bars, not a generality or SURVIVES claim.
- I5's exact convergence tick (4 cycles) depends on bid
  tie-break internals; the bound (<=10) is what was preregistered.
- The pre-amendment probe-phase draft of this report (verdict
  INCOMPLETE) is superseded; its break findings are folded into
  sections 5.3-5.5 above.

## 7. Architecture accounting

- New modes: 0. New bridges: 0. New handlers: 0. New opcodes: 0.
  New MAP/edge types: 0 (14/15/16 reused).
- New code: integ_patch.zag (157 cognition lines) +
  integ_driver.zag (335 lines, harness). Frozen files unmodified.
- Researcher scaffold (disclosed): pipeline order, withhold
  gate, kind-completion tagging, explore/exploit split, the
  Amendment 1 relation-algebra visibility design, harness
  isolation in I5/I6. Learner-owned: predictions, reliability
  values, which adaptations are created, verification outcomes,
  all wiring endpoints.
- The integrated learner adds no cognitive subsystem: it
  orchestrates existing operators under learner-owned
  verification. Capability-source delta is the pipeline itself.

## 8. Toolchain and determinism

- Safebin guard (NAMECHECK.md Step 0): PASS. No python3/python
  under worker PATH at any point. Pinned znc used.
- Pure Zag, zero RNG. 3/3 byte-identical stdout (sha256 above,
  pairwise cmp). Output via emit/e64; no _zag_print.
- stdout bytes verified against preregistered predictions before
  any claim was trusted.

## 9. Deliverables

Under docs/lab/research-lead/overnight-20260928/
composition_integration/: PREREG.md, PREREG_AMENDMENT1/2/3.md,
NAMECHECK.md, integ_patch.zag, integ_driver.zag, build.sh,
frozen copies (cc_base, un_patch, adapt_patch, revise_patch,
ts_patch, lvcomp_patch with sha256s in NAMECHECK),
integ_full.zag, integ_bin, integ_run1/2/3.txt, sha256sums.txt,
REPORT.md (this file). Committed locally with explicit pathspecs.
Nothing pushed. Paper untouched.

## 10. Recommended follow-up

1. Learner-verified rebind: the 5.1 gap is the largest
   architectural hole. Build rebind_try_lv (prediction
   termination, no expected) and test whether cross-domain
   rebinding joins the integrated pipeline.
2. Prediction revision on query failure: close the 5.2 loop.
   After a -2 with a stale prediction, the learner should
   counterexample-update its prediction from the failed
   verification, not just from fresh explore cycles.
3. Fact-store provenance: address 5.3 at the substrate level.
   Mark learner prediction FACTs (or their teach path) so
   adaptation operators can distinguish world facts from
   learner-internal records.
4. Composite staleness: extend the revision machinery to
   composites (5.5), not just for type-16 adaptations.
5. Multi-segment integration arm: exercise type-15 co-use
   wiring in the integrated pipeline.
