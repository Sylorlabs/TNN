You are grok-4.7 at highest reasoning effort. Be SUPER THOROUGH. Reason hard about every subquestion. Long, precise, mechanism-heavy answers are wanted; vibes are not.

## CONTEXT — TNN deliberation depth monotonicity problem

TNN is a deterministic AI system (no randomness anywhere in decision paths; pure Zag language; byte-identical reruns required). "Deliberation depth" = rounds of structured deliberation (hypothesis generation, evidence gathering, elimination) before releasing a judgment, measured by a pure-Zag harness.

VERIFIED FINDINGS (treat as ground truth):
1. No universal depth knee — accuracy-vs-depth saturation is family-dependent (some families saturate at depth 1, traps at depth 8, plateau-then-flip items still improving at depth 64).
2. OVERTHINKING items are ANTI-MONOTONE: accuracy falls 1.00 → 0.00 as depth increases — more thinking makes it confidently wrong.
3. Confidence is a deterministic function of deliberation state (a frozen margin formula); the confidence sensor is miscalibrated (clamped margin) and never fires on trap items; on items with no reasoning chain to complete, extra depth is pure confidence theater.
4. User-forced depth 1 is catastrophic on trap items (0/127 correct, all at maximum confidence).
5. The current stopping rule is a residual-flip bound: keep deliberating while the leading hypothesis's residual support keeps flipping.

MICAH'S NEW LAW: MORE DEPTH MUST NEVER MAKE IT WORSE — accuracy at depth d+1 must be ≥ accuracy at depth d, OR the system must explicitly abstain (never a confident wrong answer). "I didn't build TNN to be an overconfident machine." TNN must be SCAFFOLD-AND-RELEASE to not lie (scaffolding = the deliberation structure is temporary support that gets removed; only what stands on evidence is released).

## YOUR TASK — five parts. Answer all five, thoroughly.

### 1. YOUR RESEARCH PLAN
What would YOU do about this problem? Give your own proposed research plan: sequence of experiments, what you would measure, what preregistered bars you would set, in what order, and why. Be specific (families of items, metrics, falsification gates). This is not "run more depth sweeps" — propose the plan you think has the best chance of actually solving monotonicity, including anything unconventional.

### 2. MECHANISTIC HYPOTHESES — why does more deliberation degrade accuracy?
Rank candidate causal pathways. For each: the mechanism, why it produces anti-monotonicity specifically (not just flat performance), what it predicts about WHERE degradation happens (which item families, which depth ranges), and how you would test/discriminate it from the other hypotheses. Consider at minimum: hypothesis-set contamination (bad hypotheses entering the pool and out-competing good ones), evidence double-counting, deliberation as rationalization (reasoning that serves the current leader rather than testing it), eliminative asymmetry (it is easier to kill a correct hypothesis with one clever objection than to kill a wrong one), confidence/residual coupling, stopping-rule perversity, and any others you invent. Rank them by your estimated likelihood of being the dominant cause.

### 3. MECHANISM DESIGNS — guarantee monotonic non-degradation
Propose concrete mechanisms that GUARANTEE acc(d+1) ≥ acc(d), or force explicit abstention. Give PRECISE decision rules, not vibes — pseudocode-level if possible, deterministic, implementable in a pure deterministic language with no randomness. Cover at least:
- best-certified-answer tracking (never release anything worse than the best answer certified so far),
- rollback ratchets (depth can only move the released answer upward in certified quality),
- scaffold-and-release with non-degradation certificates (what exactly is the certificate, who checks it, what happens on check failure),
- abstention gating (exact trigger conditions for "I don't know" vs release),
- and any NOVEL designs you invent beyond these four.
For each: the exact rule, why it guarantees the law (proof sketch or invariant), and what it costs (compute, latency, coverage loss from abstentions).

### 4. PER-MECHANISM ANALYSIS
For each proposed mechanism: predicted behavior on the known anti-monotone overthinking cases (the 1.00 → 0.00 items — does the mechanism abstain, rollback, or still fail?), falsification criteria (what experimental result would kill the mechanism), failure modes (how could it still produce a confident wrong answer, or abstain pathologically), and cost.

### 5. RED-TEAM YOUR OWN PROPOSALS
Attack your own mechanisms. For each: construct the adversarial case (item family, deliberation dynamics) most likely to break it; identify hidden assumptions (e.g., about the certificate checker, about what "certified" means, about determinism under the harness); find the cheapest way an adversary (or just a pathological item) defeats the guarantee. Then either patch the mechanism or concede the residual risk explicitly.

## OUTPUT FORMAT
Number your sections 1–5 matching the task. Within section 3 and 4, give each mechanism a short name (e.g., M-BCAT, M-RATCHET...). End with a ranked shortlist: your top 3 mechanisms in order, one paragraph each on why, plus your single most-likely degradation hypothesis from section 2. Do not hedge everything — commit to rankings.
