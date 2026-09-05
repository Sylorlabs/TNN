# E51AJ evidence and reproduction

The scientific design is `../R32_E51AJ_REPLAY_ORDER_DOSE_PREREG.md`.
`../R32_E51AJ_EXECUTION_STATUS.json` is the live operational pointer. This
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
python3 -B Research/R32_E51AJ_ANALYSIS/verify_archive.py ARCHIVE_DIRECTORY --run RUN_ID --source SOURCE_COMMIT
```

The checker validates ZIP size/digest/CRC/paths, all 65 frozen source inputs,
source/run/attempt markers, exact compiler and immutable baseline, and equality
between archived scientific verification and a fresh invocation of the frozen
parser. It never executes archived binaries. It produces IDENTITY_CHECK.json
and LOCAL_EVIDENCE_CHECK.json. Only passing complete evidence supports a result;
partial evidence must be preserved and labeled incomplete or invalid.

Common preparation is four blocks. Checkpoint 0 is the shared learned fork;
checkpoints 1–32 are continuing updates; checkpoint -1 is the zero-residual
hybrid. Every trained arm's per-replica lineage has 38,880 record presentations,
not 38,880 distinct experiences. The frozen copy has no continuing updates.
The three new populations test this changed E51AJ design, not an exact E51AI
rerun, and do not constitute cross-task or online-stopping evidence.
