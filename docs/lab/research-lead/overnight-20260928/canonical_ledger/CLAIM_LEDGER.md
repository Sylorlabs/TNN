# Evidence-First Claim Ledger

**Path:** `docs/lab/research-lead/overnight-20260928/canonical_ledger/CLAIM_LEDGER.md`
**Built:** 2026-09-30, Canonical Reconstruction Archivist
**Source rule:** committed evidence only (git log, committed RESULT files,
committed preregs). Where the contaminated research paper asserts something
with no committed backing, the claim is marked UNVERIFIABLE. No claim rests
on paper prose alone.

**Status labels used:** SURVIVES, DOWNGRADED, KILLED, VOID, INVALID,
RETRACTED, SUPERSEDED, EXPLORATORY, BUILD-PASS, BUILD-FAIL, UNVERIFIABLE.

---

## C01. F3 REVISE causal-revision pipeline (11 stages)

Claim: causal revision mechanism progresses through the full 11-stage
promotion pipeline.

- Stage 1 prereg: c197e7cd8 (frozen before implementation)
- Stage 2 implementation: 7009d711c (REVISE-PASS)
- Stage 3 sealed eval: prereg 8cdf0992a; result 1df8addec (REVISE-SEALED-PASS)
- Stage 4 reproduction: result 7407dd4a7 (REVISE-REPRO-PASS, 33/33
  byte-identical). No separately committed step-4 prereg found in git log.
  Documentation gap noted.
- Stage 5 baseline: prereg 4786633c5; result c810d5f55 (REVISE-BASELINE-PASS)
- Stage 6 alternative-explanation attack: prereg 12da75511; result
  bbdb65c99 (REVISE-ATTACK-SURVIVES)
- Stage 7 OOD: prereg 7bf467d35; result 1125be9bb (REVISE-OOD-PASS)
- Stage 8 ablation: prereg 6dcb1f11b; result 96e22de82 (REVISE-ABLATION-PASS)
- Stage 9 transfer: prereg 7e80e52e6; result c3c3e3bc8 (REVISE-TRANSFER-PASS);
  clean pure-Zag re-run prereg 6f95d7b1c; result 53b9a9a27
  (REVISE-TRANSFER-PASS, 3/3 byte-identical, zero Python)
- Stage 10 independent red team: prereg fc57bb738; result 4a2b8ef43
  (REVISE-REDTEAM-KILLS)
- Stage 11 governance audit: prereg 62f6a9c31; result 85fe2043c
  (REVISE-AUDIT-FAIL, A3 fails at S9); clean step-9 re-audit prereg
  fc2767234; result 80c237db3 (REVISE-REAUDIT-PASS)

**Verdict:** REVISE-REDTEAM-KILLS for the generic causal-revision
interpretation. **Status: KILLED (generic L3 reading); bounded L2 utility
in confounder-free worlds SURVIVES.** Steps 1-9 have clean evidence; the
stage 9 governance blemish was separately remediated.

## C02. OpScope pipeline

Claim: word-scoped negation mechanism.

- Rebuild: 837c02c59 (OPSCOPE-REBUILD-PASS)
- Sealed eval: 7ca508cd0 (SEALED-PASS)
- Reproduction: daafbebbb (OPSCOPE-REPRO-PASS, 3/3 byte-identical)
- Baseline: prereg de0db4b64; result 4c4287c50 (OPSCOPE-BASELINE-PASS)
- Alternative-explanation attack: prereg eeca946f4; amendment afde02d2d;
  result 0add71b64 (OPSCOPE-ATTACK-KILLS, FA-SUFFIX: claimed word-scoped
  negation was suffix suppression after "not")

**Status: KILLED as word-scoped negation; bounded L2 suffix-suppression
behavior stands as a refuted-claim component, do not continue promotion
under the refuted claim.**

## C03. C1-CLEAN lifetime learning

Claim: broad lifetime learning passes clean under frozen blind protocol.

- Prereg: 13e4b1ce3 (frozen alone, before implementation)
- Freeze: b8d38d9c8 (contestant and world-generator hashes)
- Worlds: e0a30377f (5 blind seeds, 3 canonical + 2 hard worlds)
- Result: b2b1ec415 (C1-CLEAN-PASS). Canonical W0/W1/W2: 63/63 on every
  world, 3/3 byte-identical repetitions per world (9/9 canonical runs
  perfect). Exploratory hard worlds: H0 66/67 on all three repetitions,
  H1 67/67 on all three repetitions. Zero Python; hashes unchanged.

**Status: SURVIVES as canonical lifetime-learning result.** H0 contains a
deterministic law-revert miss; revision after a reverted law is a real
mechanism boundary. Hard-world prereg named denominator 64 while actual
denominator was 67; disclosed, canonical results unaffected. The older C1
wave is EXPLORATORY, GOVERNANCE-VOID, NOT CANONICAL.

## C04. Beam Design 1

Claim: beam search design variant 1 scored 50/64 vs baseline 53/64 on R3
Arm 2.

- Prereg / implementation / result commits: none located by commit-message
  search. The architecture review 2135396ce cites the scores.

**Status: UNVERIFIABLE as a standalone committed claim.** Scores are
usable only as review context, not as evidence.

## C05. Beam unified build

Claim: unified beam clean rebuild fixes the compositional search.

- Prereg: 1339b4471 (governance contaminated, K3 failed)
- Result: dac4a4187 (BEAM-UNIFIED-FAIL)
- Clean rebuild prereg: d074eda3d; result: fc03664f2 (BEAM-UNIFIED-FAIL)

**Status: KILLED.** Unified beam does not repair the R3 Arm 2 failure.

## C06. Beam G0 diagnostic

Claim: instrumented diagnostic of the failing unified beam R3 Arm 2.

- Prereg: eb0ff7fdf; result: 2faf4196d (G0-MERGED, bounded L2)

**Status: SURVIVES as a diagnostic result (bounded L2).**

## C07. Beam G2 refutation-seeking policy

Claim: G2 policy improves R3 Arm 2.

- Prereg: d4485706f; result: c0babffab (G2-FAIL). R3 Arm 2: 49/64 under G2
  vs 52/64 baseline. F-FIT, F-DIVERSE-FAIL, F-NODOM, F-BLOAT fired.

**Status: KILLED.** Alternative explanation "merged, then would have lost
anyway" survives. Pure Zag, deterministic.

## C08. Beam architecture review

Claim: the representation is wrong at the search level, not expressively
incapable.

- Review: 2135396ce (BEAM-REVIEW-COMPLETE). Baseline R3 Arm 2 53/64;
  Design 1 50/64; unified beam 52/64; G2 49/64. Pairwise composition plus
  fit and operation tax lacks a representation of partial compositional
  progress. Retention and selection were not binding constraints. R3 Arm 2
  is closed to further beam retention/selection tweaks; pivot is
  conditional-first representation-level search. Do not build G1, further
  retention/selection variants, or G4.

**Status: SURVIVES as a review verdict (bounded L2 assessment of the
lineage).**

## C09. Conditional-first program search v1

Claim: researcher-supplied COND primitive plus Branch-Accuracy Profile
combiner repairs compositional search.

- Design: e7ca7d83a (CONDITIONAL-DESIGN-COMPLETE, bounded L2 only)
- Prereg: 1981c00ea; result: c6f6d6787 (CONDITIONAL-FAIL)
- Positive: conditional hit in round 0; R3 Arm 2 solved 64/64; phase-1 D
  discovery round 4 to round 1. Failure: FREC I3 regressed 40/64 to 32/64;
  BAP-generated conditionals overfit 32-row evidence.

**Status: KILLED as a general search improvement. Bounded L2 mechanism
worked on the primary task only.**

## C10. Conditional tax v2

Claim: T1 license-cost tax plus T2 stability-gated licenses make
conditionals safe.

- Design: 18e0c12a6 (CONDITIONAL-TAX-DESIGN-COMPLETE)
- Prereg: 85b4325e5; result: b0d1749f2 (CONDITIONAL-TAX-FAIL)
- No conditional hit; R3 Arm 2 51/64; FREC I3 recovered to frozen 40/64.
  Diagnosis: fixed Tier-1 minimum slice of 4 blocked genuine D (one branch
  had fewer than 4 observed rows). An uncommitted /tmp debug build using
  minimum slice 1 was disclosed; provenance and language use unaudited.

**Status: KILLED. The /tmp debug disclosure is not canonical evidence.**

## C11. Conditional threshold calibration

Claim: recalibrated Tier-1 minimum slice min(4, en/8) repairs the tax-v2
block while preserving the FREC repair.

- Prereg: 7ae3a88fa (CONDITIONAL-THRESHOLD-PREREG-FROZEN)
- Result: d0d296650 (THRESHOLD-PASS). All frozen bars pass, verified in the
  committed RESULT file: CONDHIT round 0, A2-PASS 1 (reuse 64/64 with D
  library term), DROUND 1, R1 1/5 no regression, FREC I1/I2/I3 all at or
  above frozen (48/64, 63/64, 40/64), 3/3 byte-identical, zero Python, nine
  audits none firing.

**Status: BUILD-PASS (builder level only).** Not promoted through the
11-stage pipeline; no L3, Criterion 0, or SURVIVES claim.

## C12. Valley

Claim: valley mechanism produces accepted instances.

- Prereg: cf0c85e78; result: 32eb28f3d (VALLEY-FAIL, 0/14 accepted;
  Family K instances had two-edit solvers)
- Trigger monitor: 138491e6a (TRIGGER-NOT-FIRED; checks 2-4 also
  not-fired: 88111bb65, 098ae71bb)

**Status: KILLED.** Two redesign workers failed through output truncation;
no valid redesign exists; valley redesign gap is open.

## C13. T6 sealed evaluation

Claim: T6 passes the equality-gated quadratic/linear task.

- Gate: 9ad539fc2 (T6-GATE-READY)
- Sealed: 2c982c178 (T6-PASS means evaluation completed)
- Measured: C2 1/12 train, 0/10 held-out; D 9/12 train, 7/10 held-out; B
  not evaluated (no v2/P-VM mechanism); C2 lacks jump opcodes.

**Status: DOWNGRADED claim.** The sealed PASS certifies the evaluation ran
cleanly; capability PASS on C2 and D did not occur. Purity caveat preserved
at 69730b4ab.

## C14. C0INTEG Phase B

Claim: continuing-integration Phase B produces stable cognitive triples.

- Result: a2896f022 (PHASEB-FAIL)
- Redesign: 9f1864f9
- Pilot prereg: 237f7a1ee; pilot result: 907ccee49 (PHASEB-PILOT-FAIL;
  all G1-G5 had 0/5 stable triples)

**Status: KILLED.** C0-D remains open. No adjacent repair without an
architecture review.

## C15. Continuing-learner scale-up

Claim: one process sustains 65,536 bytes of state under pressure with zero
drops.

- Pilot: aec4b49e3 (PILOT-CLEAN-PASS)
- Prereg: 3e02255f3; result: f9b3372d5 (SCALEUP-PASS). One process, 65,536
  bytes state, zero drops, PRESS=1, deterministic.

**Status: SURVIVES as bounded L2 C0-D reuse evidence.** Not promoted
through the 11-stage pipeline.

## C16. Procedure discovery v1 (broadcast-last)

Claim: TNN invents a reusable procedure (L3).

- Result: 850b79ddb (broadcast-last discovered: SUB(N,C1), index 38)
- RT2: 6e88f3003 (Family X authoritative 8/8 PASS; semantic 85/1055;
  extraction vulnerability CONFIRMED)
- H-REVISE: c7bfaeba1 (L3 criterion 12 KILLED; mathematical impossibility
  proof against revision)

**Status: DOWNGRADED to bounded L2+. Not L3.** Met 11 of 12 L3 criteria,
failing criterion 12 (revision after counterexample). Extractor breaks on
repeated characters.

## C17. H-PROCLANG1

Claim: procedure language invention (L3).

- Reproduction: 046ab1724 (REPRODUCED)
- Baseline: prereg ddd90d06b; result e079d6dd6
- Adversary: prereg a0ea62532; result b5dc77efe (A1/A2/A3 ATTACK-SUCCEEDS;
  L3 reading DOWNGRADED to bounded L2+)

**Status: KILLED as L3; DOWNGRADED to bounded L2+.**

## C18. REPEXPAND-1

Claim: representational expansion (L3).

- Baseline: 2c020b444 (BASELINE-MATCHES)
- Adversary: 93ce9a09a (AX1-AX4 all ATTACK-SUCCEEDS; L3 interpretation
  KILLED; strong L2+ stands)

**Status: KILLED as L3; DOWNGRADED to bounded L2+.**

## C19. H-CAUSALEXP-CONSTRUCT

Claim: active causal experiment construction.

- Final governance verdict: 45db44fab (SURVIVES-AS-L2, L3 KILLED at step 11)
- Governance sweep 2026-09-30: 6b3dd03e8 (prereg lineage PASS, pure-Zag
  PASS, reproduced, 3 flags logged)

**Status: DOWNGRADED to bounded L2. SURVIVES-AS-L2.**

## C20. H-EXP2

Claim: experiment planning mechanism.

- Adversary prereg: 0c6d62b9c; result: a3e9d2966 (SURVIVES all frozen bars
  with two DOWNGRADED claims: state-selection not experiment-planning;
  ndiff ranking unvalidated)

**Status: SURVIVES with downgrades (bounded L2).**

## C21. H-EXP3

Claim: reachability-aware experiment selection.

- Result: f8299c388 (SURVIVES 4/4; reachability awareness addresses H-EXP2
  downgrades)

**Status: SURVIVES (bounded L2).**

## C22. H-MEM8 memory mechanism

Claim: memory mechanism with top-aligned recency weights and inversion
reconciliation.

- Prereg: 3314b8c24; result: 185cea90b (H-MEM8 BUILD-PASS; builder label
  only, no SURVIVES claim)
- H-MEM7 adversary: prereg a3203c3d0; result 9c41b61d2 (DOWNGRADED;
  X-M7-2 inversion, X-M7-3 lemma falsified)

**Status: BUILD-PASS (bounded L2). Not SURVIVES.**

## C23. H-ROUTER6

Claim: router mechanism survives red team.

- Prereg: 7600ab114; result: 0049ad295 (SURVIVES 4/4)

**Status: SURVIVES (bounded L2).**

## C24. H-ROUTER7

Claim: router-7 mechanism stands.

- Prereg: 8f795a1aa; result: 37ce0d271 (DOWNGRADED: capacity defeat of
  total-table headline plus phantom fallback emit; R2 holds)

**Status: DOWNGRADED.**

## C25. H-FDCR-UNIFIED8

Claim: unified FDCR concept integration.

- Result: 11918217a (SURVIVES 51/51); red team: d64a9a025 (SURVIVES 18/18)
- Earlier unified: 52d2962fc (SURVIVES 23/23); a1936a7fd (DOWNGRADED by
  red team); UNIFIED7: 18dd712a3 (SURVIVES 47/47)

**Status: SURVIVES (bounded L2).**

## C26. H-REVISE chain (procedure revision)

Claim: procedure revision under counterexample.

- R9 red team: prereg 045d5981a; result 38c847c46 (SURVIVES 17/17)
- R10: prereg 3f8304e78; result aa422610f (KILLED per K-RV10-4; prereg
  premise incorrect; R10 mechanism sound)
- R11: prereg 36b2fbc71; result 1a2fd99bd (SURVIVES 145/145)
- RV11-ADV: prereg cde064337; result 20f40a4d1 (SURVIVES, 0/4 kills)
- Procedure-revision prereg: 2d720d9bc

**Status: SURVIVES as bounded L2 procedure-revision utilities.** Note the
chain survives as revision utilities while the v1 procedure invention
(C16) still failed criterion 12 at the L3 bar; the two claims are distinct.

## C27. GOALREVISE

Claim: map revision under transfer surprise.

- Prereg: 60e4dcc9a; result: cb2a6fdbc (REVISE-TESTED)

**Status: BUILD-PASS (bounded L2).**

## C28. Bridge (generic construction replaces recipes)

Claim: generic bridge construction with episode-persistent discovery
buffer.

- Design: e4f8642fc; prereg: 19ce88021; impl: ebdc4fd3e (BRIDGE-TESTED)
- Fix prereg: 75231a87e; fix impl: d920af162 (FIX-BUILT-PASS)
- T-ADV5 re-eval prereg: 66aed6805; result: 83c02efff (TADV5-ACCEPTABLE)
- Greedy: prereg a79f842e5; impl e96b998c7 (GREEDY-PASS); regression
  338eb4241 (GREEDY-REGRESSION-PASS). T-ADV6 design 4f9f333cee48dd9bc7c2f5bd0cd1aea9edf1a443
  (TADV6-DESIGN-FAIL)

**Status: SURVIVES as bounded L2 generic construction.** K=2 robust only
for the current bounded threshold representation; no L3 or SURVIVES beyond
the L2 reading.

## C29. SEM

Claim: semantic mechanism reaches L3.

- Kill battery: fded44631 (SEM-L3 downgraded to L2+)

**Status: DOWNGRADED to bounded L2+.** Retained as bounded subsystem,
experimental baseline, and control reference; explicitly not L3, not
general semantic understanding, not representational invention. Retireable
only through explicit supersession.

## C30. H-INTENT-UNIFIED9

Claim: intent-unified mechanism stands.

- Result: 3d6a27625 (SURVIVES 4/4); red team prereg: 1ad5d1d1f; result:
  55ee07353 (IU9-ADV SURVIVES)

**Status: SURVIVES (bounded L2).**

## C31. DDES

Claim: DDES achieves L3.

- Prereg: 7abe1ef66; A1: 678ea4162 (L3-GAP-ANALYZED, all kill bars pass)
- DDESGEN prereg: c04d5610d; result: 843c45fee (FIXABLE; 6/6 converge on
  3/4/5 vars)
- DDESRT2 prereg: 8e2a8ecde; result: b19e0e594 (ATTACK-SUCCEEDS;
  synthesis is 3-var specific)

**Status: KILLED as L3; bounded DDES utility stands.** Integration into the
continuing learner is pending.

## C32. Salt-battery corrections (2026-09-29)

- H-C kill: INVALID (kill-bar thresholds invented in the results commit
  57d055bbb; bar redefined post-hoc). H-C returns to SURVIVES under its
  actual frozen bar.
- H-B verdict: VOID (bar fit one point below the observed score). Later
  re-freeze: 7aeb0cbda (H-B SURVIVES under the re-frozen principled bar).
- H-A kill: stands on the 5 wrong emissions; diagnosis RETRACTED (the Eaff
  arm carried zero uppercasing signal; H-A learned identity from destroyed
  evidence, an uncalibrated arm, not a mechanism boundary). Needs a
  calibrated re-run.

**Status: mixed (INVALID / VOID-then-SURVIVES / KILL-with-RETRACTED).**
Measurements 48/48, 119/120, 8/8 remain real and deterministic but must be
judged only against principled frozen bars.

## C33. DEVANG2 / developmental semantic language

- Prereg: 402e53d32; result: 153e2af8e (DEVANG2 BUILD-FAIL; memory-safe,
  segmentation fails)
- H-SEG2 adversary: prereg 26fc0ee4e; result 0046f4f70 (DOWNGRADED;
  frequency-fragile, long-input crash)

**Status: BUILD-FAIL / DOWNGRADED.** Developmental language remains open.

## C34. TNN-vs-LLM arena figures

- Clean canonical: 0.573, 39/68
- Research-generic: 0.691, 47/68 (audit 4a98214e0; adapter classification)
- Adapter-inflated: 0.779, 53/68 (0e72d7b1b ARENA-CAUSAL v6 BUILD-PASS,
  C9 1.000)
- Arena conflict C6: 9211de19e (BUILD-PASS 7/7, 0.632 to 0.676)
- LLM baseline: PENDING (no credentials or spending authorized)
- HUMAN BASELINE NOT MEASURED

**Status: BUILD-PASS figures only.** No competitive superiority claim is
established; arena numbers are components of a measurement apparatus, not
evidence that TNN is preferable to an LLM.

---

## C35. DDES integration into the continuing learner

Claim: the bounded DDES utility integrates with the continuing learner
at mechanism level.

- Prereg: c3fecd3c8 (frozen alone, before implementation)
- Implementation: d9f3871c5
- Evidence: f843188ad (DDES-INTEGRATION-PASS). Base learner withholds on
  the frozen ambiguous causal case; integrated learner constructs one
  discriminating intervention plan, executes once, observes an outcome
  matching exactly one of two hypotheses, eliminates the other, and
  resolves correctly. Base causal probes byte-identical between modes.
  3/3 deterministic.

**Status: SURVIVES as bounded L2 integration.** Closes the "integration
pending" item recorded under C31. Arena C9 has not been remeasured; the
arena gap is closed at the mechanism level only. No L3 claim.

## C36. L3C emergent revision-form builder

Claim: the learner constructs conditional-dispatch structure after
hitting the H-REVISE impossibility (builder level).

- Prereg: dc9a91501 (frozen alone, before implementation)
- Result: e663864f5 (L3C-FORM-PASS). Learner starts without a conditional
  form; contradiction monitor detects identical signatures requiring
  different outputs; learner constructs dispatch structure using five
  generic graph operations. Fixed discriminator discovered (f2 == 1) on
  one family and (f3 == 9) on a second, with zero source change.
  Constructed state: one dispatch node, two terminal nodes, two edges per
  signature. Family 1: 6/6; family 2: 4/4. Construction-disabled ablation
  fails clash cases while retaining training cases. 3/3 byte-identical.
  Prereg contained an arithmetic slip ("12/12 total" vs operative
  6 + 4 = 10); result preserved as 10/10 with disclosure.

**Status: BUILD-PASS (builder level only).** Evidence toward C0-A and
C0-B; NOT L3, NOT full Criterion 0, NOT SURVIVES. The fixed discriminator
and protocol may be a conditional constructor in disguise; see C41.

## C37. Continuing-learner stress battery

Claim: the continuing learner survives memory pressure, interference,
correction, and delayed reuse in one unbroken lifetime.

- Prereg: 4ca3a7196 (frozen alone); addendum e16897bc9 clarifying K-S4(b)
  pre-implementation
- Implementation + evidence: daa9bf2fc (LEARNER-STRESS-PASS). 8-phase
  lifetime, one process, no resets, no task labels, no recompilation.
  Retention 8/8 through two pressure waves and 22-rule interference;
  correction uptake 5/5 with 0/12 collateral and double-correction chains
  resolving to the latest label; corrections survive targeted bombardment
  4/4; delayed reuse 5/5 routing through corrected premises with zero
  re-teaching. 3/3 byte-identical.

**Status: SURVIVES as bounded L2 continuing-learner evidence.**
Mechanism finding: pressure wave 2 churned 19 of 20 never-queried
newcomers via a revolving-door eviction slot; new knowledge must earn
retention through use. Recorded as the pre-DDES baseline for the stress
battery.

## C38. OpScope operator/scope R1-R4

Claim: the frozen R1-R4 operator/scope design fixes negation on the
developmental battery.

- Prereg: 51c54e262 (frozen alone; K=2 preregistered with written
  justification after a prior build measured K=3 unsatisfiable; the prior
  K=3 FAIL verdict stands untouched)
- Implementation + results: c60bfbe7a (OPSCOPE-R1R4-PASS). T1 (items
  109-111) 0/3 to 3/3; full battery 16/20 to 20/20. Discovery trace: w=1
  ("not") support 12/12, diversity 2, gate 40 > 28, installed as DELETION
  operator with OPREC trig=1 sig=DELETION; w=0 positional confound killed
  by the gate. Falsifiers F1-F5 all pass vs frozen predictions; ablation
  T1 0/3 with the loss localized to the 3 NEG items. 3/3 byte-identical.
  Pure Zag.

**Status: SURVIVES as bounded L2 developmental-language result.** No L3
claim. Retirement specified but uncovered on this battery (disclosed).

## C39. DDES multi-step adaptive intervention planner

Claim: the learner chains discriminating interventions adaptively, each
round conditioned on the previous round's real outcome.

- Prereg: edcefc164 (frozen alone, before implementation)
- Implementation + evidence: 7871ca6d3 (DDES-MULTISTEP-PASS). Verbatim
  DDES derivation core plus frontier generalization over n candidates,
  oneshot and adapt modes. Frozen 3-hypothesis case M1: ONESHOT fails with
  2 survivors; ADAPT eliminates one hypothesis in round 1, derives a
  genuinely different round-2 target conditioned on the reduced survivor
  set, and resolves the winner in round 2. M2 resolves in 2 rounds.
  Regression case A resolves in 1 round under both modes. Termination
  proven (at least one elimination per round when the true world is in the
  candidate set); no plan space enumerated. 3/3 byte-identical. One
  implementation-side VERIFY.sh transcription error (summary totals)
  corrected pre-verdict with no frozen bar altered; disclosed.

**Status: SURVIVES as bounded L2 adaptive causal mechanism.** Researcher
still owns hypothesis format, frozen cases, derivation algorithm, action
vocabulary, and budget. Arena C9 re-entry not done.

## C40. Conditional threshold independent reproduction

Claim: the threshold result reproduces byte-identically from committed
source.

- Prereg: 955106ae5 (frozen alone, before any build or run)
- Reproduction: 07785ac78 (THRESHOLD-REPRO-PASS). Sources extracted via
  git show from d0d296650; all three .zag files BLOB-MATCH committed
  hashes. Every committed number reproduces exactly: R3/R1/FREC md5s
  identical 3/3, all nine .err files zero bytes, P1'' round 0, P2''
  A2-PASS 1 with REUSE_IV 64/64, P3'' DROUND < 4, P4''(a) A1-PASS 1,
  P4''(b) 1/5, P4''(c) 48/64 63/64 40/64, nine audits none firing.
  Full-file cmp of run-1 outputs vs committed originals: byte-identical.
  Diff vs v2 base b0d1749f2 confirms the single functional delta is the
  Tier-1 min slice line.

**Status: REPRODUCTION-CONFIRMS C11 BUILD-PASS.** C11's builder-level
status is unchanged; reproduction is pipeline stage 4 evidence, not
promotion.

## C41. L3C protocol-smuggling adversary

Claim: the v1 revision-form emergence claim is protocol smuggling.

- Phase 1 reproduction: 7fae6a188 (REPRO-PASS; rebuilt from committed
  source at e663864f5, all four outputs byte-identical to committed
  references)
- Phase 2 attack prereg: 7af24029e (frozen before any attack run; protocol
  lines 1-311 proven byte-identical to committed source by diff, only
  main() replaced)
- Phase 2 results: c96875d36
  (L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN). Five families vs frozen
  predictions: (a) conjunction needed, honest fail 2/4; (b) threshold
  needed, eager overfit on first clash then dead end, 3/4; (c) nested
  dispatch, silent dead end (return code 2, vectors not stashed), 4/6;
  (d) underdetermined separator, silent misresolution, held-out 2/4 with
  exactly the predicted silent errors; (e) stash-window forgetting, silent
  misresolution, observed 4/5. construct() always emits the identical
  shape; interp() implements exactly the matching fixed semantics.

**Status: the v1 "emergence" claim is RETRACTED as a C0-A candidate.**
The conditional FORM is researcher-supplied; only (feature, value)
parameters are data-driven: parameter fitting of a supplied template. The
mechanism stands as a clean bounded-L2 fixed-template conditional
constructor with data-driven parameter discovery (see C36 honest scope).
Boundary map: single-level single-feature-equality contradictions only.
Do not widen the fixed template per family; that repeats the downgraded
pattern.

## C42. Valley redesign 2

Claim: a redesigned valley battery produces accepted instances.

- Prereg: 0310c7076 (frozen alone, 108 lines within the 120-line cap)
- Implementation + validation: ea920137b (VALLEY-REDESIGN-FAIL, K2: 0/10
  accepted, 8 required). All 10 candidates passed V1 (genuine score
  valleys; REF-GREEDY halts at len 1) and all 10 failed V3, each with a
  concrete 1- or 2-edit solver found by complete exhaustive check. Three
  architectural lemmas: (1) 3-op solver lemma kills singleton-equality
  and mod-m targets on GENEXEC2; (2) 1-gate lemma kills compositional AND
  valleys; (3) MOD/DIV universality turns inert prologue constants into
  lookup tables. 3/3 byte-identical. Pure Zag.

**Status: BUILD-FAIL (validation gate; not a B/C2/D mechanism failure).**
The valley battery remains void: no accepted instances, no mechanism runs
authorized. Recommended next step: freeze the V3 checker as an oracle and
run a bounded search over (target, path) pairs to decide whether any
instance passes V1-V3, or the V3 bar itself is unsatisfiable.

## C43. L3B residual-growth constructor

Claim: the learner grows base-language programs via generic constructors
(builder level).

- Prereg: c5be6dfb5 (frozen alone, before implementation)
- Implementation: 2fb110ce7 (L3B-GROWTH-PASS). Grown structures are
  base-language programs (op codes 1-5, links, const values) executed by
  the pre-existing frozen interpreter; growth adds no production, no
  semantic case, no branch. KX1: all 512 canonical single branches score
  at most 1/12; TRACE-CREATE fired at LEARN ep3 with preregistered
  relations; HIDDEN 6/6; growth-disabled ablations 0/6; TRACE-RETIRE with
  contradiction reason and v1-to-v2 supersession demonstrated; 3/3
  byte-identical. C0-A audit: interpreter region has no dedicated relation
  cases; interpreter generality confirmed on hand-written programs never
  produced by growth.

**Status: BUILD-PASS (builder-side label only).** The C0-A question
"where are the semantics implemented" is answered mechanically: in the
pre-existing base interpreter; the grown structure is base-language
program data. Toolchain finding: pinned znc miscompiles `as *i32` slice
construction inside functions (allocation aliasing, 8 isolated repros);
u8-backed cells with little-endian pack/unpack are the mandatory
workaround (recorded in ~/AGENTS.md).

## C44. Newcomer-churn revision experiment

Claim: useful-but-not-yet-queried knowledge is churned too aggressively
under memory pressure.

- Prereg: 18fb10434 (frozen alone, before implementation)
- Implementation + results: 5db2712af (CHURN-REVISION-PASS, falsifier
  branch). Control arm: 9/10 never-queried sleepers survived a 30-item
  pressure wave; first-use probe 9/10; compositions through sleeper
  premises 3/4; recovery cost 1 re-learn; foundation 12/12 intact. The
  frozen prediction (0/10 sleepers survive) was wrong. EVICT log mechanism:
  the first eviction creates a revolving-door slot at the lowest
  importance-1 index; every subsequent eviction hits the same slot, so one
  slot absorbs all sustained pressure and spares the other 9 newcomers.
  Per the frozen prereg, the churn hypothesis is rejected for the
  single-wave regime; no policy variant adopted.

**Status: the churn concern is KILLED for the single-wave regime
(falsifier triggered).** The retention policy stands as adequate under
single pressure waves. 3/3 byte-identical. Pure Zag.

## C45. Episodic-pressure experiment

Claim: repeated separated pressure waves bleed never-queried newcomers
that a single wave spares.

- Prereg: 2e0c6ed10 (frozen alone, before implementation)
- Evidence: committed inside 9c6ee8ba8 (concurrent worker's commit;
  message/content mismatch documented); verdict + provenance: 136588de5
  (EPISODIC-PRESSURE-BLEED). All 8 evidence files blob-verified identical
  to the staged evidence; K1 holds structurally (prereg is an ancestor; no
  implementation file existed before the prereg commit). Three separated
  30-item waves with inter-wave earning: sleepers 9/10 to 8/10 to 7/10,
  every frozen prediction matched exactly (per-episode first-eviction
  victims (40,20), (41,20), (42,20); door-slot churn sequences).
  Cumulative 7/10 < 9/10 single-wave baseline. Earned flood 100% survival;
  final probes 3/3; compositions 4/4; foundation 12/12. Mechanism:
  inter-wave earning launders junk to proven status, leaving sleepers as
  the only unproven victims.

**Status: SURVIVES as a bounded L2 mechanism finding.** Provenance note:
implementation and evidence files were staged under the episodic worker's
owned pathspec but landed in concurrent commit 9c6ee8ba8 under another
worker's message; the worker blob-verified all files and documented this
in COMMIT_NOTE.md rather than rewriting history. Do not rewrite history
to fix the mismatch.

## C46. L3B C0-C adversary

Claim: the L3B mechanism achieves open structural form (C0-C).

- Attack prereg: 14a92a69d (frozen alone, before any attack file existed)
- Attack + results: a40aac558 (L3B-C0C-BOUNDARY-EXPOSED). Protocol lines
  1-438 byte-identical to committed l3b.zag at 2fb110ce7 (only main()
  replaced); committed mechanism unmodified. Family A2 (n-squared
  residual): KX-A2 max 1; analyzer fired twice and abstained honestly
  (NO-GROWTH); TRACE-CREATE 0; HIDDEN-A2 0/3. Crux exhibit: hand-built
  MUL(VAR,VAR) via CREATE/CONNECT evaluates to 25 at f0=5, so the
  execution substrate evaluates n-squared while the construction substrate
  can neither detect nor assemble it: open execution, closed construction.
  Family B2 (alternating law): TRACE-CREATE 3, TRACE-RETIRE 2; v3
  content-identical to v1 but rebuilt from scratch (no version memory);
  HIDDEN-B2 3/3, SWITCH 0/6, FINAL-B2 0/2. 3/3 byte-identical.

**Status: KILLED as C0-C.** The fixed analyzer vocabulary and static
single-program growth form are the boundary. The C0-A result (C43) is not
impugned; the mechanism stands as a clean bounded-L2 grower of single
stationary arithmetic residuals inside the vocabulary envelope. Families
A2 and B2 are frozen regression falsifiers for any v2 constructor.

## C47. DDES law-revert adaptive planner

Claim: adaptive intervention handles change-then-revert law families.

- Prereg: bb319407a (frozen alone, before implementation; NAMECHECK.md +
  prereg only)
- Implementation + evidence: 00e9a766e (REVERT-ADAPT-PASS). Time-indexed
  feed protocol; competing rule graphs. R1 change-then-revert: ADAPT
  tracks P0 to h0, P1 to h1, P2 back to h0, re-deriving h0 after the revert
  in 1 round instead of sticking with h1 (4 rounds total, as frozen). R2
  partial-revert: resolves P2 to the d2 variant, not snap-back to h0
  (5 rounds). STATIC demonstrates the frozen C1-pathology (retires h1/h2
  permanently, then misresolves P1 as SINGLE winner=h0). R3 outside-set:
  all four modes DECLARE OUTSIDE-SET and withhold. Regression e0-e4
  reproduce multi-step frozen expectations. One pre-freeze defect
  (ep_winner/ep_round offsets overlapping the STATIC mask) found and fixed
  before the verdict; documented. 3/3 byte-identical.

**Status: SURVIVES as bounded L2.** Candidate graphs are
researcher-supplied; the learner selects and re-selects. No L3 claim.
Complementary to the parallel C1 law-revert attack (prereg 482980e9f).

## C48. Fork battery wave (2026-09-30)

Claim: every enumerated fork passes the frozen battery with discriminating
negative controls.

- Enumeration: 00b62fff9 (manifest committed before results; 80 entries:
  3 LIVE, 77 fixture)
- Results: b4c81d190 (FORKBATTERY-78/80 PASS). 78 PASS, 0 FAIL,
  2 UNTESTABLE (both expected: non-TNN trees rh-pull-1-head,
  rh-pull-2-head). Negative controls discriminate on every fork. Harness
  rebuilt byte-identical to the frozen instrument (sha256 a2e6284c);
  pinned znc 498abcb5 with 0 divergence; all 77 carried fixture SHAs
  re-verified to resolve. Read-only ls-remote shows zero new remote refs.
  Finding: archive branch tnn-native-lab-wave-archive-20260929-1721pdt was
  repointed from enumerated pin 7c11ac5af to dff8c2005 (benign
  content-wise); archive branches should be immutable, re-create rather
  than move. Recommended: automated archive-branch immutability check in
  the enumeration step.

**Status: governance PASS.** This is infrastructure health, not a
capability claim.

## C49. Conditional-threshold red team

Claim: the threshold mechanism's Tier-2 pass is unreachable under its own
beam selection pressure.

- Attack prereg: 15982381c (frozen alone, before family generation and
  testing)
- Attack files: committed inside fd31db230 (concurrent C1 worker's commit;
  message/content mismatch, blobs verified byte-identical to the worker's
  files). Results: REDTEAM-THRESHOLD-BREAK. Family A (Tier-2 condition,
  fam 9: E9 = (C AND Y4) OR ((NOT C) AND Y5), C = (x1 AND x2), composite,
  must be round-built): BREAK. Round 1 culls C from the beam (C_beam=0);
  round 2 pbeam contains C but C is not in the current beam; the Tier-2
  pass requires the condition in both current beam and pbeam (two
  consecutive survivals), but beam selection rewards target-prediction
  accuracy and a discriminative condition (50% predictive) is culled after
  one round. The combiner logic was never reached; the failure is
  selection-vs-persistence and structural. Family B (crowding, fam 8 with 3
  distractors): SURVIVE-THIS-ROUND, 64/64 in 5 IVs, but installed COND
  uses D3 (NOT D) with swapped arms, behaviorally correct via equivalence;
  HAS_D=0, so the A2 reuse criterion fails under crowding. 3/3
  byte-identical. Pure Zag.

**Status: the "tiered" claim is RETRACTED.** THRESHOLD-PASS (C11) stands
as a Tier-1 recalibration only; C11 is narrowed accordingly (C11 itself is
not edited). If Tier-2 conditional discovery is wanted, the fix is in the
selection/persistence interaction, not the combiner's slice math. Do not
rewrite history to fix the fd31db230 message/content mismatch.

---

## UNVERIFIABLE items (paper prose with no committed backing)

1. Any numerical or qualitative claim in the contaminated research paper
   that cites only a "Paper: ... logged (internal log)" commit (for
   example f795823d4, 0c78abd3e, 8e6d1a1ec, 75d7adfc4, 7c82a4144, 1f681e87b,
   6af077852, 19dd863a6, 97782891d, e964682a6, 8eaeff016) as its sole
   support. These commits edit the paper; they do not add primary
   evidence. Each is UNVERIFIABLE until a result commit is found.
2. Beam Design 1 standalone evidence (C04).
3. The /tmp debug build behind the tax-v2 diagnosis (C10); disclosed but
   unaudited, not canonical.
4. Promotion stages not yet run for: C1-CLEAN (baseline, attack, OOD,
   ablation, transfer, red team, audit), threshold calibration (C11,
   stages 4-11), scale-up (C15, stages 4-11). Their verdict labels are not
   SURVIVES.

---

## Ledger tally

- Claims ledgered: 49 (C01-C34 frozen at 714178dd9; C35-C49 appended
  2026-09-30)
- SURVIVES: C03, C06, C19-as-L2 (counted under DOWNGRADED), C20, C21, C23,
  C25, C26, C28, C30, C35 (DDES integration), C37 (learner stress), C38
  (OpScope R1-R4), C39 (DDES multi-step), C45 (episodic-pressure finding),
  C47 (revert-adapt) -> 16 SURVIVES (all bounded L2 or L2+, none L3)
- KILLED: C01 (generic reading), C02, C05, C07, C09, C10, C12, C14, C31,
  C33 (DEVANG2 part), C44 (churn concern, single-wave), C46 (L3B C0-C)
  -> 12 KILLED
- DOWNGRADED: C13, C16, C17, C18, C19, C24, C29 -> 7 DOWNGRADED
- VOID / INVALID: C32 (H-B void; H-C invalid; H-A kill-with-retracted)
- BUILD-PASS: C11 (narrowed by C49 to Tier-1 recalibration), C27, C34
  (figures), C22, C36 (L3C form builder), C43 (L3B growth) -> 6 BUILD-PASS
- BUILD-FAIL: C33 (DEVANG2), C42 (valley redesign-2 validation gate)
- EXPLORATORY: old C1 wave (superseded by C03)
- UNVERIFIABLE: C04 (Design 1)
- RETRACTED: C32 (H-A diagnosis), C41 (v1 emergence claim), C49 (tiered
  claim)
- REPRODUCTION-CONFIRMS: C40 (threshold, confirms C11)
- GOVERNANCE-PASS: C48 (fork battery 78/80)
- L3 achieved anywhere: zero

No em dashes were used in this document (verified with the shell-only
check_no_dash.sh snippet).
