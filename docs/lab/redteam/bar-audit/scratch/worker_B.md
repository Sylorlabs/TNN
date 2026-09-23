# BAR-SENSITIVITY AUDIT — Worker B (red-team)

Date: 2026-09-21/22. Batteries: scale/, scale/params/, scale/fewshot/,
self-test/, noisy-teacher series (q1n-noisy-teacher/, tq-noisy25/, q1tq-noisy50/).

Method: every preregistered bar listed with exact threshold + file/section
citation; measured value from the verdict; margin computed; classified
TIGHT (<2×) / COMFORTABLE (2–10×) / TRIPWIRE (>10× slack). Headline results
with no bar get a retroactive bar proposal + pass/fail evaluation.
HONEST-FAIL marks results that fail a reasonable bar.

---

## 1. BAR TABLE

| Battery | Bar (prereg threshold) | Measured | Margin (ratio + absolute) | Classification | Tightened proposal | Notes |
|---|---|---|---|---|---|---|
| scale/ | KB-SCALING: trip iff M-mastery drops >2pp below S0 baseline (PREREG.md §"Kill bars (frozen)") | 0.00pp drop at every scale point (VERDICT.md §"Kill bars"; clean mastery 1.0000 at all 7 points) | ratio ∞ (measured 0); absolute slack = 2.00pp | TRIPWIRE | Trip iff drop > **0.25pp** (8× tighter). Why: measurement is exact deterministic counts with zero variance across 7 scale points × up-to-5 reps — the 2pp allowance was built for noisy statistical learners and doesn't apply. 0.25pp still tolerates ~15,600 wrong facts at 6.58M scale, a generous ceiling for a "no degradation" claim. | At N=6,585,360 the current bar tolerates **125,137 wrong facts** before tripping. The "no degradation" headline rests on a bar that permits city-scale corruption. |
| scale/ | KB-FORGET: trip iff last-decile − first-decile mastery >3pp (PREREG.md §"Kill bars (frozen)") | 0.00pp gap at every scale (VERDICT.md §"Catastrophic forgetting (KB-FORGET)"; all deciles 1.0) | ratio ∞ (measured 0); absolute slack = 3.00pp | TRIPWIRE | Trip iff gap > **0.5pp** (6× tighter). Why: same determinism argument as KB-SCALING; horizon gaps compound across deciles so the bar should sit closer to the observed 0. | 3pp at max scale = ~187,700 forgotten early facts allowed. |
| scale/ | KB-COST: trip iff S2 ops/fact > 1.5× S1, or S3 > 1.5× S2 (PREREG.md §"Kill bars (frozen)") | ratio exactly 1.000 (4.000/4.000 at every N≥2,400; 4.004 at S0 = one amortized audit entry) (VERDICT.md §"Scale laws") | 1.5/1.0 = **1.5×**; absolute slack = 0.50 ratio-points (6.0 − 4.0 ops/fact) | TIGHT | Trip iff ratio > **1.15×** consecutive scale points. Why: ops are exactly counted, not sampled; observed amortization drift was 4.004/4.000 = 1.001, so 15% headroom is 150× the observed drift while catching real superlinearity far earlier than 1.5×. | Tightest numeric bar in the battery. Genuinely mechanical. |
| scale/ | KB-DETERMINISM: trip iff any rep differs byte-wise (PREREG.md §"Kill bars (frozen)") | 0 diffs: 5/5 byte-identical (S0–S2), 3/3 (S3), single runs S4 (VERDICT.md §"Scale laws", Reps column) | zero slack by construction (threshold = 0, measured = 0) | TIGHT | None possible — already zero-slack. | Strongest bar in the set. Note S4 stretch reps are single runs (caveated in VERDICT.md §"Caveats"). |
| scale/ | KB-FLAW: trip iff M-flaw pass rate < 7/8 slices (PREREG.md §"Kill bars (frozen)") | 8/8 slices at 12/12 = 96/96 at every scale (VERDICT.md §"Scale laws") | 8/7 = **1.14×**; absolute slack = 1 slice | TIGHT | Require **8/8 slices** pass (drop the 1-slice allowance); keep per-slice bar at ≥10/12. Why: measured 8/8 at all 7 scale points with zero variance — the 7/8 allowance was for flaky instruments; this one isn't flaky. | Probe-level slack is larger than it looks: 7/8 slices × 10/12 hits = **70/96 (72.9%)** could still pass the bar. Measured 96/96, so no failure — but the bar's floor is far below the headline. |
| scale/params/ | KB-P-DET: any config with non-byte-identical reps → HALT (PARAM_PREREG.md §4) | 19/19 configs, 59/59 runs byte-identical (PARAM_VERDICT.md §"Kill bars") | zero slack | TIGHT | None possible. | — |
| scale/params/ | KB-P-EFF: ≥2× cost with <1pp mastery gain = efficiency-dead, report no halt (PARAM_PREREG.md §4) | Fired as designed: slot4, slot8, audit4, red4, jbig flagged dead (PARAM_VERDICT.md §"Kill bars") | n/a — classification rule, applied correctly | APPLIED AS DESIGNED | Flag at **≥1.5× cost with <0.5pp gain**. Why: measured gain above 1× is exactly 0pp everywhere, so any cost multiplier >1 is pure waste; 1.5× keeps headroom for chunk-granularity noise. Would additionally flag red2 (ops 6.0/4.0 = 1.5×, B/fact 358/202 = 1.77×) and audit2 (B/fact 333/202 = 1.65×) — both currently pass while buying nothing. | The bar works. The tightening catches two more zero-gain configs the current bar lets through. |
| scale/params/ | KB-P-EMERGE: absorption < 1.0 at any config → EMERGENT flag (PARAM_PREREG.md §4) | Fired on slot025 (292/1159 = 0.252), slot05 (586/1159 = 0.506), jsmall — then **cleared on inspection**: "the shortfall is untaught facts (capacity drops), not truth-detection. Every *taught* falsehood absorbed 1.0 at every config (292/292, 586/586)" (PARAM_VERDICT.md §"Kill bars") | n/a — fired, but on the wrong partition | MISCALIBRATED (not slack) | Repartition: flag iff **taught-falsehood absorption < 1.0** (taught = ids with slots), plus separate KB-P-DROP-REPORT requiring dropped-fact counts per config. Why: the bar's letter fires on a known-benign cause (capacity drops lose untaught facts) and the "clearance" was a discretionary analyst judgment overriding a mechanical bar. Repartitioned, the flag would not have fired (taught absorption = 1.0 everywhere) and no discretion would have been needed. | A bar that fires-then-requires-human-clearance is a bar with a hole in it. The verdict documents the clearance honestly — but the mechanism should not need it. |
| scale/params/ | KB-P-GRACE: at SLOT_MULT=0.5, clean mastery over the *taught* subset must remain 1.0 (PARAM_PREREG.md §4) | 1.0 at 0.5× and also at 0.25× slots (PARAM_VERDICT.md §"Kill bars"; per-config table: 5708/22841 = 0.2499 overall, taught subset 1.0) | zero slack (exact-equality bar, measured exactly) | TIGHT | Extend the bar's stated scope to 0.25× (already measured — free). Otherwise none. | Exact bar on the exact right partition. The one bar in this battery with no slack and no calibration issue. |
| scale/fewshot/ | *(none — PREREG.md §"Decision rules": "No kill bars: this is a floor-finding measurement")* | n/a | n/a | NO BARS PREREGISTERED | See §2 — every headline below needs a retroactive bar. | A whole battery with zero kill bars means every headline ("no floor", "one-shot works", "96/96") is bar-free by design. That is the finding. |
| self-test/ | KB-ST-AUTO: one process, zero external orchestration (SELFTEST_PREREG.md §"Kill bars") | HOLD — single run output contains verdict for every manifest battery (SELFTEST_VERDICT.md §"Kill bars") | zero slack (structural boolean) | TIGHT | None. | — |
| self-test/ | KB-ST-SKIP: any battery without a verdict = FAIL; B5 must appear as UNRUNNABLE (SELFTEST_PREREG.md §"Kill bars") | HOLD — B5=UNRUNNABLE ×5 (s1), ×50 (s10) (SELFTEST_VERDICT.md §"Kill bars") | zero slack | TIGHT | None. | Fault-injection test (skip battery 5 → ST_BLOCKED, no ST_DONE) independently confirms the gate is live. But: only ONE fault class was injected — see §2. |
| self-test/ | KB-ST-FIDELITY: orchestrator verdict == oracle recomputation on EVERY battery incl. T1/T4 (SELFTEST_PREREG.md §"Kill bars") | HOLD — 40/40 (s1), 400/400 (s10) (SELFTEST_VERDICT.md §"Kill bars") | zero slack (exact agreement required, exact agreement observed) | TIGHT | None on the threshold — but fix the B6 gap (see §2): the oracle **asserts** B6's digest equality rather than recomputing it ("B6's digest equality is self-contained; the oracle asserts the claim" — SELFTEST_VERDICT.md §"Honest limits"). 50 of the 400 s10 verdicts are self-attested, not independently recomputed. | Genuinely the tightest bar in the audit: 400/400 exact agreement including deliberate trips. The B6 exception is disclosed, not hidden — but "independent oracle" overclaims by 50 verdicts. |
| self-test/ | KB-ST-DET: 5 reps byte-identical full output, md5 (SELFTEST_PREREG.md §"Kill bars") | HOLD — 5/5 (md5 3be14786… s1, 6ffead66… s10) (SELFTEST_VERDICT.md §"Kill bars") | zero slack | TIGHT | None. | — |
| self-test/ | KB-ST-OVERHEAD: orchestration ops ≤ 2× battery ops (SELFTEST_PREREG.md §"Kill bars") | 0.0127 (SELFTEST_VERDICT.md §"Overhead") | 2.0/0.0127 = **157×**; absolute slack = 1.9873 ratio-points | TRIPWIRE | Cap at **≤ 0.10** (10% overhead ≈ 8× measured). Why: overhead is a deterministic op-counter ratio with zero variance across reps; the 2× bar was written for an unknown orchestrator cost and the measurement came in 157× under it. A 10% ceiling is a real "lean enough to scale" claim; 200% is not a claim at all. | The canonical tripwire of this audit. The bar permits orchestration to cost **200% of the batteries**; the verdict celebrates being "157× under" a bar that was never in any danger. |
| self-test/ | KB-ST-SCALE: s10 (80 batteries) — all bars above hold (SELFTEST_PREREG.md §"Kill bars") | HOLD (SELFTEST_VERDICT.md §"Kill bars") | zero slack (structural) | TIGHT | None. | — |
| self-test/ | Manifest B1: clean ≥ 236/240 (SELFTEST_PREREG.md §"Battery manifest") | 240 (SELFTEST_VERDICT.md §"Kill bars": "B1 240 PASS") | 240/236 = **1.017×**; absolute slack = 4 facts | TIGHT | ≥ **238/240**. Why: 50 observations (5 reps × 10 salts) at exactly 240, deterministic — 2-fact headroom is generous. (T1's trip-test uses its own bar ≥240, unaffected.) | — |
| self-test/ | Manifest B2: absorbed == 12 exact (SELFTEST_PREREG.md §"Battery manifest") | 12 (SELFTEST_VERDICT.md: "B2 12 PASS") | zero slack | TIGHT | None. | — |
| self-test/ | Manifest B3: correct ≥ 92/96 (SELFTEST_PREREG.md §"Battery manifest") | 96 (SELFTEST_VERDICT.md: "B3 96 PASS") | 96/92 = **1.043×**; absolute slack = 4 probes | TIGHT | ≥ **94/96**. Why: 50 observations at 96/96, deterministic; 2-probe headroom. | — |
| self-test/ | Manifest B4: resolved ≥ 46/48 (SELFTEST_PREREG.md §"Battery manifest") | 48 (SELFTEST_VERDICT.md: "B4 48 PASS") | 48/46 = **1.043×**; absolute slack = 2 | TIGHT | ≥ **47/48**. Why: same determinism argument; 1-unit headroom. | — |
| self-test/ | Manifest B5: verdict == UNRUNNABLE (SELFTEST_PREREG.md §"Battery manifest") | UNRUNNABLE (SELFTEST_VERDICT.md: "B5 UNRUNNABLE") | zero slack | TIGHT | None. | — |
| self-test/ | Manifest B6: digests equal (SELFTEST_PREREG.md §"Battery manifest") | equal → PASS (SELFTEST_VERDICT.md: "B6 PASS") | zero slack | TIGHT | None on threshold; fix oracle independence (see KB-ST-FIDELITY note). | — |
| self-test/ | Manifest T1: clean ≥ 240, taught 239 → TRIP (SELFTEST_PREREG.md §"Battery manifest") | 239 → TRIP (SELFTEST_VERDICT.md: "T1 239 TRIP") | deliberate 1-fact trip margin — by design | TRIP-TEST (by design) | None. | Proves the adjudication path is live. |
| self-test/ | Manifest T4: resolved ≥ 48, 47 resolvable + 1 tie-withhold → TRIP (SELFTEST_PREREG.md §"Battery manifest") | 47 → TRIP (SELFTEST_VERDICT.md: "T4 47 TRIP") | deliberate 1-unit trip margin — by design | TRIP-TEST (by design) | None. | Same. |
| noisy-teacher (q1n / tq-noisy25 / q1tq-noisy50) | §B.7 slice bar ≥10/12 hits (units/PREREG_FREEZE.md §B.7 — status: **PROPOSED**, never frozen) | 12/12 on all 8 slices in every leg: q1n legs 0/1/2 (Q1N_NOISY10_VERDICT.md §"Results"), tq-noisy25 (TQ_NOISY25_VERDICT.md §"Per-slice numbers": 96/96), q1tq-noisy50 (Q1TQ_NOISY50_VERDICT.md §"Per-slice numbers": 96/96) | 12/10 = **1.2×** per slice; absolute slack = 2 hits/slice (16 hits over 8 slices) | TIGHT on ratio — **MISCALIBRATED on target** | Keep ≥10/12 for form-judgment, but it cannot govern the leg question. Add KB-TQ-MASTER + KB-TQ-FILTER (see §2). The bar's PROPOSED-not-frozen status should also be resolved: freeze it or stop citing it as "the bar". | The headline "12/12" passes this bar at **51.75% teacher noise with 51.6% of taught knowledge false** (q1tq-noisy50: 93/192 true mastery, 99/99 false claims absorbed). The bar is tight on its own terms and aimed at the wrong target: it measures proposal *form*; the leg asks about knowledge *truth*. A tight bar on the wrong instrument is worse than a loose bar — it manufactures false confidence. |

---

## 2. NO-BAR RESULTS (retroactive evaluations)

For each headline result with no preregistered bar: the bar that should have
existed (threshold + rationale), then the retroactive verdict.

### scale/ — absorption 1.0 at every scale (14/14 … 328532/328532)
- **Should-have bar (KB-SCALE-ABSORB-REPORT):** any verdict citing
  integrity-relevant scores (flaw battery, mastery) must print the
  planted-falsehood absorption count alongside; a verdict citing §B.7
  scores without the absorption triple is INVALID. Rationale: the
  noisy-teacher series proved battery scores are truth-blind, so
  absorption is the load-bearing number.
- **Retroactive: PASS.** The verdict does print absorption per scale point
  (VERDICT.md §"Scale laws", Absorption column) and carries the
  truth-preservation disclaimer in §"Caveats" ("the teacher-quality finding
  (consistent lies absorbed) reproduces at 6.5M facts"). Passes — but only
  via the caveat; the "Kill bars: none tripped" headline table would read
  as an integrity clean bill of health without it.

### scale/ — clean mastery *excludes* the 5% planted falsehoods (definitional)
- **Should-have bar (KB-EXCLUSION):** the excluded-from-mastery fraction
  must equal the prereg-registered plant rate (5%, PREREG.md §"Corpus") and
  mastery must be reported both exclusive AND inclusive.
- **Retroactive: PASS.** All-fact mastery is reported alongside
  (0.9417 → 0.9501 column). Nothing stops a future verdict from quietly
  widening the exclusion — the bar would.

### scale/params/ — flaw 96/96 at slot025/slot05/jsmall is a coverage artifact
- **Should-have bar (KB-FLAW-COVER):** flaw-battery probe ids must span the
  full taught id range of the config under test; configs where coverage <
  100% of taught ids must mark the flaw column DEGRADED, not 96/96.
- **Retroactive: HONEST-FAIL** for the three reduced-capacity configs. The
  battery samples ids in [0, n/4) only, so it is "blind to capacity loss
  beyond 4× — slot025's 96/96 is a coverage artifact"
  (PARAM_VERDICT.md §"Caveats"). The per-config table still headlines
  96/96 for those configs. The caveat discloses it; the table does not.
  **HONEST-FAIL on the table presentation.**

### scale/fewshot/ — "there is no floor", one-shot 1/1 mastery
- **Should-have bar (KB-FS-FLOOR-DENOM):** a "floor at N" headline requires
  denominator ≥ 24 at that N; N=1 results are reported as existence proofs
  with explicit 1/1 denominators, never as curve points.
- **Retroactive: PASS with restatement.** The verdict reports every
  denominator honestly (VERDICT.md §"Few-shot curve": 179/179 … 1/1), so a
  reader can see the curve's evidential weight collapse. But the headline
  "The smallest N with mastery 1.0 is N=1" invites reading 1/1 as the same
  kind of evidence as 625741/625741. Under the bar the headline becomes:
  "floor ≤ 24 (22/22 at N=24); N=1 existence proof 1/1." Same facts, weaker
  slogan — which is the point.

### scale/fewshot/ — flaw "96/96\*" below N=96
- **Should-have bar:** the verdict's own prereg rule — "families reported
  with distinct-id count and a degeneracy caveat, **not presented as a
  96-probe result**" (fewshot PREREG.md §"Measures per config").
- **Retroactive: HONEST-FAIL on presentation.** The verdict's headline
  table shows "96/96" for N=4/2/1 with a footnote, i.e. it *is* presented
  as a 96-probe result with an asterisk. Distinct-id counts at N=4/2/1: **1**
  (VERDICT.md §"Few-shot curve" footnote). The compliant form —
  "1/1 distinct × 4 checks" — appears only in the footnote gloss. The
  verdict violates the letter of its own prereg's reporting rule.

### scale/fewshot/ — one-shot falsehood absorption 1/1 (off=6), 1/1 (off=5)
- **Should-have bar (KB-FS-PAIR):** any one-shot-learning headline must pair
  with the one-shot falsehood-absorption result (same pairing rule as
  KB-SCALE-ABSORB-REPORT).
- **Retroactive: PASS.** The verdict pairs them explicitly: "The honest
  asymmetry: plants are absorbed just as completely at N=1 as at 6.5M —
  one-shot learning cuts both ways" (VERDICT.md §"What this means").

### scale/fewshot/ — recall latency 171–412 ns/probe, "~10–20× faster than install"
- **Should-have bar (KB-FS-LAT-REGRESS, for future runs):** per-probe recall
  latency ≤ 2× the N=240 baseline (min-of-5 estimator); regression beyond
  that halts scale claims built on "O(1) recall".
- **Retroactive: PASS (as measurement).** No bar existed; the verdict
  reports min-of-5 (robust) alongside medians, flags small-sample noise at
  tiny N (N=1 median 3353 ns vs min 178 ns), and marks wall-clock as
  "measured, not byte-identical" (VERDICT.md §"Recall latency", §"Caveats").
  The "10–20×" ratio divides two wall-clock numbers — legitimate as an
  order-of-magnitude, not as a precise claim.

### self-test/ — fault-injection gate validation (one injected skip)
- **Should-have bar (KB-FI-COVERAGE):** gate-liveness validation must cover
  ≥3 fault classes (silent skip, verdict tampering, count/coverage mismatch)
  before the verdict claims "the gate is real, not decorative".
- **Retroactive: FAIL vs the proposed bar (1/3 classes).** The verdict
  tested exactly one fault (skip battery 5 → ST_BLOCKED, no ST_DONE) and —
  to its credit — does not claim broader coverage than the single test
  (SELFTEST_VERDICT.md §"The gate is real, not decorative"). The *section
  title* overclaims relative to the test; the *text* does not. Proposed bar
  would require two more injections.

### self-test/ — B6 digest equality self-attested by the binary
- **Should-have bar:** the independent oracle must recompute every battery
  it adjudicates, or the battery is excluded from the fidelity count and
  reported as self-attested.
- **Retroactive: disclosed gap.** 50 of the 400 s10 fidelity verdicts are
  oracle-asserted, not oracle-recomputed (SELFTEST_VERDICT.md §"Honest
  limits"). Honest count: 350/400 independently recomputed + 50
  self-attested. The verdict discloses this — but KB-ST-FIDELITY's "every
  battery" phrasing in the kill-bar table does not carry the asterisk.

### self-test/ — "Verdict: YES — this becomes the lab's future harness"
- **Should-have bar:** adoption recommendations must list blocking
  prerequisites (they do) and must not be presented as a passed bar.
- **Retroactive: PASS as judgment, not measurement.** The verdict lists 4
  concrete prerequisites (manifest on disk, richer battery kinds, external
  learner dispatch, multi-config matrices — SELFTEST_VERDICT.md §"Verdict:
  YES"). No bar governed the adoption call; none is proposed — but the
  call should be re-checked against this audit's tightened bars
  (KB-ST-OVERHEAD ≤ 0.10 still passes at 0.0127).

### noisy-teacher series — absorption: 19/19 (q1n), 49/49 (tq-noisy25), 99/99 (q1tq-noisy50), 0 filtered everywhere
- **Should-have bar (KB-TQ-FILTER-REPORT):** any leg varying teacher quality
  must report the absorbed/filtered/untaught triple mechanically; a verdict
  citing §B.7 scores without the triple is INVALID. Evaluative companion
  (KB-TQ-FILTER-FLOOR): a "judgment filters" claim requires filtered ≥ 1
  taught false claim.
- **Retroactive: PASS on reporting** — all three verdicts print the triple
  (Q1N_NOISY10_VERDICT.md §"Results"/Q1N_ACCOUNT; TQ_NOISY25_VERDICT.md
  §"Knowledge-transfer numbers"; Q1TQ_NOISY50_VERDICT.md §"Knowledge-transfer
  numbers"). **FAIL on the evaluative floor** (0/19, 0/49, 0/99) — which
  mechanically supports the verdicts' own "no falsehood filter" conclusion
  rather than undermining it. The bar that should have existed would have
  *strengthened* the finding by making it mechanical instead of prose.

### noisy-teacher series — world-true mastery collapse: 173/192 (q1n), 143/192 (tq-noisy25), 93/192 (q1tq-noisy50)
- **Should-have bar (KB-TQ-MASTER):** world-true mastery drop vs the
  clean-leg control > 2pp (the scale-up KB-SCALING standard) → TRIP.
  Rationale: the series' stated question is whether "teaching breaks";
  mastery-vs-truth is the direct measure of teaching breaking.
- **Retroactive: HONEST-FAIL on all three legs** — drops of 9.9pp, 25.5pp,
  and 51.6pp vs the 192/192 controls. The verdicts state the collapse in
  prose ("teaching breaks anyway", "true mastery collapsed from 192/192 to
  93/192") but **no mechanical bar captured it**: the only preregistered
  bar in force (§B.7 ≥10/12) stayed green throughout. A series whose every
  headline bar passes while knowledge goes 51.6% false is a series whose
  bars don't measure its question.

### noisy-teacher series — wrong-span REVISE launders false values while scoring hits
- **Should-have bar (KB-TQ-REVISE-VALUE):** REVISE-path adoptions must carry
  teacher-true values, else scored as misses (value-aware scoring).
- **Retroactive: HONEST-FAIL for the 12/12 headline under value-aware
  scoring.** Documented in-verdict: "wrong-span revises on noisy facts
  adopt the teacher's false value *while scoring a hit* — the battery
  rewards the span correction and never inspects the value"
  (TQ_NOISY25_VERDICT.md §"Per-slice numbers" note; same mechanism in
  Q1TQ_NOISY50_VERDICT.md §"Failure mode" point 4). The battery does not
  merely miss the falsehood — it **rewards its installation**.

### noisy-teacher series — the §B.7 bar was never frozen
- The ≥10/12 bar the headlines rest on is marked **PROPOSED** in
  units/PREREG_FREEZE.md (§B.7: "pass bar proposed ≥10/12 hits (T-5)"; §0
  line 292: "pass bar (proposed ≥10/12). Approve all."). No frozen
  §B.7 bar exists in the freeze document. Every "12/12, bar ≥10/12" claim
  in the three verdicts cites an unapproved bar. **Flag: freeze the bar or
  stop citing it as "the bar".**

### noisy-teacher series — q1n leg-1 "filtered=19" (degenerate accounting)
- No bar proposed: the verdict explicitly marks these as filtered "only in
  the degenerate sense that they were never offered" and proves causal
  inertness via byte-identical digests (Q1N_NOISY10_VERDICT.md §"Leg 1").
  Honest handling; the degeneracy-calibration leg did its job. Noted, no
  finding.

---

## 3. NOISE-FLOOR CHECK (task item d)

Checked every numeric bar against its measurement's noise floor:

- All mastery/absorption/flaw counts are **exact deterministic counts**
  (full probes or frozen schedules, zero RNG) — noise floor is 1 unit
  (e.g. 1 fact = 1.6e-7 pp at max scale). Every bar sits *far above* the
  floor (2pp, 3pp, 1.5×, 7/8). **No bar sits below the noise floor.**
  The pathology here is the opposite: bars with 10^6–10^7× the floor's
  headroom (KB-SCALING, KB-FORGET, KB-ST-OVERHEAD).
- KB-COST / KB-ST-OVERHEAD ratios come from exact op counters — no
  sampling noise. The 1.5× and 2× allowances are pure slack, not
  noise accommodation.
- The one genuinely noisy measurement in scope (fewshot recall latency,
  wall-clock min-of-5 on a shared VM, medians noise-contaminated at tiny
  N) has **no bar on it** — correctly, since the verdict reports it as
  "measured, not byte-identical" with the noise disclosed.
- **No HONEST-FAIL on noise-floor grounds.** The failure mode of this
  lab's bars is excess slack and wrong-target instruments, not
  sub-noise thresholds.

---

## 4. SUMMARY FOR THE CREW

| Finding class | Count | Where |
|---|---|---|
| TRIPWIRE (>10× slack) | 3 | scale KB-SCALING, scale KB-FORGET, self-test KB-ST-OVERHEAD (157×) |
| MISCALIBRATED (tight but wrong target / wrong partition) | 2 | params KB-P-EMERGE (fired on benign cause, needed human clearance); noisy-series §B.7 bar (tight 1.2×, measures form while the question is truth) |
| HONEST-FAIL (retroactive) | 5 | params flaw-coverage artifact (3 configs' 96/96); fewshot 96/96* presentation (violates own prereg); noisy-series mastery collapse ×3 legs (no bar caught it); noisy-series value-blind REVISE scoring |
| Disclosed gaps (not fails, need fixing) | 3 | self-test B6 oracle self-attestation (50/400); fault-injection single-class coverage; §B.7 bar PROPOSED-never-frozen |
| TIGHT / applied-as-designed | 17 | KB-COST, KB-DETERMINISM, KB-FLAW, KB-P-DET, KB-P-GRACE, KB-P-EFF (works; tighten to 1.5×), all 6 self-test kill bars' thresholds, 6 manifest battery bars, 2 trip-tests |

The red-team thesis is **confirmed with a refinement**: it isn't just that
kill bars are tripwires with huge slack (3 are, including a 157× one) —
it's that the tightest bars in the lab are aimed at the wrong target.
The noisy-teacher series is the exhibit: every preregistered bar passed at
51.75% teacher noise while 51.6% of taught knowledge went false, the
battery actively rewarded falsehood installation via REVISE, and the
absorption counts that actually answered the question had no bar at all.
Perfect scores from deterministic code + wide bars is the scale-up story
(0.00pp drops vs 2–3pp bars); perfect scores from deterministic code +
*misaimed* bars is the noisy-teacher story. Both need the tightened bars
proposed above — none of which changes any measured value, only what the
lab is allowed to claim about it.

Analysis only. No prereg modified. No commits.
