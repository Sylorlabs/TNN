# DOC_AUDIT.md - "Seven" vs "Six" Floor Inconsistency Audit

**Verdict: DOC-AUDIT-COMPLETE.** Two live errors found in downstream documents.
Root cause is in the frozen floor spec itself. All "seven floor tests"
references are correct.

## Ground truth

From frozen floor spec commit `f383dd11c`
(`floor_preserve/FLOOR_SPEC.md`):

- **6 capabilities enumerated:** F1, F2, F3 (freeze) + G1, G2, G3 (GW)
- **7 verification tests:** FW1, FW2, FW4, FW5, GW3 phases 1-2,
  GW7 through probe 5, GW6 primary 7 probes
- F1 covers two tests (FW1 and FW2). All other capabilities map 1:1.
  Hence 6 capabilities produce 7 tests.

Rule: "seven floor **tests**" is CORRECT. "Seven floor **capabilities**"
is INCORRECT. "Six floor **capabilities**" is CORRECT.

## "Seven floor tests": all CORRECT (8 occurrences)

| File | Line | Text |
|---|---|---|
| treadmill_guard/TREADMILL_GUARD.md | 119 | "Run the seven floor tests" |
| treadmill_guard/TREADMILL_GUARD.md | 243 | "optimizes the seven floor tests" |
| treadmill_guard/TREADMILL_GUARD.md | 266 | "The seven floor tests become" |
| guard_integration/GUARD_INTEGRATION.md | 168 | "Run the seven floor tests" |
| guard_integration/GUARD_INTEGRATION.md | 233 | "seven floor tests green" |
| revision_advice/REVISION_ADVICE.md | 210 | "the same seven floor tests must pass" |
| design_synthesis/TNN3_DESIGN_SYNTHESIS.md | 57 | "Run the seven floor tests" |
| revision_design/REVISION_DESIGN.md | 180 | "the same seven floor tests must pass" |

No action needed on any of these.

## "Six floor capabilities": CORRECT (already fixed)

- `guard_integration/GUARD_INTEGRATION.md` (fixed by issue-fixer `877d8491a`)
- `guard_integration/NAMECHECK.md` (fixed by parent commit `9e6c457cc`)

## "Seven floor capabilities": INCORRECT (remaining errors)

### Root cause (FROZEN, cannot be edited by this audit)

`floor_preserve/FLOOR_SPEC.md` (commit `f383dd11c`, FLOOR-SPEC-COMPLETE):

| Line | Text | Problem |
|---|---|---|
| 12 | "The seven capabilities below are the" | Lists 6 below |
| 168 | "The floor is seven" | Ambiguous; enumeration shows 6 |
| 234 | "Seven capabilities, four from the freeze pass set, three from the GW" | 3 freeze (F1-F3) + 3 GW (G1-G3) = 6, not 7; "four from the freeze" confuses 4 worlds (FW1/FW2/FW4/FW5) with 3 capabilities |

The spec's own commit message also says "7 capabilities (F1-F3 freeze, G1-G3 GW)"
while naming 6. This frozen-document error is the source of all downstream
propagation. Flagged for parent: a frozen spec with an internal count error
may need a transparent amendment or an erratum note, per the no-retroactive-
alteration rule.

### Downstream errors (live, fixable)

| # | File | Line | Text |
|---|---|---|---|
| 1 | treadmill_guard/TREADMILL_GUARD.md | 154 | "For each of the seven floor capabilities" |
| 2 | treadmill_guard/NAMECHECK.md | 23 | "the 7 capabilities F1-F3, G1-G3" (names 6, says 7) |
| 3 | design_synthesis/TNN3_DESIGN_SYNTHESIS.md | 11 | "the floor (7 capabilities)" |
| 4 | design_synthesis/TNN3_DESIGN_SYNTHESIS.md | 62 | "all seven floor capabilities" |
| 5 | final_tally/FINAL_TALLY.md | 27 | "7 capabilities TNN-3 must preserve" |
| 6 | prereg_check/NAMECHECK.md | 48 | "7 capabilities" |
| 7 | prereg_check/PREREG_READINESS.md | 77 | "7 capabilities" |
| 8 | synthesis_review/SYNTHESIS_REVIEW.md | 9 | "7 capabilities" |
| 9 | synthesis_review/SYNTHESIS_REVIEW.md | 31 | "the floor spec has 7: F1/F2/F3 + G1/G2/G3" (arithmetic error: 3+3=6) |

Each should read "six" / "6". None of these files is frozen.

### Ambiguous (1)

- `design_synthesis/TNN3_DESIGN_SYNTHESIS.md:132`: "the seven floor
  thresholds". "Thresholds" most plausibly refers to the 7 verification
  tests (each test carries a transcribed threshold), in which case it is
  correct. Left for the parent to confirm; not counted as an error.

### Historical references (correct as documentation, no action)

- `guard_integration/NAMECHECK.md:77,82,83,92`: documents the fix
- `integration_verify/INTEGRATION_VERIFY.md:108`: quotes the flagged issue
- `doc_audit/NAMECHECK.md`: this audit's task description

### Out of scope (1)

- `cost_curves/COSTS.md:168`: "TNN scores 0.632 with 7 capabilities".
  Different context (capability-breadth comparison against LLMs, not the
  floor spec). Not audited here.

## Recommended fix list for parent

Apply "seven" to "six" (or "7" to "6") for floor **capabilities** in:

1. `treadmill_guard/TREADMILL_GUARD.md:154`
2. `treadmill_guard/NAMECHECK.md:23`
3. `design_synthesis/TNN3_DESIGN_SYNTHESIS.md:11`
4. `design_synthesis/TNN3_DESIGN_SYNTHESIS.md:62`
5. `final_tally/FINAL_TALLY.md:27`
6. `prereg_check/NAMECHECK.md:48`
7. `prereg_check/PREREG_READINESS.md:77`
8. `synthesis_review/SYNTHESIS_REVIEW.md:9`
9. `synthesis_review/SYNTHESIS_REVIEW.md:31` (also fix the "7: F1/F2/F3 + G1/G2/G3" arithmetic)

Do NOT touch "seven floor tests" (correct). Do NOT touch the frozen
`floor_preserve/FLOOR_SPEC.md` without a transparent amendment process;
consider an erratum note instead.

## Method

- `grep -rni "seven floor"` and `grep -rn "\b7 floor"` over
  `docs/lab/research-lead/overnight-20260928/`, plus digit-form sweep
  `grep -rn "\b[67] capabilit"`.
- Ground truth established by enumerating `### F1/G1` headings in the
  frozen spec (6) and the numbered battery list in spec section 4 (7).
- Audit only: zero files edited. Paper untouched. No em dashes.
