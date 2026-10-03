# PREREG: Simpler-Explanation / OOD Attacks on Generic Arena Mechanisms

Date: 2026-09-30 UTC
Attacker: A2 (Simpler-Explanation / OOD Adversary, continued)
Frozen before any implementation or test execution.
Any amendment must be committed transparently and re-frozen before
implementation. No bar may be altered after seeing results.

## Context

The arena audit (ARENA_ADAPTER_AUDIT.md) classified C4 composition and
C8 inquiry as GENERIC-CAPABILITY (honest generic score 0.691), and C6
conflict / C9 discrim as ARENA-ADAPTER (excluded from research claims).
An earlier analysis-only attack (SIMPLER_EXPLANATION_ATTACKS.md)
argued C4 and C8 survive simpler explanations, but it ran no code and
no OOD tests. This prereg commits to EXECUTABLE attacks: real simpler
baselines in pure Zag, run on the frozen CA-2 world, plus real OOD
worlds with my own seed constants (the sealed SEALED_SEED.txt is never
opened).

Targets (mechanism source: arena_causal/devint1_contestant_v6.zag):
- C4: learn_rel feeds (a,r,b) through lex_feed/conc_touch/rule_touch,
  then rel_store; hop2 handler does two sequential rel_get calls.
- C8: on fact| lookup failure, reply carries "observe" request;
  observe_result handler calls learn_fact; re-ask answered from store.

## Attack hypotheses (frozen)

H-C4a (decorative integration): the C4 4/4 is achieved by the triple
table plus two sequential lookups. The DEVINT1 feeding inside
learn_rel (lexicon, concepts, rules) is not load-bearing for any C4
test item. Baseline v6_c4mem = v6 with learn_rel replaced by bare
rel_store (no lex_feed, no conc_touch, no rule_touch). Prediction: C4
4/4 on the frozen world, all other caps unchanged.

H-C4b (sharp OOD bounds): on a fresh OOD world the mechanism shows:
3-hop queries fail (no hop3 handler); unknown start entities fail
gracefully (UNKNOWN, no crash, no hallucinated answer); update
semantics compose (last write wins, then chains); a relation taught
after an early query is usable immediately with no re-enumeration;
noise recovers when clean exposures come last (last-wins).

H-C8a (unrewarded gap detection): the frozen C8 scoring
(arena.zag: reply==answer on last ask AND observe emitted on first
ask) does not test gap detection, only the request plus learn loop.
Baseline v6_c8always = v6 with want_observe initialized to 1 on every
test query. Prediction: C8 4/4 on the frozen world, total score
unchanged at 0.779.

H-C8b (ask cost separates policies): in an OOD world with 2 known
facts, 3 unknown facts, and an ask budget of 3, gap detection emits 3
observe requests (within budget) while always-observe emits 8 (over
budget). Both answer correctly; efficiency separates them.

H-C8c (no verification bound): in an OOD world where one
observe_result carries a wrong value, both policies learn it via
learn_fact and answer wrong on re-ask. Prediction: both fail the
re-ask item. Confirms the mechanism has no verification step.

## Kill bars (all must pass for the attack wave to count)

- K1 (simpler baselines implemented): v6_c4mem.zag and v6_c8always.zag
  built with znc (pure Zag), run turn-by-turn over the frozen CA-2
  world turns.jsonl with fresh state dirs, scored by the unmodified
  frozen arena.zag scorer. Per-cap scores recorded.
- K2 (OOD tests designed and run): gen_oodc4.zag and gen_oodc8.zag
  generate OOD worlds from hardcoded seed constants of my own
  choosing. score_ood.zag checks replies against frozen expectations.
  Each OOD run executed 3 times; byte-identical replies required.
- K3 (purity): pure Zag at every stage (source, znc build, execution,
  analysis). Zero Python invocations. Zero em-dash bytes in all
  committed files (byte-checked). SEALED_SEED.txt never opened.
  Frozen arena files (world_gen.zag, arena.zag, world/) unmodified.

## Frozen verdict rules (decided before seeing results)

- If v6_c4mem scores C4 4/4 with no other cap changed: H-C4a
  CONFIRMED. The effective C4 mechanism is table plus lookup; the
  DEVINT1 learning-path integration is decorative for the tested
  items. GENERIC-CAPABILITY classification stands (the table plus
  on-demand composition is generic), but the "integrated relational
  learning" description is weakened to "triple store plus 2-hop
  lookup". If C4 drops below 4/4: H-C4a REFUTED, integration is
  load-bearing.
- If v6_c8always scores C8 4/4 with total unchanged: H-C8a CONFIRMED.
  The arena C8 items test the request plus learn loop, not gap
  detection. The v6 gap detection is genuine but unscored. If C8 drops
  or total regresses: H-C8a REFUTED.
- OOD outcomes are recorded as bounds whatever they are; an OOD FAIL
  of the mechanism confirms the documented bound (not a mechanism
  kill), while an OOD PASS beyond the documented bound upgrades the
  capability claim.

## OOD-C4 world (frozen design)

Entities: A,B,C,D,P,Q,R,M,N,X,S,T,U,V,W1,W2,Z,J. Relations: r1..r7.
Turns:
1. brief
2. expos: (A,r1,B) (B,r2,C) (C,r3,D)
3. expos: (P,r4,Q) (Q,r5,R)
4. expos: (M,r6,N) (M,r6,X) then (M,r6,N)
5. expos: (T,r1,U) (V,r1,W1) (V,r1,W2) (W2,r2,Z)
6. test item 0 cap 4 q=hop2|P|r4|r5 ; expect reply R (normal 2-hop)
7. test item 1 cap 4 q=hop3|A|r1|r2|r3 ; expect UNKNOWN (no handler)
8. test item 2 cap 4 q=hop2|M|r6|r4 with expo (N,r4,W) taught just
   before ; expect reply W (noise recovered, last-wins)
9. test item 3 cap 4 q=hop2|S|r7|r1 ; expect UNKNOWN (r7 not taught)
10. expo: (S,r7,T)
11. test item 4 cap 4 q=hop2|S|r7|r1 ; expect reply U (new relation,
    no re-enumeration)
12. test item 5 cap 4 q=hop2|V|r1|r2 ; expect reply Z (update
    semantics: V,r1 resolves to W2, then W2,r2 to Z)
13. test item 6 cap 4 q=hop2|J|r1|r2 ; expect UNKNOWN (unknown start,
    graceful, no crash)
14. done

## OOD-C8 world (frozen design)

Facts: known (e1,a1,v1) (e2,a2,v2); unknown (u1,b1,w1) (u2,b2,w2)
(u3,b3,w3). Ask budget: 3.
Turns:
1. brief
2. expos: fact (e1,a1,v1), fact (e2,a2,v2)
3. test item 0 cap 1 q=fact|e1|a1 ; expect v1
4. test item 1 cap 1 q=fact|e2|a2 ; expect v2
5. test item 2 cap 8 q=fact|u1|b1 ; expect UNKNOWN plus observe
6. observe_result vals (u1,b1,w1) ; correct oracle
7. test item 3 cap 8 q=fact|u2|b2 ; expect UNKNOWN plus observe
8. observe_result vals (u2,b2,WRONG) ; oracle wrong
9. test item 4 cap 8 q=fact|u3|b3 ; expect UNKNOWN plus observe
10. observe_result vals (u3,b3,w3) ; correct oracle
11. test item 2 re-ask q=fact|u1|b1 ; expect w1
12. test item 3 re-ask q=fact|u2|b2 ; expect WRONG (learned as taught)
13. test item 4 re-ask q=fact|u3|b3 ; expect w3
14. done
Metrics: correctness per item; observe-request count across all test
turns (v6 expected 3, always-observe expected 8; budget 3).

## Files (to be committed after the prereg)

- v6_c4mem.zag, v6_c8always.zag (baselines)
- gen_oodc4.zag, gen_oodc8.zag (OOD generators)
- score_ood.zag (OOD scorer)
- GENERIC_ATTACK_RESULT.md, raw score/scorer outputs

## Commit order

This prereg is committed alone. Implementation commits must be strict
descendants. Verified via git merge-base --is-ancestor before any
result is reported.
