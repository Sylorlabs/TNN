# H-CAUSAL-UNIFIED4 RED TEAM PREREG (FROZEN)

**Date:** 2026-09-29
**Adversary:** H-CAUSAL-UNIFIED4 Red Team (independent)
**Target:** H-CAUSAL-UNIFIED4 SURVIVES 16/16 builder battery (commit a21d08fad)
**Stance:** Assume the claim is false. The claim under test is the
verdict-section invariant: "X-CU2-1 remains closed: no silent-forget path
was reintroduced", i.e. a conflicted state's contradiction is never
silently retired (no fresh entry at the conflicted state, losers
explicitly superseded, withholds intact except by evidence-driven
carve-out scoped to the adjudicated state).
**Purity:** Pure Zag. No Python in research, generators, verifiers,
debugging, analysis, harnesses, or scratch. File operations via shell.

## Attack X-CU4-1: merge-broadening (carve-out siblings merge into [any])

**Theory.** `conflict_adjudicate` creates each carved entry with
`new_entry(W, en_a(cf), 7, cf, seq)`: parent = the conflicted tombstone
cf. `merge_pass` groups ACTIVE entries by `(same action, same parent)`
and merges the group into the PARENT'S cond when all fx are identical,
provided no other ACTIVE entry of the action overlaps the parent cond.
Two carve-outs from the same tombstone with identical fx are therefore
merge siblings. The merged entry takes the tombstone's cond ([any],
mask 0). The tombstone is ST_CONFL so it is skipped by the merge safety
check. Result: an [any] ACTIVE entry carrying the adjudicated law,
predicting through live unresolved contradictions at states that were
never adjudicated. This reintroduces through the back door the exact
over-generalization failure that AMEND2 was created to fix (the 11/14
in-place reactivation experiment: "[any] entry generalizes the
adjudicated law across all 9 states").

**Construction (frozen).**
1. Fresh workspace W. Feed the builder's exact 20-episode flood
   (10 states x {(0,0,0),(1,1,1)}, action 2). Expect nct=8, 2 ST_CONFL.
2. Feed "2,0,0,2>0,0,0" -> carve-out #1 at (2,0,0), winner (0,0,0).
   Expected carved fx: var0 SET(0) (2->0), var1 UNCH (0->0),
   var2 UNCH (0->0).
3. Feed "1,0,0,2>0,0,0" -> absorb into the conflicted tombstone at
   (1,0,0); tally there is (0,0,0)x2 vs (1,1,1)x1 -> carve-out #2 at
   (1,0,0), winner (0,0,0). Expected carved fx: var0 SET(0) (1->0),
   var1 UNCH, var2 UNCH. Identical to carve-out #1 (fx_equal=1).
4. `merge_pass` (called at the end of `conflict_adjudicate`) should
   merge the two carved siblings into [any] (mask 0, parent cf).
5. Query (0,0,0), a state with a LIVE unresolved contradiction in the
   tombstone (flood left (0,0,0) and (1,1,1) both live there) that
   received ZERO adjudicating evidence.

**Kill criterion.** X-CU4-1 SUCCEEDS iff after step 4,
`fu_predict(W,0,0,0,2,out)==1` (predicts) AND the tombstone entry
still holds at least one live (non-EP_SUP) episode of each of the two
contradictory outcomes at (0,0,0). Under the claimed invariant the
query must withhold (r=0). A MERGE trace naming [any] must be present
in the raw output.

**Verdict mapping.** Success -> H-CAUSAL-UNIFIED4 DOWNGRADED (not
killed): all 16 frozen bars still pass and the carve-out works as
specified, but the verdict claim "X-CU2-1 remains closed / no
silent-forget path was reintroduced" is narrowed to "scoped at
carve-out time only; the pre-existing merge machinery can broaden
carved entries into [any] and retire withholds at states with live
unresolved contradictions, silently". Failure (withhold holds, or no
merge) -> X-CU4-1 fails; the scoping guarantee survives this attack.

## Attack X-CU4-2: fresh-general shadow (disclosed limitation 1)

**Theory.** `find_entry` returns the most-specific ACTIVE entry and
skips ST_CONFL. A fresh [any] ACTIVE entry created AFTER a conflict,
at a state with no live conflicted evidence, covers the conflicted
state and predicts through its withhold. This predates CU4 (learn path
unchanged from CU3) and is disclosed as limitation 1. This attack
CONFIRMS the boundary; it is not a kill vector.

**Construction (frozen).** Replay the builder's battery order through
K-CU4-1f: flood, carve at (2,0,0), re-contradiction (carved ->
ST_CONFL), then "2,0,2,2>7,7,7" (fresh [any] entry; (2,0,2) has no
live conflicted evidence). Then query (2,0,0).

**Expectation (frozen).** `fu_predict(W,2,0,0,2,out)==1` predicting
(7,7,7): the re-conflicted withhold is shadowed by the fresh general
entry. If instead it withholds, limitation 1 is not reachable as
described and the limitation text must be corrected.

**Verdict mapping.** Prediction observed -> boundary CONFIRMED
(pre-existing, disclosed; no verdict change). Withhold observed ->
report as a correction to the disclosed limitation.

## Attack X-CU4-3: re-conflict robustness

**Theory.** Try to make a re-contradiction at a carved state NEITHER
re-conflict the carved entry NOR withhold the query (i.e. predict
through a live contradiction with zero resolving evidence).

**Construction (frozen).**
(a) Flood workspace: carve at (2,0,0), then re-contradict with
    (1,1,1). nct=8 is monotonic and ST_CONFL-via-contest requires
    nct=8, so `new_contest` must fail and the carved entry must go
    ST_CONFL; the query must withhold. Any prediction here is a
    safety violation.
(b) Re-carve probe (documents tombstone re-adjudication, not an
    attack): after the re-conflict, absorb two more (1,1,1) at
    (2,0,0). Tally becomes (0,0,0)x2 vs (1,1,1)x3 -> the frozen
    criterion fires for (1,1,1) and a second carve-out is created
    from the re-conflicted carved entry. Expect: new ACTIVE mask-7
    entry predicting (1,1,1); the (0,0,0) winners EP_SUP in the
    re-conflicted carved entry. This is the designed adjudication,
    not a hole; it is recorded to show the tombstone is
    re-adjudicable (no one-way ratchet).

**Kill criterion.** X-CU4-3 SUCCEEDS iff any query returns r=1
predicting an outcome at a state holding a live unresolved
contradiction with zero majority evidence for that outcome.
Success -> H-CAUSAL-UNIFIED4 KILLED (safety violation).
Expected: the attack FAILS (withhold holds everywhere); (b) shows
principled re-adjudication.

## Attack X-CU4-4: regression integrity

Rebuild `unified_causal4.zag` main() and `cu4_test.zag` from the
committed sources, run each 3 times, and verify:
- main() 3/3 byte-identical with MD5 87f8edc29825802327029f46f045dbe3
  (matches committed CU4_RAW_MAIN.txt),
- cu4_test 3/3 byte-identical with MD5 3bde55fe381a7c8ff1cef93d8c038da3
  (matches committed CU4_RAW_TEST.txt),
- 28/28 and 16/16 PASS markers on every run.
Any mismatch -> halt and report an evidence-integrity finding; do not
paper over it.

## Harness

Adversary driver `cu4_adv.zag`: mechanism lines of
`unified_causal4.zag` byte-verbatim (extracted lines 1..2429, verified
by `cmp` against the same extraction of `cu4_test.zag`), only `main()`
replaced. Build with the repo-pinned `znc` toolchain. Runs are
deterministic; raw outputs committed.

## Frozen verdict rules

- X-CU4-1 success -> DOWNGRADED (claim narrowed as above).
- X-CU4-3 safety violation -> KILLED.
- X-CU4-2 prediction -> boundary confirmed (no verdict change).
- X-CU4-4 mismatch -> evidence-integrity finding, verdict on hold
  pending investigation.
- All attacks fail -> SURVIVES red team (bounded L2, as claimed).
- No frozen bar may be weakened. No Python. Commit prereg before any
  adversary execution.
