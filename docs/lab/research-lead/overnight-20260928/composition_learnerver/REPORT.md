# REPORT: Learner-Owned Verification for Composition (H-COMPVER-1)

**Verdict: COMPOSITION-LEARNERVER-COMPLETE.**
Wrong-expected test: treatment PASS (107) while the wrong-target control
FAILs (-2). Verification is genuinely learner-owned.

## 1. Question

The composition-compare battery (C208) found T5 FAILED for all three
composition mechanisms: all use researcher-supplied expected answers for
verification and DFS termination. The unified mechanism (C224) inherits
this. Meanwhile C181 proved learner reliability can replace researcher
`expected` for revision acceptance, with honest withholding when evidence
is absent. H-COMPVER-1: use C181-style learner verification as the
composition verifier instead of expected answers.

## 2. Mechanism (unfrozen variant only)

Base: lvcomp_base.zag = composition_C/cc_base.zag +
composition_unified/un_patch.zag, verified byte-identical (cmp) to the
first 2097 lines of composition_unified/un_full.zag. Frozen sources were
copied, never edited.

New patch: lvcomp_patch.zag (320 lines):

1. Prediction machinery ported from C181 (learner_verification/lv_base.zag),
   lv_ prefixed: PRED node recording (tag 31), lv_predict (FACT pred_score
   basis, then MAP-execute basis for the query relation; -999999 if no
   basis), lv_pred_resolve (+1/-1 on the source structure),
   lv_observe (ev_observe with prediction resolution appended).
2. lv_setup: learner prediction into hg(W,32), reliability into hg(W,36);
   -999999 if the learner has no basis. Adapted from C181.
3. lv_dfs: un_dfs with the researcher-answer termination replaced by
   learner-prediction termination (a candidate chain is complete when its
   end value equals the learner prediction). No researcher target parameter.
4. lv_verify_chain: executes the assembled composition; accepts iff output
   equals hg(W,32) (the learner prediction). Execute failure is genuine
   rejection.
5. compose_lv(W,s,r,masked,st): the learner-verified composition operation.
   Takes NO researcher answer parameter at all. Flow: lv_setup; WITHHOLD
   (-3) before any search if no prediction basis or reliability below
   threshold; else lv_dfs, assemble segment chains, seq_link,
   lv_verify_chain; on accept promote MAP_Z with LINK14 provenance to each
   segment MAP and type-15 co-use edges between consecutive segments (same
   promotion block as unified compose_try). Returns ans (>=0), -2
   (rejected/failed after search), -3 (withheld).

Honest boundary, researcher scaffold vs learner-owned:
- Researcher-authored: PRED layout, +1/-1 rule, threshold value 3,
  accept/reject/withhold structure, header fields 32/36, the evidence
  phase protocol (world reveals outcome 107 via lv_observe, C181 V4
  precedent).
- Learner-owned: all reliability VALUES (from prediction experience only),
  which predictors are trusted, the prediction used for termination and
  verification, whether composition succeeds.
- The verifier never sees a researcher target. grep audit: the token
  `expected` occurs 0 times in lvcomp_patch.zag. compose_lv and lv_dfs
  have no such parameter to consult, smuggle, or shadow.

Harness note: compose_lv and the control compose_try are called DIRECTLY,
not through ev_query. After the evidence phase the (101,70,107) FACT would
be activate-shortcut inside ev_query and bypass composition entirely; the
composition operation is the unit under test. Documented, not hidden.

## 3. Battery and results (3/3 byte-identical)

SHA-256 of each run: `b2ea4bf5c923d5c1033e959b849ea29a5b955ef52f0d268472faff6c48926361`
(runs 1, 2, 3 identical).

### 3.1 T1-LV: learner-verified composition on the 3-structure world -- PASS

T1 world (X+Y+W plen-2, rels 1/2/3; co-use episodes; gap; Z facts
101..107) + evidence phase: 5 predict/observe cycles for (101,70), true
world outcome 107. Cycle 0: pred=-999999 (no basis yet, honest); cycles
1-4: pred=107; FACT pred_score reaches 4 (>= threshold 3).

| metric | value |
|---|---|
| ans | 107 |
| segments | 3 (MAPs 13, 26, 39) |
| live MAPs | 7 -> 8 (MAP_Z promoted) |
| LINK14 out of MAP_Z | 3 |
| type-15 co-use edges | 2 -> 4 |
| tried / rejected | 1 / 0 |
| result | PASS |

K1 satisfied: ans=107, MAP+1, LINK14=3, new type-15 >= 2.

### 3.2 T-NE: no evidence -> honest withhold -- PASS

T1 world, no evidence phase. compose_lv(W,101,70):

| metric | value |
|---|---|
| ans | -3 (WITHHELD, `LV-WITHHOLD nobasis`) |
| tried / rejected | 0 / 0 (no search attempted) |
| live MAPs | 7 -> 7 (nothing promoted) |
| result | PASS |

K2 satisfied. The learner does not hallucinate a composition when it has
no evidence for the composed result. This is the C181 withholding behavior,
now demonstrated for composition. Direct answer to the task's T1 question:
on the stock T1 protocol (no (101,70) experience) learner-verified
composition withholds; with world experience it succeeds (3.1).

### 3.3 T-WE: wrong researcher target -- PASS (the critical test)

T1 world + evidence phase on fresh workspaces per arm.

| arm | call | ans | result |
|---|---|---|---|
| treatment | compose_lv(W,101,70), no target taken | 107 | PASS |
| control-wrong | compose_try(W,101,70,999,...) | -2 (COMP-FAIL) | FAIL as expected |
| control-right | compose_try(W,101,70,107,...) | 107 | PASS (sanity) |

K3 satisfied. The treatment succeeds where the wrong-target control fails:
the researcher's stated target (999) is dead wrong, yet composition
succeeds because the learner's own evidence supports the true result
(107). The control-right arm confirms expected-supervision works when the
researcher is right, isolating the difference to the verification
criterion. This proves the verification is genuinely learner-owned.

## 4. Kill bar scorecard

- K1 (T1-LV PASS with promotion metrics): PASS.
- K2 (T-NE withhold -3, tried=0, no promotion): PASS.
- K3 (T-WE treatment PASS + control-wrong FAIL + control-right PASS): PASS.
- K4 (3/3 byte-identical, SHA-256 recorded): PASS.
- K5 (0 modes/bridges/handlers/semantic cases; no researcher-target token
  in lvcomp_patch.zag): PASS (grep audits recorded; only declaration
  comments mention the words).
- K6 (cognition lines recorded): 320 lines lvcomp_patch.zag.

All bars pass: COMPOSITION-LEARNERVER-COMPLETE.

## 5. What this establishes

1. C181-style learner verification ports to composition: the composed
   structure is verified by executing it and checking the result against
   the learner's own prediction, gated by earned reliability. No
   researcher target is consulted at any point (not in DFS termination,
   not in final verification; the function signatures make consultation
   impossible).
2. Honest withholding transfers: with no evidence the operation declines
   before searching (tried=0), rather than guessing. This directly answers
   the C208 T5 failure mode: the decline-on-no-target behavior is replaced
   by a learner-evidence gate.
3. The wrong-target test discriminates the mechanism: researcher error no
   longer fails a composition the learner can genuinely support. The
   verifier follows learner evidence, not the researcher's answer key.

## 6. What this does NOT establish / limitations

1. Evidence still comes from world experience of the composed query
   relation. On a genuinely novel (s,r) with no experience, the learner
   withholds (3.2). Learner-verification does not bootstrap evidence from
   nothing; same boundary as C181.
2. The evidence phase teaches a direct FACT via lv_observe (C181 V4
   precedent). The reliability machinery, not the fact alone, gates
   verification, and the wrong-target test shows the gate follows learner
   evidence over researcher targets. But a stricter future test could build
   the prediction basis purely through MAP execution (no direct fact) to
   further separate memory from verification.
3. Threshold value 3 is researcher-set scaffold, honestly labeled; the
   learner does not yet choose its own evidence requirement.
4. +1/-1 scoring is bookkeeping inherited from C181; the learner owns the
   values and rankings, not the arithmetic.
5. Only the 3-structure world was tested; T2A/T2B/T3/T4 analogues with
   learner verification are future work, as is hooking compose_lv into
   ev_query (the direct-call harness was the honest unit-test choice here).

## 7. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: PRED layout, +1/-1 rule,
  threshold value 3, accept/reject/withhold structure, header fields
  32/36, evidence-phase protocol, direct-call harness.
  (Plus inherited: unified DFS/candidate/promotion machinery.)
- LEARNER-OWNED STRUCTURAL DECISIONS: all reliability values, which
  predictors are trusted, the T1-LV accept verdict, the T-NE withhold
  verdict, the T-WE accept-despite-wrong-target verdict.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- REUSE EVENTS: prediction reused for DFS termination and final verify.
- REVISION EVENTS: 0 (verification only).
- COGNITION LINES: 320 (lvcomp_patch.zag).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 8. Artifacts

- `PREREG.md` (frozen; committed alone before implementation, 3e692a037)
- `NAMECHECK.md` (Step 0 guard, provenance, constraints)
- `REPORT.md` (this file)
- `lvcomp_base.zag` (cc_base.zag + un_patch.zag copies, 2097 lines)
- `lvcomp_patch.zag` (learner-verified composition, 320 lines)
- `lvcomp_driver.zag` (battery: T1-LV, T-NE, T-WE)
- `lvcomp_full.zag` (assembled, 2624 lines)
- `lvcomp_bin` (binary)
- `lvcomp_compile.txt` (warnings only, same class as unified build)
- `lvcomp_run1.txt`, `lvcomp_run2.txt`, `lvcomp_run3.txt`
  (SHA-256 `b2ea4bf5c923d5c1033e959b849ea29a5b955ef52f0d268472faff6c48926361`, 3/3 identical)

Constraints honored: unfrozen variant only; frozen sources read-only
(copies); pure Zag via pinned znc; safebin active, zero Python
invocations; zero em/en dashes byte-verified; research paper untouched;
nothing pushed; explicit pathspecs on git add and git commit.
