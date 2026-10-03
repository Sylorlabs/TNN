# REPORT: H-COMPVER-2 Learner-Verified Composition Extension

**Verdict: COMPOSITION-LEARNERVER2-COMPLETE.**
All 8 tests PASS on the full battery, 3/3 byte-identical. Learner-verified
composition extends to 4-structure, 5-structure, and cross-domain worlds;
honestly fails the partial-applicability world (no false positive);
withholds on sub-threshold evidence (reliability 2) and proceeds at
exactly the threshold (reliability 3); and composes through the new
CONSTRUCT-goal query entry point without FACT recall.

## 1. Question

H-COMPVER-1 (prereg 3e692a037, results faf1b2547) built compose_lv:
learner-verified composition with no researcher answer parameter,
verification against the learner's own prediction gated by earned
reliability (threshold 3). T1-LV PASS (107), T-NE withhold PASS, T-WE
PASS (researcher error 999 no longer fails). Recorded caveats: only the
3-structure world tested; T2A/T2B/T3/T4 analogues and the ev_query hookup
are future work; compose_lv was called directly because the
post-evidence FACT would activate-shortcut through ev_query.

H-COMPVER-2 answers: (a) does compose_lv extend to other arities and
domains; (b) a principled ev_query hookup resolution; (c) the
unreliable-evidence boundary: withhold or gamble?

## 2. Mechanism (unfrozen variant only)

- Base: lv2_base.zag = byte-identical copy (cmp-verified) of
  composition_learnerver/lvcomp_base.zag (cc_base.zag + un_patch.zag).
  Copied, never edited. ev_query untouched.
- Patch: lv2_patch.zag = first 320 lines verbatim (cmp-verified) copy of
  composition_learnerver/lvcomp_patch.zag (compose_lv, lv_dfs, lv_setup,
  lv_predict, lv_pred_resolve, lv_observe, lv_verify_chain) plus a new
  27-line section: ev_cquery.
- ev_cquery: the principled hookup resolution. RETRIEVE and CONSTRUCT are
  distinct query goals served by distinct operations, not by a flag on
  one operation. ev_query keeps its frozen activate-first RETRIEVE
  pipeline (activate, rebind, composition, trial, bootstrap) untouched;
  the activate-shortcut after the evidence phase is correct RETRIEVE
  behavior, not a bug. ev_cquery(W,s,r,masked,st) is the CONSTRUCT-goal
  entry: derive the answer from learned MAP structures and verify it
  against the learner's own prediction. Direct FACT recall is not an
  answer source under this contract: the evidence FACT serves only as
  prediction basis inside lv_setup, never as the answer; the answer must
  come out of composed MAP execution equal to the learner prediction
  (lv_verify_chain). This mirrors the existing division of labor where
  rebind_try, compose_try, and mp_run are separate operations with
  separate contracts rather than flag variants of one query function.
  Withholding propagates: a CONSTRUCT goal with no reliable prediction
  basis returns -3 rather than falling back to trial, because a trial
  guess is not a constructed answer. No researcher target parameter
  exists on this entry point either.
- Driver: lv2_driver.zag (455 lines). World builders ported verbatim
  (body-identical, diff-checked) from composition_unified/un_driver.zag
  (T1/T2A/T2B/T3/T4 train, couse, zfacts, gap). Evidence helper:
  parametrized predict/observe cycles via lv_predict/lv_observe for
  (101,70) with the true world outcome o (C181 V4 precedent); after N
  cycles the evidence FACT pred_score = N-1.

## 3. Battery and results (3/3 byte-identical)

SHA-256 of each run:
`fc054b5e3bfb3ef8fcb2e4ad5d94dd0f52e5c65dc7de3b9e6ea8e282d2f8942f`
(runs 1, 2, 3 identical). Summary line: `CMP-LV2-SUMMARY 1 1 1 1 1 1 1 1`.

Evidence behavior (all worlds): cycle 0 pred = -999999 (honest no-basis);
cycles 1-4 predict the true outcome; factscore = cycles - 1.

### 3.1 T2A-LV: 4-structure -- PASS (K1)

X+Y+W+V world, evidence 5 cycles o=109, compose_lv(W,101,70,0,st).

| metric | value |
|---|---|
| ans | 109 |
| segments | 4 (MAPs 13 26 39 52) |
| tried / rejected | 1 / 0 |
| live MAPs | 10 -> 11 (MAP_Z promoted) |
| LINK14 out of MAP_Z | 4 |
| type-15 co-use edges | 3 -> 6 |

K1 satisfied: ans=109, +1 MAP, LINK14=4, type-15 >= +3, tried >= 1.

### 3.2 T2B-LV: 5-structure -- PASS (K2)

X+Y+W+V+U world, evidence 5 cycles o=111.

| metric | value |
|---|---|
| ans | 111 |
| segments | 5 (MAPs 13 26 39 52 65) |
| tried / rejected | 1 / 0 |
| live MAPs | 13 -> 14 |
| LINK14 out of MAP_Z | 5 |
| type-15 co-use edges | 4 -> 8 |

K2 satisfied: ans=111, +1 MAP, LINK14=5, type-15 >= +4.

### 3.3 T3-LV: cross-domain -- PASS (K3)

Plen-3 chain X + single-hop Y world, evidence 5 cycles o=105.

| metric | value |
|---|---|
| ans | 105 |
| segments | 2 (MAPs 27 42) |
| tried / rejected | 1 / 0 |
| live MAPs | 4 -> 5 |
| LINK14 out of MAP_Z | 2 |
| type-15 co-use edges | 1 -> 2 |

K3 satisfied: ans=105, +1 MAP, LINK14=2, type-15 >= +1.

### 3.4 T4-LV: partial applicability, honest failure -- PASS (K4)

X plen-4 (Z needs 3 of 4 hops) + Y world, evidence 5 cycles o=106.
Reliability reaches 4, so the gate passes; the question is whether the
DFS can construct anything.

| metric | value |
|---|---|
| ans | -2 (LV-COMP-FAIL) |
| tried / rejected | 0 / 0 (no verify attempted) |
| live MAPs | 4 -> 4 (nothing promoted) |

K4 satisfied. Learner verification does not fix the atomic-MAP
assumption and does not hallucinate a partial composition: the DFS
search space is identical to unified compose_try, which cannot reach
106. Evidence supports the outcome, structure does not support
construction, and the operation reports -2 rather than a false positive.
This is the "withhold where it doesn't" arm for structural support.

### 3.5 Threshold boundary: T-THR-LO withholds, T-THR-HI proceeds -- PASS (K5)

T1 world, evidence cycles varied. Reliability = cycles - 1.

| test | cycles | rel | ans | tried | maps | result |
|---|---|---|---|---|---|---|
| T-THR-LO | 3 | 2 | -3 (LV-WITHHOLD unreliable rel=2) | 0 | 7 -> 7 | PASS |
| T-THR-HI | 4 | 3 | 107 | 1 | 7 -> 8 | PASS |

K5 satisfied. The gate is exact: closed at reliability 2, open at
exactly the threshold value 3. Below threshold the operation declines
before any search (tried=0, nothing promoted).

On withhold vs gamble (task question 4): compose_lv withholds, and
withholding is the rational behavior given the gate. The gate exists to
prevent structural promotion (MAP_Z with LINK14 provenance plus new
type-15 co-use edges written into persistent learner state) on weak
evidence. Gambling would let luck drive learning: a correct guess at
reliability 2 would still be right by luck, not by earned trust, and
every gamble that writes structure on thin evidence compounds into
uncalibrated learner state. The honest consequence of a preregistered
reliability gate is to decline when the learner has not earned the
right to trust its predictor. Whether the threshold VALUE (3) is
optimal is a separate researcher-scaffold question; the experiment
validates the gate's exactness, not the value's optimality. The value
remains honestly labeled researcher scaffold, as in H-COMPVER-1.

### 3.6 Hookup: T-HOOK and T-HOOK-NE -- PASS (K6)

| test | call | ans | tried | maps | link14 | result |
|---|---|---|---|---|---|---|
| T-HOOK | ev_cquery(W,101,70,0,st), 5-cycle evidence | 107 | 1 | 7 -> 8 | 3 | PASS |
| T-HOOK-NE | ev_cquery(W,101,70,0,st), no evidence | -3 (LV-WITHHOLD nobasis) | 0 | 7 -> 7 | - | PASS |

K6 satisfied. The CONSTRUCT-goal entry point composes through the query
API: tried=1 and MAP_Z promoted with LINK14=3 prove composition
genuinely ran (compose_lv never consults activate, so the answer cannot
be FACT recall). With no evidence the entry point withholds exactly as
compose_lv does. The hookup problem is resolved without touching
ev_query: RETRIEVE keeps its activate-first pipeline; CONSTRUCT is a
separate operation with a separate contract.

## 4. Kill bar scorecard

- K1 (T2A-LV PASS with promotion metrics): PASS.
- K2 (T2B-LV PASS with promotion metrics): PASS.
- K3 (T3-LV PASS with promotion metrics): PASS.
- K4 (T4-LV honest -2, no promotion, no false positive): PASS.
- K5 (threshold boundary: LO withholds -3 tried=0, HI proceeds PASS 107): PASS.
- K6 (hookup: T-HOOK 107 via composition, T-HOOK-NE -3): PASS.
- K7 (3/3 byte-identical, SHA-256 recorded): PASS.
- K8 (0 modes/bridges/handlers/semantic cases; `expected` token 0
  occurrences in lv2_patch.zag; compose_lv/lv_dfs/ev_cquery take no
  researcher-target parameter; ev_query untouched): PASS.
- K9 (cognition lines recorded): 347 lines lv2_patch.zag (320 verbatim
  H-COMPVER-1 + 27 new ev_cquery section); driver 455 lines.

All bars pass: COMPOSITION-LEARNERVER2-COMPLETE.

## 5. What this establishes

1. Learner-verified composition generalizes across arity and domain: the
   same compose_lv (no researcher target, learner-prediction termination
   and verification) succeeds on 4-structure, 5-structure, and
   cross-domain worlds wherever evidence supports the composed outcome
   and the MAP structures support construction.
2. The honesty boundary is two-dimensional and both arms hold: (a)
   evidential: sub-threshold reliability withholds before search
   (T-THR-LO), and the gate opens at exactly the threshold (T-THR-HI);
   (b) structural: with full evidence but no constructible chain, the
   operation fails cleanly without promoting anything (T4-LV). Neither
   arm gambles or hallucinates.
3. The ev_query hookup has a principled resolution: goal-typed entry
   points. The activate-shortcut is correct RETRIEVE behavior; CONSTRUCT
   is a distinct operation (ev_cquery) whose contract excludes FACT
   recall as an answer source. No flag, no ev_query change, no mode.
4. The threshold gate is exact (opens at 3, closed at 2), and
   withholding below it is the rational behavior: the gate protects
   persistent learner state from luck-driven promotion.

## 6. What this does NOT establish / limitations

1. Evidence still comes from world experience of the composed query
   relation. On a genuinely novel (s,r) the learner withholds
   (T-HOOK-NE). Learner verification does not bootstrap evidence from
   nothing; same boundary as C181 and H-COMPVER-1.
2. T4 still fails: learner verification does not address sub-MAP
   decomposition. The atomic-MAP assumption stands as the open
   composition question.
3. Threshold value 3 remains researcher-set scaffold; the learner does
   not choose its own evidence requirement. This battery validates the
   gate's exactness, not the value's optimality.
4. ev_cquery is intentionally a thin delegation; its substance is the
   documented contract distinction. Whether CONSTRUCT vs RETRIEVE should
   be caller-specified or inferred by the learner from context is open
   future work (inference would need its own evidence and its own
   preregistered bar).
5. Only the composition-battery worlds were tested (T1/T2A/T2B/T3/T4
   analogues). Sealed adversarial worlds for learner-verified
   composition are future work.

## 7. Standing metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: PRED layout, +1/-1 rule,
  threshold value 3, accept/reject/withhold structure, header fields
  32/36, evidence-phase protocol, the RETRIEVE/CONSTRUCT contract
  distinction, world builders (frozen protocol), direct-call and
  ev_cquery harnesses. (Plus inherited: unified DFS/candidate/promotion
  machinery.)
- LEARNER-OWNED STRUCTURAL DECISIONS: all reliability values, which
  predictors are trusted, all 8 battery verdicts (5 accepts, 1
  structural fail, 2 withholds).
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- REUSE EVENTS: prediction reused for DFS termination and final verify
  (all 5 accept tests).
- REVISION EVENTS: 0 (verification only).
- COGNITION LINES: 347 (lv2_patch.zag); 27 new (ev_cquery section).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 8. Artifacts

- `PREREG.md` (frozen; committed alone before implementation, 6081afa94)
- `NAMECHECK.md` (Step 0 guard, provenance, constraints)
- `REPORT.md` (this file)
- `lv2_base.zag` (copy of lvcomp_base.zag, 2097 lines, cmp-verified)
- `lv2_patch.zag` (347 lines: 320 verbatim H-COMPVER-1 + 27 ev_cquery)
- `lv2_driver.zag` (455 lines: 8-test battery)
- `lv2_full.zag` (assembled, 2899 lines)
- `lv2_bin` (pinned znc build)
- `lv2_compile.txt` (warnings only, same A0102 class as H-COMPVER-1)
- `lv2_run1.txt`, `lv2_run2.txt`, `lv2_run3.txt`
  (SHA-256 `fc054b5e3bfb3ef8fcb2e4ad5d94dd0f52e5c65dc7de3b9e6ea8e282d2f8942f`, 3/3 identical)

Constraints honored: unfrozen variant only; frozen sources read-only
(copies, cmp-verified); pure Zag via pinned znc; safebin active, zero
Python invocations; zero em/en dashes byte-verified; research paper
untouched; nothing pushed; explicit pathspecs on git add and git commit.
