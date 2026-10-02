# Ledger Cycle 12: Draft Claim List

Prepared by the Ledger Cycle 12 Preparer. **Draft only. Do NOT append to the canonical ledger yet.**

Ledger baseline: 117 claims (C117 at `e89255aba`).

## Ready now (completed, verified commits)

### C118: COMP-1-BUILD-COMPLETE

- **Commit:** `170e39424`
- **Verdict:** BUILD-PASS
- **Claim:** Pure-Zag implementation of compositional machinery in `comp1_build/`: 879 lines, three frozen plan templates (CHAIN-2, GATHER-n, ITERATE-UNTIL), generic step executor, bootstrap miss-policy. 10/10 tests pass, byte-identical across 3 runs. P4 three-hop via plan-structure composition (template marker 4 = COMPOSED), not a fourth template. E-ruling structural: `mp_build`/`mp_build_compose` do not take `expected`; F2 verified byte-identical construction traces with expected masked/unmasked.
- **K1:** prereg `4f6f0c5c8` verified ancestor of `170e39424` (confirmed via `git merge-base --is-ancestor`).
- **K2:** zero handlers/semantic cases/modes/bridges/new core ops; exactly 3 templates.
- **K3:** pure Zag; Step 0 guard recorded (python stubbed to exit 127).
- **Note:** bootstrap miss-policy 157 source lines vs 150 projection (+7 variance on a projection, not a kill bar; documented honestly in BUILD_REPORT.md).

### C119: DEVINT-CLA2-BUILD-COMPLETE

- **Commit:** `35f9500b2`
- **Verdict:** BUILD-PASS
- **Claim:** Pure-Zag implementation of the 11-stage developmental integration on the CLA-2 workspace (`devint_cla2_build/`): 1212 lines, one continuing process handling segmentation, concept formation (GROUP nodes), learned rules, contradiction, inquiry, demotion, memory pressure, and delayed reuse with no resets. All 11 stages pass with exact frozen numbers. B1 persistence, B2 stage function, B3 blindness (source inspection: `feed_episode` takes only episode bytes), B4 interference (17/17 recognition), B5 delayed reuse (zero re-teaching S10 to S11). 3/3 byte-identical determinism.
- **K1:** prereg `f24063bcb` verified ancestor of `35f9500b2` (confirmed via `git merge-base --is-ancestor`).
- **Note:** builder caught and fixed two genuine bugs during construction (boundary-spanning substrings inflating lexicon; PROTECT anchor node 2 evicted by eviction routine). Both fixed before commit.
- Per pipeline, this is BUILD-PASS only; no SURVIVES or L3 claim made.

### C120: INTEGRATION-SCOUT-COMPLETE

- **Commit:** `c0e99a601`
- **Verdict:** EXPLORATORY
- **Claim:** Analysis-only scout for one-system integration. Duplication inventory: ~475 lines of workspace machinery written 4 times across CLA-2, CAM-1, ACT, COMP-1. CLA-2 workspace format selected (40-byte nodes, 16-byte edges, 12 edge types; already contains ACT protocol + MAP nodes). CAM-1's `eval_body` menu is deleted, not ported (per C111 red-team finding); `verify`/`promote`/`contradict` port; propose becomes COMP-1 plan construction. Unified event flow specified: one teach path, one query path with miss-policy dispatch, one ACT protocol. Projected ~1100 cognition lines vs 1555 across four separate implementations. Integration prereg shape specified with K1-K5 kill bars (including hard 1200-line ceiling and source-scan ban on CAM-1 menu reappearing) and F-INT1 through F-INT4 falsification.

### C121: INQUIRY-SCOUT-COMPLETE

- **Commit:** `b4853a9f7`
- **Verdict:** EXPLORATORY
- **Claim:** Analysis-only scout specifying the learner-driven inquiry gap. ACT read path (Piece C) is built and red-teamed, but two learner-side pieces are missing: Piece A (uncertainty reification: no learner-side process creates UNCERTAINTY nodes from -2 admissions; scaffolding does it) and Piece B (inquiry guide construction: no learner-side process performs D2 derivation; scaffolding does it). Both must be generic-primitive workspace processes or K-ACT2 fails. Four-phase discriminating experiment specified; Phase 4 is novel-domain transfer with zero researcher mapping (L3-flavored test). Prereg shape P-INQ1 through P-INQ5, F-INQ1 through F-INQ5, K-INQ1 through K-INQ4.

### C122: ACT-BID-ALIGNED

- **Commit:** `75a9b0e04`
- **Verdict:** REMEDIATION-COMPLETE
- **Claim:** Implementation of the C112 red-team finding. ACT `bid()` now counts incoming evidence edges only, matching CLA-2 `evcount()`; integration spec A3 claim ("ACT reuses the same function") is now true. Rationale per `5257ac268` analysis: outgoing SUPPORTS is a guide's claim about the world, not evidence for the guide; correctness captured directionally via incoming CONFIRMS/CONTRADICTS. Options (b) spec amendment and (c) hybrid rejected. Source diff limited to `bid()` (2 lines). Rebuilt with pinned znc. 24/24 tests PASS, byte-identical across 3 runs, no test changes needed.

### C123: GUARD-AUDIT-COMPLETE

- **Commit:** `e0a842962`
- **Verdict:** EXPLORATORY
- **Claim:** Read-only audit of all 7 Python process incidents this cycle. All 7 were process-level (accidental shell fragments, setup aids, inspection helpers); none implemented research logic, scoring, or analysis. Zero incidents since guard formalization in `0525377f3`. Workers now actively prevent invocation (restricted PATHs, stub scripts). 6 of 7 self-disclosed. Incident 7 cleanly re-frozen (C110). Recommendations: (1) fix composition scout NAMECHECK.md record (contradicts ledger C98), (2) codify restricted-PATH/stub-scripts as mandatory Step 0, (3) add pre-execution shell review for the `python3 -c "pass"` stray-fragment pattern. No structural strengthening required.

### C124: STATUS-DOC-PROCESS-FAIL

- **Commit:** `6e4a9479f`
- **Verdict:** PROCESS-FAIL
- **Claim:** Status consolidation document (STATUS-CONSOLIDATED, 248-line human-readable snapshot). **Per Micah's ruling: this documentation wave is PROCESS-FAIL.** The worker invoked `python3 -c` for a mechanical character replacement (em dash to colon in four section headers of documentation). No research logic or scientific content was produced via Python; the worker self-disclosed in NAMECHECK.md. Per Micah: the absolute ban applies; this documentation wave is process-contaminated; it does NOT contaminate unrelated scientific experiments whose research logic remained pure Zag. The guard is kept absolute; no new prompt changes required. The STATUS.md document stands as an artifact but carries the process-fail flag for its wave.

## Not ready (depend on in-flight workers)

- **Integration prereg:** worker active; claim pending completion of the integration prereg commit.
- **Inquiry prereg:** worker active; claim pending completion of the inquiry prereg commit.
- **DEVINT-CLA2 red team:** worker active; claim pending adversarial audit result.
- **MUL builder:** worker active; claim pending implementation and test results.

## Ledger-state summary for cycle 12

- New claims ready now: 7 (C118 through C124).
- Resulting claim count when appended: 124.
- New SURVIVES: zero.
- L3 achieved anywhere: still zero.
- New BUILD-PASS: 2 (C118, C119).
- New REMEDIATION-COMPLETE: 1 (C122).
- New PROCESS-FAIL: 1 (C124, documentation wave per Micah's ruling).
- New EXPLORATORY: 3 (C120, C121, C123).
- Pending in-flight claims: 4 (integration prereg, inquiry prereg, DEVINT-CLA2 red team, MUL build).
- Composition scout NAMECHECK.md record correction (guard audit recommendation 1) is an open governance item; no claim assigned.
