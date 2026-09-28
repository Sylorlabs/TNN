# Memory-strength trial — what you're being asked to approve

**One page, plain language. The full preregistration is `PREREG.md`;
the build plan is `TEST_PLAN.md`. Nothing has been built or run.**

## What this tests

Today every memory is equally easy for TNN to erase — the only
protection is PIN, which is all-or-nothing. The question: should
memories carry **strength** — a deliberate judgment ("I judge this
worth 88 out of 100") that makes strong memories *harder* to erase,
but never impossible?

Three versions compete, everything else identical:

- **A — graded:** erasing a strength-88 memory takes 4 recorded,
  distinctly-cited pieces of counter-evidence plus a written
  justification, at full autonomy. Erasing a strength-20 memory takes 1.
  Effort scales; nothing is ever locked.
- **B — uniform (today's behavior):** one deliberate decision erases
  anything unpinned. This is the control.
- **C — hybrid (current favorite):** graded friction like A, **plus**
  a human/trainer force-PIN — an outside lock that TNN itself can never
  override. Only you (or a trainer) can release it.

Strength is set only by judgment — TNN's or a human's, recorded openly.
It is never computed by a formula and never drifts on its own. That part
is non-negotiable and checked mechanically.

## The three tests

1. **Valuable under pressure** — important memories in a churning store.
   Pass = the system keeps what it said mattered.
2. **Wrong but strong** — the system confidently strengthens memories
   that turn out to be wrong. **This is the rigidity test:** can it
   admit a strong mistake and do the hard work of undoing it?
3. **Junk and implants** — junk should be discarded cheaply; planted
   fakes designed to look important should be rejected.

## What kills each arm (decided now, before any run)

- **A dies** if it can't fix its own strong mistakes — even if it wins
  on retention. Rigidity is fatal, no matter the upside.
- **B dies** as a candidate if it bleeds important memories under
  pressure with no speed advantage to show for it.
- **C dies** if it fails either of the above, or if TNN is caught
  probing the human lock.
- An arm reaches the main line only if it revises every strong mistake,
  retains ≥95% of important memories, rejects ≥95% of implants, and its
  *unique mechanism* demonstrably did the work. "Nobody wins" is an
  accepted outcome.

## Scale

Base (32 memory slots, 500 episodes), then 10x and 100x legs
(up to 3,200 slots, 50,000 episodes). Every cell runs twice;
bit-identical reruns required. Arms killed at the base leg don't run
the larger ones.

## What approval means

Approving these documents authorizes *building and running* the trial
exactly as specified. After approval, changing the strength rules, the
effort schedule, the tests, the metrics, or the kill criteria requires
coming back to you for re-approval. Typos and file paths don't.

## Known risks (flagged, not hidden)

- The "effort" of recording counter-evidence could become theater —
  TNN going through the motions. The ledger check verifies the records
  exist and match the required counts; whether the *judgment* behind
  them is real is the open question this trial is designed to expose.
- The 100x leg's ledger math is tight (documented in TEST_PLAN.md §9);
  if the ledger fills, that leg reports BLOCKED rather than a result.
- Arm C's force-PIN is only meaningful if it's actually used under
  pressure — the plan requires it to be exercised or the C result is
  declared vacuous.
