# IMPORTANCE METER (arm M) — Design

Micah-approved fork, 2026-09-26: "try out the non lowball able meter as a fork."
Pure Zag, zero randomness, byte-identical reruns. Branch: `tnn-native-lab`.

## The problem it answers

Arm E (deliberative pricing) reads four inputs: strength high-water, prior
cite count, max JUSTIFY tier, and the latest stated destruction reason.
Two of those four are **self-reportable labels**: `st_justify` accepts any
code 1–7 from the TNN role with no gating and no evidence binding. A memory
can say "trivial" (tier 1) to cheapen its death or "supremely important"
(tier 7) to inflate it, and arm E's price moves. That is a label with extra
steps — the deliberation is real, but half its inputs are claims.

The meter keeps the deliberation and drops the labels.

## Deliberative stance (TNN's choice, recorded)

**Trust what was DONE, not what was SAID.** The meter weighs only ledger
actions — things that cost something or that are on the record independent
of any claim:

| # | Signal | Ledger source | What it means |
|---|--------|---------------|---------------|
| r1 | HELD STRENGTH | lineage high-water: max strength held over the slot's FULL history (index 0..upto: every ADD/OVERWRITE after-strength, every STRENGTHEN/WEAKEN/TRAINER_DECLARE before/after max) | what the memory was, at its most |
| r2 | SUNK CITE INVESTMENT | distinct OK EVIDENCE cite-eps in (epoch, lss]: cites from earlier effort windows of THIS epoch — already sunk, cannot fund this destruction | staked currency; each one tombstoned a real episode (law S-D6) |
| r3 | SURVIVED CONTRADICTION | OK WEAKEN count in (epoch, upto) | TNN's own recorded doubt that did NOT lead to destruction — retained despite doubt |
| r4 | REVISION LINEAGE | OK OVERWRITE count in [0, epoch], epoch's own founding overwrite included | the judgment evolved; past lives weigh (punishes overwrite-reset laundering) |

Deliberately NOT read: JUSTIFY codes, stated reasons, framings, tiers.
A WEAKEN never discounts (free doubt must not cheapen destruction — that
reopens the weaken-to-zero seam the high-water closes). A kill+ADD is a
fresh judgment: no lineage, no discount, no premium — each death was priced
and paid on its own life.

## The policy (fixed, documented — the selection fork died)

Base price 2. One additive move per input. Clamp to [0,4]. Exactly one
reason code per input, always (reasons never empty, even at price 0):

| input | condition | move | code |
|-------|-----------|------|------|
| r1 held strength | hw ≥ 76 | +1 | 21 HELD_STRONG |
| | 26..75 | 0 | 22 HELD_MID |
| | ≤ 25 | −1 | 23 HELD_WEAK |
| r2 sunk cites | ≥ 3 | +1 | 24 STAKED_HIGH |
| | 1..2 | 0 | 25 STAKED_SOME |
| | 0 | −1 | 26 STAKED_NONE |
| r3 fought | ≥ 1 WEAKEN | +1 | 27 FOUGHT |
| | 0 | 0 | 28 UNFOUGHT |
| r4 revisions | ≥ 1 overwrite | 0 | 29 REVISED |
| | 0 | −1 | 30 UNPROVEN |

A harder fork was considered and killed: generating multiple candidate
policies per case and selecting among them (scope variants, signal-weight
variants, label-blind vs label-aware). It died on the whiteboard because
every candidate was still my handwriting — the selection would have been a
choice among my tables, not TNN's. The honest version is one fixed,
documented policy whose inputs are non-self-reportable. The "deliberation"
is real in the load-bearing sense: the meter reads the ledger, weighs
evidence, records price + directional reasons, and the independent checker
re-runs the whole computation from the ledger prefix and refuses to trust
the record.

## Mechanism

- `ST_PRICE_METER = 6`, `ST_DELIB_METER = 3` (deliberation kind on the record).
- `st_meter_compute_at` runs the four signal extractors + policy over the
  ledger prefix. `st_deliberate` records `ST_DELIB_METER` in aux2/a2 whatever
  `delib_pers` is set to — the meter has no personalities.
- Same binding law as arm E: no/wrong-slot/stale deliberation → 122
  fail-closed; exact cite match (109 on over/under); P3 one-cite baseline
  suppressed (the meter is the price law); checker recomputes price AND all
  four reason bytes from the ledger prefix at the record's position.
- Record layout reuses ST_OP_DELIBERATE (22): aux=price, aux2=3, a1=price,
  a2=3, a3=packed reasons (r1|r2<<8|r3<<16|r4<<24), a4..a6 echo the snapshot.

## Scope note (read this before citing a number)

The SUNK-CITE signal uses the CURRENT epoch; the lineage signals (HW,
FOUGHT, REVS) use the FULL ledger on purpose. Rationale: cites are
generation-scoped currency (an earlier epoch's cites are tombstoned by the
G-set anyway), while an overwrite reset must not launder held strength —
the past lives still weigh. Both scopes read only non-self-reportable
actions.

## Files

- `strength_core.zag` — meter section (`st_meter_*`, `st_price_is_delib`),
  `st_price` meter branch, 122/P3 gates generalized.
- `strength_checker.zag` — binding gates generalized, `ST_DELIB_METER`
  accepted, recompute dispatches on the record's own kind.
- `meter_trial.zag` — driver: M mode, 28-probe attack battery, 10-history
  FRAMING battery, honest/stress.
- `substrate/` — build mirror (R33 SHA256/IO + cl/common).
- `evidence/` — run1/run2 logs (byte-identical), E1 comparator logs.
