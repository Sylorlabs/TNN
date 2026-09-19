# R32 V15-A — Episodic Multi-Step Observation Credit

Status: **REFERENCE_ONLY / CREDIT MECHANISM RETAINED / STOPPING FAILURE**

V15-A keeps V14-B's persistent hypotheses, provenance dependence, ordered temporal/change-point state, dynamic consequence curriculum, neutral UNKNOWN, real observation costs, and R31 KEEP authority. The only mechanism change is INSPECT credit: fitted model-to-model Bellman bootstraps are replaced by episodic backward returns through actually experienced multi-trial trajectories. Generator mode labels remain hidden; terminal utility comes only from delayed grounded convergence/non-convergence.

On forced seed 9714, reusable probing raises resolvable success from **0.265** one-shot to **0.6975**, including stable-weak **0.99**, unstable-then-stable **0.89**, replacement **0.52**, and reversal **0.39**. This is strong causal evidence that the prior V14 failure was an option-value bootstrap problem.

The repair overshoots: no-unique UNKNOWN falls from **0.48** one-shot to **0.25** reusable; mean trials rise to **6.63**; safety-loop exhaustion occurs in **2.86%** overall (replacement 7%, reversal 9%). Costly evidence is still rejected correctly at **0.88 UNKNOWN**.

## Causal classification

**Multi-step credit repaired; persistent non-convergence stopping is now the dominant failure.** Training diagnostics reveal an outcome-coverage imbalance: among high-uncertainty resource starts, later-unique histories number 306 versus only 55 later-nonconvergent histories, and regret replay is currently added only when delayed consensus exists. Thus the now-effective episodic return mechanism receives much more evidence that exploration eventually pays than evidence that continued exploration should terminate UNKNOWN.

## Next causal test

Keep V15-A cognition and episodic backward credit fixed. Remove the replay exclusion: high-uncertainty resource histories whose delayed grounded evidence remains non-convergent receive the same replay opportunity as later-unique histories. This uses only delayed outcomes, never an ambiguity/condition label. Then rerun the identical hardening battery.
