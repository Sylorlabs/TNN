# H2-v2 Test Results

**Status:** H2V2-RUN-COMPLETE.
**Verdict:** K-H2-1 FAIL, K-H2-2 FAIL, K-H2-3 FAIL, K-H2-4 FAIL.
**Evaluation:** VALID (not VOID). All prerequisites held.
**Date:** 2026-10-01.
**Runs:** 3/3 byte-identical. SHA-256
`4f10c37ff6b6777faf292f6d434f55321eb78dd2c4bcc95919ad7a2b86f9ec6e`.

## Prerequisites (all held)

- **Calibration:** (i)(ii)(iii) all PASS. `t2_sig_v2` is sound.
- **TRIAL_ENTERED:** 1 on all eight scored probes. The trial executed
  with at least one candidate reaching verification on every probe.
  The VOID-wave failure (trial never ran) is repaired.
- **Hash verification:** All four world hashes matched `SEAL_H2V2.md`
  before the first probe.
- **Governance:** Pure Zag, safebin, zero Python, zero em-dashes.

## K-H2-1 (masked accuracy): FAIL

| Probe | Mode | Answer | True | Trial |
|-------|------|--------|------|-------|
| H2A-v2 | masked (flags=1, exp=-2) | 60003 | 60013 | 1 |
| H2A-v2 | unmasked (flags=0, exp=60013) | 60013 | 60013 | 1 |
| H2C-v2 | masked (flags=1, exp=-2) | 60203 | 60213 | 1 |
| H2C-v2 | unmasked (flags=0, exp=60213) | 60213 | 60213 | 1 |

Masked accuracy: 0% on both worlds. Bar requires >50%.
Unmasked controls: both PASS.

**Mechanism (white-box):** The masked branch of `t2_try_verify`
(frozen line 501-503) accepts the FIRST candidate with a clean
execution value (`v != -2 && v != -999999`) in the fixed researcher
search order (2-hop chains before 3-hop in `t2_gather` BFS order).
On trap worlds the first executable candidate is wrong by design.
There is no learner-internal criterion; the decision is
first-clean-in-fixed-order.

## K-H2-2 (lie resistance): FAIL

| Probe | Mode | Answer | Trial |
|-------|------|--------|-------|
| H2B-v2-B1 | lie (exp=60112) | 60112 | 1 |
| H2B-v2-B1 | control (exp=60103) | 60103 | 1 |
| H2B-v2-B2 | lie (exp=69999) | -2 | 1 |
| H2B-v2-B2 | control (exp=60123) | 60123 | 1 |

- B1: The lie-matching candidate (60112) was PROMOTED. Bar requires
  zero promotions of fact-contradicting candidates. VIOLATED.
- B2: No candidate matched the unconfirmable lie (69999). Answer -2
  with no key-failure trace in learner state (silent drop).
- Controls: both PASS.

**Mechanism (white-box):** No oracle-vs-facts comparison exists on
the verification path. `t2_try_verify` checks `v == expected`
(unmasked) with no reference to retained facts. The lie is absorbed
(B1) or dropped silently (B2).

## K-H2-3 (criterion causality and revisability): FAIL

**(a) Causality: FAIL.** White-box trace of `t2_try_verify`:

```
fn t2_try_verify(W,root,s0,expected,masked,st)i32 {
  if(root<0){return -2;}
  set32(st,0,get32(st,0)+1);
  let v:i32=t2_exec(W,root,s0);
  if(masked==1){
    if(v!=-2 && v!=-999999){return v;}
  } else {
    if(expected!=-2 && v==expected){return v;}
  }
  ...
}
```

The accept decision reads exactly three inputs: `v` (execution
result), `expected` (oracle-supplied), `masked` (driver flag). No
learner-created persistent state value appears in the causal chain.
The search order (which candidate is tried first) is determined by
`t2_gather` BFS order and the fixed k=2..4 loop; no policy node or
learner value influences it.

**(b) Ablation: FAIL.** No learner-created criterion value exists to
ablate. Sub-clause (a) is a prerequisite.

**(c) Revisability: FAIL.** No criterion exists to revise. A fixed
first-clean-wins rule cannot tighten after false acceptance.

## K-H2-4 (domain neutrality and reuse): FAIL

**(a) Domain neutrality: PASS.** `t2_try_verify` contains no
per-family acceptance branches. The same `v != -2` / `v == expected`
logic handles chain, sum, and count candidates identically. No new
protected-core operations were added by the evaluator.

**(b) Reuse coupling: FAIL.** `activate` (frozen line 140) matches
only tag-1 facts:

```
if(ng(W,n,36)==1 && ng(W,n,0)==1 && is_superseded(W,n)==0){
```

The `ng(W,n,0)==1` check excludes tag-20 MAPs. Promoted graphs are
never executed via the query path. `ev_query` reads only tag-1
facts, never tag-20 MAPs. No reuse trace is possible in the frozen
architecture.

Overall: FAIL (both sub-clauses required).

## What this establishes

1. **Frozen TNN-2 cannot judge/withhold structures using a
   learner-internal criterion when the environment does not provide
   the expected answer.** K-H2-1 FAIL with 0% masked accuracy on
   trap worlds. The masked branch is first-clean-in-fixed-order,
   not a learner criterion.

2. **Frozen TNN-2 cannot resist a lying oracle.** K-H2-2 FAIL. The
   lie-matching candidate is promoted (B1); the unconfirmable lie
   leaves no trace (B2).

3. **No learner-created criterion value exists in the accept/reject
   path.** K-H2-3 FAIL on all three sub-clauses. The decision reads
   only (v, expected, masked).

4. **Promoted structures are causally inert at query time.** K-H2-4
   FAIL. The verifier is domain-neutral (a), but reuse coupling (b)
   is absent by construction.

## What this does NOT establish

Per prereg section 13(d)(e)(f): Passing or failing K-H2 does not by
itself establish L3, C0-B, C0-C, SUF, cognitive reuse, or
learner-authored procedures. It does not weaken the C0-A regression
bars. This is a valid negative result about learner-internal
verification in frozen TNN-2, not a claim about what TNN-3 could do.

## Predicted outcome (prereg section 14)

The prereg predicted FAIL on all four bars from source reading. All
four predictions confirmed behaviorally. The predictions did not
govern the evaluation; the evaluator scored what the frozen binary
did.

## Standing architectural metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: The frozen TNN-2
  researcher-owned decisions are unchanged (enumerated in the
  canonical ledger). This evaluation added zero.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0. No learner-created
  persistent state value participated in any accept/reject decision.
- SOURCE-ENUMERABLE FORMS: The trial enumerates fixed families
  (chains k=2..4, sums, counts, single hops) in fixed order.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0 (no MAP executed at query time).
- REVISION EVENTS: 0.
- COGNITION LINES: 0 (evaluation only).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## Artifacts

- `NAMECHECK.md` (Step 0, toolchain guard, work plan)
- `FROZEN_PREREG.md` (frozen `84a2a4ddf`)
- `BUILD.md` (evaluator construction, t2_sig_v2, calibration)
- `TEST_RESULTS.md` (this file)
- `SEAL_H2V2.md` (world hashes, audit, attestation)
- `audit_output.txt` (pre-seal audit)
- `h2v2_driver.zag` (evaluator driver source)
- `h2v2_base.zag` (frozen prefix, lines 1-1356)
- `h2v2_full.zag` (assembled evaluator source)
- `h2v2_bin` (evaluator binary)
- `world_H2A_v2.txt`, `world_H2B_v2_B1.txt`,
  `world_H2B_v2_B2.txt`, `world_H2C_v2.txt` (sealed, `-rw-------`)
- `run1.txt`, `run2.txt`, `run3.txt` (3/3 byte-identical)

No em dashes were used in this document. Paper untouched.
Nothing pushed.
