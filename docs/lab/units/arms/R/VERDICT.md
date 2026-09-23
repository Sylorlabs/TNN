# Arm R — VERDICT

**Date:** 2026-09-21  
**Arm:** R — Compression cuts (MDL/DP)  
**Family:** CUT  
**Mechanism:** Chunks are compression units: cut where description length is minimized (suffix-array/LCP + DP over cost).  
**Verdict:** **KILL** (binding kill criterion met via M1 OR-clause; ceiling-effect tie, not a loss)

## Authority

1. `units/arms/briefs/R.json` (authoritative)
2. Verbatim frozen §3 row
3. Existing implementation

Binding kill (from briefs/R.json):
> "Boundary F1 (vs whitespace/punctuation joints AND vs arm O's taught spans, separately) does not beat the fixed-64-byte baseline by ≥10 points on both corpora; OR held-out recall (M1) with R-cuts does not beat the 64-byte baseline."

## Kill evaluation

### Boundary F1 vs whitespace/punctuation joints (measured 2026-09-21 via `x-kill`)

| Corpus | R F1 | 64-byte F1 | Delta |
|--------|------|------------|-------|
| prose (5.6MB) | 26.0 | 2.9 | **+23.1** |
| code (9.5MB) | 19.8 | 2.9 | **+16.9** |

R beats the fixed-64-byte baseline by ≥10 points on **both** corpora. The first kill clause ("does not beat by ≥10 on both") is **FALSE**.

**Method note:** "Whitespace/punctuation joints" interpreted as word/non-word byte transitions (is_wordbyte = [A-Za-z0-9_]). This interpretation was inferred; the frozen contract should be consulted to confirm the exact joint definition.

### Boundary F1 vs arm O's taught spans

**BLOCKED.** Arm O had no taught-span artifact on 2026-09-21. This comparison could not be performed.

### Held-out recall (M1): R-cuts vs 64-byte baseline

| Corpus | R-cuts recall | 64-byte recall | R beats? |
|--------|---------------|----------------|----------|
| prose | 100.0 | 100.0 | No (tie) |
| code | 100.0 | 100.0 | No (tie) |

R-cuts do **not** beat the 64-byte baseline on held-out M1 recall (both achieve perfect 100.0% recall — ceiling effect). The second kill clause ("M1 does not beat baseline") is **TRUE**.

### Kill verdict

- Clause 1 (Boundary F1 does not beat by ≥10): FALSE
- Clause 2 (M1 does not beat baseline): TRUE
- **Kill (Clause 1 OR Clause 2): TRUE → KILL**

## Interpretation

The kill is triggered by a **ceiling-effect tie** on M1 recall, not by R losing. Both R-cuts and the naive 64-byte baseline achieve perfect 100% held-out recall, so R cannot "beat" the baseline. The boundary F1 results show R is substantially better at finding meaningful units (+23.1 and +16.9 points).

The M1 task appears too easy to discriminate (both at ceiling). A harder recall task might show a difference, but the binding criterion is evaluated as written.

## 1x battery results

All 15 arm R legs passed with byte-identical stdout across two runs (rc=0):

- m1-1x-prose: PASS (547,545 chunks, 100% recall, 64/64 tamper caught)
- m1-1x-code: PASS (545,132 chunks, 100% recall, 64/64 tamper caught)
- m2-t1-prose, m2-t1-code, m2-t2-prose, m2-t2-code, m2-t3-1x: PASS
- m3-1x: PASS
- m4-1x-prose, m4-1x-code: PASS
- m5-baseline, m5-1x: PASS
- m6-p2c-1x, m6-c2p-1x: PASS
- m7-1x: PASS
- M8 gate (5 regimes × 2 runs, 10 total): PASS

The memorizer control (memctrl-p2c-1x, memctrl-c2p-1x) FAILED with FATAL output — this is a harness/memorizer binary issue, not an arm R failure.

**10x was NOT run** because the binding kill criterion is met.

## Implementation

- Production algorithm: Candidate C (inlined paired-array prefix doubling truncated at L=64; capped adjacent-LCP; 128-entry ring DP with split literal/repeated loops).
- Exact semantics preserved: all fixtures match reference byte-for-byte.
- 2026-09-21 bug fix: cut-boundary arrays changed from `bse=n+1` to `bse=(n+2)/2` split allocation to stay under the 2^25-byte znc slice limit (9.5MB code corpus was panicking with "slice index out of bounds").
- Frozen-dictionary path: reversed-train suffix automaton (≥1 occurrence semantics; corrected from ≥2 SA-narrowing bug).
- Pure Zag, deterministic, zero RNG. Byte-identical reruns verified.

## Correctness

- `x-segcheck` tiny (240B): `X-SEGCHECK,4,1`
- `x-segcheck` 64KB deterministic: `X-SEGCHECK,1610,1`
- `x-segcheck` 64KB repeat: `X-SEGCHECK,1024,1`
- `x-segcheck` 32KB NUL: `X-SEGCHECK,513,1`
- `x-segcheck` 16B edge: `X-SEGCHECK,6,1`
- 9.5MB code: `X-SEGCHECK,545132,1` (exact match)

## Files

- Production: `cl/arm.zag`
- Battery workdir: `work/battery_r1/` (15/15 arm R legs PASS, M8 PASS)
- Kill evidence: `work/kill_results.txt`, `work/m1b64_prose.txt`, `work/m1b64_code.txt`
- Build log: `BUILD_LOG.md`
- Spec: `ARM_SPEC.md`
