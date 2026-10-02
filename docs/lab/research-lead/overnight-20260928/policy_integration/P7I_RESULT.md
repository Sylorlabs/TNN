# RESULT: P7 Persistence Policy Integration with the Continuing Learner

Worker: Policy Integration Worker.
Date: 2026-09-30 UTC.
Verdict: **INTEGRATION-PROTOTYPED** (all frozen kill bars pass).

Prereg: `15d2856dd` (committed alone before any implementation;
verified strict ancestor of the implementation commit via
`git merge-base --is-ancestor`).
Implementation: `p7_integration.zag` (this directory, pure Zag).
Raw: `P7I_RAW_1.txt` (md5 `e89337d077471a07233266e3a41c0870`).
Determinism: 3/3 byte-identical, exit 0, zero stderr on all runs.
Governance: pure Zag at every stage (znc, bash, grep, git only; no
Python); zero em-dash bytes in wave files; prereg strictly precedes
implementation; commits local on `tnn-native-lab`, owned paths only.

## 1. Integration design (K1)

The P7 layer exposes three operations the continuing learner invokes at
task (domain) boundaries in one persistent run, single main(), no
process reset, no task labels:

1. `schema_discover()`: after a domain is learned, scan the rule store
   for a regularity (every rule with relation R maps to the same object
   O). If found, persist schema S = (R, O) plus the refit procedure.
   The persisted structure is the relation choice plus the refit
   procedure, never a verbatim instance: O is refit from 3 probes on
   every new domain where the gate passes.
2. `schema_verify(S, domain)`: cheap gate. On a new domain, take the
   first 3 episodes as probes; gate passes iff all 3 agree on the true
   object (3/3). On pass, the learner installs the refit schema and
   answers the remaining queries through it (3 learns instead of 4).
   On fail, fall back to per-instance learning (4 learns).
3. `schema_retire(S)`: update the accuracy ledger (schema-path minus
   fresh-path per domain) and the consecutive-rejection counter. Retire
   when ledger < 0 OR consec_reject >= 2. Ledger and counters reset on
   retirement. Rediscovery allowed afterwards.

Schema kind in v1 (disclosed as bounded): single-relation default rules,
form `(rel R) -> obj O`. If no uniform relation exists in a domain, no
schema is discovered there.

The learner itself is a DEVINT2-style rule store: instance slots
(subj, rel, obj, dom, valid) with exact-match retrieval, plus one
schema slot consulted when no instance matches. Episodes are
integer-coded; the encoding is disclosed as not under test.

Disclosed simplification: per-domain instances are tagged by domain
rather than evicted; cross-boundary persistence is the schema's job,
which is the variable under test.

## 2. Frozen workload and results

Eight sequential domains, 4 rules each, rel = legs:

- D1 mammals: all obj 4 (discovery domain).
- D2 birds: 2. D3 fish: 0. D4 insects: 6. D5 snakes: 0. D6 mammals2: 4.
- D7 mixed: (2,4,6,8). D8 mixed2: (8,6,4,2).

Observed output (from the frozen binary, 3/3 identical):

```
SCHEMA_DISC rel=1 obj=4
DOM 2 GATE=1 / APPLY dom=2 obj=2 learns=3
DOM 3 GATE=1 / APPLY dom=3 obj=0 learns=3
DOM 4 GATE=1 / APPLY dom=4 obj=6 learns=3
DOM 5 GATE=1 / APPLY dom=5 obj=0 learns=3
DOM 6 GATE=1 / APPLY dom=6 obj=4 learns=3
DOM 7 GATE=0 / FALLBACK dom=7 learns=4
DOM 8 GATE=0 / FALLBACK dom=8 learns=4
SCHEMA_RETIRED
OPS_P7 27 / OPS_FRESH 32
LEDGER 0 / APPLIES 5 / RETIRED 1
K1 1 / K2 1 / K3A 1 / K3B 1 / K3C 1 / K3D 1
VERDICT INTEGRATION-PROTOTYPED
```

## 3. Kill bar evaluation

- K1 (integration design documented): PASS. Design is in the prereg
  (section 2) and section 1 above.
- K2 (prototype in pure Zag): PASS. Compiles with the frozen toolchain,
  runs to completion, exit 0.
- K3 (multi-task test shows the policy working): PASS, all sub-checks:
  - (a) schema discovered after D1: `SCHEMA_DISC rel=1 obj=4`. PASS.
  - (b) schema applied on 5 of D2..D6 (need >= 3), each with 3 learns
    < 4 fresh. PASS.
  - (c) schema retired after 2 consecutive mixed-domain gate failures:
    `SCHEMA_RETIRED` after D8. PASS.
  - (d) OPS_P7 = 27 < OPS_FRESH = 32 (executed fresh control:
    8 domains x 4 learns). PASS.
  - (e) 3/3 byte-identical, exit 0, zero stderr. PASS.

## 4. Validity bars

- V1 (3/3 identical, exit 0, zero stderr): PASS.
- V2 (prereg strictly precedes implementation): PASS
  (`git merge-base --is-ancestor 15d2856dd <impl>` confirmed).
- V3 (zero Python, zero em dashes): PASS. Only znc, bash, grep, git
  used. The word "python" appears solely inside "no Python"
  declarations.
- V4 (gate behavior as specified): PASS. GATE=1 on all five uniform
  domains D2..D6; GATE=0 on both mixed domains D7, D8.

## 5. Interpretation

1. The policy layer works inside a continuing learner: one schema
   (`legs` has a single default) is discovered once, refit across five
   domains with different values (2, 0, 6, 0, 4), and retired when the
   form breaks (two mixed domains). The full P7 lifecycle --
   discover, verify, apply, retire -- executes in one persistent run
   with no resets.
2. The schema is genuinely re-fittable, not a frozen instance: the
   object value changes per domain (4 -> 2 -> 0 -> 6 -> 0 -> 4) while
   the form (one default for the relation) is what persists. This is
   the "schemas amortize" principle operating across task boundaries.
3. The accuracy ledger stayed at 0, exactly as predicted in the prereg:
   under exact-match retrieval both paths score 4/4, so the ledger
   cannot discriminate here. The consecutive-rejection trigger did the
   retirement work. The ledger bookkeeping is implemented and reported;
   exercising it needs a noisy-retrieval world (future work).
4. Savings are modest (5 learn ops over 8 domains) because the gate
   costs 3 probes per domain. The saving scales with domain size: on
   N-rule domains the policy spends 3 probes + (N-3) schema-covered
   queries vs N fresh learns. The prototype proves the mechanism, not
   the magnitude.

## 6. Honest scope and limits

- One schema kind (single-relation defaults). No two-hop patterns, no
  multi-relation forms.
- The schema form is researcher-supplied; the policy decides
  persistence, the learner fills values. Bounded L1/L2. Not L3.
- Synthetic workload, exact-match retrieval, small scale.
- The accuracy-ledger retirement trigger is implemented but not
  exercised (needs noise).
- No transfer across changed surface representations; no LLM/human
  comparison; no claim beyond INTEGRATION-PROTOTYPED.
- No SURVIVES claim: promotion needs the full 11-step pipeline.

## 7. Files

- `PREREG_POLICY_INTEGRATION.md` (15d2856dd, frozen before implementation)
- `p7_integration.zag` (implementation, pure Zag)
- `P7I_RAW_1.txt` (md5 e89337d077471a07233266e3a41c0870; runs 2 and 3 identical)
- `P7I_RESULT.md` (this file)
