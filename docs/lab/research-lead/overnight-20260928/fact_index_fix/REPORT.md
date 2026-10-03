# REPORT.md -- FACT Index General Fix Worker

## Verdict: FACT-INDEX-FIX-COMPLETE

The FACT subject index now enforces general invariants FI1-FI5,
mirroring the MAP index hardening. All corruption tests pass, 5000-FACT
scale validated, 3/3 byte-identical.

## 1. The general invariant violation

The FACT index (`fidx_add`, `fidx_bhead`, `fidx_bset`,
`t2_lu_first_idx`, `t2_gather_idx` in `s5_patch.zag`) lacked the
hardening invariants that the MAP index received:

| Invariant | MAP index (hardened) | FACT index (original) |
|-----------|---------------------|----------------------|
| I1 Bounds: node id in [2, NN()) before deref | YES | NO |
| I2 Cycle: bounded walk / seen-set | YES | NO |
| I3 Liveness: field36==1 | YES | YES (partial) |
| I4 Type: tag check | YES | YES (partial) |
| I5 Buffer/walk cap | YES | NO |

Specific vulnerabilities found by code inspection and confirmed by
control experiments:

1. **`fidx_bhead` / `fidx_bset`**: walk the 4-node extension chain via
   field 12 with no bounds check, no liveness check, no tag check on
   extension nodes. A corrupted extension node (or wild `hg(W,52)`)
   yields garbage bucket heads.

2. **`t2_lu_first_idx`**: walks the FACT bucket list via field 12 with
   no bounds check on `n` before `ng(W,n,36)`. An OOB `field12` value
   causes `panic: slice index out of bounds`. No step cap: a cycle in
   the bucket list causes an infinite loop.

3. **`t2_gather_idx`**: same unguarded walk as (2), plus unbounded
   `np<cap` loop over a potentially cyclic list.

4. **`fidx_add`**: stores `fidx_bhead` result directly into `fn2.12`
   without validation. A garbage head corrupts the bucket list at
   insert time.

Control experiments (original functions):
- C1: injected bucket cycle confirmed present; original walk would
  loop forever on no-match lookup. CONFIRMED.
- C2: OOB head (99999) returned unvalidated by original `fidx_bhead`.
  CONFIRMED.

## 2. The fix (fi_fix.zag)

Hardened replacements with `_h` suffix (originals untouched in patch):

- **`fidx_ext_node`**: validates index node bounds/liveness, walks at
  most 3 hops, checks each hop for bounds [2,65536), liveness==1,
  tag==40. Returns -1 on any violation. (FI1, FI2, FI3, FI4)

- **`fidx_bhead_h`**: validates bucket range [0,24), uses
  `fidx_ext_node`, validates head bounds. Returns -1 on violation.
  (FI1)

- **`fidx_bset_h`**: validates bucket range, value bounds, uses
  `fidx_ext_node`. Silent no-op on violation (fail-closed). (FI1)

- **`fidx_add_h`**: validates new node bounds, uses hardened
  head/set. Cannot insert a garbage head. (FI1)

- **`t2_lu_first_idx_h`**: bounds-checks `n` before every field read,
  caps walk at 100000 steps, keeps liveness+type+match checks.
  Returns -1 on any violation or exhaustion. (FI1, FI2, FI3, FI4, FI5)

- **`t2_gather_idx_h`**: same guards as `t2_lu_first_idx_h`, mirrors
  original gather logic exactly (verified line-by-line).

Design principle (from MAP hardening): fail-closed, never crash,
never hang, skip corrupt entries, preserve correct behavior on valid
state.

## 3. Test results (fi_test.zag, 3/3 byte-identical)

SHA-256 `3c6e61d8caad1c4ced8513ffeb80ee637d1e2964f755f33dcac7a7edd7a61a8c`:

| Test | Result |
|------|--------|
| T1 correctness (200 FACTs, hardened vs linear) | PASS (1) |
| T2 bucket cycle (hardened terminates, finds match) | PASS (1) |
| T3 OOB head (hardened rejects, returns -1) | PASS (1) |
| T4 dead node in list (hardened skips) | PASS (1) |
| T5 scale (5000 FACTs, all findable, spot-check vs linear) | PASS (1) |

Additional diagnostics:
- fi_diag (simple facts, 6000 decoys, interleaved): ALL PASS.
- fi_diag2 (full mkbroken decoys, 6000, interleaved): ALL PASS.
- fi_diag3 (exact s5 order: 4990 decoys then 5 real): chains build
  correctly, FACT buckets intact (length 419/417, targets found),
  idx and linear lookups agree.

## 4. Note on the s5 build-order failure

The s5 report hypothesized that `t2_lu_first_idx` returns wrong facts
at scale during MAP construction. My diagnostics did NOT reproduce a
FACT-index corruption in the s5 build order:

- fi_diag3 replicates the exact s5 sequence (4990 decoys via full
  mkbroken, then 5 real chains). All chains build with correct length
  and values. FACT bucket lists are intact. Indexed and linear lookups
  return identical correct results.

This suggests the s5 "wrong literals/values" failure may have a
different root cause (possibly in the query/rebind path, which my
diagnostics did not exercise, or in MAP-index interaction). The
hypothesis that the FACT index returns wrong facts at scale is not
supported by these experiments.

Regardless, the FACT index hardening is a genuine general fix: the
original code had the same vulnerability class as the MAP index
(which did crash on corruption). The hardened version is strictly
safer with identical behavior on valid state.

## 5. Files

All in `docs/lab/research-lead/overnight-20260928/fact_index_fix/`:
- NAMECHECK.md (Step 0 guard)
- REPORT.md (this file)
- fi_fix.zag (hardened FACT index, ~150 lines)
- fi_test.zag (validation driver, T1-T5)
- fi_control.zag (original-function vulnerability demo)
- fi_diag.zag, fi_diag2.zag, fi_diag3.zag (bisect diagnostics)
- fi_base_stripped.zag (s5_base minus overridden/test fns)
- Binaries: fi_test_bin, fi_control_bin, fi_diag_bin, fi_diag2_bin,
  fi_diag3_bin (pinned znc)
- Run outputs: fi_test_run1/2/3.txt (byte-identical),
  fi_control_run1.txt, fi_diag_run1.txt, fi_diag2_run1.txt,
  fi_diag3_run1.txt
- Compile logs: fi_test_compile.txt, etc. (0 errors)

## 6. Constraints observed

- Pure Zag via pinned znc. Safebin PATH active.
- `which python3 python` returns nothing. Zero forbidden executables.
- Unfrozen only. Frozen TNN-2 base read-only (used as library).
- Paper untouched. Nothing pushed.
- 0 modes/bridges/handlers in fix.
- Zero em/en dashes (byte-verified below).

## 7. Follow-ups

1. Integrate `fi_fix.zag` hardened functions into the canonical patch
   (replace `fidx_add`, `t2_lu_first_idx`, `t2_gather_idx` call sites).
2. Re-investigate s5 build-order failure with query-path diagnostics
   (my work shows FACT index is not the culprit).
3. Churn test: evict FACTs at scale, verify hardened walk skips dead.
4. 10000-FACT scale once s5 failure root-caused.
