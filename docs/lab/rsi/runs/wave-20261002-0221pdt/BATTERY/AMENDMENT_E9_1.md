# EXECUTOR-AMENDMENT-E9-1: M3-E2 world redesign (orphan-cell poisoning)

**Status:** FROZEN (this file). Frozen before the redesigned m3e2_world.txt
is generated and before the M3 block is re-run. The original
PREREG_BATTERY_E9.md is NOT modified; this amendment records the delta.

**Date:** 2026-10-02. Wave wave-20261002-0221pdt, lane BATTERY.

## 1. Defect found (world-design defect, not a mechanism repair)

The frozen M3-E2 world (section 5.8 of the prereg) is WORLD-INVALID as
built: its validity probe idx3 (post-revision QUERY (56101,56509,56113))
returned 56103, not the predicted 56113. Root cause, verified by
bisection:

- MAP_B's promotion trial (idx2, QUERY (56101,56519,56104)) tries the
  2-hop candidate [56101,56102,56103] before the winner
  [56101,56103,56104]. The rejected candidate's assembled cells
  (SETREG type 101 with DEP edges to its licensing facts) are never
  freed: they persist as orphans in learner state.
- When the contradiction OBSERVE (56102,56502,56113) arrives,
  `t2_revise_graph`'s stale-cell lookup scans ALL edges globally and
  takes the LAST type-101 node with a DEP edge to the contradicted
  fact. The orphan's DEP edge was created later than MAP_A's live
  SETREG, so the lookup patches the orphan graph, re-executes MAP_A's
  untouched root ("success" with the old value), and re-teaches the old
  value. MAP_A is never actually revised.
- This is a genuine frozen-mechanism bug (orphan trial cells poison the
  revision lookup), recorded here as a finding. But it is NOT the bug
  M3-E2 was designed to test (downstream propagation), and it breaks
  the world's validity probe. Scoring the bar on this run would test
  orphan poisoning, not propagation. The world is therefore redesigned,
  not salvaged.

## 2. Redesign (3-link MAP_A, contradict the terminal third link)

The orphan's DEP edges point to the rejected candidate's facts (links 1
and 2 of MAP_A's chain). Contradicting link 3 (which no rejected
candidate includes, because the k=2 accept short-circuits before k=3
runs) keeps the stale lookup clean. New event stream
(`m3e2_world.txt`, supersedes prereg section 5.8):

```
OBSERVE 56101 56501 56102
OBSERVE 56102 56502 56103
OBSERVE 56103 56503 56105
OBSERVE 56105 56510 56104
QUERY 56101 56509 56105
QUERY 56101 56509 56105
QUERY 56101 56519 56104
OBSERVE 56103 56503 56113
QUERY 56101 56509 56113
OBSERVE 56113 56510 56114
OBSERVE 56801 56800 56811
OBSERVE 56802 56800 56812
OBSERVE 56803 56800 56813
OBSERVE 56804 56800 56814
QUERY 56101 56519 56114
QUERY 55801 55800 55811
QUERY 55802 55800 55812
```

Probes: idx0,1 MAP_A promotion (56105); idx2 MAP_B promotion (56104;
trial tries [56101,56102,56103] reject then [56101,56105,56104]
accept); idx3 post-revision validity (56113); idx4 bar (56114);
idx5,6 collateral (M3-E1 distractors, taught values).

Mechanism walk (frozen, predicted): idx0 k=3 accepts
[56101,56102,56103,56105] (k=2 decoy [56101,56102,56103] rejects,
leaving orphans with DEP to links 1-2 only). idx2 as above. idx3:
contradiction of link 3 (56103,56503,56105 -> 56113) finds MAP_A's
SETREG#3 cleanly (no orphan DEP to link 3); terminal link,
re-execution succeeds; MAP_A ans=56113, (56101,56509,56113) taught;
MAP_B untouched (no DEP to the contradicted fact). New downstream
(56113,56510,56114) plain teach. 4 distractors (correction 2). idx4:
MAP_B's promoted fact (56101,56519,56104) still active -> exact hit
56104, expected 56114 -> FAIL. idx5,6 hits.

Predicted: idx0,1,2,3 PASS; idx4 FAIL (56104, stale downstream);
idx5,6 PASS. E-K12 FAIL.

Degenerate walks (new stream): D0: -2; validity fails ->
WORLD-INVALID. D1: idx0 most recent OBSERVE (56105,56510,56104) ->
56104 != 56105 -> WORLD-INVALID. D2: no (56101,56509) OBSERVE -> -2 ->
WORLD-INVALID. No degenerate passes E-K12.

## 3. What is unchanged

- E-K12's bar text is unchanged (validity HIT 0,1,2,3; probe 4
  correct). The barspec `HIT 0 1 2 3` / `NEED 1 4` is unchanged.
- The adversarial intent is unchanged (downstream propagation through
  stacked MAPs). The material-difference note is unchanged.
- No mechanism source was touched (frozen hashes re-verified at
  re-run). This amendment is a world-design correction, not a
  mechanism repair and not a bar weakening: the bar is identical, the
  world now actually engages the designed scenario.

## 4. Re-run plan

Regenerate m3e2_world.txt from the stream above, update
WORLD_MANIFEST.sha256, re-run the full M3 block 3 times from fresh
state (E1->E2->E3, persistent within block), re-score. M1/M2 blocks
are unaffected (no contradictions there; orphans cannot affect them).
