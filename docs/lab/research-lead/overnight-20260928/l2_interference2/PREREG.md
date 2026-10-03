# PREREG: L2-INTERFERENCE2 (pool saturation law + adversarial eviction attack)

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: L2-INTERFERENCE2 worker. Lane:
`docs/lab/research-lead/overnight-20260928/l2_interference2/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

L2-INTERFERENCE (VERDICT=PASS) showed that conflict-relocation into an
8-slot circular overflow pool protects co-resident L2-adapted structures
under benign writers, and saturates exactly as predicted at 100 percent
overlap (20 conflicts, 12 evicted, ret=34). This lane pushes the boundary
of that PASS in two directions without redesigning the mechanism:

1. POOL SATURATION LAW (Option A): with the same benign FULL writer
   (20 conflicts), vary the overflow pool size over {0, 4, 8, 16, 32} and
   test whether retention is an exact, predictable function of pool
   capacity. Pool 0 doubles as the mechanism ablation (relocation
   disabled): if the relocation policy is what does the protective work,
   pool 0 must show total loss.
2. ADVERSARIAL EVICTION ATTACK (Option C): after the benign FULL writer,
   a churn adversary repeatedly rewrites one B-owned key with alternating
   values. Each churn write is a conflict against the adversary's own
   previous value, so each one relocates a B-owned entry into the pool and
   evicts the oldest pool entry. This flushes A's relocated entries out of
   the shared FIFO pool even when the pool was large enough to absorb all
   benign conflicts. If the circular eviction policy is the weak point,
   retention must fall along an exact dose-response curve as the churn
   dose grows, and a pool of 32 that fully absorbs the benign writer
   (ret=100) must still be flushable to ret=0 by the adversary.

## Substrate (frozen; parameterized from L2-INTERFERENCE)

Single file l2_interference2.zag, self-contained. All state in one []u8
workspace, i32 little-endian cells via put32/ig helpers. The memory,
hash, teach/test, and conflict-relocation logic are carried over
unchanged from L2-INTERFERENCE except for two additions:

- Header field at offset 16: POOLN (overflow pool size). Pool base 2112,
  POOLN slots x 16 bytes; POOLN <= 32 keeps the pool inside the 4096-byte
  workspace (2112 + 32*16 = 2624).
- Conflict path: if POOLN == 0, the conflicting write destroys the
  existing entry in place (conflicts += 1, no relocation, no eviction).
  Else relocate exactly as in L2-INTERFERENCE, with the bump pointer
  modulo POOLN, and evictions counted when an in-use slot is overwritten.
- read scans the primary table then exactly POOLN overflow slots,
  owner-scoped as before.

Output discipline identical to L2-INTERFERENCE: one preallocated buffer,
cursor-returning emit helpers (e1s/e1i), single _zag_raw_syscall write.
No `as *i32` slice construction in functions. if nesting at most 3.
No `!(A && B)` in while conditions.

## Learned structures and writers (frozen; unchanged)

Owner bits: A_BASE=1, A_EXT=2, A_SPEC=4, A_TRUNC=8, B=16. A family
taught exactly as in L2-INTERFERENCE (35 distinct keys, 35 queries).
The benign writer is teach_B with cond=2 (FULL): 20 conflicting writes
on ka(i,hop) = 1000+i*10+hop, i=1..10, hop=1..2, val=777000+i*10+hop,
in B teaching order ka(1,1), ka(1,2), ..., ka(10,2).

The churn adversary (new): after the benign writer, write key 3999
(a fresh B-owned key) `w` times with alternating values 900001+w.
The first write allocates a slot; each subsequent write conflicts with
the previous one and relocates a B-owned (owner 16) entry into the pool,
evicting the oldest entry. Churn doses are expressed as relocation
counts r = w - 1.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace with POOLN set:
1. teach A family (multi).
2. pre-test: count pre_ok (expect 35).
3. teach B benign FULL (20 conflicts).
4. churn adversary with w writes (w=0 for sweep conditions).
5. post-test: count post_ok; retention = 100 * post_ok / pre_ok.
6. record conflicts, evictions, B accuracy (20 B reads), and rawA:
   key-level owner-scoped survival over A's 35 distinct keys
   (20 base keys owner 1, 10 hop-3 keys owner 2, 5 guard keys owner 4).

Conditions (9): five sweep conditions (w=0, POOLN in {0,4,8,16,32}),
two adversary conditions at POOLN=8 (w in {5,9}, i.e. r in {4,8}),
two adversary conditions at POOLN=32 (w in {21,33}, i.e. r in {20,32}).

## Predicted values (frozen; these ARE the kill-bar targets)

Relocation order under the benign writer is k11,k12,...,k101,k102; the
circular pool retains the last POOLN of the 20 relocated entries.

| cond       | POOLN | w  | pre | post | ret | conflicts | evict | bacc | rawA |
|------------|-------|----|-----|------|-----|-----------|-------|------|------|
| POOL0      | 0     | 0  | 35  | 0    | 0   | 20        | 0     | 20   | 15   |
| POOL4      | 4     | 0  | 35  | 6    | 17  | 20        | 16    | 20   | 19   |
| POOL8      | 8     | 0  | 35  | 12   | 34  | 20        | 12    | 20   | 23   |
| POOL16     | 16    | 0  | 35  | 27   | 77  | 20        | 4     | 20   | 31   |
| POOL32     | 32    | 0  | 35  | 35   | 100 | 20        | 0     | 20   | 35   |
| ADV8-5W    | 8     | 5  | 35  | 6    | 17  | 24        | 16    | 20   | 19   |
| ADV8-9W    | 8     | 9  | 35  | 0    | 0   | 28        | 20    | 20   | 15   |
| ADV32-21W  | 32    | 21 | 35  | 19   | 54  | 40        | 8     | 20   | 27   |
| ADV32-33W  | 32    | 33 | 35  | 0    | 0   | 52        | 20    | 20   | 15   |

Derivation notes (frozen with the prereg). Sweep: POOLN=0 destroys all
20 conflicted keys, so every compound query fails (post=0); the 10
hop-3 keys and 5 guard keys survive at key level (rawA=15). POOLN=4 keeps
the last 4 relocated (i=9,10 hops 1,2): A_BASE 2, A_EXT 2, A_SPEC 0,
A_TRUNC 2, post=6. POOLN=8 keeps i=7..10: post=12 (exact predecessor
reproduction). POOLN=16 keeps i=3..10: A_BASE 8, A_EXT 8, A_SPEC 3
(i=3,4,5), A_TRUNC 8, post=27. POOLN=32 keeps all 20: post=35.
Adversary at POOLN=8: after the benign writer the pool holds the last 8
relocated (i=7..10); r=4 churn relocations evict the 4 oldest (i=7,8),
leaving i=9,10: post=6, ret=17; r=8 flushes all: post=0. Adversary at
POOLN=32: the first 12 churn relocations fill the 12 empty pool slots
(no evictions); r=20 evicts the 8 oldest benign relocations (i=1..4),
leaving i=5..10: A_BASE 6, A_EXT 6, A_SPEC 1 (i=5), A_TRUNC 6, post=19,
ret=54; r=32 flushes all 20: post=0. B accuracy stays 20/20 in every
condition because B's own primary entries are never relocated away from
owner 16.

## Frozen kill bars

- K1 BASELINE: pre_ok == 35 in all 9 conditions. Else BUILD-FAIL; no
  verdict on the mechanism is drawn.
- K2 CAPACITY: POOL32 ret == 100. A pool that holds every conflict must
  absorb them all.
- K3 PREDECESSOR REPRODUCTION: POOL8 ret == 34, conflicts == 20,
  evict == 12. The parameterized substrate must reproduce the frozen
  L2-INTERFERENCE FULL numbers exactly.
- K4 ABLATION: POOL0 ret == 0. With relocation disabled, the benign
  writer must destroy everything the compound queries check.
- K5 SATURATION CURVE: ret over POOLN {0,4,8,16,32} == [0,17,34,77,100]
  exactly. This is the quantitative form of the boundary claim.
- K6 ADVERSARIAL DOSE-RESPONSE: at POOLN=8, ret over r {0,4,8} ==
  [34,17,0] exactly; at POOLN=32, ret over r {0,20,32} == [100,54,0]
  exactly. The money contrast is POOLN=32 benign (100) vs POOLN=32
  fully flushed (0): pool capacity is not protection against an
  eviction-targeting writer.
- K7 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else VOID.

Verdict: PASS iff K1..K7 all hold. Any kill-bar miss names the bar and
yields FAIL. K1 or K7 failure yields VOID. Thresholds are frozen; they
are not moved after results. rawA is reported as a diagnostic and is
not kill-barred.

## What this does NOT test

The churn adversary is a mechanism stressor on the eviction policy, not
a claim about realistic learner behavior. No sealed worlds are used; the
adversary is researcher-designed and fully specified above. Owner-scoped
reads are retained from L2-INTERFERENCE, so the caveat about label-free
routing carries over unchanged.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(l2_interference2.zag), build, runs, and REPORT.md only after.
