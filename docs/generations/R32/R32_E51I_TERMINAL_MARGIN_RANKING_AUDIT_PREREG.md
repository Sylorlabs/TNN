# R32 E51I — Terminal Margin and Ranking Geometry Audit

Date frozen: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Why this audit is next

E51F ruled out exact feature aliasing. E51G showed that sparse learner-selected pairwise and piecewise residual capacity did not remove the reachability veto. E51H showed that replacing absolute utility regression with neutral-relative sign/preference targets also did not rescue the frontier.

Before any topology rewrite, E51I asks what the remaining failures actually are in score geometry:

1. **calibration/sign failures** — the correct commit action is top-ranked among commits somewhere, but UNKNOWN wins because all commit values are too low; or
2. **ranking failures** — no stopping point ever makes a correct commit action top-ranked among the commit alternatives; and
3. whether any single evaluator-only uniform shift applied to all commit values could simultaneously make every known episode reachable and every no-unique episode safely UNKNOWN-reachable.

This is a diagnostic only. Any oracle/calibration quantities are evaluator-side measurements and are never fed to the learner.

## Fresh partitions

- stage 40: development, 3,240 episodes / 55,080 states, used only to fit the frozen absolute-utility linear terminal head;
- stage 41: validation, 5,400 episodes / 91,800 states, used for the audit;
- stage 42: confirmation allocated 10,800 and left sealed.

## Frozen learner

Use the E51E/E51G primary 32-feature evaluator-blind terminal state and the existing deterministic absolute-utility linear batch fit. UNKNOWN target and learned parameters must remain exactly zero.

No nonlinear additions, confidence rules, topology changes, graph structure, or validation-selected learner parameters are permitted.

## Exact diagnostic quantities

For each validation state compute the frozen commit scores KEEP/CURRENT/RESTORE and neutral UNKNOWN score 0.

### No-unique episode margin

For each no-unique episode define `m_nu` as the minimum across its feasible stopping states of the highest commit score. A uniform commit shift `s` makes UNKNOWN reachable in that episode iff `m_nu + s < 0` (strict because terminal tie-breaking leaves a commit selected at score 0).

### Known episode ranking and margin

At each state identify the top-ranked commit under the frozen scores. Mark whether that top commit has grounded terminal utility +1000. For each known episode:

- `rank_reachable = 1` iff at least one stopping state has a top-ranked commit whose grounded utility is +1000;
- `c_known` is the maximum top-commit score across those correct-top states.

A uniform shift can make a correct commit reachable in that episode iff `rank_reachable = 1` and `c_known + s >= 0`.

### Exact uniform-shift feasibility

Across all known episodes compute the smallest integer lower bound on `s` required to expose at least one correct top-ranked commit. Across all no-unique episodes compute the strict integer upper bound required to expose UNKNOWN in every episode.

Report whether the intersection is nonempty. This is an exact diagnostic for the family of **uniform commit-value calibration shifts**; it is not a learned rescue and cannot promote R32.

## Required outputs

- baseline known and no-unique reachability;
- known episodes with no correct commit ever top-ranked;
- known episodes that are ranking-capable but blocked only by UNKNOWN/sign calibration;
- no-unique episodes blocked by positive commit margin;
- distributions/buckets of the relevant margins;
- exact all-known lower shift bound;
- exact all-no-unique strict upper shift bound;
- whether a uniform shift can satisfy both exact reachability requirements;
- sealed confirmation executed = 0;
- forward/reverse batch identity and native byte-identical builds.

## Interpretation

- If a uniform shift has a nonempty exact interval and ranking failures are zero, the next learner experiment should learn generic calibration from development utility rather than change representation/topology.
- If the uniform interval is empty but ranking failures are zero, the residual is heterogeneous calibration and the next experiment should test learner-owned state-dependent calibration.
- If known ranking failures are nonzero, terminal action ordering itself remains wrong on some trajectories; the next experiment should target action-ranking credit/decision loss on the same state before topology.
- Only after these same-state decision mechanisms plateau is a connection-topology comparison justified.

No E51I result can promote R32 or establish AGI.
