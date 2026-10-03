# H-GENBIAS Result: N-First Generality Bias Fixes Discovery Overfitting

**Date:** 2026-09-29
**Prereg:** PREREG_GENBIAS.md (commit 71e9d3b97, frozen before implementation)
**Method:** Pure Zag, no Python. Binaries built to /tmp only, not committed.
**Raw evidence:** GENBIAS_RAW_OUTPUT.txt (test harness, 3 runs byte-identical),
  STRESS_GENBIAS_RAW.txt (stress re-run, 3 runs byte-identical).

## Verdict: H-GENBIAS SURVIVES (4/4)

| Bar | Result |
|-----|--------|
| K-G1 (overfit fixed) | PASS: uniform n=4 reverse training yields a program generalizing to 5/5 tested lengths (2,3,4,5,6,7); "hello"->"olleh" |
| K-G2 (no regression) | PASS: mixed reverse, broadcast-last, broadcast-first, identity all still work |
| K-G3 (stress survives) | PASS: H-STRESS re-run scores 17/17, H-STRESS SURVIVES (was KILLED 14/17) |
| K-G4 (determinism) | PASS: all runs byte-identical (md5-verified, 3 runs each) |

## The Fix

Two-pass search order in `pdiscover_direct` and `pdiscover_dry`:

- `prog_uses_n(prog_store, prog_index, pi)`: scans node types, returns 1 if
  any node has type 1 (N).
- `try_discover_pass(..., want_n)`: single pass considering only programs
  with `prog_uses_n == want_n`, in original enumeration order.
- `try_dry_pass(..., want_n)`: same for dry-run discovery.
- Pass 1 (`want_n=1`): N-using programs first. Pass 2 (`want_n=0`): fallback
  to original behavior. No program semantics changed, no programs added or
  removed, enumeration itself untouched.

## Evidence

CONTROL (old single-pass discovery, uniform n=4 "abcd>dcba;efgh>hgfe"):
- Found program bytes `3,255,255,4,255,255,0,255,255,6,1,2,5,0,3`
  = ADD(C1, SUB(C2, K)) = `3-K`, exactly as the H-STRESS diagnosis predicted.
- "hello" does NOT map to "olleh" (proc_apply returns 0 on idx=-1 at k=4).
- Bug reproduced in-harness. CONTROL PASS.

K-G1 (new N-first discovery, same training):
- Found program bytes `1,255,255,0,255,255,3,255,255,5,1,2,6,0,3`
  = SUB(N, ADD(K, C1)) = `n-1-k`. The general program.
- Correct reversal on lengths 2,3,4,5,6,7 (5/5). K-G1 PASS.

K-G2 (no regression, new discovery):
- Mixed-length reverse ("abc>cba;xy>yx"): PASS ("hello"->"olleh", "abcd"->"dcba")
- Broadcast-last ("abc>ccc;xy>yy"): PASS ("hello"->"ooooo", "ab"->"bb")
- Broadcast-first ("xqw>xxx;abc>aaa"): PASS ("hello"->"hhhhh", "zb"->"zz")
- Identity ("abc>abc;xy>xy"): PASS ("hello"->"hello", "abcd"->"abcd")

K-G3 (H-STRESS re-run with fixed discovery in stress_learn.zag):
- 16 events, no crash. K-S1 PASS.
- Graceful exhaustion on store-full (honest -1). K-S2 PASS.
- slot0_ok=1: slot 0 (reverse from E1) still maps "hello"->"olleh" after the
  full pressure sequence. K-S3 PASS.
- bridge0_ok=1, caus1_ok=1, caus0_ok=1, ambiguity withholds. K-S4 PASS.
- RESULT: 17/17. H-STRESS SURVIVES (previously KILLED 14/17 on K-S2/K-S3/K-S4
  via the `3-K` overfit; recharacterized by H-DIAG as discovery-time
  overfitting, now repaired at the source).

K-G4: genbias_test 3 runs md5 `21c8b9a06f1e3b55dd6e76261e7ca6ab` (identical);
  stress re-run 3 runs md5 `48766a0f1779d034e0b0d77094e39ed8` (identical);
  unified re-run 2 runs md5 `aa9166f60325a2736ac9bd870e09cc2b` (identical).

H-UNIFIED re-verified with the fix: 9/9, H-UNIFIED SURVIVES (no regression
from the bias change on the mixed-length frontier test).

## Files Changed

- `genbias_test.zag` (new): test harness with old (`pdiscover_direct_old`)
  and new (N-first `pdiscover_direct`) discovery, CONTROL + K-G1 + K-G2.
- `unified_learn.zag` (modified): N-first bias in `pdiscover_direct` and
  `pdiscover_dry`. Frontier mechanism updated.
- `stress_learn.zag` (modified): same fix, for the K-G3 re-run.
- Discovery sections of `unified_learn.zag` and `stress_learn.zag` verified
  identical after patching (diff clean).

## Honest Boundaries

- The bias is a search-order preference, not a proof of generality. A
  pathological N-using fitter that does not generalize could still be
  selected first; none was observed in testing (the affine structure of the
  1055-program space makes this rare, but it is not ruled out).
- The pre-existing F-LEAK (bridge-full slot waste on failed splits, predicted
  in the H-STRESS prereg) is untouched and remains a separate known bug.
- Other copies of the discovery code in the repo (`proc_learn.zag`,
  `bridge_learn.zag`, `route_learn.zag`, `integ_learn.zag`, `proc_cond.zag`)
  still carry the old single-pass search. They should be patched or retired;
  the frontier (`unified_learn.zag`) is fixed.
- Not L3 evidence. This is a robustness repair to a bounded L2+ mechanism.

## Commits

- `71e9d3b97`: Prereg H-GENBIAS FROZEN (K-G1..K-G4)
- (this commit): Implementation + result + raw outputs

## Classification

Bounded L2+ mechanism repair. The procedure discovery generality gap
identified by H-DIAG (and independently by the CC-A3 adversary) is closed
for the tested cases by a minimal, surgical search-order bias.
