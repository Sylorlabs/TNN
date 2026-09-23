# SPEED–INTELLIGENCE TRADEOFF — FROZEN PREREGISTRATION

**Date frozen:** 2026-09-22 · **Order:** Micah — "can we trade speed for
intelligence somehow or get free intelligence or free speed?" — as EXPERIMENTS,
not opinions (standing test-both law).
**Branch:** `tnn-native-lab` · **Dir:** `coding/reflection/speed_intel/`
**Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## 0. The question, plainly

Three sub-questions, each with its own arm and its own frozen bar:

1. **Buying intelligence with speed** (Arm 1): give the learner more
   deliberation budget per decision — does quality rise, where does it stop
   rising, and what does each quality point cost?
2. **Free intelligence** (Arm 2): mechanisms that raise quality at same-or-lower
   cost, or hold quality at strictly lower cost.
3. **Free speed** (Arm 3): mechanisms that cut cost ≥20% while quality stays
   within ±1pp.

Arm 4 combines the winners and reports the exchange rate.

## 1. Substrates (frozen, reused verbatim)

- **Coding loop:** `coding/reflection/loop/learner.zag` →
  `coding/reflection/loop/work/learner`, driven by
  `coding/reflection/loop/driver.py --budget N` (INTERFACE.md is the law:
  every coding decision lives in the learner; the driver is plumbing).
- **KB:** `coding/reflection/kb/data/entries.txt` (69 entries, `K:` keyword
  lines), recall via `coding/reflection/kb/src/kb_main.zag` on the frozen
  24-spec battery (`kb/tests/specs.txt`), scored as in RECALL_RESULTS.md.
- **Epistemic deliberator:** `prose-learning/epistemic_wave/speechact_exp/delib_sa.zag`
  (arm=2 pipeline), on the frozen 94-item set from the speech-act
  proof-of-concept: 12 planted falsehoods + 12 true controls + 70 weird-English
  items, byte-identical to the committed materials.

**TNN-native note (Micah's standing correction):** the mechanisms under test
(indexing, memoization, fast paths, pruning, branch-and-bound, precheck) are
*experimental treatments* built as harness variants. Every deliberative
decision — what to generate, how to classify a failure, which repair to
attempt, when to halt — remains the learner's. This experiment measures the
learner's speed–intelligence curve; no crew-authored architecture content
participates in any decision under measurement.

**Knowledge-first:** the 69-entry KB is installed (taught) before every coding
and KB task; the speech-act knowledge is installed before every epistemic run.
No arm runs knowledge-free.

## 2. Cost baseline (frozen, from `loop/RESULTS.md`)

- 5,000–11,000 iterations/hour (mix/load dependent)
- median 0.89s to first working build (passed items)
- 46.7% defect rate per iteration; 22.2% first-attempt rate
- deliberation (`diagnose` invoke) 5.5ms — <1% of iteration cost; successful
  znc codegen (~825ms) dominates; failed compiles fail fast (~19.5ms)
- budget sweep on the v1 battery: budgets 3/6/12 all 16/18 — flat. (This is
  WHY Arm 1 uses a harder battery: the v1 battery saturates too early to
  measure a curve.)

## 3. ARM 1 — buying intelligence with speed

### 3a. Coding battery SI (`battery_si.json`, frozen at build)

20 items, all new (no overlap with v1 battery):
- 12 multi-defect repair seeds: 2–3 defects each (drawn from the learner's
  known classes: SYNTAX, NAME, ARITY, TYPE, DUPFN, OUTPUT_FORMAT, LOGIC_VALUE),
  each requiring 3–5 deliberate iterations. Seeds must compile-fail or
  test-fail initially; the reference repair path is recorded but NOT given to
  the learner.
- 6 harder gen items: T4 novel write-from-spec, each needing ≥2 KB patterns
  composed (single-pattern items are excluded — they saturate at 1x).
- 2 unfixable-by-design (one ungenable spec → expect `halt-genfail`; one
  unrepairable defect → expect `halt-no-patch`/`halt-unknown`).

### 3b. Budgets

Driver `--budget`: **1x=2, 2x=4, 4x=8, 8x=16** iterations. (1x sits below the
v1 knee of 3; 8x=16 exceeds the deepest reference repair path.)

### 3c. Metrics (per budget level, 3 reruns, canonical logs byte-identical)

- Q_c = pass rate on the 18 fixable items
- first-attempt pass rate; honest-halt rate = correct halts on the 2
  unfixable / 2 (must be 2/2 at every budget — a budget that "fixes" an
  unfixable item by fabrication is a FAIL of that budget level)
- cost: total iterations, total znc invocations, total wall-clock
- **cost per quality point** = total znc invocations / (Q_c in pp)

### 3d. Epistemic slice (deliberation-depth budgets on `delib_sa`, arm=2)

Budget = deliberative work per item, implemented as `delib_si.zag`
(copy of `delib_sa.zag`, pipeline stages unchanged):
- **1x:** world-knowledge checks only (steps 1, 2, 4, 5 — no speech-act matchers)
- **2x:** full pipeline (1x + all 6 speech-act matchers)
- **4x:** 2x + one reconsideration round on non-unanimous items (≥1 matcher
  fired AND ≥1 counter-marker present): count pro/con marker evidence,
  majority wins, ties keep the 2x verdict
- **8x:** 4x + independent verification pass on every item: re-derive the
  verdict from the evidence ledger through an independent code path;
  disagreement → verdict=withhold, counted as a verification-flip

Metrics: per-family score (7 families × 10) and total /94; cost = mean
predicate evaluations per item. Cost per quality point = total predicate
evaluations / (Q_e in pp).

### 3e. Knee hypothesis (PREREGISTERED)

Diminishing returns with the knee in **2x–4x**: marginal Q gain 4x→8x <
marginal Q gain 2x→4x, and the 8x gain over 4x ≈ 0 (≤1pp). Cost per quality
point is minimized at or before the knee. **Verdict rule:** PASS if the
measured curve satisfies both clauses on coding AND epistemic; PARTIAL if on
one domain only; FAIL if quality keeps rising substantially through 8x
(no knee in range) or never rises (no trade exists to measure).

## 4. ARM 2 — free intelligence

Frozen bar for every "free" claim: **ΔQ ≥ 0 AND ΔC < 0**, determinism
preserved (3 reruns byte-identical). Quality-equal + cost-down PASSES
(that is the free lunch: same intelligence, cheaper). Quality-up + cost-equal
also PASSES. Anything else FAILS the claim.

### 4a. KB-indexed recall vs flat store

- FLAT (baseline): `kb_main.zag` as-is — score all 69 entries per spec.
- INDEXED: build an inverted index (keyword → entry list) once at install
  (deterministic; install digest must remain byte-identical modulo the index
  artifact); per spec, score ONLY entries reachable via the spec's keywords;
  identical scoring function, identical tie-break.
- Quality: family selections on all 24 specs must be **byte-identical**
  (prove it — diff the selection logs). Cost: mean entries scored per spec;
  must be strictly lower. Report one-time index-build cost and the break-even
  query count.

### 4b. Deliberation memoization

- Substrate: fast-loop `diagnose`. Memo key = (item id, evtype, structural
  evidence signature: the fixed reason-string multiset the trace logs — NOT
  raw evidence bytes). Table persists across the battery run.
- On hit: reuse the cached DIAG line + revised source AND **shadow-run fresh
  deliberation; byte-compare**. Any mismatch = uninstall the entry, count a
  quality defect, report it.
- Quality: battery pass rate ≥ baseline. Cost: hypothesis-evaluations +
  diagnose invocations, strictly down. Report the hit rate honestly even if
  near zero — a zero hit rate is a finding (no recurrence to exploit), not a
  failure to hide.

### 4c. Compiled fast paths

- After the same (evidence signature → class+strategy) fires **K=3** times
  (frozen), install a rule: matching signatures apply the strategy directly,
  skipping multi-hypothesis scoring. Shadow-verify the first **M=5**
  applications per rule against full deliberation; mismatch → uninstall +
  quality defect.
- Quality: pass rate ≥ baseline on the SI battery. Cost: hypothesis-
  evaluations strictly down. Determinism: installation order is a pure
  function of (K, battery order) — 3 reruns identical.

## 5. ARM 3 — free speed

Frozen bar: **|ΔQ| ≤ 1pp AND cost down ≥ 20%**. Cost = znc invocations
(primary — the dominant wall-clock) and total iterations; both reported,
znc invocations is the bar.

### 5a. Prune provably-dead deliberation branches

In `diagnose`, before scoring: compute per-class trigger presence from the
evidence envelope (e.g. NAME requires an unknown-identifier token in stderr;
SYNTAX requires a parse-error marker). Skip scoring classes with absent
triggers. **"Provably" is load-bearing:** the crew must demonstrate from the
scoring code that each pruned class's score is deterministically 0 without
its trigger (cite the trace's own refutation logs, e.g.
`NAME+0:named-is-defined-conflict`). Any class where trigger-necessity cannot
be shown is NOT pruned.
- Quality: argmax winner byte-identical on every diagnose call in the SI
  battery (prove by diff). Cost: hypothesis-evaluations down ≥20%.

### 5b. One-brain parallel deliberation (shared-ledger branch-and-bound)

Sub-deliberations (per-class scoring) share one ledger: evaluate classes in
fixed descending historical win-rate order (from `loop/RESULTS.md`: TYPE,
NAME, ARITY, SYNTAX, DUPFN, OUTPUT_FORMAT, LOGIC_VALUE, GEN_FAILURE,
RUNTIME, LOGIC_OTHER, UNKNOWN); as soon as a class's score exceeds the
theoretical maximum of all remaining classes, stop — the winner is decided.
Ties still break by the frozen priority order
(SYNTAX > DUPFN > NAME > ARITY > TYPE > UNKNOWN) regardless of evaluation
order (prove: rerun the SI battery, winners byte-identical).
- Quality: winners identical (diff-proof). Cost: hypothesis-evaluations down
  ≥20%. **Honest note:** the znc substrate here is single-threaded, so this
  measures saved evaluations (cycles), not wall-clock parallelism; wall-clock
  parallelism is reported as not-available-on-this-substrate, not claimed.

### 5c. Fail-fast precheck

New learner mode `precheck <spec> <src>`: the learner applies its own
knowledge (brace balance, defined-name check, arity-vs-definition — the same
cross-checks `diagnose` uses) and predicts COMPILE-FAIL with a reason, or
predicts compile-ok. Driver routes predicted-failures straight to
`diagnose` with evtype=PRECHECK, skipping the znc invocation. (Learner
decides; driver is plumbing — the INTERFACE.md law holds.)
- Quality: pass rate within ±1pp on the SI battery; every precheck-FAIL on a
  source that would have compiled is logged as a false positive and counts
  against quality. Cost: znc invocations down ≥20%.

## 6. ARM 4 — the exchange rate

At the knee budget from Arm 1, apply the Arm 2 and Arm 3 mechanisms that
PASSED their bars (integrated into one build; if two winners interact, the
combination is re-run and re-verified, not assumed). Report:

| budget × mechanism | Q_c | Q_e | iters | znc invocations | pred-evals/item |
|---|---|---|---|---|---|
| 1x baseline | | | | | |
| knee baseline | | | | | |
| knee + each winner alone | | | | | |
| knee + all winners | | | | | |

Then answer in plain language: **is there a real trade** (does buying
deliberation buy quality, to a knee)? **is there any free lunch** (which
mechanism, how big, with what proof)? No hype: a mechanism that passes its
bar by 21% cost reduction is "21%", not "massive".

## 7. Cross-cutting laws (all arms)

- Zero RNG in any decision path; 3 reruns byte-identical canonical logs
  (reuse `loop/measure.py` semantics).
- No gate weakening: the 6/6 gate battery from the KB work re-run per arm;
  any wrong REFUSE/ALLOW = arm FAIL.
- Honest halts stay honest: a mechanism that converts a correct halt into a
  fabricated pass fails its quality bar automatically.
- Determinism digests drop wall-clock timings (canonical form, as in
  INTERFACE.md).
- Pure Zag for learner/deliberator changes; driver changes are plumbing only
  (no error classification, no repair choice, no verdict logic in Python —
  verify by grep as INTERFACE.md requires).

## 8. Kill criteria (per arm)

- Arm 1: FAIL if no knee in 1x–8x (quality flat from 1x, or still rising
  steeply at 8x). PARTIAL if the knee appears in one domain only.
- Arm 2: each mechanism judged against §4's bar independently. A mechanism
  that reduces cost but changes ANY selection/winner (quality not equal) and
  cannot prove the change is an improvement on a frozen oracle FAILS.
- Arm 3: each mechanism judged against §5's bar independently.
- Arm 4: if no Arm 2/3 mechanism passed, Arm 4 reports the knee table only,
  honestly.

## 9. Honest limits (declared before results)

- The SI coding battery is 20 items; multi-defect seeds are still synthetic.
  Real-world code repair is unmeasured.
- The epistemic 4x/8x reconsideration and verification passes are
  crew-designed deliberation structure (the matchers themselves are the
  pre-existing hand-specified ones). The experiment measures the
  budget–quality curve of deliberation, not the origin of the knowledge.
- Single-threaded substrate: "parallel" in 5b means saved evaluations.
- Memoization (4b) is expected to show a low hit rate on a diverse battery;
  the bar does not require a high one — it requires honesty about it.

## 10. Deliverables

1. This prereg (committed BEFORE any result is generated).
2. `battery_si.json` + `delib_si.zag` + variant learners/drivers
   (`learner_si2.zag`, `learner_si3.zag`, `driver_si.py`, `kb_main_si.zag`
   — originals untouched).
3. Tradeoff curves as tables (Arm 1), per-mechanism verdict tables
   (Arms 2, 3), exchange-rate table (Arm 4).
4. All canonical logs + determinism digests.
5. Commit to `sylorlabs/TNN`, branch `tnn-native-lab`, under
   `coding/reflection/speed_intel/` (lab-relative paths); verify via GitHub
   API; report head SHA.
