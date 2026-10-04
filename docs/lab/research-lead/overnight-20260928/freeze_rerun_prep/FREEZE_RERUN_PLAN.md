# CORE FREEZE RE-RUN: PREPARATION PLAN

Status: FREEZE-RERUN-PLANNED (planning only; no freeze executed).
Date: 2026-09-30. Worker: Core Freeze Re-run Preparer.
Priority: Micah's priority 5: "Rerun Core Freeze on the consolidated core without source edits."

## 1. Original Freeze Baseline (what we know)

### 1.1 The frozen artifact
- Source: `core_freeze/stage0/world_learn.zag` (586 cognition lines)
- Binary: `core_freeze/stage0/world_learn_bin` (sha256 `8733af3d...`)
- Frozen at commit `87ac95d08`; Stage 0 READINESS-PASS at `e129b2fbd`
- Protocol: `FREEZE_PROTOCOL.md` (frozen `66e3c3f38`)

### 1.2 The 1/9 result (commit `97b28e6a6`, rescore `5325ffed8`)
| World | Capability | Verdict | Notes |
| W1 | new concepts | WORLD-PASS (10/12, ret 10/10) | Exact-key memory; 2-hop probes returned -2 |
| W2 | new procedures | WORLD-FAIL (0/8) | No procedure abstraction |
| W3 | causal laws | WORLD-FAIL (0/10) | No hypothesis construction |
| W4 | law change/revert | WORLD-FAIL (1/6, 2/6, 3/6) | Eviction pathology, not reversion |
| W5 | contradictions | WORLD-FAIL (1/2, 4/6) | Cascade from W4 instability |
| W6 | active inquiry | WORLD-FAIL (1/5) | B4 dual reading; C1 CONFOUNDED |
| W7 | planning | WORLD-FAIL (0/4) | No action-selection machinery |
| W8 | synth language | WORLD-FAIL (0/9) | Training triples evicted |
| W9 | new representation | WORLD-FAIL (0/28, 0/31) | No traversal; C1 CONFOUNDED |

### 1.3 The dominant finding: eviction pathology (C75)
Sequential teaches at importance 1 overwrite the same lowest-index slot repeatedly (tie-breaker bug). This dominated W4, W5, W6, W8, W9. It is a state-management flaw, not a missing cognitive capability. Micah's directive: the 1/9 is evidence about what the frozen core is missing, not nine requests for nine patches.

### 1.4 Sealed FW1-FW9 (commit `200387b42`, design `396895595`)
Nine fresh adversarial worlds testing the SAME nine capabilities with different surface content (ids in 30000-39999 block). Design only; never executed. Key design features:
- FW4/FW5 specifically target C75 with 2x pressure (12 sequential facts; 10-link dependency chain)
- FW9 is the general-substrate discriminator (requires learner-constructed DAG topology; no eviction tweak can produce it)
- FW1 is the stability baseline (predicted PASS; if a repair breaks FW1, the repair is regressive)
- Failure clustering: memory/eviction (FW4, FW5, FW8, FW9), construction (FW2, FW3, FW8, FW9), action (FW6, FW7)

## 2. TNN-1 Readiness Assessment

### 2.1 What TNN-1 is
- Commit `0323b97d5`; 1090 source lines (under 1200-line ceiling)
- 35/35 tests pass: CLA-2 15/15, ACT 6/6, COMP-1 10/10, CAM-1 2/2, DEVINT-CLA2 1/1, XCAP 1/1
- 3/3 byte-identical determinism
- Zero new ops/modes/bridges/handlers (F-INT3 holds)
- CAM-1 menu deleted, not ported

### 2.2 Is TNN-1 ready to be frozen?
YES, with qualifications:
- TNN-1 is BUILD-PASS, not SURVIVES. It has not yet faced independent red team (red team worker is in flight as of this writing).
- The DEVINT-CLA2 red team found 4 ATTACK-SUCCESS vectors against the standalone DEVINT build (commit `a5ccb100d`). TNN-1 ports DEVINT-CLA2 as a compact curriculum (P-INT5). The red-team findings (form_groups harness coupling, evidence cascade, M2 never computed, S6 pairing not induced) may apply to TNN-1's ported code.
- Recommendation: wait for the TNN-1 red team result before freezing. A freeze on a build with known-unexamined fragilities wastes the sealed FW battery.

### 2.3 What "without source edits" means for TNN-1
The original freeze protocol (section 2.3) requires:
1. A single compiled source file is declared as the frozen artifact
2. Source and binary hashes are recorded
3. The binary is executed against sealed worlds with NO modifications
4. Capability source delta must remain zero throughout (hash re-verified before each world)

For TNN-1, this means:
- The frozen artifact is `tnn1_build/tnn1.zag` (1088 lines) compiled with the pinned toolchain
- A TNN-1-specific world-driver interface must exist: the original freeze used `world_learn_bin` with a specific event-stream protocol (OBSERVE/QUERY/ACT lines, ANSWER/CHOICE outputs, STATE_SAVED/STATE_LOADED). TNN-1's `tnn1.zag` is a test-suite binary, NOT a world-driver binary.
- CRITICAL GAP: TNN-1 does not currently implement the freeze world interface. The original `world_learn.zag` had `stage0/INTERFACE.md` (world-input interface) and `stage0/REGIONS.md` (state regions). TNN-1 would need an equivalent driver layer to accept sealed world event streams.
- "Without source edits" CANNOT mean "run tnn1.zag as-is against FW worlds" because tnn1.zag has no world-file input path. It must mean: freeze the TNN-1 cognitive core, then add ONLY a thin driver shim (world-file parsing, event dispatch, answer emission) that contains zero cognition, OR freeze a TNN-1 variant that already includes the driver.

This is a governance question for Micah (see section 5).

## 3. Key Architectural Differences (586-line core vs 1090-line TNN-1)

### 3.1 State management (directly relevant to C75)
- Original: 36-slot fact store, importance-based eviction with lowest-index tie-break (the C75 pathology).
- TNN-1: 1024 nodes x 40B, 4096 edges x 16B, 3-step eviction with directional bid (incoming-only, per ACT alignment at `75a9b0e04`), GROUP protection.
- PREDICTION: TNN-1 should NOT exhibit the C75 tie-breaker pathology. The 3-step eviction with signed directional bids is a different mechanism. FW4/FW5 (the C75 stress worlds) are the direct test.

### 3.2 Composition and procedures
- Original: no procedure abstraction (W2 0/8), no composition (W1 2-hop probes -2).
- TNN-1: COMP-1 plan construction ported (3 frozen templates: conjunctive, inverse, transitive), EXECUTE with closed 4-op ISA, MISS_POLICY plan construction on query-miss.
- PREDICTION: TNN-1 may pass compositional probes that the original failed. FW2 (5-step procedure, fresh surface) and FW1 (3-hop chains) are the direct tests. Note: COMP-1's templates are researcher-authored; FW2 uses a 5-step procedure specifically to defeat memorization of a 4-step shape.

### 3.3 Action selection
- Original: fixed CHOICE 0 on ACT (W7 0/4, W6 degenerate).
- TNN-1: ACT 5-step protocol with directional signed bid, POLICY_ROOT, 2-hop ACTIVATE.
- PREDICTION: TNN-1 has genuine action-selection machinery the original lacked. FW7 (planning) and FW6 (inquiry) are the direct tests. Note: the inquiry Pieces A+B (uncertainty reification, guide construction) are NOT in TNN-1; they are a separate experiment (currently in re-freeze after PROCESS-FAIL).

### 3.4 Contradiction and revision
- Original: in-place revision with superseded-field versioning; W5 failed via cascade.
- TNN-1: CAM-1 verify/promote/contradict ported (menu deleted), CONTRADICTS edges, demotion with retrievable history, post-promotion corroboration (E_CORROB edge type).
- PREDICTION: TNN-1 should handle contradictions better than the original, IF the eviction pathology is fixed (W5's failure was cascade, not belief-revision logic).

### 3.5 Lines of concern (honest assessment)
- TNN-1 is 1090 lines vs 586. The additional ~500 lines are: COMP-1 plan construction (~300 est.), ACT protocol (~162), CAM-1 verify/contradict, unified query path, larger workspace.
- The compression tracker (commit `f46a89e99`) records this honestly: lines negative (1555 > 586 across four builds; TNN-1 compresses to 1090).
- Micah's metric is capability per researcher-authored line, not minimum lines. The freeze re-run is the first cross-comparable capability measurement.

## 4. Draft Re-run Plan

### 4.1 Prerequisites (all must complete before any freeze work)
1. TNN-1 red team completes (worker in flight). If ATTACK-SUCCESS on integration genuineness, fix or narrow claims before freezing.
2. Inquiry re-freeze completes (worker in flight). Decision: is inquiry part of the frozen core, or a separate experiment? (Recommendation: separate; see 4.2.)
3. Governance ruling on the driver-shim question (section 5, item 1).
4. New preregistration for the re-run (section 5, item 2).

### 4.2 Scope decision: what gets frozen
OPTION A (recommended): Freeze TNN-1 cognitive core only (the 1090-line `tnn1.zag` minus test driver). Inquiry Pieces A+B remain a separate experiment. Rationale: inquiry is still in re-freeze; its inclusion would delay the freeze by an unknown amount. The freeze measures the consolidated core; inquiry can be a follow-up freeze amendment.

OPTION B: Wait for inquiry re-freeze, then freeze TNN-1 + inquiry as a single artifact. Rationale: Micah's priority 2 (learner-driven inquiry) is architecturally central. Risk: inquiry re-freeze timeline unknown; delays priority 5.

RECOMMENDATION: Option A. The freeze re-run is already valuable on TNN-1 alone (C75 fix test, composition test, action-selection test). Inquiry integration is a separate milestone.

### 4.3 Which worlds
PRIMARY: FW1-FW9 sealed battery (never executed; designed for exactly this purpose).
- FW1 is the stability baseline (must keep passing).
- FW4/FW5 are the C75 stress tests (the key discriminator for the eviction fix).
- FW9 is the general-substrate discriminator (expects FAIL; a PASS would be extraordinary).
- FW2/FW3/FW6/FW7/FW8 test the newly-ported capabilities.

SECONDARY (optional, for comparison): Re-run W1-W9 on TNN-1 to measure delta vs original 1/9. This is scientifically valuable (same worlds, different core) but doubles the run cost. Recommendation: run FW1-FW9 first; W1-W9 re-run only if FW results warrant deeper comparison.

### 4.4 What constitutes PASS
Per-world bars are defined in the FW design document (commit `200387b42`):
- FW1: 10/12 probes, 7/10 retention
- FW2: 7/8 novel-instance probes + persistent structure + reuse
- FW3: 9/10 held-out probes, learner-constructed hypothesis
- FW4: (see design doc; C75-target with validity gates)
- FW5: (see design doc; 10-link chain)
- FW6: (see design doc; inquiry)
- FW7: (see design doc; planning)
- FW8: (see design doc; grammar + retention)
- FW9: (see design doc; DAG construction; predicted FAIL)

CHALLENGE-LEVEL: The re-run is not scored as "beat 1/9." It is scored as:
1. Did FW4/FW5 pass or improve vs W4/W5? (C75 fix validation)
2. Did any construction/action world flip from FAIL to PASS? (capability delta)
3. Did FW1 stay PASS? (non-regression)
4. Capability source delta: zero throughout (frozen protocol)

### 4.5 Handling sealed FW files
- The FW world files are sealed at commit `396895595`. The blindness audit (commit `6f0eae9f2`) governs access.
- The re-run worker must NOT read FW world contents during implementation or driver-shim construction. The driver shim must be built against the PUBLIC interface (stage0/INTERFACE.md, REGIONS.md) only.
- Anti-smuggling: the frozen TNN-1 source must be grepped for FW id ranges (30000-39999) before the run, per protocol section 4.
- The run-phase worker (not the prep worker) handles seal verification, following the original run protocol (commit `97b28e6a6`).

### 4.6 Proposed sequence
1. TNN-1 red team lands → disposition (fix or narrow)
2. Governance ruling on driver shim + scope (Micah)
3. New preregistration written and frozen (prereg author worker)
4. Driver shim built (if approved) with zero cognition; anti-smuggling audit
5. Freeze record created (hashes, build verification)
6. FW1-FW9 battery executed (run-phase worker)
7. Pure-Zag rescore (independent worker)
8. Results appended to ledger; compression tracker updated

## 5. Governance Flags (for Micah)

### FLAG 1: Driver-shim question (architectural)
TNN-1's `tnn1.zag` is a test-suite binary. It has no world-file input path. To run the freeze battery, EITHER:
(a) A thin driver shim is added (world-file parsing, event dispatch, answer emission) with a frozen attestation of zero cognition, OR
(b) TNN-1 is declared not-freezable in its current form, and a world-driver variant is built as a separate milestone.

This changes the "without source edits" interpretation. The original freeze had a purpose-built `world_learn.zag` with the driver interface. TNN-1 was built for a different purpose (integration test suite). Recommendation: (a) with strict zero-cognition attestation and red-team review of the shim.

### FLAG 2: New preregistration required (procedural)
The original freeze ran under `FREEZE_PROTOCOL.md` (frozen `66e3c3f38`). A re-run on a different artifact (TNN-1 vs `world_learn.zag`) with different worlds (FW1-FW9 vs W1-W9) needs its own frozen preregistration. Who writes it: a dedicated prereg author worker, after the scope and shim decisions. This is not optional; running sealed worlds without a frozen prereg would void the results.

### FLAG 3: EXECUTE boundary (inherited, not resolved)
The TNN-1 build uses `EXECUTE(root, frame)` with the 4-op ISA `{MOVE, BRANCHEQ, INC, DEC}` per the integration prereg (commit `7fc7148ac`). Micah approved the EXECUTE class but the exact placement recommendation (`1fc77503b`, amendments A-C) remains pending his ruling. The freeze re-run does not resolve this; it inherits the ambiguity. If Micah rules against the current placement before the freeze, TNN-1 would need modification, voiding any freeze.

### FLAG 4: Inquiry scope (architectural)
Inquiry Pieces A+B are in clean re-freeze (previous wave PROCESS-FAIL). They are NOT in TNN-1. The re-run plan recommends freezing TNN-1 without inquiry (Option A). If Micah wants inquiry in the frozen core, the re-run waits for the re-freeze plus integration work.

### FLAG 5: W1-W9 re-run (methodological)
Re-running the ORIGINAL nine worlds on TNN-1 would give a direct 1/9-vs-X/9 comparison. But W1-W9 are now unsealed (results published in RUN_RESULTS.md). A TNN-1 run on W1-W9 is not adversarial; it measures delta, not capability. The FW battery is the valid instrument. Recommend FW-first, W-re-run only as supplementary.

## 6. Open Measurement Items

From the compression tracker (commit `f46a89e99`), the freeze re-run would fill:
- R_fw (sealed FW1-FW9 worlds / cognition lines) for TNN-1: the first cross-comparable capability measurement
- Integration target row: actual lines (1090, not projected 1100), actual test results
- The "cross-comparable capability pending" evidence gap would close

## Verdict: FREEZE-RERUN-PLANNED

The plan is complete. No freeze executed. Five governance flags require Micah's attention before any implementation begins. The critical path is: TNN-1 red team → governance rulings → new prereg → driver shim → freeze → FW battery → rescore.
