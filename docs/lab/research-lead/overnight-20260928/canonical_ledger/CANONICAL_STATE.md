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
