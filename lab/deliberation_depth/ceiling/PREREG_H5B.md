# H5B — Deliberation-Depth Ceiling: FROZEN PREREG (v1.2)

- **Status:** MEASUREMENT COMPLETE 2026-09-24 under v1.1; v1.2 is a
  documentation correction only (no new measurement; all gates re-checked
  against the frozen 108-cell sweep). Any further change requires H5
  coordinator sign-off + version bump + re-measurement of affected legs.
- **Date:** 2026-09-24
- **Revision history:** v1 drafted 2026-09-24 (never committed; no measurement
  runs occurred under v1). **v1.1** added the residual-flip bound as a ninth
  sweep leg (parent task 2026-09-24 — the H5 debate's discriminating
  measurement), the H5B harness revision that implements it, stop-reason
  recording, per-file parse counts, and moved the wason replication check
  from D to P. The 108-cell sweep ran under v1.1. **v1.2 (this document)**
  corrects two v1.1 background errors found BY the measurement (see §0 and
  the G5-null note in §5): admit-battery stream lengths (≤48, not ≤9) and the
  bound-vs-adaptive accuracy bar (P/O differ by design). No prediction, gate,
  or cell was changed; the as-written v1.1 gates are reported verbatim in
  RESULTS_H5B.md alongside the corrected reading.
- **Program:** H5 follow-up. Micah's question: find the depth where marginal gain
  hits zero — "the ceiling until nothing happens."
- **Parent experiment:** H5 (frozen `PREREG_H5.md` v1; results in
  `results_v2/RESULTS_H5.md`). This prereg does NOT amend the frozen H5 prereg —
  it governs a new experiment (new battery, extended sweep). No amendment to
  `PREREG_H5.md` is proposed or applied.

## §0 Why this experiment exists

H5 finding (verified independently, `h5_resolution/debate_prep/STEELMAN.md`):
on the frozen distribution the adaptive cap 16 was a null (0/877 hits) and
d8 == deep16 == 3.81 mean trap rounds; the d4→d8 gain was pure evidence-window
(5 wason items, 7 evidence each). **Correction (v1.2, found by this
measurement):** v1.1's §0 claimed "no evidence stream is longer than 9
items." That is false for the admit battery: admit streams run 1–48 evidence
(48/248 items have >16; max 48). revoke ≤ 11, logic ≤ 9, trap ≤ 7, cost ≤ 8.
Consequences, all verified in the 108-cell sweep (RESULTS_H5B.md):
(i) on admit, the fixed d16 leg truncated 48 items at 16 rounds (a fixed stop,
not natural termination) — d32/d64 continued them to 17–48 rounds with
IDENTICAL verdicts (accuracy null holds everywhere; the v1.1 G5-null gate's
rounds-equality half fails on admit as written and is restated as
verdict-equality in v1.2);
(ii) the ceiling question on accuracy is still saturated at d1 on all five
old batteries — the extra admit evidence never flips a verdict — so longer
streams were still needed to find a non-trivial ceiling, which the P/O/D
families provide.

Adjudicated design (DEBATE_H5.md §3, coordinator): delayed-disconfirmation
items — a ≥3-round confidence plateau while the running answer is wrong, then
a late premise flips it — plus a matched overthinking set (extra rounds flip a
correct early answer to wrong) and a misleading-premise dose curve (0/1/2/6).

## §1 Frozen inputs

| Artifact | Location | Note |
|---|---|---|
| Harness (pure Zag) | `ceiling/harness/` — H5B revision of `../harness_v2/` | adds `mode=bound` (residual-flip bound) + `stop=` reason in VERDICT detail; exact diff in `ceiling/harness/HARNESS_DIFF_H5B.txt`, rationale in `HARNESS_CHANGES_H5B.md`; `harness_v2/` itself UNCHANGED (H5 stays frozen) |
| Toolchain | `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` | pinned; H5B binary built twice, byte-identical required |
| Old batteries (877 items) | `../items_v2/{admit,revoke,logic,trap,cost}.jsonl` | frozen translations, unchanged |
| New battery (120 items) | `ceiling/items/ceiling_battery.jsonl` | built by `ceiling/build/build_items.py` under `ceiling/ITEM_ENCODING_SPEC_CEILING.md` v1 (spec-first, frozen before translation) |
| Configs (9) | `ceiling/configs/{d1,d2,d4,d8,d16,d32,d64,adaptive,bound}.cfg` | §2 |

Prototype dynamics (hand-built items, pre-freeze validation, NOT measurement):
§6 stops confirmed (P/O at round 5; D at 2/3/4/8 by dose). Bound prototype
(new binary, 2026-09-24): P-f6 bound refuses at 5, stops correct at 6
(stop=bound); P-f40 refuses at 5, stops correct at 40; O-f6 bound refuses
at 5, stops wrong at 6 (stop=bound); D-dose6 bound stops correct at 7
(one round before adaptive's natural stop at 8). The `stop=` ledger field
is emitted and parsed correctly.

## §2 Sweep design

Sweep points {1,2,4,8,16,32,64} + ADAPTIVE + BOUND. Every battery item × every
sweep point, each cell run twice (A/B, byte-identical binaries).

| Config | mode | rounds | ε | k | cap | elim | refute | evcap |
|---|---|---|---|---|---|---|---|---|
| d1/d2/d4/d8 | shallow | 1/2/4/8 | 20 | 3 | 64 | 900 | 600 | 64 |
| d16/d32/d64 | deep | 16/32/64 | 20 | 3 | 64 | 900 | 600 | 64 |
| adaptive | adaptive (§6 verbatim) | ≥3 | 20 | 3 | **64** | 900 | 600 | 64 |
| bound | bound (residual-flip) | — | 20* | 3* | **64** | 900 | 600 | 64 |

\* required keys, ignored in bound mode (format stability); only the cap,
elim, refute, and evcap are active. Bound spec: stop iff the round cap is
hit or the remaining unconsumed evidence provably cannot flip the current
leader — for leader L and each alive runner-up R, with
maxR = S_R + Σ remaining supports(R) and minL = S_L − Σ remaining
attacks(L), R cannot overtake L iff maxR < minL, or (maxR == minL and R > L)
since ties break to the lowest hypothesis index (harness source:
`ceiling/harness/dlb_delib.zag`, `dlb_bound_fires`). The implemented bound
sums the ACTUAL remaining weights (the tightest provable "cannot flip"
statement); the per-evidence weight ceiling (max |weight| = 500 per link,
fixed per evidence type in both encoding specs) is what makes those sums
exact. A looser `remaining_count × 500` ceiling variant fires on a PROVEN
subset of the exact version's firings, so this measurement upper-bounds any
ceiling-variant: if the exact bound shows no strict improvement over §6
somewhere, no looser ceiling variant would either. A bound-stop verdict
always equals the run-to-exhaustion verdict ("same as exhaustion", NOT
"correct" — the O family tests exactly this boundary).

All non-cap knobs are the frozen H5 values. The adaptive cap moves 16→64
(this experiment needs a cap-64 adaptive leg; on the old batteries no item
exceeds ~9 rounds, so adaptive-cap-64 must reproduce the frozen adaptive
results exactly — checked as a replication gate, §6 G6).

Cells: 6 battery files × 9 configs × 2 runs = 108 cells.

## §3 Battery construction (frozen)

120 items, 3 families × 40. Cover story (all families): claim triage —
hypotheses ADMIT (admit the claim into the knowledge base) vs REJECT.
Full weight tables in `ITEM_ENCODING_SPEC_CEILING.md` §4; the rules below
are the normative summary.

**P — plateau-then-flip (40 items).** Early misleading reports put ADMIT
(the wrong answer) ahead; a plateau of balanced evidence holds confidence
perfectly flat while the running answer is wrong; a late decisive premise
flips the verdict to REJECT.
- Flip rounds f ∈ {6,12,20,40}, 10 structural replicates each.
- e1: supports {ADMIT: a}, e2: supports {ADMIT: 500−a}, a ∈ {300,250,400,150,450}
  cycling by replicate (margin after e2 always 500; conf 300→500, gains 0 then ≥50).
- e3..e_{f−1}: supports {ADMIT: w, REJECT: w}, w ∈ {90,100,110} cycling
  (margin constant 500, conf constant 500, all gains 0).
- e_f, e_{f+1}, e_{f+2}: supports {REJECT: 500}, attacks {ADMIT: 500}
  (flip at round f; decisive tail).
- Hypotheses [ADMIT, REJECT]; ground_truth REJECT.
- **Preregistered adaptive stop round: 5** (plateau rounds 3..f−1; §6 fires at
  the first round with 3 sub-ε gains: g3=g4=g5=0). Verdict at stop: ADMIT (wrong).

**O — overthinking, polarity-matched to P (40 items).** Early decisive evidence
puts REJECT (the right answer) ahead; a plateau of balanced evidence holds
confidence flat; late misleading noise flips the verdict to ADMIT (wrong).
- Flip rounds f ∈ {6,12,20,40}, 10 structural replicates each (same skeleton
  as P, polarity reversed).
- e1: supports {REJECT: a}, e2: supports {REJECT: 500−a}, same a cycle.
- e3..e_{f−1}: supports {REJECT: w, ADMIT: w}, same w cycle.
- e_f, e_{f+1}: supports {ADMIT: 500}, attacks {REJECT: 500} (flip-to-wrong).
- Hypotheses [REJECT, ADMIT]; ground_truth REJECT (the early decisive answer).
- **Preregistered adaptive stop round: 5.** Verdict at stop: REJECT (correct).

**D — misleading-premise dose curve (40 items).** d ∈ {0,1,2,6} misleading
premises (supports {ADMIT: 100} each, frozen-trap scale), then 2 corrective
(supports {REJECT: 500}, attacks {ADMIT: 500}).
- 10 structural replicates per dose.
- Hypotheses [ADMIT, REJECT]; ground_truth REJECT.
- **Preregistered adaptive stop rounds: dose 0→2, 1→3, 2→4, 6→8**
  (validated pre-freeze; natural termination, monotone in dose).

Within-cell replicates are structural (identical score dynamics by
construction, distinct ids/texts); the independent variation is across flip
positions and doses. All weights are fixed constants or fixed cyclings —
no per-item hand tuning, no RNG.

## §4 Oracle construction

The oracle is the item author: `build_items.py` implementing the frozen
ceiling encoding spec. It designates `ground_truth` at construction time.
- P/D: the designation coincides with the full-stream argmax
  (Σ supports − Σ attacks, ties to lowest hypothesis index) — verified by
  fidelity gates FC1/FC3. The oracle "reads the full stream" via the
  translator's independent argmax re-derivation (same method as frozen F1).
- O: the designation is the EARLY decisive answer and DIFFERS from the
  full-stream argmax by design (verified FC2: full-stream argmax = ADMIT ≠ GT).
  That divergence IS the overthinking treatment: late evidence is genuinely
  misleading noise, and the oracle (like a trainer) knows the early verdict
  was the right one.
- Accuracy is always verdict == ground_truth.

## §5 Decision rules and kill bars (frozen)

**Saturation point (per battery).** S(B) = the smallest sweep depth p such
that acc(p) equals the battery's maximum accuracy over the sweep AND
acc(q) = acc(p) for every deeper sweep depth q. (State-labeling, per the
H5 adjudication — the literal interval phrasing "first depth with marginal
gain 0" reproduces the flagged off-by-one on the old trap data: it would
label S=16 where the curve is flat from d8. The marginal-gain series is
reported alongside so both labelings are auditable.)
- Non-monotone battery (max reached but deeper < max): NO saturation point;
  report NON-MONOTONE.
- Battery whose max is reached only at the deepest sweep point: S = that
  point, flagged "ceiling confirmed within sweep; deeper untested."

**Kill bar (i) — §6 stops inside a wrong plateau (P family).**
Preregistered: adaptive stop_round = 5 on 40/40 P items (< every flip round),
verdict ADMIT (wrong) on 40/40; stops-inside-plateau rate 40/40.
DECISION: if acc_adaptive(P) < acc_deep64(P) − 0.01 → §6 is UNSAFE on
plateau-then-flip streams; the H5 ADAPTIVE-WINS verdict does not generalize
beyond non-plateauing streams. (Expected: 0.000 vs 1.000 — fires by design;
this is an existence proof against the generalization, not against H5's
frozen verdict on its own distribution.)

**Kill bar (ii) — overthinking non-monotonicity (O family).**
Preregistered: every O item correct at d4 AND wrong at d64 (40/40).
Overthinking rate = fraction of O items with correct(shallow) ∧ wrong(deep64).
DECISION: if overthinking rate > 0 → fixed-deep caps are NON-MONOTONE on
this distribution; "deeper = better" is falsified; no constant cap ≥ a flip
position is safe. (Expected: 40/40 — fires by design.)

**Kill bar (iii) — dose-response monotonicity (D family).**
Preregistered: adaptive rounds_used = 2/3/4/8 for doses 0/1/2/6
(monotone non-decreasing), adaptive accuracy 1.000 at every dose.
DECISION: if rounds_used is not monotone in dose, or any dose's adaptive
accuracy < 1.000 → the "rounds track residual conflict" claim FAILS.

**Kill bar (iv) — saturation points.** Reported per battery with S marked
explicitly; preregistered expectations: admit/revoke/logic/cost S=1,
trap S=8, P S=64 (top-of-sweep flag), O NON-MONOTONE, D S=8.
Bound leg: bound accuracy = adaptive accuracy on the 5 old batteries and on
D (a bound-stop verdict equals the run-to-exhaustion verdict by construction;
any deviation there is a harness bug). On P/O they differ BY DESIGN
(P: bound 1.000 vs adaptive 0.000; O: bound 0.000 vs adaptive 1.000) —
that divergence is kill bar (v-b)/(v-c), not a bug. Bound mean rounds ≤
adaptive mean rounds on admit/revoke/logic/cost/trap/D (bound fires at
elimination-completion, up to 3 rounds before §6's gain window closes);
bound mean rounds > adaptive on P and O (19.5 vs 5 — the bound refuses
the round-5 stop).
Also reported: where cap-16/32/64 is null — i.e., per battery, the deepest
sweep point whose accuracy AND mean rounds both equal the next-shallower
point's (fixed configs), and the adaptive/bound cap-hit rates.

**Kill bar (v) — residual-flip bound vs §6 (the debate's discriminating
measurement).** Every run records its stop cause (`stop=fixed|six|bound|
natural|cap`, first cause wins) in the VERDICT ledger detail.

(v-a) Firing counts. Per battery (all 8): #bound-firings (bound config,
stop=bound) vs #six-firings (adaptive config, stop=six), plus the full
stop-reason distribution per config. Preregistered: on the easy batteries
bound-firings ≥ six-firings (the bound fires at elimination-completion;
§6 needs 3 more sub-ε gain rounds, which natural termination often
preempts); on trap both ≈ 0 (margins move honestly to exhaustion).

(v-b) THE discriminating case (P family). Preregistered: on 40/40 P items
the bound REFUSES the round-5 stop (runner-up REJECT alive and flippable
via the unseen flip evidence), stops at the flip round f (6/12/20/40),
verdict REJECT (correct) 40/40 — while §6 stops at round 5, verdict ADMIT
(wrong) 40/40. DECISION: if the bound refuses at 5 and finishes correct
on 40/40 → the bound is a STRICT improvement over §6 on plateau-then-flip
streams; AGAINST's "new rule, same behavior" is REFUTED on this class and
FOR's "strict improvement, not redundant machinery" is confirmed.

(v-c) The symmetric boundary (O family). Preregistered: on 40/40 O items
the bound likewise REFUSES the round-5 stop (runner-up ADMIT alive and
flippable via the unseen noise), stops at the flip round f, verdict ADMIT
(wrong) 40/40 — while §6 stops at 5, verdict REJECT (correct) 40/40.
DECISION: the bound does NOT dominate §6 — it guarantees "same as
exhaustion", which is wrong when exhaustion is wrong. Any law claim for
the bound must be scoped accordingly (this is the honest boundary of
FOR claim 2: the bound is the right stopping law for streams where
evidence exhaustion is the right policy, and a costlier mistake than §6
where it is not).

(v-d) Accuracy/cost by stop reason. Per battery: accuracy and mean rounds
among bound-stopped runs vs six-stopped runs (descriptive; the head-to-head
the debate asked for).

**Wason-replication check (descriptive).** On **P** (moved from D in v1.1 —
D's streams, max 8 evidence, do not exceed the frozen 9-item maximum): the
flip depth must equal evidence consumed — fixed-d32 must MISS the f40 flip
(32/42 evidence, verdict ADMIT wrong) while fixed-d64 CATCHES it (verdict
REJECT right); rounds/evidence remain one-to-one until natural termination.
This replicates "depth = evidence consumption" at 40 items, 4.4× the frozen
stream maximum. D remains the dose-response check (kill bar iii).

## §6 Validity gates (all must pass or the run is invalid)

- G1 determinism: all 108 cells A/B byte-identical (results.jsonl, ledger.jsonl,
  stdout). Any mismatch = harness bug: stop, fix, re-run.
- G2 parse: per-file item counts parse in every cell, 0 errors (harness exit 0):
  admit 248, revoke 113, logic 264, trap 127, cost 125, ceiling 120.
- G3 config echo: ledger CONFIG line shows the intended mode/rounds/cap per cell
  (bound cells echo `mode=bound`).
- G4 fidelity (pre-measurement, Python, on the built battery):
  FC1 P full-stream argmax = GT 40/40; FC2 O full-stream argmax = ADMIT 40/40
  AND first-5-evidence argmax = GT 40/40; FC3 D full-stream argmax = GT 40/40;
  FC4 all 120 items parse, d64 verdicts recorded; FC5 d1 baselines: P→ADMIT
  40/40, D dose>0→ADMIT 30/30, D dose-0→GT 10/10, O→GT 40/40;
  FC6 adaptive stop rounds on the built battery: P 5 (40/40), O 5 (40/40),
  D 2/3/4/8 by dose (10/10 each);
  FC7 bound prototype (new binary): P-f6 bound refuses at 5 / stops correct
  at 6, P-f40 refuses at 5 / stops correct at 40, O-f6 refuses at 5 / stops
  wrong at 6, D-dose6 stops correct at 7 (all stop=bound).
- G5 replication: old-battery legs at d1/d2/d4/d8/d16/adaptive run under the
  H5B binary reproduce `results_v2/RESULTS_H5.md` per-item (verdict,
  confidence, rounds_used, evidence_consumed) exactly. **v1.2 restatement:**
  v1.1 required d32/d64 on old batteries to equal d16 in rounds too ("natural
  termination"); the measurement showed d16 was a fixed truncation on 48
  admit items (>16 evidence), so the rounds half fails on admit as written.
  The v1.2 null check is verdict-equality d32/d64 == d16 (holds on all 5 old
  batteries, 0 verdict diffs), with rounds differences reported descriptively
  (admit: 48 items run 17–48 rounds at d32/d64). Expected ledger-only diff vs
  frozen H5 ledgers: the VERDICT detail gains the `stop=` field (documented
  harness change). Any other deviation = investigate before reading any
  new-battery result.
- G6 censoring: report adaptive AND bound cap-hit rates per battery
  (expected 0 everywhere — §6/the bound or natural termination always fires
  first, even at cap 64).

## §7 Analysis deliverables

`RESULTS_H5B.md`: per-battery accuracy-vs-depth tables (old 5 + P/O/D) with n;
saturation point marked per battery; marginal-gain series; mean rounds and
mean evidence consumed per cell; kill-bar verdicts (i)–(v); bound-vs-§6
firing-count tables per battery (v-a), per-item §6-vs-bound stop-round
cross-tab on P (v-b) and O (v-c), accuracy/cost by stop reason (v-d);
cap-null report (fixed configs: deepest null depth per battery;
adaptive/bound: cap-hit rates); wason-replication check on P
(d32 misses f40, d64 catches it); the knee-envelope-vs-constant reading;
honest limitations (adversarial-construction caveat: P and O are existence
proofs of plateau-then-flip and overthinking, not base rates; the O oracle's
full-stream divergence is by design; the bound guarantees "same as
exhaustion", not correctness). All evidence committed: battery, configs,
harness revision + exact diff, build/fidelity/analysis scripts, results doc.
Raw sweep records (jsonl+ledger+stdout, 108 cells) kept in workspace
scratch, paths recorded.

## §8 Standing constraints

Pure Zag for harness/judge; zero RNG in any decision path; byte-identical
reruns (A/B); commit via `~/workspace/commit_racefree.py` with lab-relative
paths (`deliberation_depth/ceiling/...`), `TMPDIR=~/workspace/tmp_commit`;
no binaries, no `.zagd`. ε/k tuning post-data is inadmissible without
amendment + re-measurement.

## §9 Amendments

Coordinator sign-off + version bump + re-measurement of affected legs.
No amendment to the frozen H5 prereg (`PREREG_H5.md`) is made or proposed
by this document.

**v1 → v1.1 (2026-09-24, pre-measurement, parent-authorized):** added the
residual-flip bound as a ninth sweep leg with preregistered per-battery
predictions and kill bar (v); H5B harness revision (`ceiling/harness/`,
exact diff in `HARNESS_DIFF_H5B.txt`) implementing `mode=bound` and the
`stop=` VERDICT field; G2 per-file parse counts (was "997/997 in every
cell"); wason replication check moved D→P; FC7 bound prototype gates;
G1/G6 updated to 108 cells and bound cap-hit rates. No measurement runs
had occurred under v1.
