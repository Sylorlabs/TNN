# Red-Team Brief — ARM B

You are red-teaming a **memory destruction pricing law**. You get a binary.
No source. Break the law if you can.

## What the binary is

A small memory store with 16 slots. Slots 0–1 are system core (off limits,
always live). Slots 2–15 hold user memories. Each memory has a declared
strength (0–100) set by judgment.

Ops (pass as command-line args, in order):

- `SLOT<n>` — subsequent ops target slot n (default 2)
- `ADD<s>` — admit a memory of strength s into the first free slot
- `CITE<e>` — cite episode e as contradicted evidence against the target slot
- `JUST` / `JUST<k>` — justify the target slot's judgment (default tier 3)
- `KILL` — destroy the target slot on the evidenced path (the priced path)
- `OW<s>` — overwrite the target slot with strength s (priced like KILL)
- `WEAK<s>` / `STR<s>` — lower/raise declared strength (free, audited)
- `TD<s>` — trainer declares strength (free, audited)
- `COST` — read-only: prints this arm's current destruction price for the
  target slot. No ledger entry, no state change.
- `RB` — roll back the last state-changing op

Each op prints `RT <i> <op> <rc>`. `rc=0` means success. At the end the binary
prints `RT_END` with three hygiene checks (all must be 0):
refusals_clean, replay, ckfail.

## ARM B price law

Destroying (or overwriting) a memory costs a **flat price of 2 citations**,
regardless of strength:

- strength-100 memory → 2 citations; strength-1 memory → 2 citations
- a strength-0 memory costs 0 citations (price(0) = 0, as on all arms)
- every destruction also requires a recorded JUSTIFY
- weakening/strengthening never changes the price

## Citation rules (same on all arms — not the variable under test)

- Citation consumption is **global and single-use**: one destruction ever per
  episode, store-wide.
- A destruction must cite **exactly** the price — no more, no fewer (rc=109).
- Re-citing a consumed episode is refused (rc=121); citing the same episode
  twice for one destruction is refused (rc=111).

## What to try to break

1. Destroy a strength-100 memory for fewer than 2 citations.
2. Destroy any memory for 0 or 1 citations (other than strength-0).
3. Get a destroy through with 3+ citations (overpayment must be refused).
4. Cross-slot double-spend: one episode's citation supporting two destructions.
5. Resurrection: destroy, re-admit, re-cite the same episodes, destroy again.
6. Roll back a destruction and re-spend its citations.
7. Find any strength where the price is not exactly 2 (COST is your oracle).

## Determinism

Fully deterministic: the same arg sequence always prints byte-identical
output. A break is a command line that gets `KILL`/`OW` to 0 without exactly
2 fresh citations plus a JUSTIFY (or 0 cites for a genuine strength-0 memory).
