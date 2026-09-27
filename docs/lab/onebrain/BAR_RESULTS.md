# Experiment 2: One-Brain Sub-Agent Dispatch : Kill-Bar Results

**Wave:** wave-20260926-2321pdt
**Date:** 2026-09-27
**Branch:** tnn-native-lab (no commit, no push)
**Prereg:** docs/lab/onebrain/PREREG.md (frozen 2026-09-27, before implementation)

## Confirmatory set (holdout)

10 problems, `problems_holdout.tsv`, frozen 2026-09-27T06:42:47Z,
sha256 `edab14df26cd0d2e27d4ba817add7e1e8dd375101d74aa6ae2201d054a19161c`
(see `results/holdout_freeze.txt`). Expected answers grounded in the
round-4 verified behaviors (ROUND4_REPORT.md, battery_round4.txt) and fixed
before the one-brain machinery ever ran on this file. 5 problems expect R1,
5 expect R2. Every problem uses the early-mislead / late-refutation ambiguity
structure: weak opposing first evidence (probe margin 20, triggers fork),
strong early evidence for the misleading reading, and a decisive attack
(weight >= 650) that refutes it late.

| Arm | Accuracy | Forked |
|-----|----------|--------|
| One-brain (shared ledger) | 10/10 (100%) | 10/10 |
| Single-deliberation baseline (deliberation-v1) | 0/10 (0%) | n/a |
| Shared-writes-off ablation | 0/10 (0%) | 10/10 |

One-brain vs baseline: 10 wins, 0 ties, 0 losses.
One-brain vs ablation: 10 wins, 0 ties, 0 losses.
Per-problem losses for one-brain: none on the holdout.

## Kill bars

| ID | Bar | Result | Numbers |
|----|-----|--------|---------|
| K1 | No parallelism benefit | PASS | One-brain 10/10 > baseline 0/10, and ablation 0/10 does not match one-brain. Neither kill conjunct holds. |
| K2 | No shared-state effect | PASS | 6/6: evidence-poison, hypothesis-poison, and isolation-control all pass on OB-01 and OB-07. Invalidating shared e6 pre-fanout flipped OB-01 R2->R1 and changed every branch's consumption; poisoning one private ledger left the other branches byte-identical. |
| K3 | Crew scaffolding | PASS (not void) | Minimal driver with no fan_out call and no fork threshold: 10/10 holdout problems fork, fork flags and verdicts identical to the full driver. The fork decision is ledger-driven inside the machinery. |
| K4 | Decorative sharing | PASS with caveat | Delete/reorder changed the fan-out trace (ledger head hash) on 3/3 problems; the shared verdict distribution {R2,R2,R2} differs from every independent branch run. Caveat: on 2/3 problems the attack-lens branch independently reached the same verdict, so verdict-level evidence is partial; trace-level evidence (K2, differing consumption sequences) is strong. |
| K5 | Non-determinism | PASS | 3 runs x 3 arms (results TSV + ledger JSONL): all 6 files byte-identical across runs. SHA-256 manifest in results/determinism_manifest.txt. |
| K6 | RNG in decision path | PASS | Grep over all .zag sources: no RNG/RNG-seed/random-device use in any decision path. The only match is a comment stating "Zero RNG". |

No bar failed. No void was required.

## Caveats (read before citing the K1 number)

1. **Narrow structure.** The holdout tests one ambiguity structure
   (early-mislead / late-refutation). The 10/10 vs 0/10 gap is large but
   the test is narrow by construction. It does not show fan-out beats
   single deliberation on all hard problems.
2. **The attack lens alone suffices here.** In the ablation, branch 1
   (strongest-attack-on-leader) independently reached the correct verdict
   on all 10 holdout problems. The experiment shows the shared channel is
   the causal carrier of the gain *within this machinery* (K2, K4, and the
   ablation's designated verdict at 0/10), not that fan-out is the only
   policy that solves these problems.
3. **Baseline is deliberately plain.** The frozen baseline is
   deliberation-v1 with payload-order consumption (deep 6, elim margin
   400). It is the prereg-specified comparator, not the strongest
   conceivable single deliberation.

## Overhead (holdout, external measurement only, never a decision input)

| Arm | Wall time (10 verdicts) | Ledger churn | Ledger ops/verdict |
|-----|------------------------|--------------|--------------------|
| Baseline | 62 ms | 4012 bytes/verdict | 6 consumes, 0 elim |
| One-brain | 51 ms | 2577 bytes/verdict | 7 consumes, 1 elim |
| Ablation | 66 ms | 4491 bytes/verdict | 11 consumes, 2 elim |

One-brain is not slower than the baseline here; the shared ledger churns
fewer bytes than either comparator because joint reconciliation replaces
per-branch duplication.

## Developmental set (NOT confirmatory)

`problems.tsv` (15 problems, sha256 `bcce980e...` after comment cleanup)
was iterated during design: all 15 were run before any freeze, and OB-15
was added after inspecting outcomes. Its numbers are developmental only
and must not be cited as preregistered evidence:

- One-brain 13/15 (forked 14/15), baseline 3/15, ablation 3/15.
- One-brain vs baseline: 11 wins, 3 ties, 1 loss (loss: OB-15, where the
  baseline was right and one-brain wrong; wrong-but-tied: OB-09).
