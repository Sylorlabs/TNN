# ADAPTIVE DELIBERATION — epistemic arm verdict (2026-09-22)

Authority: Micah 2026-09-22 (adaptive only; no hardcoded think-count).
Frozen prereg: `242725975e62c018bf9cba5751136a692d2a204e`.
Frozen OPER_SPEC: `work_adaptive_epi/OPER_SPEC_ADAPTIVE.md` (committed
`94498207` BEFORE any trial run; no amendments).
Toolchain: `toolchain/bin/znc_linux_x86_64_abed8aa1`.
Control: `work_a1/delib_si` budget 2 (the frozen binary itself).
Adaptive binary: `work_adaptive_epi/delib_ad` (built from `delib_ad.zag`;
all 9 predicates, knowledge, `verify_ledger`, helpers byte-identical to
`delib_si.zag` — fn-level md5 verified; only the round/policy driver changed).

## Headline

**Four of six adaptive policies WIN on the frozen 94** (quality ≥ 59/94 AND
mean cost < 9.000 preds/item): (a), (d), (e), (f). The mechanism is the
round-0 early stop: 20/94 items are decided unanimously on world-knowledge
evidence alone (12 falsehoods via known_false, 5 absurd jokes, 3 known
truths), costing 3 preds instead of 9, with **zero verdict changes** —
every adaptive policy's verdicts are item-by-item identical to fixed-2x on
all 94 frozen items. (b) and (c) FAIL on cost (9.043 and 9.319 ≥ 9.000),
exactly as the OPER_SPEC predicted a priori.

## Frozen 94 (decisive)

Fixed-2x baseline to beat: 59/94, 9.000 preds/item.

| policy | quality /94 | false /12 | true /12 | per-family /10 (j,s,h,a,c,p,i) | mean preds | mean rounds | rounds hist | max rounds |
|---|---|---|---|---|---|---|---|---|
| 2 (control) | 59 | 12 | 12 | 5,3,5,3,9,5,5 | 9.000 | 2.000 | {2:94} | 2 |
| a unanimity | 59 | 12 | 12 | 5,3,5,3,9,5,5 | **8.043** | 1.787 | {1:20, 2:74} | 2 |
| b verify-all | 59 | 12 | 12 | 5,3,5,3,9,5,5 | 9.043 | 2.787 | {2:20, 3:74} | 3 |
| c dim-evidence | 59 | 12 | 12 | 5,3,5,3,9,5,5 | 9.319 | 2.000 | {2:94} | 2 |
| d uncertainty | 59 | 12 | 12 | 5,3,5,3,9,5,5 | **8.043** | 1.787 | {1:20, 2:74} | 2 |
| e capped-8 | 59 | 12 | 12 | 5,3,5,3,9,5,5 | **8.043** | 1.787 | {1:20, 2:74} | 2 |
| f verify-escalated | 59 | 12 | 12 | 5,3,5,3,9,5,5 | **8.830** | 2.574 | {1:20, 3:74} | 3 |

(families: joke, sarcasm, hypothetical, analogy, counterfactual, poetry,
implicature — identical for every policy: **no family drop anywhere**.)
Cost per quality point (SI convention, preds per pp): 2x 13.47 → a/d/e 12.04.
Determinism: all 14 cells × 3 reruns byte-identical canonical (IDENTICAL).
Wall-clock per cell (3 reps, machine-load-dependent): 0.02–0.26 s.

Verdict-vs-baseline proof: **0 verdict differences** between fixed-2x and
any adaptive policy on all 94 frozen items (checked item-by-item from raw
logs). All per-policy differences are preds-only. The 20 round-0-stopped
items: F003–F231 (12, known_false), BC01–BC03 (3, known_true), W001–W005
(5, absurd). The 74 escalated items are exactly the E1 no-evidence set.

### Empirical ceiling (frozen)

| policy | max rounds ever spent | # items | fraction | item IDs |
|---|---|---|---|---|
| a | 2 | 74 | 78.7% | the 74 E1-escalated (BC04–12, W006–W140 non-absurd) |
| b | 3 | 74 | 78.7% | same 74 (verification round) |
| c | 2 | 94 | 100% | all (always runs round 1) |
| d | 2 | 74 | 78.7% | same as (a) — 0 non-unanimous items, no verification triggered |
| e | 2 | 74 | 78.7% | same as (a) — 8-round cap never bound |
| f | 3 | 74 | 78.7% | same 74 (verification round on R1 items) |

## Fresh 52 (secondary, anti-overfit)

52 new items (12 false FFF, 12 true FTT, 28 weird FW 4×7 families), SHAs
committed before results, SHA-disjoint from `work_a1/epi/` verified.

| policy | quality /52 | false | true | families (impl noted) | mean preds | mean rounds | rounds hist | max rounds |
|---|---|---|---|---|---|---|---|---|
| 2 (control) | 49 | 12 | 9 | all 4/4 | 9.000 | 2.000 | {2:52} | 2 |
| a | **51** | 12 | 12 | impl 3/4 | 6.769 | 1.635 | {1:24, 2:23, 3:5} | 3 |
| b | **51** | 12 | 12 | impl 3/4 | 7.769 | 2.635 | {2:24, 3:23, 4:5} | 4 |
| c | **51** | 12 | 12 | impl 3/4 | 9.692 | 2.173 | {2:43, 3:9} | 3 |
| d | **51** | 12 | 12 | impl 3/4 | 6.865 | 1.731 | {1:24, 2:23, 4:5} | 4 |
| e | **51** | 12 | 12 | impl 3/4 | 6.865 | 1.731 | {1:24, 2:23, 4:5} | 4 |
| f | **51** | 12 | 12 | impl 3/4 | 7.308 | 2.173 | {1:24, 3:23, 4:5} | 4 |

Adaptive BEATS fixed-2x on fresh quality (51 vs 49) at lower cost. The
mechanism, exactly as designed in FRESH_NOTES.md:
- FTT10–FTT12 (true + matcher-bait): 2x withholds wrongly (matcher fires);
  (a)/(b)/(d)/(e)/(f) stop at round 0 on known_true unanimity → ENDORSE
  (right) without ever consulting matchers; (c) repairs via the R2 majority
  (pro=1 vs con=2) → ENDORSE (right).
- FW008/FW012/FW016/FW020/FW024 (matcher + assertion-form ties): all
  policies that reach R1 reconsider → tie → keep WITHHOLD (right); these are
  the max-round items (5/52).
- FW028 (kt-poisoning: true phrase inside a weird utterance): 2x right
  (matcher → WITHHOLD); (a)/(b)/(d)/(e)/(f) wrong (R0 kt-trust stops before
  matchers → ENDORSE); (c) wrong (R2 con>pro flips → ENDORSE). The single
  miss for every adaptive policy — the documented cost of R0 kt-trust.
- Verification (b/d/e/f) agreed on all 5 reconsidered items: **0 vflips in
  the entire trial** (frozen + fresh, all policies). The frozen-8x quirk
  (verification undoing a reconsideration flip) never triggered — no
  reconsideration in this trial ever flipped a verdict TO endorse and then
  met verification (only (c) flips, and (c) doesn't verify).

### Empirical ceiling (fresh)

| policy | max rounds | # items | fraction | item IDs |
|---|---|---|---|---|
| a | 3 | 5 | 9.6% | FW008, FW012, FW016, FW020, FW024 |
| b | 4 | 5 | 9.6% | same 5 (verification round) |
| c | 3 | 9 | 17.3% | FTT10, FTT11, FTT12, FW008, FW012, FW016, FW020, FW024, FW028 |
| d | 4 | 5 | 9.6% | same 5 (verification of reconsidered) |
| e | 4 | 5 | 9.6% | same 5 — 8-round cap never bound |
| f | 4 | 5 | 9.6% | same 5 |

Combined ceiling across both batteries: (a) 3 rounds, (b) 4, (c) 3, (d) 4,
(e) 4, (f) 4. **The empirical ceiling is 4 rounds** — the 8-round cap is
nowhere near binding.

## Verdicts per policy (frozen kill bars)

- **(a) stop-at-unanimity: WIN.** 59/94, 8.043 < 9.000, no family drop,
  deterministic. −10.6% cost at identical quality.
- **(b) stop-at-verification-agreement: FAIL.** 59/94 but 9.043 ≥ 9.000.
  Verifying every verdict (+1 pred/item) costs more than round-0 stopping
  saves, and verification never disagreed (0/146 items) — pure overhead.
- **(c) stop-at-diminishing-evidence: FAIL.** 59/94 but 9.319 ≥ 9.000.
  Proven a priori (it must run round 1 to compare markers) and confirmed;
  empirically ≡ fixed-4x verdicts+preds on all 94 (validation gate).
- **(d) uncertainty-routed: WIN.** 59/94, 8.043 < 9.000. Behaviorally
  identical to (a) on both batteries (byte-identical digests on frozen;
  +0.096 preds/item on fresh for verification that always agreed).
- **(e) cost-capped adaptive: WIN.** 59/94, 8.043 < 9.000. Identical to
  (d); the 8-round cap never bound (structural max 4).
- **(f) unanimity-or-verification: WIN.** 59/94, 8.830 < 9.000. Cheaper
  than (b) (skips verifying the cheap round-0 verdicts), costlier than
  (a)/(d)/(e).

**Champion: the (a)/(d)/(e) equivalence class** — identical verdicts and
frozen cost on all current evidence. Recommended mainline default: **(a)
stop-at-unanimity** (fewest moving parts; the E1 no-evidence escalation is
the learner's own ambiguity signal either way). (e)'s 8-round cap is a free
safety bound if the line wants belt-and-braces. "No adaptive policy beats
fixed-2x" is rejected: four do, on cost at identical quality.

## Honest limits

1. The frozen 94 never exercise reconsideration or verification (0/94
   non-unanimous — the SI Arm 1 finding), so (a)/(d)/(e) are
   indistinguishable there; the fresh battery separates them only mildly
   (5 tie-traps; verification agreed 5/5, never flipped).
2. R0 kt-trust has a documented failure mode: FW028 (a true phrase embedded
   in a weird utterance) stops all matcher consultation → wrong ENDORSE
   under (a)/(b)/(d)/(e)/(f), and (c)'s reconsideration flips it wrong too.
   Only fixed-2x gets FW028 right. Cheap early stopping trusts cheap
   evidence; adversarial phrasing can exploit that.
3. No adaptive policy recovers any of the 35/70 frozen weird misses — those
   are "no matcher fired → default endorse" and need new matchers/knowledge,
   not more rounds. Adaptive routing saves cost; it does not create
   evidence. (Consistent with SI Arm 1: 4x/8x added zero quality.)
4. The verification-disagreement path (the frozen-8x flip quirk) was never
   exercised: 0 vflips across 146 items × 7 policies × 3 reruns. (b)'s
   "otherwise reconsider" branch is therefore untested by data, though its
   logic is the frozen, reviewed 8x semantics.
5. Cost unit is predicate-function evaluations (frozen §3d convention);
   absolute values are not comparable across arms, only the orderings.

## Commits (branch tnn-native-lab)

- `944982079d62ce3017fa77208d3bac59e6c5f225` — OPER_SPEC_ADAPTIVE.md
  (frozen before any trial run), delib_ad.zag, FRESH_NOTES.md, fresh battery
  (SHAs in OPER_SPEC §6).
- Source fix after commit (this commit): one-line change to delib_ad.zag —
  the non-unanimity cm2 evaluation is now skipped for the validation-only
  policy `x` (it had added +1 pred on matcher-fired items vs frozen 2x).
  Trial policies (a)–(f) code path semantically identical before/after
  (guard is true for pol 1–6); all three validation gates re-run PASS on
  the fixed binary. All trial results above were produced with the fixed
  binary; the committed source matches it.
- This commit: results_adaptive.json, logs/ (42 canonical cell logs),
  ADAPTIVE_VERDICT_EPI.md, score_ad.py, validate_ad.py, fixed delib_ad.zag.
  Binaries and .zagd caches NOT committed.
