# RED TEAM REPORT — Experiment 2: one-brain sub-agent dispatch

**Target:** provisional verdict "H1 KILLED by K1" (`~/workspace/onebrain/meas/MEASUREMENT.md`)
**Frozen prereg:** `docs/lab/onebrain/PREREG.md` @ `1ab40adceff78d71460b992b078508acea7e8abc`
— verified byte-identical (SHA-256 `71d5d8b1…5fff`) to the copy the crews used.
**Method:** independent re-derivation from `meas/*_r1.txt` + `v4.tsv`; full-trace
audit of all 28 problems (`./onebrain_ro onebrain v4.tsv`, copy of the frozen
binary — `impl/` never modified); source read of the audit operations in
`onebrain.zag` (read-only).

**Bottom line: UPHOLD KILL — but the kill is fragile, and the report must say so.**
Every attack below was attempted in earnest. Two landed cleanly (a wrong
number in MEASUREMENT.md; substantial dead weight in the set), and one
landed with a caveat that matters more than either: the KILL turns on a
single unprincipled tie-break in one audit rule — a minimal, principled,
fully general variant (V4, §C) flips exactly one verdict (p08) and un-fires
K1's both conjuncts. The verdict is valid per the frozen prereg on the actual
evidence; it is not robust. It kills this implementation, not the fan-out
concept.

---

## A. Scoring errors — REJECTED (no mis-score; K1 math confirmed)

Independently re-derived from `meas/{single,onebrain,ablate,min,poison}_r1.txt`
vs `expected_bid` in `v4.tsv`. Result: **every per-item verdict matches the
coordinator's table exactly** (28/28 × 5 modes), including all `-1` NO_VERDICTs
and all fork flags.

| mode | correct | accuracy |
|---|---|---|
| single | 14/28 | 50.0% |
| onebrain | 14/28 | 50.0% |
| ablate | 14/28 | 50.0% |
| min | 14/28 | 50.0% |
| poison | 8/28 | 28.6% |

K1's conjuncts, re-verified:
- onebrain (50.0%) ≤ single (50.0%) ✓
- ablate accuracy (50.0%) == onebrain (50.0%); verdicts identical 25/28,
  differing only on p02 (−1/13), p05 (16/13), p11 (−1/16) ✓
- onebrain fixed **0** of the 14 single-wrong items ✓ (list:
  p02,p04,p05,p07,p08,p11,p12,p13,p14,p18,p23,p24,p25,p28)

Determinism SHAs also re-verified and match MEASUREMENT.md byte-for-byte
(single `a9b9999345c8`, onebrain `b5c20e213b0d`, ablate `1a3797e96774`,
min `1b26c18caa27`, poison `d4b4ea91d60f`; 3/3 reruns identical per mode).
K3 (`min` ≡ `onebrain` on all 28 full VERDICT lines incl. fork flags) confirmed.

## B. Set fairness — CONFIRMED (dead weight is real and quantified)

The set is **not** adversarially tuned against H1 (see G — the builder never
ran onebrain during construction, and the impotence below flows from the
implementer's GEN semantics, not from set selection). But it is padded with
items that cannot discriminate fan-out designs:

| class | n | items |
|---|---|---|
| fork=0 ⇒ onebrain ≡ single **by construction** (subpasses skipped; verified all 10 have identical winners across modes) | 10 | p01,p06,p09,p19,p20,p21,p22,p23,p24,p25 |
| fork=1, single-correct (can only lose, never gain) | 7 | p03,p10,p15,p16,p17,p26,p27 |
| fork=1, single-wrong (**the only K1-informative items**) | 11 | p02,p04,p05,p07,p08,p11,p12,p13,p14,p18,p28 |

Further, inside the dead weight:
- **p23–p25: withhold(23) is structurally unfirable.** `act_gate_rd`: 23 fires
  iff no gated fact exists; the default bid (24) always fires on `plain(9)`
  with a keyword-surfaced fact, so a gated fact always exists. Expected bid 23
  is unreachable by *any* variant of this machinery (all five modes: 24).
- **p19–p22 violate the prereg's own set spec** ("queries with ≥2 plausible
  readings"): p19 has 1 reading (provenance), p20–p22 have 1 (plain).
  Removing them changes nothing (single 10/24 = onebrain 10/24), so this is
  noted, not void-grade.

**Discriminating subset for K1 = 11 items.** That is thin — but the prereg
sets no minimum informative-item count, and the direction on those 11 is
unambiguous (0 fixed, 2 destroyed to −1, 1 moved laterally, 8 unchanged).
The attack establishes *weak test power*, not *invalid test*.

## C. NO_VERDICT collapses — "friendly fire" CONFIRMED accurate; kill is FRAGILE to one tie-break (CONFIRMED)

Traces confirm MEASUREMENT.md's story and deepen it:
- **p02:** `AUDIT_DENY fact=10 by=6` (the forget reading denied the joke fact)
  → `AUDIT_CLEAN` killed bids 13, 15, 22 → ARGMAX → −1. Worse than reported:
  the forget bid (15, the expected winner) **depends on the same fact 10 its
  own reading denies** — a self-defeating structure, not just cross-branch
  friendly fire. Any ledger state with 15's gating reading alive implies
  fact 10 denied implies 15 dead. Contradiction ⇒ unreachable.
- **p11:** `AUDIT_DENY fact=11 by=0` (correction denied the least-relevant fact)
  → all three bids (16, 18, 22 — **all share fact 11**) died → −1. Genuine
  shared-state causality, purely destructive.

The collapses are **genuine deliberation dynamics, not bugs**: deny →
cleanup → ARGMAX is the specified causal channel working as designed.

**Reachability on the actual machinery:** the fork's audit vocabulary is
{reading duels, fact denials (by=6 / by=0), bid cleanup, rescore}. For each of
the 14 single-wrong items the expected bid is **unreachable** (corr values
exact — all relevant bonuses < 3, so `bonus = corr` uncapped; duel needs
`corr(q) ≥ corr(q2)+2`):

| item | exp | why unreachable on actuals |
|---|---|---|
| p02 | 15 | self-deny (above); duel needs corr≥2, max available 1 |
| p04 | 22 | 22 shares gating reading 4 with bid 13 — any duel killing 13 kills 22 |
| p05 | 22 | 22 shares gating reading 0 with bid 16 (base 231 > 213 always beats it) |
| p07 | 15 | killing 14 needs corr≥3; max alive corr is 1 |
| p08 | 14 | duel needs corr≥2 (max 1); DENY by=0 blocked by inter tie (1 vs 1, rule needs strict `<`) |
| p11 | 18 | 18 shares fact 11 with 16; duel gaps insufficient |
| p12 | 18 | kill reading 0 needs corr≥4, max 2 |
| p13 | 18 | kill reading 1 needs corr≥3, max 1; no deny available |
| p14 | 17 | 17 shares fact 10 with 16; duel gaps insufficient |
| p18 | 20 | duel needs corr≥4 (max 0); the machinery's duel **actively killed the correct reading** (kill=3 by=2, corr 2 vs 0) |
| p23–25 | 23 | withhold unfirable (see B) |
| p28 | 22 | kill reading 8 needs corr≥2; both alive corrs are 0 |

Structural facts amplifying this: on **20/28** problems every fired bid shares
the single supporting fact hid=10 (5/28 share fact 11; only p05/p08 split
10/11; p28 has fact=−1) — so fact-denial can almost never discriminate between
bids, only annihilate them. The duel channel (the only discriminating audit)
fired on **2/28** problems: p11 (after all bids were already dead) and p18
(killed the *correct* reading).

**Fragility (the attack that lands):** the kill turns on a single
unprincipled choice — DENY by=0's strict `imin<imax` fire condition plus
first-minimal tie-break. Consider **V4**, a minimal (~3-line), principled,
fully general variant: *correction denies the least-relevant alive fact;
relevance ties broken by fewest dependent bids* (least-disruptive
invalidation — no problem-specific logic, applies uniformly). Hand-simulated
all 4 subpasses on every affected problem (candidate set: p05, p08, p11, p12,
p14 — the only fork=1 items with reading 0 alive and ≥2 gated facts):
- p08: tie {fact 10 (3 dependent bids), fact 11 (1 bid)} → kill 11 → bid 13
  dies → 14 wins (238 vs 232/214) ✓ **FIXED** (bonuses/duels re-verified
  stable post-kill: corr values flow through surviving fact 10)
- p05 → 16, p11 → −1, p12 → 16, p14 → 13: all **unchanged** (the second
  subpass re-kills fact 11 on p05/p11; p12/p14's killed facts support no bids)

V4 changes **exactly one verdict** (p08 → 14): onebrain 15/28 > single 14/28,
ablate unchanged at 14/28 (its writes are discarded) — **both K1 conjuncts
un-fire**. V4 is hand-simulated only (constraints forbid building/running
variants against the official set), so this is a flagged hypothesis, not a
refutation — but it proves the KILL is fragile: it rests on an arbitrary
tie-break in one audit rule, on one problem. The verdict kills *this
implementation*; it does not establish that shared-ledger fan-out cannot
help. Attack on the kill's validity: REJECTED. Attack on the kill's
robustness: CONFIRMED.

## D. K2 quality — pass verdict stands; report's "17/18" is wrong (15/18)

Prereg K2: *"Poison test: invalidate a fact candidate in the shared ledger
mid-deliberation; other branches' bids/eliminations do not change → KILL."*
Re-derived: poison changed the verdict on **15/18** fork items (14 → −1,
p08 13→14), **not 17/18** as MEASUREMENT.md claims. The 3 unchanged are
p02, p11 (−1→−1: nothing left alive to kill — the fork had already
annihilated all bids) and p28 (18→18: all bids have fact=−1, poison hook
finds no valid target). Non-fork items: 10/10 unaffected ✓.

K2 still **passes as written** — 15/18 with changed bids/eliminations is
decisive against "do not change". On the stricter intent-reading ("causal
cross-talk *between branches*"): the poison hook is external, but the
prereg's own causal protocol #1 explicitly operationalizes K2 as the external
flip ("every branch that read it updates its bids/eliminations in the same
deliberation" — observed), and genuine branch-written cross-talk exists too
(the 3 onebrain-vs-ablate differences, all via branch-subpass audits).
Honest qualifier, already in MEASUREMENT.md: the demonstrated cross-talk is
**causal but purely destructive** — it annihilates or reshuffles, never
constructs. That qualifier is exactly why K1 kills; it does not un-pass K2.

Minor gap: the prereg's protocol-#1 control (N independent ledgers) was not
run as such (poison exists only in onebrain mode); ablate is the nearest
proxy. Not bar-material.

## E. K4 weakness — pass stands as written; weakness CONFIRMED

Prereg K4: *"Delete/reorder a shared ledger entry: fan-out behaves identically
to N independent sequential runs → KILL."* Onebrain vs ablate differ on 3/28
(p02 13→−1, p05 13→16, p11 16→−1) — not identical, so the bar **passes as
written**. Both sides, as tasked:

- **Pass (textualist):** the bar tests liveness, not benefit — "behaves
  identically" is false, the shared writes are causally live (each difference
  traces to a branch-subpass audit → cleanup → ARGMAX chain), and the
  implementer's independent neuter test (smoke2: onebrain→compose/227 vs
  ablate→joke/242) corroborates. "Not decorative" is satisfied.
- **Fail (substantive):** all 3 differences are wrong→wrong / wrong→−1; the
  sharing's entire behavioral footprint on 28 problems never converts a loss
  to a win. Read as "does work that could matter for H1", it fails — but that
  reading collapses K4 into K1, which the prereg deliberately separates
  (K1 = benefit, K4 = liveness). Under the frozen text, K4 passes;
  MEASUREMENT.md's "(weakly)" is the honest accounting.

Attack on K4's pass/fail: REJECTED. Operationalization note: ablate (2
branches, scratch copies, still interleaved) is a proxy for, not literally,
"N independent sequential runs" — immaterial to the verdict.

## F. Alternative verdicts — REJECTED (no VOID-grade flaw; no OVERTURN)

- **OVERTURN (H1 supported):** indefensible — K1's conjuncts hold as
  independently verified (A).
- **VOID:** requires a prereg-terms violation invalidating the test. Examined:
  (i) blindness — clean (G); (ii) "≥2 plausible readings" — 4 items off-spec
  but K1-neutral on removal; (iii) baseline operationalization (`single` mode
  vs the v1 binary — apples-to-apples for the fork's marginal effect, which is
  what K1 tests); (iv) set unwinnability — flows from the machinery's own GEN
  design (shared gating readings, single shared fact), fixed before the set
  was built; the prereg requires only "hard ambiguous turns where single
  struggles" (50% single accuracy ✓), not winnability-by-fan-out. None
  void-grade.
- **Narrower kill:** unavailable — K1's "KILL the mechanism" already kills
  *this* mechanism, not the one-brain concept. The concept survives; this
  implementation doesn't.

## G. Builder blindness — REJECTED (no violation; timeline clean)

- `impl/` mode runs (onebrain/ablate/poison/min): 06:19:40 UTC, on the
  implementer's **smoke set** (numeric ids) — predating `v4.tsv`'s existence.
- `v4.tsv` created 06:26:05 UTC, SHA-256 `e74bfa51…0b2023` ✓ matches FREEZE.txt.
- FREEZE.txt written 06:26:09 (freeze stamp 06:26:07, from `date -u` before
  any scoring); builder's single-mode calibration 06:26:10 — freeze preceded
  all scoring on v4.1 ✓.
- `v4/` contains **only** single-mode output; coordinator's 5-mode scoring runs
  06:26:38–39 UTC, after the freeze ✓.
- The "predicted 50%" in FREEZE.txt is hand-analysis from single-mode
  semantics (verified against source: trigger tables, bases, bonus cap,
  tie-breaks) — no fork outcomes were observed or needed for it.

## Independent score table

Matches the coordinator's exactly (see A). Per-item (exp | sing | ob | abl |
min | poi): p01 13|13|13|13|13|13 · p02 15|13|−1|13|−1|−1 ·
p03 13|13|13|13|13|−1 · p04 22|13|13|13|13|−1 · p05 22|13|16|13|16|−1 ·
p06 14|14|14|14|14|14 · p07 15|14|14|14|14|−1 · p08 14|13|13|13|13|14 ·
p09 16|16|16|16|16|16 · p10 16|16|16|16|16|−1 · p11 18|16|−1|16|−1|−1 ·
p12 18|16|16|16|16|−1 · p13 18|17|17|17|17|−1 · p14 17|13|13|13|13|−1 ·
p15 18|18|18|18|18|−1 · p16 19|19|19|19|19|−1 · p17 19|19|19|19|19|−1 ·
p18 20|19|19|19|19|−1 · p19 20|20|20|20|20|20 · p20 24|24|24|24|24|24 ·
p21 24|24|24|24|24|24 · p22 24|24|24|24|24|24 · p23 23|24|24|24|24|24 ·
p24 23|24|24|24|24|24 · p25 23|24|24|24|24|24 · p26 21|21|21|21|21|−1 ·
p27 21|21|21|21|21|−1 · p28 22|18|18|18|18|18.

## Recommendation

**UPHOLD KILL — H1 is KILLED by K1**, per the frozen prereg's kill-bars table:
*"K1 — No parallelism benefit — One-brain accuracy ≤ single-deliberation
accuracy on the frozen hard set, AND the shared-writes-off ablation matches
one-brain → KILL the mechanism"* (both conjuncts independently verified: A),
with the K1 note's conjunctive reading satisfied. No prereg clause was
violated in a way that would support VOID (F, G); no evidence supports
OVERTURN.

**Mandatory flag (do not close the line on this verdict alone):** the kill is
fragile. It depends on DENY-by=0's strict `imin<imax` fire condition +
first-minimal tie-break — an unprincipled choice. The principled,
least-disruptive-invalidation variant V4 (§C: break relevance ties by fewest
dependent bids) is a ~3-line, fully general, non-bridge change that flips
exactly one verdict (p08 → 14) and un-fires K1 (onebrain 15/28 > single 14/28,
ablate 14/28). V4 is hand-simulated, not run (building/running variants
against the official set is out of red-team scope) — so this is a hypothesis
requiring a real test, not an overturn. But it means the evidence establishes
"this implementation's fan-out vocabulary (duels + fact-denials over a single
shared fact with entangled gating) cannot construct correct verdicts here" —
not "shared-ledger fan-out cannot help". Recommend: record the KILL against
this implementation, then re-test with V4-class (least-disruptive
invalidation) variants before treating the one-brain line as closed.

Corrigenda for the coordinator (non-verdict-changing):
1. MEASUREMENT.md "changed the verdict on 17/18 fork items" → **15/18**
   (14 → −1, p08 13→14; p02/p11 already −1, p28 unpoisonable).
2. The set's K1-informative subset is 11 items, not 28 (10 mechanically
   inert, 7 single-correct). Future fan-out tests should pre-register a
   minimum informative-item count and a winnability check (≥1 single-wrong
   item whose expected bid is reachable by the machinery's own operations) —
   here that check yields **0/14 on actuals**, which is itself the
   mechanism-level finding.
