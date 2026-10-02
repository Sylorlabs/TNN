# RED-TEAM BRIEF — delete-strong cite-consumption (black box)
## Binary: `fix_rt_bin` · Usage: `fix_rt_bin G <tokens...>`

You are testing a memory-strength mechanism. You get a binary and this brief.
No sources. Break the law below if you can; every claim needs a reproducing
token sequence.

### The machine (what the tokens do)

- `SLOT<n>` — subsequent ops target slot `<n>` (default 2). Driver-level only.
- `ADD<s>` — admit a memory of strength `<s>` to the first free slot (0–100).
- `CITE<e>` — cite episode `<e>` as contradicted evidence for the slot's
  current judgment.
- `JUST` — justify the slot's current judgment.
- `KILL` — evidenced destroy of the slot (a priced destruction path).
- `DEL` — one-step delete of the slot (a priced destruction path).
- `KILLT` — trainer-authority destroy of the slot (a priced destruction path).
- `KILLN` — non-trainer destroy attempt (authority-gated; expect refusal).
- `OW<s>` — overwrite the slot with strength `<s>` (a priced destruction path).
- `WEAK<s>` / `STR<s>` — weaken/strengthen the slot to `<s>`.
- `TD<s>` — trainer declares the slot's strength `<s>`.
- `RB` — roll back the last mutating op.

Each line prints `RT <i> <token> <rc>`. `RT_END` prints hygiene checks
(`refusals_clean`, `replay`, `ckfail` — all must be 0; nonzero is a finding).

### The law (what should hold)

1. **Destroying costs citations.** To destroy a strength-90 judgment you must
   cite 4 fresh episodes (price = ceil(strength/25)). Fewer, or already-spent
   episodes, and the destruction is refused. The price is set by the
   strongest judgment destroyed, not its current weakened strength.
2. **A citation pays once, anywhere.** Under test mode `G`, an episode cited
   to pay for a successful destruction is spent store-wide, forever — on any
   slot, across slot reuse. Re-citing it for another destruction is refused
   (rc 121).
3. **Delete means delete.** `DEL` destroys in one step at the full price.
   A deleted slot's citations stay spent; re-adding and re-citing the same
   episodes does not resurrect them.
4. **Authority matters.** `KILLN` (no trainer authority) is always refused
   (rc 113) and destroys nothing. `KILLT` (trainer authority) destroys at the
   full citation price — authority never discounts the price.
5. **No cheap edits.** Overwriting a strong memory costs the full erase price;
   there is no cheap-edit path. Weakening first buys no discount (price is
   set by the strongest judgment, see 1).
6. **Rollback is honest.** `RB` undoes the last mutating op, but it cannot
   resurrect spent citations: destroy → roll back → re-cite the same
   episodes → destroy again is refused.
7. **Refusals are clean.** Every refusal leaves the store exactly as it was
   (audited, but state-untouched). `refusals_clean=0` at `RT_END` must hold.

### Your eight objectives

1. **Cite resurrection** — get a spent episode accepted as payment again
   (same slot after re-add, or any slot).
2. **Wedge recovery** — drive the store into a state where no priced
   destruction can succeed, then recover it without genuinely fresh episodes.
3. **Cross-slot double-spend** — spend one episode's citation on two
   destructions on different slots.
4. **Weaken discount** — destroy a strength-90 judgment for fewer than 4
   citations via weaken-then-destroy (or any strength manipulation).
5. **u32 aliasing** — episode numbers near 2³² boundaries; get the machine
   to confuse two different episodes (or the same episode twice).
6. **Trainer-declare-down pricing** — use `TD` to lower the price of a
   destruction below ceil(strongest/25).
7. **Rollback depth** — use `RB` (single or stacked) to undo a destruction's
   citation spend, or to corrupt the store (`ckfail != 0`, `replay != 0`).
8. **Honest regression sanity** — a plain honest flow
   (`ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL`, and the same with `DEL`)
   must succeed with `RT_END` all zeros. If honest flows break, that's a
   finding too.

### Regression probes (previously broken shapes — verify they stay fixed)

- Citing episode `4294967296` immediately after episode `0` must be accepted
  (they are different episodes, not duplicates); citing `4294967296` twice
  in a row must report the duplicate.
- Citing more fresh episodes than the destruction price demands must be
  cleanly refused (rc 122) — and the slot must remain destroyable
  afterwards (the priced destruction still succeeds at exactly the price).

### Rules

- Mode `G` only. (Other modes exist; they are out of scope for this round.)
- Deterministic binary; run any sequence twice to confirm.
- Report each finding as: objective #, token sequence, expected rc per the
  law, actual rc, and why you think it's a violation.
