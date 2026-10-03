# TNN Native Lab: Consolidated Status

**Date:** 2026-09-30, ~15:18 PDT
**Branch:** `tnn-native-lab`
**HEAD:** `170e39424` (COMP-1 BUILD-COMPLETE)
**Ledger:** 110 claims (C01-C110); L3 achieved anywhere: zero
**This document:** a human-readable snapshot. The canonical records are
`canonical_ledger/CLAIM_LEDGER.md` and `CANONICAL_STATE.md`. It contains
no em dashes.

---

## 1. Where the program stands

The architecture wave under Micah's 2026-09-30 rulings (One-System Rule,
Core Freeze Challenge as central benchmark, protected-core ISA boundary,
pure-Zag tooling) has produced four builder landings, three adversarial
audits, two frozen experiment preregs, and a clean C1 re-derivation. The
frozen-core trajectory is measured, not guessed.

The central bet being tested: a tiny frozen domain-neutral computational
basis (the ISA) plus learner-created cognitive structures can do what the
frozen core could not, with the intelligence living in what the learner
builds rather than in how many cognitive subsystems humans wrote.

---

## 2. Current architecture: four builders landed

### 2.1 CLA-2 (consolidated continuing learner) : BUILD-PASS

- Commit `e639904f2`; binary rebuilt `ad7d3ac1c` (116,799 bytes, 15/15).
- 7 core primitives: ALLOC, READ, WRITE, LINK, ACTIVATE, DECAY, EXECUTE.
- EXECUTE(root, frame): seventh primitive with closed 4-op dispatch
  {MOVE, BRANCHEQ, INC, DEC}; unknown op tags and budget exhaustion fail
  cleanly.
- POLICY_ROOT (node 0), MISS_POLICY (node 1) as ordinary nodes writable
  via WRITE; nodes 0-1 reserved from allocation and eviction.
- Signed evidence bid: SUPPORTS/CONFIRMS/USE/DEPENDS-ON +1, CONTRADICTS -1.
- Miss-policy dispatch in QUERY: exact-key, SURPRISE, MISS_POLICY,
  HISTORY/REGRET, then -2.
- Bootstrap miss-policy: null MISS_POLICY runs frozen P-INV trial
  discovery; the learner supersedes it by writing a dispatch address once
  it promotes a MAP node.
- 685 cognition lines; 16,384 state bytes; 3 learner-created structures
  (GROUP nodes, MAP nodes, edge-derived standing).

### 2.2 CAM-1 (construct-and-apply) : BUILD-PASS, posture bounded L2

- Commit `371d20743`; 818 lines; 6/6 tests on synthetic data.
- The critical amendment is in: finite-difference regularity detection is
  OUT of P-DEP (per the ISA ruling); trial-based discovery over {EQ, ADD}
  is IN. No order detection, no coefficient fitting, no SUB, no MUL.
- W2-class literal maps, W3-class z = x + y discovered from 6 pairs,
  negative control abstains, VERIFY rejects a spurious construction-time
  regularity, contradiction demotes standing 1 to -1.
- 408 cognition lines; 344,080 state bytes (separate store, pending
  integration); 1 learner-created structure (MAP nodes with
  trial-discovered bodies).
- Posture after red team: bounded L2 template-matcher with real
  verification, NOT a discovery engine beyond its menu (see section 3).

### 2.3 ACT (learner-state action selection) : BUILD-PASS

- Commit `f7d87938f`; ~700 lines; 24/24 tests pass.
- Five-step read protocol: context assembly, POLICY_ROOT null check,
  2-hop ACTIVATE, address-equality structural match, highest-bid
  selection.
- `act_event` takes only stores plus context; zero branches on world,
  task, or relation identity.
- Uncertainty behavior is emergent: zero tag checks in the ACT path;
  P-ACT2's uncertainty-anchored guide fires from address-equality wiring.
- 162 cognition lines; 33,816 state bytes; 2 learner-created structures
  (POLICY_ROOT convention, ACTION-GUIDEs).
- One open spec divergence: bid directionality vs CLA-2 (see section 6).

### 2.4 COMP-1 (compositional machinery) : BUILD-PASS

- Commit `170e39424`; 879 lines; 10/10 tests, 3/3 byte-identical.
- Query-time plan construction firing on the query-miss path via
  MISS_POLICY. Three frozen templates {CHAIN-2, GATHER-n, ITERATE-UNTIL}
  with a three-part anti-menu defense.
- The e-ruling is implemented and tested: `expected` is post-hoc feedback
  only. The F2 e-ablation shows byte-identical construction traces with
  and without masking; `expected` changes selection, never construction.
- 3-hop via CHAIN-2 composition (template marker 4, COMPOSED); no fourth
  template added. Template ablations confirm each template carries its
  predicted load.
- Zero new core execution ops. This is the genuine compositional
  discovery that CAM-1's red team found missing from CAM-1.

---

## 3. Red team findings and postures

### 3.1 CAM-1 red team (commit `7f0ce2d97`)

- Anti-oracle: ATTACK-SUCCESS (partial). P-DEP is menu selection, not
  composition. Four researcher-composed templates {LITERAL, COPY_A,
  DBL_A, ADD_AB} in fixed priority; z = x*y or z = 2x+3y are
  undiscoverable by construction. This inverts the prereg's own
  anti-menu argument.
- Criterion-0: ATTACK-SUCCESS. MAP semantics live in `eval_body`'s
  four-way dispatch; the learner stores an index into a
  researcher-defined table. No L3 reading survives.
- Finite-difference residue: ATTACK-PASS. Genuinely removed; ISA boundary
  honored.
- VERIFY honesty: ATTACK-SUCCESS (partial). Standing is circular:
  promotion writes SUPPORTS edges from the same held-back facts used for
  verification.
- Builder's "0 semantic cases" claim was false; accurate count is 4.
- Posture: bounded L2. Compositional discovery belongs to COMP-1.

### 3.2 ACT red team (commit `73d06a6d4`)

- Genericity: ATTACK-PASS (caveat: `nbr()` hardcodes node-0 exclusion).
- POLICY_ROOT: ATTACK-PASS (caveat: three scattered hardcoded address
  checks instead of a unified register-protection mechanism).
- Evidence bid: ATTACK-SUCCESS (spec divergence). ACT counts edges in
  both directions; CLA-2's `evcount()` counts only incoming. The spec
  says "ACT reuses the same function"; it does not. Tests do not exercise
  the difference (all test evidence is incoming), so BUILD-COMPLETE
  stands, but the gap needs resolution.
- Uncertainty: ATTACK-PASS. Fully emergent.
- K1/K2/K3: PASS.

### 3.3 CLA-2 red team (commit `bd7a3f440`)

- 4/5 attack vectors pass. Hidden researcher policy: PASS. Semantic
  cases: PASS (zero). EXECUTE ISA sandbox: PASS (closed). Standing
  derivation: PASS (live edge counts, never stored).
- Finding F1 (process): the committed `cla2_bin` was stale (built from
  pre-fix source, 7/8 with P10 FAIL). Remediated at `ad7d3ac1c`: fresh
  pinned-compiler build, 15/15, source unmodified.
- Observations: the K node is never revised ("revisable" is aspirational);
  the bootstrap inflates new MAP standing via self-loop SUPPORTS edges.

---

## 4. Active preregs (frozen, awaiting builders)

### 4.1 DEVINT-CLA2 (commit `f24063bcb`)

Developmental integration on the consolidated workspace. The 11-stage
sequence from DEVINT1/2 ported to CLA-2 using the identical morpheme
domain (bik, gup, zol, tav) for direct regression comparability.
Concepts as GROUP nodes, rules as executable graphs, contradictions as
CONTRADICTS edges, inquiry as UNCERTAINTY nodes driving ACT. Kill bars
B1-B5 plus 3/3 byte-identical determinism. Failure localization table
maps each stage failure to a precise claim about what consolidation
cost. This is the experiment that most discriminates the architecture
program's central bet.

### 4.2 MUL-1 (commit `222899314`)

Learner construction of multiplication from the generic basis. 7 phases.
Rung A on {MOVE, BRANCHEQ, ADD} plus literal cells (the learner must
discover the literal-1 step). Rung B on {MOVE, BRANCHEQ, INC, DEC} with
learner-constructed ADD first. N=12 bare exemplars, no scaffolding;
8 held-out probes; scaling probe (13,17) to 221 kills disguised case
lists. L3 bar applied MUL-specifically with a template-contamination
check. The high-value variant (learner reusing ADD's loop shape one
level up) runs as a second arm.

---

## 5. C1 status: 63/63 clean, learning property stands

- C1-CLEAN: 63/63 on W0/W1/W2, 3/3 byte-identical; H0 66/67, H1 67/67.
- Pure-Zag driver re-derived all 60 runs (C109, PROCESS-FAIL on a
  development-time Python inspection; superseded).
- Clean re-freeze (C110): zero Python, 60/60 runs, 114/120 files
  byte-identical. P1-P6 all hold.
- The "flakiness" finding is retracted: commit `e98a976a0` proved it was
  a harness resume bug, not contestant non-determinism. The /tmp wipe
  killed the drive mid-run; resume re-ran two runs on stale state,
  doubling all weights and pushing D1/D2/D3 across the abstention
  threshold. Reproduced cleanly: fresh dir 63/63, stale dir 58/63 with
  the exact signature. The contestant is deterministic. Fix: clear the
  output dir on resume.
- MEM 27/63 vs C1-CLEAN 63/63: the learning-property verdict stands.
  C93 NEEDS-RERUN is fully cleared. No C1-family numeric remains flagged.

---

## 6. Open questions

1. **ACT bid directionality.** ACT counts evidence edges in both
   directions; CLA-2's reference counts only incoming. The integration
   spec claims they are the same function; they are not. Decision needed:
   align ACT to directional counting, or amend the spec with a rationale
   for bidirectional. The consequence-edge design in the ACT prereg
   makes this substantive. An analysis worker is assigned.

2. **Integration architecture.** CLA-2 + CAM-1 + ACT + COMP-1 sum to 1255
   cognition lines vs the frozen core's 586. Each builder duplicated
   roughly 400 lines of workspace machinery. Zero modes/bridges/handlers/
   semantic cases across all four, but no code compression yet. The
   integrated one-system implementation is the real test of the
   consolidation thesis. An integration scout is specifying the unified
   workspace.

3. **Seven Python process incidents this cycle.** All were
   diagnostic/inspection conveniences; none affected a committed
   artifact's logic; all were disclosed. Under the literal rule, each is
   PROCESS-FAIL regardless. The worker toolchain guard (verified PATH,
   stub binaries, Step 0 in every NAMECHECK.md) is the process-system
   fix. The pattern to watch: workers keep reaching for Python for
   quick inspection. The guard is holding on the artifacts; the
   incidents are the cost being measured.

4. **CAM-1's ceiling.** Bounded L2 per the red team. The open question is
   whether trial-based P-DEP can be promoted from menu selection to
   genuine composition, or whether COMP-1 is the right home for
   discovery and CAM-1 stays as the apply-side mechanism.

5. **Sealed FW1-FW9 evaluation.** The evaluator battery is sealed and
   blindness holds. It awaits the integrated implementation for the D7
   new-capability comparison.

---

## 7. Ledger and governance

- 110 claims (C01-C110). Zero L3 anywhere. Zero new SURVIVES in the
  architecture wave; BUILD-PASS records builder completion only.
- C93 (tooling contamination) is FULLY CLEARED.
- Three PROCESS-FAIL claims (C67, C104, C109); the C109 result was
  superseded by the clean C110 re-freeze.
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md`: zero-diff across
  every commit in this wave. Verified before each commit.
- Commits remain local. Nothing pushed. Latest verified bundle: v13
  (`~/workspace/tnn-native-lab-20260930-v13.bundle`, 2.0 GB, HEAD
  `ad7d3ac1cb98`, SHA-256
  `32de7f1648744422532b391f108eb3d76636958b544ce860aede0d84d8685cf4`).

---

## 8. What comes next

The active swarm: DEVINT-CLA2 builder, MUL builder, integration scout,
ledger cycle 11 (C111+ for the red teams, binary rebuild, flakiness
retraction, re-measurement), C1 harness fix, ACT bid analysis, and this
consolidation. The discriminating experiments are DEVINT-CLA2 (does the
consolidated workspace preserve the developmental sequence?) and MUL-1
(can the learner construct multiplication from the frozen basis?).
The integration step decides whether the One-System consolidation
delivers code compression or just structural capability.
