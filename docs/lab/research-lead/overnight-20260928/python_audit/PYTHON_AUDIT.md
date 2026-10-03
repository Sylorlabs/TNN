# Python Violation Audit

**Date:** 2026-09-30
**Auditor:** Python Violation Auditor (subagent)
**Scope:** 11 known Python usage violations against Micah's literal pure-Zag rule
**Rule:** No Python anywhere, including /tmp, diagnostics, verification, byte checks, read-only work. Disclosure does not cure use.

## Verdict: AUDIT-COMPLETE

All three kill bars pass. K1: all 11 violations catalogued with affected commits. K2: impact assessed. K3: recommendation per wave.

## Summary

| # | Wave | Commit | Nature | Disclosed in docs? | Impact | Recommendation |
|---|------|--------|--------|-------------------|--------|----------------|
| 1 | Q4 F-PARCOND | 5f56cc491 | Read-only byte check | NO (claims "Zero Python") | Peripheral | Keep + correct doc |
| 2 | Q4 reproduction | 121b6d5aa | Byte check | NO (claims "Zero Python") | Peripheral | Keep + correct doc |
| 3 | Active verification | 1c92aa353 | Read-only byte check, redone in shell | YES | Peripheral | Keep (disclosed) |
| 4 | Verification arch | 8446517e7 | Two byte-checks + no-op, redone in shell | YES | Peripheral | Keep (disclosed) |
| 5 | Form Inventor | 1b8e032c4 | /tmp diagnostic extraction | YES | Peripheral | Keep (disclosed) |
| 6 | Lifetime arena | b445614ce | /tmp compiler debugging | (wave void) | N/A | Already void |
| 7 | Verification attack | 483b0e61f | Byte check on prereg, redone in shell | YES | Peripheral | Keep (disclosed) |
| 8 | DEVANG4 | d9ebbfe6d | /tmp diagnostic patch | YES | Peripheral | Keep (disclosed) |
| 9 | Q4 adversary design | b4e9b6a14 | Process flagged; spec claims "Zero Python" | NO | Unclear | Investigate + correct |
| 10 | Continuing-transfer | 08d7c9fd5 | Setup em-dash check, replaced with shell | YES | Peripheral | Keep (disclosed) |
| 11 | Substrate-extension | 9ebd48258 | Setup em-dash check, replaced with shell | YES | Peripheral | Keep (disclosed) |

## Detailed findings

### 1. Q4 F-PARCOND byte check (5f56cc491)
Worker used Python for a read-only byte check. The committed `Q4PARCOND_RESULT.md` states "Zero Python invocations" with no disclosure. **The purity claim in the committed doc is false.** The scientific claim (7-op structure, 64/64 accuracy, 0-intervention reuse) rests entirely on Zag-produced outputs; the Python touched only verification. **Recommendation:** Keep the scientific result with explicit disclosure; correct the result doc's purity claim to disclose the byte check.

### 2. Q4 reproduction byte check (121b6d5aa)
Same pattern: worker used Python for a byte check; `Q4REPRO_RESULT.md` claims "Zero Python invocations" with no disclosure. **Purity claim false.** The reproduction (3/3 byte-identical from committed source) is valid; Python was verification-only. **Recommendation:** Keep with disclosure; correct the doc.

### 3. Active verification byte check (1c92aa353)
One read-only byte check via python3 during development. **Disclosed** in `VERIFY_ACTIVE_RESULT.md`: "redone with pure-shell grep which is the verification of record; it touched no research artifacts." **Recommendation:** Keep. Disclosure adequate.

### 4. Verification architecture checks (8446517e7)
Two disclosed read-only python3 byte-checks plus a no-op `python3 -c "pass"`. **Disclosed** in `VERIFY_ARCHITECTURE.md`, redone with shell. **Recommendation:** Keep. Disclosure adequate.

### 5. Form Inventor /tmp diagnostic (1b8e032c4)
One python3 heredoc extracted the `diagnose` function into a throwaway /tmp harness to locate a bug (byte-offset error). **Disclosed** in `FORMINVENTOR_RESULT.md`: touched only /tmp scratch (not committed, not in evidence chain); bug fixed via text edit in `inventor.zag`; rebuilt and re-verified with shell only. The Python assisted debugging but did not produce any research artifact or shape the final logic. This is debugging assistance, not Python-mirror-developed logic. **Recommendation:** Keep. Disclosure adequate.

### 6. Lifetime arena /tmp debugging (b445614ce)
Python used in /tmp during compiler debugging (V4). The wave is already ARENA-BLOCKED and void for multiple independent reasons (V2: binary hash not recorded before world generation; bug-fixed contestant frozen after generation; V4: Python use). **Recommendation:** No further action. The Python violation is documented as a contributing cause of the void. Awaits Micah's void-vs-clean-refreeze decision.

### 7. Verification attack byte check (483b0e61f)
One python3 byte-check on the prereg file during setup. **Disclosed** in `VERIFY_RESULT.md`: "redone with pure-shell grep, which is the verification of record; it touched no research artifacts." **Recommendation:** Keep. Disclosure adequate.

### 8. DEVANG4 diagnostic patch (d9ebbfe6d)
Python used to patch `/tmp/diag_d4.zag` for diagnostics. **Disclosed** in `RESULT_DEVANG4.md`: "The committed devang4.zag was NOT modified with Python." Diagnostic-only, /tmp-only. **Recommendation:** Keep. Disclosure adequate.

### 9. Q4 adversary design (b4e9b6a14)
Flagged in parent records as a Python-mirror violation during the design process. The committed `ADV_SPEC.md` claims "Zero Python" with **no disclosure of any Python use**. This is a documentation integrity gap: either the spec's purity claim is false, or the flag refers to process details not reflected in the doc. The F-PARCOND test results themselves (5f56cc491) are not invalidated because the learner ran in pure Zag, but the adversary-design process needs honest documentation. **Recommendation:** Investigate the actual Python use during adversary design; correct the spec's purity claim to disclose it. Do not treat the spec as governance-clean until corrected.

### 10. Continuing-transfer setup check (08d7c9fd5)
One setup-only python3 em-dash check on the prereg file. **Disclosed** in `CL3_RESULT.md`: "immediately replaced with a pure shell grep check... no Python was used for any source, build, execution, analysis, or verification of the research artifacts." **Recommendation:** Keep. Disclosure adequate.

### 11. Substrate-extension setup check (9ebd48258)
One python3 em-dash byte check during setup. **Disclosed** in `SE_RESULT.md`: "Immediately replaced with pure-shell LC_ALL=C grep... No Python in source, build, execution, analysis, or verification of research artifacts." **Recommendation:** Keep. Disclosure adequate.

## Cross-cutting analysis

**Pattern 1: Most violations are peripheral (8 of 11).** Read-only byte checks, em-dash checks, and /tmp diagnostics. In no case did Python generate, analyze, or shape the research logic or evidence artifacts. The scientific claims in all affected waves rest on Zag-produced outputs.

**Pattern 2: Two documentation integrity failures.** Q4 F-PARCOND (5f56cc491) and Q4 reproduction (121b6d5aa) claim "Zero Python invocations" in committed docs while workers reported Python use. These docs must be corrected. A false purity claim is worse than a disclosed violation because it defeats the audit trail.

**Pattern 3: One unresolved process question.** Q4 adversary design (b4e9b6a14) claims zero Python but was flagged for Python-mirror process violations. Needs investigation.

**Pattern 4: No Python-mirror-developed logic was adopted.** None of the 11 violations involve Python-developed logic being adopted into committed research code. The pending 6th governance ruling (whether Python-mirror-developed logic may ever be adopted) is not triggered by these violations. The Form Inventor and DEVANG4 cases are debugging assistance, not mirror development: Python was used to read/inspect, not to write logic that was adopted.

**On void-vs-keep:** Under Micah's literal rule, all 11 are violations and disclosure does not cure use. However, voiding is disproportionate where (a) the Python was verification-only or diagnostic-only, (b) the research artifacts and evidence chain are pure Zag, and (c) the violation is honestly disclosed. The proportionate response is: keep the scientific results, correct false purity claims, and maintain the violations in the governance record. Only the lifetime arena wave warrants voiding, and it is already void for independent reasons.

## Recommendations for Micah

1. **Correct two result docs:** Q4PARCOND_RESULT.md and Q4REPRO_RESULT.md must disclose the Python byte checks. Their current "Zero Python" claims are false.
2. **Investigate Q4 adversary design:** Determine what Python was used during adversary design and correct ADV_SPEC.md.
3. **No re-runs needed:** For the 8 peripheral disclosed violations, the evidence chains are pure Zag. Re-running would consume resources without changing the scientific conclusions.
4. **6th governance ruling unaffected:** None of these violations adopted Python-mirror-developed logic, so they do not force or prejudge the pending ruling.
