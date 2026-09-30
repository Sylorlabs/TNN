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
   resets, task labels, or recompilation.
8. Developmental language: after DEVANG2 BUILD-FAIL and H-SEG2 downgrade.
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
