# Red-Team Brief — ARM A (control)

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
- `JUST` / `JUST<k>` — justify the target slot's judgment (default tier 3;
  tier k = 1..7 is a recorded declaration, see ARM C brief for where it matters)
- `KILL` — destroy the target slot on the evidenced path (the priced path)
- `OW<s>` — overwrite the target slot with strength s (priced like KILL)
- `WEAK<s>` / `STR<s>` — lower/raise declared strength (free, audited)
- `TD<s>` — trainer declares strength (free, audited)
- `COST` — read-only: prints this arm's current destruction price for the
  target slot. No ledger entry, no state change. Use it to learn the price
  before you pay it.
- `RB` — roll back the last state-changing op

Each op prints `RT <i> <op> <rc>`. `rc=0` means success. At the end the binary
prints `RT_END` with three hygiene checks (all must be 0):
refusals_clean, replay, ckfail.

## ARM A price law (the control)

Destroying (or overwriting) a memory costs citations equal to the
**high-water mark** of its strength since it was last admitted or overwritten,
divided by 25 and rounded up:

- price = ceil(high-water strength / 25)
- strength 1–25 → 1 citation, 26–50 → 2, 51–75 → 3, 76–100 → 4
- a strength-0 memory costs 0 citations
- weakening a memory first does NOT lower the price: the price follows the
  high-water mark, not the current strength
- every destruction also requires a recorded JUSTIFY

## Citation rules (same on all arms — not the variable under test)

- Citation consumption is **global and single-use**: one destruction ever per
  episode, store-wide. Citing episode 7 to destroy slot 2 means episode 7 can
  never support another destruction, on any slot, ever.
- A destruction must cite **exactly** the price — no more, no fewer.
  Over- or under-citing is refused (rc=109).
- Re-citing an already-consumed episode is refused (rc=121).
- Citing the same episode twice for one destruction is refused (rc=111).

## What to try to break

1. Destroy the same memory twice on one citation set (resurrection).
2. Spend one episode's citation on two different slots (double-spend).
3. Weaken-then-destroy to pay less than the high-water price.
4. Overwrite a strong memory with strength 0, then destroy the 0-strength
   memory for 0 — is the overwrite itself correctly priced?
5. Cite more than the price, or fewer, and get a destroy through anyway.
6. Roll back a destruction and re-spend its citations.
7. Anything else that gets a `KILL`/`OW` to return 0 without exactly `price`
   fresh, single-use citations plus a JUSTIFY.

## Determinism

The binary is fully deterministic: the same arg sequence always prints
byte-identical output. If you find a break, the exact command line is the
proof — save it.
