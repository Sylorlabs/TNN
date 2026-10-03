# H-CAUSAL-UNIFIED5 RESULT (X-CU4-1 REPAIR)

**Date:** 2026-09-29
**Researcher:** H-CAUSAL-UNIFIED5 Repair Researcher
**Target:** H-CAUSAL-UNIFIED4 DOWNGRADED (X-CU4-1 merge-broadening)
**Prereg:** `PREREG_CAUSAL_UNIFIED5.md` (commit b486bad12, frozen before
any implementation)
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python
in research, generators, verifiers, debugging, analysis, harnesses,
or scratch. File operations via shell only.
**Verdict: H-CAUSAL-UNIFIED5 SURVIVES.** All four frozen bars pass.

## 1. Frozen repair (exact change set)

File `unified_causal5.zag` is byte-verbatim `unified_causal4.zag`
except one 9-line insertion in `merge_pass` (diff verified; no other
function text changed):

```
    // H-CAUSAL-UNIFIED5 (X-CU4-1): entries parented by a ST_CONFL
    // tombstone (carve-outs) never merge. The tombstone's cond is
    // [any]; merging carved siblings into it would silently broaden
    // the adjudicated law and retire withholds at states holding
    // live unresolved contradictions. Checking the seed is complete:
    // sibling grouping requires same parent, so every would-be
    // sibling of a skipped seed is itself tombstone-parented.
    let pari:i32=en_par(W,i);
    if(pari>=0 && en_st(W,pari)==ST_CONFL()){i=i+1;continue;}
```

This is the red team's frozen repair direction option A
("exclude tombstone-parented entries from merge sibling grouping").
The check is dynamic at merge time; ST_CONFL entries stay ST_CONFL
by design (tombstones are never reactivated in place), so no stale
parent hazard. All three merge_pass call sites (conflict_adjudicate,
contest path, split path) are covered by the single guard. Entries
with parent -1 or an ACTIVE parent keep pre-existing merge
behavior byte-for-byte.

## 2. K-CU5-1: X-CU4-1 closed (PASS)

Harness `cu5_adv.zag`: mechanism lines 1..2438 byte-verbatim from
`unified_causal5.zag` (cmp-verified); adversary helpers and main
verbatim from `cu4_adv.zag` (X-CU4-1..4 construction unchanged).
Raw: `CU5_ADV_RAW.txt` (run 1 of 3; 3/3 byte-identical, MD5
`f93d5d3fb5b3134ccc656314b8a21c8e`).

(a) Zero "MERGE action 2 2 siblings into [any]" traces (grep count
    0 across the whole raw).
(b) Query at (0,0,0): `r=0` (WITHHOLD), `live-contradiction-in-
    tombstone=1`. The kill criterion is inverted: the attack now
    fails.
(c) Entry dump after the two carve-outs:

    entry 0 a=2 mask=0 st=3 par=-1 neps=20 [any]
    entry 1 a=2 mask=0 st=3 par=-1 neps=2 [any]
    entry 2 a=2 mask=7 st=0 par=0 neps=2 [s0=2&s1=0&s2=0]
    entry 3 a=2 mask=7 st=0 par=0 neps=2 [s0=1&s1=0&s2=0]

    Both carved entries stay ACTIVE (st=0), mask 7, exact-state
    conds, parent 0. Tombstones stay ST_CONFL (st=3).
(d) Adjudicated law intact: `X1 sanity (2,0,0) r=1 (1,0,0) r=1`,
    both predicting (0,0,0) via the carved entries.
(e) Structural helper: `X1 broad-[any]-ACTIVE-present=0`.

Unchanged neighbors in the same raw (regression sanity):
X-CU4-2 BOUNDARY CONFIRMED (pre-existing fresh-general shadow,
unchanged, out of scope per prereg residual); X-CU4-3a HOLDS
(re-conflict re-conflicts, withhold returns); X-CU4-3b DOCUMENTED
(tombstone re-adjudicates, no one-way ratchet).

## 3. K-CU5-2: no regression (PASS)

- `cu5_test.zag` (builder battery main, mechanism lines
  byte-verbatim from unified_causal5.zag): `=== CU4 TEST RESULT:
  16/16 ===`, ALL PASS. Stdout byte-identical (cmp) to committed
  `CU4_RAW_TEST.txt`.
- `unified_causal5.zag` main(): stdout byte-identical (cmp) to
  committed `CU4_RAW_MAIN.txt` (MD5
  `87f8edc29825802327029f46f045dbe3`; 28 PASS, 0 FAIL).
- The frozen main raw contains one legitimate pre-existing merge,
  `MERGE action 2 2 siblings into [s0=2] at seq 17` (split
  children merging into a specific cond), which reproduces
  byte-identically: the guard blocks only tombstone-parented
  merges, not normal merges.

## 4. K-CU5-3: determinism (PASS)

- cu5_adv: 3/3 byte-identical, MD5
  `f93d5d3fb5b3134ccc656314b8a21c8e`.
- cu5_test: 3/3 byte-identical, MD5
  `3bde55fe381a7c8ff1cef93d8c038da3` (matches committed
  CU4_RAW_TEST.txt MD5 from the CU4 red team report).
- cu5_main: 3/3 byte-identical, MD5
  `87f8edc29825802327029f46f045dbe3` (matches committed
  CU4_RAW_MAIN.txt MD5 from the CU4 red team report).

## 5. K-CU5-4: change-set purity (PASS)

`diff causal_unified4/unified_causal4.zag
causal_unified5/unified_causal5.zag` shows exactly the frozen 9-line
merge_pass guard. No other function text changed. No fixture
literals in mechanism functions (the guard references only
en_par/en_st/ST_CONFL, all pre-existing mechanism accessors).

## 6. Causal interpretation

The failure class is closed at the mechanism level: a carved entry
is by construction parented by a ST_CONFL tombstone whose cond is
[any], so any merge that groups it with its carved siblings would
necessarily broaden into the tombstone's cond. Excluding the whole
class (tombstone-parented seeds) from sibling grouping removes the
interaction rather than patching one fixture. The narrowed claim
from the CU4 red team ("AMEND2 scoping holds at carve-out time
only") is superseded: the AMEND2 scoping guarantee now survives
merge_pass as well. The only residual is the pre-existing,
disclosed X-CU4-2 fresh-general shadow, which does not involve
tombstone-parented merging.

## 7. Governance disclosures

- Preregistration strictly preceded implementation and execution
  (commit b486bad12). No frozen bar was weakened or retroactively
  changed. Verdict rule applied verbatim from the prereg.
- Pure Zag throughout: no Python anywhere. Harness assembly via
  shell head/tail/cat/sed; mechanism regions cmp-verified
  byte-identical.
- One failed `znc build` invocation (missing output binary from an
  earlier cwd mistake) preceded the successful build; no source
  was changed between them. All final evidence comes from the
  successful builds, 3/3 byte-identical.
- Only explicitly owned paths staged: `docs/lab/research-lead/
  overnight-20260928/causal_unified5/`.
- No binaries or generated artifacts committed (raw outputs are
  text).
- Commits are local; no push attempted or authorized.
- This document contains no em dashes.

## 8. Commit lineage

- b486bad12 `PREREG H-CAUSAL-UNIFIED5 FROZEN: tombstone-parented
  entries excluded from merge grouping (before implementation)`
- (this commit) `unified_causal5.zag` (repaired mechanism),
  `cu5_adv.zag` (adversary driver), `cu5_test.zag` (battery
  driver), `CU5_ADV_RAW.txt`, and this report.

## 9. Verdict

**H-CAUSAL-UNIFIED5: SURVIVES.** K-CU5-1 through K-CU5-4 all pass.
The X-CU4-1 merge-broadening path is closed: two carved entries
from one tombstone with identical fx no longer merge; the
withhold at (0,0,0) survives with the live contradiction intact
(r=0, live=1) while the adjudicated law at (2,0,0) and (1,0,0)
keeps predicting (r=1 each). All 16 builder bars and the 28/28
main regression reproduce byte-identically. Recommended next
step: independent red team against H-CAUSAL-UNIFIED5 (probe for
other merge/carve-out interactions, e.g. second-generation carves
under a re-conflicted carved tombstone, and merge pressure on
tombstone-parented entries at entry-capacity limits).
Classification: bounded L2; nothing here is L3.
