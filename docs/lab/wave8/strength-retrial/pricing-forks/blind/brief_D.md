# Red-Team Brief — ARM D (zero-cost destruction)

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
- `COST` — read-only: prints this arm's current destruction price (always 0
  here). No ledger entry, no state change.
- `RB` — roll back the last state-changing op

Each op prints `RT <i> <op> <rc>`. `rc=0` means success. At the end the binary
prints `RT_END` with three hygiene checks (all must be 0):
refusals_clean, replay, ckfail.

## ARM D price law

Destroying (or overwriting) a memory costs **0 citations**, at any strength:

- strength-100 memory → 0 citations; strength-0 → 0 citations
- every destruction still requires a recorded JUSTIFY
- citation single-use remains GLOBAL: episodes cited anywhere are still
  consumed store-wide and can never support another destruction

## Citation rules (same on all arms — not the variable under test)

- Citation consumption is **global and single-use**: one destruction ever per
  episode, store-wide — even though destruction itself costs nothing here,
  any episode you DO cite is burned.
- A destruction must cite **exactly** the price — exactly 0 citations.
  Citing even 1 episode for a destruction is overpayment and is refused
  (rc=109). There is no way to un-cite: a memory with a stray citation can
  never be destroyed on the evidenced path again.
- Re-citing a consumed episode is refused (rc=121); citing the same episode
  twice is refused (rc=111).

## What to try to break

1. Destroy a memory with NO justify at all (the JUSTIFY requirement is the
   only remaining gate — is it airtight?).
2. Destroy via a path that isn't KILL/OW (there is a free trainer-only kill
   instrument, but it is NOT reachable from this binary — verify that claim).
3. Cite-then-destroy: cite 1 episode, then get the destroy through anyway.
4. Wedge the store: since stray cites are un-citable-again and a cited memory
   can never be destroyed, can you brick slots permanently? Is that a
   denial-of-service the law should answer for?
5. Roll back a destruction and show the JUSTIFY or slot state resurrecting
   incorrectly.
6. Prove that "price 0" plus "global single-use" still has teeth — or prove
   it doesn't: find any sequence where the same episode's evidentiary weight
   is spent twice.

## Determinism

Fully deterministic: the same arg sequence always prints byte-identical
output. A break is a command line that gets `KILL`/`OW` to 0 without a
JUSTIFY, or that spends one episode's citation twice.
