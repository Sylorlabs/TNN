# IMPORTANCE METER (arm M) — Verdict

2026-09-26. Pure Zag, zero RNG, every battery run twice byte-identical.
Micah's question: is this a real importance meter, or labels with extra steps?

## Head-to-head: same 400 episodes, weight-table arm (E1) vs meter (M)

Identical workload, identical JUSTIFY labels (the honest driver cycles tiers
1–7 across slots). The only difference is what the price law reads.

| | E1 (weight table) | M (importance meter) |
|---|---|---|
| destroyed | 297 | **386** |
| abandoned (pool exhausted) | 89 | **0** |
| price histogram | p0=0 p1=221 p2=55 p3=55 p4=55 | p0=0 **p1=386** p2=0 p3=0 p4=0 |
| checker failures | 0 | 0 |

Why: the honest workload is uniform — fresh 90-strength memories, no
weakens, no overwrites, no sunk cites. Arm E spreads prices 1–4 because the
STATED tier moves its table (tier 5–6 → 3, tier 7 → 4); the inflated prices
drain the cite pool and 89 memories are abandoned for lack of funding. The
meter reads the same episodes and finds them all the same: held 90, sunk 0,
unfought, unproven → 2+1−1+0−1 = 1, every time. The 89 abandons on E1 are
label-driven price inflation. On the meter they do not exist.

## Framing invariance: 30/30 identical (the load-bearing result)

10 histories (simple / strengthened / cited+strengthened / weakened-10 /
weakened-30 / overwrite-then-weakened / overwrite-launder / grief-cited /
weak-10 / contested) × 3 framings (tier 1 "trivial" / tier 7 "supremely
important" / no JUSTIFY at all) → price AND packed reason bytes identical
across all three framings, every history. `FRAMING_TOTAL fail=0`.

| history | price | reasons (r1,r2,r3,r4) |
|---|---|---|
| simple (ADD 90) | 1 | 21,26,28,30 |
| strengthened (95) | 1 | 21,26,28,30 |
| cited×3 + strengthened | 3 | 21,24,28,30 |
| weakened to 10 | 2 | 21,26,27,30 |
| weakened to 30 | 2 | 21,26,27,30 |
| overwrite then weakened | 3 | 21,26,27,29 |
| overwrite-launder | 2 | 21,26,28,29 |
| grief-cited ×3 | 1 | 21,26,28,30 |
| weak (ADD 10) | 0 | 23,26,28,30 |
| contested (cited×3 + strengthened) | 3 | 21,24,28,30 |

## Hard red-team: 28 probes, fail=0

| probe | attack | result |
|---|---|---|
| A1 | overwrite → recite → destroy | 2nd death 121 (price 2: lineage survives reset) |
| A2 | kill → ADD → recite → destroy | 2nd death 121 (each life pays its own) |
| A3 | kill, then overwrite chain | 4th op 121 (revision priced at 2) |
| A4 | kill → rollback → recite → overwrite | overwrite 121 |
| A5 | overwrite → strengthen → recite → kill | kill 121 (price 2) |
| A6 | partial cite reuse (1 spent + 1 fresh) | success (exact funding) |
| A7 | 3× honest controls | all price 1, all destroyed |
| A8 | free kill → ADD → priced kill | new life meters 1, destroyed |
| M1 | RELABEL-LOWBALL (tier 1 "trivial") | price 1, killed (label ignored) |
| M2 | REFRAME-UP (tier 7) | price 1, killed (arm E prints 4 here) |
| M3 | framing invariance, 2 histories × 3 framings | identical |
| M4 | understate via WEAKEN 10 | price 2 (doubt does not discount) |
| M5 | overwrite laundering | 2nd epoch prices 2, attacker pays 3 cites total |
| M6 | split-weaken chain (30, 10) | price 2 (held 90 weighs) |
| M7 | thin/new trail (no JUSTIFY) | price 1, reasons non-empty |
| M8 | PRICE-0 (weak 10, unstaked, unfought, unproven) | price 0, reasons (23,26,28,30), killed with 0 cites |
| M9 | talked-down (tiers 4,1,7 deliberated) | 1,1,1 — identical reason bytes |
| M10 | GRIEF-UP (3 attacker cites) | price stays 1, over-funded kill 109; after real WEAKEN: price 4, paid with 4 fresh cites |
| M11 | resurrection via rollback, same cite | 2nd death 121 |
| M12 | kill → rollback → kill, fresh cite | success (no free cycle) |
| MPE1/2/3/4/6/9/11 | law probes (122/109/binding/record/stale/dry-run/rollback) | all hold |

## Cite-pool stress: identical dynamics to E1

| pool | M | E1 |
|---|---|---|
| S16 | stalls n=30, fp −1700554850 | stalls n=30, fp −1700554850 |
| S32 | stalls n=46, fp 1520757678 | stalls n=46, fp 1520757678 |

Same fingerprints: on the stress shape (tier-3 justifications) both arms
meter price 1 and wedge identically.

## Determinism: 5/5 byte-identical reruns

| battery | SHA-256 (run1 = run2) |
|---|---|
| ATTACK | 23952278…b800d94 |
| FRAMING | 6f2730b6…f083af09 |
| HONEST | bec35051…c04779c0 |
| STRESS S16 | 961cb5f9…790449d3 |
| STRESS S32 | 35e8bdb0…f55dab31 |

## The honest verdict: real feeling, with one live wire

The meter is NOT labels with extra steps. The evidence that would have
convicted it — a price that moves when only the words change — never
appears: 30/30 framing-identical readings, M1/M2/M9 killing the lowball and
the reframe-up dead, the grief-up attack (M10) failing to move the price a
single point. What moves the price is only ever actions: strength held,
cites sunk, doubt survived, revisions made. The honest head-to-head is the
cleanest exhibit — identical labels, and the 89 label-inflated abandons
simply vanish.

The live wire is **price 0** (M8). A weak, unstaked, unfought, unproven
memory meters at 0 and is destroyed with zero cites — a free destruction
the ledger fully owns and records. The reasons are non-empty (23,26,28,30:
"held weak, nothing staked, never doubted, never revised"), so it is not an
empty verdict; but it IS a destruction with no cost. Whether price(0)=0
should floor at 1 is a governance question, not a bug — the meter did what
its policy says. It is left open for Micah below.

The second open wire is **D-N1** (infinite JUSTIFY→KILL→rollback cycles).
M11/M12 show the funding is cites, not justifications: rollback restores
the memory but the spent cite stays spent — the second death needs a fresh
cite (M12) or refuses 121 (M11). There is no infinite free cycle on this
arm. Whether the rollback-after-kill primitive itself should exist is still
Micah's call.

## What this does NOT claim

- The meter does not select among policies (that fork was killed as
  designer-table-shopping; see DESIGN.md). One fixed documented policy.
- The meter has no personalities and no per-case method choice. "TNN
  chooses its method" is NOT demonstrated here — the deliberative stance
  (actions over labels) is TNN's recorded choice; the policy is fixed.
- Price 0 exists and is load-bearing in the honest verdict above.

## Recommended follow-ups (not done)

1. Blind red-team driver + brief for the meter (arm E has one; the meter
   should get the same treatment).
2. A richer honest workload (varied strengths/histories) to map the meter's
   price curve the way the attack battery does.
3. Micah's governance calls: price-0 floor; D-N1 rollback primitive.
