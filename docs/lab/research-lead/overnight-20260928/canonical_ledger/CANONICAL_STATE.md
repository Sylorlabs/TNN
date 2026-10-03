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

### 9.16 L3A-trace red team breaks the BUILD-PASS verdict (C77)

- C77 L3A-TRACE-REDTEAM-BREAKS (attack plan f0c3c980f, results
  43927f0a0): ADVERSARY-BREAKS against the C70 clean rebuild claim
  as stated. Attack 1 flipped the beam's lexicographic tie-break in
  `rankfirst` (one character, no learning-logic change); the beam
  found different but equally valid 7/7 solutions, the detector
  correctly reified a genuine shared segment with credit=2, and the
  hardcoded SEGMENT-MATCH byte oracle rejected it, flipping the
  verdict PASS to FAIL. The "invention" is beam-determined, not
  learner-determined; the verdict measures beam-byte reproduction,
  not learning. Attack 2 confirmed the detector generalizes to a
  new battery (novel segment found) while the verdict oracle does
  not. Attack 3 confirmed honesty (NO-INVENTION on the negative
  control). Attack 5 found a genuine memory-safety hole: `reify`
  has no bounds check on `nre` against the 4-slot name table; the
  5th reification crashes. Attack 4 (ablation budget) INCOMPLETE.
- C70 is NOT retracted; it is qualified. The clean rebuild
  faithfully reproduces the original's behavior (3/3 byte-identical,
  red-team baseline verified). The break targets the verdict's
  evidential weight: C70 certifies byte-reproduction, not learning.
  The v3 paper staleness note now covers C64-C77; v4 regeneration
  stays deferred to ledger stability.
- The red team disclosed one python3 invocation during Attack 5
  setup (probe-file text insertion); the file was deleted,
  recreated from pristine source, and redone with awk. No
  Python-derived content in committed files. Disclosure does not
  cure use; this is the fourth process incident this cycle.
- Recommendations banked: generalize or remove the SEGMENT-MATCH
  oracle; add a `reify` capacity check before continuing-learner
  use.

## 10. Post-ledger verdicts (eighth append; 2026-09-30; ledger appendix C78-C95)

Appended to CLAIM_LEDGER.md after the C77 append. No C01-C77 entry
was modified. L3 achieved anywhere: still zero. This append records
the architecture wave under Micah's 2026-09-30 rulings: the Core
Freeze Challenge as the central benchmark, the One-System Rule, the
tooling ruling (pure Zag only), and the consolidation directives.
No new capability SURVIVES in this append; all entries are
analysis, prereg, design, audit, or evaluator-asset records.

### 10.1 Freeze failure cluster analysis (C78)

- C78 CLUSTER-ANALYSIS-COMPLETE (905586a3b): EXPLORATORY. The 8
  freeze failures trace to 4 shared causes: A. state-management
  pathology (W4, W5, W6-treatment, W8-recall, W9); B. no
  hypothesis/rule construction machinery (W2, W3); C. no
  compositional machinery (W1 two-hop, W8-novel, W9-traversal);
  D. no agentic action machinery (W6-inquiry, W7). Each cluster
  carries a falsifiable prediction. Approved as the working
  diagnosis; merge clusters if deeper unity is found.

### 10.2 L3B/L3C integration scout (C79)

- C79 L3-INTEGRATION-SCOUT-COMPLETE (d7bddbc56): EXPLORATORY.
  Recommendation REDESIGN, keep both separate. Neither mechanism
  plugs into the frozen core without a forbidden bridge. The
  missing operation is learner-owned compose-verify-promote,
  which must not be hardcoded as one giant oracle.

### 10.3 Substrate scout (C80)

- C80 SUBSTRATE-SCOUT-COMPLETE (88622725f): EXPLORATORY. The C75
  pathology is representational poverty, not scheduling; the
  memory question and the representation question are the same
  frontier from two sides. Proposed substrate: tiny cell algebra,
  one learner-owned structural workspace, generic executor, zero
  domain semantic cases. The fold-retention recommendation was
  adopted in C89.

### 10.4 CLA-1 prereg (C81); CLA-2 consolidation (C89); LORG superseded (C84)

- C81 CONTINUING-LEARNER-PREREG-COMPLETE (b4f61ff8a):
  PREREG-FROZEN. Protected core (six primitives), one
  learner-owned workspace, mechanism integration as workspace
  processes, three-part C75 answer, append-only experience log.
  P1-P7; gaps G1-G3.
- C84 MEMORY-SUBSTRATE-PREREG-COMPLETE (c830c3005): SUPERSEDED by
  C89. LORG's diagnosis was correct; its packaging as a separate
  engine was wrong.
- C89 LORG-CONSOLIDATION-PREREG-COMPLETE (24351fd31):
  PREREG-FROZEN. CLA-2 folds every LORG structure into existing
  CLA-1 workspace conventions (no weight vector; probation as
  PROTECTION edges with decay clocks). Q1/Q2/Q3 addressed with
  falsifiable P7/P8/P9. CLA-2 is the primary architecture
  direction.

### 10.5 W2/W3 and W6/W7 analyses (C82, C83); CAM-1 prereg (C90)

- C82 W2W3-ANALYSIS-COMPLETE (2121fd16d): EXPLORATORY. One shared
  cause: no construct-and-apply step in the frozen core. Approved
  as a major frontier: W2 and W3 should be instances of the SAME
  general capability.
- C83 W6W7-ANALYSIS-COMPLETE (e7bb3d0bc): EXPLORATORY. One shared
  cause: the action channel is open-loop (constant CHOICE 0).
  Proposed: a learner-state-consulting ACT handler; not a planner.
- C90 CONSTRUCT-APPLY-PREREG-COMPLETE (68a41be8a):
  PREREG-FROZEN. One propose-verify-promote-apply mechanism for
  W2/W3; split bar S1-S3; guards G1-G5 enforce the One-System
  Rule.

### 10.6 Learner-state ACT prereg (C87); comparison protocol (C88)

- C87 LEARNER-ACT-PREREG-COMPLETE (51a818141): PREREG-FROZEN.
  Generic read path from workspace to actuator; fills CLA-1 gap
  G2. Action choice from learned structures, per ruling F.
- C88 ARCH-COMPARISON-PROTOCOL-COMPLETE (128921ed9):
  PROTOCOL-FROZEN. Seven dimensions, weighted decision rule, D7
  sealed new-capability battery. CLA-1 vs contlearn2 as temporary
  competitors; converge after discrimination.

### 10.7 One-System audit (C85); unified structures (C91); compose ops (C92)

- C85 ONESYSTEM-AUDIT-COMPLETE (f2684204b): EXPLORATORY. 0
  architectural modes; 1 bridge; 7 handlers; 0 hardcoded semantic
  cases; 1 syntax router. The proc/caus split in the unified
  learner is the real architectural debt. Three consolidations
  proposed with falsifiable battery claims.
- C91 UNIFIED-STRUCTURES-EXPLORATION-COMPLETE (4ab7d3890):
  EXPLORATORY. Five cognitive objects as one executable
  workspace; the proc/caus distinction should emerge from
  learner structure.
- C92 COMPOSE-OPS-INVESTIGATION-COMPLETE (881b17638):
  EXPLORATORY. Four minimal operations (COPY, APPLY,
  CORROBORATE, PROMOTE) over the CLA-1 six; oracle O1-O3;
  falsification F1-F7.

### 10.8 Tooling contamination audit (C93)

- C93 TOOLING-AUDIT-COMPLETE (70c520637): AUDIT-COMPLETE. Under
  the pure-Zag ruling: the Core Freeze Challenge 1/9 scoring and
  the C1-family driver run_race.sh are NEEDS-RERUN (scientific
  logic in shell). Underlying artifacts and data are intact; no
  retraction of measured values, but no canonical citation until
  pure-Zag re-derivation. C64-C75 lanes audited CLEAN.

### 10.9 C1 baseline (C94); FW1-FW9 sealed (C95)

- C94 C1-BASELINE-LEARNING-PROPERTY (8a2929098): NEEDS-RERUN.
  45 runs; MEM 27/63, FREQ at most 6/63, RAND 5/63 vs C1-CLEAN
  63/63. The frozen prereg rule yields the learning-property
  verdict, but the shell driver is flagged by C93, so the claim
  is provisional pending pure-Zag rerun.
- C86 WORLDS-V2-DESIGN-COMPLETE (200387b42): DESIGN-APPROVED.
  FW1-FW9 approved as sealed evaluator/adversary assets, not
  design hints.
- C95 WORLDS-V2-SEALED (396895595): SEALED. 16 world files plus
  the FW6 responder generated in pure Zag; hashes recorded;
  five design ambiguities resolved and documented. Evaluator
  asset, not a capability claim.

The v3 paper staleness note now covers C64-C95; v4 regeneration
stays deferred to ledger stability.

## 11. Post-ledger verdicts (ninth append; 2026-09-30; ledger appendix C96-C101)

Appended to CLAIM_LEDGER.md after the C78-C95 append. No C01-C95
entry was modified. L3 achieved anywhere: still zero. This
append records: the integration incompatibilities found before
implementation, the pure-Zag freeze rescore that clears the C93
scoring flag, the composition scout, the EXECUTE placement
resolution, the FW blindness audit, and Micah's protected-core
ISA boundary ruling. No new capability SURVIVES in this append.

### 11.1 Integration spec: builders paused for amendments (C96)

- C96 INTEGRATION-SPEC-COMPLETE (62e5ebb9f): coordination
  record. Twelve incompatibilities across the CLA-2, CAM-1,
  ACT, and compose-ops specs; amendment checklist A1-A12 plus
  flagged judgment J1 for Micah. Builders (CLA-2, CAM-1, ACT)
  paused until the amendments are ruled on. The critical
  finding is INCOMPAT-6: CAM-1's finite-difference PROPOSE vs
  the {EQ, ADD} trial-based basis, a genuine allocation-of-
  intelligence question.

### 11.2 Freeze rescore clears the C93 scoring flag (C97)

- C97 FREEZE-RESCORE-COMPLETE (5325ffed8): the Core Freeze
  Challenge 1/9 verdict is re-derived in pure Zag with zero
  discrepancies (stricter than the shell scorer; count
  mismatches exit instead of silently mis-pairing). The C93
  NEEDS-RERUN flag is cleared for the freeze scoring only.
  The C1-family driver rerun remains pending; the C93 scope
  note is updated to PARTIALLY CLEARED.

### 11.3 Composition scout (C98)

- C98 COMPOSITION-SCOUT-COMPLETE (cd7a3dd28): EXPLORATORY.
  One execution core (EXECUTE vocabulary), three discovery
  problems. W1 probes test search, not learned composition
  (relation 599 has no consistent meaning across probes).
  W1 belongs in Cluster C, not B. The gap is the plan
  constructor, not the executor. Falsifiable prereg specified
  (P1-P5, F1-F5). Fifth Python process incident this cycle
  disclosed and recorded.

### 11.4 EXECUTE placement resolved (C99)

- C99 EXECUTE-PLACEMENT-RESOLVED (1fc77503b): analysis.
  EXECUTE belongs in the protected core as a seventh
  primitive over a 4-op ISA {MOVE, BRANCHEQ, INC, DEC};
  the regress argument justifies the fixed point, and the
  minimal fixed point is derived entry-by-entry. {INC, DEC}
  beats {ADD}: MUL-from-ADD needs a decrementable counter,
  and INC/DEC forces the learner to construct ADD. APPLY is
  EXECUTE. Amendments A-C pending Micah's approval.

### 11.5 FW blindness audit (C100)

- C100 BLINDNESS-AUDIT-PASS (6f0eae9f2): governance finding.
  No substrate builder accessed the sealed FW1-FW9 worlds;
  the only repo-wide reference is the ledger's own C95 seal
  record. Evaluator blindness holds; monitoring procedure
  established.

### 11.6 ISA boundary ruling (C101)

- C101 ISA-BOUNDARY-RULING (0525377f3): Micah's ruling,
  binding. The protected core may contain a SMALL, FROZEN,
  domain-neutral computational basis comparable to an ISA
  (ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, ADD, BRANCH,
  APPLY/EXECUTE, generic state/register operations). No core
  operation may encode a target-domain regularity detector
  (FIND_POLYNOMIAL_ORDER, DETECT_NEGATION, BUILD_CAUSAL_RULE,
  LEARN_PROCEDURE, FIND_THRESHOLD, MAKE_CONDITIONAL, or
  equivalents). Finite-difference regularity detection is out
  of CAM-1 core intelligence; trial/compositional discovery
  using learner-created structures is the approved route. No
  MUL for FW3; the learner must construct it. The coordinator
  package (10 core ops, MISS_POLICY, POLICY_ROOT, trial-based
  P-DEP, edge-derived standing, zero modes/bridges/handlers)
  is approved with this boundary. Worker toolchain guard
  instituted as a process-system fix: allowed toolchain
  verification before each worker, forbidden interpreters
  removed from PATH where possible, any scientific wave
  invoking a prohibited language is automatically
  PROCESS-FAIL.

The v3 paper staleness note now covers C64-C101; v4
regeneration stays deferred to ledger stability.

## 12. Builders land; C1 cleanly re-frozen (tenth append; 2026-09-30; ledger appendix C102-C110)

Appended to CLAIM_LEDGER.md after the C96-C101 append. No
C01-C101 entry was modified. L3 achieved anywhere: still
zero. This append records: the COMP-1 composition prereg,
the MUL-from-ADD construction scout, the frontier ranking
(with the 6th Python process incident), the architecture
accounting baseline, the three builder landings (CAM-1,
ACT, CLA-2) under the amended ISA package, the C1 pure-Zag
driver re-derivation (with the 7th Python process
incident), and the clean re-freeze that fully clears the
C93 NEEDS-RERUN flag. No new capability SURVIVES in this
append; three BUILD-PASS verdicts record builder
completion only.

### 12.1 COMP-1 composition prereg frozen (C102)

- C102 COMP-1-PREREG-FROZEN (4f6f0c5c8): query-time plan
  construction firing on the query-miss path via
  MISS_POLICY. Three frozen templates {CHAIN-2, GATHER-n,
  ITERATE-UNTIL} with a three-part anti-menu defense. The
  e-ruling is strict: expected only as post-hoc feedback
  on already-constructed plans, with the e-ablation
  mandatory. Q3 (MISS_POLICY bootstrap) and Q4 (no counter
  primitive; ISA arithmetic only) decided. P1-P5, F1-F7.
  Zero new core execution ops; 150-line bound on the
  bootstrap miss-policy.

### 12.2 MUL-from-ADD construction scout (C103)

- C103 MUL-SCOUT-COMPLETE (8d30083b7): EXPLORATORY. The
  construction target is a learner-tagged PROC graph with
  a back-edge (iteration), an accumulation cell, and a
  data-dependent termination test, all checkable as
  white-box graph properties. Rung A runs on the approved
  ISA basis alone (ADD, EQ, BRANCH, MOVE plus literal 1;
  no SUB needed). Rung B is the deeper test: the learner
  constructs ADD itself first, then MUL on top. The
  high-value variant: the learner reusing the ADD loop's
  shape one level up, satisfying C0-D inside the
  experiment. Template-contamination check: the final
  graph must contain at least one structural decision the
  researcher did not make. Full 7-phase experiment spec
  with P-MUL1..5 and F-MUL1..5.

### 12.3 Frontier ranking; 6th Python incident (C104)

- C104 FRONTIER-SCOUT-COMPLETE (edcb364e3): EXPLORATORY
  with PROCESS-FAIL. Ranked by information gain:
  DEVINT-CLA2 (developmental integration on the
  consolidated workspace) on top, then learner-driven
  inquiry, then linguistic relations as executable
  structures, then the transfer regression battery. The
  worker ran `python3 -c "pass"` as a stray fragment
  during the dash check (6th Python process incident this
  cycle). Content unaffected as analysis; canonical
  standing requires clean re-freeze if the ranking
  matters.

### 12.4 Architecture accounting baseline (C105)

- C105 ARCH-ACCOUNTING-BASELINE-COMPLETE (4d38aac91):
  measurement procedure frozen. Frozen core: 586
  cognition lines across 75 functions (episode/candidate
  machinery the bulk at 344), 1/9 worlds, zero
  modes/bridges/handlers, 32768 state bytes.
  contlearn2: 136 lines, 1024 bytes. Cognition lines
  count only learn/retrieve/infer/retain/plan functions.
  Re-measurement triggers on each builder landing;
  historical rows never edited.

### 12.5 The three builders land (C106-C108)

- C106 CAM1-BUILD-COMPLETE (371d20743): BUILD-PASS. The
  critical amendment is in: finite-difference OUT of
  P-DEP, trial-based discovery over {EQ, ADD} in. 6/6
  tests on synthetic data (W2-class, W3-class z = x + y
  discovered, P5 abstention, P6 VERIFY ablation, P7
  contradiction demotion, P4 exact lookup). 818 lines, 0
  semantic cases, 3/3 deterministic.
- C107 ACT-BUILD-COMPLETE (f7d87938f): BUILD-PASS.
  Five-step read protocol with POLICY_ROOT as node 0,
  signed evidence bid selection, zero branches on world
  or task identity. 24/24 tests pass. ~700 lines, 0
  handlers. One bug found and fixed (evict_to_cap
  over-evicted on high-water mark).
- C108 CLA2-BUILD-COMPLETE (e639904f2): BUILD-PASS. The
  full consolidated learner: 7 core primitives, EXECUTE
  with closed 4-op dispatch, POLICY_ROOT/MISS_POLICY as
  ordinary nodes, signed evidence bids, miss-policy
  dispatch, bootstrap discovery the learner can
  supersede. 15/15 self-tests, deterministic, K1/K2/K3
  verified. One latent bug fixed (activate returning
  history nodes).

### 12.6 C1 re-derivation; 7th Python incident; clean re-freeze (C109-C110)

- C109 C1-ZAGDRIVER-COMPLETE (d5984f313): PROCESS-FAIL.
  The pure-Zag driver re-derived all 60 runs
  byte-identically; P1-P6 all hold (C1-CLEAN 63/63, MEM
  27/63, learning property stands). The worker disclosed
  one Python invocation during development (inspection
  aid for key.json). 7th Python process incident this
  cycle. Scientific result superseded by C110.
- C110 C1-REFREEZE-CLEAN (323f2afaa):
  REPRODUCTION-CONFIRMS. Zero Python invocations
  (restricted PATH, verified before every phase). Driver
  source verified pure Zag; binary byte-identical to
  pinned-znc rebuild; worlds and contestants frozen.
  60/60 runs, 114/120 files byte-identical to d5984f313.
  New finding: the C1 contestant binary has flaky
  non-determinism on the D1/D2/D3 abstention queries
  (approximately 13% of runs; 60/63 instead of 63/63,
  retests to 63/63). The driver is deterministic; the
  flakiness is in the contestant. P1-P6 hold; the
  learning-property conclusion is intact. The contestant
  non-determinism requires investigation.
- C93 NEEDS-RERUN is now FULLY CLEARED. No C1-family
  numeric remains flagged.

The v3 paper staleness note now covers C64-C110; v4
regeneration stays deferred to ledger stability.

## 13. Red teams break CAM-1's L3 reading; flakiness reclassified; re-measurement lands (eleventh append; 2026-09-30; ledger appendix C111-C117)

Appended to CLAIM_LEDGER.md after the C102-C110 append. No
C01-C110 entry was modified. L3 achieved anywhere: still
zero. This append records: the three independent red team
audits (CAM-1 broken to bounded L2; ACT qualified on a
bid-directionality spec divergence; CLA-2's source
claims hold with a stale-binary process finding), the
CLA-2 binary rebuild that remediates that finding, the
C1 flakiness investigation (harness resume bug, not
contestant non-determinism), the architecture accounting
re-measurement (1255 vs 586 lines; integration step
required), and the verified bundle v13 backup. No new
capability SURVIVES in this append; one ADVERSARY-BREAKS,
two ADVERSARY-QUALIFIED, one REMEDIATION-COMPLETE, one
INVESTIGATION-COMPLETE, one BASELINE-UPDATED, one
BACKUP-VERIFIED.

### 13.1 CAM-1 red team: bounded-L2 posture (C111)

- C111 CAM1-REDTEAM-COMPLETE (7f0ce2d97):
  ADVERSARY-BREAKS. Three attack successes: P-DEP is
  menu selection over four researcher-composed
  templates (z = x*y undiscoverable by construction);
  MAP semantics live in eval_body's four-way dispatch
  (the learner stores an index into a
  researcher-defined table; the builder's "0 semantic
  cases" claim is false, accurate count 4); standing is
  circular (promote writes SUPPORTS edges from the same
  held-back facts used for verification). Finite
  difference genuinely removed (ISA boundary holds);
  K1/K3 pass. Recommended posture: CAM-1 survives as
  bounded L2; genuine compositional discovery belongs
  to COMP-1. C106 BUILD-PASS stands as a builder
  verdict; its L3-adjacent reading is broken.

### 13.2 ACT red team: bid divergence recorded (C112)

- C112 ACT-REDTEAM-COMPLETE (73d06a6d4):
  ADVERSARY-QUALIFIED. All 24 builder tests re-run and
  confirmed PASS. Four of five vectors pass:
  genericity (no tag checks in the ACT path; the
  uncertainty behavior is fully emergent), POLICY_ROOT
  (ordinary WRITE/READ on node 0), uncertainty, K1/K2/
  K3. One ATTACK-SUCCESS: ACT's bid() counts edges
  bidirectionally while the integration spec's CLA-2
  reference (evcount) counts only incoming edges. The
  spec says "ACT reuses the same function"; it does
  not. Tests do not exercise the difference (all test
  evidence is incoming), so BUILD-COMPLETE stands, but
  the alignment decision is pending: directional
  (match CLA-2) vs bidirectional (amend spec with
  rationale). Two low caveats: nbr() hardcodes node-0
  exclusion; three scattered hardcoded register
  protections instead of a unified mechanism.

### 13.3 CLA-2 red team: source holds; stale binary (C113)

- C113 CLA2-REDTEAM-COMPLETE (bd7a3f440):
  ADVERSARY-QUALIFIED. Four of five vectors pass:
  bootstrap_miss is fully generic (no relation names,
  no forbidden ops); zero semantic cases; EXECUTE ISA
  sandbox closed; standing computed live from edge
  counts, never stored; K1 verified across all four
  frozen inputs. Two observations: the K node is never
  revised by any code path ("revisable" aspirational);
  the bootstrap inflates MAP standing via self-loop
  SUPPORTS edges. Finding F1 (process-level
  ATTACK-SUCCESS): the working-directory cla2_bin was
  stale (pre-fix source, 7/8 with P10 FAIL). A fresh
  pinned-compiler build from committed source passes
  15/15. Remediated by C114.

### 13.4 CLA-2 binary rebuilt (C114)

- C114 CLA2-BINARY-REBUILT (ad7d3ac1c):
  REMEDIATION-COMPLETE. Fresh build from committed
  cla2.zag: 116799 bytes (matches red team size
  expectation), sha256 recorded, SELF-TESTS PASSED:
  15/15. Source untouched. The stale binary was never
  in git; the fresh one is now committed. C113 F1
  closed.

### 13.5 C1 flakiness: harness resume bug (C115)

- C115 C1-FLAKINESS-INVESTIGATED (e98a976a0):
  INVESTIGATION-COMPLETE. The C110 "contestant
  non-determinism" finding is reclassified. Root
  cause: the Zag driver mkdirs state but never clears
  it; the resume script skips on costs.txt without
  clearing partial state/ dirs. The /tmp wipe killed
  the drive at 22/60; on resume two runs re-ran on
  stale state, ingesting every turn twice (weights
  exactly 2x), which pushed D1/D2/D3 across the
  abstention threshold. Reproduced cleanly: fresh dir
  63/63, re-run on same dir 58/63 with the exact
  flaky signature. The contestant is deterministic
  given fresh state; the C110 "~13% flakiness"
  estimate is withdrawn. P2 and P6 stand without
  caveat. Fix belongs in the resume script, not the
  contestant. C93 clearance unaffected.

### 13.6 Architecture re-measurement (C116)

- C116 ARCH-REMEASURE-COMPLETE (73b0be40e):
  BASELINE-UPDATED. Per the frozen procedure: CLA-2
  685, CAM-1 408, ACT 162 cognition lines, sum 1255
  vs frozen core 586. The prereg projection of
  net-negative does not hold for separate
  implementations (roughly 404 lines of duplicated
  workspace machinery per builder). Holding at zero:
  semantic cases, modes, bridges, handlers across all
  three. Positive: learned structures now nonzero
  where both baselines were zero (CLA-2: 3, CAM-1: 1,
  ACT: 2). Trajectory: negative on lines, holding at
  zero on architectural smells, positive on
  learner-created structure. Code compression
  requires the integration step.

### 13.7 Bundle v13 verified (C117)

- C117 BUNDLE-V13-COMPLETE (73b5bfbfc):
  BACKUP-VERIFIED. 2.0G, HEAD ad7d3ac1cb98,
  SHA-256 32de7f16..., complete history across 69
  refs. Supersedes v12.

## 14. Builders land on composition and developmental integration; inquiry gap specified; guard audited (twelfth append; 2026-09-30; ledger appendix C118-C124)

### 14.1 COMP-1 compositional machinery built (C118)

- C118 COMP1-BUILD-COMPLETE (170e39424): BUILD-PASS.
  879-line pure-Zag implementation per frozen prereg
  C102 (K1 verified: 4f6f0c5c8 ancestor of 170e39424).
  10/10 tests pass, byte-identical across 3 runs. The
  e-ruling is structural: mp_build/mp_build_compose do
  not take expected as input; F2 verified byte-identical
  construction traces with expected masked/unmasked.
  P4 three-hop works via plan-structure composition
  (template marker 4 = COMPOSED), not a fourth template.
  K2/K3 hold. Bootstrap miss-policy 157 lines vs 150
  projection: projection variance, not a kill bar.

### 14.2 DEVINT-CLA2 developmental integration built (C119)

- C119 DEVINT-CLA2-BUILD-PASS (35f9500b2): BUILD-PASS.
  1212-line pure-Zag implementation per frozen prereg at
  f24063bcb (K1 verified). One continuing process, no
  resets: segmentation, GROUP-node concept formation,
  learned rules, contradiction with retrievable history,
  inquiry, demotion, memory pressure with GROUP
  protection, delayed reuse with zero re-teaching. All
  11 stages pass with exact frozen numbers; B1-B5 all
  PASS; 3/3 byte-identical determinism. The builder
  caught and fixed two genuine bugs during construction
  (boundary-spanning substrings inflating the lexicon;
  the PROTECT anchor node 2 evicted by the eviction
  routine). Per the pipeline this is BUILD-PASS only;
  no SURVIVES or L3 claim.

### 14.3 Integration scout: one-system spec (C120)

- C120 INTEGRATION-SCOUT-COMPLETE (c0e99a601):
  EXPLORATORY. Duplication inventory: about 475 lines
  of workspace machinery written 4 times across the
  implementations. CLA-2's workspace format wins
  (40-byte nodes, 16-byte edges, 12 edge types; already
  contains the ACT protocol and MAP nodes). CAM-1's
  eval_body menu is deleted, not ported (per C111).
  Unified event flow: one teach path, one query path
  with miss-policy dispatch, one ACT protocol.
  Projected about 1100 cognition lines vs 1555 across
  four separate builds. Integration prereg shape
  specified with K1-K5 (hard 1200-line ceiling,
  source-scan ban on the CAM-1 menu) and F-INT1
  through F-INT4.

### 14.4 Inquiry scout: the remaining illusion (C121)

- C121 INQUIRY-SCOUT-COMPLETE (b4853a9f7): EXPLORATORY.
  ACT can read learner state to choose an action, but
  the learner does not yet create the uncertainty
  structures or derive the action guides; test
  scaffolding does those parts. Two missing pieces:
  Piece A (uncertainty reification from -2 admissions)
  and Piece B (inquiry guide construction via D2
  derivation); both must be generic-primitive
  workspace processes. Four-phase discriminating
  experiment specified; Phase 4 is novel-domain
  transfer with zero researcher mapping (L3-flavored).

### 14.5 ACT bid aligned; guard audited (C122-C123)

- C122 ACT-BID-ALIGNED (75a9b0e04):
  REMEDIATION-COMPLETE. ACT bid() now counts incoming
  evidence edges only, matching CLA-2 evcount(); spec
  A3 ("ACT reuses the same function") is now true.
  Rationale: an outgoing SUPPORTS edge is a guide's
  claim about the world, not evidence for the guide.
  Source diff limited to bid(); 24/24 tests pass,
  byte-identical 3x, no test changes. C112 closed.
- C123 GUARD-AUDIT-COMPLETE (e0a842962): EXPLORATORY.
  All 7 Python incidents were process-level, none
  scientific. Zero incidents since guard formalization.
  Workers now actively prevent invocation (restricted
  PATHs, stub scripts). 6 of 7 self-disclosed.
  Recommendation 1 (fix the composition scout
  NAMECHECK record) has since been actioned by record
  correction 67f92ed4f.

### 14.6 STATUS doc wave process-fail (C124)

- C124 STATUS-DOC-PROCESS-FAIL (6e4a9479f):
  PROCESS-FAIL. Per Micah's ruling: the worker invoked
  python3 -c for a mechanical character replacement
  (em dash to colon in four documentation section
  headers). The absolute ban applies; this
  documentation wave is process-contaminated. It does
  NOT contaminate unrelated scientific experiments
  whose research logic remained pure Zag. The guard
  is kept absolute; no new prompt changes required.
  The STATUS.md artifact stands with the process-fail
  flag on its wave.

## 15. Integration lands; MUL constructed; inquiry needs re-freeze (thirteenth append; 2026-09-30; ledger appendix C125-C133)

### 15.1 Integration prereg frozen; TNN-1 one-system build (C125, C127)

- C125 INTEGRATION-PREREG-FROZEN (7fc7148ac):
  PREREG-FROZEN. The 480-line one-system TNN-1
  specification: unified CLA-2-format workspace,
  exact port/delete lists, K1-K5 with the hard
  1200-line ceiling (F-INT1), F-INT1 through F-INT6
  (including the trench-coat test F-INT4), P-INT1
  through P-INT7. Micah's pending EXECUTE ruling
  noted as inherited, not canonized.
- C127 TNN-1-BUILD-COMPLETE (0323b97d5): BUILD-PASS.
  One binary, 1088 source lines (under the 1200-line
  ceiling), 35/35 tests pass: CLA-2 15/15, ACT
  directional bid 6/6, COMP-1 10/10, CAM-1 ported
  P6/P7 2/2, DEVINT-CLA2 compact curriculum 1/1, XCAP
  cross-capability 1/1. 3/3 byte-identical. Zero new
  ops/modes/bridges/handlers. CAM-1 menu deleted, not
  ported. First genuine compression: ~1555 lines
  across four builds to 1088 in one binary.

### 15.2 MUL-1 Rung A: learner constructs multiplication (C128)

- C128 MUL1-RUNG-A-BUILD-COMPLETE (fbf14f73a):
  BUILD-PASS. After 4,297 incorrect candidates, the
  learner promoted a 4-cell PROC [ACCUM_RX STEP_C
  TEST_CY GOTO(0)]: a genuine repeated-addition loop,
  more efficient than the prereg's 6-cell sketch
  (zero-initialized slots make INITs unnecessary).
  5/5 P-MUL pass including the (13,17)->221 scaling
  probe; oracle audit (trial 4298, 72 genuine
  rejections, shuffled rerun 12/12); 3/3
  byte-identical. No new arithmetic op in source.
  Restricted safebin PATH, python3 ABSENT.

### 15.3 Inquiry prereg frozen; build wave process-fail (C126, C129)

- C126 INQUIRY-PREREG-FROZEN (04ac028fb):
  PREREG-FROZEN. Pieces A (uncertainty reification)
  and B (guide construction) as learner-side workspace
  processes; 4 phases; K-INQ1 through K-INQ4 with the
  300-line bound; F-INQ1 through F-INQ5; controls
  C1-C3.
- C129 INQUIRY-BUILD-PROCESS-FAIL (396ecafa4):
  PROCESS-FAIL. The builder completed all frozen bars
  (115 lines, all P-INQ pass) but self-disclosed one
  python3 invocation (9th incident). Per the guard,
  the wave is PROCESS-FAIL. Bars recorded for the
  clean re-freeze to reproduce, not as adopted
  results. A clean re-freeze worker is in flight.

### 15.4 DEVINT-CLA2 red team qualifies the build (C130)

- C130 DEVINT-CLA2-REDTEAM (a5ccb100d):
  ADVERSARY-QUALIFIED. 4 ATTACK-SUCCESS vectors:
  unseen-domain form_groups coupling, 10x-interference
  evidence cascade, GROUP protection conditional on
  hardcoded anchor, contradiction handling partial
  (SPLIT never attempted, retention blind to
  demotion). Strongest finding: S6 "procedure
  learning" does not learn from examples; the pairing
  is harness-supplied. C119 BUILD-PASS stands (B1-B5
  literally hold), but 6 prereg elements were not
  implemented as specified. M2/F4 claims corrected
  per the red team.

### 15.5 Remediations and infrastructure (C131, C132, C133)

- C131 C1-HARNESS-FIXED (fac9875b0):
  REMEDIATION-COMPLETE. Resume now clears stale state;
  old bug reproduced (32->62 facts), fix verified
  63/63 identical to fresh. C115 closed.
- C132 COMPRESSION-TRACKER-ESTABLISHED (f46a89e99):
  EXPLORATORY. R_test/R_world/R_fw defined; 4-system
  total corrected to ~1555 cognition lines.
- C133 RECORD-CORRECTED (67f92ed4f):
  REMEDIATION-COMPLETE. Composition scout NAMECHECK
  retraction aligned with C98; resolves guard audit
  recommendation 1.

No new SURVIVES. L3 achieved anywhere: still zero.
The ledger stands at 133 claims.

The v3 paper staleness note now covers C64-C133; v4
regeneration stays deferred to ledger stability.

## 16. Inquiry re-frozen clean; three red teams; freeze plan (fourteenth append; 2026-09-30; ledger appendix C134-C142)

### 16.1 Inquiry clean re-freeze supersedes the failed wave (C134)

- C134 INQUIRY-REFREEZE-BUILD (18ed3331c): BUILD-PASS.
  The INQUIRY-1 experiment re-implemented from scratch
  in pure Zag (935 lines, pinned znc abed8aa1) after the
  C129 PROCESS-FAIL wave. All frozen bars pass:
  P-INQ1 (12 queries -> exactly 12 UNCERTAINTY nodes),
  A1 (reify disabled -> 0 nodes), W1 + P-INQ2 (12 fresh
  keys -> 12 guides, all CHOICE 30, within 10 events),
  A2 (construct disabled -> 0 guides), P-INQ3
  (>=10/12 attribution), P-INQ3b (no pre-play), P-INQ4
  (>=16/20 follow-ups), P-INQ5a/b/c (novel conflict-type
  transfer), C1/C2/C3 (non-vacuous controls). K-INQ1
  through K-INQ4 PASS; 149 cognition lines (under the
  300 budget); 3/3 byte-identical. Restricted safebin
  PATH, python3 ABSENT. F-INQ1 through F-INQ5: none
  triggered. This supersedes the C129 PROCESS-FAIL
  wave; both are recorded.

### 16.2 Three red teams: TNN-1 qualified, MUL clean, COMP-1 process-level (C135, C136, C137)

- C135 TNN-1-REDTEAM (cbde38737): ADVERSARY-QUALIFIED.
  5 ATTACK-PASS: the workspace is genuinely shared
  (not three systems in a trench coat), line count
  honest (1088 lines, one 11-line dead function), no
  template smuggling, no menu resurrection, 3/3
  byte-identical, tests isolated. 1 qualified
  ATTACK-SUCCESS: the XCAP test (F-INT4) verifies
  metric co-location on one node, not plan-to-guide
  conversion; the claim needs strengthening or
  narrowing before SURVIVES consideration.
- C136 MUL-REDTEAM (44f22979b): ADVERSARY-QUALIFIED
  with no qualifications. 6/6 ATTACK-PASS, no
  successful attacks: no lookup smuggling, no oracle
  leakage (trial 4298 verified arithmetically),
  genuine scaling loop, structural honesty confirmed,
  ablation honest (ADD survives as core ISA, not
  workspace state), 3/3 byte-identical. Recorded
  under the conservative existing taxonomy; no new
  status invented.
- C137 COMP-1-REDTEAM (7ffc2dae4):
  ADVERSARY-QUALIFIED. 4 ATTACK-PASS: exactly three
  templates, three-hop behavior is genuine plan
  composition, the e-ruling is structural (no code
  path for expected to reach construction),
  determinism 3/3 byte-identical. 1 process-level
  ATTACK-SUCCESS: the bootstrap is 157 lines vs the
  150-line prereg bound; the prereg's "bound" language
  is stronger than the builder's "projection"
  framing. A prereg amendment documenting the
  157-line actual is needed before SURVIVES
  consideration.

### 16.3 Governance and measurement (C138, C140, C141)

- C138 PYTHON-AUDIT-2 (4a97c985c): EXPLORATORY. 16
  commits audited since the guard audit; 1 new
  incident (9th overall, the inquiry build,
  self-disclosed). 15 commits clean. Zero scientific
  contamination across all 9 incidents to date.
  Self-disclosure 100%, Step 0 compliance 100%.
  Weakness: only the MUL builder used a true safebin;
  recommendation to make safebin default for builders.
  Record inconsistency flagged on the inquiry
  NAMECHECK (corrected separately).
- C140 COMPRESSION-UPDATE (78a556e3a): EXPLORATORY.
  First genuine compression: ~1555 lines across four
  builds to 1088 lines in one TNN-1 binary (~30%
  smaller), 35 tests across five capability families
  plus XCAP. TNN-1 R_test 3.22/100; MUL-1 R_test
  0.89/100 (construction tests, not comparable). The
  6-test ACT compact vs 24/24 standalone deviation is
  flagged, not hidden. Cognition-line caveat stands:
  formal classification per
  MEASUREMENT_PROCEDURE.md is open. Largest evidence
  gap unchanged: no freeze worlds run on TNN-1 yet.
- C141 FREEZE-RERUN-PLANNED (4e36f31f2): EXPLORATORY.
  Full plan for the Core Freeze re-run on TNN-1.
  Critical gap: TNN-1 has no world-driver interface;
  a zero-cognition driver shim is needed or TNN-1 is
  declared not-freezable as-is. Recommended scope:
  freeze TNN-1 alone (Option A), FW1-FW9 primary,
  W1-W9 supplementary. Five governance flags for
  Micah: driver shim, new prereg, EXECUTE boundary
  (inherited), inquiry scope, W1-W9 methodology.
  Priority 5 remains blocked on rulings 1-4.

### 16.4 Remediation and backup (C139, C142)

- C139 DEVINT-REPORT-CORRECTED (a003bd19b):
  REMEDIATION-COMPLETE. The DEVINT-CLA2 BUILD_REPORT
  is amended with a dated correction note: M2
  retracted as measured (m2_check never called; M2
  was not measured; GROUP survival via hardcoded
  PROTECT, not bid-driven retention); F4 guard
  qualified as vacuous. B1-B5 and the 11 stage
  results unaffected; BUILD-PASS stands. Resolves the
  C130 recommendation.
- C142 BUNDLE-V14 (323e3bbb4): BACKUP-VERIFIED. 2.0G,
  SHA-256
  06b43ac8db876447237da11e3e33d5f44e50e7d5277429deccf9396d89759481,
  HEAD d5e3222b608c358b92332f0cad4020d00be71741,
  69 refs, 3279 commits, complete history verified.
  Supersedes v13 (C117).

No new SURVIVES. L3 achieved anywhere: still zero.
The ledger stands at 142 claims.

The v3 paper staleness note now covers C64-C142; v4
regeneration stays deferred to ledger stability.
