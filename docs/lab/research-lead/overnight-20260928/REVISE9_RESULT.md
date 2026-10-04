# REVISE9_RESULT: H-REVISE9

**Verdict: H-REVISE9 SURVIVES (133/117 + 16 new = 133/133).** R7 peeling
protocol closes B-RV8-2 (the red-team-confirmed subset/veto gap); all
frozen kill bars hold.

**Frozen prereg:** `PREREG_REVISE9.md` (commit `e6fbe9f77`), committed
alone before any implementation edit, build, or run. Ordering verified
with `git merge-base --is-ancestor` (prereg is a strict ancestor of the
result commit). No amendments.
**Date (UTC):** 2026-09-30
**Raw evidence:** `REVISE9_RAW.txt` (md5
`1388c8e2d151039b2956beb4b86bd81c`, 3/3 runs byte-identical via cmp,
exit 0, `H-REVISE9 SURVIVES`, 133/133).
**Parent:** H-REVISE8 SURVIVES (117/117, result `f03295207`); red team
SURVIVES (10/10) with boundaries B-RV8-1 (forged firing-set
amplification) and B-RV8-2 (subset/veto gap).

## R7 mechanism (frozen design)

In `diagnose_rollback_check`, Branch A (R7 single-slot semantics) and
Branch B (R6 whole-set test) are unchanged. Between them, the peeling
loop: for k = 1 .. nf-1, let S_k = {fset[0..k-1]} (most-recent first);
if every member of S_k mispredicts true_out (own program run directly)
AND the store without S_k predicts true_out, S_k is the smallest
jointly-implicating prefix: apply the contradiction protocol to every
prefix member (PROVISIONAL -> ROLLED_BACK; ACTIVE -> PROVISIONAL as a
first contradiction). Return 1 if any rolled back, 2 if any demoted.
A correct shadowed member stops the peel: it cannot join an
all-mispredict prefix.

New emit texts (peeling only): "PEEL: slot N PROVISIONAL->ROLLED_BACK
(smallest firing prefix jointly overrode a correct prediction)" and the
ACTIVE->PROVISIONAL analog. No other mechanism function touched.

## Kill-bar results

**K-RV9-1 (B-RV8-2 closure): PASS.** X-RV8-2b fixture replicated
exactly (P0-B identity; slot1 correct p0a at (2,113); slots 2,3 wrong
wprog at (1,98),(0,122); X="zbq", T="qqq"). CHECK P1: rb==1. CHECK P2:
slot3 ROLLED_BACK. CHECK P3: slot2 ROLLED_BACK. CHECK P4: slot1
untouched PROVISIONAL. CHECK P5: vs3_apply -> "qqq" exact (restoration
via slot 1, not P0). The smallest jointly-implicating prefix {3,2} was
felled; the correct shadowed member was preserved. The R8 veto is gone.

**K-RV9-2 (forged boundary unchanged): PASS.** X-RV8-1 fixture: two
correct identity revisions confirmed ACTIVE on "zbq"; forged F="qqq" =
P0-A(X). CHECK P6: first forged call returns 2, both demoted to
PROVISIONAL. CHECK P7: second forged call returns 1, both rolled back.
Dual-use remains disclosed. Peeling does not fire on the proper prefix
(store without {2} still predicts "zbq" != F), so the whole-set
implication path is identical to R6.

**K-RV9-3 (regression): PASS.** All 117 inherited named CHECK lines
byte-identical to the frozen REVISE8 raw (md5
631cd08786189b0596c0811f92168032). Full raw diff contains ONLY: banner
rename, Phase P block (16 CHECKs), PEEL emit lines from Phase P only,
final RESULT/verdict lines. Total 133/133. The inherited Branch A and
Branch B emit texts are byte-identical (verified in the P2 and P4
traces: "all firing revisions mispredicted" wording unchanged).

**K-RV9-4 (determinism): PASS.** 3 consecutive runs byte-identical via
cmp, exit 0.

**K-RV9-5 (minimality and veto preserved): PASS.** P3a: single wrong
top (slot2 wprog) atop correct fellow (slot1 p0a): CHECK P8 rb==1,
CHECK P9 slot2 ROLLED_BACK, CHECK P10 slot1 untouched. P3b: correct
most-recent member (slot2 p0a) atop wrong older (slot1 wprog): CHECK
P11 rb==0, CHECK P12 no state change. Branch A precedence and the
correct-member veto are both preserved.

**K-RV9-6 (tombstone interleave preserved): PASS.** X-RV8-3 fixture:
slot1 tombstoned by a first rollback; slots 2,3 live and wrong. CHECK
P13 rb==1. CHECK P14 slots 3 and 2 ROLLED_BACK. CHECK P15 slot1
tombstone untouched. CHECK P16 vcount==3. Peeling k=1 on {3} does not
fire (store without {3} still mispredicts via slot 2); Branch B fells
the whole live set exactly as in R8.

## Revised claim (replaces the H-REVISE8 claim)

1 contradiction fells a provisional revision and 2 fell a confirmed
one. When the most-recent prefix of firing revisions jointly overrode a
correct prediction (every prefix member mispredicts and the store
without the prefix predicts the trusted label), the contradiction
protocol applies to the smallest such prefix. If no correct uncovered
baseline exists, no action is taken.

## B-RV8-1 disposition (disclosure extension)

Forged labels remain outside every frozen claim; the mechanism does not
authenticate labels (dual-use, frozen since H-REVISE7). Peeling bounds
the forged blast radius to the smallest implicated prefix: a forged
label implicates only members whose removal restores the forged label.
When F = P0(X) the whole firing set is implicated (K-RV9-2 shows the
X-RV8-1 outcome unchanged); a forged label matching an intermediate
uncovered prediction would fell only the proper prefix. The set-wide
amplification named in B-RV8-1 is therefore narrowed to the
whole-set-implicated case.

## Boundaries (appended)

- B-RV9-1: the peel attributes blame most-recent-first and stops at the
  smallest jointly-implicating prefix. An older wrong member below a
  correct member can survive a contradiction it did not join (P3b
  shape); it is felled only when a later failure implicates it.
- B-RV9-2: peeling is inside `diagnose_rollback_check` only; the
  append-time X-RV5-1 underdetermination is unchanged.

Classification remains bounded L2+ revision with a firing-set
contradiction protocol plus peeling attribution. Not L3.

## Governance disclosures

1. Pure Zag throughout; zero Python at any stage (prereg, source,
   builds, runs, hashes, diffs, file edits).
2. No em dashes in loop documentation (byte-checked).
3. Binaries built in /tmp/rv9 only, never committed.
4. Only owned paths staged: `PREREG_REVISE9.md` (committed alone as
   `e6fbe9f77`); this commit adds `revise9.zag`, `REVISE9_RAW.txt` (+
   `_R2`, `_R3`), `REVISE9_RESULT.md` (this report). Concurrent
   workers' files untouched.
5. No push attempted or authorized.
6. Prereg strictly precedes implementation (verified with
   `git merge-base --is-ancestor`).

## Files (branch `tnn-native-lab`)

- `docs/lab/research-lead/overnight-20260928/PREREG_REVISE9.md`
  (commit `e6fbe9f77`)
- `docs/lab/research-lead/overnight-20260928/revise9.zag`
- `docs/lab/research-lead/overnight-20260928/REVISE9_RAW.txt`
  (+ `_R2`, `_R3`)
- `docs/lab/research-lead/overnight-20260928/REVISE9_RESULT.md`
  (this report)
