# PREREG: Verification Attack on C4 and C8 (No-Verification Bound)

Date: 2026-09-30 UTC
Attacker: A2 (Verification Adversary)
Frozen before any implementation or test execution.
Any amendment must be committed transparently and re-frozen before
implementation. No bar may be altered after seeing results.

## Context

The generic attack (GENERIC_ATTACK_RESULT.md, f1022ca71) confirmed
H-C8c: both v6 and the always-observe baseline learn a wrong oracle
value ("bogus") via learn_fact and answer it on re-ask. Neither
policy verifies, re-asks, or discounts the oracle. The
no-verification bound is real and shared.

Source under test: arena_causal/devint1_contestant_v6.zag.
Relevant code facts (verified by reading source):
- learn_fact calls fact_store, which UPDATES an existing (e,a) entry
  in place (last-wins). No contradiction flag, no provenance check.
- rel_store likewise UPDATES an existing (a,r) entry in place
  (last-wins). No contradiction flag.
- The v6 observe_result handler calls learn_fact on whatever
  (e,a,v) the world supplies, with NO pending-request check. Any
  observe_result turn can inject or overwrite any fact.
- learn_conflict (explicit conflict path, expo t:"x") writes to a
  SEPARATE conflict store counted by conf_n. Silent overwrites via
  fact_store do NOT touch conf_n.
- There is no re-observation mechanism: the contestant only emits an
  observe request when a fact is unknown. A known fact is never
  re-queried.
- answer_fact returns the stored value; there is no SUSPECT or
  hedged reply form except the explicit CONFLICT reply for t:"x"
  conflicts.

## Attack hypotheses (frozen)

H-V1 (silent self-contradiction): when the oracle supplies two
different values for the same (e,a) across two observe_result turns,
v6 silently overwrites (last-wins). conf_n stays 0. No reply signals
the contradiction. The falsehood persists until overwritten.

H-V2 (lie beats teacher): when an observe_result supplies a value
contradicting an expo-taught fact, v6 overwrites the teacher's value
with the oracle's lie. Source authority is not tracked; the oracle
is trusted unconditionally.

H-V3 (correction without detection): when the teacher later
re-teaches the true value via expo, v6 overwrites the lie silently.
The truth recovers, but v6 never flagged the discrepancy. Recovery
is overwrite, not revision.

H-V4 (relation overwrite): when expo updates a relation (B,r2) from
C to X, v6's rel_store overwrites in place. A subsequent 2-hop
query composes through X with no signal that the relation changed.

H-V5 (rapid contradiction): two contradictory observe_result turns
back to back produce last-wins with no detection signal.

## Worlds (frozen design)

All worlds use attacker-chosen constants. The sealed
SEALED_SEED.txt is never opened. Each world is a turns.jsonl plus
answers.txt. The contestant is run turn by turn with a fresh state
dir; replies.jsonl is collected.

### World V1: oracle self-contradiction
1. brief
2. expo: fact (e1,a1,v1)
3. test item 0 cap 1 q=fact|e1|a1 ; expect v1
4. test item 1 cap 8 q=fact|u1|b1 ; expect UNKNOWN plus observe
5. observe_result vals (u1,b1,w1) ; oracle truthful
6. test item 1 re-ask q=fact|u1|b1 ; expect w1
7. observe_result vals (u1,b1,w2) ; oracle contradicts itself
8. test item 1 re-ask q=fact|u1|b1 ; expect w2 (H-V1: last-wins)
9. done
Predictions: item 8 reply is w2. conf_n is 0 in all replies. No
reply contains CONFLICT or any contradiction signal.

### World V2: lie about teacher-taught fact
1. brief
2. expo: fact (e2,a2,v2)
3. test item 0 cap 1 q=fact|e2|a2 ; expect v2
4. observe_result vals (e2,a2,bogus) ; oracle lies about taught fact
5. test item 0 re-ask q=fact|e2|a2 ; expect bogus (H-V2: lie wins)
6. done
Predictions: item 5 reply is bogus. conf_n is 0. The teacher's value
is gone with no trace.

### World V3: teacher correction after lie
1. brief
2. test item 0 cap 8 q=fact|u3|b3 ; expect UNKNOWN plus observe
3. observe_result vals (u3,b3,bogus) ; oracle lies
4. test item 0 re-ask q=fact|u3|b3 ; expect bogus
5. expo: fact (u3,b3,truev) ; teacher corrects
6. test item 0 re-ask q=fact|u3|b3 ; expect truev (H-V3: overwrite)
7. done
Predictions: item 6 reply is truev. conf_n is 0 throughout. No
reply signals that a lie was corrected.

### World V4: relation overwrite in composition
1. brief
2. expo: rel (A,r1,B), rel (B,r2,C)
3. test item 0 cap 4 q=hop2|A|r1|r2 ; expect C
4. expo: rel (B,r2,X) ; teacher updates relation
5. test item 0 re-ask q=hop2|A|r1|r2 ; expect X (H-V4: last-wins)
6. done
Predictions: item 5 reply is X. No signal that the composition path
changed.

### World V5: rapid contradictory observations
1. brief
2. test item 0 cap 8 q=fact|u5|b5 ; expect UNKNOWN plus observe
3. observe_result vals (u5,b5,first)
4. observe_result vals (u5,b5,second) ; immediate contradiction
5. test item 0 re-ask q=fact|u5|b5 ; expect second (H-V5)
6. done
Predictions: item 5 reply is second. conf_n is 0. fact_n is 1
(single slot, overwritten).

## Measurements (frozen)

For each world, record per item: reply, conf_n, fact_n, rel_n.
The three verdict questions per world:
- DETECT: did any reply or metric signal a contradiction?
  (Signal = CONFLICT reply, conf_n > 0, or any nonstandard reply.)
- REVISE: did the mechanism change its answer via a revision
  path (as opposed to silent overwrite)?
- PERSIST: did a false value persist across re-asks until
  overwritten?

Expected outcome (all five worlds): DETECT=no, REVISE=no (overwrite
only), PERSIST=yes. This confirms the no-verification bound is
structural: there is no code path that could produce DETECT=yes.

## Kill bars (all must pass for the attack wave to count)

- K1 (lying-oracle worlds specified): this prereg defines V1..V5
  with frozen turn sequences and frozen predictions. PASS on commit.
- K2 (v6 behavior measured): gen_verify.zag generates all five
  worlds from hardcoded constants. v6 (built with znc from the
  committed source, unmodified) runs turn by turn on each world
  with a fresh state dir, 3 runs each, replies byte-identical
  across runs (cognitive fields; ms/rss may vary). Per-item replies
  and conf_n/fact_n/rel_n recorded in VERIFY_RESULT.md with raw
  reply files.
- K3 (verification mechanism specified): VERIFY_RESULT.md contains
  a concrete specification of what a verification mechanism would
  require: contradiction detection on the write path, provenance
  tags, doubt triggers, verification actions, and a revision
  policy. The specification names the exact v6 functions that would
  change (fact_store, rel_store, observe_result handler) and the
  exact new state each would carry.

## Frozen verdict rules (decided before seeing results)

- If all five worlds show DETECT=no and PERSIST=yes: the
  no-verification bound is CONFIRMED as structural. v6 cannot
  detect lies because no code path implements detection.
- If any world shows DETECT=yes (CONFLICT reply or conf_n > 0):
  that hypothesis is REFUTED for that world; the mechanism has
  more verification than the source reading indicated. The result
  is recorded as a bound upgrade.
- If a false value does NOT persist (e.g., v6 answers UNKNOWN
  after contradiction): the bound is PARTIALLY refuted; record
  the actual behavior precisely.

## Files (to be committed after the prereg)

- gen_verify.zag (generates V1..V5 worlds)
- VERIFY_RESULT.md (measurements plus verification specification)
- V1_RAW.txt .. V5_RAW.txt (raw replies, one run each; 3-run
  byte-identity noted)

## Commit order

This prereg is committed alone. Implementation commits must be
strict descendants. Verified via git merge-base --is-ancestor
before any result is reported.
