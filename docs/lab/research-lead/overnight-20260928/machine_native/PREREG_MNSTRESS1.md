# PREREG_MNSTRESS1.md -- Machine-Native Advantage Stress Test (C2)

Frozen: 2026-09-30. Committed alone before any implementation, world
generation, or measurement. Any implementation commit must strictly follow
this commit.

## 1. Claim under test

A purpose-built epistemic-state engine (the TNN contestant for Program 2)
can maintain and update an epistemic state at a scale and precision
impractical for unaided human cognition:

- exact provenance for every belief (which claims, from which sources);
- retention of 500 simultaneous contradictions as UNRESOLVED (no premature
  collapse);
- dependency-tracked correction propagation;
- evidence-withdrawal impact analysis;
- load-bearing memory identification;
- byte-identical recovery after process restart.

This is a MACHINE-NATIVE claim (scale/precision), NOT "TNN is smarter than
humans" and NOT an L3 representational-invention claim. The engine is a
bounded epistemic subsystem. No human or LLM comparison scores are claimed
here; the human protocol (section 7) is frozen for FUTURE evaluation only.

## 2. Synthetic world (deterministic from sealed seed)

Generated entirely inside the Zag program from a fixed seed constant
(sealed at implementation; recorded in the result report):

- 1000 entities (ids 0..999), synthetic names from syllable tables.
- 8 attributes per entity, small per-attribute value vocabularies.
- 5000 relationship claims (e1, rel in 0..5, e2).
- 240 sources, reliability 1..5 (deterministic).
- 6000 attribute claims, fed incrementally in seq order.
- Exactly 500 DELIBERATE contradictions: same (entity, attr), different
  values, different sources. Must remain UNRESOLVED.
- 60 temporal supersessions: value v1 at seq t1, v2 at later t2; old claim
  retained and flagged SUPERSEDED (not deleted).
- 40 delayed corrections: an earlier claim retracted by a later
  high-reliability (rel=5) correction claim.
- 3 derivation rule templates (nested dependencies) producing derived
  beliefs with provenance = base claim ids:
  - R1: (X located-in Y) + (Y habitat H) => (X habitat H)
  - R2: (X allied Y) + (Y allied Z) => (X allied Z), blocked for 80
    wartime pairs (contextual exception)
  - R3: (X descended-from Y) + (Y origin O) => (X origin O)
- 2000 unrelated junk claims as interference batch (for KB6).
- Withdrawal test set: 10 sampled claim ids with harness-computed
  dependent-belief sets (computed from the engine's own dependency
  records at generation time; the checker verifies set equality).

## 3. Contestant: epistemic engine

Maintains: claim store, per-slot current belief + support/contradict claim
lists, contested-slot hypothesis pairs (H1/H2 with evidence), derived
beliefs with base-claim provenance, dependency closure, wartime context.

Must answer 7 query types:
- Q1: current belief about (entity, attr)
- Q2: why (exact provenance: supporting claim ids + sources)
- Q3: which evidence disagrees (contradicting claim ids + sources)
- Q4: consequences under context C (derived beliefs with context applied)
- Q5: what observation would distinguish H1 from H2 (must name an
  observable slot whose predicted value differs under the two hypotheses)
- Q6: if evidence E withdrawn, which beliefs lose support (dependency
  closure over E)
- Q7: which memories are load-bearing (claims that are sole support of at
  least one current belief)

## 4. Baselines (same world, same feed)

- B-flat: (entity,attr)->value map, no provenance. Expected: Q1 only.
- B-lww: last-write-wins, collapses contradictions. Expected: Q1 only,
  contested retention near 0.
- B-noprov: claims + sources stored, no dependency graph. Expected:
  Q1-Q5 partial, Q6/Q7 fail.

Baselines are honest controls: they show which query types REQUIRE the
epistemic machinery (provenance store, contradiction retention,
dependency graph).

## 5. Kill bars (numbered; ALL must pass for BUILD-PASS)

- KB1 (world scale): entities=1000, relation claims=5000, sources=240,
  deliberate contradictions=500, temporal supersessions=60, delayed
  corrections=40, attribute claims=6000, junk=2000. Exact counts verified
  by the generator's own counters.
- KB2 (provenance exactness): 50/50 sampled Q2 queries return EXACTLY the
  recorded support set and contradict set (claim-id set equality).
- KB3 (contradiction retention): after full feed, contested slots = 500
  and collapsed contradictions = 0.
- KB4 (correction propagation): after the 40 delayed corrections, 40/40
  sampled directly-affected derived beliefs show corrected values, and
  every derived belief depending on a corrected claim is flagged
  re-derived (count verified against dependency records).
- KB5 (withdrawal): 10/10 sampled evidence withdrawals yield EXACTLY the
  harness-computed affected-belief set (set equality, no more, no fewer).
- KB6 (no accidental forgetting): after full feed + 2000 junk claims,
  100/100 sampled facts retrievable with exact provenance (Q1+Q2 correct).
- KB7 (restart): serialize full engine state to file; fresh process
  reloads; 50/50 sampled queries (Q1-Q7 mix) byte-identical before/after.
- KB8 (baseline dominance): engine 100% on all sampled query types
  (Q1:50/50, Q2:50/50, Q3:40/40, Q4:30/30, Q5:20/20, Q6:10/10, Q7: exact
  set match). B-flat: 0/50 on Q2 samples (answers Q1 only). B-lww:
  contested slots retained <= 100 (collapses >= 400 of 500). B-noprov:
  0/10 on Q6 samples and Q7 set mismatch (missing dependents).
- KB9 (determinism): 3/3 full runs byte-identical (stdout + state file).
- KB10 (purity/governance): pure Zag only (no .py files, no python3
  invocation at any stage); no em-dash bytes in docs; prereg commit
  strictly precedes implementation.

## 6. Metrics recorded (cost ledger)

Per run: claims ingested, contradictions retained, hypotheses active
(contested slots x2 + derived), query latency per type (ms, via
clock_gettime), peak RSS (kB, /proc/self/status), state bytes serialized,
derived beliefs count, corrections applied, withdrawals tested.

## 7. Human protocol (frozen, future use only)

HUMAN_PROTOCOL.md freezes a smaller subset: 30 entities, 80 claims,
8 contradictions, 2 corrections, 1 withdrawal scenario, fixed
instructions, 45-minute limit, per-question scoring rubric, note-taking
policy (two conditions: unaided = no notes; tooled = blank paper).
NO HUMAN SCORES ARE FABRICATED. The protocol exists so a future session
can run TNN vs unaided human vs human+notes on identical observations.

## 8. Honest scope and anti-spoof notes

- The engine's query handlers are authored; the WORLD (entities, values,
  contradictions, corrections) is sealed synthetic data the engine never
  sees in advance. The test measures epistemic-state maintenance, not
  invention.
- Ground-truth checks use the generator's recorded counters and id sets;
  this is structural verification, not independent reimplementation.
  Later promotion steps (independent adversary) may attack it.
- Q5's "discriminating observation" is verified by checking the named
  slot indeed has different predicted values under H1 vs H2.
- Latency/RSS are machine metrics of this VM, reported as observed, not
  as claims about other hardware.

## 9. Verdict rule

BUILD-PASS iff KB1..KB10 all pass as numbered above. Any single failure
-> BUILD-FAIL with the failing bar named. Builder reports BUILD-PASS or
BUILD-FAIL only; no SURVIVES claim (promotion pipeline steps 3..11 are
for the parent to schedule).
