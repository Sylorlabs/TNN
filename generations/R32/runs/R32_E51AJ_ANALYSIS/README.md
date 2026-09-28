# E51AJ — Verified evidence and reproduction

Completed run `33952427608`, attempt 1, artifact `9965575939`, scientific source
`9ea141b050599854783258d82cfa3ee02efb1fad`. Outcome:
`REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE`; retention direction:
`MIXED_OR_UNREPLICATED_RETENTION_DIRECTION`; `no_final_behavioral_tradeoff=false`.

Start with [the result](../R32_E51AJ_RESULT.md),
[complete tables](TABLES.md), [machine-readable evidence](../R32_E51AJ_EVIDENCE.json)
and [validation record](VALIDATION.md). R27 remains canonical. No new native
execution is needed or authorized to reproduce this analysis.

The scientific design is `../R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md`.
`../R32_E51AJ_EXECUTION_STATUS.json` is the closed operational record. This
directory contains analysis and independent archival checks, not learner code.
The native implementation and frozen parser are in `../R32_E51AJ_NATIVE/` and
`../../.github/scripts/e51aj_*.py`. Do not alter frozen scientific files after
the first experimental source commit or rerun consumed populations.

## Local synthetic checks

From the repository root:

```sh
python3 -B .github/scripts/e51aj_verify_test.py
python3 -B -m unittest discover -s Research/R32_E51AJ_ANALYSIS -p 'test_*.py' -v
```

These run synthetic fixtures, including a full-size artificial ledger. They
do not execute any cognitive binary or generate scientific trajectories.

## Terminal archive verification

Save terminal Actions metadata as RUN.json, JOBS.json, ARTIFACTS.json and the
exact identified ZIP as artifact.zip inside a new scoped archive directory.
Use the run and source IDs from the live execution status, not a guessed ID:

```sh
python3 -B Research/R32_E51AJ_ANALYSIS/verify_archive.py .scratch/e51aj/actions-33952427608-5H2tNi --run 33952427608 --source 9ea141b050599854783258d82cfa3ee02efb1fad
```

The checker validates ZIP size/digest/CRC/paths, all 65 frozen source inputs,
source/run/attempt markers, exact compiler and immutable baseline, and equality
between archived scientific verification and a fresh invocation of the frozen
parser. It never executes archived binaries. It produces IDENTITY_CHECK.json
and LOCAL_EVIDENCE_CHECK.json. Only passing complete evidence supports a result;
partial evidence must be preserved and labeled incomplete or invalid.

## Reproduce the checked analysis and delivery

Run from the repository root after the archive checker succeeds:

```sh
python3 -B Research/R32_E51AJ_ANALYSIS/derive.py .scratch/e51aj/actions-33952427608-5H2tNi
python3 -B Research/R32_E51AJ_ANALYSIS/tables.py
python3 -B Research/R32_E51AJ_ANALYSIS/package.py .scratch/e51aj/actions-33952427608-5H2tNi
python3 -B Research/R32_E51AJ_ANALYSIS/validate_delivery.py .scratch/e51aj/actions-33952427608-5H2tNi
```

`derive.py` checks the raw-log hash and independently reconstructs success masks,
all pooled/cohort metrics, retention and the primary flags. `tables.py` renders
the checked summary without selecting checkpoints. `package.py` requires exact
regeneration of every stored CSV, summary and Markdown table. The delivery
validator rechecks the archive, reproduces the package, verifies result hashes
and the primary table, reconciles authority/status/ledger, checks local links,
and protects all 65 scientific inputs, prior AI/AH results and Baseline V1.

| Output | Rows / content |
| --- | --- |
| [CURVE.csv](CURVE.csv) | 510 pooled arm/checkpoint panels |
| [RETENTION_MATRIX.csv](RETENTION_MATRIX.csv) | 2,040 cohort panels |
| [BASELINES.csv](BASELINES.csv) | 9 hybrid, fork and final-static rows |
| [CYCLE_ENDS.csv](CYCLE_ENDS.csv) | 135 shared-fork and full-cycle rows |
| [RETENTION.csv](RETENTION.csv) | 15 complete arm retention summaries |
| [COHORT_RETENTION.csv](COHORT_RETENTION.csv) | 60 cohort retention summaries |
| [SECONDARY_CONTRASTS.csv](SECONDARY_CONTRASTS.csv) | 12 fixed final contrasts |
| [EXPOSURE.csv](EXPOSURE.csv) | 396 preparation/continuation schedule rows |
| [PARAMETER_CHANGES.csv](PARAMETER_CHANGES.csv) | 396 actual parameter-change rows |
| [SUMMARY.json](SUMMARY.json) | Independently checked outcomes and boundaries |
| [TABLES.md](TABLES.md) | Deterministic human-readable comparisons |

The evidence package pins the local archive location, original API metadata,
artifact expiration, source and analysis hashes. The exact ZIP is local scratch
evidence, not embedded in Git; preserve it separately before cleaning scratch
or relying on expiring Actions retention. Its SHA-256 is
`a64d9060e695a73a31a2d5c134a5000da0c7e79d40903a72958c0ba022f3c735`.
For recovery while retained, fetch run/jobs/artifacts metadata for run
`33952427608` and the ZIP for verified artifact `9965575939` into a fresh scoped
directory, keeping the filenames expected above. Never substitute a rerun.

## Scientific limits

Common preparation is four blocks. Checkpoint 0 is the shared learned fork;
checkpoints 1–32 are continuing updates; checkpoint -1 is the zero-residual
hybrid. Every trained arm's per-replica lineage has 38,880 record presentations,
not 38,880 distinct experiences. The frozen copy has no continuing updates.
The three new populations test this changed E51AJ design, not an exact E51AI
rerun, and do not constitute cross-task or online-stopping evidence.

Replay's lower ever-lost and worst-simultaneous counts in every replica do not
erase its worse final losses in two replicas. A-only harms anchors in all three
populations, but does not isolate objective mismatch from generalization and
support effects. Primary-fit presentation counts exclude reverse-fit/sweep reads
and inherited-substrate reconstruction; they are not equal-compute evidence.
AJ probes 123–126, 131–134 and 139–142 are consumed development diagnostics.
