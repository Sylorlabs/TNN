# COLLISION NOTE — R2-11 workspace (2026-09-23)

## What happened

This agent was tasked with R2-11 (R2-9-lineage fork A + generative fork B).
At task start (~08:32 PDT) the agent verified via GitHub API (no commits
under `senses/pam-rebuild/round2/forks/R2-11` on `tnn-native-lab`) and via
the local filesystem (no R2-11 directory) that no prior R2-11 state existed,
and proceeded as STARTED FRESH.

Between ~09:14 and ~09:20 PDT, the entire `forks/R2-11/` tree this agent had
built (src/forkA, src/forkB, work/ with trials.tsv, shards, build scripts,
binaries) was deleted and replaced by a DIFFERENT crew's R2-11 implementation
(integer-math percept pipeline in zag/, Python glue in src/, its own
VERDICT_R2-11.md claiming both forks KILLED on B5 at 4.15% false installs).

The other implementation's files are timestamped 09:17–09:20 PDT — after this
agent's tree was built (08:32–09:13). None of this agent's files were
recoverable (filesystem-wide find for r2-11a.zag, build_trials.py, sense_a
binaries found nothing; the /tmp backup was also gone).

## Response

Per the task ("Fork A: replay-only Witness-Emission PAM, following R2-9" —
the other crew's integer pipeline does NOT follow R2-9, so the assigned task
was not done by their work), this agent rebuilt the R2-9-lineage
implementation from the surviving frozen R2-9 source
(`forks/R2-9/src/r29.zag`, sha256
4a1a482638b42878dea48ed8c470f0847e561ac7a4e3029c1060da4ed6617e2d)
in a NON-COLLIDING directory:

    forks/R2-11-R29/

The other crew's `forks/R2-11/` was not touched. All new work (sources,
trial lists, battery runs, evidence) lives under `forks/R2-11-R29/`.

## For the parent

Two different R2-11 experiments now exist with potentially conflicting
verdicts:

- `forks/R2-11/` (other crew): shared integer-math percept; verdict = both
  forks KILLED on B5 (415/10,000 = 4.15% false installs).
- `forks/R2-11-R29/` (this agent): R2-9-lineage f64 percept pipeline; fork A
  replay emitter (R2-9 unchanged); fork B generative renderer from the
  compressed percept. Verdict pending battery completion — see
  VERDICT_R2-11.md in this directory.

The B5 numbers do NOT transfer between the two: the percept pipelines and
confidence calibrations differ. Adjudication is the parent's call.
