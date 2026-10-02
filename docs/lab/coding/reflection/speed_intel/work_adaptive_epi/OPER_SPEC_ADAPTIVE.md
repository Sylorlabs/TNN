# OPER_SPEC_ADAPTIVE — epistemic arm (adaptive deliberation)

Frozen 2026-09-22, BEFORE any trial run. Authority: Micah 2026-09-22
("I don't wanna have a hardcoded number there" / "only try adaptive").
Frozen prereg: `242725975e62c018bf9cba5751136a692d2a204e`
(`coding/reflection/speed_intel/PREREG_ADAPTIVE.md`).

## 1. Bar to beat (frozen)

Fixed-2x full pipeline on the frozen 94: **59/94** total (false 12/12, true
12/12, weird-English 35/70), **9.000 preds/item**, 0 reconsiderations,
0 vflips (RESULTS_SI.md).
WIN = quality ≥ 59/94 AND mean preds/item < 9.000 on the frozen 94.
FAIL = mean cost ≥ 9.000 at equal quality, or quality drop in ANY family,
or non-determinism across the 3 reruns.

## 2. Binaries

- **Control** (`2`): `work_a1/delib_si` — the existing built binary, invoked
  as `delib_si epi 2 <file>`. Byte-identical frozen behavior by construction
  (it IS the frozen binary; `delib_si.zag` untouched).
- **Adaptive** (`a`–`f`,`x`): `work_adaptive_epi/delib_ad`, built from
  `work_adaptive_epi/delib_ad.zag` with the pinned toolchain
  `toolchain/bin/znc_linux_x86_64_abed8aa1`. It is a copy of
  `delib_si.zag` in which ONLY the deliberation driver changed:
  `deliberate_si` → `deliberate_ad` (round/policy structure), `main` argv[2]
  now takes a policy letter, item lines gain a `|rounds=K` field, and the
  footer gains a `ROUNDS` line. All 9 predicates, all knowledge,
  `verify_ledger`, and all helpers are byte-identical (verified by diff —
  see §8). Pure Zag for all reasoning; Python (`score_ad.py`) is glue only
  (invocation, parsing, scoring, digests).

## 3. The learner's own signals (no label-peeking)

Routing may use ONLY information available to the learner at decision time:

- Round 0 (1x pass): `kf` (is_known_false), `ab` (is_absurd), `kt`
  (is_known_true) — the learner's own predicate firings. Derived signals:
  `has_pro = kf∨ab` (withhold-direction evidence),
  `has_con = kt` (endorse-direction evidence),
  `ambiguous (E1) = ¬has_pro ∧ ¬has_con` (no evidence at all — the learner
  knows it doesn't know),
  `conflict = has_pro ∧ has_con` (essentially impossible; escalate = safe).
- Round 1 (full pipeline): `nmatch` = count of fired speech-act matchers
  (sarcasm/hypothetical/counterfactual/analogy/poetry/implicature).
- `cm2 = is_assertion_form` — a surface property of the utterance
  (assertion frame + digit), evaluated only when `nmatch≥1` (frozen pattern).
- `non-unanimous = nmatch≥1 ∧ (kt∨cm2)` — the frozen 4x trigger, unchanged.

PROOF OF NO PEEKING: every routing branch in `deliberate_ad` is a function
of `{kf,ab,kt,nmatch,cm2}` only. The item ID is used solely for output
printing. Family labels and the answer key never enter the binary; they
exist only in `score_ad.py`, which runs after the fact. No branch conditions
on ID substrings, positions, or file order.

## 4. Cost and round accounting (frozen rules, extended honestly)

- Every predicate-function evaluation counts 1 (frozen §3d rule).
- Round 0 = 3 preds (kf, ab, kt). Round 1 ADDS 6 (the matchers); the Round-0
  evaluations are shared, never repeated — an escalated item costs 3+6 = 9,
  exactly the fixed-2x cost. (Prereg §3: "round 1 = full pipeline (2x)":
  the full pipeline IS 9 evaluations; sharing the 3 already-computed ones
  is honest counting of actual work, and keeps adaptive costs comparable.)
- cm2 evaluation +1 (only when nmatch≥1, frozen pattern); the majority
  recount +1 (frozen pattern); verification derivation +1 (frozen pattern).
- Rounds per prereg §3: round 0 = 1x pass, round 1 = full pipeline,
  round 2+ = reconsideration rounds, verification counts as a round when run.
- The control's rounds are 2/item by definition (rounds 0+1 = full pipeline).

## 5. Policies — exact stop/continue/escalate predicates

Policies are selected by argv[2]: `a`..`f`. `x` is validation-only (see §8).

**(a) stop-at-unanimity.** R0. STOP iff unanimous-with-evidence:
`(has_pro ∧ ¬has_con)` → final WITHHOLD, or `(¬has_pro ∧ has_con)` → final
ENDORSE. Else (ambiguous OR conflict) → R1. After R1: if non-unanimous →
R2 = frozen majority recount (`pro=kf+ab+nmatch` vs `con=kt+cm2`; majority
wins; tie keeps the R1 verdict). Halt. No verification. Max 3 rounds.

**(b) stop-at-verification-agreement.** (a)-routing, PLUS the independent
verification pass (`verify_ledger`, frozen code, unchanged) on EVERY final
verdict — R0-stopped items (2 rounds, 4 preds) and R1 items alike. Halt when
verification agrees (the normal case); disagreement → `vflip=1`, final
WITHHOLD (frozen 8x semantics). Note: after a reconsideration that flips
WITHHOLD→ENDORSE, `verify_ledger` disagrees BY CONSTRUCTION (its `pv`
re-derives the pre-reconsideration verdict), so (b) undoes such flips —
inherited frozen behavior, documented not fixed. Max 4 rounds.

**(c) stop-at-diminishing-evidence.** R0, then R1 ALWAYS (the "did round 1
add markers?" comparison requires running it). HALT iff `nmatch==0`
(the round added no pro/con markers). Else evaluate cm2 (+1); R2 iff
`kt∨cm2` (counter-evidence exists to resolve); halt after R2 (it adds no
new markers). No verification. Max 3 rounds.
A-priori note: this is the frozen-4x routing restated, so it costs ≥9.000
by construction and CANNOT win the cost bar — it is included as the
faithful operationalization of the prereg text (§8 verifies the
equivalence empirically).

**(d) uncertainty-routed.** R0 for every item (minimum rounds elsewhere).
Escalate to R1 iff `ambiguous (E1)` or `conflict` — the learner's own
"I have no (usable) evidence" signal. Beyond R1, extra rounds ONLY for
non-unanimous items (→ R2, frozen majority) or verification-disagreed
items; verification runs ONLY on reconsidered items — the only class where
disagreement is constructible (`verify_ledger` agrees with every
non-reconsidered verdict by construction). Max 4 rounds.

**(e) cost-capped adaptive.** (d) under a hard cap of 8 rounds, enforced in
code before each escalation (`rounds+1 > 8` blocks the round). The cap never
binds on this substrate (structural max is 4 rounds); it is a safety bound,
and the empirical ceiling is the finding, not the cap.

**(f) unanimity-or-verification** (combination, per prereg §4 "test-both").
(a)-routing + verification on R1-reached items ONLY (R0-stopped verdicts
are not re-verified — tests whether verifying the cheap verdicts is worth
its +1). Max 4 rounds.

**A-priori equivalences (to be confirmed empirically):** on the frozen 94,
(a)≡(d)≡(e) in verdicts AND cost (the frozen set has 0 non-unanimous items:
RESULTS_SI.md — so no R2 and no verification ever trigger); (c)≡fixed-4x
(verdicts+preds); (b) = (a) + 1.000 preds/item; (f) = (a) + escalated-fraction.
(a) vs fixed-2x verdicts: identical on all 94 UNLESS a kt-item fires a
matcher (then (a)=ENDORSE via R0 kt-trust, 2x=WITHHOLD — (a) strictly more
correct on true controls). Verified item-by-item in §8.

## 6. Batteries

- **Frozen 94 (primary):** `work_a1/epi/b12_false.txt` (12, F*),
  `b12_true.txt` (12, BC*), `c70.txt` (70, W*) — read in place, never copied.
- **Fresh 52 (secondary, anti-overfit):** `fresh/fresh_false.txt` (FFF01–12),
  `fresh/fresh_true.txt` (FTT01–12), `fresh/fresh_weird.txt` (FW001–28:
  4/family × 7 families). New content in the same 7-family discipline;
  design rationale + expected ledgers in `FRESH_NOTES.md`. Committed here
  BEFORE any trial run. SHAs:
  - `02a4a31e48b7f0c74f3bca56928eac6edea2a349ab1e428fc7105b4b3eba1686` fresh_false.txt
  - `59430dc5d9f77b990e8de7714da6b7062217d2bbc2b91a54948193f4e9b82057` fresh_true.txt
  - `f4d09f52df5f0c57e8039879d1f8d71cb1b245d5c84884ace253e8a44981f2b2` fresh_weird.txt
  All SHA-disjoint from `work_a1/epi/` (checked 2026-09-22; no overlap).

## 7. Cells and driver

Cells: policies {2(control),a,b,c,d,e,f} × batteries {frozen94, fresh52} ×
3 reruns = 42 cells. Driver `score_ad.py` (glue): per cell, runs the binary
once per item-file, captures raw stdout to `logs/<cell>/r<rep>.log`,
records wall-clock seconds, and takes sha256 over the raw stdout (output
contains no timing ⇒ stdout IS the canonical log). Determinism bar: the 3
per-cell digests byte-identical.

Scoring (post-hoc, never in the binary): frozen F*→WITHHOLD, BC*→ENDORSE,
W*→WITHHOLD; fresh FFF*→WITHHOLD, FTT*→ENDORSE, FW*→WITHHOLD. Family maps:
frozen per `work_a1/score_epi.py` (W001–010 joke, W023–032 sarcasm,
W045–054 hypothetical, W067–076 analogy, W109–118 counterfactual,
W089–098 poetry, W131–140 implicature); fresh FW001–004 joke, 005–008
sarcasm, 009–012 hypothetical, 013–016 analogy, 017–020 counterfactual,
021–024 poetry, 025–028 implicature.

## 8. Validation gates (before the trial sweep counts)

1. `diff` delib_ad.zag vs delib_si.zag: changes confined to
   `deliberate_si`→`deliberate_ad`, `main` arg parsing, output fields.
2. Policy `x` (fixed-2x equivalent: R0+R1 always, no early stop, no
   verification) must reproduce `delib_si` budget-2 verdicts AND preds
   item-by-item on all 94 frozen items (modulo the added `|rounds=` field).
3. Policy `c` must reproduce `delib_si` budget-4 verdicts AND preds
   item-by-item on all 94 frozen items (tests R2 path + frozen accounting).
4. Fresh-item ledger spot-check: hand-derived expected ledgers
   (FRESH_NOTES.md) confirmed by the binary before scoring.

## 9. Metrics (per policy × battery)

Quality: total + per-family (+false/true groups). Cost: mean rounds/item,
FULL rounds histogram, max rounds/item + item IDs, mean preds/item,
wall-clock per cell. Determinism: canonical digest per cell (3 reruns).
Ceiling: max rounds ever spent per policy, count + fraction of items, IDs.
