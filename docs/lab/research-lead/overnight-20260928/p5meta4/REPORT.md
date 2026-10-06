# REPORT -- P5-meta4: PREDICTION CONFIRMED. The p5meta3 result was a cache.

Branch `ownership`. Prereg `p5meta4/PREREG.md` (written before the run,
with an explicit sign-flip prediction). 3/3 sha-identical
`99d1289b5c2b95529262...`. 24 fingerprint rows. No `*_ok` flags.

## THE SINGLE CHANGE FROM P5META3

Acquisition is measured on queries the prior phase **never showed**:

* prior shows `q = 0..11`
* acquisition probes `q = 12..21`, remapped into a disjoint input band
  (`pq0 = 100 + 11q mod 37`, `pq1 = 200 + 17q mod 41`)

No retained fact can match a probe query, so a fact cache **provably
cannot replay**.

## PREDICTION (recorded before running)

> If the speedup was a cache, `RELEVANT` should **degrade to or below
> `FRESH`**. I predict the sign flip.

## RESULT: THE SIGN FLIPPED

Acquisition cost (trials to 3 consecutive correct; 60 = never):

| family | FRESH | RELEVANT | IRRELEVANT | MISLEADING | META_ABLATED | ORACLE_META |
|---|---|---|---|---|---|---|
| 0 | 21 | 60 | 60 | 60 | 60 | 60 |
| 1 | 23 | 60 | 60 | 60 | 60 | 60 |
| 2 | 15 | 60 | 60 | 60 | **9** | 60 |
| 3 | 23 | 60 | 60 | 60 | 60 | 60 |
| **mean** | **20.50** | **60.00** | **60.00** | **60.00** | **47.25** | **60.00** |

Compare p5meta3 on the *same arms*:

| arm | p5meta3 (seen queries) | p5meta4 (unseen queries) |
|---|---|---|
| FRESH | 24.50 | 20.50 |
| RELEVANT | **3.00** | **60.00** |
| META_ABLATED | 3.00 | 47.25 |

**The prior went from 8x faster than fresh to never acquiring at all.**
Prior experience does not teach a mapping; it fills a cache that only
answers questions it has already seen.

## VERDICT

**M4' DECISIVE: FAILS.** `RELEVANT` (60.00) is *worse* than `FRESH`
(20.50) on never-seen queries. Per the prereg this voids the p5meta3
result.

**M2' FAILS**: `IRRELEVANT` also 60.00 — the prior is not neutral, it is
uniformly harmful on unseen queries.

**M3' FAILS**: `MISLEADING` also 60.00, indistinguishable from relevant
prior. The mechanism is indifferent to prior content.

**Control behaves correctly**: `META_ABLATED` on family 2 scores 9,
better than `FRESH` 15. That is the one anomalous cell and it is worth
naming rather than hiding: zeroing `MACH` left only a base-rate default,
and on that family the default happens to be right often enough to trip
3-in-a-row. It is a coincidence of that family's coefficients, not
evidence of machinery.

## WHAT THIS KILLS AND WHAT IT DOES NOT

1. **Falsified**: p5meta3's "learning-to-learn" result in full. Any
   account in which prior experience reduced *acquisition* is wrong.
2. **Falsified**: the `MACH` slot machinery as a learning mechanism. It
   earned nothing measurable and now costs trials.
3. **Does NOT falsify**: meta-learning in general. This substrate's
   learner has no mechanism that could represent a mapping — it is an
   associative lookup plus a content-independent scaffold.
4. **Assumption that caused the failure**: acquisition was measured on
   queries the fact store could answer. Measuring learning where the
   fastest strategy is *not learning* is the whole error.

## ARCHITECTURE SIMPLIFICATION EARNED

`MACH` can be **deleted** with no measured loss — in p5meta4 it is
actively harmful. That is a concrete simplification and must be applied
to the successor.

## SUCCESSOR (per queue rule)

The substrate must be able to *represent* a mapping before any
learning-to-learn question can be asked of it. Two materially distinct
options, both queued rather than chosen:

* **`P5-meta5a` structural substrate**: candidate *programs* whose
  coefficients are learned, so a mapping exists independently of whether
  the query was seen. Tests whether *representation* is the blocker.
* **`P5-meta5b` composition substrate**: require the learner to apply a
  learned rule to inputs it has never stored, with the rule itself the
  thing acquired.

Both are cheap falsifiers. Neither is a tuning change.

## STATUS

`P5-meta` remains OPEN, now with the blocker identified: **the
associative substrate cannot represent a mapping**, so the question was
unaskable rather than answered. That is progress — p5meta3 and p5meta4
together rule out the easiest false positive.

L3 = 0. No architecture changed. No bridges added or removed. No modes,
routers, domain names, or strategy menus.