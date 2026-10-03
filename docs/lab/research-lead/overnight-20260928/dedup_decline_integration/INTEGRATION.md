# Dedup-Decline Integration: Composition Analysis

## Verdict

**INTEGRATION-COMPLETE: REDUNDANT.** The naive combination of dedup and
decline yields byte-identical output to dedup-only. The decline gate never
fires because dedup holds the UNCERTAINTY tally at 1 per key, below the
withhold threshold of 3. Dedup dominates; decline is dead code in the
combination.

## 1. Integration Design

Cleaner path selected: start from the dedup build (`296fd79cb`,
`dedup_full.zag`, 1728 lines) and splice the decline gate into `ev_query`.

Changes (14 lines added, 0 modified):
- Helper functions `dg_n()` (=3), `dg_withhold()` (=-3),
  `dg_uncert_count()` (live tag-30 scan keyed by field20=s, field24=r)
  inserted before `ev_query` (new lines 828-837).
- Decline check inserted in `ev_query` after the `activate` hit path
  returns and before the trial loop (new lines 845-848):
  if count >= 3, log and return WITHHOLD (-3), skipping trial,
  bootstrap, and `miss_inquire`.

The dedup pre-scan at the top of `miss_inquire` is unchanged.
No new node types, fields, modes, bridges, handlers, or semantic cases.
Both mechanisms remain researcher-authored thresholds (bounded L2).

## 2. Measurements

3/3 byte-identical runs.
SHA-256 `7bfa828aa982307825d5ada42b018e60a81204aeb517df89983159cb8c965fe4`,
exactly matching the dedup-only SHA-256 from `296fd79cb`.
The integrated transcript is byte-identical to dedup-only run1 (`cmp` clean).

WITHHOLD (-3) occurrences in integrated runs: 0.
The decline gate never fired on any of the 70 miss events.

Per-phase node deltas (totdn):

| Phase | Events | Baseline | Dedup-only | Decline-only | Combined |
|-------|--------|----------|------------|--------------|----------|
| A teach | 80 | 80 | 80 | 80 | 80 |
| B qhit | 50 | 0 | 0 | 0 | 0 |
| C miss | 50 | 101 | 21 | 61 (20 dec) | 21 |
| D observe | 50 | 100 | 100 | 100 | 100 |
| E miss2 | 20 | 40 | 0 | 0 (20 dec) | 0 |
| FINAL nodes | - | 321 | 201 | 241 | 201 |
| FINAL edges | - | 489 | 369 | 369 | 369 |

Nodes saved vs baseline: dedup 120, decline 80, combined 120.
The combined saves exactly what dedup saves; decline contributes zero.

## 3. Interaction Analysis

**Does dedup reduce the tally for decline? Yes, fatally.**
The decline gate counts live UNCERTAINTY nodes per (s,r) as its
consecutive-failure tally. Dedup guarantees at most one live UNCERTAINTY
node per (s,r): the first miss reifies it, all repeats reuse it via the
content-addressed early return. The tally is therefore pinned at 1 per
key forever (until eviction, which only lowers it). The withhold
threshold is 3. The gate cannot fire by construction.

**Does decline prevent dedup opportunities? Not in the naive build.**
Because the gate never fires, every miss still reaches `miss_inquire`,
so dedup sees every repeat it would have seen alone. Hypothetically, if
the gate did fire, withheld misses would skip `miss_inquire` entirely;
but with dedup active those misses cost +0 nodes anyway, so no node
saving is lost. The compute saving (skipped trial/bootstrap) would be
lost, but DYN-1 does not measure compute.

**Which order is better? Moot for the naive combination.**
In the code path the decline check runs first (in `ev_query`, before
trial), and the dedup check runs later (in `miss_inquire`, at
allocation). Since the decline tally is broken by dedup, no ordering of
these two checks changes the outcome: the result is dedup-only
regardless.

## 4. Why They Are Redundant (Not Merely Interfering)

The two mechanisms attack the same waste with different precision:

- Dedup detects *exact structural duplication*: "this (s,r) failure was
  already reified; reifying again adds zero information." It is a
  content-addressed identity check, precise per key.
- Decline detects *repeated failure heuristically*: "3 UNCERTAINTY nodes
  for (s,r) means this key keeps failing; stop trying." The node count
  was a proxy for repetition.

Dedup subsumes the proxy. Once duplicates are impossible, the count can
never reach the heuristic threshold, because the heuristic was calibrated
on a world where every miss allocated. The mechanisms are redundant in
purpose for the DYN-1 battery, not just in this implementation: any
tally-based decline built on reified failure records is defeated by a
deduplicating allocator, since the allocator removes the very signal the
tally reads.

Decline retains one value dedup lacks: it skips trial and bootstrap
*compute*, while dedup only saves *nodes* (trial/bootstrap still run on
every miss). On a compute metric the mechanisms would compose. On the
DYN-1 node metric they are redundant, with dedup strictly dominating
(120 saved vs 80 saved).

## 5. What Would Make Them Compose

A decline mechanism that composes with dedup needs a tally independent
of reified node count, for example a per-(s,r) miss counter incremented
on every failed pursuit (including dedup hits). That requires new
persistent state per key: either a reused field on the UNCERTAINTY node
(field 32 is currently constant 0 and could serve) or a substrate
PURSUIT record. Both break the "zero new state" elegance that made the
two pilots minimal. Whether the compute saving justifies that state is
an open experimental question, not answered here.

## 6. Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 2 (dedup gate placement at
  `miss_inquire`; decline gate placement at `ev_query`; threshold N=3).
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: 0 new (reuses tag 30, tag 1, existing fields).
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0 (N=3 researcher-set; dedup identity is
  structural, not a learner criterion).
- REUSE EVENTS: all repeat misses reuse the single UNCERTAINTY per key
  (60 reuse events across 70 misses).
- REVISION EVENTS: 0.
- COGNITION LINES: 14 added (decline helpers + check); dedup 15 lines
  pre-existing in base.
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 7. Constraints Honored

Unfrozen variant only; frozen source read-only. Pure Zag via pinned znc.
Safebin active, `which python3 python` empty. Zero em/en dashes
byte-verified. Paper untouched. No sealed worlds. Nothing pushed.
Explicit pathspecs on git add and git commit.
