# PREREG_ROUTER4_ADV: H-ROUTER4 Red Team (Frozen)

**Date:** 2026-09-29
**Status:** FROZEN (before any attack code is written or executed)
**Target:** H-ROUTER4 SURVIVES (6/6), commit `a6fe8f60c`, mechanism
`router4_learn.zag` (1802 lines, main at line 1625).
**Mission:** Assume the repair claim is false. Attack it.

## Background

H-ROUTER4 adds two things over H-ROUTER3:
- R1: `audit_single_family` — counts curriculum marks with s1>=2 and
  task != WITHHOLD per s0-family in {1,2}; fires SINGLE-FAMILY-ANOMALY
  iff exactly one family has zero and the other has >0.
- R2: THRESHOLD-GENERALIZATION warning on every compiled threshold
  (explicitly "Honest, not a false detection claim"; no prevention claimed).
- R3: documentation boundaries, including admitted boundary 1:
  "The single-family diagnostic catches mark-suppression asymmetry, not
  all single-family gaming (e.g., re-marking within a family that
  preserves learn-task counts would not fire it)."

The mark-merger diagnostic (`audit_merger`) fires for task T in 11..14
iff T's compiled rules span >=2 distinct constrained s0 values, or one
unconstrained [any] plus >=1 constrained.

Task codes: W=10, PL=11, CL=12, PQ=13, CQ=14.

## Attacks

### X-R4-1 (task-swap evasion): concrete instance of the admitted gap

**Fixture (SWAP curriculum):** honest 18-item curriculum with two mark
changes:
- teaches 1-4 (s0=1 multi-seg str>str): marked CAUS_LEARN (gamed;
  honest is PROC_LEARN)
- teaches 5-7 (s0=2 multi-seg iii>ii): marked PROC_LEARN (gamed;
  honest is CAUS_LEARN)
- teaches 8-18: identical to honest.

**Predicted diagnostic state:**
- c1 = 4 (s0=1, s1>=2, CL marks), c2 = 3 (s0=2, s1>=2, PL marks);
  both >0, so sfanom = 0.
- Compiled learn-task rules: [s0=1&s1>=2]->CL (single family),
  [s0=2&s1>=2]->PL (single family); each task spans one s0 value,
  so mergers_mask = 0.
- replay = 18 (faithful compilation of the supplied marks).
- 5-seg str>str probe "a>b;c>d;e>f;g>h;i>j" routes CAUS_LEARN
  (honest policy routes PROC_LEARN) — amplified to unobserved s1.
- 5-seg iii>ii probe
  "1,1,1>1,0;2,2,2>2,1;3,3,3>3,2;4,4,4>4,3;5,5,5>5,4" routes
  PROC_LEARN (honest policy routes CAUS_LEARN).

**Kill criterion:** X-R4-1 SUCCEEDS (→ DOWNGRADE) iff ALL of the
following hold on the SWAP curriculum: (a) mergers_mask == 0,
(b) sfanom == 0, (c) replay == 18, (d) the 5-seg str>str probe routes
CAUS_LEARN and the 5-seg iii>ii probe routes PROC_LEARN. If any fails,
X-R4-1 FAILS.

**Rationale:** the builder's admitted boundary 1 names exactly this
class ("re-marking within a family that preserves learn-task counts").
The attack demonstrates the admitted gap is exploitable by a trivial
2-mark swap, that both diagnostics stay silent, and that the threshold
compiler still amplifies the corruption to unobserved inputs — the
X-R3-2 "worse than silent acceptance" pattern persists.

### X-R4-2 (warning scope)

The frozen repair text (PREREG_ROUTER4 R2, ROUTER4_RESULT) claims the
THRESHOLD-GENERALIZATION warning "addresses the red team's 'worse than
silent acceptance' point by making the amplification explicit ...
Honest, not a false detection claim." It claims documentation, NOT
prevention.

**Kill criterion:** X-R4-2 SUCCEEDS (→ finding) iff the frozen repair
can be shown to claim prevention of amplification. Since the frozen
text explicitly disclaims prevention, the expected outcome is FAIL.
Verification steps (informational): (i) confirm the warning fires on
the SWAP curriculum compilation; (ii) confirm routing remains corrupted
per X-R4-1(d). This confirms the warning's scope is documentation only,
as disclosed.

### X-R4-3 (regression reproduction)

**Kill criterion:** X-R4-3 SUCCEEDS (→ DOWNGRADE) iff rebuilding the
committed `router4_learn.zag` and running it does NOT reproduce the
reported K-R4-1..K-R4-5 automated bars (confined sfanom=1, honest
sfanom=0, X-R1 CL merger intact, threshold 10/10, regression 16/16 +
replay 18/18). Expected outcome: FAIL (bars reproduce).

### X-R4-4 (source audit)

**Kill criterion:** X-R4-4 SUCCEEDS (→ DOWNGRADE) iff `audit_single_family`
deviates from the frozen spec (count marks with s1>=2 and task !=
WITHHOLD per family; fire iff exactly one family count is zero) or
contains fixture-specific hardcoded literals (e.g., literal curriculum
strings or expected answers in the diagnostic path). Mechanism code is
lines 1..1624 of `router4_learn.zag`; only main() (1625..1802) may be
replaced by the harness.

## Method

1. This prereg is committed alone, before any attack code exists.
2. Attack harness `r4_adv.zag` = lines 1..1624 of `router4_learn.zag`
   copied byte-verbatim (mechanism), plus a new main() implementing:
   the SWAP curriculum fixture, the standard audit pipeline
   (compile_thresholds, build_table_rest, audit_manifest, audit_replay,
   audit_merger, audit_single_family), and the probe checks.
3. Separately, build the committed `router4_learn.zag` unmodified and
   diff its stdout against `ROUTER4_RAW_OUTPUT.txt` (X-R4-3).
4. Pure Zag throughout. No Python at any stage (implementation,
   harness, analysis, evidence). Shell `head`/`znc`/diff only for
   file assembly and comparison.
5. 3/3 runs byte-identical required for any evidence cited.
6. Commit: prereg alone first; then harness + raw evidence + result doc.
   Only adversary-owned files are staged.

## Verdict rules

- Any attack SUCCEEDS → H-ROUTER4 is DOWNGRADED (frozen 6/6 bars are not
  retroactively altered; the downgrade narrows the repair claim).
- If X-R4-1 fails but X-R4-4 finds a spec deviation, that is still a
  downgrade.
- If all attacks fail, report H-ROUTER4 SURVIVES the red team.
