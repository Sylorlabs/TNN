# MINUS_TWO.md - Disambiguating the -2

## Mission

The decline signal analysis (`9e0ae81d1`) found: "The -2 is pipeline exhaust, not a cognitive choice. It is overloaded across 5 distinct situations." This worker identifies the actual distinct code paths that produce -2, instruments them with white-box logging, and measures their frequency across a varied battery.

## Method

1. Traced all `-2` return statements in `ev_query` and its callees (`t2_trial`, `t2_try_verify`, `bootstrap_miss`, `mp_run`) in frozen TNN-2 source (read-only).
2. Built a driver on a VERBATIM frozen copy (SHA-256 `a29972ca...`, verified identical).
3. Instrumented the COPY with a per-query path bitmask in header 52 (free slot; nodes start at byte 64). Eight bits for eight distinct paths. Frozen original untouched.
4. Ran 12-query battery covering: empty state, masked/unmasked, facts for same/different s, wrong/correct/missing expected, observations with/without invariant, above/below threshold.
5. Verified behavior preservation: same battery on uninstrumented copy produces byte-identical `v=` values.
6. 3/3 byte-identical runs (SHA-256 `db97f21f...`).

## Path Inventory: 8 Distinct -2 Paths (Not 5)

### In `t2_try_verify` (trial candidate verification)

| ID | Bit | Location | Condition | Meaning |
|----|-----|----------|-----------|---------|
| P1 | 1 | VERIFY_BADROOT | `root<0` | Assembly produced invalid graph root. Candidate never built. |
| P2 | 2 | VERIFY_FAIL_MASKED | masked=1, `v==-2 \|\| v==-999999` | Candidate executed but produced no value or hit guard rejection. |
| P3 | 4 | VERIFY_FAIL_MISMATCH | masked=0, expected!=-2, `v!=expected` | Candidate executed to a value, but it did not match the oracle. |
| P4 | 8 | VERIFY_FAIL_NOEXP | masked=0, expected==-2 | No oracle supplied. Candidate tried but verification is structurally impossible. |

### In `bootstrap_miss` (P-INV statistical fallback)

| ID | Bit | Location | Condition | Meaning |
|----|-----|----------|-----------|---------|
| P5 | 16 | BOOTSTRAP_FEW | `cnt<2` | Fewer than 2 recent observations with matching r. Insufficient evidence. |
| P6 | 32 | BOOTSTRAP_NOINV | `inv==0` | Observations exist but values differ. No invariant. Conflicting evidence. |
| P7 | 64 | BOOTSTRAP_BELOWK | `cnt<k` (k=3) | Invariant exists but fewer than threshold observations. |
| P8 | 128 | BOOTSTRAP_ALLOCFAIL | `m<2` | Node allocation failed under memory pressure. |

### Terminal (`ev_query`)

The `return -2` at the end of `ev_query` is the aggregation point. It fires only when: `activate` found no FACT, `t2_trial` returned -2 (all candidates failed via P1-P4 or no candidates existed), AND `bootstrap_miss` returned -2 (via P5-P8). It then calls `miss_inquire` (creating the write-only UNCERTAINTY node) and returns -2 to the caller.

## Frequency Measurements

12 queries, 8 returned -2. Per-query bitmask aggregated:

| Path | Bit | Count | % of -2s | Cases |
|------|-----|-------|----------|-------|
| BOOTSTRAP_FEW | 16 | 5 | 62% | 1, 2, 4, 10, 11 |
| BOOTSTRAP_NOINV | 32 | 2 | 25% | 3, 6 |
| VERIFY_FAIL_MISMATCH | 4 | 2 | 25% | 4, 10 |
| BOOTSTRAP_BELOWK | 64 | 1 | 12% | 7 |
| VERIFY_FAIL_NOEXP | 8 | 1 | 12% | 11 |
| VERIFY_BADROOT | 1 | 0 | 0% | - |
| VERIFY_FAIL_MASKED | 2 | 0 | 0% | - |
| BOOTSTRAP_ALLOCFAIL | 128 | 0 | 0% | - |

(Percentages sum >100% because a single query can hit multiple paths; e.g., Case 4 hit both MISMATCH and FEW.)

### Per-case detail

| Case | Setup | Result | Mask | Interpretation |
|------|-------|--------|------|----------------|
| 1 | Empty, unmasked | -2 | 16 | No facts, no observations. Pure absence. |
| 2 | Empty, masked | -2 | 16 | Same as 1. Masking changes nothing without facts. |
| 3 | Facts for other s | -2 | 32 | Bootstrap found 2 observations (the taught facts) with r=1 but different values. NOINV. |
| 4 | Same s, wrong expected | -2 | 20 | Trial candidates executed but mismatched (4); bootstrap had no r=3 obs (16). |
| 5 | Same s, masked | 1 | 0 | Trial SUCCEEDED in masked mode. Control. |
| 6 | Obs, no invariant | -2 | 32 | Three observations, different values. NOINV. |
| 7 | Obs, invariant below k | -2 | 64 | Two identical observations, but k=3. BELOWK. |
| 8 | Obs, invariant at k | 10 | 0 | Bootstrap succeeded. Control. |
| 9 | Answerable fact | 42 | 0 | Activate succeeded. Control. Mask=0 confirms no -2 paths. |
| 10 | Chain facts, exp=12 | -2 | 20 | Candidates tried, mismatched (4); no r=3 obs (16). |
| 11 | Same s, no expected | -2 | 24 | Candidates tried but NOEXP (8); no r=3 obs (16). |
| 12 | Same s, masked | 1 | 0 | Trial succeeded in masked mode. Control. |

## Key Findings

### 1. Eight paths, not five

The decline signal doc said "5 distinct situations." The code has 8 distinct -2 return points (P1-P8), each with a different triggering condition. The terminal -2 collapses all of them into one integer.

### 2. BOOTSTRAP_FEW dominates (62%)

The most common reason for -2 is insufficient observations. The system most often fails because it has seen too little, not because it tried and failed.

### 3. VERIFY_FAIL_NOEXP is structural incapacity, not ignorance

Case 11 is the critical finding. When `expected==-2` in unmasked mode, the trial is structurally incapable of succeeding. Every candidate is doomed before it runs: the verification condition `expected!=-2 && v==expected` can never be true. This is not "the learner doesn't know the answer." It is "the verification machinery requires an oracle, and none was supplied." The -2 in this case reports a harness configuration problem as if it were learner ignorance.

### 4. Taught facts are visible to bootstrap as "observations"

Case 3 surprise: `bootstrap_miss` scans for "recent observations" by looking at nodes with `ng(W,n,36)==1` (live) and matching r. Taught FACTs match this scan. The bootstrap does not distinguish a deliberately taught fact from a passively observed event. This means the "statistical fallback" can fire on researcher-supplied teaching data, not just environmental observations.

### 5. Masked mode is strictly more capable

Cases 5 and 12: masked trial succeeded where unmasked would fail. In masked mode, any executable value verifies (`v!=-2 && v!=-999999`). In unmasked mode without expected, nothing verifies. The masked criterion is weaker but functional; the unmasked-without-oracle criterion is vacuous.

### 6. Three paths never fired

VERIFY_BADROOT (P1), VERIFY_FAIL_MASKED (P2), and BOOTSTRAP_ALLOCFAIL (P8) never occurred in this battery. P1 and P8 are rare edge cases (assembly failure, memory exhaustion). P2 requires masked candidates that execute to -2/-999999, which did not occur with these facts.

## What a Cognitive Decline Signal Would Need to Distinguish

The current -2 collapses at least six cognitively distinct situations:

1. **No data** (P5 with no trial candidates): nothing relevant has ever been experienced. Appropriate response: inquire, explore.
2. **Tried and failed** (P3): candidates were constructed and executed but did not match. Appropriate response: revise construction strategy, not just retry identically.
3. **Oracle required but absent** (P4): the task is well-posed but the verification machinery needs an expected value. Appropriate response: flag as harness problem, not learner failure.
4. **Insufficient evidence** (P5/P7): some data exists but below threshold. Appropriate response: gather more, withhold judgment.
5. **Conflicting evidence** (P6): observations disagree. Appropriate response: investigate the conflict, not average it away.
6. **Resource exhaustion** (P8): the system cannot allocate. Appropriate response: free resources, compress, or report incapacity.

Currently, all six produce the identical integer -2. A downstream consumer (harness, evaluator, or the learner itself) cannot distinguish "I have never seen anything relevant" from "I tried three candidates and they all failed verification" from "you did not give me an expected value."

### Minimal disambiguation requirements

- The decline output must carry at least a **reason code** (which of P1-P8, or which combination).
- The **trial vs bootstrap** distinction must be visible: did construction even attempt an answer?
- The **oracle-absent** case (P4) must be separable from genuine uncertainty: it is a measurement artifact, not a cognitive state.
- A cognitive decline would additionally need: confidence in the decline itself, what would change the answer (what evidence is missing), and whether retrying is expected to help.

## Non-claims

- This is measurement, not a proposal. No decline mechanism is designed here.
- Frequencies are battery-dependent. A different battery (more contradictions, memory pressure, adversarial inputs) would shift the distribution.
- The 3 unobserved paths (P1, P2, P8) are not proven absent; they are proven absent from this battery.
- Behavior preservation verified: instrumented and uninstrumented copies produce byte-identical query results.

## Deliverables

- `NAMECHECK.md` (Step 0, provenance, constraints)
- `MINUS_TWO.md` (this file)
- `m2_base.zag` (verbatim frozen copy, SHA-256 `a29972ca...`)
- `m2_inst.zag` (instrumented copy with header-52 bitmask)
- `m2_verify.zag` (uninstrumented copy with driver, for behavior check)
- `m2_bin`, `m2_verify_bin` (compiled binaries)
- `m2_run1.txt`, `m2_run2.txt`, `m2_run3.txt` (3/3 byte-identical, SHA-256 `db97f21f...`)
- `m2_verify_run.txt` (behavior preservation check)

## Standing Metric

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (measurement only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- SOURCE-ENUMERABLE FORMS: N/A (no new forms)
- SUF DECISIONS: 0
- COGNITION LINES ADDED: 0 to frozen source; ~40 instrumentation lines in worker-owned copy only
- MODES/BRIDGES/HANDLERS/SEMANTIC CASES: 0/0/0/0

## Verdict

**MINUS-TWO-COMPLETE** with path frequencies. Eight distinct -2 paths inventoried (not five). BOOTSTRAP_FEW dominates at 62%. VERIFY_FAIL_NOEXP identified as structural incapacity misreported as ignorance. Full disambiguation requirements specified.
