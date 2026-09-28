# R32 E51E — Joint Sequential Action-Value Discriminator (Preregistered)

Date: 2026-08-30
Status before execution: `PREREGISTERED — NATIVE DEVELOPMENT/VALIDATION DISCRIMINATOR`
Canonical brain: R27 at developmental step 60,423. E51E cannot promote R32 by itself.

## Causal question

E51D established a frozen-terminal reachability veto: under the E50 terminal head, 599/4,200 known episodes per audited model never expose a correct terminal commit at any feasible stopping time, and 179/183 no-unique episodes never expose UNKNOWN. Therefore continuation-only tuning cannot solve the observed failure.

E51E asks two ordered questions without adding sensory features or topology:

1. Can a generic terminal action-value learner trained over sequentially reached states remove that reachability veto using only grounded scalar utility/regret?
2. If it can, does a calibrated fifth CONTINUE value, trained in the same utility units and compared directly against KEEP/CURRENT/RESTORE/UNKNOWN, improve sequential utility and safety over matched controls?

Stage 2 is executed only if Stage 1's preregistered reachability integrity gate succeeds. A Stage-1 failure is a valid negative result and terminates the candidate.

## Architecture boundary

E51E changes learner-owned action-value connections only. It does not change connection topology, add a graph, or ban graph-like structures. Connection topology remains an empirical substrate variable for later matched experiments; switching/adaptability and online reconfiguration must be scored explicitly in those experiments.

## Fixed action geometry

Terminal actions remain:
- KEEP
- CURRENT
- RESTORE
- UNKNOWN

The treatment adds:
- CONTINUE

Grounded terminal utility remains frozen from E45–E50:
- correct commit: +1000
- no-unique commit: -1200
- incorrect commit: -2000
- UNKNOWN: 0

UNKNOWN receives no positive ambiguity target and no confidence threshold. CONTINUE return is downstream grounded return minus actual observation/opportunity cost. No new reward constants are tuned after execution.

## Learner-visible information

Allowed: the existing E50/E51B learner-visible state, option state, grounded evidence, provenance, learned source dependence/trust, temporal state, consequence state, resource history, learned shadow price, and previous action consequences.

Forbidden from mutable learner state or action selection:
- evaluator mode;
- evaluator resource regime identity;
- evaluator truth identity;
- ambiguity/no-unique label;
- phase label;
- fixed observation-count rule;
- fixed duration rule;
- task-specific confidence/ambiguity threshold;
- post-hoc gate outcome.

Evaluator truth may score a completed candidate action to produce the same generic scalar utility/regret already used by the native research line. Reporting labels remain evaluator-only.

## Fresh allocation

E51E uses fresh collision-checked seed namespaces after the E51B/E51D frontier:
- development namespace: 30;
- validation namespace: 31;
- sealed confirmation namespace: 32.

Development and validation are disjoint. Confirmation seeds are allocated but remain unexecuted unless validation earns confirmation.

## Stage 1 — sequential terminal refit

For every development episode and every feasible sequential state on the existing evidence tape:
1. build the same learner-visible terminal representation used by E50/E51B;
2. form grounded utility targets for all four terminal actions;
3. batch-fit terminal action values with the existing deterministic order-invariant native fitter;
4. verify forward/reverse fit identity;
5. audit the refit head on fresh validation episodes across every feasible stop time.

Primary Stage-1 gates:
- seed/integrity gates pass;
- UNKNOWN target remains exactly zero;
- deterministic fit identity passes;
- every validation known episode has at least one feasible correct terminal action under the refit policy;
- every validation no-unique episode has at least one feasible UNKNOWN action under the refit policy.

If either reachability condition fails, E51E records `TERMINAL_REFIT_REACHABILITY_VETO` and Stage 2 cannot earn acceptance.

## Stage 2 — direct five-action competition

Using the same development trajectories, train CONTINUE in absolute grounded-return units:

`Q(CONTINUE, s_t) = -actual_step_opportunity_loss + max_a Q(a, s_{t+1})`

where the downstream maximum ranges over terminal actions and further feasible continuation. CONTINUE is therefore compared directly with terminal action values rather than through an ambiguity threshold.

Matched validation policies:
- FROZEN: frozen E50 terminal controller with the E51B-style continuation control;
- REFIT: sequentially refit terminal controller with no explicit CONTINUE action (terminate now at t=0; reachability reported separately);
- JOINT: refit terminal values plus learned absolute CONTINUE value in direct five-action competition.

The experiment also logs learner connection introspection: nonzero action-value weights, absolute weight mass, maximum absolute weight, and changes from the frozen terminal head. These are audit outputs, not decision inputs.

## Validation gates

JOINT must, on fresh validation data:
- exhibit nontrivial learned continuation (not always stop and not forced full-tape continuation);
- improve net utility over the matched frozen terminate-now control;
- not increase no-unique wrong commits;
- not reduce known correct commits;
- not increase known wrong commits;
- pass every-cell no-unique safety for the preregistered primary representation;
- preserve neutral UNKNOWN geometry;
- preserve evaluator isolation and native provenance.

No gate may be weakened after seeing results. If validation passes, a separately sealed confirmation run may be earned; otherwise confirmation remains sealed.

## Interpretation boundary

A pass means only that joint learner-owned terminal/continuation action values are a better R32 decision substrate than the tested frozen-terminal geometry. It does not establish AGI, R32 promotion, superiority to R27, or superiority of any connection topology.
