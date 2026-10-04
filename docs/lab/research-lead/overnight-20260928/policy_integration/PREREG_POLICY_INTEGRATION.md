# PREREG: P7 Persistence Policy Integration with the Continuing Learner

Worker: Policy Integration Worker.
Date: 2026-09-30 UTC.
Status: FROZEN before any implementation. This file is committed alone;
no implementation exists at commit time. Implementation must be a strict
descendant of this commit.

## 1. Mission

Integrate the Program 7 persistence policy (POLICY-DESIGNED, commit
55ed019e1) into the one-continuing-learner context. P7 delivers an
implementable rule: persist validated re-fittable schemas (never
verbatim instances), verify via a cheap per-task gate before applying,
retire on sustained rejection or negative ledger, allow rediscovery.

The DEVINT2 learner (BUILD-PASS, devint2_learn.zag) is a one-process
continuing learner over (subj, rel, obj) episodes with two rule stores
(STORE-C: consequence-based eviction; STORE-R: recency eviction). It has
no persistence policy beyond eviction: it stores instances, never
schemas. The integration prototype adds a P7 policy layer the learner
invokes at task boundaries.

## 2. Integration design

### 2.1 What the learner invokes, and when

The P7 layer exposes three operations called at task (domain) boundaries
in a single persistent run, no process reset, no task labels passed to
cognition beyond the episode stream itself:

1. `schema_discover()`: after the learner has learned a domain, scan the
   rule store for a regularity: every rule with a given relation R maps
   to the same object O. If found, propose schema S = (R, O, fitted_from
   domain). This is a re-fittable form: the relation R is fixed, the
   object O is refit per domain.
2. `schema_verify(S, domain)`: cheap gate. On a new domain, take up to 3
   probe episodes with relation R and compare their true objects against
   S refit on those 3 probes. Gate passes iff all 3 agree (3/3).
   If the gate passes, the learner reuses S with 3 fitted examples
   instead of learning each rule from scratch (saving learn operations).
   If the gate fails, fall back to per-instance learning (no schema use).
3. `schema_retire(S)`: update the ledger (accuracy delta of schema path
   vs fresh path, summed) and consecutive-rejection counter. Retire when
   ledger < 0 OR consec_reject >= 2. Reset ledger and counters on
   retirement. Rediscovery allowed afterwards.

### 2.2 What schemas the learner produces

One schema kind in v1, disclosed as bounded: single-relation default
rules. Form: `(rel R) -> obj O`. Example: in the animal domain every
(animal, legs) fact has obj 4, so the schema is `(legs) -> 4`. It is a
schema, not an instance, because O is refit from 3 probes on every new
domain where the gate passes; the persisted structure is the relation
choice plus the refit procedure, not the object value.

No other schema kinds in v1. No two-hop patterns, no multi-relation
forms. If single-relation defaults do not occur in a domain, no schema
is discovered there.

### 2.3 Test workload (frozen)

One continuing learner, six domains in sequence, single main():

- D1 mammals: 4 rules, rel 1 (legs), all obj 4. Discovery domain.
- D2 birds: 4 rules, rel 1 (legs), all obj 2. Same rel, different obj.
- D3 fish: 4 rules, rel 1 (legs), all obj 0. Same rel, different obj.
- D4 insects: 4 rules, rel 1 (legs), all obj 6. Same rel, different obj.
- D5 snakes: 4 rules, rel 1 (legs), all obj 0. Same rel, different obj
  (fish obj).
- D6 mammals2: 4 rules, rel 1 (legs), all obj 4. Same as D1.

Expected policy behavior (prediction, not a bar):
- After D1: schema `(legs) -> 4` discovered and persisted.
- D2: gate on 3 probes: true objs are 2, refit gives 2, so gate
  PASSES (the schema is re-fittable; obj refit to 2). Schema applies:
  learner uses refit (3 probes) instead of 4 fresh learns. Saving 1.
  This is the schema doing its job: the form (legs has a single
  default) transfers, the value refits.
- D3: same, refit to 0, gate passes, saving 1.
- D4: same, refit to 6, gate passes, saving 1.
- D5: same, refit to 0, gate passes, saving 1.
- D6: refit to 4, gate passes, saving 1.

To exercise RETIREMENT, one domain breaks the form: a 7th domain D7
mixed: 4 rules with rel 1 but objs (2, 4, 6, 8), no single default.
Gate fails (3 probes disagree). consec_reject = 1. D8 mixed2: another
mixed domain, gate fails again, consec_reject = 2, schema RETIRED.

Total: 8 domains. Ledger tracks schema-path accuracy vs fresh-path
accuracy; both are exact here (exact-match retrieval), so the ledger
stays near 0 and the consecutive-rejection trigger is the one
exercised. This is disclosed: in this exact-match world the accuracy
ledger cannot go negative, so V-trigger verification focuses on the
consec trigger. The ledger bookkeeping is still implemented and its
value reported.

## 3. Kill bars (frozen; evaluated after execution)

- K1 (integration design documented): this file plus a DESIGN section in
  the result doc describing the three operations and when the learner
  invokes them. PASS iff present.
- K2 (prototype implemented in pure Zag): single file
  `p7_integration.zag` in this directory, compiles with the frozen
  toolchain, runs to completion. PASS iff it compiles and exits 0.
- K3 (multi-task test shows policy working): PASS iff ALL of:
  - (a) schema discovered after D1: output line SCHEMA_DISC rel=1;
  - (b) schema applied on at least 3 of D2..D6 with fewer learn ops
    than fresh (output APPLY lines);
  - (c) schema retired after 2 consecutive mixed-domain gate failures
    (output line SCHEMA_RETIRED);
  - (d) total learn operations with policy < total learn operations of
    a fresh-per-domain control run on the same 8 domains (reported as
    OPS_P7 vs OPS_FRESH, must be strictly less);
  - (e) 3/3 byte-identical runs, exit 0, zero stderr.

## 4. Validity bars (self-checks, reported honestly)

- V1: 3/3 byte-identical, exit 0, zero stderr.
- V2: prereg commit strictly precedes implementation commit
  (git merge-base --is-ancestor check).
- V3: zero Python at any stage; zero em-dash bytes in wave files
  (grep check reported).
- V4: gate behavior exactly as specified: passes on uniform domains,
  fails on mixed domains (output lines GATE=1 / GATE=0 per domain).

## 5. Governance

- Pure Zag only: no Python in source, build, execution, or analysis.
- No em dashes in any wave documentation (checked via grep).
- Commits local on branch tnn-native-lab; owned paths only:
  docs/lab/research-lead/overnight-20260928/policy_integration/.
- This prereg is committed alone. The implementation commit must be a
  strict descendant. If this ordering is violated the result is VOID.
- Report INTEGRATION-PROTOTYPED only if K1..K3 all PASS; otherwise
  INTEGRATION-BLOCKED with the failing bar named.
- No SURVIVES claim: promotion needs the full 11-step pipeline.
- Classification ceiling for this work: mechanism integration, not L3.
  The schema form (single-relation default) is researcher-supplied; the
  policy decides persistence, the learner fills values. Bounded L1/L2.

## 6. What this does NOT test

- The DEVINT2 twin-store machinery itself (already BUILD-PASS).
- Schema kinds beyond single-relation defaults.
- The accuracy-ledger retirement trigger (not exercisable under
  exact-match retrieval; bookkeeping still implemented and reported).
- Transfer across changed surface representations.
- Any claim about beating LLMs, humans, or SQLite.
