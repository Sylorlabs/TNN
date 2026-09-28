# E51AI reproducible analysis

These files analyze one completed native exploratory run. They do not train,
select, promote, or rerun a learner. Authoritative interpretation:
[E51AI result](../R32_E51AI_RESULT.md). Full identities and checks:
[E51AI evidence](../R32_E51AI_EVIDENCE.json).

## Preserved source evidence

Repository: `Sylorlabs/TNN`; scientific source
`c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22`; Actions run `33949274757`,
attempt 1, job `101260866273`, artifact `9964554609`.

The exact 4,823,283-byte ZIP and API metadata are preserved locally at
`.scratch/e51ai/actions-33949274757-k1tM4Q/`. The directory contains `RUN.json`,
`JOBS.json`, `ARTIFACTS.json`, `artifact.zip`, and `extracted/RAW.log`.
ZIP SHA-256 is `80c049ff197d7d466b694baf1a2611f1e3535de78a0ee5faa66ebdf3de121c6e`.
GitHub reports expiration `2026-12-04T06:14:32Z`; the preserved local ZIP is
therefore important. It is intentionally not a versioned binary in this commit.
A fresh clone needs this exact ZIP plus its original metadata before reproduction.

## Reproduce from the repository root

```sh
python3 -B Research/R32_E51AI_ANALYSIS/verify_archive.py .scratch/e51ai/actions-33949274757-k1tM4Q
python3 -B Research/R32_E51AI_ANALYSIS/derive.py .scratch/e51ai/actions-33949274757-k1tM4Q Research/R32_E51AI_ANALYSIS
python3 -B Research/R32_E51AI_ANALYSIS/package.py .scratch/e51ai/actions-33949274757-k1tM4Q
python3 -B -m unittest discover -s Research/R32_E51AI_ANALYSIS -p 'test_*.py' -v
python3 -B .github/scripts/e51ai_verify_test.py
python3 -B Research/R32_E51AI_ANALYSIS/validate_delivery.py
```

Use Python 3.10+ standard library. The archive verifier checks the exact commit,
tree, run, attempt, ZIP size/digest/path/CRC, 53 source inputs, compiler pin,
immutable baseline, and two identical binaries. It reruns the frozen verifier
and requires equality with the report archived by the native workflow. It
does not execute the experiment binaries. The descriptive analysis reads only
verified logs. Packaging independently recomputes retention with episode-key
sets, checks every saved analysis table against deterministic regeneration,
and records hashes. The read-only delivery check also reconciles the result
tables and current authority, checks local links, and verifies that all frozen
scientific input files remain unchanged. Tests are synthetic fixtures, not
experimental evidence.

## Data dictionary

| File | Grain and scope |
| --- | --- |
| `CURVE.csv` | 132 rows: checkpoints 0–32 × four arms, pooled across four probe cohorts. |
| `RETENTION_MATRIX.csv` | 528 rows: checkpoint × arm × probe cohort; blank anchor denominator before first encounter. |
| `POINTWISE_RETENTION.csv` | 16 rows: arm × cohort; anchor successes ever lost, never lost, regained at final, and missing at final. |
| `CYCLE_ENDS.csv` | 36 rows: baseline plus all eight cycle endpoints × four arms. |
| `PARAMETER_CHANGES.csv` | 128 rows: exact coefficient changes and accepted fit updates for each continuing block/arm. |
| `EXPOSURE.csv` | 128 rows: current and prior-cohort training-record presentations, separated from optimizer work. |
| `SHARED_ANCHOR_REPLAY.csv` | Eight supplemental rows: arms 1 and 3 measured on the intersection of their first-encounter success sets. |
| `SUMMARY.json` | All final contrasts, retention summaries, exposure and parameter counts, and interpretation limits. |

Each pooled checkpoint contains 2,160 probes: 1,680 known and 480 no-unique.
Each cohort contains 540: 420 known and 120 no-unique. A reachable success
means that a successful resource-feasible state exists; it is not an online
stopping result. `union` is evaluator-only support; `hybrid` is the deployable
frozen score-max control. Their lost/rescued columns are pointwise comparisons.

`t0success`, `t0unknown`, and `t0wrong` partition all 2,160 initial decisions.
`t0unknown` means unsuccessful UNKNOWN, not every UNKNOWN choice. Correct
UNKNOWN is already included in `t0success`.

First-encounter anchor for cohort j is checkpoint j+1. The pooled anchor mixes
four fixed checkpoints and differs across arms. It is not an acquired-competence
threshold. `ever_lost = regained_at_final + missing_at_final`; gains outside the
anchor set do not count as retention. A later zero-loss checkpoint is not
necessarily a same-cohort return or sustained recovery. Shared-anchor replay
arithmetic is supplemental and does not replace the frozen primary comparison.

Coefficient-change counts compare all 130 actual integer coefficients, not just
compact hashes. Fit loss is specific to that block's training support, so
cross-block losses do not describe one fixed objective. Record presentations,
four sweeps per head, reverse-traversal verification, backtracking work and
accepted coordinate updates are separate quantities. Matching record counts
does not demonstrate equal active computation.

No experimental source, frozen verifier, preregistration, workflow, compiler,
or Baseline V1 is modified by this analysis. All 115–118 probes are consumed
development evidence and must not later be reused as fresh validation.
