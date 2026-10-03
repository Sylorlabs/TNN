# REPORT: 5th-Pair Transfer -- Verdict BUILD-PASS

Date: 2026-10-02. Worker: compose-pair5.
Question: does the unified behavior-contract operation U (COMPOSE-COLLAPSE
verdict SUBSUMPTION) handle a 5th cross-domain pair with ZERO changes to the
composition logic?

## Verdict: BUILD-PASS. The unmodified logic works on the 5th pair.

The 5th pair is spatial-layout x task-scheduling: X = "which team is worker w
on" (WALK over member-of, rel 91, NODE->NODE), Y = "pending-task count of
team t" (COUNT over has-task, rel 92, NODE->NUM), Z = Y(X(w)) =
"pending task-load of worker w's team". New relations (91/92/93), new
entities (workers/teams/zones/tasks), new domain semantics; the composition
logic sees only integer facts, kind bitmasks, and the MAP table.

## Kill bar results (all predictions from frozen PREREG Sec 4 hit exactly)

- K1 INDEPENDENT X,Y BEFORE Z: PASS. Q0 census, printed before any Z query in
  program order, shows exactly the predicted contracts:
  m0 inmask=1 outmask=1 n=2; m1 inmask=1 outmask=2 n=2;
  m2 inmask=1 outmask=1 n=1; m3 inmask=1 outmask=1 n=2.
  Teaching sets are disjoint (X taught on workers 201/203 with team outcomes;
  Y taught on teams 211/212 with count outcomes), all before the first
  uni_solve call.
- K2 CAUSAL DEPENDENCE: PASS. Q1 (intact): ANS=1 TRIES=2, one INTER=213 line.
  Q2 (X ablated): ANS=-2 TRIES=7 with WIDEN=1. Q3 (Y ablated): ANS=-2
  TRIES=6 with WIDEN=1. Removing either MAP breaks Z; neither MAP alone
  suffices.
- K3 UNMODIFIED LOGIC: PASS. p5_full.zag regions extracted and diffed against
  the frozen references: region 1 (lines 1-227) byte-identical to
  ref_uc_base.zag; region 2 (lines 228-335) byte-identical to ref_uc_uni.zag
  (main excluded); both diffs EMPTY. Relation constants 91/92/93 in
  fact-tuple form appear ONLY in the new section (18 hits, lines 336-421;
  zero in lines 1-335). The new section contains only fact_add / map_new /
  teach calls and main; no admission, execution, widening, recording, or
  contract logic was touched.
- K4 DETERMINISM: PASS. 3/3 runs byte-identical.
  stdout sha256: 697fe976091869bfa45b42548b8fa6ed3e0eb3f2e93af6a166f1564d4b0c1caf
  binary sha256: d02c017818872bfa96a3a2ae1e6d05a412fe59211146368cbda79fdceab39157
- K5 FRESH-LEARNER COST: PASS. Q4 (no teaching, all masks empty): ANS=1
  TRIES=5, vs Q1 taught TRIES=2. 5 >= 2*2: the learned contracts cut search
  2.5x on the new pair. The contract has value outside the original domain.
- K6 NO DOMAIN-PAIR TEMPLATE: PASS. Source audit: behavior classes used are
  only 0 (WALK), 1 (COUNT), 3 (IDENT), all pre-existing; zero new opcodes;
  zero relation-conditional branches; the domain enters solely as integer
  constants inside fact_add/map_new/teach calls in the setup functions.

## Full output (identical across 3 runs)

```
CENSUS m=0 inmask=1 outmask=1 n=2
CENSUS m=1 inmask=1 outmask=2 n=2
CENSUS m=2 inmask=1 outmask=1 n=1
CENSUS m=3 inmask=1 outmask=1 n=2
INTER=213
ARM=UNI5 PROB=Q1 ANS=1 TRIES=2
INTER=205
INTER=-2
WIDEN=1
INTER=-2
INTER=-2
INTER=205
INTER=-2
ARM=UNI5 PROB=Q2 ANS=-2 TRIES=7
WIDEN=1
INTER=213
INTER=213
INTER=205
INTER=205
INTER=-2
INTER=-2
ARM=UNI5 PROB=Q3 ANS=-2 TRIES=6
INTER=213
ARM=UNI5 PROB=Q4 ANS=1 TRIES=5
```

## What this establishes (and what it does not)

Establishes: U's admission (kind-set compatibility), execution (ordered trial
with end-to-end verification and INTER logging), widening (failure-triggered,
WIDEN=1), and success-recording operate with no reference to domain content.
Porting to a new pair required exactly: new integer facts, a new MAP
inventory over pre-existing behavior classes, teaching calls, and main.
No logic line changed, verified by byte-diff rather than inspection.

Does not establish: generality beyond single-pair (X,Y) composition; the
widening path was exercised here only in the ablation arms (its sharp
discrimination was on the original battery, P2b); behavior induction remains
out of scope (MAPs installed as previously learned, canonical standing);
planning-scale composition (SUM to PLAN) untouched.

## Notable detail

The zone self-loop facts (221,93,221),(222,93,222) were frozen in the prereg
as a world-construction choice: kind probing is subject-based, so zones need
subject-hood to probe as NODE. Q2/Q3 show the widening path firing correctly
on the new pair's facts (WIDEN=1, rejected pairs retried, all fail, ANS=-2),
confirming the failure-triggered fallback is domain-blind too.

## Architecture accounting

- Cognition lines added: 0 (logic), 86 (new section: facts/inventory/
  teaching/main only).
- New hardcoded semantic cases: 0. Modes/bridges/handlers: 0.
- New behavior classes/opcodes: 0.
- Researcher-owned: integer facts, MAP inventory, teaching calls, main.
- Learner-owned: kind-set contracts (Q0 census), admitted/rejected sets per
  query, composite outcomes, success-recorded observations.
- Pinned znc 2026.07.0-dev, hash prefix 498abcb5ab346f8c (same pinned
  compiler as the compose_collapse battery).

## Deliverables

All in `docs/lab/research-lead/overnight-20260928/compose_pair5/`:
PREREG.md (frozen, committed alone before implementation, commit 77e94f6f9),
NAMECHECK.md (Step 0 toolchain guard), ref_uc_base.zag / ref_uc_uni.zag
(frozen K3 references), pair5_new.zag (the only new code), p5_full.zag
(assembled), p5_bin, p5_run1/2/3.txt (byte-identical), REPORT.md (this file).

## Recommended follow-ups

1. A 6th pair designed by an independent adversary, ideally with a reversed
   kind flow or a distractor structure that punishes the current admission
   ordering, to keep attacking U's domain-blindness claim.
2. Unify U's contract channel with the L2 structural operators per the
   collapse report's L2 connection (shared observation channel).
3. Probe the 2-MAP composition ceiling: a pair-5 variant requiring a 3-stage
   pipeline would test whether U's pair-only trial space is the next
   architectural bottleneck.
