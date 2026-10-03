# PREREG: MULTI-OWNER-CHURN probe (2-3 owner churn vs FIFO, PART, PIN)

Frozen 2026-10-03. This preregistration strictly precedes implementation.
This prereg commit contains ONLY PREREG.md and NAMECHECK.md. No kill bar
below may be weakened or reinterpreted after results are seen. VOID is
terminal: it is corrected only by fresh preregistration plus a fresh run,
never by salvage or amend-and-promote.

Worker: MULTI-OWNER-CHURN worker. Lane:
`docs/lab/research-lead/overnight-20260928/multiowner_churn/`.
Commits local only, never pushed. Explicit pathspecs on every commit.
No `git reset`. Pure Zag for all scientific computation; shell only for
znc invocation, binary execution, git ops, sha256sum, and file movement.
Pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(`znc 2026.07.0-dev (edition 2026)`).

## Objective

EVICTION-POLICY (VERDICT=PASS, 2026-10-03) compared FIFO vs
owner-partitioned vs pinning under a SINGLE-owner churn adversary and
honestly caveated its own money result: "The churn adversary is
single-owner, so PART's win partly aligns with the class boundary. A
multi-owner churn probe is the natural next prereg." This lane runs
that probe. The mechanism is frozen; only the adversary gains owners.
The parent questions under test: (1) does owner-partitioned still win
when churn crosses the class boundary, (2) does pinning still survive.

## Substrate (frozen)

Identical to the EVICTION-POLICY substrate, byte for byte in mechanism:
same header layout (0 bumpA, 4 conflicts, 8 evictions, 12
table_full_errors, 16 pool_size=32, 20 policy, 24 bumpB, 28 drop), same
pool (base 2112, 32 slots x 16 bytes), same conflict path (conflicts++
on every same-key different-value write, then policy relocation, then
install), same owner-scoped read path, same A family (35 queries), same
benign B writer (cond=2 FULL, 20 conflicts, victims with bitmasks
{15,7,11,3}), same PART classification (class 1 iff victim owner is
exactly 16, else class 0), same 16/16 PART split, same PIN first-free
scan with drop fallback. The only new code is the multi-owner churn
routine; the single-owner churn routine is carried over unchanged.

## The multi-owner churn adversary (frozen)

M2 (2 owners): keys 3998 (owner 8) and 3999 (owner 16), w=21 writes
each, interleaved per round as 3998 then 3999. Values 800001+j and
900001+j for round j in 0..20. Owner 8 carries an A-family bit, so its
victims classify as class A under PART: the churner is INSIDE the
protected class. Owner 16 is the old B-only churner (class B).

M3 (3 owners): keys 3997 (owner 4), 3998 (owner 8), 3999 (owner 16),
w=21 writes each, interleaved per round as 3997, 3998, 3999. Values
700001+j, 800001+j, 900001+j. Two churners inside class A, one in
class B.

Churn relocation counts: M2 = 2*(21-1) = 40; M3 = 3*(21-1) = 60.
The first write of each key allocates its primary slot; each later
write conflicts with its own previous value and relocates a victim
carrying exactly that write's owner.

## Protocol (frozen)

Per condition, on a freshly zeroed workspace: 1. teach A family
(multi). 2. pre-test (expect 35). 3. teach B benign FULL (20
conflicts). 4. churn: single-owner key 3999 (baseline, w in {1,21,33})
or multi-owner M2/M3 (w=21 per key). 5. post-test; retention =
100*post/pre. 6. record conflicts, evictions, drop, B accuracy, rawA.

Conditions (15): the 9 EVICTION-POLICY baseline conditions unchanged
(FIFO-B0, FIFO-A20, FIFO-A32, PART-B0, PART-A20, PART-A32, PIN-B0,
PIN-A20, PIN-A32) plus 6 multi-owner conditions (FIFO-M2, FIFO-M3,
PART-M2, PART-M3, PIN-M2, PIN-M3).

## Predicted values (frozen; these ARE the kill-bar targets)

Baseline 9 conditions reproduce the frozen EVICTION-POLICY table
exactly (all 8 metric columns):

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

Multi-owner 6 conditions (frozen derivation follows the table):

| cond    | pol | keys | pre | post | ret | cf | ev | drop | bacc | rawA |
|---------|-----|------|-----|------|-----|----|----|------|------|------|
| FIFO-M2 | 0   | 2    | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| FIFO-M3 | 0   | 3    | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| PART-M2 | 1   | 2    | 35  | 0    | 0   | 60 | 28 | 0    | 20   | 15   |
| PART-M3 | 1   | 3    | 35  | 0    | 0   | 80 | 48 | 0    | 20   | 15   |
| PIN-M2  | 2   | 2    | 35  | 35   | 100 | 60 | 0  | 28   | 20   | 35   |
| PIN-M3  | 2   | 3    | 35  | 35   | 100 | 80 | 0  | 48   | 20   | 35   |

Derivation notes (frozen with the prereg).

FIFO: benign leaves 20 victims and 12 free slots. M2: 40 churn
relocs, first 12 fill slots 20..31, remaining 28 evict (ev=28);
relocation coverage spans all 32 slots, so every benign victim is
flushed (post=0, ret=0). M3: 60 relocs, 12 fill, 48 evict. rawA=15 in
both: the flush kills all 20 benign victims; the 15 survivors are the
10 A_EXT hop-3 keys (never conflicted, still in the primary table) and
the 5 A_TRUNC guard keys (never touched). cf = 20 benign + churn
relocs = 60 / 80.

PART: benign phase is identical to baseline (20 class-A victims, 4
evictions, bumpA=4 after wrap). M2 class-A churn (key 3998, owner 8):
20 relocs land on slots 4..15, 0..3, 4..7, i.e. all 16 class-A slots,
every one in use, so 20 within-class evictions and every benign
class-A entry is overwritten (post=0, ret=0). Class-B churn (key
3999, owner 16): 20 relocs into the empty 16-slot class-B partition,
16 fill and 4 evict. ev = 4 (benign) + 20 (class-A churn) + 4
(class-B churn) = 28. M3: class-A churn is 40 relocs (keys 3997+3998,
owners 4 and 8), all into in-use class-A slots, 40 evictions; class-B
as before, 4; benign 4. ev = 4 + 40 + 4 = 48. post=0, ret=0, rawA=15
in both, by the same survival argument as FIFO.

PIN: the 20 benign victims pin slots 0..19. M2: 40 churn relocs fill
the 12 remaining free slots and 28 fall back to destroy-in-place
(drop=28); M3: 60 relocs, 12 fill, drop=48. ev=0 always; no entry is
ever disturbed, so ret=100, rawA=35 at both doses.

bacc=20 in all 15 conditions: churn keys 3997/3998/3999 are distinct
from every benign key, and a conflict relocation only ever moves the
churn key's own previous value, so B's 20 benign primary entries
(owner 16, values 777000+i*10+hop) are never disturbed.

## Frozen kill bars

- K1 BASELINE-REPRO: all 9 baseline conditions match the frozen
  EVICTION-POLICY table exactly, every column. Else VOID: a broken
  baseline makes the multi-owner numbers uninterpretable.
- K2 PART-COLLAPSE: PART-M2 ret == 0 AND PART-M3 ret == 0. Owner
  partitioning does not survive churn that crosses the class boundary;
  the protected partition is flushed from the inside.
- K3 PART-ACCOUNTING: PART-M2 ev == 28 AND PART-M3 ev == 48
  (4 benign + 20/40 class-A churn + 4 class-B churn). Every churn
  relocation after partition fill must appear as a within-class
  eviction; nothing may be lost silently.
- K4 FIFO-FLUSH: FIFO-M2 ret == 0 and ev == 28; FIFO-M3 ret == 0 and
  ev == 48. FIFO remains flushable; multi-owner churn is no harder for
  it than saturation by a single owner.
- K5 PIN-SURVIVE: PIN-M2 and PIN-M3 ret == [100,100], ev == [0,0],
  drop == [28,48]. Pinning survives multi-owner churn with zero
  evictions; the leak cost grows with the dose.
- K6 ADV-FIXED: conflicts per multi-dose identical across policies:
  60 in FIFO-M2, PART-M2, PIN-M2; 80 in FIFO-M3, PART-M3, PIN-M3. Only
  the eviction outcome may differ by policy.
- K7 BACC: bacc == 20 in all 15 conditions.
- K8 DETERMINISM: 3/3 runs byte-identical (sha256 equal). Else VOID.

Verdict: PASS iff K1..K8 all hold. A PASS verdict answers the parent
questions as preregistered: (1) owner-partitioned does NOT still win
when churn crosses the class boundary (ret 77 -> 0 in M2/M3); (2)
pinning still survives (ret 100) at a growing occupancy cost (drop
28/48). Any kill-bar miss names the bar and yields FAIL. K1 or K8
failure yields VOID. Thresholds are frozen; they are not moved after
results. rawA is reported as a diagnostic and is not kill-barred.

Discrimination design: K1 anchors the substrate to the exact frozen
baseline (any drift invalidates the probe); K2 vs K5 separates the
boundary-aligned survivor (PART, collapses) from the boundary-free
survivor (PIN, holds); K3/K4 account every eviction so the collapse
is measured, not narrated; K6 bars the "stronger adversary under
PART" confound.

## What this does NOT test

This probe answers whether PART's win was boundary-aligned; it does
not propose a repaired partitioning scheme (adaptive splits,
per-owner partitions, churner detection) and per the
no-patch-treadmill rule it canonizes none. Pinning reclamation is
still out of scope; the drop counter again only quantifies the leak.
The multi-owner churner is researcher-designed and fully specified
above; it is a mechanism stressor, not a sealed world. Owner-scoped
reads are retained, so the label-free routing caveat carries over.

## Commit order

PREREG.md + NAMECHECK.md commit strictly first. Implementation
(multiowner_churn.zag), build, runs, and REPORT.md only after.
