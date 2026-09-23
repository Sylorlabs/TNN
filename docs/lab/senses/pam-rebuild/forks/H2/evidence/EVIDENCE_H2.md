# H2 Evidence — Executable Percept Programs

**Verdict: H2 DIED on B4 (contract proof).**

The memory contract does not reduce false permanent installs. It increases
them: 7 with the contract vs 2 with the contract-less ablation. Per the frozen
prereg (§5): "fork dies if B4 fails (contract is decoration)".

## CEO-plain summary

We built a system that sees images, hears sounds, and watches movement —
not as raw numbers, but as human-like percepts ("same color", "circle",
"moving left"). Each percept comes with a tiny executable program that proves
how the judgment was reached. The system also has a memory that decides which
percepts to keep permanently.

**What worked:**
- The perception is good: 84% accuracy on the frozen test set (bar was 60%).
- It's fast: uses 38% of the compute of the raw-numbers approach (bar was 40%).
- The memory rarely makes the worst mistake (permanently keeping a wrong
  percept): 0.2% on adversarial inputs (bar was 3%).

**What killed it:**
- The memory contract — the rules for deciding what to keep — was supposed to
  PROVE its value by beating a dumb baseline. It didn't. The dumb baseline
  (just "don't keep it if you've seen the opposite") made 2 permanent mistakes.
  Our fancy contract made 7. The contract is decoration, not load-bearing.
- Per the frozen rules, this kills the fork. We do not get to fix it and retry.

**Bottom line:** Good eyes and ears, but the memory rules don't earn their keep.
The fork is dead.

## Verdict table

| Bar | Result | Value | Threshold | Pass? |
|-----|--------|-------|-----------|-------|
| B1 viability (mean primary accuracy) | 0.8426 | ≥0.60 | **PASS** |
| B2 head-to-head (H2 vs A, 5,645 clean trials) | H2=0.8308, A=0.5529, Δ=+0.2779 | informational | — |
| B3 p95 ops ratio (H2/A) | 0.385 | ≤0.40 | **PASS** |
| B4 ablation disposition-diff | 0.220 | ≥0.10 | **PASS** |
| B4 false-perm: contract vs ablation | 7 vs 2 | contract < ablation | **FAIL** |
| B5 adversarial false-perm rate | 0.0021 (7/3,279) | ≤0.03 | **PASS** |
| KB1 false-perm 10k | 0.0014 (8/5,645) | ≤0.03 | **PASS** |
| KB2 wrong high-conf reach FAIL/UNRESOLVED | 0.000 (n=1) | ≥0.90 | **FAIL** |
| KB3 adversarial decision accuracy | 0.8771 | ≥0.7125 | **PASS** |
| B6 determinism (60×3 byte-identical) | PASS | — | **PASS** |
| Ledger SHA-256 chain | verified, 10,000 links | — | **PASS** |

**Kill criterion fired:** B4(b). The contract does not strictly reduce false
permanent installs vs the ablation. Fork dies.

## B1 detail (per-task primary accuracy)

| Task | H2 accuracy | n |
|------|-------------|---|
| colordisc | 0.7833 | 60 |
| colorconst | 0.9000 | 40 |
| shapetrans | 0.9556 | 90 |
| pitchdisc | 0.8833 | 60 |
| timbredisc | 0.7500 | 60 |
| motiondir | 0.7833 | 60 |
| **Mean (equal weights)** | **0.8426** | 370 |

## B4 detail (why the contract died)

The ablation is a contract-less gate: INSTALL a judgment unless a contradictory
judgment with ≥confidence was already installed; else WITHHOLD.

- Disposition differs on 22.0% of adversarial trials (≥10% required) — the
  contract DOES change decisions.
- But false permanent installs: **7 with contract, 2 with ablation**.
- The prereg requires strictly fewer WITH the contract. 7 < 2 is false.
- Conclusion: the contract changes decisions, but not for the better. It is
  decoration.

## KB2 note

Only 1 wrong high-confidence percept occurred in 5,645 clean trials. It did not
reach FAIL/UNRESOLVED. With n=1, the 0.0 rate is statistically meaningless,
but the bar (≥0.90) is not met. This is a secondary failure; B4 is the kill.

## Artifacts

- `src/sense_h2.zag` — the percept program emitter (pure Zag, zero RNG).
- `src/memgate.zag` — the memory contract (pure Zag, SHA-256 ledger).
- `src/eval_h2.py` — the evaluation harness.
- `src/h2_gen.py` — the frozen fixture generator.
- `evidence/metrics.json` — the numbers above.
- `evidence/LEDGER.md` — ledger construction and verification.
- `evidence/PROGRAM_EXAMPLE.md` — a real percept program.
- Prereg: commit `8def308ed68a54dd9a92633afcd8b303ebbe23f9` (branch `tnn-native-lab`),
  blob `d03c8fce20ae36639dd76d516cdad5c161803865`, verified byte-identical.

## What died and why

**H2 died.** The hypothesis was that executable percept programs + a memory
contract would beat raw values. The perception part worked (84% vs 60% bar,
38% of the compute). But the memory contract — the load-bearing claim that
distinguishes H2 from "just a better classifier" — failed its proof. A dumber
baseline makes fewer permanent mistakes. We do not fix and retry; the prereg
kills the fork.
