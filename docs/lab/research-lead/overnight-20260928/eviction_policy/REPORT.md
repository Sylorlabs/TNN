# REPORT: EVICTION-POLICY comparison (FIFO vs owner-partitioned vs pinning)

Date: 2026-10-03. Worker: EVICTION-POLICY-COMPARE worker.
Prereg: committed alone as 04ba4af7f (strictly before implementation).
Implementation: eviction_policy.zag (pure Zag), built with the pinned
compiler src/tools/toolchain/znc_linux_x86_64_abed8aa1, exit 0, no
warnings on the final build.

## Verdict: PASS

All frozen kill bars hold. 3/3 runs byte-identical
(sha256 16f73dc4aef610c9fc24a3e5c03766c461125ad5ff4a4e50404a0f74973b42af).

## Results (identical across run1/run2/run3)

| cond     | pol | w  | pre | post | ret | cf | ev | drop | bacc | rawA |
|----------|-----|----|-----|------|-----|----|----|------|------|------|
| FIFO-B0  | 0   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| FIFO-A20 | 0   | 21 | 35  | 19   | 54  | 40 | 8  | 0    | 20   | 27   |
| FIFO-A32 | 0   | 33 | 35  | 0    | 0   | 52 | 20 | 0    | 20   | 15   |
| PART-B0  | 1   | 1  | 35  | 27   | 77  | 20 | 4  | 0    | 20   | 31   |
| PART-A20 | 1   | 21 | 35  | 27   | 77  | 40 | 8  | 0    | 20   | 31   |
| PART-A32 | 1   | 33 | 35  | 27   | 77  | 52 | 20 | 0    | 20   | 31   |
| PIN-B0   | 2   | 1  | 35  | 35   | 100 | 20 | 0  | 0    | 20   | 35   |
| PIN-A20  | 2   | 21 | 35  | 35   | 100 | 40 | 0  | 8    | 20   | 35   |
| PIN-A32  | 2   | 33 | 35  | 35   | 100 | 52 | 0  | 20   | 20   | 35   |

Kill bars:
- K1 BASELINE: pre==35 and bacc==20 in all 9 conditions -> PASS
- K2 FIFO REPRODUCTION: FIFO ret==[100,54,0], cf==[20,40,52],
  ev==[0,8,20] -> PASS (exact L2-INTERFERENCE2 pool=32 reproduction)
- K3 PARTITION SURVIVAL: PART ret==[77,77,77], ev==[4,8,20] -> PASS
- K4 PARTITION COST: PART-B0 ret==77 (< 100) -> PASS
- K5 PINNING SURVIVAL: PIN ret==[100,100,100] -> PASS
- K6 PINNING NO-EVICTION: PIN ev==[0,0,0], drop==[0,8,20] -> PASS
- K7 ADVERSARY FIXED: conflicts per dose identical across policies
  ([20]x3, [40]x3, [52]x3) -> PASS
- K8 DETERMINISM: 3/3 byte-identical sha256 -> PASS

## Which policy survives, and the tradeoffs

Both candidate fixes survive the churn adversary; the FIFO baseline
does not. The comparison discriminated as designed, and each policy
pays a different, now quantified, price.

FIFO (policy 0): perfect under benign load (ret=100, zero evictions,
zero waste), catastrophically flushable under churn (ret 100 -> 54 ->
0 at r=0,20,32). Cost: none when unattacked. Robustness: none. This
reproduces the L2-INTERFERENCE2 money result bit for bit on the shared
substrate, so the baseline is anchored, not re-argued.

Owner-partitioned (policy 1, 16/16 split): churn-immune for the
protected class. Retention is flat at 77 across all three churn doses
(K3), because every churn victim is class B and can only evict inside
the class-B partition. The price is fragmentation, and it is visible
even with no adversary (K4): 20 class-A benign victims do not fit in
16 class-A slots, so benign retention is 77, strictly below FIFO's
100, while the class-B half of the pool sits empty. A second, subtler
price: within-class churn still evicts (evict counts 4 -> 8 -> 20 are
all B-owned churn history). That history is read by no test here, so
retention is unaffected, but in a continuing learner the churning
structure's own past would be the casualty. The 16/16 split is a
stated policy choice, not an optimum; any other split moves the
K3/K4 tradeoff, it does not remove it.

Pinning (policy 2): perfect survival at every dose (ret=100, rawA=35)
with literally zero evictions ever (K5, K6). The price is permanent
pool occupancy, quantified by the frozen drop counter: at r=20,
12 of 32 slots are dead churn history and 8 relocations fall back to
destroy-in-place; at r=32, 20 relocations fall back. Pinning converts
churn-driven eviction into a slow memory leak: the pool fills with
pinned entries and never reclaims. In a continuing learner this policy
needs an unpin or reclamation rule, which is the obvious next question
and was deliberately out of scope here.

Head to head: pinning dominates partitioned on retention (100 vs 77
at every dose) and on benign cost (no fragmentation), but its cost is
unbounded-in-time occupancy with no tested reclamation; partitioned
bounds occupancy per class and keeps a working within-class FIFO, but
pays fragmentation up front and protects only along the class
boundary. Neither is free, and the experiment measures each price in
the open rather than hiding it.

## Reading of the results

- K2 matters beyond anchoring: the FIFO dose-response reproduced
  exactly on the policy-parameterized substrate, so the PART and PIN
  numbers are measured against a verified baseline, not a re-derived
  one.
- K7 bars the natural confound: the adversary's footprint (conflict
  counts 20/40/52 per dose) is identical across all three policies, so
  the retention differences are policy effects, not adversary-strength
  artifacts.
- The discrimination design worked as preregistered: K2 vs K3/K5
  separates the flushable baseline from the two survivors; K4 separates
  partitioned (pays a benign cost) from pinning (pays none); K6
  separates pinning (never evicts, pays in drop) from FIFO (evicts,
  drop always 0).

## Honest caveats

- The churn adversary is single-owner: it churns B's own key, so every
  churn victim is class B. Owner-partitioned wins partly because the
  isolation boundary aligns with the adversary's owner. A multi-owner
  churn adversary would flush inside each partition; the isolation is
  per-class, not absolute. Probing that boundary needs its own prereg.
- Pinning's robustness is close to trivial (nothing is ever evicted)
  and its cost is a leak with no tested reclamation. The drop counter
  quantifies the leak; it does not solve it.
- The churn adversary is researcher-designed and fully specified in the
  prereg; it is a mechanism stressor, not a sealed world and not a
  claim about realistic learner behavior.
- Owner-scoped reads are retained from L2-INTERFERENCE2, so the caveat
  about label-free routing carries over unchanged: this is a mechanism
  check on eviction policy in shared memory, not a claim about a full
  continuing learner.
- Per the no-patch-treadmill rule, this lane does NOT canonize a
  policy fix. Both survivors carry a measured cost; choosing between
  them (or designing the missing reclamation policy, or the
  multi-owner adversary probe) belongs to fresh preregistered work.

## Toolchain guard

Safebin active for the whole lane; `which python3` and `which python`
returned nothing at startup and no forbidden executable was invoked at
any point (shell used only for mkdir, git, znc, binary execution,
sha256sum, cmp, and file reads/writes). No PROCESS-FAIL condition
triggered. Per the 2026-10-03 shared-workspace lesson, git writes went
through /usr/bin/git directly.

## Commits

- 04ba4af7f: frozen prereg (PREREG.md + NAMECHECK.md), alone.
- This commit: eviction_policy.zag, eviction_policy_bin, run1/2/3.txt,
  REPORT.md. Local only, never pushed.

## Recommended follow-ups

- A preregistered pinning-reclamation comparison (e.g. unpin on
  read-recency, or bounded pin lifetime) with the churn adversary held
  fixed: pinning won on retention but its leak is unmeasured beyond
  drop.
- A multi-owner churn adversary against the owner-partitioned policy:
  the current PART PASS rests on the single-owner adversary aligning
  with the class boundary.
- Partition-split sensitivity (e.g. 24/8, 8/24, per-bit partitions):
  the K3/K4 tradeoff moves with the split and the curve is currently
  one point.
