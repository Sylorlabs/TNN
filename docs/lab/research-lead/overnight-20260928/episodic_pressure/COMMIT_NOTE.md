# COMMIT NOTE: episodic-pressure implementation + evidence

Date: 2026-09-30 PDT.
Worker: Episodic-Pressure Worker.

## Verdict

**EPISODIC-PRESSURE-BLEED**

## What happened

The implementation and evidence files for this experiment
(`episodic.zag`, `EPISODIC_RESULT.md`, `EPISODIC_RUN1/2/3.txt`,
`EPISODIC_RUN1/2/3.err`) were staged under the owned pathspec
`docs/lab/research-lead/overnight-20260928/episodic_pressure/` and were
committed inside 9c6ee8ba8, a concurrent worker's commit ("Red team:
threshold mechanism attacked; REDTEAM-THRESHOLD-BREAK"). That commit
carries the other worker's message, not this experiment's verdict.

## Verification

- All 8 files committed in 9c6ee8ba8 are blob-identical to the staged
  evidence (checked with git rev-parse vs git hash-object on
  episodic.zag, EPISODIC_RESULT.md, EPISODIC_RUN1.txt: all MATCH).
- The committed `episodic.zag` contains the corrected 12-query E0 setup
  (12x `c1r=c1r+1`); the committed RUN files are the corrected 3/3 runs
  (sha256 d12dffa34a04f9861a5adb012f51c9c4c52ecc793346dd707296921c714d6c91).
- K1 holds structurally: prereg 2e0c6ed10 ("Prereg: episodic-pressure
  experiment FROZEN", committed alone) is an ancestor of 9c6ee8ba8
  (verified with git merge-base --is-ancestor), and no implementation
  file existed before the prereg commit.
- The contaminated paper was never touched (empty diff, never staged).

## Result summary

Three separated 30-item pressure waves with inter-wave earning:
sleepers 9/10 -> 8/10 -> 7/10 per episode (every frozen prediction
matched exactly, including per-episode first-eviction victims
(40,20), (41,20), (42,20) and the door-slot churn sequences);
cumulative 7/10 < 9/10 single-wave baseline; earned flood 100%
survival; final probes 3/3; compositions 4/4; foundation 12/12;
3/3 byte-identical, exit 0, zero stderr; pure Zag; dash-clean.
Full analysis in EPISODIC_RESULT.md in this directory.
