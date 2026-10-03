# Python Incident Audit 2

**Date:** 2026-09-30
**Auditor:** Python Incident Auditor (subagent)
**Scope:** All 16 commits on `tnn-native-lab` since guard audit `e0a842962`
**Method:** Shell and git only. Zero Python invocations during audit.
**Verdict:** PYTHON-AUDIT-2-COMPLETE

## Summary

**New incidents since guard audit:** 1 (the 9th overall)

**Total Python incidents to date:** 9

**Guard effectiveness:** Mixed. Self-disclosure is working (the 9th incident was
self-disclosed by the worker). Restricted PATH adoption is weak (only 1 of 16
workers used a true safebin). Record consistency needs attention (the 9th
incident's NAMECHECK contradicts its BUILD_REPORT).

## Commits Audited (16)

All commits between `e0a842962` (exclusive) and HEAD (inclusive), in chronological
order:

1. `b4853a9f7` - Inquiry scout (analysis only)
2. `75a9b0e04` - ACT bid alignment (source edit + znc build)
3. `35f9500b2` - DEVINT-CLA2 build (pure Zag)
4. `67f92ed4f` - Record correction (composition scout NAMECHECK fix)
5. `6a3a1f69c` - Ledger cycle 12 prep (draft)
6. `366b97da2` - MUL progress monitor (read-only)
7. `29772b206` - Bundle v14 prep (read-only assessment)
8. `7fc7148ac` - Integration prereg (design document)
9. `f46a89e99` - Compression tracker (analysis)
10. `04ac028fb` - Inquiry prereg (design document)
11. `b81ca69ed` - Ledger cycle 12 (append C118-C124)
12. `fbf14f73a` - MUL-1 Rung A build (pure Zag)
13. `a5ccb100d` - DEVINT-CLA2 red team (read-only attack)
14. `fac9875b0` - C1 harness fix (shell scripts)
15. `0323b97d5` - TNN-1 integration build (pure Zag, 1090 lines)
16. `396ecafa4` - Inquiry build (pure Zag, with disclosed incident)

## Incident 9: Inquiry Build (396ecafa4)

**What happened:** The worker invoked `python3` once to text-patch a `/tmp`
scratch copy of the source (inserting diagnostic print statements). The scratch
copy was deleted without execution.

**Scientific impact:** None. No Python was used for research computation,
scoring, or result generation. The implementation (`inquiry.zag`) was written
via file tools, compiled with the pinned znc, and all reported results come
from the pure-Zag binary.

**Disclosure quality:** Good, with one inconsistency.
- BUILD_REPORT.md contains a "Toolchain Incident (disclosure)" section that
  fully describes the invocation, its scope, and its non-impact on results.
- NAMECHECK.md claims "Zero invocations during this wave" in its Step 0
  section, which contradicts the BUILD_REPORT disclosure.
- The worker self-disclosed in its final report to the parent agent.

**Adjudication:** PROCESS-FAIL per the Worker Toolchain Guard (invocation =
automatic PROCESS-FAIL for the wave). The parent agent has marked this wave
PROCESS-FAIL. A clean re-freeze worker has been spawned.

**Record inconsistency flagged:** The NAMECHECK.md Step 0 section should be
amended to acknowledge the incident, matching the BUILD_REPORT disclosure.
This is the same class of record error as the composition scout incident 5
(false "No Python invoked" in NAMECHECK), which was corrected at `67f92ed4f`.

## Note on Incident 8: STATUS Doc (6e4a9479f)

The STATUS doc incident (`python3 -c` for mechanical em-dash character
replacement in documentation) is chronologically BEFORE the guard audit commit
(22:19:30 vs 22:19:48 UTC, 18 seconds earlier) but is NOT listed among the
guard audit's 7 catalogued incidents. The guard audit report lists incidents
1-7 as: C55 OpScope, L3A trace build, C67 learner-dev, C77 L3A-trace red team,
composition scout, frontier scout, C1 driver.

This suggests the guard audit was finalized before the STATUS doc incident
was known, or it was missed. The parent agent's task description treats the
STATUS doc as the 8th incident. For consistency, this audit adopts that
numbering: STATUS doc = 8th, inquiry build = 9th.

The STATUS doc wave was marked PROCESS-FAIL per Micah's ruling (scoped to the
documentation wave only; does not contaminate unrelated pure-Zag science).

## Clean Commits (15 of 16)

The following 15 commits show zero Python invocations, with Step 0 guard
records documenting non-use:

- `b4853a9f7` (inquiry scout): Analysis only. Guard documents non-use.
- `75a9b0e04` (ACT bid fix): Source edit + znc build. "Zero Python invocations
  this wave (source edit + znc build + binary test only)."
- `35f9500b2` (DEVINT-CLA2): "Forbidden executable invoked: none. Wave status:
  not PROCESS-FAIL."
- `67f92ed4f` (record correction): Documentation fix. Guard documents non-use.
- `6a3a1f69c` (ledger 12 prep): "No Python invoked at any step."
- `366b97da2` (MUL monitor): Read-only. "Zero invocations in this monitoring wave."
- `29772b206` (bundle v14 prep): Read-only. "Zero Python invocations."
- `7fc7148ac` (integration prereg): Design doc. "Guard status: PASS. Not PROCESS-FAIL."
- `f46a89e99` (compression tracker): Analysis. "This wave is not PROCESS-FAIL."
- `04ac028fb` (inquiry prereg): Design doc. "Zero invocations of python3."
- `b81ca69ed` (ledger 12): "Zero invocations of python3 or python during this wave.
  This wave is NOT process-failed."
- `fbf14f73a` (MUL build): **Used restricted safebin PATH.** "Under safebin PATH:
  `python3` = ABSENT, `python` = ABSENT." This is the gold standard.
- `a5ccb100d` (DEVINT red team): Read-only attack. Guard documents non-use.
- `fac9875b0` (C1 harness fix): Shell scripts only. "Zero Python invocations this wave."
- `0323b97d5` (TNN-1 build): "Zero Python invocations. Zero other interpreter
  invocations."

All 7 committed Zag source files (`.zag`) and 2 shell scripts (`.sh`) were
scanned for Python references. The only matches are comments stating "No Python"
or "Pure Zag"; no actual Python code or invocations in any committed source.

## PROCESS-FAIL Wave Handling

**Incident 8 (STATUS doc, 6e4a9479f):**
- Marked PROCESS-FAIL per Micah's ruling.
- Scoped to documentation wave only.
- Does not contaminate unrelated pure-Zag scientific experiments.
- Ledger C124 records this correctly.

**Incident 9 (Inquiry build, 396ecafa4):**
- Marked PROCESS-FAIL per Worker Toolchain Guard.
- Scientific result (all frozen bars pass) is uncontaminated but has no standing
  until cleanly re-frozen.
- Clean re-freeze worker spawned with zero-tolerance guard.
- NAMECHECK inconsistency (claims zero invocations, contradicts BUILD_REPORT)
  should be corrected as part of re-freeze or via separate record correction.

**Contamination check:** No PROCESS-FAIL wave's output has been used as input
to a clean wave's scientific claims. The inquiry re-freeze is building from the
frozen prereg (`04ac028fb`), not from the PROCESS-FAIL implementation.

## Guard Effectiveness Assessment

### What is working

1. **Self-disclosure:** Both new incidents (8 and 9) were self-disclosed by the
   workers. This is the disclosure pattern Micah trusts. The guard audit noted
   "strong self-disclosure" and it continues.

2. **Step 0 records:** All 16 commits include NAMECHECK.md with Step 0 guard
   records. Compliance is 100%.

3. **No scientific contamination:** All 9 incidents to date are process-level.
   None involved Python in research computation, scoring, or result generation.
   The pure-Zag scientific results stand.

4. **Restricted PATH (when used):** The MUL builder's safebin approach
   (`~/workspace/mul_safebin` with python3 ABSENT) is the gold standard and
   proves the technique works.

### What needs improvement

1. **Restricted PATH adoption is weak.** Only 1 of 16 workers (MUL builder)
   used a true restricted PATH where python3 was absent. The other 15 documented
   that "surgical PATH removal is not possible without breaking git/sha256sum/grep"
   and relied on documented non-use instead.

   The MUL builder proves it IS possible (safebin with symlinks to allowed tools).
   The "not possible" claim in other NAMECHECKs reflects effort, not technical
   impossibility.

   **Recommendation:** Make safebin-style restricted PATH the default for builder
   workers (those compiling/running Zag). Documentation workers may continue
   with documented non-use given their lower risk profile.

2. **Record consistency.** The inquiry build's NAMECHECK claims "Zero invocations"
   while its BUILD_REPORT discloses an invocation. This is the same error class
   as composition scout incident 5. Workers should update NAMECHECK if an
   incident occurs mid-wave, not leave the Step 0 "zero invocations" claim
   standing alongside a disclosure elsewhere.

   **Recommendation:** If a worker invokes a forbidden executable mid-wave, it
   must amend its NAMECHECK.md Step 0 section before commit, not just disclose
   in BUILD_REPORT or final report.

3. **Guard audit timing.** The guard audit (e0a842962) missed the STATUS doc
   incident (6e4a9479f) that occurred 18 seconds earlier. Audits should include
   a final `git log` check immediately before commit.

## Incident Tally

| # | Commit | Description | Disclosure | Scientific Impact |
|---|--------|-------------|------------|-------------------|
| 1 | (pre-audit) | C55 OpScope displacement | adequate | none |
| 2 | (pre-audit) | L3A trace original build | adequate | none |
| 3 | (pre-audit) | C67 learner-dev P12 | adequate | none |
| 4 | (pre-audit) | C77 L3A-trace red team | adequate | none |
| 5 | (pre-audit) | Composition scout | poor (fixed at 67f92ed4f) | none |
| 6 | (pre-audit) | Frontier scout | adequate | none |
| 7 | (pre-audit) | C1 driver | adequate | none |
| 8 | 6e4a9479f | STATUS doc char replacement | self-disclosed | none (docs only) |
| 9 | 396ecafa4 | Inquiry build scratch patch | self-disclosed | none |

**Total:** 9 incidents. All process-level. Zero scientific contamination.

## Recommendations

1. **Adopt safebin as default for builders.** The MUL builder's approach works.
   Document the pattern in AGENTS.md.

2. **Fix inquiry NAMECHECK inconsistency.** Amend the Step 0 section to
   acknowledge the incident, or handle as part of the clean re-freeze.

3. **Audit timing.** Future guard audits should run `git log` immediately
   before commit to catch last-second incidents.

4. **No guard strengthening required beyond the above.** The core mechanism
   (Step 0 check + self-disclosure + PROCESS-FAIL on invocation) is working.
   The issue is adoption of the strongest prevention (restricted PATH), not
   the guard rules themselves.
