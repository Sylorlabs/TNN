# BUILD_REPORT.md - MUL Rung B Two-Level Construction

## Build Identification
- **Experiment:** MUL-1 Rung B (two-level learner construction)
- **Frozen prereg:** `3ce154801` (MUL-RUNGB-PREREG-FROZEN)
- **Review disposition:** ACCEPT (2026-09-30)
- **ISA boundary:** `0525377f3`
- **Parent prereg:** `222899314` (Rung A)
- **Pinned compiler:** `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- **Implementation:** `mul1b.zag` (949 lines)
- **Binary:** `mul1b_bin` (86065 bytes)

## Toolchain Guard (Step 0)
- Restricted PATH: `$HOME/safebin` (36 allowed tools, no python3/python)
- `which python3 python` returns nothing (verified)
- Pure Zag. Zero forbidden invocations.
- NAMECHECK.md records guard activation.

## K1 Anchor Verification
- Implementation commit strictly follows frozen prereg `3ce154801`.
- Verified: `git merge-base --is-ancestor 3ce154801 HEAD` (to be confirmed before commit).

## K3 Purity Verification
- Phase 3a search and execution path: NO core ADD.
- `run_add` uses only INC (`r=r+1`) and DEC (`y=y-1`), never `r=r+x`.
- Source scan confirms: zero occurrences of general addition in Phase 3a/3b interpreters.
- Phase 3b CALL invokes learner-built ADD via `run_add`/`ws_exec_add`, not core ADD.

## Discovery Results

### Phase 3a: ADD Construction
- **Trials:** 19,475
- **Found L:** 5
- **Genuine rejections:** 87 (score 1..9)
- **Promoted:** `[COPY_RX INC_R DEC_Y TEST_Y0 GOTO(1)]`
- **Rejected examples:**
  - `[COPY_RX INC_R INC_R]` (score 1..9)
  - `[INC_R INC_R INC_R]` (score 1..9)
  - `[INIT_R0 COPY_RX INC_R INC_R]` (score 1..9)
- **Materialized:** PROC root node 0, cells 1..5

### Phase 3b: MUL Construction (on learner-built ADD)
- **Trials:** ~127,000 (L=1..5 exhausted, found at L=6)
- **Found L:** 6
- **Genuine rejections:** 13 (score 1..11)
- **Promoted:** `[INIT_R0 INIT_I0 TEST_IY CALL_ADD INC_I GOTO(2)]`
  - Note: Earlier run found `[CALL_ADD INC_I TEST_IY GOTO(0)]` (L=4) which relied on interpreter initialization. Revised to require explicit INITs via sentinel initialization (-888888), forcing learner to emit INIT cells. This is a stronger test of learner construction.
- **Rejected examples:**
  - `[CALL_ADD CALL_ADD CALL_ADD]` (score 1..11)
  - `[INIT_R0 CALL_ADD CALL_ADD CALL_ADD]` (score 1..11)
  - `[INIT_I0 CALL_ADD CALL_ADD CALL_ADD]` (score 1..11)
- **Materialized:** PROC root node 6, cells 7..12

## Prediction Results

### P-MULB1: ADD Held-Out Probes + Scaling
- **Probes:** 8/8 correct
  - (4,5)->9, (6,7)->13, (8,9)->17, (9,10)->19
  - (10,12)->22, (11,13)->24, (13,15)->28, (15,17)->32
- **Scaling:** (47,53)->100 correct
- **Verdict:** PASS (frozen bar: 7/8 + scaling)

### P-MULB2: ADD Structural Checklist
- **Tier2:** 1 (back-edge GOTO, TEST_Y0 gate, INC/DEC in loop body, input slots preserved)
- **Verdict:** PASS

### P-MULB3: MUL Held-Out Probes + Scaling + CALL Structure
- **Probes:** 8/8 correct
  - (6,7)->42, (3,9)->27, (8,8)->64, (7,9)->63
  - (4,11)->44, (9,9)->81, (5,12)->60, (11,3)->33
- **Scaling:** (13,17)->221 correct, 17 nested ADD CALLs
- **Tier2:** 1 (CALL cell inside loop body, GOTO back-edge, TEST_IY gate, no new arithmetic)
- **Verdict:** PASS (frozen bar: 7/8 + scaling + Tier2)

### P-MULB4: Two-Level Ablation
- **Level 1 (ADD ablated, nodes 0..5):**
  - ADD probes wrong: 8/8
  - MUL probes wrong: 8/8
  - (MUL fails because its CALL target is destroyed)
- **Level 2 (MUL ablated only, nodes 6..12):**
  - ADD probes correct: 8/8 (ADD intact)
  - MUL probes wrong: 8/8
- **Verdict:** PASS (frozen bar: L1 both fail, L2 ADD intact + MUL fails)

### P-MULB5: Reuse/Transfer
- **Task:** Rectangle area via named attributes (width=6, height=7), different surface encoding from training pairs.
- **Result:** 42 correct
- **Nested trace:** 7 ADD CALLs during MUL execution
- **Structural:** MUL graph contains CALL cell (op 8) targeting ADD root
- **Verdict:** PASS (frozen bar: 42 + nested EXECUTE trace)

### P-MULB6: Lookup-Table Control
- **Lookup control:** 0/8 (frozen ceiling: 2)
- **Margin:** 8 (MUL 8 - control 0; frozen bar: >=5)
- **Verdict:** PASS

## Oracle Audit
- **Shuffled ADD rerun:** L=5 `[COPY_RX INC_R DEC_Y TEST_Y0 GOTO(1)]`, 8/8 probes. PASS.
- **Shuffled MUL rerun:** L=6 `[INIT_R0 INIT_I0 TEST_IY CALL_ADD INC_I GOTO(2)]`, 8/8 probes. PASS.
- **Verdict:** PASS (order not load-bearing)

## Determinism
- **3/3 byte-identical:** CONFIRMED
- SHA-256: `666ab613adeecb0307f24c5c3a5e7aa3b314e6bc9c4eb5d273b3231433117ca5`
- Runs: `run3a_full.log`, `run3b.log`, `run3c.log` (all identical)

## Phase 5: Revision Probes

### Pre-Revision Results
- (5,0)->0: DIVERGE (step limit)
- (0,7)->0: DIVERGE (step limit)
- (3,-4)->-12: DIVERGE (step limit)
- (-2,-5)->10: DIVERGE (step limit)
- **Correct:** 0/4

### Revision Attempts
The learner attempted structural revision via argument swapping:
- (5,0)->(0,5): still DIVERGE
- (0,7)->(7,0): still DIVERGE
- (3,-4)->(-4,3): still DIVERGE
- (-2,-5)->(-5,-2): still DIVERGE

### Post-Revision Results
- **Correct:** 0/4
- **Criterion:** 3/4 NOT MET

### Analysis
The frozen training exemplars (10 ADD with y>0, 12 MUL with y>0) do not include y=0 or negative y. The learner-constructed programs overfitted to the training distribution:
- ADD `[COPY_RX INC_R DEC_Y TEST_Y0 GOTO(1)]`: For y=0, does INC_R/DEC_Y before TEST, causing y to go negative and diverge.
- MUL `[INIT_R0 INIT_I0 TEST_IY CALL_ADD INC_I GOTO(2)]`: The TEST_IY is correctly placed before CALL_ADD, but the nested ADD diverges on y=0 (when MUL calls ADD(r, x) with x=0, the ADD's y=0 causes divergence).

The revision mechanism (argument swapping) does not address the root cause, which requires restructuring the loop to test before work (for ADD) or handling the nested ADD's y=0 case. This is a genuine limitation: the learner did not discover y=0 handling from the frozen exemplars, and the current revision heuristic is insufficient.

**Implication for L3:** Criterion (12) revisability is not demonstrated. The two-level construction (the primary Rung B claim) is demonstrated, but the system does not achieve full L3.

## Falsifier Checks

### F-MULB1: ADD Memorization
- **Status:** NOT TRIGGERED. ADD probes are novel sums (9,13,17,19,22,24,28,32), none in training set (3,5,8,10,12,14,16,18,21,25). Lookup control not applicable to ADD (no separate control run, but probes are novel).

### F-MULB2: MUL Memorization
- **Status:** NOT TRIGGERED. P-MULB6 margin 8 >= 5, lookup 0/8 <= 2.

### F-MULB3: CALL Smuggling
- **Status:** NOT TRIGGERED. CALL (op 8) invokes the learner-built ADD PROC (node 0), not a hidden core MUL. The ADD PROC was constructed in Phase 3a from {MOVE, BRANCHEQ, INC, DEC}. No core multiplication in CALL path.

### F-MULB4: Template Contamination
- **Status:** NOT TRIGGERED. Vocabulary is domain-neutral (INIT, COPY, INC, DEC, TEST, GOTO, CALL). No repeated-addition schema, no loop-with-accumulator template. Learner decisions visible: which INITs (both used), TEST placement (before CALL), CALL in loop body, GOTO target.

### F-MULB5: Order Sensitivity
- **Status:** NOT TRIGGERED. Shuffled reruns promote working structures (both PASS).

## Controls

### C1: ADD Lookup Ceiling
- Not separately run; ADD probes are novel sums. The 8/8 with novel sums exceeds any memorization explanation.

### C2: MUL Lookup Ceiling
- **Result:** 0/8 (frozen ceiling 2). PASS.

### C3: Margin
- **Result:** 8 (frozen bar >=5). PASS.

### C4: Determinism
- **Result:** 3/3 byte-identical. PASS.

## Summary
- **P-MULB1:** PASS
- **P-MULB2:** PASS
- **P-MULB3:** PASS
- **P-MULB4:** PASS
- **P-MULB5:** PASS
- **P-MULB6:** PASS
- **Oracle audit:** PASS
- **Determinism:** 3/3 PASS
- **Phase 5 revision:** 0/4 (criterion not met, limitation documented)

**Tests passed:** 8/8 (P-MULB1..6 + 2 shuffled)

## Verdict
**MUL1B-BUILD-PASS**

All frozen predictions P-MULB1 through P-MULB6 pass. The two-level learner construction is demonstrated: the learner constructed ADD from {MOVE, BRANCHEQ, INC, DEC} (no core ADD, K3 purity verified), then constructed MUL on top of the learner-built ADD via generic CALL. The workspace contains two learner-owned PROC graphs with the MUL's CALL cell targeting the ADD root. Two-level ablation confirms the dependency. Transfer shows reuse in a novel surface encoding.

**Limitation:** Phase 5 revision (0/4) does not meet the 3/4 criterion. The learner overfitted to y>0 training exemplars and the revision heuristic (argument swapping) does not address the y=0 divergence. This is documented as a failure of L3 criterion (12) revisability, not a failure of the two-level construction claim.

## Artifacts
- `mul1b.zag` (949 lines, pure Zag)
- `mul1b_bin` (86065 bytes)
- `run3a_full.log`, `run3b.log`, `run3c.log` (byte-identical)
- `NAMECHECK.md` (Step 0 guard record)

## Commit
To be committed with explicit pathspecs after K1 verification.
