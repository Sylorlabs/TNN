# Canonical Scientific State: TNN Native Lab (reconstructed)

**Date:** 2026-09-30
**Branch:** tnn-native-lab
**Author:** Canonical Reconstruction Archivist
**Basis:** committed evidence only. See `CLAIM_LEDGER.md` in this directory
for per-claim commit pointers. This document replaces the 2026-09-29
07:56 PDT canonical state (commit d24eda8bd) and is derived only from
committed preregs, ancestry, raw results, reproductions, adversaries, and
governance audits. It does not use the contaminated research paper.

**Style note:** this document contains no em dashes, per loop
documentation rules.

---

## 1. Established results

### 1.1 Clean lifetime learning: C1-CLEAN (SURVIVES)

Prereg 13e4b1ce3; freeze b8d38d9c8; worlds e0a30377f; result b2b1ec415
(C1-CLEAN-PASS). Canonical worlds W0/W1/W2: 63/63 on every world, 3/3
byte-identical repetitions per world (9/9 canonical runs perfect).
Exploratory hard worlds: H0 66/67 on all three repetitions, H1 67/67 on
all three. Zero Python; frozen contestant and world-generator hashes
unchanged. This is the canonical lifetime-learning result; the older C1
wave is EXPLORATORY, GOVERNANCE-VOID, NOT CANONICAL.

Mechanism boundary (real, deterministic): H0 contains a law-revert miss.
Revision after a reverted law is an open revision hypothesis, not a
passing case.

### 1.2 REVISE pipeline (KILLED generic reading; bounded L2 utility SURVIVES)

Steps 1-9 have clean evidence: prereg c197e7cd8, builder 7009d711c,
sealed 1df8addec, reproduction 7407dd4a7, baseline c810d5f55, attack
bbdb65c99, OOD 1125be9bb, ablation 96e22de82, transfer c3c3e3bc8, and a
pure-Zag clean re-run 53b9a9a27. Stage 10 red team 4a2b8ef43
(REVISE-REDTEAM-KILLS) killed the generic causal-revision
interpretation. Stage 11 audit 85fe2043c (REVISE-AUDIT-FAIL, A3 fails at
S9) was separately remediated by clean step-9 re-audit 80c237db3
(REVISE-REAUDIT-PASS).

Standing characterization: bounded L2 utility in confounder-free worlds.
No L3, no Criterion 0, no SURVIVES beyond the bounded reading.

### 1.3 OpScope (KILLED as word-scoped negation)

Rebuild 837c02c59, sealed 7ca508cd0, repro daafbebbb, baseline
4c4287c50, then alternative-explanation attack 0add71b64
(OPSCOPE-ATTACK-KILLS, FA-SUFFIX). The claimed word-scoped negation was
suffix suppression after "not". Do not continue promotion under the
refuted claim.

### 1.4 Scale-up (SURVIVES, bounded L2)

Pilot aec4b49e3 (PILOT-CLEAN-PASS); prereg 3e02255f3; result f9b3372d5
(SCALEUP-PASS). One process, 65,536 bytes state, zero drops, PRESS=1,
deterministic. Bounded L2 C0-D reuse evidence only.

### 1.5 Bounded L2/L2+ mechanisms (SURVIVES, none L3)

- H-CAUSALEXP-CONSTRUCT: SURVIVES-AS-L2, L3 KILLED (45db44fab); governance
  sweep 6b3dd03e8 passes prereg lineage and pure-Zag with 3 flags logged.
- H-EXP2: SURVIVES with two downgrades (a3e9d2966).
- H-EXP3: SURVIVES 4/4 (f8299c388).
- H-ROUTER6: SURVIVES 4/4 (0049ad295).
- H-FDCR-UNIFIED8: SURVIVES 51/51, red team SURVIVES 18/18 (11918217a,
  d64a9a025).
- H-INTENT-UNIFIED9: SURVIVES 4/4, red team SURVIVES (3d6a27625,
  55ee07353).
- H-REVISE chain: R9 SURVIVES 17/17 (38c847c46); R10 KILLED on prereg
  error with mechanism sound (aa422610f); R11 SURVIVES 145/145
  (1a2fd99bd); RV11-ADV SURVIVES 0/4 kills (20f40a4d1).
- Bridge: BRIDGE-TESTED (ebdc4fd3e), FIX-BUILT-PASS (d920af162),
  TADV5-ACCEPTABLE (83c02efff), GREEDY-PASS (e96b998c7),
  GREEDY-REGRESSION-PASS (338eb4241). K=2 robust only for the current
  bounded threshold representation.
- GOALREVISE: REVISE-TESTED (cb2a6fdbc).
- Beam G0 diagnostic: G0-MERGED (2faf4196d).
- SEM: bounded L2+ subsystem (fded44631); retireable only by explicit
  supersession.
- Procedure discovery v1: bounded L2+, 11 of 12 L3 criteria, criterion 12
  failed (850b79ddb, 6e88f3003, c7bfaeba1).
- H-MEM8: BUILD-PASS (185cea90b); H-MEM7 DOWNGRADED (9c41b61d2).

### 1.6 Conditional threshold calibration (BUILD-PASS, builder level)

Prereg 7ae3a88fa; result d0d296650 (THRESHOLD-PASS), verified in the
committed RESULT file: all frozen bars pass, CONDHIT round 0, A2-PASS 1,
DROUND 1, FREC at or above frozen, 3/3 byte-identical, zero Python, nine
audits none firing. This is the working mechanism of the conditional
lane; it has not entered the 11-stage pipeline.

### 1.7 Salt-battery corrections

- H-C kill: INVALID. H-C reverts to SURVIVES under its actual frozen bar.
- H-B verdict: VOID, then SURVIVES under the re-frozen principled bar
  (7aeb0cbda).
- H-A kill: stands on 5 wrong emissions; diagnosis RETRACTED (uncalibrated
  arm, not a mechanism boundary); needs a calibrated re-run.

### 1.8 Arena measurement figures

Clean canonical 0.573 (39/68); research-generic 0.691 (47/68, audit
4a98214e0); adapter-inflated 0.779 (53/68, 0e72d7b1b). LLM baseline
PENDING. HUMAN BASELINE NOT MEASURED. These are apparatus figures, not
superiority evidence.

---

## 2. Killed and voided claims (with lineage)

- REVISE generic causal revision: KILLED at stage 10 (4a2b8ef43).
- OpScope word-scoped negation: KILLED at attack (0add71b64).
- Beam unified: KILLED (dac4a4187, fc03664f2).
- Beam G2: KILLED (c0babffab).
- Conditional-first v1: KILLED (c6f6d6787). Conditional tax v2: KILLED
  (b0d1749f2).
- Valley: KILLED (32eb28f3d); trigger not fired (138491e6a).
- Phase B: KILLED (a2896f022); pilot KILLED (907ccee49).
- Procedure v1 as L3: DOWNGRADED at criterion 12 (c7bfaeba1).
- H-PROCLANG1 as L3: KILLED (b5dc77efe). REPEXPAND-1 as L3: KILLED
  (93ce9a09a). DDES as L3: KILLED (b19e0e594).
- SEM as L3: DOWNGRADED to L2+ (fded44631).
- H-CAUSALEXP as L3: KILLED at step 11 (45db44fab).
- T6 capability: DOWNGRADED; sealed PASS means the evaluation ran, not that
  C2/D passed (2c982c178).
- DEVANG2: BUILD-FAIL (153e2af8e). H-SEG2: DOWNGRADED (0046f4f70).
- H-ROUTER7: DOWNGRADED (37ce0d271).
- Old C1 wave: EXPLORATORY, GOVERNANCE-VOID, SUPERSEDED by C1-CLEAN.
- H-C kill: INVALID. H-B verdict: VOID then re-frozen. H-A diagnosis:
  RETRACTED.
- Beam R3 Arm 2 retention/selection lineage: closed by architecture review
  2135396ce; do not build G1, retention/selection variants, or G4.

---

## 3. Open questions

1. Criterion 0 / L3: no mechanism has achieved learner-authored executable
   semantics. The highest-priority frontier remains a generic executable
   representation substrate tested against C0-A through C0-D.
2. C1-CLEAN law-revert: attack the deterministic H0 law-revert miss with
   fresh sealed worlds; revision after reverted law is the live revision
   hypothesis.
3. Conditional lane: promote the threshold mechanism (d0d296650) through
   the 11-stage pipeline starting with independent reproduction.
4. Valley: no valid redesign exists; a narrow design review is needed that
   does not repeat the output-truncation failures.
5. C0INTEG Phase B: C0-D remains open; no adjacent repair without an
   architecture review.
6. DDES: integrate the bounded DDES utility into the continuing learner.
7. Continuing learner integration: vocabulary, concepts, procedures,
   conflicting evidence, active inquiry, causal learning, memory pressure,
   interference, corrections, and delayed reuse in one process with no
   resets, task labels, or recompilation. P11 law-change-and-revert now
   SURVIVES as bounded L2 in the same lifetime (C57); P12
   developmental-language integration is in flight.
8. Developmental language: after DEVANG2 BUILD-FAIL and H-SEG2 downgrade.
   OpScope negation is position-contingent L2 (C55); position-general
   negation is killed. Cross-context behavioral validation is in
   flight.
9. LLM baseline: PENDING (no credentials or spending authorized).
10. Six governance rulings awaiting Micah's decision (see section 4).

---

## 4. Items awaiting Micah's ruling

1. Strike S7 versus approve the narrowed artifact-touch Python test.
2. MD-SSD-1: keep with UNVERIFIABLE versus re-freeze and rerun.
3. Pull the S11 image pair.
4. Pull S11-AUD.
5. C12: keep in the judge queue versus pull as a confounded stack.
6. Whether Python-mirror-developed logic may ever be adopted.

Until he rules, no newly Python-mirror-developed logic may be adopted.

---

## 5. Governance standing orders referenced

- Never edit, stage, or commit
  `docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`.
  It is a contaminated internal log, not canonical evidence. This document
  and the claim ledger are the canonical records; they rest on committed
  preregs, ancestry, raw results, reproductions, adversaries, and
  governance audits.
- No L3 claim anywhere is established. Zero SURVIVES at L3 or Criterion 0.
- Preregistration strictly precedes implementation; frozen bars are never
  moved after results.
- Commits remain local. Nothing is pushed without Micah's explicit
  approval.

---

## 6. Post-ledger verdicts (2026-09-30; ledger appendix C35-C49)

Appended to CLAIM_LEDGER.md after the 714178dd9 freeze. No C01-C34
entry was modified. L3 achieved anywhere: still zero.

### 6.1 DDES line: integration, multi-step, revert (C35, C39, C47)

- C35 DDES-INTEGRATION-PASS (prereg c3fecd3c8, impl d9f3871c5, evidence
  f843188ad): SURVIVES as bounded L2 integration. Closes the C31
  "integration pending" item at mechanism level. Arena C9 not remeasured.
- C39 DDES-MULTISTEP-PASS (prereg edcefc164, impl 7871ca6d3): SURVIVES as
  bounded L2. Adaptive chaining resolves the frozen 3-hypothesis case in
  2 rounds where one-shot fails; termination proven.
- C47 REVERT-ADAPT-PASS (prereg bb319407a, impl 00e9a766e): SURVIVES as
  bounded L2. Adaptive re-derivation after law revert in 1 round;
  partial-revert resolves to the new variant; STATIC shows the frozen
  C1-pathology; outside-set declares and withholds.

Open question 6 (DDES integration) is resolved at mechanism level.
Arena C9 re-entry remains parked.

### 6.2 Continuing learner: stress, churn, episodic pressure
(C37, C44, C45)

- C37 LEARNER-STRESS-PASS (prereg 4ca3a7196, addendum e16897bc9, impl
  daa9bf2fc): SURVIVES as bounded L2. 8-phase lifetime: retention 8/8,
  correction 5/5 with 0/12 collateral, interference 8/8, delayed reuse
  5/5 through corrected premises. Revolving-door eviction finding.
- C44 CHURN-REVISION-PASS (prereg 18fb10434, impl 5db2712af): the churn
  concern is KILLED for the single-wave regime (falsifier triggered;
  9/10 sleepers survive).
- C45 EPISODIC-PRESSURE-BLEED (prereg 2e0c6ed10, evidence in 9c6ee8ba8,
  verdict 136588de5): SURVIVES as a bounded L2 mechanism finding.
  Sleepers 9/10 to 8/10 to 7/10 across episodes; inter-wave earning
  launders junk to proven status. Provenance note: files landed in a
  concurrent commit under a mismatched message; blob-verified and
  documented in COMMIT_NOTE.md; history not rewritten.

Open question 7 (continuing-learner integration) advances: stress,
correction, interference, delayed reuse, and memory pressure are now
measured in one process. The recency-guarded earning terminal experiment
is in flight.

### 6.3 Developmental language: OpScope R1-R4 (C38)

- C38 OPSCOPE-R1R4-PASS (prereg 51c54e262, impl c60bfbe7a): SURVIVES as
  bounded L2. Negation fixed: T1 0/3 to 3/3, battery 16/20 to 20/20;
  falsifiers F1-F5 pass; DELETION operator discovered with white-box
  OPREC trace. K=2 preregistered with justification; prior K=3 FAIL
  stands.

Open question 8 (developmental language) advances on negation. The K=2
gate stress attack is in flight.

### 6.4 Conditional lane: reproduction and red team (C40, C49)

- C40 THRESHOLD-REPRO-PASS (prereg 955106ae5, repro 07785ac78):
  REPRODUCTION-CONFIRMS C11 BUILD-PASS. Every committed number
  byte-identical from committed source.
- C49 REDTEAM-THRESHOLD-BREAK (attack prereg 15982381c, files in
  fd31db230): the "tiered" claim is RETRACTED. The Tier-2 pass is
  unreachable under beam selection pressure (selection-vs-persistence,
  structural); THRESHOLD-PASS stands as a Tier-1 recalibration only.
  Crowding: SURVIVE-THIS-ROUND with correct-via-equivalent caveat.

Open question 3 (conditional lane pipeline): stage 4 done; stage 10 done
with the tiered claim retired. C11 narrowed, not edited.

### 6.5 L3C line: builder and adversary (C36, C41)

- C36 L3C-FORM-PASS (prereg dc9a91501, result e663864f5): BUILD-PASS,
  builder level only. Evidence toward C0-A/C0-B; NOT L3, NOT Criterion 0.
  Prereg arithmetic slip disclosed (10/10 preserved).
- C41 L3C-ADVERSARY-PROTOCOL-SMUGGLING-PROVEN (repro 7fae6a188, attack
  prereg 7af24029e, results c96875d36): the v1 "emergence" claim is
  RETRACTED as a C0-A candidate. Fixed template with data-driven
  parameters; five breaking families; boundary map committed.

Open question 1 (Criterion 0 / L3) is unchanged: zero. Protocol v2
(recursive constructor) is in flight with families A-E as frozen
falsifiers.

### 6.6 L3B line: builder and adversary (C43, C46)

- C43 L3B-GROWTH-PASS (prereg c5be6dfb5, impl 2fb110ce7): BUILD-PASS,
  builder-side label only. C0-A answered mechanically (semantics in the
  pre-existing interpreter). Toolchain finding recorded in ~/AGENTS.md:
  pinned znc miscompiles `as *i32` slice construction in functions;
  u8-backed cells mandatory.
- C46 L3B-C0C-BOUNDARY-EXPOSED (attack prereg 14a92a69d, attack
  a40aac558): KILLED as C0-C. Open execution, closed construction
  (n-squared); revision churn with no version memory (alternating law).
  C43 not impugned.

Open question 1 unchanged. Constructor-level v2 redesign is in flight.

### 6.7 Valley redesign 2 (C42)

- C42 VALLEY-REDESIGN-FAIL (prereg 0310c7076, impl ea920137b):
  BUILD-FAIL at the validation gate (0/10 accepted). Three architectural
  lemmas committed. Battery remains void.

Open question 4 (valley): bounded satisfiability search in flight to
decide whether the V3 bar is satisfiable at all.

### 6.8 Fork battery governance (C48)

- C48 FORKBATTERY-78/80 PASS (enum 00b62fff9, results b4c81d190):
  governance PASS. 78 PASS, 0 FAIL, 2 UNTESTABLE (expected). Harness
  byte-identical; toolchain uniform. Archive-branch repoint finding
  (tnn-native-lab-wave-archive-20260929-1721pdt moved 7c11ac5af to
  dff8c2005); archive branches must be re-created, not moved.

### 6.9 Provenance incidents (2026-09-30 wave)

Shared-branch index races caused crossed commits: 9c6ee8ba8 carries
episodic-pressure files (C45) under the threshold red team message, and
fd31db230 carries threshold red team files (C49) under the C1 worker
message. Content verified blob-identical in both cases; provenance
documented (COMMIT_NOTE.md for C45); history not rewritten. Workers now
use explicit pathspecs with pre-commit status checks.

## 7. Post-ledger verdicts (second append; 2026-09-30; ledger appendix
C50-C53)

Appended to CLAIM_LEDGER.md after the C35-C49 append. No C01-C49
entry was modified. L3 achieved anywhere: still zero.

### 7.1 Continuing learner: retention closed, integration composed
(C50, C53)

- C50 RECENCY-GUARD-CONTAINED (prereg 68c5796d4, impl 6d7681138):
  SURVIVES as bounded L2. The recency-guarded earning discipline
  (skip the most recent arrival at inter-episode earning) holds 9/10
  sleeper retention across three pressure waves vs the 7/10 episodic
  baseline. The retention-policy lane is CLOSED; the discipline is
  adopted. The "in flight" note in 6.2 is resolved.
- C53 LEARNER-INTEGRATION-PASS (prereg c6288274d, impl d1305bd43):
  SURVIVES as bounded L2. One learner, one state: the frozen stress
  battery byte-identical (no regression) plus mid-lifetime causal
  ambiguity resolved by two adaptive interventions, persisted and
  retrieved after pressure. C50's discipline is active in the composed
  learner.

Open question 7 advances: the integrated learner now covers stress,
correction, interference, delayed reuse, memory pressure, and active
causal intervention in one process. Law-revert (P11 episode) is in
flight.

### 7.2 Developmental language: gate killed (C51)

- C51 GATE-STRESS-FAIL (pilot 82262d90c, prereg 37d4212d, sealed
  ebd62fe5): KILLED as a robust operator gate. A mid-utterance confound
  clearing K=2 installs as a DELETION operator and destroys novel
  composition (5/20 vs 20/20). K=2 discriminates K=2-deficient
  confounds; the Position-0 Lemma is confirmed empirically. C38 is not
  impugned within its battery.

Open question 8: the tak-displacement family is in flight.

### 7.3 Program discovery: D-v2 review (C52)

- C52 HYPD-REVIEW-COMPLETE (prereg 2c4c58e80, review c6069aca4):
  EXPLORATORY diagnostic. The T3 miss is structurally explained
  (dilution + carried niche poisoning); the predicted solution is real.
  D-v3 is in flight with both fixes as kill bars.

Open question 1 unchanged: zero.

## 8. Post-ledger verdicts (third append; 2026-09-30; ledger appendix
C54-C63)

Appended to CLAIM_LEDGER.md after the C50-C53 append. No C01-C53
entry was modified. L3 achieved anywhere: still zero.

### 8.1 Causal lane: learner-constructed graphs survive change and
revert (C54)

- C54 CAUSAL-REVERT-PASS (prereg c09afd95e, amendment ab68dd121, impl
  da0cd17b6): SURVIVES as bounded L2+. R1 REVISE: W0 -> k=2 -> W1 ->
  k=2 -> W2=W0 in 2 intervention rounds; R1 REBUILD takes 3 rounds;
  R2 permanent-change control shows no false snapback; FROZEN controls
  show the failure-to-revise pathology. 41/41 checks, 3/3
  byte-identical. The edit vocabulary (change-delay / add-rule /
  remove-rule) remains researcher-supplied; the learner-authored-edit
  frontier is in flight (causal_editinvent/).

Per the standing ONE-SYSTEM RULE, the revise machinery is
experimental evidence, not final architecture; it is not canonized.

### 8.2 Developmental language: displacement proves the position
assumption load-bearing (C55)

- C55 OPSCOPE-DISPLACEMENT-LOAD-BEARING (prereg ae9c3f13e, sealed
  54d3e3ca9): SURVIVES as bounded L2+ boundary-mapping evidence. The
  true negator at position 0 cannot install (cs==cb at every check; no
  operator; probes 0/3; 17/20 no-operator accuracy). The earlier OpScope
  result is position-contingent L2; any position-general reading is
  killed. Governance caveat travels: the worker disclosed one
  inadvertent python3 heredoc invocation during setup (placeholder
  only, no artifact); purity is not asserted fully clean for this
  lane. No further admission-gate lineage per the lane ruling.

### 8.3 Constructor-level redesign: L3B v2 (C56)

- C56 L3B-V2-PASS (prereg 05620eaa2, addendum 197e2547a, impl
  7a1d3265d): SURVIVES as bounded L2. The learner assembles
  MUL(VAR,VAR) from a generic 205-program grammar through
  CREATE/CONNECT; the fixed rel_of analyzer was removed, not widened.
  Hidden 3/3 on the square family. The constructor remains a finite
  menu under adversarial scrutiny (l3b_v2_adv2/ in flight); per the
  lane ruling it will not be expanded (redesign toward incrementally
  constructed executable state instead).

### 8.4 Continuing learner: law change and revert in one lifetime
(C57)

- C57 LEARNER-REVERT-PASS (prereg daf4f015d, impl dc20745db):
  SURVIVES as bounded L2. P1-P10 byte-identical to the C53 state; P11
  adapts through change and revert in 4 total rounds (h0/1, h1/2,
  h0/1); STATIC reproduces the C1 pathology; the re-derived law
  persists through a 20-item pressure wave. One 32,768-byte state, no
  reset, pure Zag. P12 (developmental-language integration) is in
  flight under learner_dev/.

### 8.5 Threshold boundary map; Tier-2 retired (C58)

- C58 THRESHOLD-BOUNDARY-MAP-COMPLETE (prereg 2eaa1f122, impl
  ab9a3ccfd): SURVIVES as bounded L2 boundary-mapping evidence. Both
  frozen predictions were wrong in opposite informative directions:
  Tier-1 floods the beam under crowding (evidence-perfect 16/16 CONDs
  scoring 9600 remove the terminals), while Tier-2 is unreachable when
  needed. Tier-2 ambitions for this lineage are permanently retired;
  the cond_disc2/ redesign (protected track for composite
  discriminative conditions) is in flight. Open question 3: the
  threshold mechanism stands as a Tier-1 recalibration with a boundary
  map; Tier-2b on the old substrate is closed.

### 8.6 L3C v2 adversary: survives this round (C59)

- C59 L3C-V2-ADV-SURVIVES-THIS-ROUND (prereg 2c0e52739, results
  8b82a836a): SURVIVES as bounded L2, this round only. Depth-3
  refinement 4/4; disjunction is an honest permanent by-design blind
  spot of disc2 (3 honest failures, no silent misresolution);
  default-edge repointing 5/5. One disclosed wording mismatch (prereg
  F2 scoring described as 2/4 vs the implementation's 4/4
  withhold-signature view); mechanism-facing facts unchanged. Round 2
  (l3c_v2_adv2/) in flight.

### 8.7 L3A trace: BUILD-FAIL on process (C60)

- C60 L3A-TRACE-BUILD-FAIL (prereg 05898699e, impl a6fbee865):
  BUILD-FAIL. The worker's result doc claims BUILD-PASS with strong
  technical results (invention, reuse, C0-A A1-A7), but the worker used
  a python3 heredoc on /tmp scratch during diagnostics; disclosure
  does not cure use under the literal pure-Zag rule, so K3 FAILS.
  Technical findings are exploratory only; a clean rebuild is in
  progress. No L3 or C0-A credit is canonical.

### 8.8 Governance: fork battery and paper audit (C61, C62)

- C61 FORKBATTERY-80/82 PASS (manifest a3d7a9ed3, results 801736ec4):
  GOVERNANCE-PASS. 80 PASS, 0 FAIL, 2 UNTESTABLE (expected); the
  consistency gate is now permanent infrastructure.
- C62 PAPER-GOVERNANCE-V2-PASS (audit d66466101): GOVERNANCE-PASS. The
  v2 clean paper is faithful to the 53-claim freeze; all 166 cited
  commits resolve. The paper is now stale for post-freeze verdicts; it
  stands only as a record against 8837d2ee0.

### 8.9 Paper artifact superseded (C63)

- C63 PAPER-DERIVED-COMPLETE (draft 6425f5a55): SUPERSEDED. A 34-claim
  evidence-first draft, superseded by v1 (94c30752f) and v2
  (89cf970ee). Not evidence; recorded for provenance.

## 9. Post-ledger verdicts (fourth append; 2026-09-30; ledger appendix
C64-C74)

Appended to CLAIM_LEDGER.md after the C54-C63 append. No C01-C63
entry was modified. L3 achieved anywhere: still zero.

### 9.1 L3B v2 adversary: bounded; run-1 honest FAIL (C64)

- C64 L3B-V2-ADV-BOUNDED (prereg 42538c6b6, addendum 252440aa4, impl
  5be03c94f): SURVIVES as bounded L2 (boundary confirmed by
  adversary). Run 1 FAIL was the adversary's own hand-derivation
  error, honestly recorded. Run 2 BOUNDED: depth-3 n^4 and
  constant-outside-range n+12 both honest no-growth with provable
  menu-edge traces; 8-version churn/revisit succeeds. Two
  limitations documented (silent first-match on ambiguous probes; no
  archive-exhaustion discipline, 9th version panics). The 205-program
  constructor is confirmed as a finite menu with a fixed archive; per
  the lane ruling it will not be expanded. The two limitations are
  addressed in C68.

### 9.2 Causal edit invention: learner-authored delay extension
(C65); generality broken by adversary (C71)

- C65 CAUSAL-EDITINVENT-PASS (prereg 811fc06c9, impl 4c233f82a):
  SURVIVES as bounded L2+ with learner-authored edit vocabulary. Old
  edit vocabulary provably insufficient (0/78); the learner derived
  the residual arrival pattern, identified delay_max as binding via
  generic diagnose-and-relax (max_rules -> 3: 0/220; delay -> 3:
  13/171), and constructed EXTEND-DELAY by computing dmax+1. The
  edit persisted; 3/3 byte-identical. No new modes, bridges,
  handlers, or semantic cases. Honest ceiling: L2+, not L3.
- C71 EDITINVENT-ADV-BREAKS (SCOPE-COLLAPSE) (prereg d71be66dc,
  attack 16c7665bd, results df270dc82): ADVERSARY-BREAKS (generality
  claim broken; C65 not retracted). The declared scope {max_rules,
  delay_max} was never two-dimensional: under min-arrival semantics
  a 3rd rule can only lower arrival times, so the max_rules arm was
  dead code (220/220 3-rule graphs have signatures inside the old
  15-signature set; binding=max_rules unreachable in every
  reachable trace; the ambiguous branch unreachable too). The one
  demonstrated self-revision (EXTEND-DELAY) traveled the only
  diagnostic path the machinery could ever take. Revised ceiling for
  the editinvent line: "learner-authored delay-domain extension in
  one law-change family; diagnose-and-relax is provably
  delay-specific, not parameter-generic." For the L3-revision
  program, general revision-machinery revision remains unproven.

### 9.3 L3C v2 adversary round 2: survives this round (C66)

- C66 L3C-V2-ADV2-SURVIVES-THIS-ROUND (prereg c3fc2b964, results
  593cc5906): SURVIVES as bounded L2, this round only. Simultaneous
  sibling-edge refinements serialize without record loss; the
  mixed-output guard fired correctly; depth-4 refinement composed;
  RACE 6/6; MIXED 6/6. No dropped records, double builds,
  misrouting, or silent misresolution. The remaining structural
  blind spot is disjunction, now closed by C73.

### 9.4 Learner-dev P12: PROCESS-FAIL (C67)

- C67 LEARNER-DEV-P12-PROCESS-FAIL (prereg 980981716, impl
  fd8757ba9): PROCESS-FAIL, not a clean pass. Technical findings
  preserved as reported: P12 integrated the position-contingent
  OpScope learner; P1-P11 byte-identical; P12 3/3; one 32,768-byte
  lifetime; +1,168 source lines; an independent 8,400-byte OpScope
  slice (architectural debt). The worker disclosed a python3
  invocation for the F3 literal audit; under the literal pure-Zag
  rule, disclosure does not cure use, so the previously reported
  LEARNER-DEV-PASS is governance-invalidated. The compression
  successor (learner_compress/) is the architecturally relevant
  path; a clean rebuild of the same composed subsystem architecture
  is not worthwhile under the one-system rule.

### 9.5 L3B v2 robustness: ambiguity and archive discipline (C68)

- C68 L3B-V2-ROBUST-PASS (prereg 92c73aeca, impl 41b87007a):
  SURVIVES as bounded L2. The two C64 limitations are fixed
  generically: explicit ambiguity records with a most-recent policy
  (no silent first-match, 3/3); archive-full refusal with a
  learner-observable signal (no panic, 3/3, exit 0). The 205-program
  grammar region is sha256-identical to v2; the interpreter region
  is identical. Zero new semantic cases, modes, bridges, or
  handlers; ~+110 source lines. Ceiling unchanged: bounded L2
  (finite menu); the incremental-construction redesign remains a
  separate program per the lane ruling.

### 9.6 OpScope behavioral validation: PASS; gate lineage closed
(C69)

- C69 OPSCOPE-BEHAV-PASS (prereg 82e0e94fd, amendments 428c00e23,
  54c943702, impl e8be2d5ef): SURVIVES as bounded L2. The final
  allowed cross-context validation: all frozen predictions matched,
  3/3 byte-identical per family. B3 overcomes the Position-0 Lemma
  blindness behaviorally ("not" installs via STRICT with posmask=0,
  TEST_ACC 20/20). Net -39 source lines (six count bars replaced by
  one generic behavioral check): architectural compression. The
  gate lineage is CLOSED per the lane ruling; no further gate is
  permitted. The standing question points at type-based semantic
  routing (scope bound to learned word types, not positions) as the
  deeper redesign, to be justified under the one-system rule.

### 9.7 L3A trace clean rebuild: BUILD-PASS (C70)

- C70 L3A-TRACE-CLEAN-BUILD-PASS (preregs 05898699e, 444617dd4,
  439dd54c5, impl e16cc0391): BUILD-PASS only (steps 1-3 of the
  11-step pipeline), not an L3 claim. Clean-room rebuild with zero
  Python anywhere reproduces all five frozen bars 3/3
  byte-identical; C0-A audit A1-A7 all PASS on the new
  implementation. 884 source lines; zero new semantic cases; the
  invented operator's semantics lives entirely in learner state.
  Independent red team (T-ADV) remains PENDING. This supersedes the
  exploratory technical findings of C60 with a clean process.

### 9.8 Hypothesis D v3: selection schedule necessary and
sufficient (C72)

- C72 HYPD-V3-PASS (prereg 3847065e2, impl e7149e452): SURVIVES as
  bounded L2 per the prereg; no L3 claim. Fix 1 (deterministic
  four-source parent schedule, SEL_MODE=1) and Fix 2 (carried
  programs banded into a seed pool never entering the archive,
  CARRY_MODE=1) implemented. v3-both T3 parity SOLVE 3/3
  byte-identical (556,548 evals, 14-op solution, held-out 31/39);
  CARRY_BLOCK_CHECK clean (niche 17570 natively generated,
  carried_match=0). Key finding: Fix 1 is NECESSARY and SUFFICIENT
  for T3 SOLVE; the selection-only ablation also solved T3
  (165,976 evals, 39/39 held-out) despite R5 poisoning; the
  carry-only ablation failed. ~180 source lines; 0 hardcoded
  semantic cases; 0 bridges/handlers. Governance note (process
  blemish, prereg document only): the frozen PREREG_HYPD_V3.md line
  142 and NAMECHECK.md contain em-dashes (a writing error, now
  immutable under the freeze); the result document is dash-clean.
  The verdict stands; the blemish is recorded on the prereg
  document, not the result.

### 9.9 L3C v3: disjunction blind spot closed without an OR case
(C73)

- C73 L3C-V3-PASS (prereg 3124d2e9a, impl 3bfa0947c): SURVIVES as
  bounded L2. Candidate A (alternative-cover dispatch) from the
  frozen disjunction design: the F2 disjunction truth family
  (previously 3 HONEST_FAILs) now builds a correct two-edge cover
  dispatch (DISP with 2 labeled edges (f1==1),(f2==9) to TERM(0),
  default to TERM(2)) with 4/4 truth eval, using only the
  interpreter's pre-existing union semantics. The interpreter diff
  is EMPTY. The memorization world produced no spurious cover (the
  per-element EVID_MIN=2 bar fired); the ambiguity world withheld
  with k=2; F1/F3 regression exact. 3/3 byte-identical. +269
  cognition source lines; 0 new semantic cases/modes/bridges/
  handlers; 0 interpreter lines changed. The new machinery is the
  general learning operation of cover-set composition, not
  disjunction-specific. Disclosed prereg analysis miss on P4 (the
  prediction forgot disc2 runs before disc_cover; the mechanism was
  correct); the bar was not moved. A genuine
  minimality-vs-memorization cover-path test remains untested,
  left for a follow-up builder under a fresh prereg.

### 9.10 Governance note: v3 paper audit process-invalidated (not a
numbered claim)

The v3 clean paper (c4855a65b) was built with zero Python (clean).
Its governance audit (b5a200ba0, claiming PAPER-GOVERNANCE-V3-PASS)
disclosed a single python3 heredoc invocation for read-only regex
extraction (re-verified with grep/git afterward; no artifact, no
logic adopted). Under the literal pure-Zag rule, any Python
invocation is a process failure; disclosure does not cure use. The
audit's PASS label is therefore process-invalidated and is NOT
ledgered as a clean governance-pass claim, consistent with the C60
and C67 rulings. The audit's technical findings (all 63 claims
present, 173 cited hashes resolve, no defects found) were
re-verified without Python and stand as reported. This is the
third Python process incident this cycle (C60 L3A-trace, C67 P12,
and this audit), a pattern worth noting: all three were
diagnostic/inspection conveniences, none affected a committed
artifact's logic, and all three were disclosed. The literal rule
applies regardless.

### 9.11 Governance: fork-battery wave 81/83 PASS (unnumbered
governance claim)

FORKBATTERY-81/83-PASS (manifest fe20cb7fe, results fe8485d7e):
GOVERNANCE-PASS. This is a governance instrument, not a numbered
C-claim. 83 named entries: 81 PASS, 0 FAIL, 2 UNTESTABLE (the
expected non-TNN trees rh-pull-1-head and rh-pull-2-head, pinned
toolchain absent). The consistency gate now runs PRE-RUN (A1+A2) as
well as post-run (A1-A4), all PASS. Archive immutability 41/41
clean. Negative controls discriminate on all 81 PASS entries.
Harness byte-identical to the frozen instrument. Governance
improvement note: the worker recommends adding an A0 uniqueness
assertion to the pre-run gate (duplicate entry names would collide).

### 9.12 Learner compression: OpScope slice eliminated (C74)

- C74 COMPRESSION-PASS (prereg 08a0c0ac4, impl 5722ff3a8):
  SURVIVES as bounded L2 (ceiling inherited). The 8,400-byte bespoke
  OpScope slice is deleted from the continuing learner; operator
  discovery now runs entirely on learner-owned structures (episodes
  as DDES ledger experience entries e7/e8/e9; the oprec as a
  stress-store fact under generic learn()/eviction; tallies as
  transient derivation). All five frozen prediction groups hold 3/3
  byte-identical. Source delta: net +0 lines (2380 = 2380,
  neutral). Net persistent bespoke bytes: -8,400. Zero new modes,
  bridges, handlers, or semantic cases. The standing question is
  answered: no new general operation was needed; the closest
  missing piece is a first-class append/replay
  experience-sequence accessor on the ledger (an API nicety, not a
  capability gap). Succession: this supersedes the P12
  architectural debt recorded in C67 (the slice is gone); C67's
  PROCESS-FAIL standing is unchanged (the process failure is not
  cured, only the debt is resolved). Architectural compression
  achieved: one learner-owned structural workspace, as the
  one-system rule requires.

### 9.13 Eviction tie-breaker pathology: the top continuing-learner blocker (C75)

- C75 EVICTION-TIE-BREAKER-PATHOLOGY (source 97b28e6a6,
  FREEZE-RUN-COMPLETE): SURVIVES as bounded L2 (characterization,
  not a capability claim). The frozen binary's evict_c() breaks
  lowest-importance ties by lowest index; when the 36-slot store
  fills with importance-1 slots, sequential teaches overwrite the
  same slot (signature: OBSERVED immediately followed by EVICT of
  the just-taught key). This revised the W4 prediction (PASS to
  FAIL) and the W5 prediction (PASS to FAIL) with a mechanism-level
  cause, and confounded W6-treatment and W9 per the pre-registered
  C1 clause. The substrate cannot stably hold 6 sequential new
  facts; experience accumulation across worlds is broken by the
  tie-breaker, independent of any capability-specific limitation.
  This is the top continuing-learner blocker identified by the
  freeze challenge. It revises two world predictions, not any
  survival verdict; the finding is on the frozen binary, so no
  source or binary change is implicated.

### 9.14 Governance note: FREEZE-RUN-COMPLETE (not a numbered claim)

The Core Freeze Challenge run phase completed at 97b28e6a6. All
9 sealed worlds executed against the frozen binary in protocol
order W1-W9 with persistent state carried across (S0 null through
S9). The battery did not void: binary hash 8733af3d2814 verified
before every world and re-verified after; source hash
b761efd90cb1 re-verified after (MATCH); all 15 world-file seals
verified before running. Learner profile: 1/9 WORLD-PASS (W1 new
concepts, 10/12 plus retention 10/10, CONFIRMS). W2, W3, W7, W8
failed as predicted (CONFIRMS). W4 and W5 predictions REVISED
(PASS to FAIL) by the C75 eviction pathology. W6 FAILED on the
adversary's attribution reading (treatment 1/5, 0/3 vault probes;
the action channel is constant CHOICE 0, so any gap is
world-authored); the literalist PASS reading is also recorded.
The W6 B4 interpretation is a protocol-interpretation call for
Micah and is NOT decided here. W9 failed as predicted on accuracy
(0/28 tree A, 0/31 tree B) but is C1-confounded. V0 PASS (untaught
triples return sentinel -2, not echo). C1 CONFOUNDED for
W6-treatment and W9. This is the challenge-level instrument
verdict (FREEZE-CHALLENGE-COMPLETE), not a learner trophy.

The v3 clean paper is now stale for C64-C76 (its derivation rule
pins it to the 63-claim freeze 236a63a5a0). A v4 regeneration
should wait for ledger stability; the v3 audit stands as a
historical audit against 236a63a5a0.

### 9.15 Smallest-consistent-k revision: causal lever confirmed (C76)

- C76 SMALLK-REVISION-CONFIRMED (prereg 22e2554b8, freeze
  13efc8f86, results 92ab7a270): SURVIVES as bounded L2 (revision
  validation, not a new capability claim). The sealed F-E family
  (6e03b2fa5) confirmed the periodic-demo key ambiguity as a
  systematic failure mode (24/24 R1 APPLICATION misses): the
  rotation class's largest-match-k tie-break yields k=3 for a
  period-2 demo against k=1 for normal demos, collapses the class,
  and falls back. Swapping the tie-break to smallest-consistent-k
  (one line modified at contestant.zag line 807, zero lines added)
  converts all 24 misses to hits; all frozen predictions hold
  (P-SK1 through P-SK5), with the H0 reversal-ambiguity baseline
  unchanged. The diag UNCLASSIFIED artifact is a stale-model
  classification issue, not a contestant failure; ground truth
  confirms 24/24 correct. This is a revision experiment under the
  standing execution rule (a finished experiment causes the next to
  begin; a located failure mode causes the fix to be tested): the
  failure was a tie-break policy, not an architectural limitation.
  Architecture delta: 1 line modified, 0 added; 0 new semantic
  cases/modes/bridges/handlers.
