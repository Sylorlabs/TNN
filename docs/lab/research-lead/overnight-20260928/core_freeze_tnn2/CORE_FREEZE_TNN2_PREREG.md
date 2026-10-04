# CORE-FREEZE-TNN2 Preregistration

Date: 2026-09-30. Status: PREREG-FROZEN.
Governance: Micah's Core Freeze workflow (second cycle). Root-cause basis `ed38121d4`. TNN-2 build `f4de7ff46` (TNN2-BUILD-PASS). Reproduction `fdf1fa626` (TNN2-REPRO-PASS).

## 1. Mandate

Freeze TNN-2 and evaluate against sealed adversary-generated worlds
FW1-FW9 with no source edits after world exposure. This is the
second freeze cycle, testing whether the three architectural changes
(runtime 4-op construction, miss-to-act inquiry loop, generic
revision) fix the five failure clusters from the TNN-1 freeze
(FW SCORE 4/9).

Workflow: BUILD GENERATION → FREEZE → SEALED ADVERSARIAL TEST →
ROOT-CAUSE ANALYSIS → NEXT GENERATION.

## 2. Frozen artifacts

### TNN-2 (contestant)
- Source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  Lines: 1591 (base 1328 + 263; not compressed per Micah's ruling, separate axis)
- Binary: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin`
  SHA-256: `6044f91f8fe35e307e1d6f73a4ee73bffb930fa0a16a9c899048a086d0d5f77b`
  Built with pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
- Build commit: `f4de7ff46` (TNN2-BUILD-PASS; 46/46 tests, 3/3 byte-identical)
- Repro commit: `fdf1fa626` (TNN2-REPRO-PASS; byte-identical recompile)

### Driver shim (to be built under this prereg)
- Purpose: Transport world events into TNN-2's public interface; return TNN-2 outputs/actions.
- Zero-cognition requirement: same as CORE-FREEZE-TNN1. The shim may NOT interpret world semantics, reason, solve tasks, inject task identities, construct cognitive structures, select policies, or translate failures into answers.
- If significant cognition is required in the shim, that is itself an architecture failure (F-FZ1).
- TNN-2's public interface: `ev_observe`, `ev_query`, `ev_act` (same as TNN-1; `tnn2_init` replaces `tnn1_init`).
- Shim source and binary hashes frozen independently before evaluation.
- K1 ordering: This prereg strictly precedes the shim implementation.

### Compiler/toolchain
- Pinned: `src/tools/toolchain/znc_linux_x86_64_abed8aa1` (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`)

### Scorer
- Pure Zag. Frozen before evaluation. Same methodology as CORE-FREEZE-TNN1.

### FW1-FW9 seal
- Same sealed assets. No contestant cognition edits after world exposure.

### Architectural metrics (frozen baseline)
- TNN-2 source lines: 1591
- TNN-2 cognition lines: to be measured (same method as TNN-1's 641)
- F-INT1 ceiling: 1200 lines (EXCEEDED; compression fail recorded, not waived; separate axis)
- Modes: 0. Bridges: 0. Handlers: 0. New opcodes: 0.

### Interpretation rules
- Primary comparison: TNN-2 FW SCORE vs TNN-1 FW SCORE (4/9).
- Report FW SCORE (primary) and OLD-WORLD REGRESSION SCORE (supplementary) separately.
- Per-cluster analysis: which of the 5 TNN-1 failure clusters (arithmetic, planning, novel utterance, relational DAG, degenerate inquiry) does TNN-2 fix?
- Do not combine old-world results into the fresh sealed primary score.
- Do not add new opcodes in response to FW failures.

## 3. Kill bars

- K-FZ2-1 (ordering): This prereg commit strictly precedes shim implementation, which strictly precedes evaluation.
- K-FZ2-2 (no cognition edits): TNN-2 source/binary hashes verified before and after; exact match.
- K-FZ2-3 (shim purity): Driver shim contains zero cognition. Verified by source inspection.
- K-FZ2-4 (determinism): 3 runs byte-identical per world.
- K-FZ2-5 (seal integrity): FW1-FW9 accessed only through authorized evaluator.

## 4. Falsifiers

- F-FZ2-1: Shim requires cognition (architecture failure).
- F-FZ2-2: TNN-2 hashes change after world exposure (integrity failure).
- F-FZ2-3: FW seal broken (evaluation invalid).

## 5. What success looks like

The three changes target specific clusters:
- Change 1 (runtime construction) targets FW3, FW8, FW9, half of FW7.
- Change 2 (miss-to-act inquiry) targets FW6 and half of FW7.
- Change 3 (generic revision) targets the revision ceiling; may not move FW scores directly but future-proofs Change 1.

A FW SCORE above 4/9 with no regressions on FW1/FW2/FW4/FW5 would
confirm the architectural diagnosis. A score at or below 4/9, or
regressions on previously passing worlds, would falsify the
root-cause analysis and require re-clustering.

## Verdict: CORE-FREEZE-TNN2-PREREG-FROZEN
