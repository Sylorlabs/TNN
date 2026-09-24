#!/usr/bin/env python3
"""Assemble Round 3 convergence prompts: each debater gets all four R2 rebuttals."""
import os
D = os.path.expanduser("~/workspace/tnn-lab/knowledge/web_guides/live_ingest/h3_novelty/debate")
rebuttals = {
    "a": open(f"{D}/r2_a_sol.md").read(),
    "b": open(f"{D}/r2_b_grok.md").read(),
    "c": open(f"{D}/r2_c_step.md").read(),
    "d": open(f"{D}/r2_d_swe.md").read(),
}
names = {"a": "Sol", "b": "Grok", "c": "Step", "d": "Swe"}
pos = {
    "a": "position (a): novelty = absence of a matching installed fact (ledger lookup)",
    "b": "position (b): novelty = failure of corroboration (the withhold side of the >=2-source gate)",
    "c": "position (c): novelty = surprise relative to the world-model (model-relative entailment)",
    "d": "position (d): novelty = learner uncertainty (undecided epistemic status)",
}
for me in "abcd":
    others = "\n\n".join(
        f"--- REBUTTAL {k.upper()} ({names[k]}, {pos[k]}) ---\n{rebuttals[k]}"
        for k in "abcd" if k != me
    )
    prompt = f"""You are {names[me]}, in the final round of a structured debate on novelty detection for TNN (deterministic, zero-RNG AI substrate; install rule G4 = >=2 independent sources as byte-identical normalized sentences; LI-1 pilot: 0 installs/9 withholds; red-team A2 sockpuppet closed by BUGFIX-1, A9 colluding-hosts still installs; semantic-similarity thresholds proven gameable).

YOUR position throughout: {pos[me]}.
YOUR Round 2 rebuttal is on file; below are the three rivals' Round 2 rebuttals.

ROUND 3 TASK (convergence), <=450 words total:
1. State the single strongest point made AGAINST your position across all three rounds that you accept as valid, and how it changes (or doesn't change) your position.
2. Propose the operational definition of novelty you would hand to the mechanism crew building H3 ("TNN distinguishes 'corpus had nothing new' from 'I failed to learn'"). Be concrete: what is computed, over what inputs, with what frozen vs heuristic parts. <=200 words.
3. Your confidence in that definition (0-100%) with a one-line reason.
4. What you leave open (<=3 items).

{others}
"""
    with open(f"{D}/prompts/r3_{me}.txt", "w") as f:
        f.write(prompt)
    print("wrote", f"prompts/r3_{me}.txt", len(prompt), "chars")
