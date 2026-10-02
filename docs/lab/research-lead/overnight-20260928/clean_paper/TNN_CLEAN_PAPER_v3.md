# TNN Clean Research Paper v3 (canonical, evidence first)

**Status:** canonical draft derived only from the evidence-first claim
ledger. Not yet canonical itself.
**Derived from:** `canonical_ledger/CLAIM_LEDGER.md` (63 claims; freeze
714178dd9 for C01-C34, append 71fe67563 for C35-C49, append 8837d2ee0
for C50-C53, append 236a63a5a0 for C54-C63) and
`canonical_ledger/CANONICAL_STATE.md` (reconstructed 2026-09-30,
sections 6, 7, and 8 appended).
**Supersedes:** TNN_CLEAN_PAPER_v2.md (89cf970ee), which is stale for
C54-C63 and stands only as a record against freeze 8837d2ee0. The v2
paper passed governance audit (d66466101) at that freeze (C62).
**Derivation rule:** every factual claim below carries a commit pointer
and a ledger claim ID. No claim rests on the contaminated research paper
`docs/lab/research-lead/overnight-20260928/
TNN_RESEARCH_PAPER_20260929.md`, which is a contaminated internal log
and is never edited, staged, or committed. Paper-log-only assertions
are UNVERIFIABLE and are deleted here unless re-cited to a result
commit from the ledger.
**Style note:** this document contains no em dashes or en dashes, per
loop documentation rules.
**Distribution note:** this paper is an internal record against ledger
freeze 236a63a5a0. It is not for publication.

---

## 0. Top line

As of 2026-09-30, on branch `tnn-native-lab`: the ledger holds 63
claims. 24 SURVIVE at bounded L2 or L2+ and none at L3, 13 are KILLED,
7 DOWNGRADED, 6 BUILD-PASS, 3 BUILD-FAIL, 3 RETRACTED, 3
GOVERNANCE-PASS, 1 REPRODUCTION-CONFIRMS, 1 UNVERIFIABLE, 1 SUPERSEDED.
L3 achieved anywhere: zero.

New since the v2 freeze: learner-constructed causal graphs survive law
change and revert (C54); the OpScope position assumption is proven
load-bearing (C55); the L3B constructor was redesigned at constructor
level toward learner assembly (C56); one continuing learner survives a
law change and revert inside one unbroken lifetime (C57); the threshold
boundary is fully mapped and Tier-2 ambitions for that lineage are
permanently retired (C58); the L3C v2 adversary round is survived this
round only (C59); the L3A trace build fails on process grounds (C60);
fork battery governance passes (C61); the v2 paper passed governance
audit (C62); the 34-claim paper draft is superseded (C63).

The standing architectural directive is now the ONE-SYSTEM RULE
(2026-09-30): new capability must come from experience plus new
learned state, not from new Zag subsystems, modes, bridges, or
handlers. The top-priority research program is the CORE FREEZE
CHALLENGE. No L3 mechanism has achieved learner-authored executable
semantics. The LLM baseline remains PENDING; no competitive superiority
claim is established. Eight governance rulings await Micah.

---

## 1. The controlling question and the honest answer

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
  implemented as dedicated cases); at least one evaluation family must
  be designed by an independent adversary after freeze.
- C0-D. Cognitive reuse: the invented structure must improve transfer,
  prediction, procedure learning, causal inference, memory, planning, or
  sample efficiency; existence alone is insufficient.

Partial Criterion 0 evidence is not L3. Every SURVIVES in this paper is
labeled bounded. L3 achieved anywhere: zero.

An 11-stage frontier promotion pipeline governs new capability claims
(C34 context): committed preregistration, implementation, sealed
evaluation, independent reproduction, simple-baseline comparison,
alternative-explanation attack, OOD test, ablation, transfer or reuse
test, independent red team, governance audit. Only a complete pipeline
may produce SURVIVES; builders report BUILD-PASS or BUILD-FAIL only.

---

## 2. Bounded survivals by lane

Every entry below is SURVIVES as bounded L2 or L2+ unless noted
otherwise. None is L3. None satisfies Criterion 0.

### 2.1 Lifetime learning and the continuing learner

- C03 C1-CLEAN (b2b1ec415). Prereg 13e4b1ce3; freeze b8d38d9c8; worlds
  e0a30377f. Canonical worlds W0-W2 63/63 on every world, 3/3
  byte-identical repetitions per world. Exploratory hard worlds: H0
  66/67 on all three repetitions, H1 67/67. Zero Python; frozen hashes
  unchanged. SURVIVES as the canonical lifetime-learning result. The H0
  law-revert miss is a real deterministic mechanism boundary; the older
  C1 wave is EXPLORATORY, GOVERNANCE-VOID, NOT CANONICAL.
- C15 scale-up (f9b3372d5). Pilot aec4b49e3; prereg 3e02255f3. One
  process, 65,536 bytes of state, zero drops, PRESS=1, deterministic.
  SURVIVES as bounded L2 C0-D reuse evidence.
- C37 continuing-learner stress battery (daa9bf2fc).
  Prereg 4ca3a7196; addendum e16897bc9. 8-phase lifetime, one process,
  no resets, no task labels, no recompilation. Retention 8/8 through
  two pressure waves and 22-rule interference; correction uptake 5/5
  with 0/12 collateral; corrections survive targeted bombardment 4/4;
  delayed reuse 5/5 through corrected premises. 3/3 byte-identical.
  SURVIVES as bounded L2 continuing-learner evidence. Mechanism
  finding: pressure wave 2 churned 19 of 20 never-queried newcomers via
  a revolving-door eviction slot; new knowledge must earn retention
  through use.
- C45 episodic-pressure finding (verdict 136588de5; evidence files
  committed inside 9c6ee8ba8). Prereg 2e0c6ed10. Three separated
  30-item waves with inter-wave earning: sleepers 9/10 to 8/10 to 7/10,
  every frozen prediction matched exactly. SURVIVES as a bounded L2
  mechanism finding. Provenance note preserved: the implementation and
  evidence files were staged under the worker's owned pathspec but
  landed in concurrent commit 9c6ee8ba8 under another worker's message;
  the worker blob-verified all files and documented the mismatch in
  COMMIT_NOTE.md rather than rewriting history. C44 (the single-wave
  churn concern, prereg 18fb10434, result 5db2712af) is KILLED for the
  single-wave regime (falsifier branch: 9/10 sleepers survived).
- C50 recency-guarded earning (6d7681138). Prereg 68c5796d4.
  Inter-episode earning skips the most recent arrival. Sleepers 9/10
  across all three episodes vs the 7/10 episodic baseline (C45) and
  the 9/10 single-wave baseline (C44); zero sleeper evictions in EP2
  and EP3. 3/3 byte-identical. SURVIVES as bounded L2. The
  retention-policy lane is CLOSED; the discipline is ADOPTED as the
  inter-episode rule; no follow-up variants warranted.
- C53 learner integration with DDES planner (d1305bd43). Prereg
  c6288274d. One 32,768-byte state (stress store W[0..8192], DDES
  ledger slice W[16384..32768]), one main(), no resets. P1-P8
  byte-identical to the committed C37 baseline (cmp against
  STRESS_RAW_OUTPUT.txt at daa9bf2fc). New capability: the M1 causal
  ambiguity is encountered DURING the lifetime and resolved by two
  genuinely adaptive interventions (round 1 eliminates h0, round 2
  eliminates h1, winner h2); the outcome persists as three earned
  rule-store facts, all three retrieved after a further 20-item
  pressure wave (3/3), with foundation 8/8 and corrections 2/2 intact.
  The C50 discipline is active in code. SURVIVES as bounded L2. The
  "one continuing learner" goal is approached, not claimed.
- C57 continuing-learner law change and revert (dc20745db). Prereg
  daf4f015d (PREREG-P11). P1-P10 byte-identical to d1305bd43 (C53).
  P11: ADAPT re-derives h0 in 1 round, h1 in 2 rounds, h0 in 1 round,
  total 4; STATIC reproduces the C1 pathology (permanent retirement
  causes h0 misresolution after the change); the re-derived law
  persisted as facts 910/911/912 through a 20-item pressure wave; P11
  causal 3/3, foundation 8/8, corrections 2/2. One 32,768-byte state,
  no reset, pure Zag, 3/3 byte-identical. SURVIVES as bounded L2. One
  continuing learner now covers law change and revert in one lifetime.

### 2.2 Causal lane

- C19 H-CAUSALEXP-CONSTRUCT (45db44fab). Final governance verdict:
  SURVIVES-AS-L2; L3 KILLED at step 11. Governance sweep 6b3dd03e8
  passes prereg lineage and pure-Zag with 3 flags logged. Status:
  DOWNGRADED to bounded L2.
- C35 DDES integration into the continuing learner (f843188ad).
  Prereg c3fecd3c8; impl d9f3871c5. Base learner withholds on the
  frozen ambiguous causal case; integrated learner constructs one
  discriminating intervention plan, executes once, observes an outcome
  matching exactly one of two hypotheses, eliminates the other, and
  resolves correctly. Base causal probes byte-identical between modes.
  3/3 deterministic. SURVIVES as bounded L2 integration. Closes the
  "integration pending" item from C31 at mechanism level; arena C9 has
  not been remeasured. No L3 claim.
- C39 DDES multi-step adaptive intervention planner (7871ca6d3).
  Prereg edcefc164. Frozen 3-hypothesis case M1: ONESHOT fails with 2
  survivors; ADAPT eliminates one hypothesis in round 1, derives a
  genuinely different round-2 target conditioned on the reduced
  survivor set, and resolves the winner in round 2. Termination proven
  (at least one elimination per round when the true world is in the
  candidate set); no plan space enumerated. 3/3 byte-identical. One
  implementation-side VERIFY.sh transcription error corrected
  pre-verdict with no frozen bar altered; disclosed. SURVIVES as
  bounded L2 adaptive causal mechanism. The researcher still owns
  hypothesis format, frozen cases, derivation algorithm, action
  vocabulary, and budget.
- C47 DDES law-revert adaptive planner (00e9a766e). Prereg
  bb319407a. R1 change-then-revert: ADAPT tracks P0 to h0, P1 to h1,
  P2 back to h0, re-deriving h0 after the revert in 1 round (4 rounds
  total, as frozen). R2 partial-revert resolves to the d2 variant, not
  snap-back. STATIC shows the frozen C1-pathology. R3 outside-set: all
  modes DECLARE OUTSIDE-SET and withhold. 3/3 byte-identical.
  SURVIVES as bounded L2. Candidate graphs are researcher-supplied;
  the learner selects and re-selects. No L3 claim.
- C54 causal revert with learner-constructed graphs (da0cd17b6).
  Prereg c09afd95e; transparent pre-implementation amendment
  ab68dd121; result CAUSAL-REVERT-PASS. Learner-constructed graphs now
  survive change and revert: R1 REVISE W0 to k=2 to W1 to k=2 to
  W2=W0, total 2 intervention rounds; R1 REBUILD reaches identical
  winners in 3 rounds reconstructing afresh; R2 permanent-change
  control shows W2=W1 and W2!=W0 (no false snapback); FROZEN controls
  show the intended failure-to-revise pathology. 41/41 checks pass;
  3/3 byte-identical; pure Zag. SURVIVES as bounded L2+. The honest
  ceiling is bounded L2+, not L3: the change-delay, add-rule, and
  remove-rule edit vocabulary remains researcher-supplied. Per the
  ONE-SYSTEM RULE, this is experiment-level revise machinery and
  evidence, not final architecture; revise mode is not canonized.

### 2.3 Procedure, planning, and revision utilities

- C20 H-EXP2 (a3e9d2966). Attack prereg 0c6d62b9c. SURVIVES all frozen
  bars with two DOWNGRADED claims (state-selection not
  experiment-planning; ndiff ranking unvalidated). SURVIVES with
  downgrades (bounded L2).
- C21 H-EXP3 (f8299c388). Reachability-aware experiment selection.
  SURVIVES 4/4 (bounded L2).
- C23 H-ROUTER6 (0049ad295). Prereg 7600ab114. SURVIVES 4/4 (bounded
  L2).
- C26 H-REVISE chain. R9 red team 38c847c46 (SURVIVES 17/17, prereg
  045d5981a); R10 KILLED per K-RV10-4 (aa422610f; prereg premise
  incorrect, mechanism sound); R11 SURVIVES 145/145 (1a2fd99bd, prereg
  36b2fbc71); RV11-ADV SURVIVES with 0/4 kills (20f40a4d1, prereg
  cde064337). SURVIVES as bounded L2 procedure-revision utilities.
  Distinct from C16: the chain survives as revision utilities while
  the v1 procedure invention still failed criterion 12 at the L3 bar.
- C28 bridge (ebdc4fd3e). Prereg 19ce88021; design e4f8642fc. Fix
  d920af162 (prereg 75231a87e); TADV5-ACCEPTABLE (83c02efff, prereg
  66aed6805); greedy passes e96b998c7 and 338eb4241. SURVIVES as
  bounded L2 generic construction. K=2 robust only for the current
  bounded threshold representation.
- C30 H-INTENT-UNIFIED9 (3d6a27625). Red team 55ee07353 (prereg
  1ad5d1d1f). SURVIVES 4/4; red team SURVIVES (bounded L2).
- C25 H-FDCR-UNIFIED8 (11918217a). Red team d64a9a025 (SURVIVES
  18/18). SURVIVES 51/51 (bounded L2).
- C56 L3B constructor v2 (7a1d3265d). Prereg 05620eaa2;
  pre-implementation addendum 197e2547a (arithmetic correction P-B2c
  SWITCH 3/6 to 2/6). Generic 205-program grammar (VAR, constants
  0..8, ADD/MUL/SUB, depth <=2); winning programs assembled through
  generic CREATE/CONNECT; the fixed rel_of analyzer removed rather
  than widened; version archive recalls old structures through
  node-id-preserving dispatch. Square A2: the learner assembled
  MUL(VAR,VAR), hidden 3/3. Alternating B2: Creates=2, dispatches=2,
  SWITCH 2/6, FINAL 1/2 (first post-flip episode unpredictable without
  task labels, disclosed). 3/3 byte-identical; pure Zag. SURVIVES as
  bounded L2. Ceiling is bounded L2; C0-C beyond the two frozen
  families untested. The constructor remains a finite menu under
  adversarial scrutiny; per the lane ruling it will not be expanded
  to 500 or 5,000 entries.
- C59 L3C v2 adversary round (8b82a836a). Prereg 2c0e52739. F1
  depth-3 successive refinement: D1 to D2 to D3 composed correctly,
  4/4. F2 disjunction blind spot: exactly three honest failures, no
  build and no silent misresolution; OR remains a permanent by-design
  blind spot of disc2. F3 default-edge refinement: the previously
  untested repointing path worked, 5/5. 3/3 byte-identical; pure Zag.
  SURVIVES as bounded L2, this round only. One disclosed wording
  mismatch: the prereg described F2 base-rate scoring as 2/4 while the
  implementation reported the equivalent withhold signature 4/4 under
  a different scoring view; mechanism-facing facts and verdict
  unchanged.

### 2.4 Developmental language and conditional diagnostics

- C38 OpScope operator/scope R1-R4 (c60bfbe7a). Prereg 51c54e262
  (K=2 preregistered with written justification; prior K=3 FAIL
  stands untouched). T1 0/3 to 3/3; full battery 16/20 to 20/20.
  Discovery trace: w=1 ("not") support 12/12, gate 40 > 28, installed
  as DELETION operator with OPREC trig=1; w=0 positional confound
  killed by the gate. Falsifiers F1-F5 all pass; ablation T1 0/3 with
  the loss localized to the 3 NEG items. 3/3 byte-identical; pure
  Zag. SURVIVES as bounded L2 developmental-language result. No L3
  claim. Retirement specified but uncovered on this battery
  (disclosed). Valid only within its position-1 battery per C55.
- C55 OpScope displacement (54d3e3ca9). Prereg ae9c3f13e. The true
  negator at utterance position 0 cannot install: cs==cb at every
  check; no operator installs; negation probes 0/3; overall
  no-operator accuracy 17/20. The positional assumption is
  load-bearing: the earlier OpScope result is position-contingent L2,
  not position-general negation learning. 3/3 byte-identical. SURVIVES
  as bounded L2+ boundary-mapping evidence. Governance note preserved
  verbatim: the worker disclosed one inadvertent python3 heredoc
  invocation during setup (placeholder only, no artifact). Disclosure
  does not cure use per the literal pure-Zag rule; the caveat travels
  with this entry. Purity is not asserted as fully clean for this
  lane. No further admission-gate lineage per the lane ruling.
- C06 beam G0 diagnostic (2faf4196d). Prereg eb0ff7fdf. SURVIVES as a
  diagnostic result (bounded L2).
- C08 beam architecture review (2135396ce). BEAM-REVIEW-COMPLETE.
  Baseline R3 Arm 2 53/64; Design 1 50/64; unified beam 52/64; G2
  49/64. Pairwise composition plus fit and operation tax lacks a
  representation of partial compositional progress. SURVIVES as a
  review verdict (bounded L2 assessment of the lineage). R3 Arm 2 is
  closed to further beam retention/selection tweaks; do not build G1,
  further variants, or G4.
- C58 threshold boundary map (ab9a3ccfd). Prereg 2eaa1f122. Both
  frozen predictions were wrong in opposite informative directions.
  A2: even a 15/16-target-predictive composite condition was culled;
  Tier-1 constructs evidence-perfect 16/16 CONDs scoring 9600, floods
  the beam, and removes the condition and arm terminals; Tier-2 fires
  only when redundant and is unreachable when needed. B2: with only
  non-equivalent distractors, the mechanism found the true D term,
  64/64, HAS_D=1; Tier-1 reuse under crowding is robust. 3/3
  byte-identical; pure Zag. SURVIVES as bounded L2 boundary-mapping
  evidence. Final boundary: permanently retire Tier-2 ambitions for
  this lineage; do not build Tier-2b on the old substrate. Per the
  lane ruling, no growing COND library of researcher-authored
  cognitive cases.

---

## 3. Killed claims and what they taught

Thirteen claims are KILLED. Each kill is evidence; kills are reported
as wins, not apologies.

- C01 REVISE generic reading (4a2b8ef43). Stages 1-9 passed the
  pipeline (prereg c197e7cd8, builder 7009d711c, sealed 1df8addec,
  repro 7407dd4a7, baseline c810d5f55, attack bbdb65c99, OOD
  1125be9bb, ablation 96e22de82, transfer c3c3e3bc8); stage 10
  independent red team (prereg fc57bb738) killed the generic
  causal-revision interpretation; stage 11 audit 85fe2043c failed at
  A3/S9 and was separately remediated by the clean step-9 re-audit
  80c237db3. KILLED for the generic reading; bounded L2 utility in
  confounder-free worlds SURVIVES. Lesson: a full pipeline can fail at
  stage 10; the stages matter.
- C02 OpScope word-scoped negation (0add71b64). Rebuild 837c02c59,
  sealed 7ca508cd0, repro daafbebbb, baseline 4c4287c50, then the
  alternative-explanation attack (prereg eeca946f4, amendment
  afde02d2d) showed the claimed word-scoped negation was suffix
  suppression after "not" (FA-SUFFIX). KILLED as word-scoped
  negation. Do not continue promotion under the refuted claim.
- C05 beam unified build (dac4a4187, fc03664f2). Preregs 1339b4471
  (governance contaminated) and d074eda3d. Unified beam does not
  repair the R3 Arm 2 failure. KILLED.
- C07 beam G2 refutation-seeking policy (c0babffab). Prereg
  d4485706f. R3 Arm 2 49/64 under G2 vs 52/64 baseline. KILLED. The
  representation was wrong, not the search policy (C08).
- C09 conditional-first v1 (c6f6d6787). Prereg 1981c00ea; design
  e7ca7d83a. R3 Arm 2 solved 64/64 but FREC I3 regressed 40/64 to
  32/64; BAP-generated conditionals overfit 32-row evidence. KILLED
  as a general search improvement; bounded L2 mechanism worked on the
  primary task only.
- C10 conditional tax v2 (b0d1749f2). Prereg 85b4325e5; design
  18e0c12a6. No conditional hit; the fixed Tier-1 minimum slice of 4
  blocked genuine D. KILLED. An uncommitted /tmp debug build using
  minimum slice 1 was disclosed; it is not canonical evidence.
- C12 valley (32eb28f3d). Prereg cf0c85e78. 0/14 accepted; Family K
  instances had two-edit solvers. Trigger not fired (138491e6a,
  88111bb65, 098ae71bb). KILLED.
- C14 C0INTEG Phase B (a2896f022). Pilot prereg 237f7a1ee; pilot
  result 907ccee49 (all G1-G5 0/5 stable triples). KILLED. C0-D
  remains open; no adjacent repair without an architecture review.
- C31 DDES as L3 (b19e0e594). Attack prereg 8e2a8ecde. Synthesis is
  3-var specific. KILLED as L3; bounded DDES utility stands (and is
  integrated at C35).
- C33 DEVANG2 part (153e2af8e). Prereg 402e53d32. Memory-safe, but
  segmentation fails. BUILD-FAIL. Developmental language remains
  open.
- C44 newcomer-churn concern, single-wave (5db2712af). Prereg
  18fb10434. The frozen prediction (0/10 sleepers survive) was wrong:
  9/10 survived; the first eviction creates a revolving-door slot
  that absorbs all sustained pressure. KILLED for the single-wave
  regime (falsifier triggered); the retention policy stands as
  adequate under single waves.
- C46 L3B C0-C adversary (a40aac558). Attack prereg 14a92a69d. Family
  A2 (n-squared): analyzer abstained honestly, TRACE-CREATE 0,
  HIDDEN-A2 0/3; hand-built MUL(VAR,VAR) evaluates n-squared while
  the construction substrate can neither detect nor assemble it
  (open execution, closed construction). Family B2 (alternating law):
  version memory absent; SWITCH 0/6; FINAL-B2 0/2. KILLED as C0-C.
  The mechanism stands as a bounded-L2 grower of single stationary
  arithmetic residuals inside the vocabulary envelope; families A2
  and B2 are frozen regression falsifiers for any v2 constructor.
- C51 OpScope K=2 DELETION gate (ebd62fe5). Pilot 82262d90c; attack
  prereg 37d4212d. A mid-utterance confound clearing K=2 installs as
  a DELETION operator and destroys novel composition (TEST_ACC 5/20
  vs 20/20 baseline); the gate has no behavioral validation. KILLED
  as a robust operator gate. C38 is not impugned within its battery;
  the Position-0 Lemma was confirmed empirically. Lesson: the battery
  itself was the artifact; the attack showed the battery's
  position-1 "not" may be a hidden researcher choice.

---

## 4. Downgrades

Seven claims were DOWNGRADED rather than killed:

- C13 T6 sealed evaluation (2c982c178). The sealed PASS certifies the
  evaluation ran cleanly; capability PASS on C2 and D did not occur
  (C2 1/12 train, 0/10 held-out; D 9/12 train, 7/10 held-out; B not
  evaluated). Gate 9ad539fc2.
- C16 procedure discovery v1 broadcast-last (850b79ddb). Met 11 of 12
  L3 criteria; criterion 12 (revision after counterexample) KILLED
  by mathematical impossibility proof (c7bfaeba1); RT2 6e88f3003
  found the extractor breaks on repeated characters ("aaa" failed).
  DOWNGRADED to bounded L2+.
- C17 H-PROCLANG1 (b5dc77efe). Attack prereg a0ea62532; A1/A2/A3
  ATTACK-SUCCEEDS. KILLED as L3; DOWNGRADED to bounded L2+.
- C18 REPEXPAND-1 (93ce9a09a). AX1-AX4 all ATTACK-SUCCEEDS; L3
  interpretation KILLED. DOWNGRADED to bounded L2+.
- C19 H-CAUSALEXP-CONSTRUCT (45db44fab). L3 KILLED at step 11.
  DOWNGRADED to bounded L2; SURVIVES-AS-L2.
- C24 H-ROUTER7 (37ce0d271). Prereg 8f795a1aa. Capacity defeat of the
  total-table headline plus phantom fallback emit; R2 holds.
  DOWNGRADED.
- C29 SEM (fded44631). SEM-L3 downgraded to L2+. Retained as a
  bounded subsystem, experimental baseline, and control reference;
  explicitly not L3, not general semantic understanding, not
  representational invention. Retireable only by explicit
  supersession.

---

## 5. Builders, fails, retractions, and governance records

Builders report BUILD-PASS or BUILD-FAIL only; only a complete
11-stage pipeline may produce SURVIVES.

- C11 conditional threshold calibration (d0d296650). Prereg
  7ae3a88fa. All frozen bars pass in the committed RESULT file:
  CONDHIT round 0, A2-PASS 1, DROUND 1, FREC I1/I2/I3 at or above
  frozen (48/64, 63/64, 40/64), 3/3 byte-identical, zero Python, nine
  audits none firing. BUILD-PASS, builder level only; narrowed by
  C49 to a Tier-1 recalibration (C11 itself is not edited). Stages
  4-11 not yet run.
- C22 H-MEM8 (185cea90b). Prereg 3314b8c24. BUILD-PASS (builder label
  only, no SURVIVES claim). H-MEM7 DOWNGRADED (9c41b61d2, prereg
  a3203c3d0): X-M7-2 inversion, X-M7-3 lemma falsified.
- C27 GOALREVISE (cb2a6fdbc). Prereg 60e4dcc9a. REVISE-TESTED.
  BUILD-PASS (bounded L2).
- C34 arena figures. Clean canonical 0.573 (39/68); research-generic
  0.691 (47/68, audit 4a98214e0); adapter-inflated 0.779 (53/68,
  0e72d7b1b ARENA-CAUSAL v6 BUILD-PASS, C9 1.000). LLM baseline
  PENDING (no credentials or spending authorized); HUMAN BASELINE NOT
  MEASURED. BUILD-PASS figures only: components of a measurement
  apparatus, not evidence that TNN is preferable to an LLM.
- C36 L3C emergent revision-form builder (e663864f5). Prereg
  dc9a91501. Learner starts without a conditional form; contradiction
  monitor detects identical signatures requiring different outputs;
  learner constructs dispatch structure using five generic graph
  operations. Family 1 6/6; family 2 4/4; construction-disabled
  ablation fails clash cases. 3/3 byte-identical. Prereg arithmetic
  slip disclosed ("12/12 total" vs operative 6+4=10; preserved as
  10/10). BUILD-PASS, builder level only: evidence toward C0-A and
  C0-B, NOT L3, NOT Criterion 0. The fixed discriminator may be a
  conditional constructor in disguise (see C41).
- C43 L3B residual-growth constructor (2fb110ce7). Prereg c5be6dfb5.
  Grown structures are base-language programs executed by the
  pre-existing frozen interpreter; growth adds no production, no
  semantic case, no branch. KX1: all 512 canonical single branches
  score at most 1/12; TRACE-CREATE fired at LEARN ep3; HIDDEN 6/6;
  growth-disabled ablations 0/6; TRACE-RETIRE with contradiction
  reason demonstrated; 3/3 byte-identical. BUILD-PASS (builder-side
  label only). The C0-A question is answered mechanically: semantics
  live in the pre-existing base interpreter. Toolchain finding:
  pinned znc miscompiles `as *i32` slice construction inside
  functions (allocation aliasing, 8 isolated repros); u8-backed cells
  with little-endian pack/unpack are the mandatory workaround
  (recorded in AGENTS.md).
- C42 valley redesign 2 (ea920137b). Prereg 0310c7076. 0/10 accepted
  at the validation gate (8 required); all 10 passed V1 and failed
  V3 with concrete 1- or 2-edit solvers found by exhaustive check;
  three architectural lemmas committed. BUILD-FAIL at the validation
  gate; the battery remains void.
- C60 L3A trace invention (a6fbee865). Prereg 05898699e. The worker's
  result doc claims BUILD-PASS with strong technical results
  (invention, reuse, C0-A audit A1-A7 pass). BUILD-FAIL on K3 process
  grounds: the worker used a python3 heredoc to patch /tmp scratch
  during diagnostic debugging; disclosure does not cure use per the
  literal pure-Zag rule, so K3 FAILS. Technical findings are
  exploratory only, not canonical evidence; a clean rebuild is in
  progress.
- C40 conditional threshold independent reproduction (07785ac78).
  Prereg 955106ae5. Sources extracted via git show from d0d296650;
  every committed number reproduces exactly; full-file cmp of run-1
  outputs byte-identical. REPRODUCTION-CONFIRMS C11 BUILD-PASS.
  C11's builder-level status is unchanged; reproduction is pipeline
  stage 4 evidence, not promotion.
- Retractions preserved verbatim: C41, the v1 L3C "emergence" claim
  as a C0-A candidate (repro 7fae6a188, attack prereg 7af24029e,
  results c96875d36 L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN: five
  breaking families; construct() always emits the identical shape;
  fixed template with data-driven parameters; boundary map: single
  level single-feature-equality contradictions only); C49, the
  threshold "tiered" characterization (attack prereg 15982381c,
  results REDTEAM-THRESHOLD-BREAK); C32, the H-A diagnosis
  (RETRACTED: the Eaff arm carried zero uppercasing signal; H-A
  learned identity from destroyed evidence, an uncalibrated arm, not
  a mechanism boundary; the kill stands on the 5 wrong emissions).
  C32 is otherwise mixed: H-C kill INVALID (kill-bar thresholds
  invented in the results commit 57d055bbb); H-B verdict VOID then
  SURVIVES under the re-frozen principled bar 7aeb0cbda.
- C48 fork battery wave 2026-09-30 (b4c81d190). Manifest 00b62fff9
  (80 entries, 3 LIVE, 77 fixture; committed before results). 78
  PASS, 0 FAIL, 2 UNTESTABLE (both expected: non-TNN trees
  rh-pull-1-head, rh-pull-2-head). Negative controls discriminate on
  every fork; pinned znc 498abcb5 with 0 divergence. GOVERNANCE-PASS
  (infrastructure health, not a capability claim). Archive-branch
  finding: tnn-native-lab-wave-archive-20260929-1721pdt was repointed
  from 7c11ac5af to dff8c2005 (benign content-wise); archive branches
  must be re-created, not moved.
- C61 fork battery wave 2026-09-30 0750pdt (801736ec4). Manifest
  a3d7a9ed3 (82 entries, 1 LIVE). 80 PASS, 0 FAIL, 2 UNTESTABLE
  (expected non-TNN trees). The automated manifest/driver/result
  consistency gate passed and is now permanent infrastructure.
  GOVERNANCE-PASS.
- C62 paper governance audit v2 (d66466101). PAPER-GOVERNANCE-V2-PASS;
  stage 11 second cycle. All 53 claims checked, labels match, tally
  matches ledger; 166 cited hashes resolve, 20/20 subjects match;
  shell+git only, dash-clean, contaminated paper untouched. Two
  observations logged, no blocking flags. GOVERNANCE-PASS. The v2
  paper remains a valid internal record only against freeze
  8837d2ee0; it is stale for post-freeze verdicts.
- C63 evidence-first paper draft (6425f5a55). SUPERSEDED by the v1
  clean paper (94c30752f) and the v2 clean paper (89cf970ee). Not
  evidence; recorded for provenance only.
- C04 Beam Design 1: UNVERIFIABLE as a standalone committed claim
  (no prereg/impl/result commits located; the architecture review
  2135396ce cites the scores). Scores usable only as review context.

Provenance incidents preserved: shared-branch index races on
2026-09-30 caused crossed commits. 9c6ee8ba8 carries episodic-pressure
files (C45) under the threshold red team message; fd31db230 carries
threshold red team files (C49) under the C1 worker message; 20705ab5a
carries fork-battery and L3C-v2 content under a fork-battery message
with a git note documenting the bundling. Content was blob-verified
identical in each case; provenance documented; history not rewritten.
A fork-battery worker used `git commit --amend` on the shared branch
and amended another worker's commit; the original C1 commit 418b7bc89
is recoverable through reflog. Never amend on the shared branch.

---

## 6. The one-system architectural directive and what it changes

On 2026-09-30 Micah issued the ONE-SYSTEM RULE as a standing
architectural directive. It is not itself a ledger claim; it is the
standing rule that now governs how every ledger claim is read and how
research priority is assigned. This section records it exactly as it
applies to the evidence above.

The rule: TNN must not converge into dozens or hundreds of cognitive
subsystems connected through routers, bridges, special modes, and
task-specific admission gates. Those mechanisms may remain as research
experiments and historical evidence (C19, C23, C28, C30, and the bridge
line remain bounded-L2 evidence), but they are not the desired final
architecture. The desired architecture is ONE general cognitive
substrate: a small generic protected core plus learner-created
cognitive structures plus persistent experience.

A new cognitive capability should primarily require EXPERIENCE leading
to NEW LEARNED STATE or STRUCTURE, not a new Zag subsystem, mode,
bridge, or handler. After a sufficiently general cognitive core is
frozen, new domains should increasingly require zero cognition-source
changes. Capability obtained with zero source delta is far more
architecturally important than another subsystem passing its own
benchmark.

Concretely, every new result must now record: cognition source lines
added; new hardcoded semantic cases; new modes; new bridges; new
task-specific handlers; learner-state structures created. The
capability-source delta should approach zero. The ledger's architecture
notes (preserved above per claim) begin this tracking: C54 records
experiment-level revise machinery with a researcher-supplied edit
vocabulary (not canonized); C55 records an attack battery with no new
mechanism and no new gates; C56 records generic CREATE/CONNECT ops
replacing a removed analyzer with no new hardcoded semantic case; C57
records an extension of the single integrated state with no new
subsystem state formats; C58 records a deletion (Tier-2 lineage
retired); C59 records an adversary round with no new mechanism; C60
records a builder with no canonized architecture.

MODES are architectural smells. CAUSAL_MODE, REVISION_MODE,
LANGUAGE_MODE, MEMORY_MODE, and PROCEDURE_MODE are named as smells.
Revision, inquiry, planning, and memory management should become
generic cognitive operations selected from current learner state,
goals, hypotheses, and evidence. A temporary experimental mode may
isolate a hypothesis but must not silently become canonical
architecture. Consequence for the ledger: C54's causal-revert result is
kept as evidence; revise mode is not canonized as final architecture
(C54 architecture note). The next experiment that derives structural
modifications from prediction failure is the correct frontier.

BRIDGES: do not solve integration by accumulating bridges. If two
mechanisms need a custom bridge, ask first what shared representation
would let them interact directly. Repeated bridge requirements trigger
ARCHITECTURE REVIEW; three custom bridges around the same boundary
block further bridge work until a shared-substrate alternative is
tested. Consequence for the ledger: C28's bounded-L2 bridge
construction remains evidence; it is not the final architecture.

SHARED STRUCTURES: the target is one generic persistent structural
substrate capable of representing concepts, relations, procedures,
causal models, hypotheses, linguistic structures, plans, and memory
policies, differing primarily by learned topology and content rather
than by separate engines. GENERIC OPERATIONS for the fixed core may
include create structure, connect, disconnect, execute, compare,
clone/version, specialize, generalize, retire, retrieve, evaluate
evidence, simulate, and act; the learner determines what structures
these operations create. CREATE_CAUSAL_RULE, CREATE_NEGATION_OPERATOR,
CREATE_ABS, and CREATE_LANGUAGE_CONCEPT are named as things not to add
as final architecture primitives.

The ARCHITECTURE COMPRESSION TEST asks periodically whether two
existing subsystems could be replaced by one generic mechanism.
Deletion is rewarded: a version that deletes 500 lines while retaining
capability is potentially more important than one that adds 2,000
lines and gains one benchmark. Track the number of cognitive
subsystems, modes, bridges, and special semantic cases; the long-term
desired trend is capability up while special-case architecture goes
down. The BEAUTIFUL-ARCHITECTURE CRITERION prefers an architecture
that explains many capabilities with a small number of mechanisms:
maximal generality per mechanism, not maximal modularity. Research
directions are scored on GENERALITY, ARCHITECTURAL COMPRESSION,
LEARNER AUTHORITY, and CAPABILITY SOURCE DELTA. The standing question
for every proposed subsystem: "Why can the existing general
architecture not learn this behavior?"

---

## 7. Open frontiers

The CORE FREEZE CHALLENGE is the top-priority research program.
Freeze one cognitive TNN binary. After freeze: no cognition-source
edits, no recompilation, no new handlers, no new semantic cases, no
new task modes. Expose the same learner sequentially to sealed
adversary-generated worlds requiring: (1) new concepts, (2) new
procedures, (3) causal laws, (4) law changes and reversions, (5)
contradictions, (6) active inquiry, (7) planning, (8) new synthetic
language, (9) new representational structure. The learner must acquire
capabilities through persistent learner-created state. At least two
worlds must be generated by an independent adversary AFTER binary
freeze. Measure: capability source delta, learner state delta,
transfer, retention, interference, compute. No result has yet been
ledgered under this program; it is the program, not evidence.

Other live frontiers (all marked in the ledger as in-flight work, not
evidence):

- Learner-authored causal edit vocabulary (causal_editinvent/): the
  learner must derive its own edit type from prediction failures,
  with an old-vocabulary impossibility proof. This is the correct
  successor to C54, which remains bounded L2+ with a
  researcher-supplied edit vocabulary.
- L3B v2 independent adversary (l3b_v2_adv2/): depth-3 requirements,
  constants outside 0..8, ambiguous dispatch, long churn, archive
  eviction. Successor to C56; if the 205-program constructor proves
  to be a larger finite menu, trigger architecture redesign toward
  incrementally constructed executable state, never menu expansion.
- L3C v2 round-2 adversary (l3c_v2_adv2/): simultaneous sibling-edge
  refinement races; mixed outputs after a D1 to D2 to D3 chain.
  Successor to C59 (survived this round only); the disjunction blind
  spot is permanent by design for disc2.
- Protected-track composite conditional discovery (cond_disc2/):
  A1, A2, B2 frozen as kill bars. Successor to the C58 boundary
  map (Tier-2 retired on the old substrate).
- Continuing-learner P12 developmental-language integration
  (learner_dev/): P1-P11 byte-identical, position restriction
  explicit. Successor to C57; the lane ruling for C55 applies (no
  gate lineage; the question is what general semantic-learning
  process learns position-independent negation).
- OpScope cross-context behavioral validation (opscope_behav/):
  validation before operator installation. Successor to C51/C55; one
  discriminating hypothesis, not a new gate lineage.
- HypD v3 (hypd_v3/): fixes search dilution and cross-task niche
  poisoning. Successor to C52's exploratory diagnosis; niche 17570
  occupancy as an explicit falsification check.
- Valley bounded satisfiability search (valley_satsuch/): return
  FOUND or UNSATISFIABLE for the V3 bar. Successor to C42.
- TNN-vs-LLM arena with a capable non-crippled baseline: 15
  capabilities, honest resource charging, capability curves rather
  than a superiority declaration. LLM baseline PENDING; no
  credentials or spending authorized. Arena figures (C34) are
  apparatus only.
- Architecture compression: the periodic test from section 6, with
  deletion rewarded.
- L3A trace invention: clean rebuild after C60's process FAIL; the
  technical findings (invention, reuse, C0-A A1-A7) are exploratory
  only pending the rebuild.

The continuing learner is HIGH PRIORITY: use the current integration
result as scaffolding (C53, C57); gradually eliminate independent
subsystem state formats; the target is one learner-owned structural
workspace rather than several engines sharing one byte array.

---

## 8. Decisions pending for Micah

The following items await Micah's ruling. They are not decided here.

1. Strike S7 versus approve the narrowed artifact-touch Python test.
2. MD-SSD-1: keep with UNVERIFIABLE versus re-freeze and rerun.
3. Pull the S11 image pair.
4. Pull S11-AUD.
5. Keep C12 in the judge queue versus pull it as a confounded stack.
6. Whether Python-mirror-developed logic may ever be adopted. Until
   Micah rules, no newly Python-mirror-developed logic may be
   adopted.
7. Beam Design 1 (C04): re-freeze and rerun versus exclude
   permanently from the canonical lineage.
8. L3C-v2 Family D arithmetic slip: transparently amend k=3 to k=2
   versus change the clash vector if three competitors were intended.
   Until Micah rules, retain L3C-V2-PARTIAL; do not reinterpret it as
   PASS.

---

## 9. Standing governance orders referenced

- Never edit, stage, or commit
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`.
  It is a contaminated internal log, not canonical evidence.
- No L3 claim anywhere is established. Zero SURVIVES at L3 or
  Criterion 0.
- Preregistration strictly precedes implementation; frozen bars are
  never moved after results. Never move, reinterpret, or weaken a
  frozen bar after results.
- Preserve RETRACTED, SUPERSEDED, INVALID, VOID, and UNVERIFIABLE
  exactly.
- Commits remain local on `tnn-native-lab`. Nothing is pushed without
  Micah's explicit approval.

**End of TNN Clean Research Paper v3. Derived only from the 63-claim
ledger at 236a63a5a0. L3 achieved anywhere: zero.**
