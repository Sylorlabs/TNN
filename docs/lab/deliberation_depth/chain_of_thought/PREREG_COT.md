# H5 Chain-of-Thought Mini-Prereg — Trace Quality vs Depth

Date: 2026-09-24. Author: H5-COT crew (subagent).
Status: FROZEN — committed before any measurement. Amendments need re-approval.

## 0. Question

Micah: does depth strengthen reasoning chains and logic solving? H5 measured
deliberation depth vs **accuracy**. The logic battery scored 1.000 at every
depth including d1 — but per RESULTS_H5.md §8.1 its evidence weights are
anchored to the source program's verdict, so 1.000 measures convergence, not
reasoning. This experiment measures the **quality of the reasoning trace** as
a function of depth, on the logic battery and on a new harder battery.

Two rival hypotheses:
- **H-MORE-ROUNDS**: deeper runs add idle re-confirmation rounds; d1's trace is
  already maximal-quality. Depth buys confidence theater, not reasoning.
- **H-BETTER-REASONING**: deeper runs do more genuine reasoning work (more
  correct eliminations, longer correct chains, more premises doing work).

## 1. Frozen structural fact F1

From `harness_v2/dlb_delib.zag` (`dlb_run`): the per-round body
(EVIDENCE→ELIMINATE→TEST→ROUND) is identical across modes; modes differ ONLY
in the stop condition (shallow: `r >= shallow_rounds`; deep: `r >= deep_rounds`;
adaptive: §6 rule; plus natural termination when a round changes nothing).
Evidence is consumed in payload order, one item per round.

**Consequence: for a fixed item, trace(depth) is a strict prefix of the
natural (uncapped) trace.** "Did deeper runs eliminate the right contenders
*earlier*?" is therefore ill-posed — deeper runs see the SAME early rounds and
additionally see more of the tail. The honest cross-depth question is: does
the tail contain reasoning work (eliminations, refutations, margin growth,
leader changes) or only restatement? The metrics below are built for exactly
this.

## 2. Trace-quality metrics (defined BEFORE measuring)

Parsed per item from the ledger segment BEGIN..VERDICT: ordered ROUND lines
`(r, leader, margin, conf)`, interleaved EVIDENCE / ELIMINATE / TEST events.
`leader(0)` := lowest hypothesis index, `margin(0)` := 0 (all scores 0, all
alive at start; ties break to lowest index per `dlb_leader`).

**Q1 — Productive-round fraction (PRF).** Round r is *productive* iff ≥1 of:
(a) an EVIDENCE event fired in r; (b) an ELIMINATE event fired in r;
(c) a TEST event with `refuted` fired in r; (d) `leader(r) != leader(r-1)`;
(e) `margin(r) > margin(r-1)`.
`PRF = (#productive rounds) / rounds_used`, mean over items per depth.
Also report mean productive-round **count** per depth. If depth buys only
rounds, the count is flat while the fraction falls.

**Q2 — Premise leverage (PL).** For each EVIDENCE event fired in round r:
*decisive* iff round r is productive per Q1 (the round's work is attributed to
its consumed evidence — in this harness all elimination/refutation in round r
happens after evidence application). `PL = (#decisive evidence) /
(#consumed evidence)`, mean per depth. Measures whether consumed premises do
work or are consumed after the verdict settled.

**Q3 — Correct eliminations per item (CE).** Count of ELIMINATE events + TEST
`refuted` events in the trace where the eliminated hypothesis ≠ ground_truth,
**on items whose final verdict == ground_truth** (items decided wrong
contribute 0: killing the right answer is anti-reasoning). Mean per item per
depth. This is the direct "genuine reasoning work" counter: killing wrong
contenders for the right reasons.

**Q4 — Post-settlement idle rounds (PSIR, unflippable version).** From the
item file, remaining evidence at round r = evidence indices ≥ consumed(r)
(consumed(r) from EVIDENCE events; evcap=64 never binds). Alive set at round r
reconstructed from ELIMINATE/TEST-refuted events. For each alive non-leader S:
`swing(S) = Σ_{e remaining} (supports(e,S) + attacks(e,leader(r)))`.
Leader is *unflippable* at r iff `margin(r) > max_S swing(S)` (strict; future
evidence cannot close the gap even in the most adversarial combination).
`PSIR = rounds_used − first_unflippable_round`; items never unflippable get
PSIR=0 and are counted in `never_unflippable_share`. Mean PSIR per depth =
the "wasted rounds" count. Report alongside `never_unflippable_share`.

All four are deterministic functions of (ledger, items file, jsonl).
No RNG, no wall-clock, no dict-order dependence (items sorted by id).

## 3. Measurement layer (frozen choice)

- **Harness/judge: pure Zag.** `delib_harness` built from `harness_v2/` with the
  pinned znc toolchain (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`);
  verdicts and the `correct` flag come from the binary itself.
- **Metric computation: deterministic Python** (`chain_of_thought/measure_cot.py`,
  no RNG, stdlib only). Rationale: the metrics are post-hoc *measurement* over
  frozen artifacts (same role as `h5_resolution/debate_prep/rederive_h5.py`);
  input SHAs are pinned in the output so any rerun is verifiable. Byte-identical
  reruns hold because all inputs are frozen bytes and the script is deterministic.

## 4. Part A — logic battery (existing sweep, no rerun)

Inputs: `~/workspace/scratch-h5/sweep/{d1,d2,d4,d8,deep16,adaptive}_logic_{A,B}.ledger`
(+ matching `.jsonl` for cross-check: `#ROUND lines == rounds_used`,
`final leader == verdict`). 264 items × 6 depths × 2 arms.

**Frozen predictions (H-MORE-ROUNDS on this battery):**
- Accuracy = 1.000 at all depths (replication of the sweep).
- Productive-round count flat across depths (≈1.0–1.3: one evidence round;
  natural termination adds one idle round at deep16/adaptive).
- Q1 (PRF) declines with depth: d1 ≈ 1.0 → deep16 ≈ 0.5.
- Q2 (PL) declines with depth (extra evidence consumed after settling).
- Q3 (CE) ≈ 0 at all depths — verify: with single 500-weight evidence,
  `elim_margin=900` should never fire and TEST should always `hold`.
- Q4 (PSIR) grows with depth: the idle natural-termination tail.

**Decision rule (logic battery):** H-MORE-ROUNDS confirmed iff productive-round
count is flat (max−min < 0.15/item), Q3 = 0 at every depth, and Q4 is
non-decreasing with depth. Any depth with strictly more productive rounds or
Q3 > 0 falsifies it on this battery.

## 5. Part B — harder logic battery (`logic_hard`, 48 items)

Design principle: the verdict must NOT be recoverable from verdict-anchored
single weights — it must require the *chain*: sequential elimination /
overturning a misleading prefix / accumulating sub-threshold premises.
Three families × 16 items, `task_type: "logic"`, same JSONL schema
(hypotheses + ordered evidence with supports/attacks + text). The `text` field
of every item states the intended inference chain for human audit.

- **Family CE (chain-elimination), 16 items.** 5 hypotheses; 4 evidence items,
  each decisively attacking one wrong contender (weight 950 ≥ elim_margin 900
  once the leader's score is set) while supports (600–800) set a wrong leader
  early. Intended chain: e1 kills contender A, e2 kills contender B, e3 kills
  the two early wrong leaders at once, e4 confirms the survivor = GT.
  Shallow depths decide wrong (wrong leader / tie-break); the verdict needs
  the full 3-hop chain.
- **Family FP (misleading prefix → flip), 16 items.** 3 hypotheses; evidence
  e1(–e2) strongly supports the WRONG hypothesis (700+600); later evidence
  attacks it (950) and supports the GT (800+300). d1/d2 verdicts are wrong;
  the correct verdict requires consuming past the misleading prefix.
- **Family DA (distractor accumulation), 16 items.** 3 hypotheses; 6 evidence
  items each supporting GT by 200 (sub-threshold individually). The leader is
  GT from round 1 (so d1 is *correct*), but eliminations only fire at rounds
  5–6 when the margin crosses 900. Tests whether deeper runs build *longer
  correct chains* (Q3) even when d1 was already right.

**Deterministic variation (no RNG):** within each family, item i varies
GT position (`i mod n_hyp`), which contender each evidence targets (rotation),
and weight scale (3 fixed patterns) — all pure index arithmetic in the
generator. Ground truth = the intended survivor by construction; the deep16
run must reproduce it on all 48 items — any mismatch is an *encoding bug*,
fixed in the battery and re-run (documented), never "fixed" by moving GT.

**Run plan:** build `delib_harness` (pinned znc, `--no-zagd`); run the 6
configs (d1/d2/d4/d8/deep16/adaptive) × `logic_hard.jsonl`, two arms A/B
(identical bytes; A/B byte-identical check required). Outputs
(`*.jsonl`, `*.ledger`, `*.stdout`) go to `~/workspace/scratch-h5/cot/`
(scratch — NOT committed, same as the H5 sweep raw records).

**Frozen predictions (H-BETTER-REASONING on this battery):**
- Accuracy: CE family 0.0 at d1/d2 → 1.0 at d4+; FP family 0.0 at d1
  (prefix-2 variants also 0.0 at d2) → 1.0 at d4+; DA family 1.0 at all depths.
- Q3 (CE): rises with depth, saturating at the family's chain length
  (CE≈3, FP≈1–2, DA≈2). Strictly: Q3(d8) > Q3(d1) on CE and DA.
- Productive-round count: rises with depth on all three families.
- Q4: small on CE/FP (verdict settles exactly when the chain completes;
  unflippable soon after) — depth's extra rounds here are *chain links*,
  not idle tail.

**Decision rule (harder battery):** H-BETTER-REASONING confirmed iff accuracy
increases with depth on CE and FP (d1 < d4 strictly) AND Q3 increases with
depth on CE and DA (d8 > d1 strictly) AND productive-round count increases
with depth. If accuracy is flat at 1.000 everywhere, the battery failed to be
harder (report as battery-design failure, not as a depth finding).

## 6. Headline rule

- If Part A confirms H-MORE-ROUNDS and Part B confirms H-BETTER-REASONING:
  headline = **depth buys nothing on verdict-anchored items; depth buys
  genuine chained/eliminative reasoning exactly where the verdict is not
  recoverable from any single evidence item or early prefix** — i.e., depth
  helps the *chain*, and the logic battery has no chain to help.
- If Part B also shows flat metrics: headline = depth buys only rounds,
  even on chained items (falsifies the "depth strengthens chains" hope in
  this harness).
- Report per-depth tables for both batteries; name the exact kind of
  reasoning depth helps (elimination chains? overturning misleading
  prefixes? sub-threshold accumulation?) from the family breakdown.

## 7. Commit plan

1. This prereg → `deliberation_depth/chain_of_thought/PREREG_COT.md`
   (commit BEFORE any measurement).
2. After measurement: `chain_of_thought/batteries/logic_hard.jsonl`
   (frozen battery), `chain_of_thought/measure_cot.py`,
   `chain_of_thought/RESULTS_COT.md`, and the run SHAs. Raw run outputs stay
   in scratch. No binaries, no `.zagd`.

Kill criteria: if the deep16 verification run disagrees with intended GT on
>2 of 48 items after one encoding fix pass, the battery design is unsound —
stop, report the failure, do not tune weights to force agreement.
