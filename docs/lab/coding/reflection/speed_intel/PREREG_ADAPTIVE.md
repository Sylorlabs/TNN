# ADAPTIVE DELIBERATION — FROZEN PREREGISTRATION

**Date frozen:** 2026-09-22 · **Order:** Micah — "I don't wanna have a
hardcoded number there" / "only try adaptive" (2026-09-22). TNN itself
decides, per decision, how many reconsideration rounds to spend.
**Explicit correction from Micah:** do NOT test fixed higher budgets —
4×/8× already proved they add nothing. Adaptive only.
**Branch:** `tnn-native-lab` · **Dir:** `coding/reflection/speed_intel/`
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 0. Source evidence (frozen, committed)

- Speed–intel prereg: `43eceed210c73b1b065f0685644d171a5837a4a`
- Arm 1 results: `coding/reflection/speed_intel/work_a1/RESULTS_SI.md`
  (2× knee: coding 18/18, epistemic 59/94; 4×/8× add zero)
- Promotion prereg: `coding/reflection/speed_intel/PROMOTION_PREREG.md`
  (2× deliberation → mainline default)

## 1. The question, plainly

Fixed budgets are a hardcoded number. Can TNN choose its own think-count
per decision — spending extra rounds only where its own evidence says
they're needed — and match the fixed-2× knee quality at LOWER mean cost?
The empirical ceiling (max rounds the champion policy ever actually
spends) is discovered, never set.

## 2. Fixed-2× baselines (frozen; the bar to beat)

**Coding:** driver `--budget 4` → **18/18** fixable, honest-halt 2/2,
46 total iterations, 27 znc invocations (RESULTS_SI.md, the measured knee
row; the row is labeled "4x (4)" there — this prereg anchors to the
measured budget=4 row, not the label).
Mean cost: 46/20 = **2.30 iters/item**, 27/20 = 1.35 znc/item.

**Epistemic:** full pipeline (arm=2 equivalent) → **59/94** total
(false 12/12, true 12/12, weird-English 35/70), 9.000 preds/item,
0 reconsiderations fired, 0 verification flips (RESULTS_SI.md).
Mean cost: **9.000 predicate-evaluations/item**.

## 3. Round definitions (frozen)

- **Epistemic round:** round 0 = 1× pass (world-knowledge checks only:
  steps 1,2,4,5, no speech-act matchers); round 1 = full pipeline (2×);
  round 2+ = reconsideration rounds; verification pass counts as a round
  when run. Mean rounds/item and max rounds/item are recorded.
- **Coding round:** one driver iteration (gen → compile → diagnose →
  repair). The learner's existing stop judgments (success / honest halt)
  are untouched; adaptive policies modulate the per-item budget the
  learner requests and the driver's grant, subject to a hard cap.

## 4. Candidate policies (frozen intents; exact operationalizations in §4.1)

(a) **stop-at-unanimity** — halt when all markers agree after a round.
(b) **stop-at-verification-agreement** — run the independent verification
    pass; halt when it agrees with the verdict; otherwise reconsider.
(c) **stop-at-diminishing-evidence** — halt when a round adds no new
    pro/con markers (epistemic) / no new diagnostic information vs the
    previous iteration (coding).
(d) **uncertainty-routed** — spend extra rounds ONLY on items the
    learner's own signals flag as non-unanimous or verification-disagreed;
    minimum rounds elsewhere (epistemic: round 0 first, escalate on the
    learner's own ambiguity signals; coding: per-item requested budget).
(e) **cost-capped adaptive** — policies (a)–(d) each under a hard cap
    (epistemic: 8 rounds; coding: 16 iterations). A cap is a safety bound,
    not a think-count: the policy still chooses every round below it.

**Test-both / maximize:** arms may add further policies if cheap
(e.g. combinations like d+e, unanimity-or-verification). Every added
policy is named and frozen in the arm addendum before results.

### 4.1 Operationalization freeze (required, before any trial run)

Each arm writes `OPER_SPEC_ADAPTIVE.md` (committed) specifying, in full:
the exact stop/continue/escalate predicates, what the learner's own
signals are (no label-peeking: routing criteria may use only information
available to the learner at decision time), the binary variants built
(control = byte-identical frozen learner/deliberator; adaptive variants
separate), and the driver invocation per cell. No trial run starts before
its arm's OPER_SPEC is committed.

## 5. Batteries (frozen)

- **Frozen originals (primary):** coding `work_a1/battery_si.json`
  (20 items: S01–S12 repair, G05–G10 gen, X3/X4 unfixable);
  epistemic frozen 94 via `work_a1/epi/` copies
  (`b12_false.txt`, `b12_true.txt`, `c70.txt`).
- **Fresh disjoint items (secondary, anti-overfit):** each arm builds and
  commits its own fresh battery BEFORE results — epistemic ≥40 new items
  in the same 7-family discipline (new content, new SHAs); coding ≥10 new
  items in the same construction discipline (new seeds, new SHAs, reference
  paths recorded, never exposed). Disjoint from the frozen originals AND
  from the SI-Arm-1 extended crew's items by independent construction
  (their item lists are committed separately; accidental overlap is
  checked by SHA at analysis time and reported).
- **3 reruns per cell; canonical logs (timing-free) byte-identical.**

## 6. Metrics (per policy × battery)

Quality: Q_c /18 (+honest-halt 2/2) coding; total /94 + per-family /12,
/12, /70 epistemic. Cost: mean rounds/item, FULL rounds distribution
(histogram), max rounds/item, total iterations/znc (coding),
mean preds/item (epistemic), wall-clock. Determinism: canonical digest.

## 7. Ceiling discovery (required deliverable)

Per policy per domain: the empirical ceiling = max rounds the policy
ever actually spent, on how many items (count + fraction), and which
items (IDs). "The best number for now" is read off the ceiling, not set.

## 8. Kill bars (frozen)

- **WIN:** quality ≥ fixed-2× baseline (§2) AND mean cost < fixed-2×
  mean cost, on the frozen originals. Both must hold.
- **FAIL:** (i) mean cost ≥ fixed-2× for equal quality; (ii) quality
  degrades anywhere (any per-family drop epistemic; any item-class drop
  or honest-halt failure coding); (iii) non-determinism across reruns.
- **PARTIAL:** wins on one domain only.
- Secondary (reported, not decisive): cost per quality point; fresh-item
  battery replication of the verdict.

## 9. Deliverable

`ADAPTIVE_VERDICT.md`: the policy×battery quality/cost table, the rounds
histograms, the discovered ceiling per policy, the champion policy (or
champion combination, or NONE — "no adaptive policy beats fixed-2×" is
an allowed verdict), and the recommendation for mainline defaults.

## 10. Standing laws

Zero RNG anywhere in decision paths. Byte-identical reruns. Pure Zag for
anything reasoning or verifying; Python is glue only (drivers, analysis,
commits). No binaries or `.zagd` caches committed. Commits via
`~/workspace/commit_racefree.py` from `~/workspace/tnn-lab`,
`TMPDIR=~/workspace/tmp_commit`, lab-relative paths.
