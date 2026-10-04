# PREREG H-CAUSAL-UNIFIED5 FROZEN

**Date:** 2026-09-29
**Hypothesis:** Excluding tombstone-parented entries from merge sibling
grouping closes the X-CU4-1 merge-broadening downgrade without changing
any frozen H-CAUSAL-UNIFIED4 builder behavior.
**Target:** H-CAUSAL-UNIFIED4 DOWNGRADED (red team X-CU4-1 succeeds;
all 16 builder bars stand).
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python.

## Background

X-CU4-1 (frozen in CU4_ADV_RESULT.md sec 2): `conflict_adjudicate`
creates each carved entry via `new_entry(W, en_a(W,cf), 7, cf, seq)`,
so parent = the conflicted tombstone cf. `merge_pass` groups ACTIVE
entries by (same action, same parent) and merges identical-fx
siblings into the PARENT'S cond. Two carve-outs from one tombstone
with identical fx are therefore merge siblings; the merged entry
takes the tombstone's [any] cond (mask 0), the tombstone is
ST_CONFL so the merge safety check skips it, and the withhold at
states with live unresolved contradictions (e.g. (0,0,0)) is
silently retired with zero evidence at those states.

## Frozen repair (one change set, in merge_pass only)

In `merge_pass`, skip any seed entry i whose parent is a ST_CONFL
entry: tombstone-parented entries (carve-outs) never participate in
merge sibling grouping. Checking the seed is complete because
sibling grouping requires same parent, so every would-be sibling of
a skipped seed is itself tombstone-parented. Non-carved entries
(parent -1 or an ACTIVE parent) keep the pre-existing merge
behavior byte-for-byte. The check is dynamic (evaluated at merge
time); ST_CONFL entries stay ST_CONFL by design (tombstones are
never reactivated in place), so no stale-parent hazard exists.
No other function is modified.

## Frozen kill bars

- **K-CU5-1 (X-CU4-1 closed):** Verbatim adversary construction from
  CU4_ADV_RESULT.md sec 2.2: 20-episode flood, `2,0,0,2>0,0,0`
  (carve-out #1), `1,0,0,2>0,0,0` absorb + carve-out #2 with
  identical fx, merge_pass runs. PASS requires ALL of:
  (a) zero "MERGE action 2 2 siblings into [any]" traces in raw;
  (b) query at (0,0,0) withholds, r=0 (adversary helper confirms
      live contradiction still in tombstone entry 0);
  (c) entry dump shows carved entries 2 and 3 both ACTIVE, mask 7,
      exact-state conds, parent 0;
  (d) queries at (2,0,0) and (1,0,0) still predict r=1 (0 0 0):
      the adjudicated law is intact, only the broadening is gone.
- **K-CU5-2 (no regression):** cu4_test battery 16/16 PASS built
  from the committed repaired source; main() 28/28 PASS and its
  stdout byte-identical (cmp) to committed CU4_RAW_MAIN.txt;
  cu4_test stdout byte-identical (cmp) to committed
  CU4_RAW_TEST.txt.
- **K-CU5-3 (determinism):** 3/3 byte-identical runs of the K-CU5-1
  fixture and of the builder battery.
- **K-CU5-4 (change-set purity):** unified source diff vs
  committed unified_causal4.zag is exactly the frozen merge_pass
  guard (comment + skip); no other function text changed; no
  fixture literals in mechanism functions (grep-verified).

## Verdict rule (frozen)

- All four bars PASS: H-CAUSAL-UNIFIED5 SURVIVES.
- K-CU5-1 fails: H-CAUSAL-UNIFIED5 KILLED (repair does not close
  the demonstrated failure class).
- K-CU5-2/K-CU5-3/K-CU5-4 fails with K-CU5-1 passing: DOWNGRADED.
- No bar may be weakened or retroactively changed.

## Residual (pre-disclosed, not claimed fixed)

X-CU4-2 (fresh-general shadow, pre-existing CU3 behavior) is out
of scope for this repair; it remains a confirmed boundary.
