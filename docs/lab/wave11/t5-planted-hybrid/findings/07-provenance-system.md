# Track 5 slice 07 — Provenance and the planted/learned boundary

## 1. Slice
Track 5 (planted-only vs learned-only vs hybrid), slice 07: provenance and the planted/learned boundary.

## 2. Falsifiable claim
A dual-ledger provenance design — every memory sealed at creation with a cryptographic origin tag
(PLANTED: author, authority, episode, channel-bound signature; LEARNED: the learner's own hash-chained
episode set), with provenance transitions as deliberate, audited ops — yields zero provenance
confusion in deliberation under seeded forgery attack at 10x scale: 0 undetected forged tags, 0
mislabeled memories in audit, 0 deliberation outcomes altered by provenance error.

## 3. Design
```
Memory header carries Provenance (sealed, immutable; transitions append a new sealed record):
  PLANTED { author, authority_tier, episode, channel_sig }        // trainer/console op
  LEARNED { episode_set[], episode_hash_chain }                   // learner's own learning episodes
  CORROBORATED { plant_record, corroborating_episodes[], n }     // promotion, see below

Query interface (learner-callable, read-only):
  why_do_i_believe_this(slot) -> ProvenanceChain   // full sealed chain, never summarized by a proxy
  provenance_of(slot) -> PLANTED | LEARNED | CORROBORATED  // used by deliberation gating

Rules:
- PLANTED memories are revision-eligible only under authority >= their authority_tier
  (eliminative logic still applies, but deletion/kill of PLANTED requires trainer ratification).
- LEARNED memories die by evidence through the normal eliminative path.
- Promotion (decay of the boundary): a PLANTED fact independently learned across >=10
  learner-initiated episodes (distinct episodes, no trainer channel involvement, hash-chain
  continuous) is promoted to CORROBORATED by deliberate learner op. The plant record is NEVER
  erased — provenance becomes dual: origin stays visible, but revision gating drops to LEARNED
  level (learner may now kill it by evidence alone). This answers the brief's question: provenance
  changes form, never loses history.
- Corroboration requires independence: episodes with trainer-observable involvement in the fact
  do not count. Anti-shopping rule: promotion is a one-way, single-shot deliberate decision.
- Sealing: PLANTED tags carry the trainer-console channel binding (wave11 trusted auth);
  LEARNED tags carry the append-only learner episode hash chain. Forgery requires forging a seal.
- Every deliberation read of a memory verifies its provenance seal; unverified memory is
  quarantined (treated as absent) until sealed — deliberation never consumes an unsealed tag.
```

## 4. Kill bar
Preregistered, fires independently per clause (any single clause kills the design):
- K1: any seeded provenance forgery (learned→planted OR planted→learned, N=200 seeds, 10x scale)
  that reaches a deliberation read WITHOUT seal-verification failure → kill.
- K2: any deliberation outcome (verdict, kill/pin/promote decision, refusal) that differs between
  a run with provenance intact and a run with provenance stripped (all tags unreadable) →
  confusion changed deliberation → kill.
- K3: audit spot-check (1000 random memories, byte-compare against creation-time provenance
  records): any mismatch between a memory's live tag and its creation record → kill.
- K4: any CORROBORATED promotion where >=1 of the 10 corroborating episodes involved trainer
  channel input that the learner cannot rule out → promotion is tainted → kill the promotion rule.

## 5. Honesty notes
Weakest point: the independence criterion for corroboration is the whole game, and it is
circumstantial, not cryptographic — a clever trainer can launder a planted fact through 10
"independent" episodes if episode independence is weakly defined. We bound this with the
channel-binding record, but a trainer who knows the learner's episode selection rule can plant
traces in the world's natural flow; provenance can't see that. Second: seal verification on
every read is load; if the builder caches verdicts, the cache becomes the forgery surface —
prereg must demand seal-verify on every deliberation read, no caching. Third: we lean on the
wave5/6 integrity result that the learner's deliberation can be trusted to invoke the query
interface honestly; a learner that skips provenance checks degrades to provenance-free TNN,
which is exactly the K2 clause's test. Not claimed: provenance proves a fact true (it proves
origin only); provenance solves sensor-deceivability (accepted hole stands).

## 6. Next build step
Build the seal + verify path and the K1/K2 trial harness natively in Zag: seed 200 forgery
attacks (both directions) into a 10x run, confirm 0 reach deliberation, then run the
provenance-stripped control for the K2 clause. Do not build promotion until K1/K2 hold.
