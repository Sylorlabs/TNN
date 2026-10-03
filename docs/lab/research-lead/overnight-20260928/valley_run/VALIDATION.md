# Valley battery step (b): instance generation and validation

Prereg: `cf0c85e78` (frozen before instance generation).
Design: `VALLEY_DEPTH_DESIGN.md` (`76c7a887c`).
Implementer: Valley Runner, 2026-09-30. Pure Zag, no Python.

## Implementation

- `vinst.zag`: frozen GENEXEC2 straight-line VM (verified op-for-op against
  the embedded VMs of B, C2-clean, D on straight-line code), instance
  table, canonical paths, scoring.
- `vgen.zag`: V1 (score profile), V2 (REF-GREEDY), V3 (exhaustive 1-edit
  plus 2-edit neighborhoods).
- V4 drivers for frozen A and C1 were not built: every instance was
  already dropped at V1/V3, so calibration runs would test dropped
  instances. This is documented, not skipped silently.
- V5: 3/3 byte-identical validation runs (sha256 below).

## Result

**0 of 14 valley instances accepted. All dropped with documentation.**

CAL-0 passes (not a valley instance; s0=1, IN0 solves 9/9).

### Family K (12 instances): all DROP at V3

V1 PASS and V2 PASS for all 12. V3 FAIL: exhaustive search finds a
solving program within 2-op edit distance of a canonical prefix.

The structural cause: P3 = [PUSH 0, PUSH 1, IN0]. Appending two ops
reaches a solver:

- K=1 (all depths): [PUSH 0, PUSH 1, IN0, DIV] (4 ops). Computes 1/x
  with div-by-zero yielding 0, which is 1 iff x=1 on x>=0. One append
  from P3 (found via 2-edit enumeration; also 1-edit from P3).
- K in {2,5,9}: [PUSH 0, PUSH 1, IN0, PUSH K, EQ] (5 ops). Computes
  x==K directly. Two appends from P3.
- (n=2,K=3): [PUSH 0, PUSH 1, IN0, PUSH 2, GT] (5 ops). x>2 iff x=3
  on x in 0..3. Two appends from P3.

The prereg disclosed [IN0, PUSH K, SUB, PUSH 0, EQ] as a 5-op shortcut
"beyond 2 ops". The programs above are different programs that lie
within 2 ops of P3, so V3 as frozen rejects the instances. The
canonical bit-test route is not the shallowest route; the valley is
not real.

### A1: DROP at V1

The C2 walkthrough (`e658766bd` section 5) repair sequence after P0 is
[IN0, PUSH 1] then [IN0, ADD, ADD], giving F=[PUSH 1, IN0, PUSH 1,
IN0, ADD, ADD] (7 ops). V1 over non-empty proper prefixes: k=3 scores
1 (tie with s0=1), k=5 scores 1 (tie). Two ties violate "at most one
ties". The alternative 5-op canonical [PUSH 1, IN0, PUSH 2, MUL,
PUSH 1, ADD] passes V1 but fails V3 ([PUSH 1, IN0, PUSH 2, MUL, ADD]
solves and is 1 edit from its P4). No canonical satisfies V1+V3
simultaneously under the frozen constraints.

### A2: DROP at V3

V1 PASS (one proper prefix, score 0, no ties; full scores 17/17).
V2 PASS (REF-GREEDY halts at 7/17). V3 FAIL: [IN0, PUSH -3, MOD]
(3 ops) solves 17/17 and is two appends from P1=[IN0]. The VM's
mod_nonneg with a negative divisor yields x mod 3 for x>=0, so this
is a genuine 3-op solver the design did not anticipate.

## V5 determinism

```
ba6f3f8ffb7153eeaf08c9861877e3df030786a7fece0530f309b33f946f4304  build/vgen_run3.txt
ba6f3f8ffb7153eeaf08c9861877e3df030786a7fece0530f309b33f946f4304  build/vgen_run4.txt
ba6f3f8ffb7153eeaf08c9861877e3df030786a7fece0530f309b33f946f4304  build/vgen_run5.txt
```
3/3 byte-identical: yes.

## Consequence

With zero accepted instances, mechanism runs (step c) have no valid
input. The battery is void under the frozen prereg. Verdict:
VALLEY-FAIL (validation gate; no mechanism was run).
