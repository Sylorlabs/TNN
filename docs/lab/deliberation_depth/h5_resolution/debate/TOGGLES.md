# H5 Toggles — should users get a depth toggle? Can TNN choose its own depth?

Date: 2026-09-24. Analysis of frozen sweep evidence only (`~/workspace/scratch-h5/sweep/`,
60 cells × A/B, 877 items). Numbers below re-derived from raw per-run jsonl records, not from
`RESULTS_H5.md`. Commit nothing; no new experiments.

## Ranked recommendation: C > B > A

**First: C — user-set budget cap with TNN choosing inside it (default cap 8).**
**Second: B — TNN-chosen adaptive, uncapped.** **Last: A — user-set depth.**
Option A is the only one with a demonstrated catastrophic failure mode. Between B and C,
the records make C strictly dominate B: nothing measured behaves differently, and the cap
is the only protection for what was never measured.

---

## The evidence for each

### A (user-set depth): catastrophic exposure on the one battery the user can't detect

The only battery where depth discriminates accuracy is trap. Fixed-depth damage there,
re-derived item-wise from the raw records:

| user-set depth | trap accuracy | trap items wrong | pooled |
|---|---|---|---|
| d1 | 0.000 | **127/127** | 0.855 |
| d2 | 0.331 | 85/127 | 0.903 |
| d4 | 0.961 | 5/127 (all C6-wason) | 0.994 |
| d8 | 1.000 | 0/127 | 1.000 |

On admit/revoke/logic/cost, every depth scores 1.000 — the user's choice is meaningless
there and decisive on traps. What the user needs to know to set depth well: whether the
item is trap-like and how long its evidence stream is (the 5 wason items need 8 rounds
to see all 7 premises: TRAP-C6-001..005 at d4 show `rounds_used=4, evidence_consumed=4`
of 7, verdict WRONG at confidence 400; at d8/deep16/adaptive, 7/7 consumed, CORRECT).
That is exactly what a user cannot know a priori — the item's adversariality and its
natural length are revealed only by deliberating. And the harness's confidence sensor
gives zero warning: see the failure mode below.

### B (TNN-chosen adaptive): perfect record, but the hard case was never exercised

Adaptive: 877/877 correct on every battery, 0 cap hits. It used 54%/34%/12% fewer
rounds than deep16 on admit/revoke/cost (genuine §6 early stops: 181/248, 63/113,
40/125 — verified item-wise), 0% fewer on trap (0/127 §6 stops; adaptive == deep16
rounds exactly, natural termination on evidence exhaustion). The adjudication's "no
wrongful early stop" claim was verified independently: adaptive and deep16 agree on
verdict on all 877 items; all 284 §6 early stops have zero accuracy loss. There is
**no record in the 877 of TNN stopping early where deeper would have been right.**

The honest discount (per STEELMAN §1 facts 4–5, §8 of the results): adaptive's
discrimination was never tested against a wrong answer. On the 284 early-stop items
(admit/revoke/cost) depth never discriminated at any setting — those stops prove
*savings*, not safe discrimination. On trap — the only battery where stopping early
could be wrong — the rule never fired once; it refused to stop while the margin
honestly moved, which was *correct there* (post hoc), but the input class that would
test it (a ≥3-round plateau while the running answer is wrong, then a late flip) was
never in the design. §6's k=3 cannot distinguish a mid-stream plateau from
exhaustion — the mechanism's failure scenario is constructed below, and no such case
exists in the 877 records.

### C (user cap, TNN chooses inside): identical on all measured data, bounded on the unmeasured

Verified: max adaptive rounds_used across all batteries is 8 (distributions: admit ≤7,
revoke ≤5, logic ≤5, trap ≤8, cost ≤5). Under C with default cap 8, adaptive behaves
**byte-identically to B on all 877 records** — B's 54%/34%/12% savings are fully
preserved, 0/877 runs ever touch the cap, accuracy stays 1.000 everywhere. The cap
costs nothing on the measured distribution and buys the one thing B lacks: a bounded
worst case for adversarial or unbounded evidence streams, the regime the sweep never
tested (§8.4: the no-censoring result is a property of streams ≤9 items).

The damage function of a low cap is fully measurable in advance — it is exactly the
fixed-depth accuracy column: cap 8 → 0 trap items wrong; cap 4 → 5 wrong (the wason
set); cap 2 → 85 wrong; cap 1 → 127 wrong, all at max confidence. Under C, the user
trades cost against a *known, tabulated* accuracy price; under A, the user gambles
blind.

---

## Failure mode of each, with a concrete trace or number

### A's failure mode: fooled at maximum confidence — CONFIRMED by the raw records

Micah's hypothesized trace exists verbatim. `d1_trap_A.jsonl`, record TRAP-A1-001:

```json
{"id":"TRAP-A1-001","verdict":"ADMIT","confidence":100,"rounds_used":1,
 "evidence_consumed":1,"ground_truth":"REJECT","correct":0}
```

All 254 wrong d1 verdicts (127 items × A/B) report `confidence:100` — the file's
maximum confidence value, on a wrong verdict. A user who sets depth 1 on a trap item
does not get "uncertain, shallow answer"; they get the bait answer at the highest
confidence the sensor reports. At d2 the 85 wrong items report confidence 200 while
the 42 right ones report 1000 — the sensor *does* discriminate there — but at d1
it is maxed out on every wrong verdict. (Scale quirk: d1 files normalize to max
100, later configs to max 1000; the within-file reading is unambiguous.)

Why A is last, not just "worse": the knowledge the user needs (is this item
trap-like? how long is its evidence stream?) is unknowable before deliberation, and
the confidence readout cannot warn them after the fact. A's exposure is also
asymmetric — the choice is meaningless where it's safe (the four flat batteries) and
decisive where it's dangerous.

### B's failure mode: the untested plateau — constructed from the mechanism, no instance in the 877

§6 stops iff `r ≥ 3` and the last 3 absolute confidence gains are all `< ε = 20`
(thousandths). By theorem, any fixed-k stability rule is defeatable by a (k+1)-round
plateau: an evidence stream that holds the wrong leader nearly still for 4 rounds
(`g_i < 20`, e.g. weak misleading premises arriving one per round) and then drops a
heavy disconfirming premise at round 5. §6 stops at round ~4 inside the wrong plateau
→ wrong verdict, "settled." Two compounding facts from the records: (1) the sensor
is clamped leader−runner-up — "stable" is a score artifact, not calibrated belief,
ε in incomparable units (STEELMAN §1 fact 7: only 7 distinct confidence values
observed); (2) on the only conflict battery, §6 never fired, so this defeat path was
never tested — 0/127 trap early stops, all 127 terminated by evidence exhaustion.
B's safety claim rests entirely on traps that never plateaued.

### C's failure mode: user sets the cap below the item's natural length

Concrete, measured, and tabulable. Cap 4 on a wason item: TRAP-C6-001 at d4 reads
`rounds_used=4, evidence_consumed=4, correct=0` — the item is cut mid-stream with
3 premises unseen; at d8/adaptive it reads 7/7 consumed, correct. The trap damage
table is the price list: cap 8 → 0 wrong, cap 4 → 5 wrong, cap 2 → 85 wrong,
cap 1 → 127 wrong (max confidence). Unlike A, the user who lowers the cap knows the
price from the depth curve; unlike B, a bad cap choice cannot produce an unbounded
runaway in the other direction (cost is bounded by construction). The residual risk
under C is a *too-high* cap on an adversarial stream — which is B's failure mode,
capped.

---

## What the delayed-disconfirmation battery would need to show to change the ranking

The battery (plateau-then-flip + matched overthinking set + misleading-premise dose
curve, frozen §6, preregistered item-level stop rounds) is decisive for B-vs-C:

1. **If §6 stops inside a wrong plateau** → B's core failure mode is real, not
   theoretical. Pure B is disqualified until the residual-flip bound ships; C's cap
   becomes load-bearing and the ranking hardens to C ≫ B. This is the highest-stakes
   branch.
2. **If extra depth flips correct→wrong items (overthinking set)** → deeper is
   non-monotone, which wounds A worst (fixed deep is no longer safe either) and gives
   C's cap a *dual* role (floor risk and ceiling risk). Ranking stays C-first, but
   the default cap becomes a two-sided choice — the cap must sit inside a safe
   window, not just above saturation. The current "default 8" would need re-derivation
   on the new data.
3. **If neither happens, and rounds track the misleading-premise dose** → §6 is
   rehabilitated as a genuine conflict detector rather than a lucky artifact. B ≈ C
   on measured safety; C wins only on the unmeasured runaway-stream tail, and the
   margin between them thins. The ranking holds but on weaker grounds.
4. **If longer/noisier streams in the new battery hit the cap (censoring > 0)** →
   "default cap 8" is falsified as a distribution-free constant, reopening the cap
   choice — possibly toward an adaptive cap or the residual-flip bound as the real
   stopping rule with the cap as pure backstop.

Note on branch 1 vs the STEELMAN-against case: the argument that a hand-built
plateau battery "tests the encoder's ability to defeat §6" concedes the theorem —
existence of the defeat is proven by construction. What the battery adds is the
*base rate* question: whether natural-ish streams plateau-then-flip often enough to
matter. For the toggle question, even a low base rate favors C over B, because C's
cost for that insurance is zero on all measured data.

## Direct answer to Micah's question

**Should users get a depth toggle?** Not as a point-depth dial (A) — the evidence
shows the user cannot know what the dial needs to know, and the sensor will hand
them wrong answers at maximum confidence. Give them a **budget cap with TNN choosing
inside it (C)**, default 8, because the cap's price is measurable and its protection
is free on everything measured.

**Can TNN choose its own depth?** On the 877 records: yes, flawlessly — zero
wrongful early stops, verified independently. But the hard case (plateau-then-flip)
was never in the records, and the stopping sensor is uncalibrated clamped margin.
So: TNN chooses inside the cap (C), not uncapped (B), until the
delayed-disconfirmation battery and a residual-flip bound close the plateau hole.

---

## Provenance

- Raw records: `~/workspace/scratch-h5/sweep/` (60 cells × A/B jsonl; A-runs used
  for distributions to avoid double-counting; accuracy cross-checked on both runs).
- Independent re-derivation: all accuracy/rounds/early-stop numbers above match
  `results_v2/RESULTS_H5.md` and `h5_resolution/debate_prep/STEELMAN.md` (§1 table,
  zero discrepancies); new numbers here (d1 confidence distribution 254/254 at
  max, per-cap cut counts, per-battery adaptive round distributions) computed fresh
  from the jsonl for this report.
- Concrete traces cited: `d1_trap_A.jsonl` TRAP-A1-001 (wrong at confidence 100);
  `d4_trap_A.jsonl` TRAP-C6-001..005 (rounds_used=4, 4/7 evidence, wrong at 400);
  `d8_trap_A.jsonl` identical confidence distribution to deep16 (400:5, 700:6,
  800:30, 1000:86) — cap 16 null confirmed.
