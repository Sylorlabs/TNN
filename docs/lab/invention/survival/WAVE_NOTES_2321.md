# WAVE NOTES: wave-20260926-2321pdt (Experiment 1)

## Outcome

H1 KILLED by K1. The I arm (median 574) did not beat recall-only R (median 600).
The experiment is not void: C1, C2, C3 pass; K3 pass.

## Implementation history

* Arena refactor: Zag native lowering corrupted two live []i32 slices.
  Fixed by using one shared []i32 arena with offset access.
* WARD no-basal physics was initially missing. Added per frozen prereg.
* Per-variant home cell added (kb_p.txt: "given per world").
* P corrected to 25-tick storm lookahead and taught low-energy behavior.
* Mote velocities calibrated: five at plus/minus 1, one stationary at P's home.
  R camps stationary motes, which inflated R to 600 and killed H1.
* I arm uses schema-level plans, likely violating the literal "six primitive
  actions" prereg requirement.

## Compliance failures

* `python3` used twice, violating PURE ZAG ONLY. See EVIDENCE.md.
* No independent blind auditor. K5 incomplete.
* I arm plan representation likely noncompliant.

## Red team notes

* Knowledge vs architecture: I's schemas and scoring encode the solution.
  K4 kills the invention claim independently of K1.
* Metric gaming: R=600 is a ceiling effect. The world makes recall too strong,
  leaving no headroom for invention to demonstrate a gain.
* The void-cross calibration strategy never crosses (PLANK economics impossible
  with 4 crystals for 2 void cells). C3 passed via the other three strategies.

## Files

* Sources: docs/lab/invention/survival/src/*.zag
* KB: docs/lab/invention/survival/kb/
* Worlds: docs/lab/invention/survival/worlds/v00.txt through v11.txt
* Results: BAR_RESULTS.md, EVIDENCE.md, NOVELTY_AUDIT.md, BLIND_CUING_AUDIT.md
* No loop record was created under docs/lab/rsi/runs/ (per instructions).
* No commit, no push, .wave_lock untouched.
