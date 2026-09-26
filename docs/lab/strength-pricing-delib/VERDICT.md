# VERDICT.md — Arm E: DELIBERATIVE DESTRUCTION-PRICING

## 1. Plain-English verdict

**Deliberative pricing works.** The mechanism is sound, the checker holds,
and the price genuinely tracks the memory's history instead of being a
fixed number. On the honest workload it destroys more than every fixed arm
except the two cheapest (C2/D), with zero checker failures and
byte-identical reruns. The two personalities behave identically where they
should and diverge exactly where designed (after an overwrite reset).

The honest caveat: whether the *specific* weights (e.g. "3 prior cites
pushes the price up") are the *right* weights is a tuning question this
battery cannot answer. What it proves is the *mechanism*: deliberate →
record → bind → independently verify. That mechanism is solid.

## 2. Head-to-head (identical honest workload: 14 slots, 400 episodes)

| arm | destroyed | abandoned | 121s | other | ckfail | price behavior |
|-----|-----------|-----------|------|-------|--------|----------------|
| A (high-water) | 99 | 287 | 0 | 0 | 0 | 1–4 by strength |
| B (flat) | 199 | 187 | 0 | 0 | 0 | always 2 |
| C1 (felt) | 199 | 187 | 0 | 0 | 0 | 2 by tier policy |
| C2 (recency) | 386 | 0 | 0 | 0 | 0 | 1–4 by age |
| D (zero) | 386 | 0 | 0 | 0 | 0 | always 0 |
| **E1 (HISTORY-SEEING)** | **297** | **89** | 0 | 0 | 0 | **1–4 deliberated** |
| **E2 (EPOCH-FRESH)** | **297** | **89** | 0 | 0 | 0 | **1–4 deliberated** |

A–D rerun here from this binary's unchanged fixed-arm paths; every number
matches the sibling fork's committed honest-400 results exactly (workload
identity proven, not assumed).

E price distribution (386 deliberations): p0=0, p1=221, p2=55, p3=55,
p4=55. Prices 1–4 all occur; the price varies with the justification tier
the driver states (tiers 1–4 → 1, tier 5 → 2, tier 6 → 3, tier 7 → 4 on a
fresh 90-strength memory). Price 0 never occurs on this workload (it needs
a weak or fully-discounted memory); PE5 and the RT driver prove 0 prices
correctly.

## 3. Does deliberation add useful gain, or variance without gain?

**Useful gain, with a boundary.** The variance is not noise: the price is a
deterministic function of the memory's lived history (strength high-water,
prior cites, JUSTIFY trail, stated reason), recomputed identically by the
independent checker. On this workload E destroys 297 vs B/C1's 199 because
the common case (strong, uncontested, tier-3 justification, contradicted
reason) deliberates to price 1 — cheaper than B's flat 2 — while salient
or directive memories deliberate higher and are the ones abandoned (89).
That is *discriminative* pricing: cheap where the history is cheap,
expensive where it isn't. A fixed arm cannot do that; C2/D destroy more
only by being indiscriminately cheap.

The boundary: the honest workload contains no overwrites, so E1 and E2
are identical here (same fingerprint). The personality contrast lives in
the attack battery (PE5), where it is load-bearing: after
overwrite→deliberate, HISTORY-SEEING prices the pre-overwrite
90-strength life at **2**; EPOCH-FRESH prices the fresh post-overwrite
memory at **0**. Same ledger, same ops, different deliberated price — the
fork-within-the-fork is real and observable.

## 4. Attack battery (19 probes per personality, fail=0 both)

E A1–A8 (deliberation-aware shapes of the fixed-arm attacks): all pass.
Notably, the overwrite→recite→destroy shape is personality-aware by
design: E1 refuses 121 (the recited cites are spent and the price still
sees the old life); E2 succeeds at price 0 (the overwrite genuinely reset
the price — the overwrite itself was the priced step).

PE1–PE11 (deliberation-law probes): all pass.
- PE1: no deliberation → 122. PE2: wrong-slot deliberation → 122.
- PE3: cite count ≠ price → 109 (over- and under-cite).
- PE4: the record carries price 1 + all four reason codes (non-empty).
- PE5: the personality floor contrast (2 vs 0, reason r1 STRONG vs WEAK).
- PE6: strength-set after deliberation stales it → 122.
- PE7: double deliberation binds the most recent. PE8: tier-7 stated
  reason overrides to price 4 (reason DIRECTIVE recorded).
- PE9: read-only COST oracle agrees with the recorded price.
- PE10: deliberate-before-justify prices 2 (unstated reason → OTHER).
- PE11: rollback of a DELIBERATE record refused (108); the record stands.

## 5. Stress (160-cycle, pool=8, price=1)

8 destroys, then the 121 wedge — exactly pool/price, both personalities,
ckfail=0, byte-identical reruns. At cycle 22 the run stalls on slot
exhaustion (the 14 wedged memories stay live and occupy every user slot);
this is the workload shape's limit, not a mechanism failure, and is
reported explicitly rather than hidden.

## 6. Determinism

Every battery (ATTACK/HONEST/STRESS × E1/E2) executed twice; all six pairs
byte-identical (`cmp`). Zero RNG anywhere in the deliberation path.

## 7. Residuals / open questions

1. The weight table (§2 of DESIGN.md) is explicit and auditable but not
   derived from first principles — a different table would pass the same
   batteries. Tuning it is future work; the mechanism doesn't care.
2. The honest workload never overwrites, so the E1/E2 honest identity is a
   workload property, not a mechanism property. A curriculum with
   overwrites would separate them on throughput too.
3. E2's post-overwrite price-0 destruction is by design, but it means an
   attacker who can afford the overwrite price gets a cheap kill — the
   overwrite is the priced step, and that tradeoff is now explicit.
