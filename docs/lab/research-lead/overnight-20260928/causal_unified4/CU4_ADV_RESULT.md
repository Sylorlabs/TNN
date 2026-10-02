# H-CAUSAL-UNIFIED4 RED TEAM REPORT (X-CU4-1..4)

**Date:** 2026-09-29
**Adversary:** Independent H-CAUSAL-UNIFIED4 Red Team
**Target:** H-CAUSAL-UNIFIED4 SURVIVES 16/16 builder battery (commit a21d08fad)
**Prereg:** `PREREG_CAUSAL_UNIFIED4_REDTEAM.md` (commit dcb5c2cd3, frozen
before any adversary execution)
**Harness:** `cu4_adv.zag` (mechanism lines 1..2429 byte-verbatim from
`unified_causal4.zag`, verified by `cmp`; only helpers and `main()`
are adversary code)
**Raw evidence:** `CU4_ADV_RAW.txt` (run 1 of 3; runs 2 and 3
byte-identical, MD5 `175be9b95d883092ffa251eef6252167`)
**Toolchain:** `znc 2026.07.0-dev (edition 2026)`. Pure Zag. No Python
in research, generators, verifiers, debugging, analysis, harnesses,
or scratch. File operations via shell only.
**Verdict: H-CAUSAL-UNIFIED4 DOWNGRADED** (not killed). X-CU4-1
succeeds. X-CU4-2 boundary confirmed (pre-existing, disclosed).
X-CU4-3a holds. X-CU4-3b documents designed re-adjudication.
X-CU4-4 holds (regression intact).

## 1. What was attacked

The verdict-section invariant of H-CAUSAL-UNIFIED4: "X-CU2-1 remains
closed: no silent-forget path was reintroduced", i.e. a conflicted
state's contradiction is never silently retired. The carve-out
mechanism itself (16 frozen bars) was not expected to fail its own
spec; the attacks targeted the invariant around it.

## 2. X-CU4-1: merge-broadening (SUCCEEDS -> DOWNGRADE)

### 2.1 Theory (frozen in prereg)

`conflict_adjudicate` creates each carved entry via
`new_entry(W, en_a(cf), 7, cf, seq)`: parent = the conflicted
tombstone cf. `merge_pass` groups ACTIVE entries by (same action,
same parent) and, when all fx are identical and no other ACTIVE
entry of the action overlaps the parent cond, merges the group into
the PARENT'S cond. Two carve-outs from the same tombstone with
identical fx are therefore merge siblings. The merged entry takes
the tombstone's cond ([any], mask 0). The tombstone is ST_CONFL so
the merge safety check skips it. Result: an [any] ACTIVE entry
carrying the adjudicated law, predicting through live unresolved
contradictions at states that were never adjudicated.

### 2.2 Execution (frozen construction)

1. Fresh workspace; the builder's exact 20-episode flood. nct=8,
   2 ST_CONFL entries (entry 0 holds seq 1-18, entry 1 holds the
   (2,0,1) pair), as in the builder battery.
2. `2,0,0,2>0,0,0` -> carve-out #1 at (2,0,0), winner (0,0,0),
   carved entry 2, fx [v0:=0, v1=same, v2=same], parent 0.
3. `1,0,0,2>0,0,0` -> absorb into tombstone entry 0 at (1,0,0);
   tally (0,0,0)x2 vs (1,1,1)x1 -> carve-out #2, carved entry 3,
   fx [v0:=0, v1=same, v2=same] (identical: var0 SET(0) in both,
   var1/var2 UNCH in both), parent 0.
4. `merge_pass` (end of `conflict_adjudicate`) merged entries 2+3.

### 2.3 Raw evidence

```
MERGE action 2 2 siblings into [any] at seq 22 fx=[v0:=0,v1=same,v2=same]
UNCONFLICT action 2 state (1 0 0) at seq 22: winner outcome (0 0 0) support 2 vs loser (1 1 1) support 1; carved new entry 3 [s0=1&s1=0&s2=0] with 2 winner episode(s); 1 loser episode(s) SUPERSEDED in conflicted entry 0 (ST_CONFL kept)
```

Entry dump after step 4:

```
entry 0 a=2 mask=0 st=3 par=-1 neps=20 [any]
entry 1 a=2 mask=0 st=3 par=-1 neps=2 [any]
entry 2 a=2 mask=7 st=2 par=0 neps=2 [s0=2&s1=0&s2=0]
entry 3 a=2 mask=7 st=2 par=0 neps=2 [s0=1&s1=0&s2=0]
entry 4 a=2 mask=0 st=0 par=0 neps=4 [any] fx=[v0:=0,v1=same,v2=same]
```

(st=3 is ST_CONFL, st=2 is ST_SUPER, st=0 is ST_ACTIVE.)

### 2.4 Kill criterion (frozen): met

Query at (0,0,0), a state with a LIVE unresolved contradiction in
the tombstone that received ZERO adjudicating evidence:

```
(rule) X1 query (0,0,0): r=1 out=(0 0 0) live-contradiction-in-tombstone=1
X-CU4-1 SUCCEEDS: withhold at (0,0,0) retired with zero evidence there; live contradiction still in tombstone
```

- `fu_predict(W,0,0,0,2,out)==1` predicting (0,0,0) via the merged
  [any] entry's rule (the `(rule)` trace prefix; no exact episode
  at (0,0,0) exists in entry 4).
- `adv_live_contra(W,2,0,0,0)==1`: tombstone entry 0 still holds at
  least one live (0,0,0) and one live (1,1,1) episode at (0,0,0)
  (flood seq 1-2, never superseded; both carve-outs only retired
  losers at (2,0,0) and (1,0,0)).
- Under the claimed invariant the query must withhold (r=0).
  Observed r=1. The kill criterion is met on all 3 runs
  (3/3 byte-identical raw outputs).

### 2.5 Causal interpretation

This is the 11/14 in-place-reactivation failure returning through
the back door. AMEND2 was motivated by the finding that "in-place
reactivation generalizes the adjudicated law across all 9 states";
the carve-out was the fix. But `merge_pass` cannot distinguish a
carved entry from a split child: same parent + identical fx reads
as "siblings that agree", so it rebuilds exactly the [any] entry
AMEND2 was created to avoid, with the tombstone's live
contradictions still inside. The UNCONFLICT traces are explicit
about what they retire; the MERGE trace says nothing about the
withholds it retires. The retirement is silent.

The failure is an interaction between the new carve-out and
pre-existing machinery, not a bug in the adjudication criterion:
the tally, the 2-vs-1 bar, the loser supersession, and the
tombstone all behave as specified. That is why the verdict is
DOWNGRADE rather than KILL: all 16 frozen bars stand (verified
independently in X-CU4-4 below), and the carve-out works as
specified at carve-out time.

### 2.6 Narrowed claim (replaces the verdict-section invariant)

OLD: "X-CU2-1 remains closed: no silent-forget path was
reintroduced; the learn path never creates a fresh entry at a
conflicted state."

NEW: The learn path never creates a fresh entry at a conflicted
state (K-CU4-2a holds; re-verified). Losers are explicitly
superseded at carve-out. BUT the pre-existing merge machinery
treats carved entries as ordinary merge siblings: two carved
entries from one tombstone with identical fx merge into the
tombstone's [any] cond, retiring withholds at states with live
unresolved contradictions and zero evidence at those states
(demonstrated). The AMEND2 scoping guarantee therefore holds at
carve-out time only. X-CU2-1's invariant ("a conflicted state's
contradiction is never silently retired") does not survive the
merge interaction.

### 2.7 Repair direction (for H-CAUSAL-UNIFIED5, not this report)

`merge_pass` sibling grouping must exclude entries whose parent
is a ST_CONFL tombstone, or the merge safety check must refuse to
broaden into a cond covered by a live ST_CONFL tombstone holding
unresolved contradictions. Either fix is small, white-box, and
directly targets the demonstrated failure class.

## 3. X-CU4-2: fresh-general shadow (BOUNDARY CONFIRMED)

Construction: flood, carve at (2,0,0), re-contradiction (1,1,1)
(carved -> ST_CONFL, `find_entry` = -1), then `2,0,2,2>7,7,7`
(fresh [any] ACTIVE entry; (2,0,2) has no live conflicted
evidence). Query (2,0,0):

```
(rule) X2 query (2,0,0) after fresh [any]: r=1 out=(7 7 7)
X-CU4-2 BOUNDARY CONFIRMED: re-conflicted withhold shadowed by fresh general entry (pre-existing, disclosed limitation 1)
```

The re-conflicted withhold is retired by zero evidence at
(2,0,0). This is the builder's disclosed limitation 1, reachable
in CU3 as well (the learn path is unchanged by CU4), so it is a
pre-existing boundary, not a CU4 regression. No verdict change
from this attack. Note the builder's battery never queries
(2,0,0) after K-CU4-1f, which is why the battery passes while the
withhold is gone; the ordering note discloses the interaction but
the battery does not probe it.

## 4. X-CU4-3a: re-conflict forced (HOLDS)

Construction: flood, carve at (2,0,0), re-contradiction (1,1,1).

```
ENTRY action 2 [s0=2&s1=0&s2=0] CONFLICTED: contradiction untracked (contest cap) at seq 22 (WITHHOLD)
WITHHOLD (no-entry)
X3a re-contradiction: find_entry=-1 query r=0
X-CU4-3a HOLDS: re-contradiction re-conflicts, withhold returns
```

nct is monotonic and ST_CONFL-via-contest requires nct=8, so
`new_contest` must fail on the re-contradiction and the carved
entry must go ST_CONFL. No prediction through a live
contradiction was observed. The attack fails as expected; the
re-conflict safety property is robust. (ST_CONFL can also arise
via split/ambiguity paths with nct<8, in which case a
re-contradiction opens a tracked contest instead of
re-conflicting; `predict()` withholds on unresolved contests
either way, so the safety property holds on both paths.)

## 5. X-CU4-3b: re-carve probe (DOCUMENTED, designed behavior)

After the X-CU4-3a re-conflict, absorbing two more (1,1,1) at
(2,0,0):

```
X3b after 3rd (1,1,1): nent 3->3 (expect stable: 2-vs-2)
UNCONFLICT action 2 state (2 0 0) at seq 24: winner outcome (1 1 1) support 3 vs loser (0 0 0) support 2; carved new entry 3 [s0=2&s1=0&s2=0] with 3 winner episode(s); 2 loser episode(s) SUPERSEDED in conflicted entry 2 (ST_CONFL kept)
X3b after 4th (1,1,1): nent 3->4 (expect +1: 2-vs-3 re-carve)
(exact-episode) X3b query (2,0,0): r=1 out=(1 1 1)
```

The 2-vs-2 absorb is stable (nent unchanged); the 2-vs-3 absorb
fires the frozen criterion for (1,1,1) and carves a second-generation
entry (parent = the re-conflicted carved entry), superseding the
(0,0,0) winners. The tombstone is re-adjudicable: no one-way
ratchet. The adjudicated law flip-flops only when the evidence
majority flips, which is the designed contest-bar behavior, not a
hole.

## 6. X-CU4-4: regression integrity (HOLDS)

Rebuilt `unified_causal4.zag` and `cu4_test.zag` from the committed
sources with the pinned toolchain; each run 3 times:

- main(): 3/3 byte-identical, MD5
  `87f8edc29825802327029f46f045dbe3`, exactly matching committed
  `CU4_RAW_MAIN.txt`. 28 PASS, 0 FAIL.
- cu4_test: 3/3 byte-identical, MD5
  `3bde55fe381a7c8ff1cef93d8c038da3`, exactly matching committed
  `CU4_RAW_TEST.txt`. 16/16 PASS, 0 FAIL.

The builder's evidence is intact and reproducible. All 16 frozen
bars stand, which bounds this red-team verdict to DOWNGRADE
rather than KILL.

## 7. Governance disclosures

- Preregistration strictly preceded adversary implementation and
  execution (commit dcb5c2cd3). No frozen bar was weakened or
  retroactively changed. Kill criteria are quoted verbatim from
  the prereg.
- Pure Zag throughout: no Python in research, generators,
  verifiers, debugging, analysis, harnesses, or scratch. The
  harness was assembled with shell (`sed`/`cat`/`cmp`); the
  mechanism lines are byte-verbatim (cmp-verified).
- The first `znc build` invocation exited 2 with warnings on
  stderr; a rerun exited 0 and produced a working binary. No
  source was changed between the two invocations; the binary
  used for all evidence came from the successful build. All
  final evidence is 3/3 byte-identical.
- Only explicitly owned paths were staged and committed:
  `docs/lab/research-lead/overnight-20260928/causal_unified4/`.
- No binaries or generated artifacts committed (raw outputs are
  text).
- Commits are local; no push was attempted or authorized.
- This document contains no em dashes.

## 8. Commit lineage

- dcb5c2cd3 `PREREG H-CAUSAL-UNIFIED4 RED TEAM FROZEN: X-CU4-1..4 attacks (before execution)`
- (this commit) adversary harness (`cu4_adv.zag`), raw output
  (`CU4_ADV_RAW.txt`), and this report.

## 9. Verdict

**H-CAUSAL-UNIFIED4: DOWNGRADED.** X-CU4-1 demonstrates a
silent-forget path the verdict claimed was closed: two carved
sibling entries with identical fx merge into the tombstone's
[any] cond, retiring the withhold at (0,0,0) with zero evidence
at that state while the tombstone still holds the live
contradiction (3/3 deterministic). The carve-out mechanism itself
survives all 16 frozen bars (X-CU4-4 re-verified); the claim that
must be narrowed is the X-CU2-1 closure invariant, which now
reads: the learn path never creates a fresh entry at a
conflicted state, losers are explicitly superseded at carve-out,
but the AMEND2 scoping guarantee holds at carve-out time only
because the pre-existing merge machinery can broaden carved
entries and silently retire withholds at contradicted states.
X-CU4-2 confirms the disclosed fresh-general shadow boundary
(pre-existing). X-CU4-3a holds (re-conflict robust). X-CU4-3b
documents principled tombstone re-adjudication. Classification
remains bounded L2; nothing here is L3. Recommended next step:
H-CAUSAL-UNIFIED5 repairing the merge/carve-out interaction
(exclude tombstone-parented entries from merge sibling
grouping, or make the merge safety check conflict-aware).
