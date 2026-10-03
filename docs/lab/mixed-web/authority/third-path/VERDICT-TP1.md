# VERDICT-TP1: the third-path trial (frozen corpus, 220 envelopes)

**Prereg:** `44afdbefc168edddcae50e9dd91eac12cd9fa156` (committed before any
trial run; design frozen). **Result commit:** this file's commit (see
REPRODUCE.md). Pure Zag, zero RNG, 5/5 byte-identical runs, independent
Python oracle recomputed every decision and every ledger head: **PASS**.

## The question

Round 3 licensed "loose authority" (trust the primary source) on
uncorroborated disputes, gated on independently-established reliability —
but left two open problems: genuine 2v2 ties (both old rules fiat-broke
them, 100% false confidence) and whether a third path beats the two
frozen options. Three candidates went head-to-head on the frozen 220-envelope
corpus (180 uncorroborated disputes, 20 genuine ties, 20 no-reliability
controls):

- **T1 — gated loose authority.** Trust the primary source's newest answer,
  but only if its track-record reliability beats the k/(k+1) bar, and never
  on a genuine tie, never with no track record.
- **T2 — SUSPECT / defer.** Withhold judgment until a *causally independent*
  second channel settles it.
- **T3 — one-brain deliberation.** The full deliberation procedure over a
  shared ledger — shape the dispute, check the gate, then decide.

## The headline

| Path | Block U value (180 cases) | Genuine ties (20) | No-reliability controls (20) | License |
|---|---|---|---|---|
| T1 gated loose | **+78** (+0.43/case) | 0 fires, 0% false confidence | 0 fires | **EARNED** |
| T2 defer | 0 (withholds; nothing to defer to in-corpus) | 0 fires | 0 fires | **CONDITIONAL** — only if a real second channel exists (priced below) |
| T3 deliberation | **+78** — verdict-identical to T1 on all 880 decisions | 0 fires | 0 fires | **NONE beyond T1** — deliberation bought zero extra value here |
| Frozen C (always withhold) | 0 | 0 fires | 0 fires | baseline |
| Frozen D (round-3 loose, ungated) | +66 (+0.37/case) | **20/20 fires, 100% false confidence** | fires | superseded by T1 |

T1 beats both frozen rules in total: it takes the better of the two at
every reliability level — it fires exactly where the old loose rule was
profitable and withholds exactly where the old loose rule destroyed value.
And the mandatory tie guard fixes the round-3 embarrassment: 100% false
confidence on ties → 0%.

## What the numbers say (plain English)

**On the 180 uncorroborated disputes:** T1 reproduces the round-3 law
exactly — where it fires, each reliability level pays 2r−1 per case
(50% reliable → breaks even, 99% reliable → +1.00/case). The gate works:
at the k=1 bar (fire only at ≥50% reliability) it never fires a
value-destroying case, finishing +78 vs the ungated rule's +66. Wrong
installs land exactly where the reliability says they should (10 of 20
wrong at 50%, 0 of 20 wrong at 99%).

**On the 20 genuine ties:** all three paths withhold on all 20. False
confidence: 0% — down from 100% for both round-3 rules. The tie guard is
no longer optional; it's proven.

**On the 20 no-reliability controls:** all three paths fire 0 times. No
track record → no fire, no exceptions.

**T3 vs T1:** 880 decisions, 880 identical verdicts. The preregistration
predicted exactly this (a dispute's rows carry no information about who
is right — the twin-identity theorem), and the trial confirms it.
Deliberation's value here is auditability (every step on the shared
ledger), not better outcomes.

**T2's price tag** (parametric — the corpus has no second channel, so
this is math, not measurement): deferring beats doing nothing once the
channel arrives often enough; it beats loose authority wherever loose
authority destroys value (below 50% reliability). Concrete: with a
perfect second channel and a modest cost for never-resolving, T2 needs
the channel to show up more than ~20% of the time to earn its keep, and
it wins outright in the low-reliability band where firing is a losing
bet. Expected wait for resolution is 1/ρ channel-arrivals; the
never-resolved fraction is 1−ρ. Without a real channel, T2 is just
withholding with extra steps.

## Decision

1. **License T1** (gated loose authority + mandatory tie guard + no-fire
   without independent reliability) for the uncorroborated-dispute shape.
   It strictly dominates both frozen rules.
2. **Do not license T3 separately** — it is T1 with a paper trail on this
   corpus. Keep the deliberation machinery for its audit value, not as a
   separately licensed decider.
3. **License T2 conditionally**: only in deployments with a genuine
   causally-independent second channel, and only where (ρ, q, δ) clear
   the priced frontier in §6 of the analysis. No channel → no license.
4. **The tie guard stays mandatory** for any future path.

## Integrity record

- Shape classifier: 200 uncorroborated / 20 ties / 0 corroborated /
  0 other — exactly the frozen corpus composition, 220/220.
- 5 runs, byte-identical (sha256 `d57fda22…32d1d9`).
- Independent oracle: all 2,640 decisions, all 3 ledger heads, all shape
  counts recomputed from the frozen data — 0 mismatches.
- Ledger heads: T1 `e17861ba…`, T2 `3c030dd4…`, T3 `d2f45295…`
  (880 chained entries each; full values in evidence/run0.log).
- Nothing was committed after the prereg except this evidence; the trial
  binary was built from the frozen sources with the pinned toolchain.
