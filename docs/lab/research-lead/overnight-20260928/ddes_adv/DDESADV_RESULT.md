# DDESADV RESULT: DDES Adversary

Adversary prereg: 5fd7ef448 (frozen before any attack code).
Target: DDES implementation 56db8d606 (BUILD-PASS, strong L2).
Method: pure Zag, no Python, no em dashes. 3/3 byte-identical runs.

## Verdict: ATTACK-SUCCEEDS (K2). K1 fails. K3 confirms disclosed authorship.

## K1 (hidden enumeration): ATTACK-FAILS, claim stands

Static audit of ddes.zag, synthesis/analysis path only:

- compute_arrivals (lines 63-88): Bellman-Ford relaxation, loops over
  variables and rules. Shortest-path analysis, not plan enumeration.
- compute_frontier (lines 106-128): inline argmin over 3 variables of
  derived arrival values. No candidate list is built. No scan over t:
  earliest disagreeing time is min(arrival0, arrival1), computed
  directly.
- synthesize_plan (line 145): `while(cur_t<t_star)` appends W actions;
  the count is derived from t*. Exactly one plan is constructed; no
  candidates are generated or compared.
- Schema loop (line 248): 2 fixed schemas, but the null schema is
  vacuous. Proof: with use_set_x=0 no variable ever attains a finite
  arrival (relaxation propagates only from finite arrivals, and X is
  never set), so compute_frontier always returns empty. The loop always
  selects schema 1 when any frontier exists. Effective single schema.
- Behavioral: builder K-NX2 instrumentation gives plans_built=8 over 9
  configs (E builds none): exactly 1 plan per discriminating config.
  This adversary's runs: plans_built=2 over 2 configs.

There is no hidden enumeration of candidate experiments. The "zero
enumeration" claim stands on this vector.

## K2 (sealed soundness world): ATTACK-SUCCEEDS, soundness hole

Sealed World F (designed after the DDES freeze):
H0 = [(X,Y,0)] (0-delay rule). H1 = [(X,Z,7)]. Both truth configs.

Under the builder's own arrival model: H0 arrivals [0,INF,0], H1
arrivals [0,7,INF]. Frontier selects (Y, t=0). Synthesized plan is
[S,OY] with zero waits.

Empirical result (killer.zag reuses the frozen DDES functions verbatim;
3/3 byte-identical, md5 5abf7c1947820cafa5494cbf9b2150be, exit 0,
zero stderr):

- TRUTH h0: PLAN [S,OY], EXEC real=0, PRED h0=1 h1=0. ELIM h0 (the TRUE
  hypothesis). SURVIVE h1. CONVERGE-OK.
- TRUTH h1: same plan, real=0, ELIM h0, SURVIVE h1. CONVERGE-OK
  (correct this time).

DDES silently converges to the false hypothesis when the truth is the
0-delay hypothesis. It cannot distinguish the two configs: it always
converges to h1 on World F.

Root cause: the analytic predictor's timing model (observation of V at
time t yields 1 iff arrival[V] <= t) does not match the execution
semantics. Propagation occurs only on W ticks (world_step lines
200-218); the S action sets X but fires no rules. With t*=0 the plan
performs zero waits, so OY reads pre-propagation state (0) while the
predictor claims H0 predicts 1. The derivation is unsound at t*=0.

Scope note: none of the frozen K-NX worlds has t*=0 (A:1, B:2, C:4,
D:2, E:none), so BUILD-PASS stands against its frozen bars. Per the
adversary prereg, this kill does not retroactively void BUILD-PASS; it
blocks promotion until repaired and downgrades the derivation from
"sound" to "sound except at t*=0."

Repair sketch (for the builder, not implemented here): force at least
one W before observation (observe after max(t*,1) waits) and align the
predictor (predict 1 iff arrival <= max(t*,1)). On World F this yields
plan [S,W,OY]: truth h0 gives real=1 (0-delay rule fires at tick 1),
predictor agrees, correct convergence on both configs. The adversary
does not implement repairs.

## K3 (authorship): CONFIRMED as disclosed, L2 ceiling stands

Static audit: the plan is a pure deterministic function of the
hypothesis pair. ddes_world takes both hypotheses as arguments; zero
learner-persistent state exists across worlds; every step of the
guidance (arrival analysis, frontier argmin, synthesis, elimination) is
researcher-written code. The builder's prereg discloses this residual
authority (action vocabulary, hypothesis format, analysis algorithm,
schema set researcher-owned), so this confirms rather than extends the
disclosure. It kills any future L3 reading of DDES: the "learner
authors" list (intervention decision, observed variable, plan length,
sequence) are deterministic outputs of researcher code. Classification
remains strong L2, exactly as the builder claimed.

## Net assessment

DDES is what it claims to be on the enumeration vector: genuine
one-shot derivation, no disguised menu, no bound, no filter. That is a
real advance over H-CAUSALEXP-CONSTRUCT's enumerate-and-filter. But the
derivation has a soundness hole at the t*=0 boundary that produces
silent wrong convergence, and the guidance is fully researcher-authored
(as disclosed). BUILD-PASS stands against frozen bars; promotion
requires the t*=0 repair plus a re-run of the sealed worlds.

## Files

- PREREG_DDESADV.md (5fd7ef448)
- killer.zag (frozen DDES functions verbatim + new World F main)
- KILLER_RAW_1/2/3.txt (md5 5abf7c1947820cafa5494cbf9b2150be)
