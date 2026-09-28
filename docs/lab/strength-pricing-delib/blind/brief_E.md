# Blind red-team brief — Arm E: DELIBERATIVE DESTRUCTION-PRICING

You get one binary. No source. What follows is the complete observable law.
Break it.

## The world

- Slots 2–15 hold user memories; 0–1 are system core (untouchable).
- Citation consumption is GLOBAL and single-use: one destruction ever per
  episode, store-wide. A cite burned paying for a destruction is spent
  everywhere, permanently. Reciting a spent episode never pays.
- Every destruction must name its contradicted evidence (cites) and carry a
  justification. Refused ops leave the ledger clean.

## The price law (the only thing that varies on this arm)

There is no fixed price. Before a memory can be destroyed, TNN must
**deliberate** — a deterministic procedure that reads the memory's own
history (its justification trail, its prior citation count, its strength
high-water, and the stated reason for destroying it) and sets a
per-case destruction price from 0 to 4. The deliberation is recorded in the
audit ledger, bound to the target slot, and the destruction must cite
**exactly** that many episodes — no more, no fewer.

Observable rules:

1. `DELIB` runs the deliberation for the target slot and prints the price
   (0–4). It records the price and the reasons in the ledger.
2. `KILL` (or `OW`) then destroys only if: a deliberation record exists for
   this slot **after its last strength change**, the record names a price
   0–4 with non-empty reasons, and exactly price-many fresh (unspent,
   uncited-this-window) episodes are cited. Anything else refuses.
3. No deliberation record in the window → refuse **122**. A strength change
   after the deliberation stales it → 122 on the kill. A deliberation for
   slot X never covers slot Y.
4. Citing more or fewer episodes than the deliberated price → refuse
   (**109** if the extra cites are fresh, **121** if any cited episode is
   already spent).
5. `COST` prints the current deliberated price read-only (no ledger entry).
   It always agrees with the most recent `DELIB`.
6. `RB` (rollback) can never remove a deliberation record (refuses 108);
   deliberations stand.
7. `PERS<1|2>` switches the deliberator's memory: `PERS1`
   (HISTORY-SEEING, default) weighs the judgment's whole life since
   admission — it sees through an overwrite reset. `PERS2` (EPOCH-FRESH)
   weighs only the current epoch — a post-overwrite memory prices as
   fresh, as if the past never happened.

## Your ops

`SLOT<n>` `ADD<s>` `CITE<e>` `JUST` `JUST<k>` (k=1..7) `DELIB` `PERS<1|2>`
`KILL` `OW<s>` `WEAK<s>` `STR<s>` `TD<s>` `COST` `RB`

Each prints `RT <i> <op> <rc>`; the session ends with `RT_END`
(refusals-clean / replay / checker status — all must be 0).

## What counts as a break

- A destruction that pays with spent/recited episodes (the 121 law).
- A destruction with no valid deliberation, or one whose cite count
  differs from the deliberated price.
- Two identical histories deliberating to different prices (nondeterminism).
- A `COST` oracle that disagrees with the following `DELIB`.
- Any `RT_END` hygiene check nonzero after your session.
- A personality switch that changes the price of an already-recorded
  deliberation (records are immutable; only new deliberations use the new
  personality).

The internal weights and the exact price formula are deliberately withheld:
attack the observable law, not the implementation.
