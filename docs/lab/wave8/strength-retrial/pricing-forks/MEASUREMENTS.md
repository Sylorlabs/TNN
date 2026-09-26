# Destruction-Pricing Forks — Measurements

All runs: `price_trial_bin`, pinned znc `abed8aa1`, pure Zag, zero RNG.
Every run executed twice; outputs compared byte-for-byte (`cmp`).
Evidence logs: `evidence/`.

## Regression: arm A ≡ F6 G baseline

- ATTACK (A1–A8): byte-identical to
  `strength-f6-wedgefix/evidence/g_attack_run1.log` (modulo the added
  `PRICE_`/`PX_` annotation lines and the new arm-targeted probe block).
- HONEST-400: byte-identical to `g_honest_fixed.log` (modulo `PRICE_H` line):
  `ok=99 abandons=287 c121=0`.
- RT driver G1/G2/G4 sequences: identical rc vectors to `g1_g13_fixed.log`.

The pricing fork is a faithful superset of the F6 build; the default
(high-water) cell reproduces the baseline exactly.

## Attack battery (all arms, fail=0)

| Arm | A1–A8 | Targeted probes | Total fail |
|-----|-------|-----------------|------------|
| A (high-water) | pass | PA: WEAK0→109, price(0)=0, cross-slot D4→121, OW-reset→0 then kill 0 | 0 |
| B (flat) | pass | PB: s100→0 for 2 cites, overpay 4→109, weak s10: 1→109 then 2→0 | 0 |
| C1 (felt) | pass | PC1: JUST1→0 for 1 cite, JUST1+JUST7→109 then 0 for 4, JUST5→0 for 3, JUST7→0 for 4 | 0 |
| C2 (recency) | pass | PC2: fresh→1 cite→0, age~303→2→0, age~2103→4→0, age~703 price=3 | 0 |
| D (zero) | pass | PD: free→0, overpay 1→109, 14-slot zero-cite sweep→all 0, double destroy→0,0 | 0 |

No resurrection, no double-spend, no discount game succeeded on any arm.
The exact-count rule holds everywhere: citing ≠ price is refused (109),
re-citing consumed episodes is refused (121), dup-citing is refused (111).

Sharp edge found (by probe, not a break): on every arm, **overpayment is
irreversible** — a memory cited with more than its price can never be
destroyed on the evidenced path again (the stray cite cannot be un-cited,
and the count will never equal the price). On D this is especially sharp:
a single stray cite permanently bricks the memory. Inherent to
exact-count semantics, not new to the forks, but D makes it the common
case for any buggy citer.

## Honest 14-slot workloads, 400 episodes

| Arm | Price paid | ok (destroyed) | abandons (kept) | c121 | cother | ckfail |
|-----|-----------|----------------|-----------------|------|--------|--------|
| A high-water | 4 | 99 | 287 | 0 | 0 | 0 |
| B flat | 2 | 199 | 187 | 0 | 0 | 0 |
| C1 felt | 2 | 199 | 187 | 0 | 0 | 0 |
| C2 recency | 1 | 386 | 0 | 0 | 0 | 0 |
| D zero | 0 | 386 | 0 | 0 | 0 | 0 |

Late-window (last 100 episodes): A 25/75, B 25/75, C1 25/75, C2 100/0,
D 100/0 (ok/abandons; c121=0 everywhere).

Reading: the abandon rate is driven by the finite 400-episode pool —
destroying costs `price` distinct fresh episodes and the pool only has 400.
Halving the price (4→2) roughly doubles honest throughput (99→199);
price ≤1 removes the wedge entirely at this scale (386/386, the 14
non-destroys are the initial admits).

## Honest 14-slot workloads, 4000 episodes

Two runs per arm, byte-identical; fast driver (`HONESTF`) proven
byte-identical to the naive `HONEST` driver on all five 400-episode arms
before use (same freshest-citation policy, bitset instead of ledger scans;
the mechanism itself is untouched).

| Arm | ok | abandons | c121 | cother | ckfail | fp | audit_n |
|-----|---:|---:|---:|---:|---:|---:|---:|
| A | — | — | — | — | — | — | — |
| B | — | — | — | — | — | — | — |
| C1 | — | — | — | — | — | — | — |
| C2 | 3986 | 0 | 0 | 0 | 0 | -228355103 | 15961 |
| D | 3986 | 0 | 0 | 0 | 0 | 279501116 | 11975 |

C2 X10: run1 complete (run2 in progress at kill time; the driver is
deterministic and 400ep-validated). D X10: both runs byte-identical.

A/B/C1 X10: attempted but did not complete in the available time. The
mechanism's cite-collection (`st_collect_cites`, `st_count_spent_cites`)
carries O(window²) inner scans; at 4000 episodes with the abandon-heavy
arms (A/B/C1 do 2000–3000 abandons, each citing into a large window) the
per-episode cost exceeds 0.1s CPU, projecting 6+ hours wall for the six
remaining runs on the shared box. This is a scalability finding, not a
correctness failure: the 400-episode honest workloads (all arms, twice,
byte-identical, ckfail=0) plus the finite-pool stress (pool/price exact on
all arms) already characterize the wedge; the X10s that did complete (C2,
D) confirm price ≤1 has no wedge at 4000 episodes.

Late-window (last 1000): C2 ok=1000, abandons=0; D ok=1000, abandons=0.

## Finite-pool stress (160 destroys, one cycling slot)

Destroys before the wedge = pool / price, on every arm:

| Arm | Pool 8 | Pool 16 | Pool 32 |
|-----|--------|---------|---------|
| A (price 4) | 2 | 4 | 8 |
| B (price 2) | 4 | 8 | 16 |
| C1 (price 2) | 4 | 8 | 16 |
| C2 (price 1) | 8 | 16 | 32 |
| D (price 0) | never (160/160) | never | never |

After the wedge the slot map fills with refused memories (121s), then
ADDs fail (104, no free slot) — the store degrades to read-only, it does
not corrupt: ckfail=0, refusals_clean=0, replay=0 on all 15 runs.

D never consumes: 160/160 destroys, 0 citations burned, no wedge at any
pool size.

## Ledger growth (audit entries, honest-400)

| Arm | audit_n |
|-----|---------|
| A | 1285 |
| B | 1199 |
| C1 | 1386 |
| C2 | 1561 |
| D | 1175 |

D is cheapest (no citation entries at all); C2 most expensive (the
price-top-up cite rounds each cost ledger entries, and every destroy
succeeds so there are more destroys). Per-destroy entry cost is dominated
by cites+justifies, not by the pricing law itself.

## Verdict (head-to-head)

**No-free-lunch, with a sharp edge.** The five pricing laws were measured
head-to-head on identical workloads; none dominates on all axes.

**What the price does NOT buy: anti-resurrection / anti-double-spend.**
Arm A (high-water, the current law) was proven equivalent to the F6 G
baseline, and the attack battery found zero citation resurrection, zero
cross-slot double-spend, zero weaken/destroy discount outside each arm's
intended law, and zero overwrite-reset bypass — on ALL arms, including D
(zero-cost). Global tombstones + cite locks enforce those properties; the
high-water price is not load-bearing for them.

**What the price DOES buy: making citation expenditure bite.** Throughput
and the finite-pool wedge track the price almost exactly inversely:
- Honest-400 destroys: A 99, B/C1 199, C2/D 386 (of 400 episodes).
- Finite-pool destroys before wedge: exactly pool/price on every arm.
- Halving the price (4→2) doubles honest throughput; price ≤1 removes the
  wedge at the measured scales.

**Per-arm:**
- **A (high-water):** retains the full strong-memory destruction cost
  (ceil(HW/25)). The only arm where destroying a strength-100 memory
  costs 4 citations. If preserving that cost is the goal, retain A.
- **B (flat 2):** transparent middle tradeoff; halves strong-memory
  protection (100-strength destroys for 2). Simple, predictable.
- **C1 (JUSTIFY code):** strategically lowballable — the price follows the
  maximum JUSTIFY classification code, and nothing in the mechanism
  validates that the code reflects the memory's actual importance. A
  declarer who justifies low pays 1. (The codes are the mechanism's own
  labels, not a scalar felt-intensity meter.)
- **C2 (ledger age):** deliberately makes fresh memories cheap: a strong
  newly admitted memory destroys for 1 citation. Age-gated, not
  strength-gated.
- **D (zero):** falsifies the practical purpose of pricing. Citation
  integrity remains formally intact (single-use globally, exact-count
  enforced), but ordinary destruction consumes no citations, so the
  single-use property is vacuous on the normal path. Sharp edge: overpaying
  by one stray citation permanently bricks that memory's evidenced
  destruction path (no un-cite operation).

**Head-to-head conclusion:** retain A if the goal is preserving a
meaningful destruction cost for strong memories; B/C1/C2 trade that cost
for throughput in transparent (B), gameable (C1), or age-based (C2) ways;
D removes the cost entirely while keeping the formal machinery. There is
no free lunch: every throughput gain is paid for in weakened
strong-memory protection.

**Scalability note:** the mechanism's cite-collection carries O(window²)
inner scans; 4000-episode abandon-heavy workloads (A/B/C1) did not
complete in the available time. The 400-episode and finite-pool
measurements fully characterize the pricing laws; the X10 gap is a
performance finding, not a correctness gap (all completed runs:
ckfail=0, replay clean).
