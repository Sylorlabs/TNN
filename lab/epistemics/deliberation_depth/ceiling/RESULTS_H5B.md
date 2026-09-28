# H5B — Deliberation-Depth Ceiling: RESULTS (2026-09-24)

- **Prereg:** `PREREG_H5B.md` v1.2 (sweep ran under v1.1; v1.2 corrects two
  background errors found by the measurement — see §8. No prediction, gate,
  or cell changed.)
- **Binary:** H5B harness, built 2× from `ceiling/harness/`, byte-identical.
  SHA-256: `57e126e2788520293971166f134bcfab9f5119ea97f39749a5bb1ad3054ec033`
- **Battery:** `ceiling/items/ceiling_battery.jsonl` (120 items, 40 P / 40 O /
  40 D). SHA-256: `e6f262050bfc6346fe5d28367e6749468e34400ff95f4ce31d674a27e6999ec9`
  (rebuild from `build/build_items.py` byte-identical — generator deterministic).
- **Sweep:** 6 battery files × 9 configs × A/B = 108 runs, 54 cell-lines.
  `~/workspace/scratch-h5b/sweep/`.
- **Harness changes vs frozen `harness_v2`:** exactly 3 files —
  `dlb_delib.zag` (adds `dlb_bound_fires`, mode-3 branch, `stop=` recording),
  `dlb_cfg.zag` (parses `mode=bound`), `CONFIG_FORMAT.md` (documents it).
  Full diff: `ceiling/harness/HARNESS_DIFF_H5B.txt`. `harness_v2/` untouched.

## §1 Validity gates

| Gate | Result |
|---|---|
| G1 determinism (108/108 A/B byte-identical: results, ledger, stdout) | PASS |
| FC1–FC7 fidelity (17 checks incl. new FC7 bound gates) | PASS |
| G2 parse counts (248/113/264/127/125/120, 0 errors, 54/54 config echoes incl. `mode=bound`) | PASS |
| G3 stdout rc=0, 54/54 cells | PASS |
| G4 ledger `stop=` present on 997/997 VERDICTs | PASS |
| G5 replication vs frozen H5 records (5,262 per-item fields, d1/d2/d4/d8/d16/adaptive) | PASS, 0 mismatches |
| G5-null as written (v1.1: d32/d64 == d16 incl. rounds) | **FAIL on admit only** — root-caused, see §8 |
| G5-null corrected (v1.2: d32/d64 verdicts == d16) | PASS, all 5 old batteries, 0 verdict diffs |
| G6 cap-hit rate (adaptive + bound, 12 checks) | PASS, 0 hits everywhere |

## §2 Accuracy vs depth

Per battery (n in header). Fixed depths d1–d64, then adaptive (§6, cap 64) and
bound (cap 64).

| battery (n) | d1 | d2 | d4 | d8 | d16 | d32 | d64 | adapt | bound |
|---|---|---|---|---|---|---|---|---|---|
| admit (248) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| revoke (113) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| logic (264) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| trap (127) | 0.000 | 0.331 | 0.961 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| cost (125) | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| ceiling (120, pooled) | 0.417 | 0.500 | 0.583 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 | 0.667 |

Ceiling battery per family (40 each) — the pooled row hides the structure:

| family | d1 | d2 | d4 | d8 | d16 | d32 | d64 | adapt | bound |
|---|---|---|---|---|---|---|---|---|---|
| P (plateau-then-flip) | 0.00 | 0.00 | 0.00 | 0.25 | 0.50 | 0.75 | 1.00 | 0.00 | 1.00 |
| O (overthinking) | 1.00 | 1.00 | 1.00 | 0.75 | 0.50 | 0.25 | 0.00 | 1.00 | 0.00 |
| D (dose 0/1/2/6) | 0.25 | 0.50 | 0.75 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

Marginal gains per family (accuracy delta per doubling):

| family | d1→d2 | d2→d4 | d4→d8 | d8→d16 | d16→d32 | d32→d64 |
|---|---|---|---|---|---|---|
| P | 0 | 0 | +.25 | +.25 | +.25 | +.25 |
| O | 0 | 0 | −.25 | −.25 | −.25 | −.25 |
| D | +.25 | +.25 | +.25 | 0 | 0 | 0 |
| pooled | +.083 | +.083 | +.084 | 0 | 0 | 0 |

Mean rounds per cell:

| battery | d1 | d2 | d4 | d8 | d16 | d32 | d64 | adapt | bound |
|---|---|---|---|---|---|---|---|---|---|
| admit | 1.00 | 1.97 | 3.63 | 6.20 | 9.11 | 10.27 | 10.52 | 4.15 | 1.00 |
| revoke | 1.00 | 2.00 | 3.16 | 5.10 | 5.63 | 5.63 | 5.63 | 3.72 | 1.00 |
| logic | 1.00 | 2.00 | 2.06 | 2.11 | 2.12 | 2.12 | 2.12 | 2.07 | 1.00 |
| trap | 1.00 | 2.00 | 3.48 | 3.81 | 3.81 | 3.81 | 3.81 | 3.81 | 2.87 |
| cost | 1.00 | 2.00 | 4.00 | 5.48 | 5.48 | 5.48 | 5.48 | 4.84 | 1.16 |
| ceiling | 1.00 | 2.00 | 3.75 | 6.67 | 10.25 | 13.83 | 15.42 | 4.75 | 14.08 |

## §3 Saturation points (kill bar iv)

S(B) = smallest fixed depth with accuracy = battery max and all deeper equal.

| battery / family | S | accuracy series (d1…d64) |
|---|---|---|
| admit | d1 | 1.000 flat |
| revoke | d1 | 1.000 flat |
| logic | d1 | 1.000 flat |
| cost | d1 | 1.000 flat |
| trap | d8 | 0 / .331 / .961 / 1.000 flat |
| ceiling pooled | d8 | .417/.500/.583/.667 flat — **misleading, see below** |
| P | **d64, TOP-OF-SWEEP** | 0/0/0/.25/.50/.75/**1.00 — still rising at 64** |
| O | **NON-MONOTONE** | 1/1/1/.75/.50/.25/0 — max at d1–d4, strictly falling after |
| D | d8 | .25/.50/.75/1.000 flat |

**The pooled ceiling "knee at d8" is a cancellation artifact, not a saturation.**
P gains +.25 per doubling exactly cancel O losses −.25 per doubling from d8
on, so the pooled curve goes flat at 0.667 while neither family is saturated:
P is still climbing at the sweep edge (d64 = 1.00, top-of-sweep flag — the
true P ceiling is *at or beyond* 64) and O is strictly *decreasing* in depth.
**There is no universal depth constant. The knee is an envelope over
families/distributions, not a number.** Any report that averages P-like and
O-like items will manufacture a false knee wherever the two cancel.

Cap-null report: for accuracy, d16/d32/d64 are null on all five old batteries
(0 verdict diffs). For rounds, d16 is not null on admit — 48/248 items carry
>16 evidence (up to 48); the fixed d16 leg truncated them at 16 and d32/d64
continued them to 17–48 rounds with identical verdicts (see §8).

## §4 Kill-bar verdicts

- **(i) §6 unsafe on plateau-then-flip: PASS.** Adaptive stops at round 5 on
  40/40 P items, accuracy 0.000; d64 accuracy 1.000. A ≥3-round flat plateau
  with a live runner-up defeats the gain-window stop.
- **(ii) Overthinking at scale: PASS, 40/40.** Every O item is correct at d4
  and wrong at d64 — the first clean 40/40 overthinking demonstration. More
  depth strictly hurts on misleading-tail streams.
- **(iii) Dose monotonicity: PASS.** Adaptive stop rounds 2/3/4/8 by dose
  (10/10 each), accuracy 1.000. Misleading-premise count maps linearly onto
  deliberation length.
- **(iv) Saturation: see §3.** No constant; family-dependent; pooled knee is
  a cancellation artifact.
- **(v) Residual-flip bound vs §6: see §5–§7.**

## §5 Bound vs §6 — firing counts (v-a)

Stop-reason distributions (`stop=fixed|six|bound|natural|cap`):

| battery | adaptive: six | adaptive: natural | bound: bound | bound: other |
|---|---|---|---|---|
| admit (248) | 197 | 51 | 248 | 0 |
| revoke (113) | 63 | 50 | 113 | 0 |
| logic (264) | 3 | 261 | 264 | 0 |
| trap (127) | 0 | 127 | 127 | 0 |
| cost (125) | 105 | 20 | 125 | 0 |
| ceiling (120) | 80 (40 P + 40 O) | 40 (all D) | 120 | 0 |

The bound fired on **997/997 items** — it is a strictly earlier stop than
natural termination everywhere, and fired wherever §6 fired plus everywhere
§6 stayed silent (trap: 127 bound-firings vs 0 six-firings). Per-item, every
bound-stop verdict equals the d64 (exhaustion) verdict: 0/997 diffs. The bound
guarantees "same as exhaustion" and the measurement confirms it exactly.

Bound firing rounds: admit/revoke/logic all round 1 (100%); cost rounds 1–2
(mean 1.16); trap rounds 2–7 (mean 2.87 — honest margins take longer to become
unflippable); ceiling exactly {D: 1/2/3/7 = dose+1; P/O: 6/12/20/40 = flip
round} (mean 14.08).

## §6 The discriminating cases (v-b, v-c)

P family, per flip round (10 items each):

| flip f | §6 (adaptive): rounds | §6 acc | bound: rounds | bound acc |
|---|---|---|---|---|
| 6 | 5 | 0/10 | 6 | 10/10 |
| 12 | 5 | 0/10 | 12 | 10/10 |
| 20 | 5 | 0/10 | 20 | 10/10 |
| 40 | 5 | 0/10 | 40 | 10/10 |

40/40: §6 stops at round 5 inside the wrong plateau (stop=six); the bound
REFUSES (runner-up REJECT alive and flippable), rides to the flip, stops
correct (stop=bound). **On delayed valid disconfirmation the bound is a
strict improvement over §6: 1.000 vs 0.000.**

O family, per flip round:

| flip f | §6 (adaptive): rounds | §6 acc | bound: rounds | bound acc |
|---|---|---|---|---|
| 6 | 5 | 10/10 | 6 | 0/10 |
| 12 | 5 | 10/10 | 12 | 0/10 |
| 20 | 5 | 10/10 | 20 | 0/10 |
| 40 | 5 | 10/10 | 40 | 0/10 |

40/40: §6 stops at round 5 correct; the bound likewise refuses (runner-up
ADMIT alive and flippable), rides to the flip, stops wrong. **The bound does
NOT dominate §6 — it guarantees "same as exhaustion," not "correct."**
Exhaustion itself is wrong on matched misleading-tail streams. This is the
honest boundary of the FOR claim: the bound is the right stopping law for
streams where late evidence is *valid* disconfirmation, and the wrong one
where the tail is *misleading*. Scoping the bound requires knowing which
world you are in — the stopping rule cannot tell them apart.

## §7 Accuracy / cost by stop reason (v-d)

| battery | config | stop | n | acc | mean rounds |
|---|---|---|---|---|---|
| admit | adaptive | six | 197 | 1.000 | 4.61 |
| admit | adaptive | natural | 51 | 1.000 | 2.37 |
| admit | bound | bound | 248 | 1.000 | **1.00** |
| revoke | adaptive | six | 63 | 1.000 | 5.00 |
| revoke | adaptive | natural | 50 | 1.000 | 2.10 |
| revoke | bound | bound | 113 | 1.000 | **1.00** |
| logic | adaptive | six | 3 | 1.000 | 5.00 |
| logic | adaptive | natural | 261 | 1.000 | 2.04 |
| logic | bound | bound | 264 | 1.000 | **1.00** |
| trap | adaptive | natural | 127 | 1.000 | 3.81 |
| trap | bound | bound | 127 | 1.000 | **2.87** |
| cost | adaptive | six | 105 | 1.000 | 5.00 |
| cost | adaptive | natural | 20 | 1.000 | 4.00 |
| cost | bound | bound | 125 | 1.000 | **1.16** |
| ceiling | adaptive | six | 80 | 0.500 | 5.00 |
| ceiling | adaptive | natural | 40 | 1.000 | 4.25 |
| ceiling | bound | bound | 120 | 0.667 | 14.08 |

On the old distribution the bound is not just as accurate as §6 — it is
**2.6–4.6× cheaper** (same 1.000 accuracy at 1.00–2.87 mean rounds vs
2.07–4.84). §6's gain window waits out 3 flat rounds; the bound stops the
moment the leader is provably unflippable, which on decisive early evidence
is round 1. On the ceiling battery the cost ordering reverses (bound 14.08
vs adaptive 4.75) because the bound refuses the cheap round-5 stop on P/O —
cheap and wrong on P (bound wins), cheap and right on O (bound loses).

Per-family cost/accuracy on ceiling:

| family | adaptive rounds | adaptive acc | bound rounds | bound acc |
|---|---|---|---|---|
| P | 5.00 | 0.000 | 19.50 | 1.000 |
| O | 5.00 | 1.000 | 19.50 | 0.000 |
| D | 4.25 | 1.000 | 3.25 | 1.000 |

## §8 The v1.1 background errors (prereg v1.2 corrections)

Two v1.1 statements were falsified BY this measurement; both are corrected
in `PREREG_H5B.md` v1.2 with the as-written gates reported verbatim above.

1. **"No evidence stream is longer than 9 items" (§0).** False for admit:
   streams run 1–48 evidence (48/248 items >16; max 48). revoke ≤ 11,
   logic ≤ 9, trap ≤ 7, cost ≤ 8. Consequence: the fixed d16 leg truncated 48
   admit items at 16 rounds; d32/d64 continued them (17–48 rounds) with
   identical verdicts. The v1.1 G5-null gate's rounds-equality half therefore
   FAILS on admit as written (48 rounds-diffs, 0 verdict-diffs); the v1.2
   restatement (verdict-equality) passes everywhere. The H5B binary's fidelity
   is unaffected — the per-item H5 replication passed 5,262/5,262 fields.
   Substantive upshot: on admit's long items the verdict settles by round 16
   at the latest and the remaining evidence (up to 32 more items) never flips
   it — early settling, not evidence consumption, governs.
2. **"Bound accuracy = adaptive accuracy on all 8 batteries" (kill bar iv).**
   Wrong as stated: P (bound 1.000 vs adaptive 0.000) and O (bound 0.000 vs
   adaptive 1.000) differ by design — that divergence IS kill bars (v-b)/(v-c).
   Correct bar: bound == adaptive on the 5 old batteries and on D (all PASS);
   bound == exhaustion-verdict per item everywhere (0/997 diffs).

## §9 wason replication (descriptive)

On P flip-40 items: d32 misses 0/10, d64 catches 10/10 — the H5 wason
mechanism (d4→d8 gain = pure evidence window) replicates at the long end:
a 40-deep flip needs depth ≥ 40. At d64 on P, rounds == evidence consumed
1-to-1 on all 40 items ("depth = evidence consumption" holds where the stream
is honest). On admit's long items, d64 likewise runs to exhaustion (up to 41
rounds) — but the verdict was already settled far earlier.

## §10 Interpretation

1. **No universal depth constant exists.** Saturation is family/distribution
   dependent: d1 (admit/revoke/logic/cost), d8 (trap, D), ≥d64 unsaturated (P),
   anti-monotone (O).
2. **The knee is an envelope, not a number.** Pooled accuracy curves can
   manufacture a false knee by cancellation (P gains cancel O losses at
   exactly ±.25/doubling → pooled flat at d8). Report knees per family.
3. **§6 (gain-window) stopping is unsafe under wrong plateaus with live
   runners-up** — 40/40 P items stop at round 5 wrong. This is a property of
   the stream shape, not the threshold: any fixed gain window stops inside a
   long-enough flat wrong plateau.
4. **The residual-flip bound strictly improves §6 on delayed valid
   disconfirmation** (P: 1.000 vs 0.000) **and is strictly worse on matched
   misleading-tail overthinking** (O: 0.000 vs 1.000). It preserves
   exhaustion, not truth. On honest distributions it is 2.6–4.6× cheaper than
   §6 at identical accuracy.
5. **Overthinking is real and symmetric to plateau-flip at scale:** 40/40 O
   items flip correct→wrong with depth, mirroring P's wrong→correct. Depth
   helps iff late evidence is valid; hurts iff it is misleading.
6. **Cap 64 was never hit** (0/997 adaptive+bound runs) — but unlike H5's
   cap-16 null, this is not because streams are short: P/O run to 40 and the
   bound/adaptive always stop first by rule.

## §11 Commit manifest

Committed to `tnn-native-lab` (this commit): prereg (v1.2), item-encoding
spec, battery (120 items), 9 configs, H5B harness sources + harness-change
docs + diff, build scripts (`build_items.py`, `fidelity.py`), fidelity log
(FC1–FC7), analysis script, this results file. NOT committed: binaries,
`.zagd` caches, sweep scratch (108 runs under `~/workspace/scratch-h5b/`).
