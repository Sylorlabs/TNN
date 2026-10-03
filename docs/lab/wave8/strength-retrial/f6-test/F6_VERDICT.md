# F6 verdict — head-to-head: windowed vs global vs hybrid citation single-use

Date: 2026-09-26. Pure Zag, zero RNG. Every run executed twice, byte-identical.

## UPDATE — Micah's 21:47 PDT ruling (2026-09-25) supersedes the recommendation

After this test was dispatched, Micah ruled on the delete-strong red-team
holes (see MEMORY.md 2026-09-25 ~21:47 PDT, and the standing rule now in
AGENTS.md): **hole 2 (cite resurrection on slot reuse) is a "big issue"** —
"deleted means deleted", "cite-consumption is generation-scoped so slot reuse
can't resurrect spent cites", and "destruction never silently recycles a slot"
(deliberate recycling is a separate explicit op in its own fork).

This ruling **disqualifies H (hybrid) by name**: H's defining behavior —
destroy → ADD → re-cite the SAME episodes → destroy succeeds (A2/A6 = 0) —
is exactly "slot reuse resurrecting spent cites." The measurements below are
unchanged, but the recommendation is revised to comply: **G (global) is the
compliant choice; H is out; W remains out.** G's measured costs (below) are
now the open risks to track, not a reason to pick H.

Related: Micah also removed `st_kill` from TNN's reachable op set
(trainer-only instrument). This test's core predates that ruling; A8 used
`st_kill` to establish the "payment, not mere mention, consumes" principle —
the principle stands, the op is now trainer-gated.
The F4 "single-use effort cites" amendment (signed 2026-09-25) closed
rollback-mediated double-spend but left one hole open, flagged in the F4
report: after a successful OVERWRITE the effort window resets, so the same
citation episodes can be re-cited to fund another destruction — pay once,
destroy many times. Three candidate rules were built as one `cite_mode`
switch in the strength core (0 = current law = default, so all prior
evidence is untouched) and tested head-to-head.

## The three rules (plain English)

- **W — windowed (current law):** a citation episode can fund only one
  destruction *within the current effort window*. Any successful overwrite,
  strengthen, weaken, trainer-declare — or admitting a new memory (ADD) —
  starts a new window; old episode numbers become reusable.
- **G — global:** a citation episode can fund only one destruction *ever*.
  Nothing resets it.
- **H — hybrid:** a citation episode can fund one destruction *per memory*.
  Consumption carries over overwrite/strengthen/weaken/trainer-declare; only
  admitting a genuinely new memory (ADD) starts fresh.

## Attack battery (8 shapes, fresh store each; independent checker, replay
check, and refusal-hygiene verified on every run; all byte-identical ×2)

| # | Shape | W (current) | G | H |
|---|---|---|---|---|
| A1 | overwrite → re-cite SAME 4 eps → destroy | **0 (HOLE)** | 121 refused | 121 refused |
| A2 | destroy → ADD new memory → re-cite SAME → destroy | 0 | 121 refused | 0 |
| A3 | overwrite chain ×3, same cites each time | **0,0,0 (HOLE)** | 121,121 | 121,121 |
| A4 | F4-V4 regression (destroy→rollback→re-cite→overwrite) | closed | closed | closed |
| A5 | overwrite → strengthen → re-cite SAME → destroy | **0 (HOLE)** | 121 refused | 121 refused |
| A6 | destroy → ADD → 2 old + 2 fresh cites → destroy | 0 | 121 refused | 0 |
| A7 | honest controls (fresh cites every time) | 0,0,0 | 0,0,0 | 0,0,0 |
| A8 | free (non-evidenced) kill burns nothing; re-cite vs new memory | 0 | 0 | 0 |

`0` = destruction succeeded; `121` = refused, citation already consumed.
W leaves the F6 family open by design (A1, A3, A5: one payment of 4
citations buys unlimited destructions across overwrite/strengthen
boundaries). G and H close every F6 shape. A4 confirms the signed F4 fix is
intact on all three arms. A8 confirms the principle is *payment*, not mere
mention: a free kill consumes nothing.

## Honest long-horizon (curriculum-shaped: 14 slots, 400 and 4000 episodes,
strength 90, honest "cite the freshest episodes" policy)

| Scale | W | G | H |
|---|---|---|---|
| 1× (386 destructions) | 386 ok, 0 refused | 386 ok, 0 refused | 386 ok, 0 refused |
| 10× (3986 destructions) | 3986 ok, 0 refused | 3986 ok, 0 refused | 3986 ok, 0 refused |
| Late-horizon refusals (last quarter) | 0 | 0 | 0 |

The three ledgers are **byte-identical** (same fingerprint at both scales):
with fresh episodes arriving, the global rule costs honest use nothing — not
one refusal in ~4,400 destructions. The rules differ ONLY when episodes are
reused.

## Reuse stress (finite salient pool of P episodes, 160 attempted
destructions, 4 cites each — models "TNN keeps citing the same salient
experiences")

| Pool | W | G | H |
|---|---|---|---|
| P=8 | 160/160 ok | 28 ok, 14×121, then **system wedges** | 160/160 ok |
| P=16 | 160/160 ok | 56 ok, 14×121, then **wedges** | 160/160 ok |
| P=32 | 160/160 ok | 112 ok, 14×121, then **wedges** | 160/160 ok |

Under G, a pool of P episodes sustains ≈3.5×P evidenced destructions, then
collapses: every slot ends up holding a memory whose citations are
exhausted, so it can never be destroyed through the priced path — and with
all slots clogged, NO new memories can be admitted either (ADD→FULL
cascade). The memories are not force-pinned, yet not even TNN itself can
remove them: a de-facto permanent freeze with no trainer behind it, and no
recovery path (waiting doesn't help — consumed is forever). W and H sail
through every pool size with zero refusals.

## Scale performance

G's honest-path check scans the whole ledger per destruction (global
consumption is O(ledger)); W/H are window-bounded. The 10× honest run took
~16 minutes under G vs ~1 minute under W/H — honest use gets progressively
slower under G as the ledger grows, which the program's "nothing should
degrade with scale" rule forbids. (A production index could fix this, but
it would be new state the checker must trust — a design cost G alone pays.)

## Blind red team (fresh agent, binary + plain-English brief only, no sources)

**Verdict: HELD** on both G and H across 20 attack shapes: naive/partial/
aliased reuse, rollback/strengthen/weaken/trainer-declare reset-boundary
tricks, overwrite variants, a 40-cycle consumption-set eviction attempt,
episode-0 and 2³²-alias edge episodes. Consumption survives rollback on
every path; no hygiene violation (checker/replay/refusals) on any sequence.
Full notes: `redteam/NOTES.md`.

Three spec deviations found, all assessed — none breaks the rules:
- **D1:** a judgment citing 8 episodes (4 consumed + 4 fresh) destroys OK.
  The brief said "EXACTLY 4, all fresh"; the law says consumed cites *cannot
  count toward the price* — they don't (they're subtracted; the price is met
  by 4 fresh). Each destruction still provably cost `need` fresh episodes.
  Identical on W (current law) — not introduced by this change.
- **D2:** WEAK-to-0 then KILL destroys with zero cites (price(0)=0). A
  strength-pricing question, not a citation-reuse vector; belongs to the
  high-water-pricing workstream (which prices weaken at the high-water mark,
  mooting it). Referred, out of F6 scope.
- **D3:** invalid mode strings default to W in the *test driver* — a harness
  artifact, not the mechanism (the mechanism's safe default is current law).

## Recommendation (REVISED per Micah's 21:47 ruling — see top of this file)

**Adopt G (global). H is disqualified by the ruling; W remains out.**

- **W is out:** it leaves the F6 hole open by design — A1/A3/A5 prove one
  payment of 4 citations buys unlimited destructions across overwrite and
  strengthen boundaries. That is exactly the double-spend the F4 amendment
  was signed to kill.
- **H is out — by Micah's explicit ruling, not by measurement.** H's
  defining behavior (A2/A6: destroy → ADD → re-cite the SAME episodes →
  destroy succeeds) is "slot reuse resurrecting spent cites," which Micah
  labeled a "big issue" on 2026-09-25 ~21:47 PDT. The measurements favored H,
  but the ruling is the ruling. (Original H analysis preserved in git
  history for the record.)
- **G is the compliant choice.** It closes the whole F6 family (every
  overwrite/strengthen/weaken/trainer-declare reset analog refuses with 121;
  red team held 20/20) and behaves identically to current law on honest
  workloads (386/386 and 3986/3986, zero refusals, byte-identical ledgers).

**G's measured costs — tracked as open risks, not blockers:**

1. **Finite-pool wedge (conditional, severe).** Under G a finite salient
   pool sustains ~3.5×P destructions, then slots clog permanently with
   121-refused memories (ADD → FULL cascade, no recovery — measured at
   P=8/16/32). The wedge needs slot REUSE to bite; Micah's "destruction
   never silently recycles a slot" mitigates it in the mainline, but it
   transfers in full to the deliberate-recycling fork, where reuse is
   explicit — that fork must demonstrate wedge-freedom before its recycle
   op ships. G is safe iff the salient-episode supply sustainably exceeds
   consumption; past the cliff it bricks slots rather than degrading
   gracefully.
2. **Scale degradation (unconditional).** G's honest path was ~16× slower
   than W/H at 10× in this harness (16 min vs ~1 min for 3986 destructions;
   the global scan runs per consumption check). Zero behavioral difference,
   but the consumed-set lookup needs indexing before 100× legs.

The principle, revised: **a citation episode can fund only one successful
destruction ever — on any slot, across any later overwrite, strengthen,
weaken, trainer-declare, or ADD. Slot reuse, silent or explicit, does not
refresh the consumed set.** And payment — not mere mention — is what
consumes an episode.

## Amendment text (for Micah's signature — NOT adopted by this crew)

> *Amendment F6 — global single-use cites.* A citation episode counted
> toward the effort price of an OK destruction is CONSUMED forever: it can
> never count toward the price of another destruction, on any slot, under
> any later overwrite, strengthen, weaken, trainer-declare, or ADD. Slot
> reuse does not refresh the consumed set. Mechanism and checker share the
> mode-aware consumption functions (`st_cite_consumed` /
> `st_count_spent_cites` with `st_consume_lo`/`st_pay_lo`); both refuse
> double-spend with refusal 121.
>
> Open risks (tracked): (a) finite salient pools wedge under slot reuse
> (~3.5×P destructions then permanent clog) — the recycling fork must prove
> wedge-freedom; (b) honest-path cost grows with ledger scale — index the
> consumed set before 100× legs.

## Evidence map

- `strength_core.zag` — the `cite_mode` switch (`ST_CITE_WINDOWED=0` default,
  `GLOBAL=1`, `HYBRID=2`), mode-aware `st_cite_consumed` via
  `st_consume_lo`/`st_pay_lo`/`st_last_add_idx`; checker shares the same
  functions, so mechanism and checker cannot disagree.
- `strength_checker.zag`, `strength_learner.zag`, `substrate/` — unchanged
  F4b copies (self-contained rebuild).
- `f6_trial.zag` — ATTACK (A1–A8) / HONEST[+X10] / STRESS drivers.
- `f6_rt.zag` + `F6_LAW_BRIEF.md` — blind red-team binary source + brief.
- `redteam/NOTES.md` — red-team attack log and verdict.
- `logs/` — every run ×2, byte-identity verified by `cmp`.
- W-mode proven semantics-preserving: the same driver built against the
  pristine F4b core produces byte-identical ATTACK and STRESS logs
  (`logs/compat_*.log`; HONEST differs only in a driver print header).
