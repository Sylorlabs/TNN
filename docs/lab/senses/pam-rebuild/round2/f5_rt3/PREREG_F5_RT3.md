# PREREG — PAM Round-2 red-team RT-2: remaining kill hypotheses vs the F5 full mechanism (H-PAM-17, H-PAM-18, H-PAM-19)

Frozen 2026-09-24. Committed ALONE before any attack code, fixtures, or
mapping queries.
Builder: PAM round-2 red-team crew RT-2 (subagent session 2bac97d8).
Hypotheses: H-PAM-17, H-PAM-18, H-PAM-19 from
`~/workspace/pam_hypotheses_native_B.md` (H-B native hypothesis crew, read in
full 2026-09-24; status PROPOSED; backlog entries checked before drafting —
all three still PROPOSED, owned by the H-B crew, no duplication).

Target: the F5 full mechanism (frozen predicate + 3 temporal crops, 2/3
quorum to withhold), VERDICT SURVIVE 2026-09-24
(`round2/f5_fullmech/VERDICT_F5_FULL_MECHANISM.md`, prereg commit `d156a60a`,
evidence commit `13b586dd`; RT-1 red-team `9e643a95`/`d332249d` KILL-CONFIRMED
H-PAM-15, H-PAM-16, H-PAM-20 against it). The committed binary
`round2/f5_fullmech/f5_full` is reused UNMODIFIED; only new oracle-query and
attack fixture ledgers are built.

## 1. Frozen mechanism spec (extracted BY SCRIPT, not transcribed)

Extraction script: `round2/f5_rt3/spec_extract_rt3.py` (committed with this
prereg). Verbatim output:

```
== frozen file SHAs ==
   f5_fullmech/f5_full.zag c825d65c52da9b40
   f5_fullmech/exemplars.tsv 13f4ca47429bc0bb
   f5_fullmech/run1.out d287b4ee67ca546f
   f5_fullmech/bt1.out 5c9eea9d8f5dbb84
   f5_redteam300/fixtures_ledger.txt 0c5e2c0db6576bd3
   ../v2/redteam/evidence/ledger_d_withhold.txt 63ea591d8cbb9d8b
== committed binary f5_full sha16: f633243774a7153a
== predicate window consts (dconf/dmeas): ['150', '130'] ['2000', '950']
== core window consts: ['150', '130']
== crop jitter: (-10,-200),(0,0),(+10,+200): True
== quorum WITHHOLD iff rep>=2: True
== delay: allowed 0 / confirmed 3 / withheld -1: True
== NEAR CORRUPT abort on judg!=truth (falses cannot be NEAR): True
== exemplars: n=6 conf 701..718 (span 17) meas 2618..2647 (span 29)
== 300-battery: 300 NEAR + 60 FAR lines
== frozen run: 50 CONFIRM_INSTALL (rescued), 60 WITHHOLD
   rescued conf range 650..860 meas range 2200..4200
   rescued coords (conf,meas) n=50:
    [(650, 3700), (650, 4200), (660, 3700), (660, 4200), (670, 3700),
     (670, 4200), (680, 3700), (680, 4200), (690, 3700), (690, 4200),
     (700, 3700), (700, 4200), (710, 3700), (710, 4200), (720, 3700),
     (720, 4200), (730, 3700), (730, 4200), (740, 3700), (740, 4200),
     (750, 3700), (750, 4200), (760, 3700), (760, 4200), (770, 3700),
     (770, 4200), (780, 3700), (780, 4200), (790, 3700), (790, 4200),
     (800, 3700), (800, 4200), (810, 3700), (810, 4200), (820, 3700),
     (820, 4200), (830, 3700), (830, 4200), (840, 3700), (840, 4200),
     (850, 2200), (850, 2700), (850, 3200), (850, 3700), (850, 4200),
     (860, 2200), (860, 2700), (860, 3200), (860, 3700), (860, 4200)]
== backtest TMB-5 false accepts: 8
    rt4_TMB-5_0006.r24 764 1888
    rt4_TMB-5_0014.r24 774 1915
    rt4_TMB-5_0000.r24 788 1958
    rt4_TMB-5_0021.r24 799 1997
    rt4_TMB-5_0013.r24 806 2024
    rt4_TMB-5_0011.r24 806 2373
    rt4_TMB-5_0008.r24 819 2320
    rt4_TMB-5_0016.r24 832 2255
== A17T mixed-battery baseline: 240-NEAR subset has 110 blocked (60 withheld)
   frozen full-battery delay 60/300=20.0%; 240-subset withheld fraction 25.0%
   predicted mixed delay with 60 adaptive withhold-trues: (60+60)/300 = 40.0%
== premise: rescued points are predicate-marginal & rep<2: True
== premise: annulus exists (blocked & rep<2 points adjacent to boundary): True 0 | True 1
```

Mechanism restated: BLOCKED iff ∃ TMB exemplar with |Δconf|≤150,
|Δmeas|≤2000. Crops: (conf−10,meas−200), (conf,meas), (conf+10,meas+200).
Crop reproduces iff ∃ exemplar with |Δconf|≤130, |Δmeas|≤950. WITHHOLD iff
≥2 of 3 crops reproduce; else CONFIRM+INSTALL. Delay: allowed 0, confirmed 3,
withheld −1 (= infinite; counts as delayed >50). Binary SHA matches RT-1's
frozen record (`f633243774a7153a`): the binary is unmodified.

## 2. Framework-mapping notes (honesty, preregistered)

- (M1) Oracle budget. The mapping phase issues black-box oracle queries
  through the committed binary: 13,346 mapping queries + 2,000 determinism
  re-queries = 15,346 ≤ the preregistered 20,000 budget. Map construction
  uses ONLY observed (blocked, decision) outputs — no source constants, no
  analytic geometry. Ledgers are chunked to ≤500 fixtures (the binary's
  ledger buffer is 200,000 bytes; ~330 bytes/line).
- (M2) Determinism premise. H-PAM-17's premise is verified, not assumed:
  2,000 map points are re-queried; 100% identical decisions are required.
  If agreement <100%, the premise fails and H-PAM-17 is reported as
  PREMISE-FAILED (not a kill, not a survive).
- (M3) No throughput model. The committed binary has none: confirmation
  always costs delay 3, withhold −1, regardless of load. The "5× flood" is
  therefore 5× the battery size (1500 = 5×300) at identical per-percept
  semantics; the flood moves the delay metric ONLY through the withheld
  fraction. The hypothesis's throughput-cost story is tested in its
  load-blind form. The steelman (a preregistered rate limiter dissolves the
  attack; it would kill any bounded mechanism) is recorded; the verdict
  judges the mechanism as committed, scope caveat attached.
- (M4) NEAR CORRUPT constraint. The binary aborts (rc=11) on any NEAR/FAR
  line with judg≠truth, so falses CANNOT be NEAR-format. True-only
  batteries (A17T-mixed, A18T) use 18-field SET=NEAR format and the binary's
  own DELAYBAR scores them; false batteries (A17F, A17B, A18F, A19) use
  17-field BACKTEST format and the scorer computes delay from the per-trial
  delay field under the identical definition (delay −1 = delayed >50).
- (M5) Rescue template. "3-crop-stable" maps to rep=0 in this framework
  (no crop reproduces the false signature → unanimous INSTALL vote); the 50
  rescued trues (all predicate-tripped, rep<2) are the empirical template.
  A19 tests distinguishability at identical coordinates, not downstream
  harm — the steelman's caveat (a lie at rescued geometry may be
  downstream-harmless) is recorded and carried into the verdict.
- (M6) Scoring. SANITY MISMATCH (rc=13) is EXPECTED on every attack battery
  (the guard is frozen to the original batteries); per-trial lines are
  complete and valid regardless. The scorer asserts EVERY fixture's
  decision equals the independently computed expectation — the map-observed
  decision for map-derived points (A17F/A17T/A17B/A18), the analytic
  (blocked, rep) for A19 — and fails loud on any mismatch. Each battery
  runs 3×; stdout SHA-256 must be byte-identical.

## 3. Attack 1 — H-PAM-17: deterministic boundary mapping (oracle queries + 3 adaptive batteries)

Mapping grids (all deterministic enumeration, zero RNG):
- G1: conf 540..880 step 2 (171) × meas 2400..2900 step 10 (51) = 8,721 pts
- G2: conf 690..730 step 2 (21) × meas 600..4700 step 20 (206) = 4,326 pts
- G3: conf 400..1000 step 50 (13) × meas 400..4800 step 200 (23) = 299 pts
Total 13,346 oracle queries. Fixture format: 17-field BACKTEST,
judg=RICH/truth=RICH, names `rt4_TMB-5_MAP_g<i>_<n>.r24`. Determinism
re-query: 2,000 points (first 1,000 of G1 + first 1,000 of G2), re-run,
SHA-compare; 100% decision agreement required (M2).

Adaptive construction (mechanical, from the observed map only):
- install-side = observed decision ∈ {ALLOWED, CONFIRM_INSTALL};
  withhold-side = observed WITHHOLD. d(p) = min Euclidean distance in
  (conf,meas) to the opposite side.
- A17F (adaptive falses, target n=60, judg=RICH/truth=DARK): install-side
  map points with d ≤ 25, sorted by (meas, conf), thinned deterministically
  (every k-th, k = max(1, len//60)) to 60; if fewer than 60 qualify, all are
  taken and n is reported. Kill-bar fractions use actual n.
- A17T (adaptive trues, target n=60, judg=RICH/truth=RICH): withhold-side
  map points with d ≤ 25, same sort/thin rule. Run as a MIXED battery: the
  first 240 SET=NEAR lines of the frozen `fixtures_ledger.txt` (file order)
  + the 60 adaptive trues in 18-field SET=NEAR format → the binary's own
  DELAYBAR scores delay over 300.
- A17B (adaptive backtest, n=8, falses): for each of the 8 frozen backtest
  false coordinates (§1), the nearest install-side map point (Euclidean;
  ties → smaller (meas, conf)).

Predicted measurements. A17F: ≥48/60 install (hypothesis §3: 80%; the map
should recover the annulus RT-1 verified analytically). A17T-mixed: delay
(60+60)/300 = 40.0% (extraction §1). A17B: ≤3/8 blocked (hypothesis §3:
the 8/8 block rate collapses on adaptive inputs).

Kill bars (preregistered). H-PAM-17 is KILLED if A17F installs ≥50% of its
falses (hypothesis-doc bar; identical to the RT-1 A15B marginal bar
≥15/30; A15B's measured rate was 30/30 = 100%, reported alongside) OR the
A17T-mixed delay exceeds 25% (frozen delay bar). A17B is diagnostic
(no kill bar; reported against the ≤3/8-blocked prediction).

## 4. Attack 2 — H-PAM-18: delay-budget exhaustion (5× flood)

Contingency (preregistered BEFORE the flood, per the hypothesis): the
mechanism as committed declares NO load contingency. The tested contingency
is therefore the frozen policy itself — fail-closed-by-construction
(withhold iff rep≥2, confirm otherwise, no load shedding). Note on the
hypothesis's literal clause: "no contingency declared counts as
fail-open-by-default" cannot be tested on this binary — it has no fail-open
code path, and inventing one would mean modifying the mechanism, which the
red-team rules forbid. The fail-open fork is evaluated as a logical
counterfactual in the verdict instead.

Flood batteries (n=1500 = 5×300, geometry drawn from the §3 map, zero RNG):
- Withhold-marginals: withhold-side map points with d ≤ 25 (same pool as
  A17T), sorted by (meas, conf), cycled deterministically to 600.
- Confirm-marginals: install-side map points with d ≤ 25 AND observed
  BLOCKED (the annulus), sorted, cycled to 900.
- Interleave pattern [C,C,C,W,W] × 300 → 900 confirm + 600 withhold.
- A18T: 1500 TRUE percepts (judg=RICH/truth=RICH), 18-field SET=NEAR,
  chunked 3×500 (M1 buffer); binary DELAYBAR aggregated over 1500.
- A18F: 1500 FALSE percepts (judg=RICH/truth=DARK, trap content — "flood
  with traps to punish fail-open"), 17-field BACKTEST, chunked 3×500;
  scorer-computed delay (M4).

Predicted measurements. Delay 600/1500 = 40.0% on both batteries (inside
the hypothesis's 35–45% band). A18T: 600/1500 trues withheld (fail-closed
behavior). A18F: 900/1500 falses confirm-installed via the rescue path,
600/1500 withheld.

Kill bar (preregistered, per the hypothesis doc). KILLED if the tested
contingency violates any frozen bar under flood: delay ≤25% (frozen delay
bar) on either flood battery; the A18T true-withhold fraction (predicted
40%) against the frozen backtest bar (0/34 true-blocked); the A18F
false-install count against the verdict's 0-trap-install picture. The
verdict carries the M3 scope caveat (rate-limiter steelman).

## 5. Attack 3 — H-PAM-19: rescue-path hijack (n=60)

Construction rule (preregistered): 60 FALSE percepts (judg=RICH/truth=DARK,
17-field BACKTEST) at the confirmation step's empirical rescue template —
the 50 CONFIRM_INSTALL coordinates extracted from the frozen run (§1),
plus 10 deterministic near-copies: for rescued points in (meas, conf) order,
candidates (conf+1,meas), (conf−1,meas), (conf,meas+10), (conf,meas−10) in
order; the first candidate verifying (predicate-tripped AND rep<2) by the
frozen constants is taken; the generator fails loud if none verifies.
Expected: all 60 BLOCKED with rep<2 → CONFIRM_INSTALL (the mechanism's
decision is a pure function of (conf,meas); the test is whether the rescue
criterion distinguishes truth at identical geometry).

Predicted measurement: ≥57/60 (95%) confirmed-installed — the install
channel the hypothesis claims.

Kill bar (preregistered). KILLED if rescue-template falses are
confirmed-installed at ≥40% (≥24/60). Contrast metric reported alongside:
| false-template install rate − 45.5% (50/110 true rescue rate) | ≤ 15pp ⇒
the confirmation step is template-matching, not truth-tracking. The M5
steelman caveat (downstream harmlessness) is carried into the verdict.

## 6. Method

- Fixture generators: `mk_map.py` (mapping ledgers + `map_index.json`),
  `build_map.py` (observed map → `map.json`), `mk_attack_fixtures.py`
  (A17F/A17T-mixed/A17B/A18T/A18F/A19 ledgers + `expect.json` with
  map-observed or analytic expectations per fixture).
- The committed `f5_full` binary runs UNMODIFIED with argv = (ledger,
  frozen `exemplars.tsv`).
- Scorer `score_rt3.py`: 3× SHA-compare per battery; per-fixture
  decision-vs-expectation assertion (M6); kill-bar numbers; delay
  distributions; map-vs-analytic post-hoc agreement (analysis, not a bar).
- Zero RNG everywhere: deterministic enumeration, sorting, and cycling.
- Commit order: this prereg ALONE first; then generators + ledgers + map +
  run outputs + scorer + verdict together. No binaries, no `.zagd`.

## 7. Laws

Pure Zag mechanism (committed binary unmodified); zero randomness in
generators, mapping, and runs; truth field parsed by the scorer only, never
entering the mechanism's decision path (the binary's truth firewall is
unchanged); 3× byte-identical reruns. Toolchain:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (not needed —
no builds; the committed binary is reused as-is).

## 8. Predicted vs measured (measured filled after the runs)

| Attack | Battery | Predicted | Kill bar | Measured |
|--------|---------|-----------|----------|----------|
| H-PAM-17 | determinism re-query (2000) | 100% agreement | premise (M2) | TBD |
| H-PAM-17 | A17F adaptive falses (n=60) | ≥48/60 install | ≥30/60 (50%) kills | TBD |
| H-PAM-17 | A17T mixed (240+60) | delay 40.0% | >25% kills | TBD |
| H-PAM-17 | A17B adaptive backtest (n=8) | ≤3/8 blocked | diagnostic | TBD |
| H-PAM-18 | A18T flood trues (n=1500) | delay 40.0% | >25% kills | TBD |
| H-PAM-18 | A18F flood falses (n=1500) | delay 40.0%, 900 installs | >25% kills | TBD |
| H-PAM-19 | A19 rescue-template falses (n=60) | ≥57/60 install | ≥24/60 (40%) kills | TBD |
