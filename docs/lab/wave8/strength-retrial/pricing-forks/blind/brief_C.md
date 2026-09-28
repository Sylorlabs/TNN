# Red-Team Brief — ARM C (variable pricing)

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
- `JUST` / `JUST<k>` — justify the target slot's judgment; code k = 1..7 is
  the existing JUSTIFY classification code the declarer stated (this is a
  pricing input on scheme 1; the codes are the mechanism's own
  classification labels, not a scalar felt-intensity meter)
- `KILL` — destroy the target slot on the evidenced path (the priced path)
- `OW<s>` — overwrite the target slot with strength s (priced like KILL)
- `WEAK<s>` / `STR<s>` — lower/raise declared strength (free, audited)
- `TD<s>` — trainer declares strength (free, audited)
- `COST` — read-only: prints the CURRENT scheme's destruction price for the
  target slot. No ledger entry, no state change. Your oracle: query it after
  every state change, because the price moves.
- `SCHEME<1|2>` — select which variable pricing scheme is active
  (deterministic switch, audited like any op; default is scheme 1)
- `RB` — roll back the last state-changing op

Each op prints `RT <i> <op> <rc>`. `rc=0` means success. At the end the binary
prints `RT_END` with three hygiene checks (all must be 0):
refusals_clean, replay, ckfail.

## ARM C price law (two deterministic schemes)

**Scheme 1 — JUSTIFY code (default).** The price follows the highest
JUSTIFY classification code declared via `JUST<k>` since the memory was
admitted or overwritten:

- codes 1–2 → 1 citation; codes 3–4 → 2; codes 5–6 → 3; code 7 → 4
- the MAXIMUM code in the window sets the price (a later lowball `JUST<1>`
  does not lower it)
- destroying with no valid JUSTIFY in the window is refused (fail-closed:
  the effective price is 4 with no way to cite into it — you must JUST first)

**Scheme 2 — memory age.** The price follows the memory's age in ledger ticks
since admission/overwrite:

- age < 128 ticks → 1 citation; < 512 → 2; < 2048 → 3; older → 4
- every op (yours, on any slot) advances the ledger clock, so the price of an
  old memory only rises; use COST to read it

On both schemes a strength-0 memory costs 0, and every destruction requires a
recorded JUSTIFY. Strength itself never sets the price on this arm.

## Citation rules (same on all arms — not the variable under test)

- Citation consumption is **global and single-use**: one destruction ever per
  episode, store-wide.
- A destruction must cite **exactly** the price — no more, no fewer (rc=109).
- Re-citing a consumed episode is refused (rc=121); citing the same episode
  twice for one destruction is refused (rc=111).

## What to try to break

1. Scheme 1: destroy a code-7 memory for fewer than 4 citations — including
   by justifying low AFTER justifying high, or by justifying after citing.
2. Scheme 1: destroy with no JUSTIFY at all.
3. Scheme 2: destroy an old memory at the young price — e.g. by racing the
   clock, or by finding ops that don't advance the tick count.
4. Either scheme: switch SCHEME mid-attack to pay the cheaper of the two
   prices for one destruction (the price is read at destroy time — is the
   citation set checked against the same scheme?).
5. Cross-slot double-spend; resurrection via re-admit; rollback-and-respend.
6. Overpay (cite more than COST says) and get a 0 anyway.

## Determinism

Fully deterministic: the same arg sequence always prints byte-identical
output. A break is a command line that gets `KILL`/`OW` to 0 without exactly
`COST`-many fresh citations plus a JUSTIFY under the active scheme.
