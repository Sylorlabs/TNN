# TNN Clean Research Paper (canonical, evidence first)

**Status:** canonical draft derived only from the evidence-first claim
ledger. Not yet canonical itself.
**Derived from:** `canonical_ledger/CLAIM_LEDGER.md` (49 claims; freeze
714178dd9 for C01-C34, append 71fe67563 for C35-C49) and
`canonical_ledger/CANONICAL_STATE.md` (reconstructed 2026-09-30,
section 6 appended).
**Derivation rule:** every factual claim below carries a commit pointer
and a ledger claim ID. No claim rests on the contaminated research paper
`docs/lab/research-lead/overnight-20260928/
TNN_RESEARCH_PAPER_20260929.md`, which is a contaminated internal log
and is never edited, staged, or committed. Paper-log-only assertions
are UNVERIFIABLE and are deleted here unless re-cited to a result
commit from the ledger.
**Style note:** this document contains no em dashes or en dashes, per
loop documentation rules.

---

## 0. Top line

As of 2026-09-30, on branch `tnn-native-lab`: the ledger holds 49
claims. 16 SURVIVE at bounded L2 or L2+, 12 are KILLED, 7 DOWNGRADED,
6 BUILD-PASS, 2 BUILD-FAIL, 3 RETRACTED, 1 REPRODUCTION-CONFIRMS, 1
GOVERNANCE-PASS, 1 EXPLORATORY, 1 UNVERIFIABLE. TNN has a clean broad
lifetime-learning result (C03) and a measured 8-phase continuing
lifetime (C37), plus a working DDES integration, multi-step, and
law-revert chain at bounded L2 (C35, C39, C47). No mechanism has
achieved L3 representational invention or the conjunctive Criterion 0
for learner-authored executable semantics: L3 achieved anywhere is
zero. Three claims were retracted this cycle: the v1 conditional
emergence claim as a C0-A candidate (C41), the threshold's "tiered"
characterization (C49), and the H-A diagnosis (C32). The LLM baseline
remains PENDING; no competitive superiority claim is established. Six
governance rulings await Micah.

---

## 1. The controlling question and Criterion 0

The standing question the loop answers is: what prevents TNN from
being a genuinely general, continuously learning architecture that we
would choose instead of an LLM. The research mandate is to determine
whether TNN is genuinely progressing toward a new general-purpose
cognitive architecture, not to make TNN look impressive.

Evidence levels used in this paper: L0 storage (records supplied
information; infrastructure, not intelligence evidence), L1 parameter
learning (humans define the representation; TNN fills values), L2
structural learning (TNN constructs new relationships, procedures,
causal structures, or combinations from generic mechanisms; the exact
learned structure did not exist in source), L3 representational
invention (TNN invents or recruits a useful internal representation the
researcher did not enumerate as the solution space, and reuses it). L3
is the primary research target.

For an L3 claim on learner-authored executable semantics, Criterion 0
is conjunctive and all four parts must hold:

- C0-A. Runtime-defined semantics: the semantics of the new cognitive
  object must reside in learner-created persistent state; the source
  must contain only generic execution or construction machinery, with no
  dedicated semantic case for the invented representation. Kill bar: if
  the question "where are the semantics implemented" is answered "in
  this dedicated switch branch written before training", the L3 claim
  dies.
- C0-B. Open structural form: the learner must not select one complete
  answer from a finite researcher-enumerated solution family;
  variable-sized or growing structures are required, and the exact final
  topology must emerge incrementally.
- C0-C. Multiple unforeseen forms: freeze the mechanism, then expose
  it to sealed worlds requiring materially different representations
  (conditional, repeated or recursive, relational coupling, periodic,
  hierarchical composition as functional test descriptions, never
  implemented as dedicated cases); at least one evaluation family is
  designed by an independent adversary after the freeze.
- C0-D. Cognitive reuse: the invented structure must improve transfer,
  prediction, procedure learning, causal inference, memory, planning, or
  sample efficiency; existence alone is insufficient.

Partial Criterion 0 evidence is not L3. Promotion to SURVIVES requires
all eleven stages: committed preregistration, implementation, sealed
evaluation, independent reproduction from committed source,
simple-baseline comparison, alternative-explanation attack, OOD test,
ablation, transfer or reuse test, independent red team, and governance
audit. Builders report BUILD-PASS or BUILD-FAIL only; only the full
pipeline may produce SURVIVES.

---

## 2. Established bounded results (with commit citations)

Every mechanism below survives at bounded L2 or L2+. None is L3.
None satisfies Criterion 0.

### 2.1 C1-CLEAN: clean lifetime learning (C03, SURVIVES)

Prereg 13e4b1ce3 frozen alone before implementation. Freeze b8d38d9c8
pinned contestant and world-generator hashes. Worlds e0a30377f (sealed
blind seeds: 3 canonical W0/W1/W2, 2 hard exploratory H0/H1). Result
b2b1ec415: C1-CLEAN-PASS. Canonical worlds 63/63 on every world, 3/3
byte-identical repetitions per world (9/9 canonical runs perfect).
Hard worlds: H0 66/67 on all three repetitions, H1 67/67 on all three.
Zero Python; frozen hashes unchanged.

Real mechanism boundary (deterministic, disclosed): H0 contains a
law-revert miss. Revision after a reverted law is an open revision
hypothesis, not a passing case. Disclosed protocol blemish: the
hard-world prereg named denominator 64 while the actual denominator
was 67; canonical results unaffected. The older C1 wave is EXPLORATORY,
GOVERNANCE-VOID, NOT CANONICAL; C03 supersedes it.

### 2.2 Continuing learner: scale-up and stress (C15, C37, SURVIVES)

- Scale-up (C15): pilot aec4b49e3 (PILOT-CLEAN-PASS); prereg 3e02255f3;
  result f9b3372d5 (SCALEUP-PASS). One process sustains 65,536 bytes of
  state with zero drops, PRESS=1, deterministic. Bounded L2 C0-D reuse
  evidence only; not promoted through the pipeline.
- Stress battery (C37): prereg 4ca3a7196 frozen alone; addendum e16897bc9
  clarifying kill bar K-S4(b) pre-implementation; implementation plus
  evidence daa9bf2fc (LEARNER-STRESS-PASS). 8-phase lifetime in one
  process with no resets, no task labels, no recompilation: retention 8/8
  through two pressure waves and 22-rule interference; correction uptake
  5/5 with 0/12 collateral and double-correction chains resolving to the
  latest label; corrections survive targeted bombardment 4/4; delayed
  reuse 5/5 routing through corrected premises with zero re-teaching.
  3/3 byte-identical. Mechanism finding: pressure wave 2 churned 19 of
  20 never-queried newcomers through a revolving-door eviction slot;
  new knowledge must earn retention through use. Recorded as the
  pre-DDES baseline for the stress battery.
- Episodic-pressure finding (C45): prereg 2e0c6ed10 frozen alone;
  evidence in 9c6ee8ba8 with verdict and provenance 136588de5
  (EPISODIC-PRESSURE-BLEED). Three separated 30-item waves with
  inter-wave earning: sleepers 9/10 to 8/10 to 7/10, every frozen
  prediction matched exactly; earned flood 100% survival; final probes
  3/3; compositions 4/4; foundation 12/12. Mechanism: inter-wave
  earning launders junk to proven status, leaving sleepers as the only
  unproven victims. Provenance: files landed in concurrent commit
  9c6ee8ba8 under a mismatched message; blob-verified identical and
  documented in COMMIT_NOTE.md; history not rewritten. SURVIVES as a
  bounded L2 mechanism finding.

### 2.3 DDES line: integration, multi-step, revert (C35, C39, C47)

- Integration (C35): prereg c3fecd3c8 frozen alone; implementation
  d9f3871c5; evidence f843188ad (DDES-INTEGRATION-PASS). Base learner
  withholds on the frozen ambiguous causal case; integrated learner
  constructs one discriminating intervention plan, executes once,
  observes an outcome matching exactly one of two hypotheses,
  eliminates the other, resolves correctly. Base causal probes
  byte-identical between modes. 3/3 deterministic. SURVIVES as bounded
  L2 integration. Closes the C31 "integration pending" item at
  mechanism level. Arena C9 not remeasured; the arena gap is closed at
  mechanism level only.
- Multi-step (C39): prereg edcefc164 frozen alone; implementation plus
  evidence 7871ca6d3 (DDES-MULTISTEP-PASS). Frozen 3-hypothesis case M1:
  ONESHOT fails with 2 survivors; ADAPT eliminates one hypothesis in
  round 1, derives a genuinely different round-2 target conditioned on
  the reduced survivor set, and resolves the winner in round 2. M2
  resolves in 2 rounds. Regression case A resolves in 1 round under
  both modes. Termination proven (at least one elimination per round
  when the true world is in the candidate set); no plan space
  enumerated. 3/3 byte-identical. One implementation-side summary
  transcription error corrected pre-verdict with no frozen bar altered;
  disclosed. SURVIVES as bounded L2. The researcher still owns
  hypothesis format, frozen cases, derivation algorithm, action
  vocabulary, and budget. Arena C9 re-entry not done.
- Law-revert (C47): prereg bb319407a frozen alone; implementation plus
  evidence 00e9a766e (REVERT-ADAPT-PASS). Time-indexed feed protocol;
  competing rule graphs. R1 change-then-revert: ADAPT re-derives h0
  after the revert in 1 round instead of sticking with h1. R2
  partial-revert: resolves to the d2 variant, not snap-back to h0.
  STATIC demonstrates the frozen C1-pathology (retires h1/h2
  permanently, then misresolves P1). R3 outside-set: all four modes
  DECLARE OUTSIDE-SET and withhold. One pre-freeze defect found and
  fixed before the verdict; documented. 3/3 byte-identical. SURVIVES as
  bounded L2. Candidate graphs are researcher-supplied; the learner
  selects and re-selects.

### 2.4 Developmental language: OpScope R1-R4 (C38, SURVIVES)

Prereg 51c54e262 frozen alone (K=2 preregistered with written
justification after a prior build measured K=3 unsatisfiable; the
prior K=3 FAIL verdict stands untouched). Implementation plus results
c60bfbe7a (OPSCOPE-R1R4-PASS). Negation fixed: T1 items 109-111 0/3 to
3/3; full battery 16/20 to 20/20. Discovery trace: w=1 ("not") support
12/12, diversity 2, gate 40 > 28, installed as DELETION operator with
OPREC trig=1 sig=DELETION; w=0 positional confound killed by the gate.
Falsifiers F1-F5 all pass vs frozen predictions; ablation drops T1 to
0/3 with the loss localized to the 3 NEG items. 3/3 byte-identical.
Pure Zag. SURVIVES as bounded L2. No L3 claim. Retirement specified
but uncovered on this battery (disclosed).

### 2.5 Bounded L2 mechanism family (SURVIVES)

- H-CAUSALEXP-CONSTRUCT (C19): SURVIVES-AS-L2, L3 KILLED at step 11
  (45db44fab). Governance sweep 6b3dd03e8 passes prereg lineage and
  pure-Zag with 3 flags logged. Counted under SURVIVES (bounded L2)
  and under DOWNGRADED.
- H-EXP2 (C20): SURVIVES with two downgrades (a3e9d2966: state-selection
  not experiment-planning; ndiff ranking unvalidated).
- H-EXP3 (C21): SURVIVES 4/4 (f8299c388); reachability-aware experiment
  selection addresses the H-EXP2 downgrades.
- H-ROUTER6 (C23): SURVIVES 4/4 (0049ad295).
- H-FDCR-UNIFIED8 (C25): SURVIVES 51/51, red team SURVIVES 18/18
  (11918217a, d64a9a025). Earlier UNIFIED7 SURVIVES 47/47 (18dd712a3);
  UNIFIED6 DOWNGRADED by red team (a1936a7fd).
- H-INTENT-UNIFIED9 (C30): SURVIVES 4/4, red team SURVIVES (3d6a27625,
  55ee07353).
- H-REVISE chain (C26, procedure-revision utilities, bounded L2): R9
  SURVIVES 17/17 (38c847c46); R10 KILLED per K-RV10-4 because the prereg
  premise was incorrect, mechanism sound (aa422610f); R11 SURVIVES
  145/145 (1a2fd99bd); RV11-ADV SURVIVES with 0/4 kills (20f40a4d1).
  This chain survives as revision utilities while the v1 procedure
  invention (section 3.5) still failed criterion 12 at the L3 bar; the
  two claims are distinct.
- Bridge (C28, generic construction replaces recipes): BRIDGE-TESTED
  (design e4f8642fc, prereg 19ce88021, impl ebdc4fd3e), FIX-BUILT-PASS
  (fix prereg 75231a87e, impl d920af162), TADV5-ACCEPTABLE (83c02efff,
  re-eval prereg 66aed6805), GREEDY-PASS (e96b998c7, greedy prereg
  a79f842e5), GREEDY-REGRESSION-PASS (338eb4241). SURVIVES as bounded L2
  generic construction. K=2 robust only for the current bounded
  threshold representation; no L3 or SURVIVES beyond the L2 reading.
  T-ADV6 design 4f9f333cee48dd9bc7c2f5bd0cd1aea9edf1a443 is
  TADV6-DESIGN-FAIL. Note: the bridge implementation is ebdc4fd3e
  under prereg 19ce88021; do not confuse with the F3 REVISE builder
  implementation 7009d711c.
- Beam G0 diagnostic (C06): G0-MERGED (2faf4196d, prereg eb0ff7fdf).
  SURVIVES as a diagnostic result (bounded L2).
- SEM (C29): bounded L2+ subsystem, experimental baseline, negative or
  control reference, possibly a useful low-level component (fded44631).
  Explicitly not L3, not general semantic understanding, not
  representational invention. Retireable only through explicit
  supersession.

### 2.6 Salt-battery corrections (C32, recorded 2026-09-29)

- H-C kill: INVALID (kill-bar thresholds invented in the results commit
  57d055bbb; bar redefined post-hoc). H-C returns to SURVIVES under its
  actual frozen bar.
- H-B verdict: VOID (bar fit one point below the observed score). Later
  re-freeze 7aeb0cbda: H-B SURVIVES under the re-frozen principled bar.
- H-A kill: stands on 5 wrong emissions; diagnosis RETRACTED (the Eaff
  arm carried zero uppercasing signal; H-A learned identity from
  destroyed evidence, an uncalibrated arm, not a mechanism boundary).
  Needs a calibrated re-run.
- Measurements 48/48, 119/120, 8/8 remain real and deterministic but
  must be judged only against principled frozen bars.

### 2.7 Arena measurement figures (C34, BUILD-PASS figures only)

Clean canonical 0.573 (39/68); research-generic 0.691 (47/68, audit
4a98214e0); adapter-inflated 0.779 (53/68, 0e72d7b1b ARENA-CAUSAL v6
BUILD-PASS 7/7, 0e72d7b1b, C9 1.000). Arena conflict C6: 9211de19e
(BUILD-PASS 7/7, 0.632 to 0.676). LLM baseline PENDING (no credentials
or spending authorized). HUMAN BASELINE NOT MEASURED. These are
apparatus figures, not superiority evidence; no competitive
superiority claim is established.

---

## 3. Killed claims and what they taught

Each kill below is a finding, not a failure: the bars that killed them
are the same bars that certify the surviving results.

### 3.1 F3 REVISE generic causal revision (C01, KILLED)

Steps 1-9 have clean evidence (prereg c197e7cd8, builder 7009d711c,
sealed 1df8addec, reproduction 7407dd4a7, baseline c810d5f55, attack
bbdb65c99, OOD 1125be9bb, ablation 96e22de82, transfer c3c3e3bc8, and a
pure-Zag clean re-run 53b9a9a27). Stage 10 red team 4a2b8ef43
(REVISE-REDTEAM-KILLS) killed the generic causal-revision
interpretation. Stage 11 audit 85fe2043c (REVISE-AUDIT-FAIL, A3 fails at
S9) was separately remediated by clean step-9 re-audit 80c237db3
(REVISE-REAUDIT-PASS). Standing characterization: bounded L2 utility in
confounder-free worlds only. Documentation gap noted: no separately
committed step-4 prereg was found; the verdict stands on the committed
result 7407dd4a7, flagged.

### 3.2 OpScope word-scoped negation (C02, KILLED)

Rebuild 837c02c59, sealed 7ca508cd0, repro daafbebbb, baseline 4c4287c50,
then alternative-explanation attack 0add71b64 (OPSCOPE-ATTACK-KILLS,
FA-SUFFIX). The claimed word-scoped negation was suffix suppression
after "not". Do not continue promotion under the refuted claim. (The
separate OpScope R1-R4 result C38 is a different, bounded claim.)

### 3.3 Beam lineage (C05, C07, C08)

- Unified beam (C05): prereg 1339b4471 (governance contaminated, K3
  failed), result dac4a4187 (BEAM-UNIFIED-FAIL); clean rebuild prereg
  d074eda3d, result fc03664f2 (BEAM-UNIFIED-FAIL). KILLED. The unified
  beam does not repair the R3 Arm 2 failure.
- G2 refutation-seeking policy (C07): prereg d4485706f; result
  c0babffab (G2-FAIL). R3 Arm 2: 49/64 under G2 vs 52/64 baseline.
  F-FIT, F-DIVERSE-FAIL, F-NODOM, F-BLOAT fired. KILLED. The
  alternative explanation "merged, then would have lost anyway"
  survives. Pure Zag, deterministic.
- Architecture review (C08): 2135396ce (BEAM-REVIEW-COMPLETE). Baseline
  R3 Arm 2 53/64; Design 1 50/64; unified beam 52/64; G2 49/64.
  Pairwise composition plus fit and operation tax lacks a
  representation of partial compositional progress; retention and
  selection were not binding constraints. R3 Arm 2 is closed to further
  beam retention or selection tweaks; the pivot is conditional-first
  representation-level search. Do not build G1, further
  retention or selection variants, or G4. SURVIVES as a review verdict
  (bounded L2 assessment of the lineage).

### 3.4 Conditional v1 and tax v2 (C09, C10, KILLED)

- Conditional-first v1 (C09): design e7ca7d83a; prereg 1981c00ea;
  result c6f6d6787 (CONDITIONAL-FAIL). Positive: conditional hit in
  round 0; R3 Arm 2 solved 64/64; phase-1 D discovery round 4 to round
  1. Failure: FREC I3 regressed 40/64 to 32/64; BAP-generated
  conditionals overfit 32-row evidence. KILLED as a general search
  improvement. Bounded L2 mechanism worked on the primary task only.
- Tax v2 (C10): design 18e0c12a6; prereg 85b4325e5; result b0d1749f2
  (CONDITIONAL-TAX-FAIL). No conditional hit; R3 Arm 2 51/64; FREC I3
  recovered to frozen 40/64. Diagnosis: fixed Tier-1 minimum slice of
  4 blocked genuine D (one branch had fewer than 4 observed rows). An
  uncommitted /tmp debug build using minimum slice 1 was disclosed;
  provenance and language use unaudited. KILLED. The /tmp debug
  disclosure is not canonical evidence.

### 3.5 Procedure invention v1 (C16, DOWNGRADED)

Result 850b79ddb (broadcast-last discovered: SUB(N,C1), index 38).
RT2 6e88f3003 (Family X authoritative 8/8 PASS; semantic 85/1055;
extraction vulnerability CONFIRMED). H-REVISE c7bfaeba1 (L3 criterion
12 KILLED; mathematical impossibility proof against revision).
DOWNGRADED to bounded L2+. Not L3. Met 11 of 12 L3 criteria, failing
criterion 12 (revision after counterexample). Extractor breaks on
repeated characters.

### 3.6 H-PROCLANG1 and REPEXPAND-1 as L3 (C17, C18, KILLED as L3)

- H-PROCLANG1: reproduction 046ab1724; baseline prereg ddd90d06b,
  result e079d6dd6; adversary prereg a0ea62532, result b5dc77efe
  (A1/A2/A3 ATTACK-SUCCEEDS). KILLED as L3; DOWNGRADED to bounded L2+.
- REPEXPAND-1: baseline 2c020b444 (BASELINE-MATCHES); adversary
  93ce9a09a (AX1-AX4 all ATTACK-SUCCEEDS). KILLED as L3; strong L2+
  stands.

### 3.7 DDES as L3 (C31, KILLED as L3)

Prereg 7abe1ef66; A1 678ea4162 (L3-GAP-ANALYZED, all kill bars pass).
DDESGEN prereg c04d5610d, result 843c45fee (FIXABLE; 6/6 converge on
3/4/5 vars). DDESRT2 prereg 8e2a8ecde, result b19e0e594
(ATTACK-SUCCEEDS; synthesis is 3-var specific). KILLED as L3; bounded
DDES utility stands (see C35, C39, C47 for its bounded integration).

### 3.8 SEM as L3 (C29, DOWNGRADED); H-CAUSALEXP as L3 (C19, KILLED as L3)

- SEM: kill battery fded44631 downgraded the L3 claim to L2+.
  Retained as bounded subsystem, experimental baseline, and control
  reference; explicitly not L3, not general semantic understanding,
  not representational invention. Retireable only through explicit
  supersession.
- H-CAUSALEXP: final governance verdict 45db44fab (SURVIVES-AS-L2, L3
  KILLED at step 11). Governance sweep 2026-09-30: 6b3dd03e8 (prereg
  lineage PASS, pure-Zag PASS, reproduced, 3 flags logged).

### 3.9 C0INTEG Phase B (C14, KILLED)

Result a2896f022 (PHASEB-FAIL); redesign 9f1864f9; pilot prereg
237f7a1ee; pilot result 907ccee49 (PHASEB-PILOT-FAIL; all G1-G5 had 0/5
stable triples). C0-D remains open. No adjacent repair without an
architecture review.

### 3.10 Valley (C12, KILLED); valley redesign 2 (C42, BUILD-FAIL)

- C12: prereg cf0c85e78; result 32eb28f3d (VALLEY-FAIL, 0/14 accepted;
  Family K instances had two-edit solvers). Trigger monitor 138491e6a
  (TRIGGER-NOT-FIRED; checks 2-4 also not-fired: 88111bb65,
  098ae71bb). KILLED.
- C42: prereg 0310c7076 (frozen alone, 108 lines within the 120-line
  cap); implementation plus validation ea920137b
  (VALLEY-REDESIGN-FAIL, K2: 0/10 accepted, 8 required). All 10
  candidates passed V1 (genuine score valleys; REF-GREEDY halts at len
  1) and all 10 failed V3, each with a concrete 1- or 2-edit solver
  found by complete exhaustive check. Three architectural lemmas: (1)
  3-op solver lemma kills singleton-equality and mod-m targets on
  GENEXEC2; (2) 1-gate lemma kills compositional AND valleys; (3)
  MOD/DIV universality turns inert prologue constants into lookup
  tables. 3/3 byte-identical. Pure Zag. BUILD-FAIL at the validation
  gate; not a mechanism failure. The valley battery remains void: no
  accepted instances, no mechanism runs authorized.

### 3.11 Churn concern for the single-wave regime (C44, KILLED)

Prereg 18fb10434 frozen alone; implementation plus results 5db2712af
(CHURN-REVISION-PASS, falsifier branch). Control arm: 9/10
never-queried sleepers survived a 30-item pressure wave; first-use
probe 9/10; compositions through sleeper premises 3/4; recovery cost
1 re-learn; foundation 12/12 intact. The frozen prediction (0/10
sleepers survive) was wrong. Mechanism: the first eviction creates a
revolving-door slot at the lowest importance-1 index; every subsequent
eviction hits the same slot, so one slot absorbs all sustained
pressure and spares the other 9 newcomers. Per the frozen prereg, the
churn hypothesis is rejected for the single-wave regime; no policy
variant adopted. 3/3 byte-identical. Pure Zag.

### 3.12 L3B open-form claim (C46, KILLED as C0-C)

Attack prereg 14a92a69d frozen alone before any attack file existed.
Attack plus results a40aac558 (L3B-C0C-BOUNDARY-EXPOSED). Protocol
lines 1-438 byte-identical to committed l3b.zag at 2fb110ce7 (only
main() replaced); committed mechanism unmodified. Family A2 (n-squared
residual): KX-A2 max 1; analyzer fired twice and abstained honestly
(NO-GROWTH); TRACE-CREATE 0; HIDDEN-A2 0/3. Crux exhibit: hand-built
MUL(VAR,VAR) via CREATE/CONNECT evaluates to 25 at f0=5, so the
execution substrate evaluates n-squared while the construction
substrate can neither detect nor assemble it: open execution, closed
construction. Family B2 (alternating law): TRACE-CREATE 3,
TRACE-RETIRE 2; v3 content-identical to v1 but rebuilt from scratch
(no version memory); HIDDEN-B2 3/3, SWITCH 0/6, FINAL-B2 0/2. 3/3
byte-identical. KILLED as C0-C. The fixed analyzer vocabulary and
static single-program growth form are the boundary. The C0-A result
(C43) is not impugned; the mechanism stands as a clean bounded-L2
grower of single stationary arithmetic residuals inside the vocabulary
envelope. Families A2 and B2 are frozen regression falsifiers for any
v2 constructor.

### 3.13 Developmental and capability downgrades

- T6 (C13): gate 9ad539fc2; sealed 2c982c178 (T6-PASS means evaluation
  completed); measured C2 1/12 train, 0/10 held-out; D 9/12 train, 7/10
  held-out; B not evaluated (no v2/P-VM mechanism); C2 lacks jump
  opcodes. DOWNGRADED: the sealed PASS certifies the evaluation ran
  cleanly; capability PASS on C2 and D did not occur. Purity caveat
  preserved at 69730b4ab.
- DEVANG2 (C33): prereg 402e53d32; result 153e2af8e (DEVANG2
  BUILD-FAIL; memory-safe, segmentation fails). H-SEG2 adversary:
  prereg 26fc0ee4e; result 0046f4f70 (DOWNGRADED; frequency-fragile,
  long-input crash). BUILD-FAIL / DOWNGRADED. Developmental language
  remains open.
- H-ROUTER7 (C24): prereg 8f795a1aa; result 37ce0d271 (DOWNGRADED:
  capacity defeat of total-table headline plus phantom fallback emit;
  R2 holds).

---

## 4. Retractions, reproductions, and boundary maps

### 4.1 Retracted claims

1. **v1 conditional emergence as a C0-A candidate (C41, RETRACTED).**
   Phase 1 reproduction 7fae6a188 (REPRO-PASS; rebuilt from committed
   source at e663864f5, all four outputs byte-identical to committed
   references). Phase 2 attack prereg 7af24029e (frozen before any
   attack run; protocol lines 1-311 proven byte-identical to committed
   source by diff, only main() replaced). Phase 2 results c96875d36
   (L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN). Five families vs frozen
   predictions: (a) conjunction needed, honest fail 2/4; (b) threshold
   needed, eager overfit on first clash then dead end, 3/4; (c) nested
   dispatch, silent dead end (return code 2, vectors not stashed), 4/6;
   (d) underdetermined separator, silent misresolution, held-out 2/4
   with exactly the predicted silent errors; (e) stash-window
   forgetting, silent misresolution, observed 4/5. construct() always
   emits the identical shape; interp() implements exactly the matching
   fixed semantics. The conditional FORM is researcher-supplied; only
   (feature, value) parameters are data-driven: parameter fitting of a
   supplied template. The mechanism stands as a clean bounded-L2
   fixed-template conditional constructor with data-driven parameter
   discovery (see C36 honest scope). Boundary map: single-level
   single-feature-equality contradictions only. Do not widen the fixed
   template per family; that repeats the downgraded pattern.
2. **The threshold "tiered" claim (C49, RETRACTED).** Attack prereg
   15982381c frozen alone before family generation and testing. Attack
   files committed inside fd31db230 (concurrent C1 worker's commit;
   message/content mismatch, blobs verified byte-identical to the
   worker's files). Results: REDTEAM-THRESHOLD-BREAK. Family A (Tier-2
   condition, fam 9: E9 = (C AND Y4) OR ((NOT C) AND Y5), C = (x1 AND
   x2), composite, must be round-built): BREAK. Round 1 culls C from
   the beam (C_beam=0); round 2 pbeam contains C but C is not in the
   current beam; the Tier-2 pass requires the condition in both current
   beam and pbeam (two consecutive survivals), but beam selection
   rewards target-prediction accuracy and a discriminative condition
   (50% predictive) is culled after one round. The combiner logic was
   never reached; the failure is selection-vs-persistence and
   structural. Family B (crowding, fam 8 with 3 distractors):
   SURVIVE-THIS-ROUND, 64/64 in 5 IVs, but installed COND uses D3 (NOT
   D) with swapped arms, behaviorally correct via equivalence; HAS_D=0,
   so the A2 reuse criterion fails under crowding. 3/3 byte-identical.
   Pure Zag. THRESHOLD-PASS (C11) stands as a Tier-1 recalibration only;
   C11 is narrowed accordingly (C11 itself is not edited). If Tier-2
   conditional discovery is wanted, the fix is in the
   selection/persistence interaction, not the combiner's slice math.
   Do not rewrite history to fix the fd31db230 message/content
   mismatch.
3. **H-A diagnosis (C32, RETRACTED).** The H-A kill stands on the 5
   wrong emissions; the diagnosis is retracted (the Eaff arm carried
   zero uppercasing signal; H-A learned identity from destroyed
   evidence: an uncalibrated arm, not a mechanism boundary). Needs a
   calibrated re-run.

### 4.2 Builder-level results that are not SURVIVES

- Conditional threshold calibration (C11): BUILD-PASS, builder level
  only (see section 4.1 item 2 for the narrowing to Tier-1
  recalibration). Independent reproduction C40: prereg 955106ae5
  frozen alone before any build or run; reproduction 07785ac78
  (THRESHOLD-REPRO-PASS). Sources extracted via git show from
  d0d296650; all three .zag files BLOB-MATCH committed hashes. Every
  committed number reproduces exactly: R3/R1/FREC md5s identical 3/3,
  all nine .err files zero bytes, P1'' round 0, P2'' A2-PASS 1 with
  REUSE_IV 64/64, P3'' DROUND < 4, P4''(a) A1-PASS 1, P4''(b) 1/5,
  P4''(c) 48/64 63/64 40/64, nine audits none firing. Full-file cmp of
  run-1 outputs vs committed originals: byte-identical. Diff vs v2
  base b0d1749f2 confirms the single functional delta is the Tier-1
  min slice line. Status: REPRODUCTION-CONFIRMS C11 BUILD-PASS. C11's
  builder-level status is unchanged; reproduction is pipeline stage 4
  evidence, not promotion.
- L3C emergent revision-form builder (C36): prereg dc9a91501 frozen
  alone; result e663864f5 (L3C-FORM-PASS). Learner starts without a
  conditional form; contradiction monitor detects identical signatures
  requiring different outputs; learner constructs dispatch structure
  using five generic graph operations. Fixed discriminator discovered
  (f2 == 1) on one family and (f3 == 9) on a second, with zero source
  change. Family 1: 6/6; family 2: 4/4. Construction-disabled ablation
  fails clash cases while retaining training cases. 3/3 byte-identical.
  Prereg contained an arithmetic slip ("12/12 total" vs operative 6 +
  4 = 10); result preserved as 10/10 with disclosure. BUILD-PASS
  (builder level only). Evidence toward C0-A and C0-B; NOT L3, NOT full
  Criterion 0, NOT SURVIVES. The fixed discriminator and protocol may
  be a conditional constructor in disguise; see C41.
- L3B residual-growth constructor (C43): prereg c5be6dfb5 frozen alone;
  implementation 2fb110ce7 (L3B-GROWTH-PASS). Grown structures are
  base-language programs (op codes 1-5, links, const values) executed
  by the pre-existing frozen interpreter; growth adds no production, no
  semantic case, no branch. KX1: all 512 canonical single branches
  score at most 1/12; TRACE-CREATE fired at LEARN ep3 with
  preregistered relations; HIDDEN 6/6; growth-disabled ablations 0/6;
  TRACE-RETIRE with contradiction reason and v1-to-v2 supersession
  demonstrated; 3/3 byte-identical. C0-A audit: interpreter region has
  no dedicated relation cases; interpreter generality confirmed on
  hand-written programs never produced by growth. BUILD-PASS
  (builder-side label only). The C0-A question "where are the
  semantics implemented" is answered mechanically: in the pre-existing
  base interpreter; the grown structure is base-language program data.
  Toolchain finding: pinned znc miscompiles `as *i32` slice
  construction inside functions (allocation aliasing, 8 isolated
  repros); u8-backed cells with little-endian pack/unpack are the
  mandatory workaround (recorded in ~/AGENTS.md).
- H-MEM8 (C22): prereg 3314b8c24; result 185cea90b (H-MEM8 BUILD-PASS;
  builder label only, no SURVIVES claim). H-MEM7 adversary: prereg
  a3203c3d0; result 9c41b61d2 (DOWNGRADED; X-M7-2 inversion, X-M7-3
  lemma falsified).
- GOALREVISE (C27): prereg 60e4dcc9a; result cb2a6fdbc
  (REVISE-TESTED). BUILD-PASS, bounded L2.
- Arena figures (C34): BUILD-PASS figures only; see section 2.7.

### 4.3 Fork battery governance (C48, GOVERNANCE-PASS)

Enumeration 00b62fff9 (manifest committed before results; 80 entries:
3 LIVE, 77 fixture). Results b4c81d190 (FORKBATTERY-78/80 PASS). 78
PASS, 0 FAIL, 2 UNTESTABLE (both expected: non-TNN trees rh-pull-1-head,
rh-pull-2-head). Negative controls discriminate on every fork. Harness
rebuilt byte-identical to the frozen instrument (sha256 a2e6284c);
pinned znc 498abcb5 with 0 divergence; all 77 carried fixture SHAs
re-verified to resolve. Read-only ls-remote shows zero new remote
refs. Finding: archive branch tnn-native-lab-wave-archive-20260929-1721pdt
was repointed from enumerated pin 7c11ac5af to dff8c2005 (benign
content-wise); archive branches should be immutable, re-create rather
than move. Recommended: automated archive-branch immutability check in
the enumeration step. This is infrastructure health, not a capability
claim.

### 4.4 Provenance incidents (2026-09-30 wave)

Shared-branch index races caused crossed commits: 9c6ee8ba8 carries
episodic-pressure files (C45) under the threshold red team message, and
fd31db230 carries threshold red team files (C49) under the C1 worker
message. Content verified blob-identical in both cases; provenance
documented (COMMIT_NOTE.md for C45); history not rewritten. Workers now
use explicit pathspecs with pre-commit status checks.

### 4.5 UNVERIFIABLE items

1. Any numerical or qualitative claim in the contaminated research
   paper that cites only a "Paper: ... logged (internal log)" commit
   (for example f795823d4, 0c78abd3e, 8e6d1a1ec, 75d7adfc4, 7c82a4144,
   1f681e87b, 6af077852, 19dd863a6, 97782891d, e964682a6, 8eaeff016) as
   its sole support. These commits edit the paper; they do not add
   primary evidence. Each is UNVERIFIABLE until a result commit is
   found.
2. Beam Design 1 standalone evidence (C04). Scores (50/64 vs 53/64)
   are usable only as review context, not as evidence.
3. The /tmp debug build behind the tax-v2 diagnosis (C10); disclosed
   but unaudited, not canonical.
4. Promotion stages not yet run for: C1-CLEAN (baseline, attack, OOD,
   ablation, transfer, red team, audit), threshold calibration (C11,
   stages 4-11), scale-up (C15, stages 4-11). Their verdict labels are
   not SURVIVES.

---

## 5. Current frontier state and what would change it

### 5.1 What the evidence establishes today

- TNN has a clean broad lifetime-learning result under a frozen blind
  protocol (C03) and a measured 8-phase continuing lifetime with
  retention, correction, interference, delayed reuse, and memory
  pressure in one process (C37, C45).
- TNN has a working adaptive causal-intervention chain at bounded L2:
  one-shot integration (C35), multi-step chaining with proven
  termination (C39), and law-revert handling with outside-set
  withholding (C47). The candidate graphs remain researcher-supplied;
  the port to learner-constructed candidate graphs is the live causal
  question.
- TNN has a working developmental-language negation operator with a
  white-box discovery trace and falsifiers (C38).
- The conditional lane has a Tier-1 recalibration that reproduces
  byte-identically (C11, C40) but whose Tier-2 pass is structurally
  unreachable under its own beam selection pressure (C49); the "tiered"
  characterization is retracted.
- The representation-invention frontier (Criterion 0) has builder-level
  constructors (C36, C43) whose boundaries are mapped by adversarial
  results (C41, C46): the v1 conditional form was a fixed template with
  data-driven parameters, and the L3B grower has open execution with
  closed construction. C0-A is answered mechanically for L3B (semantics
  in the pre-existing interpreter); C0-C is broken at the fixed
  analyzer vocabulary and static single-program growth form.
- Infrastructure is healthy: 78/80 fork battery with discriminating
  negative controls (C48); pinned toolchain 498abcb5 uniform.

### 5.2 What would change the L3 verdict

An L3 claim requires the conjunctive Criterion 0 plus the 11-stage
promotion pipeline. The specific missing pieces named by the evidence:

1. A constructor whose search space is genuinely program-shaped, not a
   vocabulary fit, with Families A2 and B2 (frozen in C46) as
   regression falsifiers, plus version memory so revision recalls
   rather than rebuilds.
2. A recursive form constructor with compositional predicates, deferred
   construction, revision, and ambiguity handling, with Families A-E
   (frozen in C41) as falsifiers, and an anti-template-widening source
   audit.
3. Learner-constructed candidate graphs for the DDES revert chain
   (the port in progress), replacing researcher-supplied hypothesis
   format.
4. A selection or persistence mechanism for conditional discovery that
   does not cull discriminative conditions before the Tier-2 gate can
   see them, demonstrated by the Tier-2 combiner actually firing (the
   boundary mapping in progress), not by re-labeling Tier-1 success.
5. Composition of the surviving mechanisms into one continuing learner
   (vocabulary, concepts, procedures, conflicting evidence, active
   inquiry, causal learning, memory pressure, interference,
   corrections, delayed reuse) with no resets, task labels, or
   recompilation, measured on the frozen stress battery with a clean
   with/without comparison.
6. An independent red team that fails to trivially break the claim,
   after all of the above.

Until then: L3 achieved anywhere is zero.

### 5.3 Open questions (carried from canonical state, updated)

1. Criterion 0 / L3: unchanged; zero.
2. C1-CLEAN law-revert: attack the deterministic H0 law-revert miss
   with fresh sealed worlds (in flight).
3. Conditional lane: stage 4 done, stage 10 done with the tiered claim
   retired; C11 narrowed to Tier-1 recalibration; boundary mapping in
   flight.
4. Valley: bounded satisfiability search in flight to decide whether
   the V3 bar is satisfiable at all (the battery remains void).
5. C0INTEG Phase B: C0-D remains open; no adjacent repair without an
   architecture review.
6. DDES: integration resolved at mechanism level (C35); learner-
   constructed candidate port in flight; arena C9 re-entry parked.
7. Continuing-learner integration: composition into one learner in
   flight, measured against the pre-DDES baseline.
8. Developmental language: negation SURVIVES (C38); K=2 gate stress
   attack in flight.
9. LLM baseline: PENDING (no credentials or spending authorized).
10. Six governance rulings awaiting Micah's decision (see section 5.4).

### 5.4 Items awaiting Micah's ruling

1. Strike S7 versus approve the narrowed artifact-touch Python test.
2. MD-SSD-1: keep with UNVERIFIABLE versus re-freeze and rerun.
3. Pull the S11 image pair.
4. Pull S11-AUD.
5. C12: keep in the judge queue versus pull as a confounded stack.
6. Whether Python-mirror-developed logic may ever be adopted.

Until he rules, no newly Python-mirror-developed logic may be adopted.

Beam Design 1 disposition (retained from the prior draft): UNVERIFIABLE
as a standalone claim; Micah's call is between re-freeze/rerun and
permanent exclusion from the canonical lineage.

### 5.5 Ledger tally (49 claims)

- SURVIVES: C03, C06, C19-as-L2 (counted under DOWNGRADED), C20, C21,
  C23, C25, C26, C28, C30, C35, C37, C38, C39, C45, C47 -> 16 SURVIVES
  (all bounded L2 or L2+, none L3)
- KILLED: C01 (generic reading), C02, C05, C07, C09, C10, C12, C14,
  C31, C33 (DEVANG2 part), C44 (churn concern, single-wave), C46 (L3B
  C0-C) -> 12 KILLED
- DOWNGRADED: C13, C16, C17, C18, C19, C24, C29 -> 7 DOWNGRADED
- VOID / INVALID: C32 (H-B void; H-C invalid; H-A kill-with-retracted)
- BUILD-PASS: C11 (narrowed by C49 to Tier-1 recalibration), C27, C34
  (figures), C22, C36 (L3C form builder), C43 (L3B growth) -> 6
  BUILD-PASS
- BUILD-FAIL: C33 (DEVANG2), C42 (valley redesign-2 validation gate)
- EXPLORATORY: old C1 wave (superseded by C03)
- UNVERIFIABLE: C04 (Beam Design 1)
- RETRACTED: C32 (H-A diagnosis), C41 (v1 emergence claim), C49
  (tiered claim)
- REPRODUCTION-CONFIRMS: C40 (threshold, confirms C11)
- GOVERNANCE-PASS: C48 (fork battery 78/80)
- **L3 achieved anywhere: zero**

---

**Derivation note:** this paper was generated top-down from
`canonical_ledger/CLAIM_LEDGER.md` (49 claims) and
`canonical_ledger/CANONICAL_STATE.md` only. It supersedes the stale
34-claim draft `TNN_RESEARCH_PAPER_CANONICAL.md` in this directory. The
contaminated internal log `TNN_RESEARCH_PAPER_20260929.md` was not read
for evidence and was not modified. The next ledger append cycle (new
verdicts since 71fe67563) requires this paper to be regenerated before
it is used as a canonical record.
