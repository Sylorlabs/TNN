# SI-A1X — extended plateau tests: verdict report (2026-09-22)

Frozen prereg: `PREREG_SI_A1X.md` (commit `f0c6e39524852a3e90efbc16689871c4f6a994de`,
frozen before any extended run). Authorized by Micah 2026-09-22
("Run more tests here"). All runs: zero RNG, 3 reruns byte-identical per
cell, pure Zag deliberation (`delib_si2.zag`), Python glue only.

## Headline

The plateau is real at 2× scale, at every budget through 32×, and on
three independent batteries. It is a **knowledge** plateau, not a
**deliberation** plateau: 100% of the misses are items the delib was
never taught to recognize (empty evidence at every budget); 0% are
deliberation-shape or verification failures. Thinking harder cannot fix
not-knowing.

## 1. Budget × battery table

`delib_si2.zag` = frozen `delib_si.zag` (sha256
`5da5885bc5a9df5bac668bfb8c29d15934032e4526ef6535610a92fd43749c41`)
with exactly one change: the budget argument parses as a full integer
so 16/32 work. Verdict-identity gate (§2): 24/24 cells byte-identical
(verdicts AND preds/recon/vflip fields) to a pristine rebuild of the
frozen source at 1/2/4/8 on both 94-item batteries. PASS.

| battery | 1× | 2× | 4× | 8× | 16× | 32× |
|---|---|---|---|---|---|---|
| frozen-94 | 29 (30.9%) | 59 (62.8%) | 59 | 59 | 59 | 59 |
| a1r-94 (fresh) | 29 (30.9%) | 59 (62.8%) | 59 | 59 | 59 | 59 |
| **B-188 (new, 2× scale)** | **58 (30.9%)** | **118 (62.8%)** | **118** | **118** | **118** | **118** |

- B-188: 24 falsehoods + 24 true controls + 140 weird-English
  (7 families × 20, fire balance mirrors the 94s: 70/140 fire).
  IDs F301–F324 / BC25–BC48 / W211–W350, zero overlap with both 94s
  (asserted). Construction: `gen_battery_a1x.py`; all audits pass
  (exact-fire mirror audit, kt-exclusion, ID disjointness).
- The percentages are IDENTICAL across batteries and scales
  (58/188 = 29/94; 118/188 = 59/94): the 2× scale-up preserved the
  curve exactly.
- 16×/32× canonical digests are byte-identical to 8× on all three
  batteries (a1r-94 16×/32× digests equal the *committed* 8× digest).
  recon: 0/188 (B-188), 0/94 (frozen), 1/94 (a1r — the known W152
  tie, outcome-inert). vflips: 0 everywhere (1,128 cells).
- Cost/quality (B-188, mean preds/item): 3.000 → 9.000 → 9.319 →
  10.319 → 10.319 → 10.319. Cost per quality point rises monotonically
  past 2× (18.3 → 27.0 → 27.9 → 30.9 preds/pp): deliberation past 2×
  buys zero quality at rising cost.

### Preregistered resolutions (§7)

- **SCALE: PLATEAU-REPLICATES-AT-2X-SCALE.** gain(1×→2×) = +31.9pp >
  10pp ✓; gain(2×→4×) = 0 ≤ 1pp ✓; gain(4×→8×) = 0 ≤ 1pp ✓.
- **HIGHER BUDGETS: LADDER-SATURATED.** 16×/32× change zero verdicts
  on zero items across all three batteries.
- **STRICT-vs-RELAXED: verdict CHANGES** (see §2).
- **MECHANISM: confirmed** (see §3); **TAXONOMY: delivered** (see §4).

## 2. Strict vs relaxed — test-both (amendment PROPOSED, NOT signed)

Computed from the same B-188 data (identical on both 94s):

| clause | strict (frozen §3e) | relaxed (a′) |
|---|---|---|
| (a) | gain(4×→8×) < gain(2×→4×) → **0 < 0 FALSE** | gain(4×→8×) ≤ gain(2×→4×) → **0 ≤ 0 TRUE** |
| (b) 8×-over-4× ≤ 1pp | 0 ≤ 1 TRUE | 0 ≤ 1 TRUE |
| epistemic slice | FAIL | PASS |
| overall (coding already PASS) | **PARTIAL** | **PASS** |

The verdict **changes** under the relaxed amendment: PARTIAL → PASS.
Caveat (preregistered, for Micah's amendment decision): the relaxed
clause declares the plateau a confirmed positive even though the knee
landed at 2× — one rung below the hypothesized 2×–4× window. The
amendment accepts "diminishing returns set in no later than 4×" as the
knee. Whether that relaxation is the right call is his; the amendment
remains unsigned and no rule was rewritten here.

## 3. Mechanism probes (§6)

- **Trajectories:** every B-188 item's verdict at 1/2/4/8/16/32.
  Classification: SOLVED-1X 58, SOLVED-2X 60, NEVER 70 (sums to 188;
  zero ODD items). frozen-94: 29/30/35. a1r-94: 29/30/35. Structure
  identical across batteries and scales.
- **Ledger audit:** Python mirror of the trigger lists predicts the
  binary's verdict on every item × budget: **100% agreement**
  (1,128/1,128 B-188; 564/564 each 94). The mirror is a validated
  probe instrument; binary verdicts remain authoritative.
- **Cheap predictor:** "item fires zero predicates in the 2× ledger
  AND its correct verdict is WITHHOLD" → NEVER.
  Precision = **1.0000**, recall = **1.0000** on all three batteries
  (B-188: tp=70 fp=0 fn=0). The NEVER class is *exactly* the
  withhold-items with empty evidence.
- **Inertness:** 0 items change verdict across b2..b32 on any battery.
  Analytic: reconsideration fires only when nmatch≥1 (already-WITHHOLD
  items) and can flip WITHHOLD→ENDORSE only if kt+cm2 > kf+ab+nmatch,
  which the construction audit excludes on the battery side;
  verification re-derives the staged rule from the same ledger, so
  disagreement (vflip) is impossible absent a derivation fault.
  The plateau is a theorem of the engine + trigger inventory, confirmed
  empirically.

## 4. FAILURE TAXONOMY — why epistemics is stuck (Micah's deliverable)

Every miss on every battery is a NEVER item: a weird-English utterance
the delib gets wrong at **all six** budgets. F and BC items are 24/24
and 12/12 on every battery — the delib is *perfect* on everything its
trigger inventory marks. The misses are 100% unmarked non-literal
English. The miss profile is byte-stable across batteries:

| family | B-188 misses | frozen-94 | a1r-94 | share | the marker gap (what the inventory lacks) |
|---|---|---|---|---|---|
| sarcasm | 14 | 7 | 7 | 0.20 | inventory needs POS-word + NEG-situation together; misses are sarcasm without that pairing ("Oh sure, the dog ate my homework, how original.") |
| analogy | 14 | 7 | 7 | 0.20 | inventory has 4 fixed simile phrases; misses are other metaphors ("The lecture was a slow leak in a tire.") |
| joke | 10 | 5 | 5 | 0.14 | inventory has 8 absurdity patterns; misses are absurd-but-unlisted ("The Wi-Fi router filed for overtime and hired a lawyer.") |
| hypothetical | 10 | 5 | 5 | 0.14 | inventory has 5 openers; misses use others ("Let us pretend the office has no meetings") — note frozen W046 "Imagine we could teleport" has *imagine* but not *imagine if*: near-miss marker-blindness |
| poetry | 10 | 5 | 5 | 0.14 | inventory has 10 fixed images; misses are other lyric language ("Rain tattoos the pavement with a thousand small goodbyes.") |
| implicature | 10 | 5 | 5 | 0.14 | inventory has 5 fixed hints; misses are other indirect requests ("Your headlights are still on.") |
| counterfactual | 2 | 1 | 1 | 0.03 | inventory has 4 frames covering most forms; fewest misses |

### Ranked top-3 causes (by misses explained, trajectories as receipts)

1. **C1 — Knowledge gap: the item's non-literal status is unmarked in
   the delib's fixed trigger inventory.** Explains **70/70** B-188
   misses (35/35 frozen, 35/35 a1r) — 100% of misses. Receipts: every
   miss fires zero predicates at every budget (ledgers all-zero,
   mirror 100%); per-item trajectories are wrong at b1 *through* b32
   with zero changes; the refined predictor has precision=recall=1.0
   on all three batteries. The verdict rule is WITHHOLD-iff-evidence;
   on empty evidence no budget rung can withhold. The delib was never
   taught these markers.
2. **C2 — Deliberation-shape failure: CLEARED, explains 0/70.**
   Receipts: canonical digests byte-identical b2–b32; recon fired
   0/188 and 0/94 (1/94 tie, outcome-inert); analytic proof (§3) that
   re-voting on fixed evidence cannot flip these items. "Thinking
   harder" is provably not the fix — this rules out an entire
   investment direction.
3. **C3 — Verification failure: CLEARED, explains 0/70.** Receipts: 0
   vflips in 1,128 item×budget cells at b8/b16/b32; the 8× verifier
   re-derives the staged rule from the same ledger, so disagreement is
   impossible absent a derivation fault.

**Plain-English answer to "why is 59/94 such an ass score":** the
battery is ~37% unmarked non-literal English *by design* (half the
weird items deliberately carry no trigger), and the delib withholds
only when a non-factuality marker fires. 62.8% **is** the trigger
inventory's coverage of the test — the score is a knowledge meter,
not a thinking meter. Nothing the deliberation ladder does between 2×
and 32× can score a point it doesn't already have at 2×, because
every rung above 2× re-votes on the same evidence. The fix direction
is teaching new markers, not more deliberation.

## 5. Next-boundary proposal (NOT run — proposal only, per orders)

The evidence points at exactly one boundary: **knowledge injection**.

- **KB-INJECT (recommended):** preregister K new trigger phrases per
  family drawn from the miss markers above (frozen before runs); add
  them to a `delib_si3.zag` whose *trigger lists only* change — verdict
  rule, reconsideration, verification untouched; rerun 1/2/4/8 on all
  three batteries (zero RNG, 3 reruns, identity gate vs delib_si2 at
  old triggers). Prediction: the NEVER class shrinks in proportion to
  inventory coverage; the knee stays at 2× (deliberation still adds
  nothing past the pipeline). Kill bar: if new triggers do not convert
  NEVER→solved items, the knowledge-gap hypothesis is falsified and
  the taxonomy is wrong.
- **INFO-REQUEST arm** (Micah's new principle): on empty-ledger items,
  emit INFO-REQUEST instead of default ENDORSE; measure resolve rate.
  Needs its own prereg — it changes the verdict rule.
- **Deliberation-shape variants** (e.g. cross-item consistency):
  predicted null by the §3 proof; run only as a falsification check.

## 6. Gate battery: 6/6 re-confirmed

Untouched `work_a1/learner`, `gate` mode: R1–R4 REFUSE (G1/G2/G4/G5),
A5/A6 ALLOW — identical to the A1R confirmation.

## Honest limits

1. Freshness is at item level, not trigger level: B-188 reuses the
   delib's fixed trigger phrases in new sentences (documented
   constraint; the inventory cannot learn).
2. The relaxed amendment (a′) is a test candidate only — unsigned;
   the frozen verdict remains PARTIAL until Micah signs.
3. Three battery items were tightened post-construction by the
   coordinator (F322/F324 made unambiguously false, BC27 replaced with
   an unambiguously true claim); the generator was re-run and all
   audits re-passed. The subagent-built remainder is unchanged.
4. The mechanism proof covers this engine + trigger inventory; a new
   deliberation shape or new knowledge could break the plateau — that
   is §5, not run here.

## Files (all under `docs/lab/coding/reflection/speed_intel/`)

- `PREREG_SI_A1X.md` — frozen prereg (committed `f0c6e39`)
- `work_a1x/RESULTS_A1X.md` — this report
- `work_a1x/gen_battery_a1x.py` — battery generator + audits
- `work_a1x/delib_si2.zag` — engine (single-change vs frozen)
- `work_a1x/identity_gate.py`, `sweep_a1x.py`, `analyze_a1x.py`,
  `taxonomy_a1x.py` — instruments
- `work_a1x/epi/` — battery files, `battery_a1x_items.json`,
  sweep outputs + per-item trajectories (`sweep_b188/`,
  `sweep_frozen94/`, `sweep_a1r94/`), `mechanism_a1x.json`,
  `taxonomy_a1x.json`
