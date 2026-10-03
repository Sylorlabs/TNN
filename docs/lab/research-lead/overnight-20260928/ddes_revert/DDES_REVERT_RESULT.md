# DDES Law-Revert Adaptive Intervention Builder: Result

Date: 2026-09-30. Verdict: **REVERT-ADAPT-PASS**.

## What was built

`ddes_revert.zag`: an adaptive intervention planner on the time-indexed
feed protocol. Episodes carry one phase-relative passive observation each;
per-episode sealed true graphs let a change-then-revert sequence become
competing rule graphs across episodes. Four planner modes run the same
frozen case battery:

* BASE: passive filter only, withholds on ambiguity.
* ONESHOT: one derived intervention per episode, no chaining.
* ADAPT: re-filters the FULL candidate set per episode, chains up to 3
  intervention rounds per episode.
* STATIC: carries a cross-episode survivor mask with monotonic retirement
  (never restores a retired hypothesis). This is the C1-pathology
  baseline: it cannot recover from a revert.

The derivation core (arrival computation, frontier, effective waits,
plan synthesis, analytic predictor, world stepper, n-candidate survivor
frontier) is copied verbatim from `ddes_multistep.zag` at DDES-MULTISTEP-PASS
commit `7871ca6d3`. Only the protocol layer is new.

## Preregistration and governance

* Prereg committed alone: `bb319407a` ("Prereg: DDES law-revert adaptive
  planner (FROZEN; committed alone)"), containing only NAMECHECK.md and
  PREREG_DDES_REVERT.md.
* Precedence verified: `git merge-base --is-ancestor bb319407a HEAD`
  returns true; no implementation file existed in the owned path at prereg
  commit time.
* Implementation committed after the frozen verification passed (see below).
* Pure Zag, zero Python at every step. No em or en dashes in loop docs
  (checked with `worker_snippets/check_no_dash.sh`).

## Execution

* `BUILD.sh`: pinned znc at
  `/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc`.
  Build clean, 94089 byte native binary, zero Python.
* `RUN.sh`: 3 runs, all exit 0, byte-identical
  (md5 `fbb74a5536d031e8b152ac4cacfb83dc` x3). DETERMINISM-OK 3/3.
* `VERIFY.sh`: all 27 frozen prereg lines present in RUN1.txt. VERIFY-OK.

One defect was found and fixed before freezing results: the implementation
initially placed `ep_winner`/`ep_round` at offsets overlapping the STATIC
cross-episode mask (`+1056`/`+1072` instead of the documented `+1068`/
`+1084`), which corrupted survivor masks and inflated resolution counts.
After the one-line offset correction (sed `1056`->`1068`, `1072`->`1084`),
all four frozen SUMMARY lines matched exactly. The prereg trace lines were
unaffected because they do not depend on those offsets.

## Kill-bar results (frozen bar: exact SUMMARY lines + all 27 trace lines)

| Mode    | ok/total | resolved | Frozen | Result |
|---------|----------|----------|--------|--------|
| BASE    | 13/13    | 0        | 13/13, 0 | PASS |
| ONESHOT | 15/15    | 4        | 15/15, 4 | PASS |
| ADAPT   | 24/24    | 9        | 24/24, 9 | PASS |
| STATIC  | 19/19    | 9        | 19/19, 9 | PASS |

All four modes meet their frozen bars. Overall: REVERT-ADAPT-PASS.

## The revert demonstration (R1, change-then-revert, e5)

True phase graphs: P0=G0 (X->Y d1), P1=G1 (X->Z d1, Z->Y d1),
P2=G0 (revert). Passive observation per phase: Y at t=2 is 1.

ADAPT trace (from RUN1.txt):

```
ADAPT e5 P0 RESOLVED winner=h0 rounds=1
ADAPT e5 P1 RESOLVED winner=h1 rounds=2
ADAPT e5 P2 RESOLVED winner=h0 rounds=1
```

The planner tracks the law through the change and back: after the revert
it re-derives h0 in 1 round (EXEC real=1 on the Y probe) instead of
sticking with h1. Total rounds for e5: 4, as frozen.

P1 detail (the 2-round discrimination):

```
ADAPT e5 P1 ROUND 1 survivors=[h0,h1,h2] TARGET V*=1 t*=1 schema=1
ADAPT e5 P1 ROUND 1 PLAN [S,W,O(1)] built=1
ADAPT e5 P1 ROUND 1 EXEC real=0
ADAPT e5 P1 ROUND 1 PRED h0=1 h1=0 h2=0
ADAPT e5 P1 ROUND 1 ELIM h0
ADAPT e5 P1 ROUND 2 survivors=[h1,h2] TARGET V*=2 t*=1 schema=1
ADAPT e5 P1 ROUND 2 PLAN [S,W,O(2)] built=1
ADAPT e5 P1 ROUND 2 EXEC real=1
ADAPT e5 P1 ROUND 2 PRED h1=1 h2=0
ADAPT e5 P1 ROUND 2 ELIM h2
ADAPT e5 P1 RESOLVED winner=h1 rounds=2
```

## The partial-revert demonstration (R2, e6)

True phases G0, G1, G0p (X->Y d2, not a full return to d1). ADAPT:

```
ADAPT e6 P0 RESOLVED winner=h0 rounds=1
ADAPT e6 P1 RESOLVED winner=h1 rounds=2
ADAPT e6 P2 RESOLVED winner=h2 rounds=2
```

The planner identifies the partial revert as h2 (5 rounds total, as
frozen) rather than snapping back to h0. Post-resolution query Q(6,2,2)
returns 0 under the final winner h2, consistent with the true G0p graph
(Y arrival 3 > 2).

## The C1-pathology baseline (STATIC, e5)

```
STATIC e5 P0 RETIRE h1
STATIC e5 P0 RETIRE h2
STATIC e5 P0 RESOLVED winner=h0 rounds=1
STATIC e5 P1 SINGLE winner=h0 rounds=0
STATIC e5 P2 SINGLE winner=h0 rounds=0
```

STATIC retires h1 and h2 permanently in P0 and can never restore them, so
when the true law changes to G1 in P1 it misresolves to h0 without running
a single intervention round. This is the frozen predicted failure, and it
is exactly the failure mode the parallel C1 Law-Revert Attacker prereg
(`482980e9f`) models at the mechanism level: an application-level
elimination that never revisits retired hypotheses. The contrast is the
point of the family: ADAPT re-derives, STATIC cannot.

## Honest failure (R3, e7, outside-set)

True graph G3 (X->Z d1) is outside the candidate set for the passive
observation (Z,1)=1: all three candidates predict 0. All four modes emit
`DECLARE e7 P0 OUTSIDE-SET` and withhold. The intervention-level
world-outside-set guard is unreachable here (binary outcomes: one side
always matches the real observation) and remains coded only as a backstop,
as preregistered.

## Regression (e0-e4)

All ported multi-step cases reproduce their frozen expectations in every
mode: e0/e1 unambiguous probes pass through passive filtering; e2 (M1)
resolves to h2 in 2 rounds under ADAPT/STATIC; e3 (M2) resolves to h1 in
2 rounds; e4 (A) resolves to h1 in 1 round; ONESHOT fails e2/e3 as frozen
(AMBIGUOUS, no chaining) and resolves e4 in 1 round; BASE withholds on all
ambiguous episodes (13/13, resolved=0).

## What this shows, plainly

A planner that re-filters the full candidate set per episode and chains
interventions can track a law that changes and then reverts, including a
partial revert it has never seen, while a planner with monotonic
cross-episode retirement (the C1 pathology shape) demonstrably misresolves
after the change. The mechanism is white-box: every elimination names the
derived plan, the real execution, and the predicted-vs-real comparison that
killed the hypothesis. Scope stays L2: the candidate graphs are
researcher-supplied; the learner selects and re-selects among them, it does
not invent a new graph form. No L3 claim is made.

## Recommended next step

Port the revert battery onto the H-CAUSALEXP causal lane: replace the
researcher-supplied candidate graphs with graphs the causal learner itself
constructed in earlier episodes, so a change-then-revert tests whether a
*learned* structure (not a menu entry) survives a law change. That is the
cheapest experiment that moves this family from L2 selection toward the
revision half of the L3 criteria.
