# B9 verdict, in plain language

**Date:** 2026-09-25. **Question from Micah:** should we change B9, the frozen
release rule? **Answer: no — don't change it.** This page explains why, without jargon.

## What B9 is

When the system thinks about a test item, it works in rounds — depth 1, 2, 4, 8, 16,
32 (more rounds = deeper thinking). At each depth it may *release* a judgment for an
item (publish a confidence number, like "I'm 57% sure") or *abstain* (stay silent).

**B9 is the frozen release rule: the fixed list of which items get a judgment at
each depth.** "Frozen" means it never changes — it's part of the test setup, not
something the system decides. Think of it as the exam proctor's seating chart:
it decides who is in the room at each round.

## The checks involved (plain definitions)

- **B3, the no-rises check:** take the average confidence of the released items,
  minus their actual accuracy. Call that the *gap*. (Negative gap = the system is
  underconfident.) B3 says: as thinking goes deeper, the gap must never go **up**.
  Even a tiny rise counts as a failure. The idea: more thinking shouldn't make the
  system look *more* confident relative to how right it is.
- **B13, the underconfidence floor:** the gap must not sink below −0.10. Being too
  unsure is also a failure — a system that answers "1% sure" to everything it gets
  right is badly calibrated.
- **B6, the coverage check:** the release rule must keep answering roughly the same
  items it always answered (at least 95% of them). You can't fix the average by
  simply refusing to answer hard questions.

## The O-rises: what went wrong

On one family of test items (family "O"), the gap did this as thinking deepened:

| depth | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| gap | −0.414 | −0.439 | −0.449 | **−0.430** | **−0.425** | −0.433 |

Two rises: −0.449 → −0.430 (**+0.019**) from depth 4 to 8, and −0.430 → −0.425
(**+0.005**) from depth 8 to 16. Small — but B3 counts any rise, so that's 2 failures.

## Why the rises happen: the survivor-mean effect

This is the core mechanism, and it's pure arithmetic — not a bug in the system's
thinking.

At depth 8, the frozen release rule **stops answering 10 items** — specifically the
10 items whose confidence was below average (about 470 out of 1000, vs 566 for the
items it kept answering).

When you remove below-average members from any group, the average of the survivors
goes up. Remove the lowest test scores from a class and the class average rises —
nothing about the remaining students changed. Here: dropping the 10 low-confidence
items mechanically lifted the survivors' average confidence by about +0.024, which
is essentially the measured +0.019 rise. The system's thinking didn't get worse;
the *room got smaller*, and the people who left were the humble ones.

We proved this causally, not just by correlation: one experiment froze the item set
(see FIXED below) — with no selection happening, the rises vanished completely.

## The four redesigns we tried (B9X = "B9 experimental")

The question was: can we redesign the release rule — change *who is in the room* —
so the rises disappear, without breaking the other checks? We tried four genuinely
different designs. The strict rule for adopting one: it must (1) clear the rises,
(2) not worsen underconfidence (B13), and (3) not break any other passing check.

**1. FIXED — answer the same items at every depth.**
The rises vanished (0 failures — nothing changes, so the average can't shift).
But it forces the system to keep answering the low-confidence items it had wisely
gone quiet on, at every depth. Underconfidence got much worse: B13 failures went
from 6 to 13. Fails rule (2). *Lesson: the selection was load-bearing — removing it
fixes the rises but the price is paid in underconfidence.*

**2. DECORR — pick who to answer by lottery instead of by confidence.**
(Deterministic lottery — a hash of the item ID, no randomness.) The rises vanished,
but the lottery stopped answering many items it should have answered: coverage (B6)
collapsed to 0.43 where 0.95 is required. That breach alone disqualifies it, and
underconfidence didn't improve either. Fails rule (3).

**3. STRAT — answer a balanced mix at every depth (new in this round).**
Keep the confidence *mix* constant: at each depth, answer the same number of
low-, medium-, and high-confidence items (same total count as before). It killed
the exact rise it aimed at — depth 4→8 is now a *fall*, not a rise — and it was the
only redesign besides DECORR that didn't worsen underconfidence (B13 held at 6).
But the strict no-rises check catches even tiny wiggles (+0.001 counts), and as the
item counts shrink at deeper depths, the mix can't be held exactly: three small new
rises appeared deeper (+0.004, +0.001, +0.003). It also broke coverage on one item
family (0.66 < 0.95), because reshuffling *which* items get answered breaks the
match with which items the old rule answered. Fails rules (1) and (3).

**4. GRAD — drop the low-confidence items gradually instead of all at once
(new in this round).** Instead of dropping all 10 at depth 8, keep 5 for one more
round, then drop them. The result was decisive: **the rise followed the drop.**
Depth 4→8 became a fall (the kept low-confidence items dragged the average down),
then depth 8→16 rose +0.009 when those items were dropped, and depth 16→32 rose
+0.019 — as large as the original — when the next kept batch was dropped. This
refuted the idea that the *suddenness* of the cut was the problem: **any** dropping
of below-average items, at any depth, recreates the rise. And keeping low-confidence
items around longer deepened underconfidence badly: B13 failures 6 → 15. Fails
rules (1) and (2).

## Why the recommendation is "don't amend B9"

Four different redesigns, four failures — and the failures form a pattern:

- The only design that clears the rises (FIXED) does it by never changing the item
  set, and pays for it in underconfidence.
- Every design that changes the item set with depth re-creates the selection effect
  *somewhere* — the strict check (any rise > 0.000000000001 counts) means even a
  +0.001 wiggle at a deep depth is a failure.
- The two goals pull in opposite directions **on the release side**: clearing the
  rise means keeping low-confidence items in the room; the underconfidence check
  punishes exactly that.

In other words: the release rule is not the right place to fix this. The rise is a
mathematical consequence of *which items are counted*, and every way of changing
who gets counted either moves the rise, shrinks nothing, or breaks a different
check. If the residual is to be fixed at all, it belongs on the **confidence**
side — how confident the system is in each item — not on the release side. (There
is already evidence that direction works: a confidence-side variant clears these
rises without outside help. That's a separate verdict.)

So: **B9 stays frozen.** The "don't change it" recommendation now rests on four
searched designs instead of two, including a direct refutation of the
"maybe the cut was just too abrupt" hypothesis.

## The numbers, for reference

| design | O-rises (B3) | underconfidence (B13) | coverage (B6) | qualifies? |
|---|---|---|---|---|
| current rule (m11) | 2 failures | 6 | 1.00 | — (baseline) |
| FIXED | 0 ✅ | 13 ❌ | 1.00 | no |
| DECORR | 0 ✅ | 5 | 0.43 ❌ | no |
| STRAT (new) | 3 ❌ | 6 ✅ | 0.66 ❌ | no |
| GRAD (new) | 3 ❌ | 15 ❌ | 1.00 | no |

*Technical detail, stated plainly: the underconfidence counts use the frozen
definition (only depths with at least 8 answered items count). An earlier round-1
table counted a few extra small-sample cells (showing 15 and 7 for FIXED/DECORR);
the conclusions are identical either way — no design passes all three rules.*

---
*Companion to the technical verdict in `VERDICT_Q1.md` (Q1b/c section + B9X2 update).
Full evidence: `ADDENDUM_B9X2_2026-09-25.md`, `q1/RUNLOG_B9X2.md`.*
