#!/usr/bin/env python3
"""Assemble Round 2 rebuttal prompts: each debater gets the three rival R1 openings."""
import os
D = os.path.expanduser("~/workspace/tnn-lab/knowledge/web_guides/live_ingest/h3_novelty/debate")
openings = {
    "a": ("position (a): novelty = absence of a matching installed fact (ledger lookup)", open(f"{D}/r1_a_sol.md").read()),
    "b": ("position (b): novelty = failure of corroboration (the withhold side of the >=2-source gate)", open(f"{D}/r1_b_grok.md").read()),
    "c": ("position (c): novelty = surprise relative to the world-model (model-relative entailment)", open(f"{D}/r1_c_step.md").read()),
    "d": ("position (d): novelty = learner uncertainty (undecided epistemic status; deterministic uncertainty is real)", open(f"{D}/r1_d_swe.md").read()),
}
names = {"a": "Sol", "b": "Grok", "c": "Step", "d": "Swe"}
for me in "abcd":
    rivals = "\n\n".join(
        f"--- RIVAL {k.upper()} {openings[k][0]} ---\n{openings[k][1]}"
        for k in "abcd" if k != me
    )
    prompt = f"""You are {names[me]}, debating novelty detection for TNN (deterministic, zero-RNG AI substrate; install rule G4 = >=2 independent sources as byte-identical normalized sentences; LI-1 pilot: 0 installs/9 withholds because live pages never repeat sentences byte-identically; red-team A2 sockpuppet closed by BUGFIX-1, A9 colluding-hosts still installs; semantic-similarity thresholds proven gameable).

YOUR position: {openings[me][0]}.

Below are the Round 1 openings of your three rivals. ROUND 2 TASK (rebuttals), <=600 words total:
1. For EACH rival, give your single strongest objection to their position (<=150 words each). Attack the position, not the author. Be specific: name the mechanism, example, or failure mode.
2. Then state the hardest objection to YOUR OWN position that you concede has genuine force (<=150 words). Steelman the other side once: what is the best reason you might be wrong?

{rivals}
"""
    with open(f"{D}/prompts/r2_{me}.txt", "w") as f:
        f.write(prompt)
    print("wrote", f"prompts/r2_{me}.txt", len(prompt), "chars")
