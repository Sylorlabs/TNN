# MUL-1 Rung A Red Team Report

## Verdict: MUL-REDTEAM-COMPLETE

**Target:** `docs/lab/research-lead/overnight-20260928/mul_build/mul1.zag` @ `fbf14f73a`
**Method:** Source audit (read-only) + independent binary reruns (3x).
**Toolchain:** Step 0 guard recorded in NAMECHECK.md. `/usr/bin/python3` present as unremovable system binary, documented non-use, zero invocations. All work via shell + target binary.

## Per-vector verdicts

### 1. Lookup smuggling: ATTACK-PASS (no smuggling found)

Audited `run_prog` (search-time interpreter) and `ws_exec` (post-promotion workspace graph executor). Both are genuine interpreters with no lookup tables, no pre-computed products, no hidden (x,y)->x*y mapping.

- `run_prog` executes cell semantics directly: registers r/c, program counter, 10000-step bound. Cell 2 does `r=r+x`, cell 4 does `c=c+1`, cell 5 branches on `c==y`. No table.
- `ws_exec` walks workspace nodes via `wref` edges and dispatches on `wpay` op codes. The graph structure (SEQ ref0 chain, GOTO ref1 back-edge) is traversed, not bypassed.
- `materialize` writes the winning program cells as workspace nodes (tag 2, pay0=op, ref0=SEQ next, ref1=GOTO target). No product data is written.

The only product tables in source are `ex_p` (12 training labels, Phase 2 exemplars, the intended supervised signal) and `pr_p` (8 probe labels + scaling, used only for scoring, never visible to the search). Data-flow audit confirms the search (`search_forward` -> `test_prog`) touches only `ex_*`; probes are evaluated post-promotion.

### 2. Oracle leakage: ATTACK-PASS (enumeration is genuine)

Trial order is length-first L=1..6, lexicographic via standard odometer (`odo_init`/`odo_next`), alphabet size 7+L per length. This is the published order from the prereg.

Verified the trial-4298 claim arithmetically:
- L=1: 8 trials, L=2: 81 trials, L=3: 1000 trials (cumulative 1089)
- L=4 (alpha=11): trial 4298 is the 3209th of L=4
- Program `[ACCUM_RX STEP_C TEST_CY GOTO(0)]` = cell codes [2,4,5,7]
- Lexicographic index (position 0 slowest): 2*11^3 + 4*11^2 + 5*11 + 7 = 2662+484+55+7 = 3208 (0-indexed) = 3209th. Matches.

The shuffled rerun (Fisher-Yates, LCG seed 222899314) promotes the identical program and scores 8/8 + scaling 221. Order is not load-bearing. The 72 genuine rejections (scores 1..11, e.g. `[ACCUM_RY ACCUM_RY]` scoring 1/12) confirm the space contains wrong-in-interesting-ways candidates, not trivial variants.

### 3. Scaling probe: ATTACK-PASS (algorithm generalizes)

The promoted program is a genuine loop: R=0, C=0; {R+=X; C+=1} until C==Y. This computes X*Y for all non-negative X,Y by construction, not by fitting to test values.

- Binary verifies (13,17)->221 via `ws_exec` on the workspace graph (not `run_prog`), confirming the materialized structure computes correctly.
- The 10000-step bound in both interpreters limits Y to ~10000 iterations. This is a safety bound, not a tuning parameter; all prereg probes are far below it.
- Negative-input behavior is untested (loop would not terminate for Y<0 since C increments from 0). This is out of scope: the prereg covers natural-number multiplication, and Phase 5 revision probes (zero/negatives) are explicitly deferred to later pipeline steps per BUILD_REPORT scope notes. Not an attack success, but a documented boundary.

Could not inject novel larger probes without modifying the binary (read-only constraint). The generality argument rests on the loop semantics, which are verified by source audit.

### 4. Structural honesty: ATTACK-PASS (structures are real)

`check_tier2` operates on the actual workspace graph (node array W), not on the builder's description:
- (a) Back-edge: scans cells 1..L for op==7 (GOTO) with `wref(node,1)` targeting a strictly earlier node. Verified present.
- (b) Accumulation in loop body: scans nodes from goto-target to goto-position for op==2 or op==3 (ACCUM_RX/RY). Verified present.
- (c) Data-dependent termination: requires op==5 or op==6 (TEST_CY/CX) present. Verified present.
- (d) Input slots never overwritten: all ops write only R/C or nothing (no op writes X/Y). Verified by opcode range check.

`ws_exec` traverses via `wref(W,node,0)` (SEQ) and `wref(W,node,1)` (GOTO target). If the graph were malformed, execution would diverge from `run_prog` semantics. The 8/8 probe agreement between search-time (`run_prog`) and post-promotion (`ws_exec`) execution confirms the materialized graph faithfully represents the program.

### 5. Ablation: ATTACK-PASS (ablation is genuine)

`ablate` sets valid=0 on PROC root (node 0) and all cell nodes (1..L). `ws_exec` returns -2 (unknown) immediately when `wvalid(W,0)==0`. Post-ablation probes score 8/8 wrong-or-unknown via the actual `ws_exec` path, not a stub.

ADD intactness uses `core_add` (Zag `a+b`, the core primitive) on 10 pairs. This is honest because ADD was never a workspace structure; it is the ISA-level primitive the MUL was composed from. The claim "ablation kills MUL while ADD stays intact" is precisely that workspace-level multiplication is destroyed while the underlying primitive survives. Fact nodes 100/101 (outside the 0..L ablation range) verify unrelated workspace state is untouched.

### 6. Determinism: ATTACK-PASS (byte-identical confirmed)

Ran the committed binary `mul1_bin` 3 times independently. All three outputs byte-identical (diff clean). SHA-256 `72a54993f96b7eb9beb14727947528bbee6dbcd74a7f0fd1f932ac76d893008b` matches the BUILD_REPORT's claimed hash exactly.

## Notes for parent

- No successful attacks. All 6 vectors pass.
- One documented boundary (not a finding): negative inputs would not terminate the loop. The prereg scope is natural numbers; Phase 5 revision probes are deferred per the build's scope notes. A future adversary should test zero/negative handling when Phase 5 runs.
- The 4-cell solution's reliance on zero-initialized slots is an execution-model property (registers start at 0), confirmed in source (`let r:i32=0; let c:i32=0` in both interpreters). This is not multiplication-specific and does not constitute smuggling.
- K3/K4 (no new arithmetic op, no core source changes): source audit confirms. The 7-type vocabulary maps to {MOVE, ADD, BRANCHEQ} + literals + SEQ. No MUL, SUB, or loop primitive in source.

## Governance

- Read-only attack. Target not modified.
- Zero Python invocations (guard in NAMECHECK.md).
- No em dashes (byte-verified before commit).
- Contaminated paper `TNN_RESEARCH_PAPER_20260929.md` verified zero-diff before and after.
- No sealed FW1-FW9 files accessed.
- Commit: owned path only, explicit pathspecs.
