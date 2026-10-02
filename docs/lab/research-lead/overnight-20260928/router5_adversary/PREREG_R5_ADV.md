# PREREG_R5_ADV: H-ROUTER5 Red Team (frozen)

**Date:** 2026-09-29
**Status:** FROZEN (before any attack code or execution)
**Target:** H-ROUTER5 SURVIVES claim (`ROUTER5_RESULT.md`, `router5_learn.zag`)
**Stance:** Assume the claim is false. Attacks below are designed to fire.

## Target recap (from source)

`audit_task_family` anchors per content type on query marks: for items with
s0=0, s1=1, task in {PQ, CQ}, it collects the task family per s2 (qk).
If at least one anchor exists for a qk AND all agree on one family,
anchor[qk] = that family; else anchor[qk] = UNKNOWN (0). It then checks
learn items (s1>=2, task in {PL, CL}): s0=1 items must match anchor[1],
s0=2 items must match anchor[2]. Returns bitmask (bit0 s0=1, bit1 s0=2).
Disclosed evasions: coherent re-labeling of query anchors (11 items), and
anchor-missing curricula (silent by design).

## Attacks

### X-R5-1: Coherent re-labeling (boundary confirmation)

Fixture `run_coherent_relabel`: the X-R4-1 SWAP learns (s0=1 multi-seg
str>str -> CL; s0=2 multi-seg iii>ii -> PL) PLUS re-marked queries:
"hello"/"world" -> CQ, "1,0,0"/"0,0,0" -> PQ. WITHHOLD items unchanged.

Expected per disclosure: tfam=0, mergers_mask=0, sfanom=0 (full silence).
Corruption check: route3("zz>yy;xx>ww") must be CL (honest: PL) and
route3("3,3,3>3,2;4,4,4>4,3") must be PL (honest: CL), proving the
evasion is not toothless.

- PASS (boundary confirmed): tfam=0 AND both probes show swapped routing.
- FINDING (unexpected, report as downgrade-grade): tfam!=0 on this
  curriculum (false positive on a coherent curriculum), or routing NOT
  corrupted (evasion toothless).

### X-R5-2: Anchor games

**X-R5-2a (anchor-missing):** SWAP learns, all four queries taught as
WITHHOLD. Expected: tfam=0 with "task-family-anchor-missing". Boundary
per disclosure. PASS iff tfam=0.

**X-R5-2b (anchor pollution, the sharp attack):** SWAP learns + honest
queries + TWO added items: "zzz" (plain string, features (0,1,1)) marked
CQ, and "9,9,9" (triple, features (0,1,2)) marked PQ. The added marks
disagree with the honest anchors, so a1=0 and a2=0 (UNKNOWN) by the
all-agree rule, and both family checks are skipped.

- DOWNGRADE FIRES iff: tfam=0 AND mergers_mask=0 AND sfanom=0 on this
  curriculum (full system evasion via 2 added items, a vector not in the
  disclosed evasions). The disclosed evasions are coherent re-labeling
  (11 re-marked items) and anchor-missing; disagreement-pollution is
  neither.
- If any diagnostic fires, X-R5-2b FAILS (attack defeated, report why).

**X-R5-2c (single-sided pollution + summary honesty):** s0=1-only swap
(s0=1 learns -> CL, s0=2 learns honest CL) + honest queries + "zzz"->CQ.
Expected mechanics: a1=0 (disagreement) so the s0=1 check is skipped;
s0=2 CL matches a2=CAUS; tfam=0. The merger is expected to still fire
(this is the X-R1 shape), so this is NOT a system-level evasion.

- FINDING (honesty defect, supports downgrade): tfam=0 AND the run emits
  "no-task-family-inconsistency" while a s0=1 swap is present but
  unchecked. The summary line overstates what was verified.
- If the merger does NOT fire either, escalate: full evasion, stronger
  downgrade.

**X-R5-2d (single-segment coverage probe):** honest curriculum +
"ab>ba" (features (1,1,0), s1=1) marked CL. The family check requires
s1>=2, so it skips this item by spec.

- NO HOLE iff the mark-merger fires (CL rules then span s0=1 and s0=2).
- HOLE (downgrade-grade) iff merger=0 AND tfam=0 AND sfanom=0: a routing-
  changing mark (W->CL on single-seg string pairs) invisible to every
  diagnostic.

### X-R5-3: False-positive hunt

**X-R5-3a (intended flag):** string queries PQ, string-pair learns CL
(intentional cross-family assignment), triple queries CQ, triple learns
CL. Per disclosure the diagnostic SHOULD flag this for researcher review.
PASS iff bit0 fires. (Firing here is intended, not a kill.)

**X-R5-3b (novel legitimate):** honest + extra WITHHOLD items and an
extra qk=3 query ("12a" -> W, features (0,1,3), cannot anchor). PASS iff
tfam=0, merger=0, sfanom=0.

**X-R5-3c (conflicted duplicate):** honest + "abc>cba;xy>yx" taught a
second time as CL (same features (1,2,0), genuinely conflicting marks).
PASS iff bit0 fires (flagging genuine mark conflict is correct).

- DOWNGRADE FIRES iff the diagnostic fires on a curriculum whose
  learn/query families AGREE per content type (true false positive).
  X-R5-3a firing does not count (disclosed intended behavior).

### X-R5-4: Regression and source audit

- Rebuild `router5_learn.zag` from the committed source and run: output
  must be byte-identical to committed `ROUTER5_RAW_OUTPUT.txt`
  (md5 0bb790e8adfc5cf22786356c72254f8a).
- Diff `router5_learn.zag` vs `router4_learn.zag`: only the new
  `audit_task_family` (+ helpers already present), its call sites, the
  SWAP fixture, and main() sections may differ.
- Verify the four sections report tfam 0, 1, 1, 3 as documented.
- INTEGRITY FAILURE (downgrade/invalid as appropriate) on any mismatch.

## Verdict rules

- H-ROUTER5 is DOWNGRADED if X-R5-2b fires (new 2-item full evasion), or
  X-R5-2d shows a hole, or X-R5-3 finds a true false positive, or X-R5-4
  finds an integrity mismatch. X-R5-2c's honesty defect supports but does
  not alone carry a downgrade.
- X-R5-1 and X-R5-2a confirming are boundaries, not kills.
- If all attacks fail, report H-ROUTER5 SURVIVES this red team.

## Governance

Pure Zag. No Python at any stage. Harness = byte-verbatim copy of
`router5_learn.zag` mechanism lines with only main() replaced (verified
by cmp). Only adversary-owned files staged. No em dashes in loop docs.
