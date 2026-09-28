# H2 Evidence — Executable Percept Programs

**Verdict: H2 DIED on kill criterion #2 (percept overconfidence).**

The memory contract is proven load-bearing — it makes ZERO false permanent
installs against 186 for the contract-less ablation (B4 passes decisively).
But the percept programs themselves are poorly calibrated: when wrong with
high confidence, only 38.9% flag their own errors with FAIL/UNRESOLVED
(kill bar: ≥90%). Per the frozen prereg §5, the fork dies.

## CEO-plain summary

We built a system that sees images, hears sounds, and watches movement —
not as raw numbers, but as human-like percepts ("same color", "circle",
"moving left"). Each percept comes with a tiny executable program that proves
how the judgment was reached. The system also has a memory that decides which
percepts to keep permanently.

**What worked:**
- The perception is good: 84% accuracy on the frozen test set (bar was 60%).
- It's fast: uses 39% of the compute of the raw-numbers approach (bar was 40%).
- The memory contract is genuinely load-bearing: across 5,000 adversarial
  trials it changed 45% of install/withhold decisions vs the dumb baseline,
  and made ZERO false permanent installs while the baseline made 186.
- The audit ledger is intact: 10,000 hash-chained links, independently verified.

**What killed it:**
- The percept programs don't know when they're wrong. Of 108 cases where the
  system was wrong AND highly confident, only 42 programs flagged FAIL or
  UNRESOLVED. The bar demands 90%.
- The memory gate caught all 108 (none were installed), but the kill bar tests
  the programs' self-calibration, not the gate. The bar is the bar.
- Per the frozen rules, this kills the fork. We do not get to fix it and retry.

**Bottom line:** Excellent memory, overconfident eyes. The contract earned its
keep; the percept programs' calibration didn't. The fork is dead.

## Verdict table (frozen denominators; full 10,000-trial evaluation)

| Bar | Result | Threshold | Pass? |
|-----|--------|-----------|-------|
| B1 viability (mean primary accuracy) | 0.8426 | ≥0.60 | **PASS** |
| B2 head-to-head (H2 vs A, 9,987 A-clean trials) | H2=0.7913, A=0.6217, Δ=+0.1696 | informational | — |
| B3 p95 ops ratio (H2/A) | 0.385 | ≤0.40 | **PASS** |
| B4 ablation disposition-diff | 0.453 | ≥0.10 | **PASS** |
| B4 false-perm: contract vs ablation | 0 vs 186 | contract < ablation | **PASS** |
| B5 adversarial false-perm rate | 0.0000 (0/5,000) | ≤0.03 | **PASS** |
| B6 determinism (60×3 byte-identical) | PASS | — | **PASS** |
| Kill 1: false-perm / 10,000 | 0.0000 (0/10,000) | ≤0.03 | PASS |
| Kill 2: wrong high-conf → FAIL/UNRESOLVED | 0.389 (42/108) | ≥0.90 | **FAIL** |
| Kill 3: adversarial decision accuracy | 0.7272 | ≥0.7125 | PASS |
| Kill 4: p95 ops ratio | 0.385 | ≤0.40 | PASS |
| Kill 5: byte-identity on rerun | PASS | — | PASS |
| Kill 6: sensory acceptance | N/A (no output by design) | — | — |
| Ledger SHA-256 chain | verified, 10,000 links | — | **PASS** |

**Kill criterion fired:** #2. 38.9% < 90%. Fork dies.

## B1 detail (per-task primary accuracy, frozen 370)

| Task | H2 accuracy | n |
|------|-------------|---|
| colordisc | 0.7833 | 60 |
| colorconst | 0.9000 | 40 |
| shapetrans | 0.9556 | 90 |
| pitchdisc | 0.8833 | 60 |
| timbredisc | 0.7500 | 60 |
| motiondir | 0.7833 | 60 |
| **Mean (equal weights)** | **0.8426** | 370 |

## B4 detail (the contract is load-bearing)

The ablation is a contract-less gate: INSTALL a judgment unless a contradictory
judgment with ≥confidence was already installed; else WITHHOLD. Same H2
judgments, same order, per-task belief tables.

- Disposition differs on 45.3% of the 5,000 adversarial trials (≥10% required).
- False permanent installs: **0 with contract, 186 with ablation**.
- The prereg requires strictly fewer WITH the contract. 0 < 186 holds decisively.
- Conclusion: the contract is not decoration. It is the reason zero falsehoods
  were permanently installed.

## Kill-2 detail (why the fork died)

108 trials had judgment ≠ truth with confidence ≥ 700. Of those, 42 percept
programs emitted FAIL or UNRESOLVED (38.9%); 66 emitted PASS. The bar requires
≥90% to reach FAIL/UNRESOLVED.

Caveat that does not save the fork: the memory gate withheld all 108 from
installation (108/108 safe at the gate). The kill bar as written tests the
percept programs' self-flagging, and on that test H2 fails.

## Notes on the evaluation

- H2 ran all 10,000 trials clean. Approach A deterministically fails
  (`task_failed`) on 13 shapetrans fixtures; B2/B3 use the 9,987 A-clean trials.
- The memgate.zag source was fixed (fixture buffer aliasing) after the first
  binary build; the committed source rebuilds to a binary producing
  byte-identical ledgers and 0/10,000 disposition differences vs the pre-fix
  binary. All reported numbers come from the committed-source binary.
- An earlier partial analysis (5,645-trial subset, biased by an A-binary
  rebuild mid-sweep) reported B4 as 7 vs 2; that subset is superseded by this
  complete 10,000-trial evaluation.

## Artifacts

- `src/sense_h2.zag` — the percept program emitter (pure Zag, zero RNG).
- `src/memgate.zag` — the memory contract (pure Zag, SHA-256 ledger).
- `src/eval_h2.py` — the evaluation harness (test glue, not architecture).
- `src/det_h2.py` — the B6 determinism protocol (test glue).
- `src/h2_gen.py` — the frozen fixture generator.
- `evidence/metrics.json` — the numbers above.
- `evidence/LEDGER.md` — ledger construction and verification records.
- `evidence/PROGRAM_EXAMPLE.md` — a real percept program.
- `VERDICT_H2.md` — the frozen-prereg verdict.
- Prereg: commit `8def308ed68a54dd9a92633afcd8b303ebbe23f9` (branch `tnn-native-lab`),
  blob `d03c8fce20ae36639dd76d516cdad5c161803865`, verified byte-identical.
