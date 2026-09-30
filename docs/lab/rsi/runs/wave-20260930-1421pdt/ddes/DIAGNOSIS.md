# DIAGNOSIS: DDES t*=0 soundness hole (white-box trace)

Wave: wave-20260930-1421pdt, DDES repair worker (R3).
Target lineage: ddes.zag @ 56db8d606 (BUILD-PASS, strong L2).
Adversary evidence: e40bdfc9b (ATTACK-SUCCEEDS via K2, 3/3 identical).
Sealed World F: H0 = [(X,Y,0)] (0-delay rule). H1 = [(X,Z,7)].

## The defect, traced step by step

World F, set-X schema. Arrival analysis (compute_arrivals):
H0 arrivals: X=0, Y=0 (the 0-delay rule X->Y fires at 0+0), Z=INF.
H1 arrivals: X=0, Z=7, Y=INF.

compute_frontier: Y disagrees (0 vs INF), earliest t = min(0,INF) = 0;
Z disagrees (INF vs 7), earliest t = 7. Winner: (V*=2 (Y), t*=0).
Trace line: TARGET V*=2 t*=0 schema=1.

synthesize_plan: `while(cur_t < t_star)` with t_star=0 never iterates.
Plan = [S, OY]: zero waits. (KILLER_RAW_1.txt confirms: PLAN [S,OY].)

Execution (world_step): the S action (a==0) sets X=1 but fires NO rules
(rule firing lives only in the a==1 W branch). With zero W ticks, no
propagation ever occurs. OY then reads Y = 0: pre-propagation state.
Trace line: EXEC real=0.

predict: the analytic predictor says the observation of V* is 1 iff
arrival[V*] <= t*. For H0: arrival[Y]=0 <= 0, so PRED h0=1. For H1:
arrival[Y]=INF <= 0 is false, so PRED h1=0.

Elimination: truth is h0. p0=1 != real_obs=0, so the trace prints
ELIM h0: the TRUE hypothesis is eliminated. p1=0 == real_obs, so
SURVIVE h1. p0 != p1 and exactly one survivor, so CONVERGE-OK prints.
Silent wrong convergence: CONVERGE-OK with the false hypothesis
surviving. (KILLER_RAW_1.txt, TRUTH h0 block, verbatim.)

## Root cause (one sentence)

The analytic predictor models the observation as happening after the
propagation that t* wait ticks allow, but the execution model fires
rules only on W ticks and synthesize_plan performs exactly t* waits,
so at the boundary t*=0 the predictor claims arrival[V]<=0 is
observable while the execution reads pre-propagation state: synthesis
and prediction disagree on the effective wait count, and the
derivation is unsound exactly at t*=0.

## Why the frozen K-NX worlds were unaffected

None of the frozen K-NX worlds has t*=0 (A:1, B:2, C:4, D:2, E:none),
so every frozen plan performs at least one W tick and the predictor's
timing model matches execution there. BUILD-PASS stands against its
frozen bars; the repair must not change A-E behavior.

## Repair principle (frozen in PREREG_DDESREPAIR3.md)

Force the two models to agree on the effective wait count:
eff_waits(t*) = max(t*, 1). synthesize_plan waits while
cur_t < eff_waits(t*); predict reads 1 iff arrival[V*] <=
eff_waits(t*). On World F the plan becomes [S,W,OY]: truth h0 gives
real=1 (the 0-delay rule fires at the first tick), the predictor
agrees (0 <= 1), and both configs converge on the true hypothesis.
The derivation path additionally flags the t*=0 boundary explicitly
(FLAG TSTAR-ZERO-BOUNDARY floor=1) instead of passing through it
silently. The clamp and the flag are generic boundary conditions on
the derived scalar t*, the same kind as the existing null-schema
fallback and the n<1 guard in z_alloc: no branch on any delay value,
variable id, or world id; no new enumeration; no new modes, bridges,
handlers, or core ops (ISA ruling respected).

No em-dashes in this documentation.
