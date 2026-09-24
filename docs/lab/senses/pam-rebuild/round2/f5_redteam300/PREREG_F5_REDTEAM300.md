# PREREG — F5 counter-corroboration trap, 300-percept red-team

Frozen 2026-09-24. Committed ALONE before any code. Builder: F5 round-2
red-team crew (subagent session d29b21df).

This prereg executes the frozen conditional clause from
`v2/preregs/PREREG_F5_BACKTEST.md` §6:

> ONLY if both bars pass: red-team with 300 near-exemplar correct percepts;
> KILL if > 25% are delayed > 50 trials. This is filed here as a conditional
> clause and is NOT run under this prereg — generating 300 fresh percepts is
> not an offline replay of committed logs and needs its own fixture-generation
> prereg.

The backtest verdict (`v2/f5_backtest/VERDICT_F5.md`, committed 2026-09-23)
was SURVIVE (8/9 false blocked, 0/34 over-blocked, 3 byte-identical runs),
so this clause is now live. Per Micah's rule it runs BEFORE any live-gate
build of F5.

## 1. Hypothesis under test

The pre-confirmation block predicate (frozen: family-stem match;
|Δconf| ≤ 150; |Δmeasure| ≤ 2000) does not over-block near-exemplar correct
percepts: when stressed with 300 truth-correct timbredisc percepts drawn from
the exemplar neighborhood, the fraction delayed > 50 trials stays ≤ 25%,
and a far-from-exemplar correct control set is blocked at rate 0.

## 2. Scope (explicit honesty, same as the backtest)

**Pre-confirmation block predicate ONLY.** The "three deliberate
re-inspections from three temporal crops" confirmation machinery is still
unbuilt and is NOT exercised here. Because the frozen clause's kill bar is
written in delay terms ("delayed > 50 trials") and the predicate itself is
binary (BLOCKED/ALLOWED), §5 preregisters the delay operationalization as an
explicit assumption about the unbuilt machinery. It is an assumption, not a
test of the machinery. If F5 survives, building the confirmation path is
still separate future work.

## 3. Fixture design (fresh generation, zero RNG)

### 3a. The 300 near-exemplar correct percepts (the red-team set)

Ledger-format lines (same 17-field `|` format as the backtest ledger, plus a
trailing `SET=` field — see §7), `DISP=ACCEPT_INSTALL` on every line:

- Family: `rt4_TMB-5_%04d.r24`, seq 0–299, trials 1–300. TMB-5 is the family
  of the 8 false accepts the trap caught in the backtest — the hardest fair
  case for the family-stem rule (stem `TMB`, same as the TMB-1 exemplars).
- Correctness: judgment `RICH`, truth `RICH` (truth-correct). This is the
  sharpest over-block probe: numerically inside the bad-exemplar
  neighborhood, but genuinely correct — the exact percepts the trap must
  not eat. (Exemplars are RICH-judged/BRIGHT-true; these are RICH/RICH.)
- Confidence/measure grid (deterministic parameter sweep, literal values,
  no RNG):
  - conf = 650 + 10·i, i = 0..29 → 30 values, 650–940
  - measure = 2200 + 500·j, j = 0..9 → 10 values, 2200–6700
  - 30 × 10 = 300 points, row-major (conf outer, measure inner).
- Anchoring (why this region — grounded, not tuned):
  - Exemplar bank (frozen `v2/f5_backtest/exemplars.tsv`, SHA
    `13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e`):
    conf 701–718, measure 2618–2647.
  - Real TMB-5 true accepts from the committed backtest ledger
    (`v2/redteam/evidence/ledger_d_withhold.txt`, re-read live 2026-09-24):
    conf 869–952, measure 4000–6000.
  - The grid spans the exemplar neighborhood, through the boundary zone,
    into the observed true-accept region — so the battery measures trap
    occupancy inside, on, and outside the window. Uniform grid: it measures
    window occupancy over the anchored region, NOT a real-world over-block
    frequency (no distributional claim is made).

### 3b. The 60 far-from-exemplar correct controls

Same ledger format, trials 301–360, all `DISP=ACCEPT_INSTALL`, all
truth-correct:

- 20× COL family: `rt4_COL-4_%04d.r24`, judgment `SAME`, truth `SAME`,
  conf = 800 + 5·k (800–895), measure = 50000 + 500·k (50000–59500).
  Different family stem (COL ≠ TMB) → must be ALLOWED.
- 20× TMB family, outside both windows: `rt4_TMB-5_%04d.r24`,
  judgment `RICH`, truth `RICH`, conf = 950 + 2·k (950–988, all > 868 =
  exemplar max + 150), measure = 5500 + 50·k (5500–6450, all > 4647 =
  exemplar max + 2000). Same stem but outside both windows → must be ALLOWED.
- 20× PTC family: `rt4_PTC-4_%04d.r24`, judgment `HIGHER`, truth `HIGHER`,
  conf = 780 + 8·k (780–932), measure = 1000 + 2500·k (1000–48500).
  Different family stem (PTC ≠ TMB) → must be ALLOWED.

k = 0..19 in each group. All values literal, deterministic, zero RNG.

## 4. Frozen predicate (unchanged from the backtest)

Candidate BLOCKED iff there EXISTS a bank exemplar with ALL three:

1. Same family stem (`TMB-1` → `TMB`; `rt4_TMB-5_0000.r24` → `TMB`).
2. |conf_cand − conf_ex| ≤ 150.
3. |measure_cand − measure_ex| ≤ 2000.

**Margin substitution carried exactly as the backtest (§4 of
PREREG_F5_BACKTEST.md):** `measure` (task-specific raw quantity — for
timbredisc, the spectral-centroid-like raw value, NOT the classification
margin mrgF) is the second distance axis. The synthetic fixtures carry conf
+ measure with the same semantics; no true-margin axis exists in the frozen
predicate, and adding one would test a different mechanism. A true-margin
replay remains the documented upgrade path if F5 survives.

## 5. Delay operationalization (preregistered assumption about unbuilt machinery)

The frozen clause kills on "delayed > 50 trials", but the predicate under
test is binary. The confirmation machinery ("three deliberate
re-inspections from three temporal crops") is unbuilt, so no measured delay
exists. Preregistered model — the most generous reasonable cadence to F5:

- **Primary model:** blocked correct percepts enter a FIFO confirmation
  queue in trial order. The unbuilt machinery performs at most one
  deliberate re-inspection per trial (deliberation is expensive; one per
  trial is fast for deliberate deliberation). Each blocked percept needs its
  three re-inspections (three temporal crops = three separate deliberate
  sessions). The k-th blocked percept (k = 1-based, queue order) therefore
  clears 3·k trials after its block: delay_k = 3k. Allowed percepts:
  delay 0.
- **Sensitivity S1 (slow deliberation):** one re-inspection per 5 trials →
  delay_k = 15k.
- **Sensitivity S2 (unbounded parallel machinery):** every blocked percept
  confirmed in exactly 3 trials → delay_k = 3 for all blocked (0% can exceed
  50 under any block count).

The kill bar (a) is evaluated under the PRIMARY model. All three cells are
reported, so the verdict's assumption-dependence is explicit.

Delay-length distribution bins (preregistered, over the 300 NEAR percepts):
0 | 1–3 | 4–10 | 11–50 | 51–100 | 101–300 | 301+.

## 6. Kill bars

- **(a) Delay bar:** > 25% of the 300 near-exemplar percepts (≥ 76 of 300)
  delayed > 50 trials under the primary model → KILL.
- **(b) Far-control bar:** far-control over-block rate must be 0
  (0/60 BLOCKED) → any block → KILL.
- **(c) Distribution report:** full delay-length histogram (bins from §5)
  plus the S1/S2 sensitivity cells — not just the binary bar.

## 7. Laws and method

- The block predicate is implemented in pure Zag (the predicate IS the
  mechanism under test), extended from the frozen `v2/f5_backtest/f5_pred.zag`
  (SHA `4fa4e2e4da86eeb1b21c4f43598d2bf69277131f096f7f3ddfc82fe8b9990430`)
  with the queue/delay accounting added. The predicate logic itself is
  unchanged.
- Fixture generator: deterministic Python (`mk_fixtures.py`), literal sweep
  values, zero RNG; byte-identical regeneration (SHA-checked).
- Battery binary reads argv[1] = fixture ledger, argv[2] = frozen
  `exemplars.tsv`. Fixture ledger = the 17-field backtest format plus field
  17 `SET=NEAR` / `SET=FAR`; all 360 lines `DISP=ACCEPT_INSTALL`.
- Program asserts judgment == truth on every line (all fixtures are correct
  by construction); any mismatch aborts loud (nonzero exit), it is never
  silently counted.
- Run 3×; SHA-256 of stdout byte-identical across all three runs.
- Commit order: this prereg ALONE first; then build + run; then evidence
  (sources, generator, fixture ledger, frozen bank copy, three run outputs,
  SHASUMS.txt) + verdict committed together. No binaries, no `.zagd` /
  `.zag-cache` files.
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Work: `docs/lab/senses/pam-rebuild/round2/f5_redteam300/`
  (branch `tnn-native-lab`).

## 8. Pre-registered sanity expectations (implementation check, NOT the verdict)

Hand-computed from the frozen predicate against the §3a grid (the battery
must reproduce these exactly, or the implementation is wrong):

- Blocked conf range: [701−150, 718+150] = [551, 868] → grid confs 650–860
  (22 of 30 values).
- Blocked measure range: [2618−2000, 2647+2000] = [618, 4647] → grid
  measures 2200–4200 (5 of 10 values).
- Expected blocked: 22 × 5 = **110/300** (36.7%).
- Expected primary-model delayed > 50: delay_k = 3k > 50 → k ≥ 17 →
  110 − 16 = **94/300 = 31.3%**.
- Expected S1 delayed > 50: 15k > 50 → k ≥ 4 → 107/300 = 35.7%.
- Expected S2 delayed > 50: 0/300.
- Expected far-control blocked: **0/60**.

The verdict comes from §6 applied to the battery's measured numbers, not
from these expectations.

## 9. Transparency note

The delay model (§5) is the one free choice in this battery and it concerns
unbuilt machinery — it is preregistered here as an assumption with two
sensitivity cells rather than tuned after the fact. The grid (§3a) is
anchored on the frozen exemplar bank and the re-read real ledger, not on
outcomes. No threshold tuning, no post-hoc family exceptions, no
outcome-conditioned rules. The 300 are all truth-correct by construction;
the battery's only question is how many the frozen predicate would delay.

## 10. Deliverable

Verdict: SURVIVE or KILL with measured numbers (delayed>50 / 300 under
primary, S1, S2; far-control blocked / 60; delay histogram), run SHAs,
commit SHAs, and an explicit go / no-go for the F5 live-gate build.
If killed: say so plainly with the numbers and stop — no rescue mission.
