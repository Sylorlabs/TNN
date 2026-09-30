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

- Claims ledgered: 34
- SURVIVES: C03, C06, C19-as-L2 (counted under DOWNGRADED), C20, C21, C23,
  C25, C26, C28, C30 -> 10 SURVIVES (all bounded L2 or L2+, none L3)
- KILLED: C01 (generic reading), C02, C05, C07, C09, C10, C12, C14, C31,
  C33 (DEVANG2 part) -> 10 KILLED
- DOWNGRADED: C13, C16, C17, C18, C19, C24, C29 -> 7 DOWNGRADED
- VOID / INVALID: C32 (H-B void; H-C invalid; H-A kill-with-retracted)
- BUILD-PASS: C11, C27, C34 (figures), C22 -> 4 BUILD-PASS
- BUILD-FAIL: C33 (DEVANG2)
- EXPLORATORY: old C1 wave (superseded by C03)
- UNVERIFIABLE: C04 (Design 1)
- RETRACTED: C32 (H-A diagnosis)
- L3 achieved anywhere: zero

No em dashes were used in this document (verified with the shell-only
check_no_dash.sh snippet).
