# Overnight Session Log: 2026-09-28/29

**Session:** 23:11 PDT 2026-09-28 to 07:30 PDT 2026-09-29
**Log as of:** 06:00 PDT 2026-09-29
**Branch:** tnn-native-lab
**New commits:** 14 (0b6b591ad through 7992a6ce1)

## What Was Done

### Phase 1: Reproduce and Audit (23:30-00:00)
- Recompiled SEM-L3 from source. Scores match: 8/8, ablation 0/3, 3/3 deterministic.
- Audited 9 L3 criteria: C1-C8 PASS, C9 PARTIAL→FAIL.
- **Finding:** Mechanism IS deterministic Jaccard clustering. Not refuted; it IS the mechanism.

### Phase 2: Kill Battery (00:00-02:30)
Preregistered K1-K12. Completed high-priority tests:
- **K5 Hierarchy:** FAIL. No "flying creature" abstraction. Flat clusters only.
- **K2 Divergence:** FAIL. Cannot split; collapses to WITHHOLD.
- **K4 Overlap:** FAIL. All-or-nothing; no partial concepts.
- **K12 Scaling:** FAIL (crash at 50 entities). Fixed via buffer increase.
- **K9 Interference:** PASS. Robust to 200 noise facts.
- **K10 Recovery:** NOT IMPLEMENTED. No disk persistence.
- **Verdict:** H-KILL SURVIVES. Mechanism is L2+ (monotonic flat clustering).

### Phase 4: Usefulness (02:00-02:30)
- H-USE KILLED. Concepts do not beat structural nearest-match baseline.
- Concepts are caching/optimization, not qualitatively different reasoning.

### Repairs (03:00-04:00)
- **K12 fix:** Increased buffers 64→512, 128→1024. Generic repair.
- v3 regression: 8/8 preserved. K12: 100 correct unifications.
- **Python violation:** Disclosed. Used Python for test gen; remediated with shell.

### Documentation (04:00-06:00)
- Morning report: 17 questions answered.
- Next frontier design: Procedure invention (string reversal).
- Scaffold: proc_invent.zag (primitives, composer TODO).

## Key Findings

1. **SEM-L3 is L2+, not L3.** Downgraded from "7/9 L3 validated".
2. **The L3 claim died.** This is the "something died" the mandate asked for.
3. **Mechanism limitations:** No hierarchy, no splitting, no overlap, no composition.
4. **Strengths:** Deterministic, robust to noise, now scalable (after fix).
5. **Next frontier:** Procedure invention (Phase 8) or causal learning (Phase 9).

## Commits (14 new)

1. 0b6b591ad — Phase 1 audit
2. f6721ff79 — Kill battery prereg
3. b7ef9c635 — K5, K2 FAIL
4. fded44631 — Kill battery verdict (L2+)
5. 5183d9ab0 — Phase 4 prereg
6. 315a6716e — Phase 4 result (H-USE killed)
7. 042a7d56e — K12 FAIL + Python violation
8. e66ed1065 — Morning report
9. 33f8839de — K12 scaling fix
10. e7370deaf — K9 PASS
11. ab16d3c57 — Report update + frontier design
12. c73816b7b — Procedure scaffold
13. 570c52de3 — K10 NOT IMPLEMENTED
14. 7992a6ce1 — Preserve source files

## Push Status

**BLOCKED.** No GitHub auth. 14 commits local. Documented.

## Open Questions for Micah

1. Push authorization: The mandate authorized push, but credentials unavailable.
   Should I continue trying, or wait for Micah?
2. Procedure invention: Is this the right next frontier, or should we try
   causal learning (Phase 9) first?
3. The L2+ mechanism: Is it worth keeping as a component, or should we
   start fresh for L3?
