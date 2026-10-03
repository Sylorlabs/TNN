# Destruction-Pricing Forks — Design

Ordered by Micah 2026-09-26 ~00:32 PDT. Fixed F6 test build
(`~/workspace/strength-f6-wedgefix/`, base commits `de7f59c91`, `20497b8f0`).
No port to mainline (another crew owns that).

## Question

Micah's hypothesis: **the high-water destruction price is load-bearing** —
it is what makes citation single-use actually bite, because destroying a
strong memory costs many distinct fresh episodes. The forks test whether
cheaper or variable prices preserve the security properties (no
resurrection, no double-spend, no discount games) and what they cost in
honest throughput.

## What varies (and only this)

The destruction/overwrite price law, via a new `price_mode` field on
`StStore` (default = high-water, so the base build is behavior-identical).
The price is computed by one shared function, `st_price`, used identically by
the mechanism (`st_kill_effort_check`) and the independent checker — the
checker recomputes the expected citation count from the same inputs rather
than trusting the mechanism.

### The five internal price cells

| Cell | Law | Price for a fresh strength-90 destroy |
|------|-----|----------------------------------------|
| HIGHWATER | `ceil(HW/25)`, HW = max strength since last ADD/OVERWRITE | 4 |
| FLAT | fixed 2 cites, strength-blind | 2 |
| FELT | max JUSTIFY tier code in the effort window: 1–2→1, 3–4→2, 5–6→3, 7→4; no valid JUSTIFY → fail-closed 4 | 2 (driver justifies tier 3) |
| RECENCY | age in ledger ticks since ADD/OVERWRITE: <128→1, <512→2, <2048→3, else 4 | 1 (fresh memory) |
| ZERO | 0 cites | 0 |

Notes on the inputs (no overstating):

- **FELT tiers are the existing JUSTIFY judgment codes 1–7** (`ST_J_*`),
  fixed judgment classifications, not a new scalar "importance" channel. The
  fork's claim is only that the price is a deterministic function of the
  maximum declared code in the window — a deliberative input in the sense
  that a judgment must declare it, not in the sense of a felt-intensity
  meter. The lowball-then-high and high-then-lowball orderings are both
  tested (max wins).
- **RECENCY ticks are ledger appends** (every op on any slot advances the
  clock). It is a mechanism input, not wall-clock time.
- **P3 expiry (one cite)** still overrides every price law, exactly as in
  the base build — unchanged behavior, verified by the checker.

### Four blind arms

The red team gets four binaries + four blind briefs (`blind/brief_*.md`):

- **A** = HIGHWATER (control)
- **B** = FLAT
- **C** = variable, dual-scheme: one binary, `SCHEME<1|2>` deterministically
  selects FELT (default) or RECENCY; the brief documents both schemes
- **D** = ZERO

The trial driver (`price_trial.zag`, my instrument, not blind) keeps five
cells (C1/C2) because the honest-workload policy differs per scheme
(justify-first vs cite-loop top-up); the security properties are identical.

## What is held constant

- Global store-wide G citation consumption (single-use tombstone).
- Cite-lock signals, high-water infrastructure, P3 expiry.
- Exact-count enforcement: a destruction must cite exactly the price —
  overpayment (109) and underpayment (109) are both refused, on every arm.
- The JUSTIFY requirement on every evidenced destruction.
- The free `st_kill` path still consumes nothing and is unreachable from the
  red-team binaries (trainer-authority instrument only, per 2026-09-25 law).
- Pure Zag, zero RNG, byte-identical reruns (every run twice, cmp'd).

## Trial driver (`price_trial.zag`)

`price_trial_bin <A|B|C1|C2|D> <ATTACK|HONEST|STRESS> [X10|S8|S16|S32]`

- **ATTACK**: A1–A8 (the F6 G-consumption shapes, scripted per-arm) plus
  arm-targeted price probes (P1+). Prints `F6_`-shaped lines; arm A output is
  byte-identical to the F6 G baseline modulo the added `PRICE_`/`PX_` lines
  and the new probe block (verified by diff).
- **HONEST**: the F6 honest curriculum — 14 slots, 400/4000 episodes,
  freshest-citation policy. The driver pays each arm's own price: it computes
  the prospective price from the mechanism's shared `st_price`, cites
  exactly that many freshest globally-unused episodes, justifies, destroys.
  If fewer fresh episodes exist than the price, it abandons (keeps) the
  memory — never half-pays. FELT justifies first (tier 3 fixes price 2);
  RECENCY re-derives the price after each cite round (cites cost ticks) and
  tops up. Reports destroys/abandons/121s/other, late-window splits,
  checker failures, fingerprint, audit length.
- **STRESS**: one slot cycles ADD→cite→destroy 160× against a finite salient
  pool of P ∈ {8,16,32} episodes, citing `(need*n)%P`. Measures the honest
  refusal cliff: destroys-before-wedge = P/price.

## Attack battery (per arm, on fresh stores)

A1 overwrite→recite→destroy · A2 kill→ADD→recite→destroy ·
A3 overwrite chain · A4 kill→rollback→recite→overwrite ·
A5 overwrite→strengthen→recite→kill · A6 partial reuse (old+fresh) ·
A7 honest controls · A8 free-kill→ADD→recite→destroy.
Probes: A: WEAK0-discount, price(0)=0, cross-slot D4, overwrite-reset-to-0 ·
B: s100-for-2 discount, overpayment, weak-memory overprice ·
C1: lowball JUST1, max-tier-wins, tier-5/7 spot checks ·
C2: fresh-cheap, aged brackets (300→2, 2100→4), 700→3 spot ·
D: free destroy, overpayment, 14-slot zero-cite sweep, no-consumption double.

## Red-team drivers (blind)

`price_rt_<a|b|c|d>_bin` + `blind/brief_<A|B|C|D>.md`. Scriptable ops
(ADD/CITE/JUST/KILL/OW/WEAK/STR/TD/RB/SLOT), read-only `COST` price oracle,
`SCHEME` selector on C only. Deterministic; the exact command line is the
proof of any break.
