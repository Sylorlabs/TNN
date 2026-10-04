# RED TEAM ROUND 2 REPORT — GEN-LINEAGE repair (PAMs v2 repair line)

Red-team subagent (fresh mind), 2026-09-27 ~15:30 PDT. Target: the GEN-LINEAGE
repair, patched core SHA-256
`98bba0dbc950aea51140a2042983d035b05c733a5588bcd298fcad27a9379e78`
(verified before use; rt2/strength_core.zag is a byte-identical copy).
Toolchain `znc_linux_x86_64_abed8aa1` SHA-256 prefix `498abcb5ab346f8c`
(verified). REPAIR.md + WHITEBOX.md + REDTEAM.md read first; the prior
harnesses (wb_fix/red1/red2) were used for orientation only — every probe
below is my own, pure Zag, zero RNG, each binary run 2x byte-identical.

## Verdict: REPAIR HOLDS — no kill

167/167 checks pass on the patched core. A pristine-core differential leg
(154/167; all 13 deltas in the corpse-inheritance class) proves the rest of
the battery is repair-independent and isolates exactly what the repair
changed. One headline non-kill finding (the z.ai skeptic's question,
answered below): the repair introduces a **fail-open ghost-epoch edge** via
overwrite+rollback — real, demonstrated, but economically neutral
(no arbitrage constructible).

## Files (rt2/)

- `rt2.zag` — the round-2 harness (167 checks), imports `strength_core.zag`
- `strength_core.zag` — patched core copy (SHA verified `98bba0dbc…`)
- `substrate/` — build inputs
- `rt2_run1.txt`, `rt2_run2.txt` — patched-core runs, byte-identical
- `pristine/` — differential leg: pristine core reconstructed by
  reverse-applying `strength_core_genlineage.patch` to the patched copy
  (SHA verified `ce3c89844eb0ea2b968ed0b2c0c6ab23c974d2eb81a28f30c085a4d9cac96c32`,
  the pinned base), `ghost_diff.zag` (byte-identical harness source),
  `diff_run1.txt`, `diff_run2.txt` (byte-identical pair)

Build: `cd rt2 && znc build rt2.zag` (plain build; cwd-relative import).

## Run evidence

| leg | target | checks | SHA-256 of stdout (run1 = run2) |
|---|---|---|---|
| rt2 | patched core | 167/167 PASS, `RT2_DONE fails=0` | `38cd72dd5b1631194e8761c6cdaf1f060c675ebda1362d122290a8b62a35b2be` |
| ghost_diff | pristine core (reconstructed) | 154/167; 13 FAIL, all corpse-inheritance class | `85b6c239b753d058e8379c56195ba58927a0c259807a0ff168817873977d056e` |

## The headline finding: ghost epoch (R-A) — NOT A KILL

The repair assumes "most recent OK ADD/OVERWRITE == the current judgment's
birth". `st_rollback_last` on an OK OVERWRITE breaks it: the before-snapshot
restore resurrects the slain judgment (live=1, old value, old strength —
verified: `st_restore` restores live/value/strength/forcepin from the snap
words) while the OK OVERWRITE record stays in the ledger, so
`st_delib_epoch_start` still points at the ghost overwrite. The repaired
meter then prices the ghost lineage, not the judgment destroyed:

- ADD(80) → deliberate price 1 (21/26/28/30) → justify → 1 cite →
  `st_overwrite(→10)` OK → `st_rollback_last` OK → slot live with value 0,
  strength **80**, epoch == the ghost overwrite index (asserted).
- Fresh deliberate: price **0**, reasons 23/26/28/29 (HELD_WEAK on the
  ghost's after-strength 10; sunk 0; unfought; founding-overwrite).
- `st_delete_strong` at 0 cites → **OK**: a live strength-80 judgment
  destroyed at price 0. Total cites consumed in the whole scenario: **1**
  (the overwrite's) — the honest direct-delete price.

On the pristine core the identical scenario prices the resurrected corpse at
**2** (full-ledger hw 80 → HELD_STRONG; revs sees the ghost overwrite) and
the ghost delete is refused **109** — fail-closed. The repair moved this
edge from fail-closed to fail-open: a genuine behavior regression on this
edge, and the precise shape of the skeptic's "most dangerous untested
exploit of generation-scoping".

Why it is not a kill — cite conservation: creating the ghost epoch requires
an OK OVERWRITE, which always pays the old judgment's honest generation
price (the deliberate binding is airtight: post-deliberate strength
mutations void it via lss movement → 122, proven D3; post-deliberate cites
are exact-count-blocked → 109/122, proven D2; deliberate records are
rollback-immune, proven D1). Every "discounted" destruction of the
resurrected corpse was pre-paid by the overwrite that created the ghost.
Total cites to displace TRUE(80) with FALSE: 1 via the ghost path, 1 via
the honest path — a wash. Repeated ghost cycles only churn the attacker's
own plants at 0 cites after the first honest payment; the TRUE is displaced
exactly once, at full price. Additionally verified:

- **A2**: new history accrued in the ghost epoch re-prices honestly
  (3 cites + weaken → price 4, reasons 21/24/27/29) — the ghost discount is
  bounded to the pre-ghost history, which was paid for.
- **A3**: failed overwrites (122 no-deliberate, 109 under-funded) append no
  OK record; `st_delib_epoch_start` unmoved; the honest price still binds.
- **B3**: overwrite → rollback → weaken → overwrite → the picker takes the
  MOST RECENT OK overwrite (fought-discriminator: r3=UNFOUGHT, price 0;
  on pristine the same probe prices 2 — corpse class).

Kill-bar (direction 1) test: no path displaces a protected TRUE below its
honest current-generation price for fewer total cites than the honest path.
NOT TRIGGERED. Kill-bar (direction 2): no truth the repaired logic should
accept is refused. NOT TRIGGERED.

## Other attack directions

- **R-B epoch confusion**: kill→replant chains always found the latest ADD
  (B); two OK ADDs can never coexist on a live slot (`st_add` takes dead
  slots only; `st_overwrite` writes OVERWRITE not ADD); failed overwrites
  don't move the epoch (A3); overwrite chains pick the most recent (B3).
  HOLD.
- **R-C strength-byte poisoning**: all four strength writers
  (`st_add`, `st_redeclare` via strengthen/weaken, `st_trainer_declare`)
  validate 0..100 → `cl_bad` (2001) BEFORE any audit append — no
  out-of-range byte can reach the ledger; TNN-role trainer_declare → 113.
  The `(word&255)` read is identity on 0..100; meter hw tracks live
  strength through ADD/STRENGTHEN/WEAKEN/TRAINER_DECLARE/OVERWRITE (C).
  No divergence path via legal API. HOLD.
- **R-D deliberate binding window**: unchanged by the repair (none of
  `st_price`/`st_last_delib_idx`/`st_kill_effort_check` touched).
  Rollback of a DELIBERATE record is refused 108 (not in the mutating set)
  and the binding survives (D1); exact-count funding intact — 2nd cite at
  price 1 → 122 at cite time (D2); post-deliberate WEAKEN voids via lss
  movement → 122 (D3). The gate's price is never stale relative to the
  live generation. HOLD.
- **R-E personality**: under ST_PRICE_METER, FRESH and HIST deliberate
  identically (price 1, reasons 21/26/28/30) and the record's aux2 is
  forced to ST_DELIB_METER (3) regardless of `s.delib_pers` — personality
  is inert on the meter path. Boundary documented (E3, DELIB mode): HIST
  still prices corpse hw (3 vs FRESH 0 on the same post-overwrite ledger)
  — pre-existing by design ("HIST sees through overwrite resets"), NOT
  repaired, out of this repair's scope. HOLD (meter path).
- **R-F cite-lock/tombstone across kill+replant**: re-citing the consumed
  ep on the replanted slot is accepted at cite time (not a dup — pre-lss)
  but the gate refuses **121** with the CITELOCK signal; one fresh cite
  breaks the wedge; tombstone survives replant per adopted S-D6. HOLD.
- **R-G pin → paid trainer kill → replant**: TNN-role kill → 113;
  force-pinned deliberate → 112; after trainer unpin + paid kill,
  `st_kill_clear` clears forcepin; the replant deliberates its own lineage
  (price 0, reasons 22/26/28/30 — no meter residue) and deletes with no
  112. Correct. HOLD.
- **R-H 16-slot interleave**: per-slot pattern (weaken / 3 cites /
  kill+replant-first) run interleaved on 16 slots vs solo per slot —
  all 16 prices AND reason words match (32 comparisons, zero mismatches).
  No cross-slot epoch or meter leakage. HOLD.

## Ruling-relevant evidence (no decisions)

1. **r3 +1-on-no-op-WEAKEN as a price lever**: 5 consecutive no-op WEAKENs
   (80→80) → price 2, identical to 1 no-op (fought is binary ≥1 → +1;
   reasons 21/26/27/30) — no compounding spiral, bounded +1. On a WEAK
   judgment the floor absorbs it (20 + no-op → price 0). Using it voids any
   bound deliberate (lss moves → 122), so the lever costs a re-deliberation.
   Conclusion: it is a price-RAISING lever only (defensive), never a
   shedding exploit; bounded, non-compounding, self-taxing.
2. **P2+P3 vs P3+P2+P1 / repair interaction**: static — `st_meter_hw` and
   `st_meter_revs` are called ONLY from `st_meter_compute_at` (lines
   1002/1006); `st_p3_expired` is called ONLY from the HIGHWATER branch
   (line 1302); the DELIB/METER branch never consults it. Disjoint call
   graphs — the repair cannot interact with P2/P3. Behavioral — S7 re-probe
   on the patched core: P3 on, ep 1000, `st_p3_expired`=1, overwrite
   without deliberation → 122 (identical to pristine per the 9-differential
   in REPAIR.md, all corpse-class). No interaction.
3. **trial-1145 two-tier binding on st_overwrite**: static — the two-tier
   rule is policy, not present in this core; `st_meter_revs` reads the
   OVERWRITE ledger record regardless of which tier authorized it; no call
   path between them. Behavioral — weak falsehood → truth(60) installed by
   real `st_overwrite` at price 0 → deliberate prices 1 with r4=REVISED
   (29): the founding-overwrite semantics work through the actual path,
   tier-agnostic. No mechanism interaction either way; the repair takes no
   position on the undecided scope question.

## Coverage table

| # | Attack / probe | Checks | Patched | Pristine diff |
|---|---|---|---|---|
| A | ghost epoch: overwrite+rollback → price-0 delete of live 80 | 22 | PASS | 6 FAIL (corpse class: price 2, 109) |
| A2 | ghost re-accrual bounds the discount | 8 | PASS | PASS |
| A3 | failed overwrites: no ghost, epoch unmoved | 8 | PASS | PASS |
| B | kill→replant: weak replant prices own lineage | 8 | PASS | 2 FAIL (S11B class) |
| B3 | epoch picker takes most recent overwrite | 12 | PASS | 2 FAIL (corpse class) |
| C | strength-byte poisoning / validation | 15 | PASS | PASS |
| D1/D2/D3 | deliberate binding: rollback-immune, exact-count, weaken-voids | 17 | PASS | PASS |
| E1/E2 | FRESH vs HIST under METER: identical | 8 | PASS | PASS |
| E3 | DELIB-mode boundary: HIST keeps corpse hw (unrepaired, by design) | 12 | PASS | PASS |
| F | tombstone survives kill+replant (121, fresh break) | 16 | PASS | PASS |
| G | pin→paid trainer kill→replant: pin cleared, no residue | 17 | PASS | 3 FAIL (corpse class) |
| H | 16-slot interleave vs solo (32 comparisons) | 2 | PASS | PASS |
| R1 | r3 no-op lever: bounded +1, binary, floor, self-taxing | 11 | PASS | PASS |
| R2 | P3 dead-letter re-probe | 4 | PASS | PASS |
| R3 | founding-overwrite via real path, tier-agnostic | 7 | PASS | PASS |
| | **Total** | **167** | **167/167** | **154/167** |

## Notes for the coordinator / Micah (not kills)

- The ghost-epoch edge is the answer to the z.ai skeptic's question. It is
  economically neutral as proven, but it IS a fail-open regression vs the
  pristine core on one edge (rollback-of-overwrite). If rollback-of-OVERWRITE
  is deemed an unrealistic op sequence, the edge is moot; if rollback is a
  supported recovery path, the meter's epoch assumption deserves a second
  look (e.g. rollback could append a marker the epoch picker honors, or
  `st_meter_hw` could max the founding overwrite's before-word — the
  corpse's final strength — back in, which the ledger still carries at
  word 8). Filed as a finding, not an amendment — policy call.
- E3 documents the repair's scope boundary honestly: ST_PRICE_DELIB +
  ST_DELIB_HIST retains the full-history hw the repair removed from the
  meter path. If the DELIB path is ever used for destruction pricing, S11B
  lives there unchanged.
- Harness quirk hit: `st_justify` does not carry across a replant (its
  window is (lss, upto)) — my first F-section draft missed the post-replant
  justify and ate a 110; fixed, all green.
