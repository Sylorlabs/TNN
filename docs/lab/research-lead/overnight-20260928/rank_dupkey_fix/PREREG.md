# PREREG: RANK-DUPKEY-FIX (duplicate-key repair for Sim B)

Date: 2026-10-03. Worker: RANK-DUPKEY-FIX (non-ledger task;
claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_dupkey_fix/.
Frozen: this file is committed alone before any
implementation. No errata; no post-result bar changes.

## Background

RANK-SEALED-ADVERSARIAL (VERDICT=FAIL 7/8) mapped Sim B's
generality boundary: Sim B is exact on 13/13
non-adversarial worlds but BREAKS on S7 DUPKEY (mm=1,
d=45). White-box root cause: key 1051 has two
cold-resident entries (slots 8 and 53). The substrate's
`cold_lookup` scans slots 0..63 and hits the LOWEST slot
holding the key (slot 8, charges 9). Sim B's `sim_prosp`
keeps a key->slot map `ks` that stores only the LATEST
install slot per key (slot 53, charges 54). Generality
boundary: Sim B assumes at most one cold-resident entry
per key. This lane implements the recommended repair
(lowest-slot hit semantics in Sim B) under a fresh prereg.

## Frozen repair spec (additive; substrate untouched)

In `sim_prosp` only (`sim_predict`/`pw` are dead code in
main and stay untouched; the substrate is byte-unchanged):

1. New variant seqmove=2: the fixed entry-attached
   exile-seq model (identical to seqmove=1, including the
   `sq` swap on periodic swap) PLUS the duplicate-key
   repair. seqmove=0 (legacy) and seqmove=1 (parent Sim B)
   are preserved bit-for-bit as controls.
2. Hit path (et==1): replace `sraw = ks[key]` with a
   lowest-slot scan of the sim's slot->key layout `sk`:
   the first slot 0..63 holding the key. This mirrors the
   substrate's `cold_lookup` scan order. Cost charged is
   sraw+1; layout validation compares sraw against the rk4
   trace's pre-move slot as before.
3. Promote path (et==3): replace `ps = ks[key]` with the
   same lowest-slot scan of `sk`. Rationale: the substrate
   promotes the entry it hit (post-move slot); the sim's
   hit entry is the lowest-slot entry, so the freed slot
   must be found the same way. (S7's pm=0 never exercises
   this path; the new sealed S9 world does.)
4. `ks` continues to be maintained as before (harmless);
   on non-duplicate worlds the lowest-slot scan provably
   equals `ks[key]` (single entry per key; all update
   sites keep `sk`/`ks` consistent), so seqmove=2 must be
   behaviorally identical to seqmove=1 wherever no key has
   two cold-resident entries.

## Frozen sealed world S9 (DUPKEY-PROMOTE)

New driver `run_dupkey_pm1` (substrate untouched; same
phases A-D as the frozen S7 `run_dupkey`, then pm=1
reads):

1. mem_zero(M); M[16]=32; M[20]=6; M[32]=16.
2. teach_A(M,1,TR,tro); teach_B(M,2,TR,tro).
3. j=0..33: mem_write(M,3999,900001+j,16,TR,tro).
4. tr_rec(TR,tro,4,0,1,0).
5. mem_write(M,1051,888051,16,TR,tro).
6. tr_rec(TR,tro,4,0,2,0).
7. j=34..66: mem_write(M,3999,900001+j,16,TR,tro).
8. tr_rec(TR,tro,4,0,3,0).
9. Twice: mem_read_recov(M,1051,1,1,rk,TR,tro).
   (owner=1, pm=1: first read rc 0->1, no promote;
   second read rc 1->2, promote fires on the hit entry.)
10. R row records ro+92=cold_cost total,
    ro+128=rank_cost total; other fields zero.

Rows: S9 rk0/rk4 = rows 35/36 (ro=r*144, tro=r*24592).
Buffers: R 5328 (37 rows x 144); TR 909904 (37 x 24592);
OB 65536; RES3 544 (17 rows x 32).

Predicted substrate behavior (white-box, pre-freeze):
both reads hit cold slot 8 (lowest slot holding 1051
with owner intersecting 1); the second read promotes the
entry (pm=1, rc=2), freeing slot 8 and exiling one pool
victim to the first free cold slot. The unrepaired
seqmove=1 sim breaks at the first hit (ks[1051]=53);
a hit-only repair without the et==3 repair would break
at the promote (frees slot 53 instead of 8).

## Frozen design

1. Copy rank_sealed_adversarial.zag to rank_dupkey_fix.zag;
   LANE=RANK-DUPKEY-FIX. All substrate functions (through
   run_dupkey) byte-unchanged.
2. `sim_prosp`: add the seqmove=2 repair (hit scan +
   promote scan); `sq` swap condition becomes
   seqmove==1 || seqmove==2.
3. Add `run_dupkey_pm1` (frozen S9 script above) and
   `s9_valid(TR,tro)` (1 iff key 1051 has >=2 etype-2 AND
   >=1 etype-1 AND >=1 etype-3 records in the trace).
4. main(): rows 0-34 identical calls; rows 35/36 S9
   rk0/rk4; parent RES/RES2 suites unchanged (regression
   control, incl. S7 seqmove=1 break reproduction);
   new RES3 suite (17 rows): M2C2,V1-V6,S1-S6,S8 x
   seqmove=2 (14 rows), S7 x seqmove=2, S9 x seqmove=1,
   S9 x seqmove=2.
5. Kill-bar evaluation in main; per-world SUM lines for
   the new-variant runs; K-bar lines; verdict line.

## Frozen kill bars

- K1 SUBSTRATE-ANCHOR: row 0 bit-for-bit equals the frozen
  RANK-LAZY row-0 values (same 35 field checks as the
  parent K1). The substrate copy is untouched; any
  deviation fails.
- K2 DUPKEY-FIXED: S7 with seqmove=2: mm==0 AND d==0
  (predB - meas). The S7 break is gone.
- K3 NO-REGRESSION: each of the 14 non-duplicate worlds
  (M2C2,V1,V2,V3,V4,V5,V6,S1,S2,S3,S4,S5,S6,S8) with
  seqmove=2: d==0 AND mm==0. The repair must not perturb
  any world without duplicate keys.
- K4 PROMOTE-DUPKEY: S9 with seqmove=2: mm==0 AND d==0.
  Validates the et==3 (promote) half of the repair, which
  S7 cannot exercise (pm=0).
- K5 REPAIR-LOAD-BEARING (discrimination control): S7
  with seqmove=1 still breaks exactly as the parent
  measured (mm>0 AND d!=0), AND S9 with seqmove=1 breaks
  (mm>0). If the unrepaired variant stopped breaking,
  the S7/S9 worlds drifted and K2/K4 prove nothing.
- K6 S7-VALIDITY: S7 pair well-formed under the repair
  run: dup_valid(rk0 tro)==1, eseq==1, no trace overflow
  on either trace.
- K7 S9-VALIDITY: s9_valid(rk0 tro)==1 (the duplicate
  was planted AND the promote fired for key 1051),
  eseq==1, no trace overflow on either trace. If
  invalid, S9 is VOID as a promote probe.
- K8 DETERMINISM: 3/3 runs byte-identical (external
  sha256).

## Amendment A1 (2026-10-03; committed separately after the
frozen spec, BEFORE the kh implementation below is run)

The scan-version implementation (et==3 lowest-slot scan,
per frozen section 3) was built and run once. Result:
K3 FAILED (V1 d=11, V6 d=9, S5 d=31; mm_et=3,
mm_first=90 on all three) while K1, K2, K4, K5, K6, K7
passed. K3's failure is informative and the frozen bars
are not weakened; the repair spec is corrected
transparently as follows.

Root cause, trace-verified: the substrate's promote_slot,
on the pool-full path, exiles a pool victim to cold
BEFORE freeing the promoted cold slot. When the cold
tier is full, exile_victim does min-exile-seq eviction,
which can select the very slot being promoted (it holds
the oldest exile-seq). The substrate then unconditionally
frees that slot (put32(M,co+12,0)), DESTROYING the
just-installed victim entry. Trace signature: etype-2
(victim, cs) immediately followed by etype-3 (key, cs)
with the same slot cs (V1: i=89 et=2 key=3998 slot=2,
i=90 et=3 key=1021 slot=2).

The parent Sim B's ks map is stale across this
overwrite (ks[old] is not cleared on overflow install)
and therefore still points at cs at the etype-3; freeing
sk[cs] exactly mirrors the substrate's clobber. The
frozen et==3 lowest-slot scan finds no entry (it was
overwritten) and frees nothing, diverging from the
substrate. So the frozen section-4 claim ("on
non-duplicate worlds the lowest-slot scan provably
equals ks[key]") is WITHDRAWN for the promote path:
the clobber case is a non-duplicate world where
scan != ks and ks is the correct predictor.

Corrected et==3 repair spec (replaces frozen section 3):
maintain a key->hit-slot map `kh` (16384 bytes, init
-1) in sim_prosp. On et==1, after the hit and any
periodic swap, record kh[key] = post-move slot (0 if
swapped, else the scanned hit slot). On et==3,
ps = kh[key] (then clear kh[key], as with ks).
Rationale: the substrate promotes/frees the entry it
HIT (post-move slot); the hit slot is the correct
identity across the intervening victim-exile, in all
three cases: normal (kh == ks), clobber (kh == ks ==
hit slot; the stale ks is load-bearing), and
duplicate-key (S9: kh[1051] = 8, the hit slot, while
ks[1051] = 53 is wrong). Between a key's hit and its
promote the trace contains at most the victim-exile
etype-2 (substrate cold_lookup is atomic across
hit/rank-move/promote), so no cross-key swap can
invalidate kh. The et==1 lowest-slot scan (frozen
section 2) is UNCHANGED: it is correct on hits
(S9-r2 white-box: scan=8=trace, ks=53).

The kill bars K1-K8 are UNCHANGED by this amendment.

## Verdict rule

VERDICT=PASS iff K1..K8 all PASS. A PASS verdict means
the duplicate-key repair restores exactness on S7
(mm=0, d=0), holds on the duplicate-promote probe S9,
causes zero regression on all 14 non-duplicate worlds,
and the bars discriminated (the unrepaired variant still
breaks both probes). It does NOT rule on whether
duplicate cold residency is intended substrate semantics;
that investigation is reported separately and needs the
research director's ruling. Any other combination is
VERDICT=FAIL (n/8). The bars above are frozen; no
weakening, no post-result changes.
