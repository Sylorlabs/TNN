# PREREG — F5 full mechanism: predicate + fast confirmation machinery

Frozen 2026-09-24. Committed ALONE before any code. Builder: F5 round-2
confirmation crew (Crew 4, subagent session 1f9bd76d, hypothesis H-PAM-3).

This prereg executes the verdict's honest path #3 from
`round2/f5_redteam300/VERDICT_F5_REDTEAM300.md`:

> build the confirmation machinery and re-run this battery against the full
> mechanism — the trap may be salvageable as predicate + fast confirmation,
> but the predicate alone is not.

The red-team KILL rested on two facts: (1) predicate-level, 110/300 (36.7%)
of near-exemplar correct percepts fall inside the frozen block window; (2)
delay-level, 94/300 delayed > 50 trials under the preregistered FIFO queue
model of the then-unbuilt machinery. This battery builds the actual
confirmation machinery ("three deliberate re-inspections from three
temporal crops") in pure Zag and re-runs the identical 300-percept battery
against the FULL mechanism (predicate + confirmation), measuring delay on
the real mechanism instead of the queue model.

## 1. Hypothesis under test

The F5 counter-corroboration trap is salvageable as predicate + fast
confirmation: with the confirmation machinery built, the delay bar
(recomputed on the real mechanism) passes, the far-control bar still passes
at 0/60, the backtest's 8 blocked false accepts are still withheld (8/9
retention), and a substantial share of the 110 blocked-correct percepts are
confirmed-and-installed within budget.

## 2. Frozen inputs (verified by script before drafting)

- Fixture ledger `round2/f5_redteam300/fixtures_ledger.txt`, SHA
  `0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0`
  (360 lines: 300 NEAR + 60 FAR, all truth-correct, all
  `DISP=ACCEPT_INSTALL`).
- Exemplar bank `v2/f5_backtest/exemplars.tsv`, SHA
  `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`
  (6 TMB-1 exemplars; conf 701–718, measure 2618–2647).
- Backtest candidate ledger
  `v2/redteam/evidence/ledger_d_withhold.txt` (43 `DISP=ACCEPT_INSTALL`
  lines: 9 false — 8× TMB-5 RICH-judged — + 34 true), for the 8/9
  retention replay.
- Frozen block predicate: BLOCKED iff ∃ exemplar with same family stem,
  |Δconf| ≤ 150, |Δmeasure| ≤ 2000 (unchanged from the backtest and the
  red-team; logic identical to `f5_pred.zag` /
  `round2/f5_redteam300/f5_rt300.zag`).
- `measure` substitution carried exactly as the backtest (task-specific raw
  quantity, NOT the margin mrgF). A true-margin replay remains the
  documented upgrade path.

## 3. The confirmation machinery (deterministic spec)

### 3a. Temporal-crop construction

A blocked percept with observed `(conf, measure)` is re-inspected from
three temporal crops of its sense trace — three deliberate re-measurement
sessions. The synthetic battery models each crop as a deterministic
re-derivation with fixed re-measurement dispersion (zero RNG):

- crop 0 (early): `(conf − JIT_C, measure − JIT_M)`
- crop 1 (mid):   `(conf, measure)`
- crop 2 (late):  `(conf + JIT_C, measure + JIT_M)`

with `JIT_C = 10`, `JIT_M = 200` (fixed constants: 1/15 of the conf block
half-width, 1/10 of the measure block half-width — small re-measurement
dispersion, preregistered, not tuned).

Limitation (stated up front, not post-hoc): the synthetic fixtures carry a
fixed judgment string, so the crops re-derive only the (conf, measure)
observables, not the judgment itself. What this battery tests is the
geometric corroboration machinery; true judgment re-derivation from sense
traces is future work with real traces.

### 3b. Re-inspection predicate (per crop)

Crop k "reproduces the false signature" iff there EXISTS a bank exemplar
with ALL three:

1. Same family stem.
2. `|conf_crop − conf_ex| ≤ Tc`.
3. `|measure_crop − measure_ex| ≤ Tm`.

`(Tc, Tm)` is the confirmation core window — strictly tighter than the
block window — derived in §4 from the known false accepts only.

### 3c. Confirmation quorum

- **WITHHOLD** (terminal: the percept is never installed) iff ≥ 2 of the 3
  crops reproduce the false signature — the suspicious signature is stable
  across independent temporal re-inspections, so the percept is treated as
  a false accept.
- **CONFIRM + INSTALL** otherwise — the block was a false alarm; the
  percept installs once its three re-inspections complete.

### 3d. Delay accounting in trials (the REAL mechanism)

- ALLOWED percepts: installed at their arrival trial → delay 0.
- Blocked + CONFIRMED: the three re-inspections are provisioned in
  parallel on the fast confirmation path (deliberation is expensive, but
  the trap's whole point is spending it here — this is the "fast" in fast
  confirmation) and complete 3 trials after the block → installed at
  trial+3 → delay 3.
- Blocked + WITHHELD: never installed → delay ∞, which counts as
  delayed > 50 trials for the delay bar (a withheld correct percept is
  stalled forever, strictly worse than a delayed one).

### 3e. Bounded budget

- Exactly 3 deliberate re-inspections per blocked percept, no more.
- WITHHOLD is terminal: no re-queue, no second confirmation round.
- Confirmation applies ONLY to predicate-blocked percepts; ALLOWED
  percepts (including all far controls) never enter confirmation.

### 3f. Sensitivity S-serial (reported, not the verdict)

The red-team's scarcity model applied to the real mechanism's decisions:
one deliberate re-inspection per trial globally, FIFO in trial order → the
k'-th confirmed percept (confirmation order) has delay 3k'; withheld stay
∞. Reported to show the cost of under-provisioned deliberation; the
verdict uses the provisioned fast path (§3d).

## 4. Parameter derivation — by script, from frozen evidence only

`Tc`/`Tm` are derived from the 8 KNOWN false accepts (frozen backtest
evidence — the percepts the trap exists to catch), never from the 110
blocked-correct outcomes:

- For each of the 8: min over exemplars of |Δconf|, |Δmeas|.
- `Tc = ceil10(max Δconf + JIT_C)`, `Tm = ceil50(max Δmeas + JIT_M)`
  (smallest round numbers strictly covering the jitter-expanded
  false-cluster bounding box).

Extraction script: `round2/f5_fullmech/spec_extract.py` (SHA
`c513d03824b5030b30c1ce2d3549573c49dbeda4fa241d15eade2ff65f76fdb5`).
Verbatim output:

```
backtest ACCEPT_INSTALL lines: 43
known TMB false accepts: 8
max min-exemplar |dconf| over 8 falses = 114
max min-exemplar |dmeas| over 8 falses = 730
DERIVED confirmation core window: Tc=130 Tm=950
  (rule: ceil10(114+10) / ceil50(730+200))
BACKTEST replay: blocked-false=8/9 withheld-false=8 escaped-false=1 true-blocked=0
BATTERY: near=300 blocked=110 confirmed+installed=50 withheld=60
BATTERY: far=60 blocked=0
DELAY BAR (real mechanism): delayed>50 = 60/300 = 20.0%  (bar: <=25%, i.e. <76)
CONFIRM-INSTALL RATE on blocked-corrects: 50/110 = 45.5%
```

The Zag implementation must reproduce every one of these numbers exactly,
or the implementation is wrong. (These are implementation checks, not the
verdict — the verdict comes from §5 applied to the battery's measured
numbers.)

## 5. Kill bars

- **(a) Delay bar (REAL mechanism, not the queue model):** > 25% of the 300
  near-exemplar percepts (≥ 76 of 300) with delay > 50 trials — installed
  with delay > 50, or withheld (delay ∞) — → KILL.
- **(b) Far-control bar:** 0/60 far controls blocked/withheld → any block →
  KILL. (Predicate unchanged; confirmation never sees them.)
- **(c) Backtest retention:** the full mechanism must still WITHHOLD the 8
  blocked false accepts (8/9; the COL-4 false escapes the predicate as
  before, by design) and block 0/34 true accepts → fewer than 8 withheld →
  KILL. The confirmation machinery must not install known false accepts.
- **(d) Confirm-and-install rate on the 110 blocked-corrects:** REPORTED
  metric, no frozen kill threshold (none was frozen). It informs the
  salvageability reading: the higher the rate, the more of the trap's
  over-block the confirmation recovers.

Verdict: SURVIVE iff (a), (b), (c) all pass; KILL otherwise, stated
plainly with the numbers. Delay histogram bins (installed delays):
0 | 1–3 | 4–10 | 11–50 | 51–100 | 101–300 | 301+, plus WITHHELD (∞) count.

## 6. Laws and method

- Mechanism in pure Zag (`f5_full.zag`, extended from the frozen
  `f5_rt300.zag` predicate): the decision path
  (predicate → crops → re-inspection → quorum) takes ONLY
  (family stem, conf, measure). The truth field is parsed solely for
  offline scoring counters and the 300-battery's judgment==truth
  construction assert; it never enters a decision. (Code-reviewed before
  the run; the firewall is documented in source comments.)
- Fixture reuse: the frozen `fixtures_ledger.txt` is reused deterministically
  (SHA re-verified at build time); no new fixtures, zero RNG.
- Backtest replay: the same binary runs the 43-candidate ledger (17-field
  format, no `SET=` field → scored as BACKTEST set, no truth assert) for
  bar (c).
- Binary reads argv[1] = ledger, argv[2] = frozen `exemplars.tsv`.
- Run 3× on the 300-battery; SHA-256 of stdout byte-identical across runs.
  Backtest replay run 3× likewise.
- Commit order: this prereg ALONE first; then build + run; then evidence
  (sources, extractor + its output, frozen bank copy, run outputs,
  SHASUMS.txt) + verdict committed together. No binaries, no `.zagd` /
  `.zag-cache` files.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Work: `docs/lab/senses/pam-rebuild/round2/f5_fullmech/`
  (branch `tnn-native-lab`).

## 7. Pre-registered honesty notes

- The 110 blocked-corrects' geometry was NOT consulted when deriving
  (Tc, Tm); the derivation used only the 8 frozen false accepts. Whatever
  confirm/withhold split the battery measures is the mechanism's, not a
  tuned outcome.
- Withheld correct percepts count against the delay bar (§3d) — the bar is
  a joint test of confirmation speed AND confirmation precision.
- The synthetic crops model re-measurement dispersion only (§3a
  limitation); a real-trace evaluation of judgment re-derivation is out of
  scope for this battery.
- If the mechanism SURVIVES here, the live-gate go/no-go still needs
  Micah's word per the program's standing governance; this battery decides
  the mechanism question only.

## 8. Deliverable

Verdict: SURVIVE or KILL with measured numbers (delayed>50 / 300 on the
real mechanism; far-control blocked / 60; backtest withheld / 9;
confirm-install / 110; delay histogram; S-serial sensitivity), run SHAs,
commit SHAs, and an explicit salvageability reading for the F5 trap.
