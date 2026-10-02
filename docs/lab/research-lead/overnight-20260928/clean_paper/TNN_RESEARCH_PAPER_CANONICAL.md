# TNN Research Paper (canonical draft, evidence first)

**Status:** draft derived from the evidence-first claim ledger and the
reconstructed canonical state. Not yet canonical itself.
**Derived from:** `canonical_ledger/CLAIM_LEDGER.md` (LEDGER-COMPLETE,
714178dd9, 34 claims) and `canonical_ledger/CANONICAL_STATE.md`
(reconstructed 2026-09-30). **Derivation rule:** every factual claim
below carries a commit pointer. No claim rests on the contaminated
research paper `docs/lab/research-lead/overnight-20260928/
TNN_RESEARCH_PAPER_20260929.md`, which is a contaminated internal log
and is never edited, staged, or committed. Claims in that log that cite
only "Paper: ... logged (internal log)" commits are UNVERIFIABLE and are
deleted here unless re-cited to a result commit from the ledger.

**Style note:** this document contains no em dashes, per loop
documentation rules.

---

## 0. Top line

As of 2026-09-30, on branch `tnn-native-lab`: TNN has a clean broad
lifetime-learning result (C1-CLEAN, C03: SURVIVES) and several genuinely
useful bounded L2 mechanisms. No mechanism has achieved L3
representational invention or the conjunctive Criterion 0 for
learner-authored executable semantics. Ten claims SURVIVE at bounded L2
or L2+, seven are DOWNGRADED, ten are KILLED, and several governance
items await Micah's ruling. The LLM baseline remains PENDING; no
competitive superiority claim is established.

---

## 1. Established results (bounded, with commit citations)

### 1.1 C1-CLEAN: clean lifetime learning (SURVIVES)

Prereg 13e4b1ce3 was frozen alone, before implementation. Freeze
b8d38d9c8 pinned contestant and world-generator hashes. Worlds e0a30377f
(sealed blind seeds: 3 canonical worlds W0/W1/W2, 2 hard exploratory
worlds H0/H1). Result b2b1ec415: C1-CLEAN-PASS. Canonical worlds
63/63 on every world, 3/3 byte-identical repetitions per world (9/9
canonical runs perfect). Hard worlds: H0 66/67 on all three repetitions,
H1 67/67 on all three. Zero Python; frozen hashes unchanged.

Real mechanism boundary (deterministic, disclosed): H0 contains a
law-revert miss. Revision after a reverted law is an open revision
hypothesis, not a passing case. Disclosed protocol blemish: the
hard-world prereg named denominator 64 while the actual denominator was
67; canonical results unaffected. The older C1 wave is EXPLORATORY,
GOVERNANCE-VOID, NOT CANONICAL; C03 supersedes it.

### 1.2 Continuing-learner scale-up (SURVIVES, bounded L2)

Pilot aec4b49e3 (PILOT-CLEAN-PASS); prereg 3e02255f3; result f9b3372d5
(SCALEUP-PASS). One process sustains 65,536 bytes of state with zero
drops, PRESS=1, deterministic. This is bounded L2 C0-D reuse evidence
only; it has not entered the 11-stage promotion pipeline.

### 1.3 Bounded L2 mechanisms that survive

- H-CAUSALEXP-CONSTRUCT: SURVIVES-AS-L2, L3 KILLED at step 11
  (45db44fab). Governance sweep 6b3dd03e8 passes prereg lineage and
  pure-Zag with 3 flags logged.
- H-EXP2: SURVIVES with two downgrades (a3e9d2966: state-selection, not
  experiment-planning; ndiff ranking unvalidated).
- H-EXP3: SURVIVES 4/4 (f8299c388); reachability-aware experiment
  selection addresses the H-EXP2 downgrades.
- H-ROUTER6: SURVIVES 4/4 (0049ad295).
- H-FDCR-UNIFIED8: SURVIVES 51/51, red team SURVIVES 18/18 (11918217a,
  d64a9a025). Earlier UNIFIED7 SURVIVES 47/47 (18dd712a3); UNIFIED6
  DOWNGRADED by red team (a1936a7fd).
- H-INTENT-UNIFIED9: SURVIVES 4/4, red team SURVIVES (3d6a27625,
  55ee07353).
- H-REVISE chain (procedure-revision utilities, bounded L2): R9
  SURVIVES 17/17 (38c847c46); R10 KILLED per K-RV10-4 because the prereg
  premise was incorrect, mechanism sound (aa422610f); R11 SURVIVES
  145/145 (1a2fd99bd); RV11-ADV SURVIVES with 0/4 kills (20f40a4d1). This
  chain survives as revision utilities while the v1 procedure invention
  (section 2.4) still failed criterion 12 at the L3 bar; the two claims
  are distinct.
- Bridge (generic construction replaces recipes): BRIDGE-TESTED (design
  e4f8642fc, prereg 19ce88021, impl ebdc4fd3e), FIX-BUILT-PASS (fix prereg
  75231a87e, impl d920af162),
  TADV5-ACCEPTABLE (83c02efff, re-eval prereg 66aed6805), GREEDY-PASS
  (e96b998c7, greedy prereg a79f842e5), GREEDY-REGRESSION-PASS
  (338eb4241). Status: SURVIVES as bounded L2 generic construction. K=2
  robust only for the current bounded threshold representation; no L3 or
  SURVIVES beyond the L2 reading. T-ADV6 design
  4f9f333cee48dd9bc7c2f5bd0cd1aea9edf1a443 is TADV6-DESIGN-FAIL.
- GOALREVISE (map revision under transfer surprise): REVISE-TESTED
  (cb2a6fdbc, prereg 60e4dcc9a). BUILD-PASS, bounded L2.
- Beam G0 diagnostic: G0-MERGED (2faf4196d, prereg eb0ff7fdf). SURVIVES
  as a diagnostic result (bounded L2).
- SEM: bounded L2+ subsystem, experimental baseline, negative/control
  reference, possibly a useful low-level component (fded44631). Explicitly
  not L3, not general semantic understanding, not representational
  invention. Retireable only through explicit supersession.
- H-MEM8: BUILD-PASS (185cea90b, prereg 3314b8c24). Bounded L2; not
  SURVIVES. H-MEM7 DOWNGRADED (9c41b61d2).

Note on the bridge impl pointer: the bridge builder implementation is
ebdc4fd3e under prereg 19ce88021; do not confuse with the F3 REVISE
builder impl 7009d711c (section 2.1).

### 1.4 Conditional threshold calibration (BUILD-PASS, builder level)

Prereg 7ae3a88fa; result d0d296650 (THRESHOLD-PASS). Verified in the
committed RESULT file: all frozen bars pass, CONDHIT round 0, A2-PASS 1
(reuse 64/64 with D library term), DROUND 1, R1 1/5 no regression, FREC
I1/I2/I3 at or above frozen (48/64, 63/64, 40/64), 3/3 byte-identical,
zero Python, nine audits none firing. This is the working mechanism of
the conditional lane; it has not entered the 11-stage pipeline.

### 1.5 Salt-battery corrections (recorded 2026-09-29)

- H-C kill: INVALID (kill-bar thresholds invented in the results commit
  57d055bbb; bar redefined post-hoc). H-C returns to SURVIVES under its
  actual frozen bar.
- H-B verdict: VOID (bar fit one point below the observed score). Later
  re-freeze 7aeb0cbda: H-B SURVIVES under the re-frozen principled bar.
- H-A kill: stands on the 5 wrong emissions; diagnosis RETRACTED (the
  Eaff arm carried zero uppercasing signal in teaching; H-A correctly
  learned identity from destroyed evidence: an uncalibrated arm, not a
  mechanism boundary). H-A needs a calibrated re-run.

Measurements 48/48, 119/120, 8/8 remain real and deterministic but must
be judged only against principled frozen bars.

### 1.6 Arena measurement figures (apparatus only)

Clean canonical 0.573 (39/68); research-generic 0.691 (47/68, audit
4a98214e0, adapter classification); adapter-inflated 0.779 (53/68,
0e72d7b1b ARENA-CAUSAL v6 BUILD-PASS, C9 1.000). Arena conflict C6:
9211de19e (BUILD-PASS 7/7, 0.632 to 0.676). LLM baseline: PENDING (no
credentials or spending authorized). HUMAN BASELINE NOT MEASURED.
Status: BUILD-PASS figures only. These numbers are components of a
measurement apparatus, not evidence that TNN is preferable to an LLM.

---

## 2. Killed, voided, and downgraded claims (with lineage)

### 2.1 F3 REVISE causal-revision pipeline (generic reading KILLED;
bounded L2 utility SURVIVES)

Full 11-stage lineage, all committed: stage 1 prereg c197e7cd8 (frozen
before implementation); stage 2 implementation 7009d711c (REVISE-PASS);
stage 3 sealed eval: prereg 8cdf0992a, result 1df8addec
(REVISE-SEALED-PASS); stage 4 reproduction: result 7407dd4a7
(REVISE-REPRO-PASS, 33/33 byte-identical) with a disclosed documentation
gap, no standalone step-4 prereg commit located after deep ancestry
search (see governance note in section 5); stage 5 baseline: prereg
4786633c5, result c810d5f55 (REVISE-BASELINE-PASS); stage 6
alternative-explanation attack: prereg 12da75511, result bbdb65c99
(REVISE-ATTACK-SURVIVES); stage 7 OOD: prereg 7bf467d35, result
1125be9bb (REVISE-OOD-PASS); stage 8 ablation: prereg 6dcb1f11b, result
96e22de82 (REVISE-ABLATION-PASS); stage 9 transfer: prereg 7e80e52e6,
result c3c3e3bc8 (REVISE-TRANSFER-PASS); clean pure-Zag re-run prereg
6f95d7b1c, result 53b9a9a27 (REVISE-TRANSFER-PASS, 3/3 byte-identical,
zero Python); stage 10 independent red team: prereg fc57bb738, result
4a2b8ef43 (REVISE-REDTEAM-KILLS); stage 11 governance audit: prereg
62f6a9c31, result 85fe2043c (REVISE-AUDIT-FAIL, A3 fails at S9); clean
step-9 re-audit prereg fc2767234, result 80c237db3
(REVISE-REAUDIT-PASS).

Verdict: REVISE-REDTEAM-KILLS for the generic causal-revision
interpretation. KILLED (generic L3 reading); bounded L2 utility in
confounder-free worlds SURVIVES. Steps 1-9 have clean evidence; the
stage 9 governance blemish was separately remediated.

### 2.2 OpScope (KILLED as word-scoped negation)

Rebuild 837c02c59 (OPSCOPE-REBUILD-PASS); sealed eval 7ca508cd0
(SEALED-PASS); reproduction daafbebbb (OPSCOPE-REPRO-PASS, 3/3
byte-identical); baseline prereg de0db4b64, result 4c4287c50
(OPSCOPE-BASELINE-PASS); alternative-explanation attack prereg eeca946f4
(amendment afde02d2d), result 0add71b64 (OPSCOPE-ATTACK-KILLS,
FA-SUFFIX). The claimed word-scoped negation was suffix suppression
after "not". Bounded L2 suffix-suppression behavior stands as a
refuted-claim component; do not continue promotion under the refuted
claim.

### 2.3 Beam lineage closures

- Beam unified build: KILLED. Prereg 1339b4471 (governance contaminated,
  K3 failed); result dac4a4187 (BEAM-UNIFIED-FAIL). Clean rebuild prereg
  d074eda3d, result fc03664f2 (BEAM-UNIFIED-FAIL). Unified beam does not
  repair the R3 Arm 2 failure.
- Beam G2 refutation-seeking policy: KILLED. Prereg d4485706f, result
  c0babffab (G2-FAIL). R3 Arm 2: 49/64 under G2 versus 52/64 baseline.
  F-FIT, F-DIVERSE-FAIL, F-NODOM, and F-BLOAT fired. The alternative
  explanation "merged, then would have lost anyway" survives. Pure Zag,
  deterministic.
- Beam architecture review: SURVIVES as a review verdict (2135396ce,
  BEAM-REVIEW-COMPLETE). Findings: baseline R3 Arm 2 53/64; unified beam
  52/64; G2 49/64; pairwise composition plus fit and operation tax lacks
  a representation of partial compositional progress; retention and
  selection were not binding constraints. R3 Arm 2 is closed to further
  beam retention/selection tweaks; pivot is conditional-first
  representation-level search. Do not build G1, further
  retention/selection variants, or G4.

Note: this review cites Beam Design 1 at 50/64 versus baseline 53/64.
Design 1 has no locatable prereg, implementation, or result commits and
is UNVERIFIABLE as a standalone committed claim (see section 5.1). It is
excluded from this paper and recorded only in the decisions-pending
list.

### 2.4 Procedure invention and representational expansion (no L3
anywhere)

- Procedure discovery v1 (broadcast-last): DOWNGRADED to bounded L2+
  (850b79ddb; RT2 6e88f3003; H-REVISE c7bfaeba1). Met 11 of 12 L3
  criteria, failing criterion 12 (revision after counterexample), with a
  mathematical impossibility proof against the v1 revision claim. The
  extractor breaks on repeated characters.
- H-PROCLANG1: KILLED as L3; DOWNGRADED to bounded L2+ (adversary
  b5dc77efe, A1/A2/A3 ATTACK-SUCCEEDS; baseline e079d6dd6 under prereg
  ddd90d06b; reproduction 046ab1724).
- REPEXPAND-1: KILLED as L3; strong L2+ stands (adversary 93ce9a09a,
  AX1-AX4 all ATTACK-SUCCEEDS; baseline 2c020b444 BASELINE-MATCHES).
  Learner-selected parameters sat inside researcher-authored semantic
  forms.
- DDES: KILLED as L3 (DDESRT2 b19e0e594, ATTACK-SUCCEEDS: synthesis is
  3-var specific). Bounded DDES utility stands (prereg 7abe1ef66, A1
  678ea4162 L3-GAP-ANALYZED; DDESGEN c04d5610d / 843c45fee FIXABLE, 6/6
  converge on 3/4/5 vars). Integration into the continuing learner is
  pending.

### 2.5 Conditional-first program search (killed attempts)

- Conditional-first v1: KILLED as a general search improvement (design
  e7ca7d83a, prereg 1981c00ea, result c6f6d6787 CONDITIONAL-FAIL).
  Researcher-supplied COND primitive plus Branch-Accuracy Profile
  combiner. Positive: conditional hit in round 0; R3 Arm 2 solved 64/64;
  phase-1 D discovery round 4 to round 1. Failure: FREC I3 regressed
  40/64 to 32/64; BAP-generated conditionals overfit 32-row evidence and
  crowded out stronger binary candidates. The mechanism worked on the
  primary task only (bounded L2).
- Conditional tax v2: KILLED (design 18e0c12a6, prereg 85b4325e5, result
  b0d1749f2 CONDITIONAL-TAX-FAIL). No conditional hit; R3 Arm 2 51/64;
  FREC I3 recovered to frozen 40/64. Diagnosis: fixed Tier-1 minimum
  slice of 4 blocked genuine D (one branch had fewer than 4 observed
  rows). A disclosed uncommitted /tmp debug build using minimum slice 1
  is not canonical evidence (provenance and language use unaudited).

### 2.6 Valley (KILLED)

Prereg cf0c85e78; result 32eb28f3d (VALLEY-FAIL, 0/14 accepted; Family K
instances had two-edit solvers). Trigger monitor 138491e6a
(TRIGGER-NOT-FIRED; checks 2-4 also not-fired: 88111bb65, 098ae71bb).
Two redesign workers failed through output truncation; no valid redesign
exists; the valley redesign gap is open.

### 2.7 C0INTEG Phase B (KILLED)

Result a2896f022 (PHASEB-FAIL); redesign 9f1864f9; pilot prereg
237f7a1ee; pilot result 907ccee49 (PHASEB-PILOT-FAIL, all G1-G5 had 0/5
stable triples). C0-D remains open. No adjacent repair without an
architecture review.

### 2.8 T6 sealed evaluation (DOWNGRADED)

Gate 9ad539fc2 (T6-GATE-READY); sealed 2c982c178 (T6-PASS means the
evaluation completed). Measured: C2 1/12 train, 0/10 held-out; D 9/12
train, 7/10 held-out; B not evaluated (no v2/P-VM mechanism exists); C2
lacks jump opcodes. The sealed PASS certifies the evaluation ran
cleanly; capability PASS on C2 and D did not occur. Purity caveat
preserved at 69730b4ab.

### 2.9 Developmental language (BUILD-FAIL / DOWNGRADED)

- DEVANG2: prereg 402e53d32, result 153e2af8e (DEVANG2 BUILD-FAIL;
  memory-safe, segmentation fails).
- H-SEG2 adversary: prereg 26fc0ee4e, result 0046f4f70 (DOWNGRADED;
  frequency-fragile, long-input crash).

Developmental language remains open.

### 2.10 H-ROUTER7 (DOWNGRADED)

Prereg 8f795a1aa; result 37ce0d271 (DOWNGRADED: capacity defeat of the
total-table headline plus phantom fallback emit; R2 holds).

---

## 3. Open questions

1. Criterion 0 / L3: no mechanism has achieved learner-authored
   executable semantics. The highest-priority frontier remains a generic
   executable representation substrate tested against C0-A through C0-D
   (learner-created persistent state owns semantics; structures grow
   openly and incrementally; frozen machinery handles multiple unforeseen
   forms including a post-freeze independent adversary; the invented
   structure causes cognitive reuse).
2. C1-CLEAN law-revert: attack the deterministic H0 law-revert miss
   (b2b1ec415) with fresh sealed worlds; revision after reverted law is
   the live revision hypothesis.
3. Conditional lane: promote the threshold mechanism (d0d296650) through
   the 11-stage pipeline, starting with independent reproduction.
4. Valley: no valid redesign exists; a narrow design review is needed
   that does not repeat the output-truncation failures.
5. C0INTEG Phase B: C0-D remains open; no adjacent repair without an
   architecture review.
6. DDES: integrate the bounded DDES utility into the continuing learner.
7. Continuing-learner integration: vocabulary, concepts, procedures,
   conflicting evidence, active inquiry, causal learning, memory
   pressure, interference, corrections, and delayed reuse in one process
   with no resets, task labels, or recompilation.
8. Developmental language after DEVANG2 BUILD-FAIL and H-SEG2 downgrade.
9. LLM baseline: PENDING (no credentials or spending authorized).
10. Beam R3 Arm 2 retention/selection lineage: closed (2135396ce); the
    conditional-first representation-level pivot is the live direction.

---

## 4. Decisions pending (Micah)

Evidence only, no decisions. These rulings are Micah's.

1. Beam Design 1 fate. The architecture review 2135396ce cites Design 1
   at 50/64 versus baseline 53/64 on R3 Arm 2, but no prereg,
   implementation, or result commits exist; the claim is UNVERIFIABLE as
   a standalone committed claim. Design 1 is excluded from this paper.
   Options: (a) re-freeze and rerun Design 1 under a committed prereg and
   report clean scores; (b) drop the lineage and treat the review's
   scores as review context only.
2. Strike S7 versus approve the narrowed artifact-touch Python test.
3. MD-SSD-1: keep with UNVERIFIABLE versus re-freeze and rerun.
4. Pull the S11 image pair.
5. Pull S11-AUD.
6. C12: keep in the judge queue versus pull as a confounded stack.
7. Whether Python-mirror-developed logic may ever be adopted. Until he
   rules, no newly Python-mirror-developed logic may be adopted.
8. Promotion priority for C1-CLEAN through stages 4-11 (baseline,
   alternative-explanation attack, OOD, ablation, transfer, red team,
   governance audit), and for the conditional threshold mechanism and
   scale-up.

---

## 5. Governance notes

### 5.1 REVISE step-4 prereg documentation gap (disclosed)

A deep ancestry search on 2026-09-30 covered: the full parent chain
from the sealed result 1df8addec to the reproduction result 7407dd4a7
(a linear window containing only the Phase B pilot prereg 237f7a1ee,
OpScope sealed artifacts 7f24f2f9d, 7ca508cd0, paper log commits, the
trigger monitor 88111bb65, the OpScope repro daafbebbb, and the REVISE
repro result itself); commit-message searches for revise reproduction
preregs; `git log -S` and `git log -G` sweeps for embedded prereg
documents; and inspection of the result commit's file set (two files
only: RESULT_REVISE_REPRO.md and repro_build_run.log, no embedded
prereg document). Conclusion: no standalone step-4 prereg commit exists.
Prereg discipline at REVISE step 4 is undocumented. The step-4 verdict
(REVISE-REPRO-PASS, 33/33 byte-identical) stands on the committed result
7407dd4a7 plus the result file's internal frozen-learner integrity gate
(sha256 checks matching the sealed evaluator's gate) and the
independent-reconstruction method recorded in that file. Flagged, not
backfilled: no prereg was created after the fact.

### 5.2 Paper-derived claim hygiene

Every "Paper: ... logged (internal log)" commit (for example f795823d4,
0c78abd3e, 8e6d1a1ec, 75d7adfc4, 7c82a4144, 1f681e87b, 6af077852,
19dd863a6, 97782891d, e964682a6, 8eaeff016, 339255678, 20769a59a,
ae5c869dd, c7ec5cf39, 0c9e4378e, d7858b10f, 2cf6f5e87, fd97796c1,
c80fdda09, 1e2dc1e31, 9506a9f54) edits the contaminated paper only. They
add no primary evidence and are not cited as claim support in this
paper. Each claim they assert is UNVERIFIABLE until a result commit is
found.

### 5.3 Frozen bars

Preregistration strictly precedes implementation. Frozen bars are never
moved after results. Commits remain local; nothing is pushed without
Micah's explicit approval. Verdicts name the exact frozen bars that
governed them.

---

## 6. Verdict labels used

SURVIVES (10, all bounded L2 or L2+, none L3): C03, C06, C19-as-L2
(downgraded), C20, C21, C23, C25, C26, C28, C30. KILLED (10): C01
(generic reading), C02, C05, C07, C09, C10, C12, C14, C31, C33 (DEVANG2
part). DOWNGRADED (7): C13, C16, C17, C18, C19, C24, C29. VOID / INVALID
/ RETRACTED (C32: H-B void then re-frozen SURVIVES; H-C kill invalid;
H-A diagnosis retracted). BUILD-PASS (4): C11, C22, C27, C34 (figures).
BUILD-FAIL: C33 (DEVANG2). EXPLORATORY: the old C1 wave, superseded by
C03. UNVERIFIABLE: C04 (Beam Design 1) and paper-log-only claims.
L3 achieved anywhere: zero.
