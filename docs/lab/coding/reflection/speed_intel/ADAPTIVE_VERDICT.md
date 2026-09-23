# ADAPTIVE DELIBERATION — COMBINED VERDICT

**Date:** 2026-09-22 · **Authority:** Micah — "I don't wanna have a
hardcoded number there" / "only try adaptive" (adaptive only; fixed
higher budgets dropped per his explicit correction).
**Frozen prereg:** `coding/reflection/speed_intel/PREREG_ADAPTIVE.md`
(commit `242725975e62c018bf9cba5751136a692d2a204e`).
**Branch:** `tnn-native-lab` · **Dir:** `coding/reflection/speed_intel/`
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Overall verdict: PARTIAL — adaptive wins on epistemics, fails on coding

| Domain | Result | Champion |
|---|---|---|
| Epistemic (94-item frozen + 52 fresh) | **4 policies WIN** | (a) stop-at-unanimity (equivalence class a/d/e) |
| Coding (20-item frozen + 12 fresh) | **0 WIN, 3 FAIL, 2 NULL** | none — keep fixed budget-4 |

## 1. Epistemic arm (commits `94498207`, `9de7b901`)

Frozen kill bars: WIN = ≥59/94 AND <9.000 preds/item.

**Frozen 94** — per-family /10 identical for ALL policies
(joke 5, sarcasm 3, hypothetical 5, analogy 3, counterfactual 9,
poetry 5, implicature 5). Zero verdict differences vs fixed-2x on all
94 items for every adaptive policy (item-by-item verified); all deltas
are cost-only. 42 cells × 3 reruns byte-identical.

| policy | qual /94 | mean preds | mean rounds | rounds hist | max rnd | verdict |
|---|---|---|---|---|---|---|
| 2x (control) | 59 | 9.000 | 2.000 | {2:94} | 2 | baseline |
| (a) unanimity | 59 | **8.043** | 1.787 | {1:20, 2:74} | 2 | **WIN** |
| (b) verify-agree | 59 | 9.043 | 2.787 | {2:20, 3:74} | 3 | FAIL |
| (c) dimin-evidence | 59 | 9.319 | 2.000 | {2:94} | 2 | FAIL |
| (d) uncert-routed | 59 | **8.043** | 1.787 | {1:20, 2:74} | 2 | **WIN** |
| (e) cost-capped | 59 | **8.043** | 1.787 | {1:20, 2:74} | 2 | **WIN** |
| (f) unanim-or-verify | 59 | **8.830** | 2.574 | {1:20, 3:74} | 3 | **WIN** |

**Fresh 52 (secondary)** — adaptive beats fixed-2x on quality AND cost:

| policy | qual /52 | mean preds | mean rounds | rounds hist | max rnd |
|---|---|---|---|---|---|
| 2x (control) | 49 (true 9/12) | 9.000 | 2.000 | {2:52} | 2 |
| (a) | **51** | 6.769 | 1.635 | {1:24, 2:23, 3:5} | 3 |
| (b) | **51** | 7.769 | 2.635 | {2:24, 3:23, 4:5} | 4 |
| (c) | **51** | 9.692 | 2.173 | {2:43, 3:9} | 3 |
| (d) | **51** | 6.865 | 1.731 | {1:24, 2:23, 4:5} | 4 |
| (e) | **51** | 6.865 | 1.731 | {1:24, 2:23, 4:5} | 4 |
| (f) | **51** | 7.308 | 2.173 | {1:24, 3:23, 4:5} | 4 |

Mechanism notes: on fresh FTT10–12 (true+matcher-bait) fixed-2x
wrongly withholds; adaptive policies stop at round 0 on known_true and
endorse correctly. FW008/012/016/020/024 (matcher+assertion-form) —
reconsider → tie → keep WITHHOLD, correct. FW028 (kt-poisoning) — the
single adaptive miss: round-0 kt-trust wrongly ENDORSEs; only fixed-2x
gets it right. **0 verification flips in the entire trial**
(146 items × 7 policies × 3 reruns) — verification is pure overhead.

**Discovered ceiling (both batteries): 4 rounds.** The 8-round cap never
came close to binding. On frozen, max was 2 (a/d/e) and 3 (b/f).

**Epistemic champion: the (a)/(d)/(e) equivalence class.**
Recommended mainline default: **(a) stop-at-unanimity** — fewest moving
parts; the no-evidence escalation is the learner's own ambiguity signal
either way. −10.6% cost at identical quality on frozen; better quality
at lower cost on fresh.

**Honest limits:** no adaptive policy recovers any of the 35/70 frozen
weird misses — those need new matchers/knowledge, not more rounds.
Adaptive routing saves cost; it does not create evidence. FW028 is a
documented failure mode where fixed-2x wins.

## 2. Coding arm (commits `1394add7`, `6a24ff95`)

Frozen kill bars: WIN = ≥18/18 AND honest-halt 2/2 AND mean <2.30
iters/item on the frozen battery.

| policy | frozen Q / halt / mean | fresh Q / halt / mean | verdict |
|---|---|---|---|
| fixed budget-4 | 18/18, 2/2, 2.300 | 11/11, 1/1, 2.500 | baseline |
| (a) unanimity | 18/18, 2/2, 2.300 | 11/11, 1/1, 2.500 | NULL (inert) |
| (b) verify-agree | **17/18**, 2/2, 1.650 | 11/11, 1/1, 1.750 | **FAIL** |
| (c) dimin-evidence | 18/18, 2/2, 2.300 | 11/11, 1/1, 2.500 | NULL (inert) |
| (d) uncert-routed | **17/18**, 2/2, 2.250 | **10/11**, 1/1, 2.417 | **FAIL** |
| (e) cost-capped | **16/18**, 2/2, 1.600 | **10/11**, 1/1, 1.667 | **FAIL** |

Rounds histograms (frozen): control/a/c `{1:8, 3:10, 4:2}`;
b `{1:8, 2:11, 3:1}`; d `{1:8, 2:1, 3:9, 4:2}`; e `{1:8, 2:12}`.
**Empirical ceiling: 4 iterations** (S06, S12). Hard cap 16 never
approached. 36 cells × 3 reruns byte-identical.

**Failure root causes** (design flaws the trial caught, not impl bugs):
1. (b)/(e) verify-extend: `patch_arg_unquote` stripped quotes from
   `_zag_print("42")` → `_zag_print(42)`, breaking S10 into an unfixable
   ARITY error → halt-no-patch. A patch-applicability check is not a
   defect detector — in the frozen learner that patch only runs after a
   TYPE diagnosis; verify-extend ran it with no type evidence.
2. (d)/(e) budget requests: S08 needs 3 rounds (NAME + test-visible
   LOGIC_VALUE) but the learner requested 2 — the rule counts only
   source-only classes, blind to test-visible defects → budget-exhausted.
   Replicated on fresh (10/11).

(a) and (c) are inert nulls: (a) behavior-identical to control;
(c)'s halt-hopeless fired 0 times in 36 runs.

**The deeper finding:** the fixed budget of 4 was already near-optimal
because the learner's per-round diagnosis already adapts — gen items use
1 round, hard items use 3–4. The "think count" was already adaptive;
making it *more* adaptive broke it. Cost savings were real (b: 33 vs 46
iters; e: 32 vs 46) but inseparable from quality loss on this battery.

## 3. The ceiling, discovered not hardcoded

| Domain | Champion policy | Max rounds ever spent | Cap | Cap bound? |
|---|---|---|---|---|
| Epistemic | (a) stop-at-unanimity | **4** (5 fresh items, 9.6%) | 8 | never |
| Coding | none (fixed-4 stands) | **4** (S06, S12) | 16 | never |

Micah's "best number for now," read off the data: **4 rounds**. No
policy in either domain ever needed more; caps at 8/16 were dead
weight. The number is discovered, not set.

## 4. Recommendation for mainline defaults

1. **Epistemic: adopt (a) stop-at-unanimity** as the deliberation default
   (−10.6% cost, identical quality on frozen; wins on fresh).
2. **Coding: keep the fixed budget-4 default** (promotion prereg P1).
   Do not adopt any adaptive coding policy — all fail or are inert.
3. **Do not adopt verification-as-round** anywhere: 0 flips in 146
   epistemic items; the coding verify-extend actively broke a repair.
   Verification stays a post-hoc audit, not a deliberation round.
4. **Epistemics 59/94 is a knowledge ceiling, not a rounds ceiling.**
   No round policy recovers the 35/70 weird misses. The SI-Arm-1
   failure-taxonomy work (why it's stuck) is the load-bearing next step,
   not more deliberation.

## 5. Evidence

- Epistemic: `work_adaptive_epi/` — OPER_SPEC_ADAPTIVE.md (frozen
  pre-trial), delib_ad.zag, FRESH_NOTES.md + 52 fresh items,
  results_adaptive.json, 42 canonical cell logs, ADAPTIVE_VERDICT_EPI.md.
- Coding: `work_adaptive_code/` — OPER_SPEC (frozen pre-trial),
  learner_adapt.zag, driver_adapt.py, fresh battery, 36 run logs,
  ADAPTIVE_VERDICT.md (arm-level).
- Determinism: every cell × 3 reruns byte-identical canonical.
- Zero RNG in all decision paths. Pure Zag reasoning; Python glue only.
