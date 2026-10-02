# CORE-FREEZE-TNN1 Preregistration

Date: 2026-09-30. Status: PREREG-FROZEN.
Governance: Micah's five Core Freeze rulings, 2026-09-30.

## 1. Mandate

Freeze the current TNN-1 architecture (ACT-remediated, 1328 lines) and
evaluate it against sealed adversary-generated worlds FW1-FW9 with no
source edits, recompilation, handlers, semantic cases, or modes after
world exposure.

Workflow: BUILD GENERATION → FREEZE → SEALED ADVERSARIAL TEST →
ROOT-CAUSE ANALYSIS → NEXT GENERATION.

Do not move the freeze target while evaluation is being prepared.

## 2. Frozen artifacts

### TNN-1 (contestant)
- Source: `docs/lab/research-lead/overnight-20260928/tnn1_act_remed_build/tnn1_act.zag`
  SHA-256: `d3895083c9f8b5b0f82ac1c74b11eb2c90341059fcf9e37be30b9c085de0cc6b`
  Lines: 1328 (exceeds frozen 1200-line F-INT1 ceiling; ARCHITECTURE-COMPRESSION FAIL recorded, not waived)
- Binary: `docs/lab/research-lead/overnight-20260928/tnn1_act_remed_build/tnn1_act_bin`
  SHA-256: `efa36ecd0604a8e3f650e0fef715a25c2383f271f20349c6e26a8f91116507a1`
  Built with pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Commit: `293bf662b` (ACT-REMED-BUILD-PASS; 41/41 tests, 3/3 byte-identical)

### Driver shim (to be built under this prereg)
- Purpose: Transport world events into TNN-1's public interface; return TNN-1 outputs/actions.
- Zero-cognition requirement: The shim may NOT interpret world semantics, reason, solve tasks, inject task identities, construct cognitive structures, select policies, or translate failures into answers.
- If significant cognition is required in the shim, that is itself an architecture failure.
- The shim source and binary hashes will be frozen independently before evaluation.
- K1 ordering: This prereg strictly precedes the driver shim implementation.

### Compiler/toolchain
- Pinned: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- No other compilers or interpreters for research code.

### Scorer
- Pure Zag. Frozen before evaluation.
- Scores FW1-FW9 (primary) and W1-W9 (supplementary regression) separately.
- Do not combine old-world results into the fresh sealed primary score.

### FW1-FW9 seal
- Sealed pure-Zag evaluator assets. FW blindness audit PASS.
- No contestant cognition edits after world exposure.

### Architectural metrics (frozen baseline)
- TNN-1 cognition lines: 641 (53 functions) per remeasurement `6c40f4238`
- Source lines: 1328 (ACT-remediated)
- F-INT1 ceiling: 1200 lines (EXCEEDED; compression fail recorded)
- Modes: 0. Bridges: 0. Handlers: 0. Semantic cases: 0.
- R_test: 5.46 per 100 cognition lines (35 tests / 641 lines)

### Interpretation rules
- Report FW SCORE (primary) and OLD-WORLD REGRESSION SCORE (supplementary) separately.
- Capability and architectural compression are separate axes.
- After the freeze, if capability improved substantially, the next experiment may test whether equivalent capability can be retained while compressing back below the ceiling.
- Do not add new opcodes in response to FW failures.

## 3. EXECUTE placement (approved)

EXECUTE is accepted as a protected-core domain-neutral ISA primitive.

Rationale: EXECUTE supplies the ability to run learner-authored
executable structure. It does not choose what structure to build.

The ISA is now frozen. Do not add new opcodes in response to FW failures.

Documented deviations (recorded, not erased):
- Execution budget is currently a code literal (`while(st<1000)`) rather than learner-visible state as specified.
- The specified INC/DEC kind guard is absent from the implementation.

These are documented deviations, not current placement falsifiers.

## 4. Inquiry scope

FREEZE CURRENT TNN-1 NOW. Do not delay the benchmark to incorporate
newly completed mechanisms.

The clean inquiry mechanism (149 cognition lines, all bars pass,
commit `18ed3331c`) remains valid research and may enter the NEXT
architecture generation if not already contained in the frozen TNN-1
artifact.

## 5. World methodology

FW1-FW9 are PRIMARY. W1-W9 are supplementary regression/context only.

Do not combine old-world results into the fresh sealed primary score.

Report:
- FW SCORE (0-9, primary)
- OLD-WORLD REGRESSION SCORE (0-9, supplementary)

## 6. MUL Rung B status

Preserve as BUILD-PASS only (commit `a2223cc11`).

The two-level learner construction (primitive basis → learner-built
ADD → learner-built MUL using CALL) is important. However revision
remains 0/4, so do not promote to L3.

After the Core Freeze run, high priority is generic revision of
learner-created executable structures, not another
multiplication-specific patch.

## 7. Kill bars

- K-FZ1 (ordering): This prereg commit strictly precedes driver shim implementation, which strictly precedes evaluation. Verified by git merge-base --is-ancestor.
- K-FZ2 (no cognition edits): No modifications to TNN-1 source or binary after world exposure. Hashes verified before and after.
- K-FZ3 (shim purity): Driver shim contains zero cognition per section 2. Verified by source inspection.
- K-FZ4 (determinism): 3 runs byte-identical per world.
- K-FZ5 (seal integrity): FW1-FW9 accessed only through the authorized evaluator. No contestant pre-exposure.

## 8. Falsifiers

- F-FZ1: Shim requires cognition to function (architecture failure).
- F-FZ2: TNN-1 hashes change after world exposure (integrity failure).
- F-FZ3: FW seal broken (evaluation invalid).

## Verdict: CORE-FREEZE-TNN1-PREREG-FROZEN
