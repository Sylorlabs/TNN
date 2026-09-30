# PREREG_R8_ADV.md: H-ROUTER8 RED TEAM FROZEN PREREGISTRATION

**Date:** 2026-09-29
**Researcher:** H-ROUTER8 Red Team (independent subagent)
**Target:** H-ROUTER8 SURVIVES (builder result `41ec8f641`, prereg `ada8db14d`).
Builder claim: bounded L2+ structural learning with provenance diagnostics
and honest capacity signaling. Frozen kill bars K-R8-1..K-R8-4 all PASS.
**Status:** FROZEN. No amendments after this commit. Any change requires a
new prereg, not an edit.

## 0. Method

Assume the claim is false. Four attacks, each with explicit kill criteria
below. Harness: committed `router8_learn.zag` lines 1-1830 byte-verbatim
(`cmp`-verified against `git show HEAD:`) + attack-only `main()`.
The mechanism region (lines 1-1830, everything before `fn main`) is not
modified, renumbered, or paraphrased. Pure Zag throughout: fixtures,
builds, runs, greps, md5, cmp. Zero Python at any stage. No binaries
committed (builds in /tmp/r8adv only). Toolchain pinned:
`znc 2026.07.0-dev (edition 2026)`.

Task codes: TC_W()=10 WITHHOLD, TC_PL()=11 PROC_LEARN, TC_CL()=12
CAUS_LEARN, TC_PQ()=13 PROC_QUERY, TC_CQ()=14 CAUS_QUERY.
Feature domain (from `route_features`): s0 in {0,1,2,3} (pattern kind),
s1 in {1..9} (segment count, capped), s2 in {0,1,2,3} (query kind):
144 triples total.

## 1. X-R8-1: merge soundness

**Background.** The H-ROUTER7 red team recommendation R3: V2's
`[s0=1]->CAUS_LEARN` / `[s0=2]->PROC_LEARN` overgeneralized entries are
"kept harmless only by first-match ordering beneath specific rules" and
"worth a dedicated red-team pass on merge soundness." `merge_pass`
claims: "SAFE only if merged cond does not overlap any other active
entry for the action." `build_table_rest` sorts ACTIVE FX_SET entries by
specificity (constrained-var count) descending, so more-specific rules
precede more-general ones in first-match `route3`.

**White-box probes** (direct entry crafting via `new_entry` + setters,
then `merge_pass`; all entries action ACT_ROUTE()=7):

- **P1a (safety check must block).** Parent P: SUPERSEDED, mask {s0},
  cv s0=1. Children C1: ACTIVE, parent P, mask {s0,s1}, cv (1,2),
  fx var0 FX_SET(2) fp CAUS_LEARN(12), v1/v2 FX_UNCH. C2: ACTIVE,
  parent P, mask {s0,s1}, cv (1,3), identical fx to C1. Overlapping
  entry K: ACTIVE, parent -1 (root), mask {s0,s1}, cv (1,2), fx var0
  FX_SET fp PROC_LEARN(11) (DIFFERENT effect, overlapping cond).
  Call `merge_pass(W,1)`. **KILL iff** a merge fires: C1 or C2 becomes
  non-ACTIVE, or any new entry is created (nent increases), or K's
  state changes. The safety check must see K overlapping the merged
  parent cond [s0=1] and refuse.
- **P1b (control: check is not vacuous).** Same as P1a but K has cond
  [s0=2&s1=2] (no overlap with [s0=1]). **FAIL (attack fails) iff**
  no merge fires; the merge MUST fire here, creating merged entry M
  with parent cond [s0=1], C1/C2 SUPERSEDED.
- **P1c (semantic preservation).** After P1b's merge, run
  `compile_thresholds` + `build_table_rest` on the world and probe
  `route3` on (1,2,0), (1,3,0) (ex-children triples) and (1,9,0)
  (merged-general region): all must return CAUS_LEARN(12).
  **KILL/DOWNGRADE iff** any probe returns a different task or -1.
- **P1d (black-box natural merge).** Teach: (1,1,0)->PL, (1,2,0)->CL
  (split on s1: [s1=1]->PL, [s1=2]->CL), then (1,1,0)->CL again
  (contradiction at [s1=1]; contest/resolve). If resolve supersedes the
  PL episode, [s1=1] and [s1=2] become identical-effect siblings and
  `merge_pass` should merge them. Report the outcome verbatim; then
  `check_route`-style probes on the taught triples.
  **KILL iff** a merge fires and any taught triple misroutes
  afterwards. If no merge fires naturally, P1d is INCONCLUSIVE
  (reported as such, not a pass).

**Kill rule X-R8-1:** P1a merge fires (unsound merge) -> H-ROUTER8
KILLED on merge soundness. P1c misroute -> DOWNGRADED (merge changes
routing semantics). P1b must fire (else the harness is broken and P1a
is void). P1d inconclusive-without-merge is reported, not counted.

## 2. X-R8-2: warning spoofing (TABLE-NON-TOTAL)

**Background.** R8-2: on refused fallback append, emit loud
TABLE-NON-TOTAL instead of a phantom rule line. Claim: "a route3 -1 at
capacity is now declared, never silent."

- **P2a (false negative: -1 without warning).** By code analysis:
  `route3` returns -1 iff no rule matches. If any all-ANY rule is
  compiled, `hasany`=1 and route3 is total. If `hasany`=0 and nrt<24,
  the fallback append succeeds (rt_add only refuses at nrt>=24),
  contradiction. Hence -1 is reachable only if nrt==24 and hasany==0,
  which is exactly the warning condition. Empirical check: in the
  frozen V2 replay section, confirm the warning fired exactly once and
  CAP-PROBE -1 coincides with it. **KILL iff** a constructible world
  yields route3 -1 with zero TABLE-NON-TOTAL in its build trace.
  Expected result: HOLD (impossibility argued + V2 confirms).
- **P2b (false positive: warning on a total table).** White-box:
  craft 24 ACTIVE FX_SET entries, hasany==0, whose conds jointly cover
  all 144 domain triples: covers [s0=0],[s0=1],[s0=2],[s0=3] (sp=1,
  tasks W/PL/CL/PQ) + 20 fillers [s0=0&s1=v] v=1..9, [s0=1&s1=v]
  v=1..5, [s0=2&s1=v] v=1..3, [s0=3&s1=v] v=1..3 (sp=2, tasks = cover
  task of their s0). Run build_table_rest; count TABLE-NON-TOTAL
  (expect 1: nrt==24, hasany==0, fallback refused); then probe route3
  on all 144 triples and count -1s. **CONFIRMED BOUNDARY (not a kill)**
  iff warning fires AND zero probes return -1: the warning is
  sufficient but not necessary for non-totality (conservative).
  The warning text says "may return -1", so a false positive does not
  falsify any frozen bar. **KILL iff** warning does NOT fire here
  (nrt==24, hasany==0, fallback refused, but silent).

**Kill rule X-R8-2:** P2a constructible -1-without-warning -> KILLED.
P2b no-warning-on-refused-fallback -> KILLED. P2b warning-on-total
table -> CONFIRMED BOUNDARY (reported, not a kill).

## 3. X-R8-3: capacity gaming

**Background.** `rt_add` refuses past 24 rules (no eviction);
`build_table_rest` inserts most-specific first, so the least-specific
rules are dropped at capacity. Threshold rules (Phase 1b) compile
before entry rules. R8 explicitly declines cap-raising/eviction as
future work; the defense is honest signaling.

- **P3a (junk displacement).** Black-box via teach: curriculum L of
  10 legitimate specific triples (s0=0, s1=1..9 distinct tasks
  alternating PL/CL, plus one more), then junk curriculum J of 20
  further legitimate teaches at distinct triples with sp=3-eligible
  shapes... NOTE: route_features yields at most sp=3 via (s0,s1,s2)
  all constrained; s2 in {1,2,3} requires single-segment lines with
  field kinds. Concretely: J marks are single-segment "X>Y"-shaped
  lines with s0 in {0..3}, s1 in {1..9} via ';'-repetition is
  multi-segment (s2=0)... s2!=0 needs nseg==1. So J: single-segment
  lines "aa>bb" variants with field_kind -1/3/other -> s2 in {1,2,3},
  s1=1 always, s0 in {0..3}. These give entries [s0=k&s1=1&s2=q]
  (sp=3). L: multi-segment marks (s2=0) giving sp<=2 entries.
  After L+J, build the table: expect 24 rules, TABLE-NON-TOTAL fired,
  and some L triples now probe -1 (their sp=2 rules displaced by sp=3
  junk). **KILL iff** any taught triple (L or J) probes to a WRONG
  task (silent corruption, not -1). -1-with-warning on displaced L
  triples is the disclosed boundary -> HOLD with boundary confirmed.
- **P3b (threshold displacement).** Curriculum inducing threshold
  rules for s0v in {1,2} (clean s1 boundary per compile_thresholds)
  PLUS enough entry rules to exceed 24 total. Verify: threshold rules
  occupy the first slots; dropped rules are the least-specific entry
  rules; TABLE-NON-TOTAL fires iff fallback refused. **KILL iff** a
  taught triple misroutes (wrong task) or -1 occurs without warning.

**Kill rule X-R8-3:** silent wrong-task routing induced by capacity
pressure -> KILLED. -1 only where the warning fired -> HOLD (boundary
confirmed, gaming degrades gracefully as disclosed).

## 4. X-R8-4: regression (no silent changes)

- Rebuild `router8_learn.zag` from `git show HEAD:`-extracted source,
  run 3x, `cmp` byte-identical to committed `ROUTER8_RAW_OUTPUT.txt`
  (md5 `bc4019ee7e44438a839de5c6584fc4c8`).
- Re-verify K-R8-1 (in-code CAP- lines), K-R8-2 (external greps:
  1 TABLE-NON-TOTAL, 0 phantom fallback lines in section, 24 gated
  entry emits, 2 anchored ^TABLE OVERFLOW), K-R8-3 (zero FAIL lines),
  K-R8-4 (3/3 identical).
- Diff `router7_learn.zag` vs `router8_learn.zag`: must contain ONLY
  the frozen R8-1..R8-4 change categories.
**KILL iff** any mismatch: raw differs, any frozen bar fails, or the
diff shows non-frozen changes.

## Verdict rules

- Any KILL above -> H-ROUTER8 KILLED (or DOWNGRADED where specified).
- All attacks fail -> SURVIVES. Confirmed boundaries are reported as
  boundaries, not kills.
- Classification of the target remains bounded L2+; no L3 claimed or
  tested.

## Files and commits

New files (owned by this red team), all under
`docs/lab/research-lead/overnight-20260928/router8_adversary/`:
- `PREREG_R8_ADV.md` (this file)
- `r8_adv.zag` (harness: mechanism lines 1-1830 verbatim + attack main)
- `R8_ADV_RAW.txt`, `R8_ADV_RAW_R2.txt`, `R8_ADV_RAW_R3.txt`
- `R8_ADV_RESULT.md`

Commit plan: this prereg committed ALONE before any attack code exists.
Result commit afterwards with pathspec-restricted staging of exactly the
owned files. `git merge-base --is-ancestor` check before the result
commit. No push. No em dashes in loop documentation (byte-checked).
