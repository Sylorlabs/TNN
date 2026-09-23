# VERDICT_H2 — Executable Percept Programs

**Status: DEAD** — kill criterion #2 (frozen prereg §5): fewer than 90% of wrong
high-confidence percepts reach FAIL or UNRESOLVED (42/108 = 38.9%).

**Deciding bar:** Kill-2. The memory contract itself is proven load-bearing
(B4 passes decisively: 0 false permanent installs with the contract vs 186
with the contract-less ablation, 45.3% disposition difference). What fails is
the percept programs' self-calibration: when wrong with confidence ≥ 700,
only 38.9% emit FAIL/UNRESOLVED. The gate withholds all 108 from installation,
but the bar as written tests the programs, not the gate.

## Bar table (frozen denominators, full 10,000-trial evaluation)

| Bar | Criterion | Result | Verdict |
|-----|-----------|--------|---------|
| B1 | mean primary accuracy ≥ 0.60 | 0.8426 | PASS |
| B2 | head-to-head (informational) | H2=0.7913, A=0.6217 (n=9,987) | — |
| B3 | p95 ops ratio ≤ 0.40 | 0.385 | PASS |
| B4 | disposition Δ ≥ 10% AND contract false < ablation | Δ=45.3%; 0 vs 186 | PASS |
| B5 | adversarial false-perm ≤ 0.03 | 0/5,000 | PASS |
| B6 | determinism | 60×3 byte-identical, recompute valid | PASS |
| Kill 1 | false-perm / 10,000 ≤ 0.03 | 0/10,000 | PASS |
| Kill 2 | wrong high-conf → FAIL/UNRESOLVED ≥ 0.90 | 42/108 = 0.389 | **FAIL** |
| Kill 3 | adversarial accuracy ≥ 0.7125 | 0.7272 | PASS |
| Kill 4 | p95 ops ratio ≤ 0.40 | 0.385 | PASS |
| Kill 5 | byte-identity on rerun | PASS | PASS |
| Kill 6 | sensory acceptance | N/A by design | — |
| Ledger | 10,000 links, independent verify | a1a8b21f… | PASS |

## What died and why

The percept programs are overconfident. Across 10,000 trials, 108 judgments
were wrong with confidence ≥ 700; only 42 of those programs emitted FAIL or
UNRESOLVED. The frozen kill bar demands ≥90%. 38.9% is not close, and the
prereg allows no fix-and-retry. The fork dies on the calibration of its
percepts, not on its memory.

## What survives (and matters)

- **The memory contract is load-bearing.** This is the scientifically important
  result: the contract changes 45.3% of adversarial install/withhold decisions
  and installs zero falsehoods where the shared-rule ablation installs 186.
  The contract is not decoration — it is the reason the ledger holds zero
  false permanents.
- Executable percept programs as a representation: 84% accuracy at 39% of the
  raw approach's compute, deterministic, ledger-bound.
- The audit ledger machinery: 10,000 links, tamper-evident, independently verified.

## Honest caveats

- Approach A deterministically fails (`task_failed`) on 13 shapetrans fixtures;
  B2/B3 use the 9,987 A-clean trials. H2 ran all 10,000 clean. All H2 bars use
  the frozen 10,000/5,000 denominators.
- The memgate.zag source was fixed (fixture buffer aliasing) after the first
  binary build; the binary rebuilt from the committed source produces
  byte-identical ledgers and 0/10,000 disposition differences. All numbers above
  come from the committed-source binary.
- An earlier partial analysis on a biased 5,645-trial subset reported B4 as
  7 vs 2 against the contract; the complete evaluation reverses this (0 vs 186).
  The subset result is superseded and was an artifact of order-dependent gate
  state on a truncated trial sequence.
- The gate withholds 108/108 wrong high-confidence percepts from installation;
  kill-2 as written does not credit this. If the bar had tested installed
  falsehoods, H2 would live. It tests program self-flagging, and on that H2 dies.
