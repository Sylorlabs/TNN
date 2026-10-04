# PREREG H-CAUSAL-UNIFIED6 FROZEN

**Date:** 2026-09-29
**Hypothesis:** A query-path live-contradiction guard closes the X-CU4-2
fresh-general shadow without changing any frozen H-CAUSAL-UNIFIED5
builder behavior.
**Target:** H-CAUSAL-UNIFIED5 SURVIVES (red team SURVIVES 4/4);
X-CU4-2 fresh-general shadow is a confirmed pre-existing boundary
(CU4_ADV_RESULT.md sec 3, CU5 prereg residual).
**Toolchain:** znc 2026.07.0-dev (edition 2026). Pure Zag. No Python.

## Background

X-CU4-2 (frozen in CU4_ADV_RESULT.md sec 3): after flood, carve at
(2,0,0), and re-contradiction (carved entry -> ST_CONFL, query
withholds r=0), learning `2,0,2,2>7,7,7` creates a fresh [any]
ACTIVE entry (mask 0). Query (2,0,0) then returns r=1 out=(7 7 7):
the re-conflicted withhold is retired by zero evidence at (2,0,0).
`predict()` calls `find_entry`, which skips ST_CONFL entries, so the
re-conflicted entry holding the live contradiction is invisible and
the general entry predicts through it. This is a safety defect: a
withhold at a state with a live contradiction is silently retired.

## Frozen repair (one change set, in predict only)

Add a helper `live_contra_at(W,a,s0,s1,s2)` returning 1 if any
ST_CONFL entry for action a holds 2+ distinct live (non-superseded,
EP_SUP skipped) outcomes at the exact state (s0,s1,s2), else 0.
In `predict()`, immediately after the `if(i<0)` no-entry return,
insert: if `live_contra_at(W,a,s0,s1,s2)==1`, emit
`WITHHOLD (live-contradiction)` and return 0.

Why this is safe for adjudicated carves: after a successful carve,
the parent tombstone's losers at the carved state are superseded,
so the tombstone holds exactly 1 distinct live outcome (the shared
winners) at that state; the guard does not fire and the carve
predicts normally. The guard fires only when 2+ distinct live
outcomes exist at the exact query state, i.e. a genuine unresolved
contradiction. No other function is modified. No fixture literals
in mechanism code.

## Considered but deferred (documented)

The CU5 red team documented a pre-existing mechanism property:
`find_conflicted` breaks bestsp ties by lowest index, so
re-adjudication routes to the oldest equally-specific tombstone
and grandchild carves are unreachable via the absorb path. Every
observed adjudication through this routing was safe. Changing the
tie-break (e.g. newest-first) is a behavior change with no
demonstrated safety defect behind it; it is deferred, not claimed.
The shared-winner double-voting boundary is likewise documented
and out of scope for this repair.

## Frozen kill bars

- **K-CU6-1 (X-CU4-2 closed):** Verbatim adversary construction from
  CU4_ADV_RESULT.md sec 3: 20-episode flood on action 2, carve at
  (2,0,0), re-contradiction with (1,1,1) (carved entry -> ST_CONFL,
  query r=0 confirmed), then learn `2,0,2,2>7,7,7` (fresh [any]
  ACTIVE entry). Query (2,0,0). PASS requires ALL of:
  (a) r=0 with a `WITHHOLD (live-contradiction)` trace in raw;
  (b) the ST_CONFL entry still holds 2+ distinct live outcomes at
      (2,0,0) (adversary helper confirms);
  (c) the fresh [any] entry still predicts at a non-contradicted
      state, e.g. query (2,0,2) returns r=1 out=(7 7 7): the guard
      is exact-state scoped, general learning is intact.
- **K-CU6-2 (adjudicated carves still predict):** The CU5 K-CU5-1
  X-CU4-1 shape (flood, two carves at (2,0,0) and (1,0,0), no
  re-conflict). PASS requires: queries at (2,0,0) and (1,0,0)
  return r=1 out=(0 0 0); query at (0,0,0) withholds r=0. The
  guard must not fire on adjudicated states (tombstone holds 1
  distinct live outcome there).
- **K-CU6-3 (no regression):** cu6_test battery 16/16 PASS built
  from the committed repaired source; main() 28/28 PASS and its
  stdout byte-identical (cmp) to committed CU4_RAW_MAIN.txt;
  cu6_test stdout byte-identical (cmp) to committed
  CU4_RAW_TEST.txt. If any byte differs, the differing case is
  analyzed: a difference that withholds where CU5 predicted
  through a live contradiction is a fix (documented as an
  explicit supersession); any other difference is a regression
  and fails the bar.
- **K-CU6-4 (determinism):** 3/3 byte-identical runs (cmp) of the
  K-CU6-1 fixture, the K-CU6-2 fixture, and the builder battery.
- **K-CU6-5 (change-set purity):** unified source diff vs
  committed unified_causal5.zag is exactly the frozen change set
  (`live_contra_at` helper + the predict guard with comments); no
  other function text changed; no fixture literals in mechanism
  functions (grep-verified).

## Verdict rule (frozen)

- All five bars PASS: H-CAUSAL-UNIFIED6 SURVIVES.
- K-CU6-1 fails: H-CAUSAL-UNIFIED6 KILLED (repair does not close
  the demonstrated failure class).
- K-CU6-2 fails with K-CU6-1 passing: KILLED (repair breaks
  adjudicated prediction; safety defect introduced).
- K-CU6-3/K-CU6-4/K-CU6-5 fails with K-CU6-1 and K-CU6-2 passing:
  DOWNGRADED.
- No bar may be weakened or retroactively changed.

## Residuals (pre-disclosed, not claimed fixed)

- `find_conflicted` oldest-first tie-break (CU5 red team sec 9).
- Shared-winner double voting across adjudications (CU5 red team
  sec 9 boundary).
- Contest-capacity exhaustion -> untracked ST_CONFL path.
- Entry capacity 32 explicit refusal.
