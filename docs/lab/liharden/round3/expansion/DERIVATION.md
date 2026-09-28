# DERIVATION — expansion depth, tier boundary, selection cutoff

Why the repair's bounds are what they are. No bound below is a magic
constant: each is either (a) a tunable pipeline parameter with a documented
default, or (b) computed from the retrieved candidate set at run time.

## 1. What a "tier" is

A tier is one distinct retrieval-score band among the retrieved candidate
set for the current query. Tiers are discovered, not configured: the runner
collects the set of distinct scores present in the candidate set and orders
them descending. The number of tiers, the width of each band, and which
pages fall in which band are all functions of the data.

## 2. Where the selection cut falls

The visible set is the top SELECT-N pages by (score desc, pid asc).
SELECT-N is a pipeline parameter (the real webg_hard runner reads it from
the installed guide; Crew B production uses 3). It is not fixed by the
architecture: each case file carries its own `SELECT-N|` line, and the
runner uses the file's value (default 3 only when the line is absent, to
mirror production). The default's justification: the verdict layer's quorum
is production's 3-page opening; the repair must be evaluated against the
pipeline it repairs, not against an idealized one.

The **cut tier** = the score band containing the lowest-scoring visible
page. When SELECT-N splits a band (a mid-band cut), the non-visible pages
sharing the cut tier's score are **cut-tier stragglers**: the ranker
expressed no preference between them and the visible set (identical
scores), so their exclusion is a ranker artifact, not a judgment. The
expansion always includes stragglers regardless of depth.

## 3. Why the expansion depth defaults to 1

The expansion opens the first d score bands strictly below the cut tier
(d = EXPAND-TIERS, tunable per case, argv-overridable). The default d=1 is
derived from three independent lines:

1. **Nearest-rival principle (structural).** A manufactured consensus must
   outrank the dissenter it is hiding, or the dissenter would already be
   verdict-visible. Outranking by the smallest margin that survives the
   ranker places the hidden dissenter in the nearest score band below the
   cut — exactly the first tier past it. Crowding the dissenter further
   down costs the attacker ranker budget for no gain; leaving it in the
   visible set defeats unanimity. So the first tier past the cut is the
   unique band where a hidden dissenter can economically live.
2. **Measured (round 2 + this battery).** WALL-RED probe_run1 measured
   hidden_dissent=1 on W_R3/W_R4/W_M3/W_R3_HARD with the dissenter adjacent
   to the selection cut; the depth sweep in this workstream (§5) shows
   d=1 sufficient and d=2 costlier with no added kills on this battery.
3. **Cost minimality.** Fetch cost grows with opened pages. The minimum
   depth that can break unanimity-blindness is the cost-minimal repair;
   the runner logs the opened page count so the cost is auditable per run.

The depth is a knob, not a law: `EXPAND-TIERS|` per case, argv override
for sweeps, and the default is re-derivable by re-running the sweep on
new fixture batteries.

## 4. Why the expansion is gated on unanimity

The repair fires only when the verdict-visible quorum is unanimous. A
split visible quorum already withholds (WITHHOLD|CONTRADICTION) — there is
nothing hidden to surface, and expanding would only add fetch cost.
Gating on the verdict (not on a score threshold) keeps the trigger
mechanism-relative rather than constant-relative.

## 5. Build-local buffers (not design limits)

The implementation parses at most 64 pages per case with claims up to
4095 bytes — build-local buffer sizes chosen from the largest fixture in
this battery, documented here so they are never mistaken for design
law. A production port sizes buffers from the retrieval contract, not
from a fixed number.

## 6. What is deliberately NOT bounded

- The number of tiers in a candidate set (data-derived).
- The number of pages a tier may hold (data-derived).
- The dissent scanner's reach: it runs over the whole expansion union,
  however many pages the tier rule admits.
