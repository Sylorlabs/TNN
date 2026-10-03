# REPORT: L2-INTERFERENCE2 (pool saturation law + adversarial eviction attack)

Date: 2026-10-03. Worker: L2-INTERFERENCE2 worker.
Prereg: committed alone as 2898c0649 (strictly before implementation).
Implementation: l2_interference2.zag (pure Zag), built with the pinned
compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1, exit 0, no
warnings on the final build.

## Verdict: PASS

All frozen kill bars hold. 3/3 runs byte-identical
(sha256 8eb6215d14ca2deda056e6259533e834c55bd8d74ac09468075056b1de753f55).

## Results (identical across run1/run2/run3)

| cond      | pool | churnw | pre | post | ret | conflicts | evict | bacc | rawA |
|-----------|------|--------|-----|------|-----|-----------|-------|------|------|
| POOL0     | 0    | 0      | 35  | 0    | 0   | 20        | 0     | 20   | 15   |
| POOL4     | 4    | 0      | 35  | 6    | 17  | 20        | 16    | 20   | 19   |
| POOL8     | 8    | 0      | 35  | 12   | 34  | 20        | 12    | 20   | 23   |
| POOL16    | 16   | 0      | 35  | 27   | 77  | 20        | 4     | 20   | 31   |
| POOL32    | 32   | 0      | 35  | 35   | 100 | 20        | 0     | 20   | 35   |
| ADV8-5W   | 8    | 5      | 35  | 6    | 17  | 24        | 16    | 20   | 19   |
| ADV8-9W   | 8    | 9      | 35  | 0    | 0   | 28        | 20    | 20   | 15   |
| ADV32-21W | 32   | 21     | 35  | 19   | 54  | 40        | 8     | 20   | 27   |
| ADV32-33W | 32   | 33     | 35  | 0    | 0   | 52        | 20    | 20   | 15   |

Kill bars:
- K1 BASELINE: pre==35 in all 9 conditions -> PASS
- K2 CAPACITY: pool32 ret=100, bar==100 -> PASS
- K3 PREDECESSOR REPRODUCTION: pool8 ret=34, conflicts=20, evict=12,
  bars==[34,20,12] -> PASS
- K4 ABLATION: pool0 ret=0, bar==0 -> PASS
- K5 SATURATION CURVE: ret=[0,17,34,77,100], need=[0,17,34,77,100] -> PASS
- K6 ADVERSARIAL DOSE-RESPONSE: pool8 [34,17,0], pool32 [100,54,0],
  both exact -> PASS
- K7 DETERMINISM: 3/3 byte-identical sha256 -> PASS

## What was tested

Built directly on L2-INTERFERENCE (no mechanism redesign): the same A
family (A_BASE/A_EXT/A_SPEC/A_TRUNC, 35 queries), the same benign FULL
writer (20 conflicting value substitutions), the same conflict-relocation
policy with owner-scoped reads. Two additions: (1) a parameterized
overflow pool size POOLN in {0,4,8,16,32} (POOLN=0 disables relocation:
the mechanism ablation); (2) a churn adversary phase that rewrites one
B-owned key with alternating values after the benign writer, each churn
write relocating a B-owned entry into the pool and evicting the oldest
entry (FIFO flush).

## Reading of the results

- The saturation law is exact. All nine conditions match the prereg
  predictions bit for bit, including the non-obvious interior points
  (pool=16 -> ret=77, pool=4 -> ret=17) and the rawA key-level
  diagnostics. Retention is a deterministic, hand-derivable function of
  (conflict count, pool size, writer order). The mechanism model from
  L2-INTERFERENCE is quantitatively correct, not just directionally.
- K3 reproduces the predecessor's FULL numbers exactly (ret=34,
  conflicts=20, evict=12) on the parameterized substrate: the follow-up
  did not drift from the frozen mechanism.
- K4 confirms the relocation policy does the protective work: with it
  disabled, the benign writer destroys everything the compound queries
  check (ret=0). The L2-INTERFERENCE PASS was earned by the mechanism,
  not by the substrate being insensitive.
- The money result is K6: pool capacity is NOT protection against an
  eviction-targeting writer. At pool=32 the benign writer is fully
  absorbed (ret=100, zero evictions), yet the churn adversary flushes
  all 20 of A's relocated entries and drives retention to 0, along an
  exact dose-response curve (r=0 -> 100, r=20 -> 54, r=32 -> 0 at
  pool=32; r=0 -> 34, r=4 -> 17, r=8 -> 0 at pool=8). The circular FIFO
  eviction policy is the weak point: a writer that churns its own keys
  starves everyone else's relocated entries. In a continuing learner, a
  frequently-updating structure co-resident with others would do exactly
  this by accident, not malice.
- Interference stays one-sided throughout: B accuracy is 20/20 in every
  condition, including under full adversarial flush. The writer is never
  damaged; only the earlier structures lose.
- rawA (key-level survival) isolates mechanism from test structure: the
  10 hop-3 keys and 5 guard keys, never conflicted, survive every
  condition (rawA floor 15); compound queries mask them, which is why
  ret can read 0 while 15 of 35 keys remain readable.

## Honest caveats

- The churn adversary is researcher-designed and fully specified in the
  prereg; it is a mechanism stressor, not a sealed world and not a claim
  about realistic learner behavior. The qualitative point (FIFO eviction
  is flushable by churn) transfers to any co-resident high-churn writer,
  but the exact dose numbers are construction artifacts.
- Owner-scoped reads are retained from L2-INTERFERENCE, so the caveat
  about label-free routing carries over unchanged: the result is a
  mechanism check on conflict-relocation and eviction policy in shared
  memory, not a claim about a full continuing learner.
- Per the no-patch-treadmill rule, this lane does NOT propose an
  eviction-policy fix. The boundary is now mapped; competing hypotheses
  (owner-partitioned pool, pinned entries, recency-weighted eviction)
  belong to a fresh preregistered comparison, not to a repair lineage on
  this mechanism.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup and no forbidden executable was invoked at
any point (shell used only for mkdir, git, znc, binary execution,
sha256sum, and file reads/writes). No PROCESS-FAIL condition triggered.

## Commits

- 2898c0649: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: l2_interference2.zag, l2_interference2_bin, run1/2/3.txt,
  REPORT.md. Local only, never pushed.

## Recommended follow-ups

- Option B (cross-structure analogical transfer: re-adapting a structure
  for a new purpose without interference) remains untested and is the
  natural next lane; it needs its own prereg.
- A fresh preregistered comparison of eviction policies under the churn
  adversary (FIFO vs owner-partitioned vs pinning), with the adversary
  held fixed, would discriminate candidate fixes without a patch
  treadmill.
