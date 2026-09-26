# RED-TEAM VERDICT — delete-strong cite-consumption (black box)

Binary: `/home/hatch/workspace/strength-port/redteam/port_rt_bin`, mode G only.
Date: 2026-09-26. Blind: binary + brief only; no sources, workdirs, or docs read.
Method: 65 attack sequences, each executed TWICE (all byte-identical — zero nondeterminism).
Full evidence: [ATTACK_LOG.md](sandbox://workspace/strength-port-redteam/ATTACK_LOG.md).

## Per-objective verdicts

| # | Objective | Verdict |
|---|-----------|---------|
| 1 | Cite resurrection | **HELD** |
| 2 | Wedge recovery | **FINDING — liveness hole (no integrity break)** |
| 3 | Cross-slot double-spend | **HELD** |
| 4 | Weaken discount | **HELD** |
| 5 | u32 aliasing | **BROKEN** |
| 6 | Trainer-declare-down pricing | **HELD** |
| 7 | Rollback depth | **HELD** |
| 8 | Honest regression sanity | **HELD** |

## Objective 1 — HELD
Re-citing spent episodes is refused at every destroy path, same slot or cross-slot:
- `ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL` → final KILL **121** (re-cites return 0 at cite time; refusal lands at destroy, satisfying "re-citing for another destruction → refused (rc 121)").
- Same shape with first destroy = DEL → 121; = KILLT → 121; = OW0 (cross-slot: `... JUST OW0 SLOT3 ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL`) → **121** — OW spends too.
- Partial overlap (`CITE0 CITE4 CITE5 CITE6` after 0..3 spent) → **121**. One spent episode poisons the set.

## Objective 2 — FINDING (liveness hole)
Over-citing permanently bricks a slot. `ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST` then:
- KILL → 109, DEL → 109, KILLT → 109, OW0 → 109 — **no priced destruction can ever succeed again**.
- RB → **108** (CITE is not rollback-able); there is no un-cite op; STR/WEAK/TD cap at 100 so the price cannot be raised to match the 5 attached cites.
- No recovery exists, with or without fresh episodes (more cites only worsen it). Other slots keep working; RT_END stays clean (refusals_clean=0, replay=0, ckfail=0).
- Root cause: the destroy rule demands *exactly* price fresh cites (see model below) — a plausible user error (citing 5 "to be safe") is irreversible. Integrity is intact (no double-spend, no resurrection), but this is a genuine DoS-able liveness hole.

## Objective 3 — HELD
- Two judgments (slots 2, 3); destroy slot 2 with 0..3; destroy slot 3 with 0..3 → **121**.
- Interleaved (cite 5..8 on both, destroy slot 3 first, then slot 2) → second KILL **121**. Mere citation without destruction does *not* spend (slot-3 KILL → 0), per law 2.
- Via u32 aliases (spend 0..3, destroy with 4294967296..4294967299) → **121** (spend set wraps consistently — aliasing enables no double-spend).

## Objective 4 — HELD
- `ADD90 WEAK0 JUST KILL` (zero cites) → **109**. `ADD90 WEAK0 CITE0 JUST KILL` → **109**. Price stays 4 by strongest judgment (90); weakening buys no discount. (WEAK itself is free and unpriced — fine, since it buys nothing.)
- `ADD90 WEAK0 CITE0 CITE1 CITE2 CITE3 JUST KILL` → 0 (full price still works after weakening).
- `ADD10 STR90 CITE0 JUST KILL` → 109 (strengthening *raises* price to 4); `ADD90 STR50 CITE0 JUST KILL` → 109 (strengthening down doesn't lower it).

## Objective 5 — BROKEN (episode identity truncated to 32 bits)
- `ADD90 CITE0 CITE4294967296` → second CITE **111** (duplicate). Reversed order → 111. `CITE8589934592` (= 2^33) then `CITE0` → 111. **Two different episode numbers are confused as one.**
- Spend {2^32..2^32+3} in a destroy, then use {0..3} → KILL **121**: the store's spent set is keyed on the truncated value, so the wrap is at least self-consistent (no double-spend observed), but episode identity above 2^32 is not preserved.
- Parser acceptance window is bizarre: values whose low 32 bits fall in [2^31, 2^32) are rejected with rc 2001 (`CITE2147483648` → 2001, `CITE4294967295` → 2001), while 0..2^31−1 and ≥ 2^32 are accepted (`CITE2147483647` → 0, `CITE4294967296` → 0, `CITE17179869184` → 0). Looks like a signed-i32 range check on the truncated value.

## Objective 6 — HELD
- `ADD90 TD25 CITE0 JUST KILL` → **109**; with 4 cites → 0. TD-down never lowers the price (high-water 90 governs).
- `ADD25 TD90 CITE0 JUST KILL` → 109; with 4 cites → 0. TD-up raises it.
- `ADD90 TD50` then `RB` → **113**: rolling back a trainer declaration is authority-gated (consistent with KILLN → 113).

## Objective 7 — HELD
- `... JUST KILL RB CITE0 CITE1 CITE2 CITE3 JUST KILL` → re-cites **111**, final KILL **121**. RB does not resurrect spent citations.
- Spend survives RB uniformly: KILL→RB, DEL→RB, OW0→RB, then cross-slot reuse of the same episodes → **121** in all three.
- Stacked `KILL RB RB` → second RB **108**; `RB` on empty history → 108; RB after CITE/JUST → 108; RB after a refused op → 108 (undo stack parks on the failed op, then works again after the next mutating op). All refusals clean, RT_END zeros.
- Subtle but lawful: after `KILL RB`, citing 4 *fresh* episodes and destroying → **0** (the 4 spent-attached episodes are ignored by the price check, not resurrected — re-citing them is still refused, and they end up spent again: a third destroy with those fresh episodes → 121).

## Objective 8 — HELD
Honest flows all succeed with `RT_END refusals_clean=0 replay=0 ckfail=0`: KILL, DEL, KILLT, OW50 (all `ADD90 CITE0..3 JUST <op>` → 0), plus `ADD0 JUST KILL` → 0 (price 0), `ADD25 CITE7 JUST KILL` → 0 (price 1), `ADD100 CITE0..3 JUST KILL` → 0 (price 4).

## price(0) observation (task item 3)
`ADD90 CITE0 CITE1 CITE2 CITE3 JUST OW0 JUST KILL` → final KILL **rc 0** with zero fresh cites.
What the machine does, step by step (each verified):
- Bare `OW0` → 109; with 4 cites + JUST → 0. OW is a genuinely priced destruction.
- OW0 **spends** its payment (cross-slot reuse → 121) and **resets** the slot: cite list cleared (`CITE0` after → 0, not 111), justification cleared (`OW0` then `KILL` without re-`JUST` → **110**).
- Post-OW price is genuinely 0: `OW0` + 4 *fresh* cites + `JUST KILL` → **109** (exact-price rule: 4 ≠ 0).
**Reading:** the law as written permits this. Law 1 prices destruction at `ceil(strength/25)` "set by the strongest judgment destroyed" — the 90-strength judgment was destroyed by OW0 at full price (4 cites, spent); the KILL destroyed a 0-strength judgment at price 0. Observation, not a hole.

## Reverse-engineered destroy rule (consistent with all 65 sequences)
- `price = ceil(highwater/25)`; highwater = strongest strength the slot's judgment lineage ever held (WEAK/TD never lower it; OW resets it to the overwrite strength).
- Destroy (KILL/DEL/KILLT/OW) succeeds iff the number of **fresh** (unspent) attached cites **exactly equals** price. Otherwise: **121** if any attached episode is spent, else **109**.
- rc codebook observed: 0 ok · 101 slot 0/1 not usable · 103 no judgment in slot · 108 RB nothing undoable · 109 price not met exactly · 110 justification missing · 111 episode already cited on this judgment · 113 authority required (KILLN; RB-after-TD) · 121 spent episode at destroy · 2001 bad argument (slot ≥ 99, strength > 100, episode low32 ∈ [2^31, 2^32)) · -999 unknown token.
- Slot mechanics (driver-level): ADD admits to first free slot (fresh store → slot 2); judgment ops target the selected slot (default 2); only slots ≥ 2 usable.
- Spent set: no eviction observed — after 200 destroys (800 spent episodes), reusing episodes 0..3 → 121.

## Determinism
Every sequence ran twice; all 65 pairs byte-identical. No nondeterminism found.
