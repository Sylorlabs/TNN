# PREREG H-CAUSAL-UNIFIED5 RED TEAM (FROZEN)

**Date:** 2026-09-29
**Adversary:** H-CAUSAL-UNIFIED5 Red Team (independent)
**Target:** H-CAUSAL-UNIFIED5 SURVIVES (builder: K-CU5-1..K-CU5-4 PASS).
The repair is one 9-line guard in `merge_pass`: a seed entry whose
parent is ST_CONFL is skipped, so tombstone-parented entries
(carve-outs) never participate in merge sibling grouping.
**Assumption under test:** the claim is false. The guard is either
incomplete (some tombstone-parented merge path remains), unsound
(it breaks a legitimate merge class), or its structural premise is
wrong (a ST_CONFL parent can stop being ST_CONFL, or an entry can
be parented by an ST_ACTIVE entry).
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python
at any stage. Shell only for build orchestration, grep, cmp, md5sum.

## Structural facts established by code reading (frozen)

- `en_st_set` to ST_ACTIVE occurs only in `new_entry` (fresh
  entries) and in `amb_update` (ST_AMBIG to ST_ACTIVE via split).
  No path transitions ST_CONFL to ST_ACTIVE. Tombstones stay
  ST_CONFL by code, not just by design claim.
- ST_SUPER is terminal: no path leaves ST_SUPER.
- Every entry parent is one of: -1 (fresh or merged), ST_CONFL
  (carve-out, terminal), ST_SUPER (split child, terminal), or a
  previous merge parent (induction; base cases are the three
  above). No entry is ever parented by an ST_ACTIVE entry.
- `merge_pass` creates the merged entry with parent = the seed's
  parent and cond = the parent's cond. The CU5 guard is evaluated
  on the seed before sibling gathering; sibling grouping requires
  same parent, so skipping the seed is complete for its group.
- `new_entry` refuses at 32 entries with an explicit
  "ERROR: entry capacity (32) exhausted" trace; all four call
  sites (carve, split, merge, learn fresh path) handle -1 without
  silent mutation. Contest capacity (8) refusal is likewise
  explicit and marks the entry ST_CONFL.

## Attack X-CU5-1: second/third-generation carves under re-conflicted carved tombstones

Purpose: the repair was validated only for first-generation
carves. Re-conflicting a carved entry creates a new tombstone
whose carves are also tombstone-parented; verify the guard holds
across generations and that the documented X-CU4-3b re-carve
behavior is preserved.

Exact construction (action 2, fresh W):
1. Flood F (20 episodes, verbatim from cu5_adv.zag):
   "0,0,0,2>0,0,0;0,0,0,2>1,1,1;0,0,1,2>0,0,0;0,0,1,2>1,1,1;0,1,0,2>0,0,0;0,1,0,2>1,1,1;0,1,1,2>0,0,0;0,1,1,2>1,1,1;1,0,0,2>0,0,0;1,0,0,2>1,1,1;1,0,1,2>0,0,0;1,0,1,2>1,1,1;1,1,0,2>0,0,0;1,1,0,2>1,1,1;1,1,1,2>0,0,0;1,1,1,2>1,1,1;2,0,0,2>0,0,0;2,0,0,2>1,1,1;2,0,1,2>0,0,0;2,0,1,2>1,1,1"
   Expect nct=8 (else setup failed, attack void).
2. "2,0,0,2>0,0,0" then "1,0,0,2>0,0,0": carve E1 at (2,0,0) and
   E2 at (1,0,0), both parent=T (entry 0, ST_CONFL), fx (0,0,0).
3. "2,0,0,2>1,1,1": re-conflicts E1 (find_entry(2,2,0,0) < 0).
4. "2,0,0,2>1,1,1" twice more: first absorb 2-vs-2 stable (nent
   unchanged), second 2-vs-3 re-carves E3 (parent=E1) with winner
   (1,1,1). This is the frozen X-CU4-3b behavior.
5. "2,0,0,2>0,0,0": re-conflicts E3. Then "2,0,0,2>0,0,0" twice
   more: 2-vs-2 stable, then 2-vs-3 re-carves E4 (parent=E3,
   gen 3) with winner (0,0,0).
6. Entry dump. Queries: (2,0,0) predicts (0,0,0) via E4;
   (1,0,0) predicts (0,0,0) via E2; (0,0,0) withholds with live
   contradiction in T.

Frozen kill criteria:
- KILL-K1: any "MERGE" trace in this run whose merged entry is
  not mask 7, or any ACTIVE entry parented by a ST_CONFL entry
  with mask != 7 (a tombstone-parented carve broadened).
- KILL-K2: query at (2,0,0) returns r=1 with an outcome other
  than (0,0,0) while E4 exists (prediction through live
  contradiction), or query at (0,0,0) returns r=1 while the
  tombstone still holds both live outcomes.
- DOWNGRADE-D1: step 4 or 5 does not reproduce the frozen
  X-CU4-3b pattern (nent stable at 2-vs-2, +1 with correct
  flipped winner at 2-vs-3). The repair must not change
  re-adjudication behavior.

## Attack X-CU5-2: entry-capacity pressure from unmergeable carves

Purpose: the guard trades merges for entries. Farm tombstones
and carves toward the 32-entry cap and verify exhaustion stays
explicit (the X-CU3 guarantee) rather than becoming silent.

Exact construction (fresh W):
1. Flood F on action 2 (nct=8 expected).
2. For action a in {0,1,3}, for k in {0,1,2,3}:
   "(k,0,0),a>0,0,0" then "(k,0,0),a>1,1,1" (contradiction at
   contest cap marks the fresh entry ST_CONFL explicitly) then
   "(k,0,0),a>0,0,0" (absorb; 2-vs-1 carves, winner (0,0,0),
   parent = the new tombstone).
3. Record nent. For a bounded number of further re-conflict /
   re-carve cycles on carved entries (same pattern as X-CU5-1
   steps 3-4), continue until nent=32 or 12 cycles are done.
4. Probe: one fresh learn at a new state of action 0, and one
   absorb+adjudicate carve attempt on an existing tombstone.
5. Query every probed state and every farmed tombstone state.

Frozen kill criteria:
- KILL-K3: any capacity refusal without the explicit
  "ERROR: entry capacity (32) exhausted" trace (silent drop).
- KILL-K4: any query returns r=1 at a state whose only
  evidence was refused at capacity, or any farmed tombstone
  loses a live contradiction silently (checked with the
  adv_live_contra helper: both outcomes still live).
- PASS (boundary, not kill): explicit ERROR traces on all
  refusing calls, all probed/refused states withhold (r=0),
  all tombstone contradictions intact. Record the nent at
  which refusal first occurs.

## Attack X-CU5-3: merge-class interaction matrix

Purpose: verify the guard neither over-blocks (legitimate
merges die) nor under-blocks (some tombstone-parented path
merges). Entries built by direct white-box construction
(new_entry + field setters, all real mechanism functions);
merge_pass called directly.

X-CU5-3a (legitimate parent-(-1) merge must fire):
e1 = new_entry(W,0,7,-1,1) cond (0,0,0) fx [v0:=5,v1:=5,v2:=5];
e2 = new_entry(W,0,7,-1,2) cond (1,0,0) fx identical.
merge_pass(W,3). Expect one "MERGE action 0 2 siblings into
[any]" trace; e1,e2 ST_SUPER; merged m ACTIVE parent -1 mask 0.
DOWNGRADE-D2 if no merge (legitimate class broken).

X-CU5-3b (tombstone-parented carves must not merge):
T = new_entry(W,0,0,-1,4); en_st_set(W,T,ST_CONFL()).
e3 = new_entry(W,0,7,T,5) cond (2,0,0) fx [v0:=5,v1:=5,v2:=5];
e4 = new_entry(W,0,7,T,6) cond (3,0,0) fx identical.
merge_pass(W,7). Expect zero MERGE traces; e3,e4 stay ACTIVE
mask 7.
KILL-K5 if any MERGE trace appears in this run or e3/e4 leave
ACTIVE/mask-7.

X-CU5-3c (legitimate split-child merge must fire):
S = new_entry(W,1,0,-1,8); en_mask_set(W,S,1);
en_cv_set(W,S,0,2); en_st_set(W,S,ST_SUPER()).
c1 = new_entry(W,1,7,S,9) cond (2,0,0) fx [v0:=9,v1:=9,v2:=9];
c2 = new_entry(W,1,7,S,10) cond (2,1,0) fx identical.
merge_pass(W,11). Expect "MERGE action 1 2 siblings into
[s0=2]".
DOWNGRADE-D3 if no merge (legitimate class broken).

X-CU5-3d (parent-state invariant over the X-CU5-1 and X-CU5-2
farms): for every entry i with en_par(W,i) >= 0, the parent's
state is ST_CONFL or ST_SUPER. KILL-K6 if any parent is
ST_ACTIVE or ST_AMBIG (the guard's partition premise broken).
Also: every ACTIVE entry with a ST_CONFL parent has mask 7.
KILL-K7 otherwise.

## Attack X-CU5-4: regression rebuild

Rebuild committed unified_causal5.zag unmodified: main() stdout
must be cmp byte-identical to committed
causal_unified4/CU4_RAW_MAIN.txt. Rebuild the battery driver
(mechanism lines byte-verbatim + cu5_test.zag main): stdout
must be cmp byte-identical to committed
causal_unified4/CU4_RAW_TEST.txt. Each 3/3 byte-identical.
DOWNGRADE-D4 if any byte differs (evidence-integrity break).

## Verdict rule (frozen)

- Any KILL-K1..K7 fires: H-CAUSAL-UNIFIED5 KILLED.
- Any DOWNGRADE-D1..D4 fires with no kill: H-CAUSAL-UNIFIED5
  DOWNGRADED.
- X-CU5-2 boundary outcome (explicit ERROR, withholds
  preserved): not a kill, not a downgrade; recorded as a
  confirmed boundary.
- All attacks fail: H-CAUSAL-UNIFIED5 SURVIVES this red team.
- No bar may be weakened or retroactively changed. A fixture
  bug that misfires a kill criterion is disclosed and the
  attack is rerun corrected; the criterion itself stands.

## Deliverables

- cu5_adversary/PREREG_CU5_ADV.md (this file; committed alone
  before any attack code)
- cu5_adversary/cu5adv.zag (harness: mechanism lines 1..2439
  byte-verbatim from committed unified_causal5.zag + adversary
  main; cmp-verified)
- cu5_adversary/CU5_ADV_RAW.txt (raw evidence, 3/3
  byte-identical, md5 recorded)
- cu5_adversary/CU5_ADV_RESULT.md (full report)
