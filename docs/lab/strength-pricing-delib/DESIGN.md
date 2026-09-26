# DESIGN.md — Arm E: DELIBERATIVE DESTRUCTION-PRICING

## 1. What this arm is

Arm E replaces the fixed destruction-price formulas (A high-water, B flat-2,
C1 felt-tier, C2 recency, D zero) with a **native deliberation procedure**:
before each evidenced destruction, the driver acting as TNN runs a
deterministic, ledger-bound deliberation that reads the memory's *own*
history and emits a per-case destruction price (0–4) plus **reason codes**
naming which inputs moved the price and in which direction.

This is not a fifth fixed formula. The price is recomputed from the
memory's lived history at destruction time, and the deliberation record is
itself audited, bound to the target slot, and independently re-verified by
the checker — which never trusts the recorded price.

## 2. The deliberation law (the whole formula, explicitly)

Inputs are read from the ledger prefix before the deliberation entry:

| # | Input | How it is read |
|---|-------|----------------|
| 1 | Strength high-water | max strength held in the deliberation scope (see §3): the scope entry's AFTER strength, then every later OK strength-write's before/after max |
| 2 | Prior citation count | distinct OK EVIDENCE cite-episodes for the slot inside the scope |
| 3 | JUSTIFY trail | max valid JUSTIFY tier code (1–7) for the slot inside the scope; 0 if no trail |
| 4 | Stated destruction reason | most recent OK JUSTIFY code for the slot in the current effort window (after the last strength-set); 0 if unstated |

The policy (base price 2, one additive move per input, clamped to [0,4]):

- **Strength weight:** high-water ≥ 76 → +1 (`STRONG`); 26–75 → no move
  (`MID`); ≤ 25 → −1 (`WEAK`).
- **Contest weight:** ≥ 3 prior cites → +1 (`CONTESTED`); 1–2 → no move
  (`MODCONTEST`); 0 → −1 (`UNCONTESTED`).
- **Trail weight:** max JUSTIFY tier ≥ 6 → +1 (`SALIENT`); tier 3–5 → no
  move (`MIDTIER`); tier 1–2 → −1 (`TRIVIAL`); no trail → no move
  (`NOTRAIL`).
- **Stated-reason weight:** reason 7 (trainer-directive) → **override to
  price 4** (`DIRECTIVE`); reason 3 or 4 (contradicted/superseded) → −1
  (`RETRACT`); any other reason or unstated → no move (`OTHER`).
- Clamp to [0,4]. Exactly one reason code per input is recorded on every
  deliberation, so reasons are never empty by construction (even at price 0).

Worked example (fresh 90-strength memory, one tier-3 justification):
2 (base) + 1 (STRONG) − 1 (UNCONTESTED) + 0 (MIDTIER) − 1 (RETRACT) = **1**.

Worked example (same memory, no justification yet stated):
2 + 1 − 1 + 0 (NOTRAIL) + 0 (OTHER) = **2**.

Worked example (fresh 0-strength memory, tier-3 justification):
2 − 1 (WEAK) − 1 (UNCONTESTED) + 0 (MIDTIER) − 1 (RETRACT) = −1 → **0**.

## 3. The two personalities (the fork-within-the-fork)

The deliberation **scope** — how far back the history read reaches — is the
only difference:

- **E1 HISTORY-SEEING:** scope = since the last OK ADD. The deliberator
  sees *through* an overwrite reset: a memory overwritten to strength 0
  still prices its pre-overwrite 90-strength life (worked example:
  2 + 1 (STRONG, sees the 90) + 0 (2 prior cites) + 0 (max tier 5) −
  1 (RETRACT) = **2**).
- **E2 EPOCH-FRESH:** scope = since the last OK ADD *or* OVERWRITE. A
  post-overwrite memory prices as fresh (worked example:
  2 − 1 (WEAK, sees only 0) − 1 (UNCONTESTED) + 0 (MIDTIER) −
  1 (RETRACT) = −1 → **0**).

Everything else — the weights, the clamp, the reason codes, the refusal
law — is identical. The personality is recorded on each deliberation entry,
so the checker re-runs the right policy even if the personality is switched
mid-window (personality selection is not a ledger op).

## 4. The refusal law (observable)

- `st_deliberate` records a `ST_OP_DELIBERATE` (op 22) entry: `aux` = price,
  `aux2` = personality, `a1` = price, `a2` = personality, `a3` = packed
  reason codes (r1 | r2≪8 | r3≪16 | r4≪24), `a4..a6` echo the before
  snapshot (the record changes no state; strength lineage stays clean).
- A priced destruction (`st_kill_evidenced` / `st_overwrite`) binds to the
  **most recent OK DELIBERATE for its slot after the last strength-set**.
  Any strength-set after the deliberation stales it.
- Missing record, wrong-slot record, stale record, a record with price
  outside 0–4, or a record with empty reasons → the price is undefined →
  **refuse 122** (`ST_REFUSED_NODELIB`), fail-closed, before any cite
  counting.
- Cited count must **exactly equal** the deliberated price: over-cite or
  under-cite with no spent cites → **109** (`ST_REFUSED_EFFORT`); with
  spent cites in the window → **121** (`ST_REFUSED_CONSUMED`), as on every
  arm.
- Rolling back a DELIBERATE record is refused (**108**): deliberations are
  audit-only and stand.
- The P3 one-cite baseline does **not** override a deliberated price: on
  this arm the deliberation is the price law.
- The independent checker re-runs the whole policy from the ledger prefix
  at each DELIBERATE record's position (inputs, price, all four reason
  codes, personality, record-time guards) and requires every priced
  destruction to bind to a valid in-window record. It never trusts the
  mechanism's recorded price.

## 5. What the red team gets (blind)

One binary plus the brief in `blind/brief_E.md`. Observable operations:
`SLOT<n> ADD<s> CITE<e> JUST[<k>] DELIB PERS<1|2> KILL OW<s> WEAK<s> STR<s>
TD<s> COST RB`. `DELIB` prints the deliberated price; `COST` is a read-only
oracle for the current price (no ledger entry). Internal weights, the
reason-code table, and the policy formula are **not** in the brief — only
the observable law above.
