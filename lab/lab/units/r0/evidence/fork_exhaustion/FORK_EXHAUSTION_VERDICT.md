# FORK-EXHAUSTION VERDICT — R-3 / R-4 / R-5

Fork-exhaustion crew · Track R0 · 2026-09-21 · branch `tnn-native-lab`
Task: Micah's order — "for the 3 recommendations you should test all paths
and all forks that appear."

## Method

For each R-number: enumerated the full candidate space (not just debated
points), tested every cell against the swarms' normative suites PLUS new
adversarial cases generated for gaps the suites didn't cover, added forks
that appeared mid-testing, and mapped the full sensitivity surface.

- R-3: 6 ε × 5 ratio floors × 5 variants (boundary ×2, chunk-conjunct ×3) = 150 cells; 11 scenarios (2 measured + 9 adversarial, 3 of them probes)
- R-4: 8 formulations × 5 tolerances × 2 boundaries = 80 cells; 18 curves (10 inherited + 8 new adversarial)
- R-5: 10 floor wordings × 4 contested rules = 40 cells; 16 scenarios (measured + D1–D7 + 8 new adversarial), deterministic 384-row battery rebuilt in-harness

Harness: `fork_exhaustion.py` — pure arithmetic on frozen formal-leg numbers
(commit 13bbaf07067e). No RNG anywhere (no `random` import; all inputs
literal); deterministic by construction. Raw per-cell outcomes: `r3_raw.json`,
`r4_raw.json`, `r5_raw.json`. Sensitivity maps: `R3/R4/R5_SENSITIVITY_MAP.md`.

No TNN-side code was written or run (nothing to compile); the "pure Zag"
requirement applies to TNN test code, and this sweep is analysis arithmetic
on already-frozen byte-identical evidence, per the swarms' precedent.

## Verdicts

| Item | Swarm recommendation | Exhaustion verdict |
|---|---|---|
| R-3 / B-T2 | ε ≤ 25/1000, ratio ≥ 1.15 | **CONFIRM** — in zero-mismatch region; ε=25 uniquely picked out by the cross-swarm materiality quantum; 1.1 fallback confirmed evidence-compatible |
| R-4 / B-T3 | max drawdown from running max ≤ 25/1000 | **CONFIRM, strengthened** — unique zero-mismatch cell in the full 8×5 grid (swarm tested 4 formulations; we tested 8) |
| R-5 / B-T4 | strict 8/8 per exposure per leg, zero contested recruitments | **CONFIRM** — unique survivor up to provable wording-equivalence; fork space closed |

No fork moved any recommendation. Details:

**R-3.** Zero-mismatch region on the inherited suite: ε ∈ {0,5,10,15,25} ×
floor ∈ {1.1, 1.15}. Killed neighbors: floor=1.0 lets the degenerate
dual-is-raw (A1) and trivial 1.02 compression (A2) pass; floor ≥1.2 rejects
leg 1's pre-registered 1.195 regime (N1); ε=50 tolerates a 6-label miss (A3);
`<` boundary fails the at-ε case (A4) and even the measured legs at ε=0;
dropping the chunk conjunct lets chunk=dual pass (A5) against the frozen
prereg. New fork that appeared mid-test — the ε-underdetermination fork:
the inherited suite can't separate ε ∈ {0..25} (Δ=0 measured). Resolved by
the materiality-quantum fork: 25/1000 = 5 probes is independently derived in
R-4 (span occurrence budget) and R-3 (probe resolution); adopting "5-label
miss passes, 6-label miss fails" as normative makes ε=25 the UNIQUE
zero-mismatch value. The 1.1-vs-1.15 choice is provably undiscoverable by any
suite (no scenario falls between them) — it stays disclosed judgment, with
1.1 as the confirmed fallback.

**R-4.** New formulations tested: endpoint-only (killed by A1/A4/A8 — blind
to interior damage), total-variation (near-miss, killed by S5 sawtooth),
recovery-allowed (killed by A1/A8 double-dip/V-shape), bleed-flag-hardened
(killed 4 ways — over-strict). New adversarial curves gave adjacent-only two
more bleed-loophole instances (A4, A7) beyond S3b, and gave cumulative-only
a third peak-blindness instance (A4) beyond T1/T2. `<` boundary killed by the
four drawdown-exactly-25 curves. F1 × 25 (≤) is the single zero-mismatch cell
out of 80.

**R-5.** New forks tested: onset-split/outcome-only wording (killed by
D7/D10 — reason codes are load-bearing, not cosmetic), pooled variants at
three slack levels (killed by D6/D11/D15 single-rep flakes), cross-leg
pooling (equivalent at 100%, killed with slack), proportional contested
leniency C3/C4 (miss single leaks by design — D5/D12 pass at the boundary).
Equivalence proof: W1 ≡ W4a ≡ W7 byte-identical across the whole grid —
pooled-100% is a restatement, not a fork. Fork-closure: every
non-equivalent fork dies on a named scenario; nothing keepable remains
untested.

## Cross-item finding

25/1000 = 5 probes emerged independently as the materiality quantum in all
three items (R-3 probe resolution, R-4 span occurrence budget, R-5's
single-case-is-a-bug under determinism). The three recommendations are
mutually consistent, not three separate round numbers.

## What Micah signs — unchanged

The three amendment texts in `R3/R4/R5_RECOMMENDATION.md` stand exactly as
the swarms wrote them. Formal B-T2/B-T3/B-T4 PASS claims remain blocked until
he signs the dated frozen-prereg amendments — this verdict changes no gates,
it only closes the fork space behind the recommended numbers.

## Files (this commit)

- `docs/lab/units/r0/evidence/fork_exhaustion/FORK_EXHAUSTION_VERDICT.md` (this file)
- `docs/lab/units/r0/evidence/fork_exhaustion/R3_SENSITIVITY_MAP.md`
- `docs/lab/units/r0/evidence/fork_exhaustion/R4_SENSITIVITY_MAP.md`
- `docs/lab/units/r0/evidence/fork_exhaustion/R5_SENSITIVITY_MAP.md`
- `docs/lab/units/r0/evidence/fork_exhaustion/fork_exhaustion.py`
- `docs/lab/units/r0/evidence/fork_exhaustion/r3_raw.json`
- `docs/lab/units/r0/evidence/fork_exhaustion/r4_raw.json`
- `docs/lab/units/r0/evidence/fork_exhaustion/r5_raw.json`
