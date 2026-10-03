# PREREG: EVICTION-POLICY comparison (FIFO vs owner-partitioned vs pinning)

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: EVICTION-POLICY-COMPARE worker. Lane:
`docs/lab/research-lead/overnight-20260928/eviction_policy/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

L2-INTERFERENCE2 (VERDICT=PASS, 2026-10-03) established the pool
saturation law and the money result that circular FIFO eviction is
flushable: at pool=32 the benign FULL writer is fully absorbed
(ret=100, zero evictions), yet the churn adversary drives retention to
0 along an exact dose-response curve (r=0 -> 100, r=20 -> 54, r=32 -> 0).
Its report recommended, and the task for this lane orders, a fresh
preregistered eviction-policy comparison with the churn adversary held
fixed: FIFO (baseline) vs owner-partitioned vs pinning. This is not a
repair lineage on the L2-INTERFERENCE2 mechanism: the mechanism is
frozen, only the pool eviction policy varies.

## Substrate (frozen)

Single file eviction_policy.zag, self-contained, built directly on the
l2_interference2.zag substrate with these frozen differences:

- Overflow pool size fixed at 32 for all policies and all conditions.
  The POOL0 ablation is not repeated (established in L2-INTERFERENCE2
  K4); the pn==0 branch is removed.
- Header layout: 0 bumpA (FIFO bump pointer; PART class-A bump pointer),
  4 conflicts, 8 evictions, 12 table_full_errors, 16 pool_size (=32),
  20 policy (0 FIFO, 1 PART, 2 PIN), 24 bumpB (PART class-B bump
  pointer), 28 drop (PIN fallback count: relocations refused because the
  pool is full of pinned entries).
- Pool base 2112, 32 slots x 16 bytes (key, val, owners, used), inside
  the 4096-byte workspace.
- Conflict path: conflicts++ on every same-key different-value write
  (identical adversary footprint accounting in all policies), then the
  policy relocation, then the new value installs in the primary table.
- Read path: primary table then all 32 pool slots, owner-scoped,
  unchanged.

## The three policies (frozen)

Policy 0, FIFO (baseline): single circular bump pointer modulo 32.
Relocate the victim into slot bumpA, evict++ when the slot was in use.
This is the exact L2-INTERFERENCE2 code path at pool=32.

Policy 1, PART (owner-partitioned): the victim's owner bitmask selects
a class. Class 1 iff the victim owner is exactly 16 (B-only entries);
class 0 otherwise (any A-family bit set). This classification is exact
under the frozen protocol: benign-phase victims carry bitmasks
{15,7,11,3} (never 16, since B never co-wrote those keys before the
benign writer), and churn-phase victims carry owner exactly 16 (key
3999 is B-only). Each class owns a 16-slot partition (class A: slots
0..15, class B: slots 16..31) with its own circular bump pointer
modulo 16 (bumpA at header 0, bumpB at header 24). Eviction is FIFO
within a class only; a class-B churn can never evict a class-A entry.
Rationale for the 16/16 split, preregistered: an equal split is the
policy that can be stated without tuning to the benign conflict count
(a real owner-partitioned pool does not know the benign load in
advance); the fragmentation cost this imposes is part of what the
experiment measures (see K4).

Policy 2, PIN (pinning): every relocated entry is pinned, meaning it
can never be evicted by any later relocation. The allocator scans the
32 slots for the first free one (used==0) and places the victim there.
If no free slot exists, drop++ and the conflict falls back to
destroy-in-place: the new value installs in the primary table and the
old value is lost. Under the frozen protocol the fallback can only
ever strike churn key 3999 values, which no test reads, so the fallback
cost is isolated to the drop counter rather than to retention. The
pinning tradeoff under test is therefore: zero evictions and full
survival against the measured cost of permanent pool occupancy
(quantified by drop).

## Learned structures and writers (frozen; unchanged from L2-INTERFERENCE2)

Owner bits: A_BASE=1, A_EXT=2, A_SPEC=4, A_TRUNC=8, B=16. A family
taught exactly as in L2-INTERFERENCE2 (35 distinct keys, 35 queries).
Benign writer: teach_B cond=2 (FULL), 20 conflicting writes on
ka(i,hop) = 1000+i*10+hop, i=1..10, hop=1..2, val=777000+i*10+hop,
in B teaching order. Churn adversary (held fixed across all policies):
after the benign writer, write key 3999 (fresh B-owned key) `w` times
with alternating values 900001+w. The first write allocates a primary
slot; each subsequent write conflicts with the previous one and
relocates a B-owned (owner 16) victim. Churn doses are relocation
counts r = w - 1, with w in {1, 21, 33}, i.e. r in {0, 20, 32}.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace with pool_size=32 and the
policy set: 1. teach A family (multi). 2. pre-test (expect 35).
3. teach B benign FULL (20 conflicts). 4. churn adversary with w
writes. 5. post-test; retention = 100 * post_ok / pre_ok. 6. record
conflicts, evictions, drop, B accuracy (20 B reads), rawA (key-level
owner-scoped survival over A's 35 distinct keys).

Conditions (9): FIFO-B0 (policy 0, w=1), FIFO-A20 (policy 0, w=21),
FIFO-A32 (policy 0, w=33), PART-B0 (policy 1, w=1), PART-A20
(policy 1, w=21), PART-A32 (policy 1, w=33), PIN-B0 (policy 2, w=1),
PIN-A20 (policy 2, w=21), PIN-A32 (policy 2, w=33).

## Predicted values (frozen; these ARE the kill-bar targets)

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

Derivation notes (frozen with the prereg).

FIFO: exact reproduction of the L2-INTERFERENCE2 pool=32 rows
(POOL32, ADV32-21W, ADV32-33W): the code path is identical (single
circular pool, 32 slots). Benign: 20 victims fit, ret=100, ev=0.
r=20: 12 churn relocations fill the 12 free slots, 8 evict the oldest
benign victims (i=1..4), post=19, ret=54, ev=8, rawA=27. r=32: all 20
benign victims flushed, post=0, ret=0, ev=20, rawA=15.

PART benign: all 20 victims are class A (bitmasks {15,7,11,3}), so the
class-A 16-slot circular FIFO keeps the last 16 (i=3..10, hops 1,2)
and evicts the 4 oldest (i=1,2). This is exactly the L2-INTERFERENCE2
POOL16 row: A_BASE 8, A_EXT 8, A_SPEC 3 (i=3,4,5), A_TRUNC 8, post=27,
ret=77, ev=4, rawA=31 (base keys survive for i=3..10: 16, plus 10
hop-3 plus 5 guard). PART churn: all churn victims are class B
(owner 16), so they occupy only the class-B partition: r=20 fills 16
slots and evicts 4 B entries (old churn values, read by no test);
r=32 fills 16 and evicts 16 B entries. Class A is untouched, so
ret stays 77 and rawA stays 31 at every dose; ev totals 4+4=8 and
4+16=20.

PIN benign: 20 victims scan into slots 0..19, ev=0, drop=0, post=35.
PIN churn: the 20 benign victims are pinned in slots 0..19. r=20: 12
churn relocations fill slots 20..31 (pinned), the remaining 8 find no
free slot, drop=8, destroy-in-place on key 3999 (old churn values lost,
read by no test). r=32: 12 fill, drop=20. ev=0 always; A entries never
disturbed, so ret=100 and rawA=35 at every dose.

B accuracy stays 20/20 in every condition: B's 20 benign primary
entries are never relocated away from owner 16 in any policy (a
conflict relocates the old value and installs B's new value in the
primary; the PIN fallback only touches key 3999, which the B test does
not read).

## Frozen kill bars

- K1 BASELINE: pre_ok == 35 and bacc == 20 in all 9 conditions. Else
  BUILD-FAIL; no verdict on the policies is drawn.
- K2 FIFO REPRODUCTION: FIFO conditions ret == [100,54,0],
  conflicts == [20,40,52], evict == [0,8,20]. The baseline must
  reproduce the frozen L2-INTERFERENCE2 pool=32 dose-response exactly.
- K3 PARTITION SURVIVAL: PART conditions ret == [77,77,77] across
  r = 0,20,32; evict == [4,8,20]. Retention must be flat across churn
  doses: the partition isolates the protected class from the churn.
- K4 PARTITION COST: PART-B0 ret == 77 (strictly below 100). The
  equal-split partition pays a visible fragmentation cost under benign
  load: 20 class-A victims do not fit in 16 class-A slots.
- K5 PINNING SURVIVAL: PIN conditions ret == [100,100,100] across
  r = 0,20,32. Pinning must hold full retention at every dose.
- K6 PINNING NO-EVICTION: PIN conditions evict == [0,0,0] and
  drop == [0,8,20]. Nothing is ever evicted; the frozen exhaustion cost
  is permanent pool occupancy, quantified by drop.
- K7 ADVERSARY FIXED: conflicts per dose identical across all three
  policies: dose r=0 -> 20 in FIFO-B0, PART-B0, PIN-B0; r=20 -> 40 in
  FIFO-A20, PART-A20, PIN-A20; r=32 -> 52 in FIFO-A32, PART-A32,
  PIN-A32. The churn adversary's footprint must be policy-invariant;
  only the eviction outcome may differ.
- K8 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else VOID.

Verdict: PASS iff K1..K8 all hold. Any kill-bar miss names the bar and
yields FAIL. K1 or K8 failure yields VOID. Thresholds are frozen; they
are not moved after results. rawA is reported as a diagnostic and is
not kill-barred.

Discrimination design: K2 vs K3/K5 separates the flushable baseline
from the two survivors; K4 separates partitioned (pays a benign cost)
from pinning (pays none); K6 separates pinning (never evicts, pays in
drop) from FIFO (evicts, drop always 0); K7 bars the "weaker adversary
under pinning" confound.

## What this does NOT test

The churn adversary is a mechanism stressor on the eviction policy,
not a sealed world and not a claim about realistic learner behavior.
Owner-scoped reads are retained from L2-INTERFERENCE2, so the caveat
about label-free routing carries over unchanged. The 16/16 partition
split is a stated policy choice, not an optimal sizing; other splits
would shift the K3/K4 tradeoff and are out of scope. Pinning as tested
has no unpin or reclamation policy; the drop counter quantifies the
resulting pool exhaustion, and reclamation design is explicitly out of
scope. No claim is made about a full continuing learner.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(eviction_policy.zag), build, runs, and REPORT.md only after.
