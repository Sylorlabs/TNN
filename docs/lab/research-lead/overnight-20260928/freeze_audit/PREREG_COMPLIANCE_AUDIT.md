# Freeze Prereg Compliance Audit

**Auditor:** Freeze Prereg Compliance Checker
**Date:** 2026-10-01
**Verdict:** PREREG-COMPLIANCE-AUDIT-COMPLETE

## 1. Documents Audited

| Document | Location | Status |
|----------|----------|--------|
| Frozen prereg | `ce1a7c5f8:docs/lab/research-lead/overnight-20260928/core_freeze_tnn2/CORE_FREEZE_TNN2_PREREG.md` | CORE-FREEZE-TNN2-PREREG-FROZEN |
| Evaluator draft | `docs/lab/research-lead/overnight-20260928/core_freeze_tnn2_eval/FREEZE_REPORT.md` | Untracked, on disk |
| TNN-1 reference | `docs/lab/research-lead/overnight-20260928/core_freeze_tnn1_eval/FREEZE_REPORT.md` | Committed `7bde57f52` |
| Seal integrity | Commit `0c97a669a` | SEAL-INTEGRITY-CHECK-COMPLETE |

## 2. Frozen Prereg Requirements (ce1a7c5f8)

### Kill Bars

- **K-FZ2-1 (ordering):** Prereg commit strictly precedes shim implementation, which strictly precedes evaluation.
- **K-FZ2-2 (no cognition edits):** TNN-2 source/binary hashes verified before and after; exact match.
- **K-FZ2-3 (shim purity):** Driver shim contains zero cognition. Verified by source inspection.
- **K-FZ2-4 (determinism):** 3 runs byte-identical per world.
- **K-FZ2-5 (seal integrity):** FW1-FW9 accessed only through authorized evaluator.

### Falsifiers

- **F-FZ2-1:** Shim requires cognition (architecture failure).
- **F-FZ2-2:** TNN-2 hashes change after world exposure (integrity failure).
- **F-FZ2-3:** FW seal broken (evaluation invalid).

### Interpretation Rules

- Primary comparison: TNN-2 FW SCORE vs TNN-1 FW SCORE (4/9).
- Report FW SCORE (primary) and OLD-WORLD REGRESSION SCORE (supplementary) separately.
- Per-cluster analysis: which of the 5 TNN-1 failure clusters does TNN-2 fix?
- Do not combine old-world results into the fresh sealed primary score.
- Do not add new opcodes in response to FW failures.

### Success Criteria

"A FW SCORE above 4/9 with no regressions on FW1/FW2/FW4/FW5 would confirm the architectural diagnosis. A score at or below 4/9, or regressions on previously passing worlds, would falsify the root-cause analysis and require re-clustering."

Change targets:
- Change 1 (runtime construction) targets FW3, FW8, FW9, half of FW7.
- Change 2 (miss-to-act inquiry) targets FW6 and half of FW7.
- Change 3 (generic revision) targets the revision ceiling; may not move FW scores directly.

## 3. Draft Claims vs Prereg Requirements

### Inconsistency A: Arithmetic Error (FW SCORE 5/9 vs 4 passes)

**Draft states:**
- Verdict section: "FW SCORE (primary, sealed): 5/9 (TNN-1: 4/9)"
- Results table: FW1 PASS, FW2 PASS, FW3 FAIL, FW4 PASS, FW5 PASS, FW6 FAIL, FW7 FAIL, FW8 FAIL, FW9 FAIL
- Summary line: "FW SCORE: 5/9 (FW1, FW2, FW4, FW5)"

**Fact:** The table lists 4 PASS (FW1, FW2, FW4, FW5) and 5 FAIL. The parenthetical "(FW1, FW2, FW4, FW5)" names 4 worlds.

**Prereg requirement:** The prereg requires honest reporting of FW SCORE. While it does not explicitly state "SCORE = count of PASS", this is definitional. The FW SCORE is the number of worlds passed out of 9.

**Violation:** The draft claims 5/9 while documenting 4/9. This is an arithmetic error that must be corrected to 4/9.

**Impact:** Under the prereg's success criteria, "A FW SCORE above 4/9... would confirm the architectural diagnosis. A score at or below 4/9... would falsify the root-cause analysis and require re-clustering." The difference between 5/9 and 4/9 is the difference between confirming and falsifying the diagnosis. This is not a minor typo.

### Inconsistency B: COMPLETE Verdict with PENDING Kill Bar

**Draft states:**
- Verdict: "FREEZE-EVAL-COMPLETE"
- K-FZ2-4 (determinism): "PENDING (3 runs in progress)"

**Prereg requirement:** K-FZ2-4: "3 runs byte-identical per world." This is a kill bar. All kill bars must be resolved before a final verdict.

**Violation:** A verdict of FREEZE-EVAL-COMPLETE cannot be issued while K-FZ2-4 is PENDING. The prereg defines K-FZ2-4 as a requirement, not an optional check.

**Required action:** The verdict must be downgraded to IN-PROGRESS (or equivalent) until K-FZ2-4 is verified PASS. If determinism fails, the verdict must reflect that.

### Inconsistency C: Incomplete Supplementary Reporting

**Draft states:**
- "OLD-WORLD REGRESSION SCORE (supplementary): pending"
- "Per-Cluster Fix Analysis (TNN-1 -> TNN-2): (pending W results)"

**Prereg requirement:**
- "Report FW SCORE (primary) and OLD-WORLD REGRESSION SCORE (supplementary) separately."
- "Per-cluster analysis: which of the 5 TNN-1 failure clusters does TNN-2 fix?"

**Assessment:** These are incomplete, not incorrect. The prereg requires them to be reported, but does not forbid a phased report. However, combined with Inconsistency B, they reinforce that the evaluation is not complete.

The per-cluster analysis is particularly important because the prereg's success criteria depend on it: "A score at or below 4/9, or regressions on previously passing worlds, would falsify the root-cause analysis and require re-clustering." With FW at 4/9 (corrected), the per-cluster analysis determines whether this falsifies the diagnosis or reveals a more nuanced pattern.

## 4. FW6 Interpretation

**Draft states:** "FW6 | FAIL | Responder withheld reveal (post-diagnostic ACT was CHOICE 30, not contract's literal CHOICE 0); treatment 0/3"

**TNN-1 reference:** "FW6 | FAIL (degenerate) | B1 3/3, B2 0/3 numerically met; B4 FAIL. All CHOICE lines constant 'CHOICE 0' (5/5). Adversary reading: WORLD-FAIL. Literalist reading: numeric pass."

**Analysis:**

In TNN-1, FW6 failed because the action mechanism was degenerate: all CHOICE lines were constant "CHOICE 0". The adversary reading was WORLD-FAIL (the world requires contingent inquiry, which a constant action cannot provide).

In TNN-2, the draft notes the ACT was CHOICE 30, not the contract's literal CHOICE 0. The inquiry red team (commit `4e329c772`) established that TNN-2's guide action is hardcoded to 30 (lines 805-808), and `ev_act` returns this constant.

The draft correctly marks FW6 as FAIL. The note about CHOICE 30 vs CHOICE 0 is explanatory: TNN-2's constant differs from TNN-1's constant, but it is still a constant. The FW6 world tests for discriminating inquiry (Change 2's target: "miss-to-act inquiry targets FW6"). A constant action, whether 0 or 30, cannot express contingent inquiry.

**Prereg compliance:** The FAIL verdict for FW6 is consistent with the prereg. Change 2 was predicted to target FW6, and FW6 remains FAIL. This is a valid result, not a scoring error.

**No action required** on FW6 scoring. The draft's FAIL is correct.

## 5. Required Reconciliation Steps

The evaluator must complete the following before the report can be committed with a COMPLETE verdict:

1. **Correct the arithmetic:** Change "FW SCORE: 5/9" to "FW SCORE: 4/9" in both the Verdict section and the results summary. Verify the parenthetical lists match the count.

2. **Resolve K-FZ2-4:** Complete the 3-run determinism verification. Update K-FZ2-4 from PENDING to PASS (with evidence) or FAIL (with explanation). Do not issue COMPLETE verdict until resolved.

3. **Complete W battery:** Run W1-W9 and report OLD-WORLD REGRESSION SCORE. The prereg requires this to be reported separately from the primary FW SCORE.

4. **Complete per-cluster analysis:** For each of the 5 TNN-1 failure clusters (arithmetic, planning, novel utterance, relational DAG, degenerate inquiry), state whether TNN-2 fixes it, with evidence from FW and W results.

5. **Verify post-eval hashes:** The draft's hash table shows "Post-eval: pending" for all four artifacts. Complete the post-evaluation hash verification required by K-FZ2-2.

6. **Downgrade verdict until complete:** Change "FREEZE-EVAL-COMPLETE" to "FREEZE-EVAL-IN-PROGRESS" (or remove the verdict line) until steps 1-5 are complete.

## 6. What Is NOT a Violation

- **FW6 FAIL:** Correct. TNN-2's constant CHOICE 30 is as degenerate as TNN-1's constant CHOICE 0 for FW6's purposes.
- **Seal integrity:** Verified by independent checker (commit `0c97a669a`). K-FZ2-5 PASS is valid.
- **K-FZ2-1 ordering:** Draft claims PASS with `git merge-base --is-ancestor` evidence. No reason to dispute.
- **K-FZ2-2 pre-eval:** Draft claims PASS with hash verification. Post-eval pending is noted, not a violation yet.
- **K-FZ2-3 shim purity:** Draft claims PASS, references frozen shim build. No reason to dispute.

## 7. Summary

| Issue | Severity | Prereg Citation |
|-------|----------|-----------------|
| FW SCORE 5/9 vs 4 documented passes | **Critical** | Interpretation: honest FW SCORE reporting; Success criteria depend on >4/9 vs <=4/9 |
| COMPLETE verdict with K-FZ2-4 PENDING | **Critical** | K-FZ2-4: "3 runs byte-identical per world" (kill bar) |
| W results pending | **Major** | "Report FW SCORE (primary) and OLD-WORLD REGRESSION SCORE (supplementary) separately" |
| Per-cluster analysis pending | **Major** | "Per-cluster analysis: which of the 5 TNN-1 failure clusters does TNN-2 fix?" |
| Post-eval hashes pending | **Major** | K-FZ2-2: "hashes verified before and after; exact match" |
| FW6 FAIL (CHOICE 30) | **Not a violation** | Correct application of FW6 criteria |

**Overall assessment:** The draft contains a critical arithmetic error and prematurely claims completion. The underlying evaluation work (FW battery runs, hash verifications, seal checks) appears sound, but the report cannot be committed in its current state. The evaluator must reconcile the inconsistencies listed in Section 5.

## Verdict: PREREG-COMPLIANCE-AUDIT-COMPLETE
