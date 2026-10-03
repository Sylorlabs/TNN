# PREREG: RANK-SEALED-ADVERSARIAL (sealed post-freeze adversarial worlds for Sim B)

Date: 2026-10-03. Worker: RANK-SEALED-ADVERSARIAL (non-ledger
task; claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_sealed_adversarial/.
Frozen: this file is committed alone before any implementation.
No errata; no post-result bar changes.

## Background

RANK-OVERFLOW-FIX (VERDICT=PASS 8/8) closed the overflow-world
magnitude gap: the fixed Sim B (entry-attached exile-seq model,
seqmove=1) predicts scan cost exactly (simcc==ccT4,
simpay==rkT4, integer-exact) on all 7 worlds (M2C2, V1-V6; 4
with overflow), with 0 slot mismatches against the rk4 traces.
Its own report lists the honest gap: the fixed Sim B "is exact
on 7 worlds (4 with overflow) but hasn't faced sealed
post-freeze adversarial worlds -- that remains the generality
test for the predictor." This lane is that test.

## Adversary hat (sealing statement)

This worker designs the sealed worlds BEFORE any
implementation or run in this lane. The adversary's inputs:
(1) the parameter coordinates of the 7 tested worlds:
M2C2(1,21,10), V1(1,40,10), V2(2,21,10), V3(3,21,10),
V4(0,21,10), V5(1,30,10), V6(3,40,10) as (mode,w,c2w);
(2) white-box mechanism analysis of the substrate and Sim B
sources (read, not run, before the freeze). The adversary
observes NO Sim B outputs on any sealed world. The worlds are
NOT tuned to Sim B's strengths: S1-S6 push churn rate and
overflow depth past every tested coordinate, S8 probes the
trace-capacity boundary, and S7 is explicitly designed to
BREAK Sim B (a predicted failure, barred as K4). If S7 comes
back exact, the adversary's mechanism model is wrong and the
verdict is FAIL.

## Frozen hypotheses

- H-robust: the fixed Sim B remains exactly predictive
  (d=0, mm=0) on sealed regime worlds S1-S6. Rationale: they
  exercise the same mechanisms (min-seq overflow, periodic
  swap, miss accounting) more intensely, not new mechanisms.
- H-break: Sim B BREAKS on S7 (mm>0 and d!=0). Rationale:
  Sim B's key->slot map (`ks`) keeps only the LATEST install
  slot per key, while the substrate's cold_lookup hits the
  LOWEST slot holding the key. S7 plants two cold-resident
  entries for one key (second install without intervening
  promote, which would have freed the first slot) and then
  cold-reads it. Substrate charges lowest-slot+1; Sim B
  charges latest-slot+1. Predicted: first-duplicate-hit
  mismatch, mm>=1, d!=0.
- H-boundary: S8 (w=360) overflows the frozen 1536-record
  trace; the predictor must abort cleanly (sentinel state, no
  emitted prediction), mapping the harness boundary of the
  deployed predictor.

## Frozen sealed-world definitions

Regime probes (standard run_promo script, pol=6):
- S1: mode=0, w=64, c2w=10. Single-owner heavy churn; cold
  installs stay under 64 (sub-overflow control at high w).
- S2: mode=1, w=64, c2w=10. Two-key heavy overflow (1.6x the
  max tested w).
- S3: mode=2, w=64, c2w=10. Three-key extra-heavy overflow.
- S4: mode=3, w=64, c2w=10. X2 heavy overflow.
- S5: mode=1, w=40, c2w=40. Deep second-phase overflow after
  recovery (c2w 4x the tested max).
- S6: mode=2, w=32, c2w=48. Extra-churner deep second phase.

Access-pattern probe (custom frozen script run_dupkey; new
driver code only, substrate untouched):
- S7 DUPKEY:
  1. mem_zero(M); M[16]=32; M[20]=6; M[32]=16.
  2. teach_A(M,1,TR,tro); teach_B(M,2,TR,tro).
     (20 B-keys end primary (K,777000+i*10+hop,16),
     pool (K,Aval,owner15).)
  3. j=0..33: mem_write(M,3999,900001+j,16,TR,tro).
     (34 churn writes; pool min-stamp exiles the 20 A-keys
     to cold, first cold entries, then churn-key exiles.)
  4. tr_rec(TR,tro,4,0,1,0).
  5. mem_write(M,1051,888051,16,TR,tro).
     (conflict reinstalls (1051,777051,16) to the pool.)
  6. tr_rec(TR,tro,4,0,2,0).
  7. j=34..66: mem_write(M,3999,900001+j,16,TR,tro).
     (33 churn writes; pool min-stamp eventually exiles
     (1051,777051,16) to cold: the SECOND cold entry for
     key 1051. Total cold installs 55 < 64: no min-seq
     eviction removes the first entry.)
  8. tr_rec(TR,tro,4,0,3,0).
  9. i=1..10, hop=1..2:
     mem_read_recov(M,1000+i*10+hop,1,0,rk,TR,tro).
     (20 cold reads, owner=1, pm=0: 19 single-entry exact
     hits plus key 1051's duplicate hit. Substrate hits the
     lowest slot holding 1051; Sim B charges the latest
     install slot.)
  R row records ro+92=cold_cost total, ro+128=rank_cost
  total; other fields zero.
  Predicted: mm>=1 at the 1051 hit, d!=0 (substrate
  charges lowest-slot+1, sim charges latest-slot+1).

Boundary probe (standard script):
- S8: mode=1, w=360, c2w=10. Trace-capacity probe; expected
  to exceed the frozen 1536-record trace on one or both
  traces.

Rows (ro=r*144, tro=r*24592; rows 0-18 identical to the
parent lane): S1 rk0/rk4 = rows 19/20; S2 = 21/22; S3 =
23/24; S4 = 25/26; S5 = 27/28; S6 = 29/30; S7 = 31/32
(run_dupkey); S8 = 33/34.

## Frozen design (additive; no substrate change)

1. Copy rank_overflow_fix.zag to rank_sealed_adversarial.zag;
   LANE=RANK-SEALED-ADVERSARIAL. All substrate functions
   (through run_promo) byte-unchanged.
2. Add run_dupkey (the frozen S7 script above; the single key-1051
   rewrite is one inlined mem_write call).
3. main(): rows 0-18 identical calls (substrate anchor plus
   the 7-world regression suite, kept as a control);
   rows 19-34 as defined above.
4. Sealed prospective suite after row 34: prosp1 both
   seqmove variants for S1-S7; seqmove=1 only for S8.
   RES2: 15 rows x 32 bytes.
5. Buffers: R 5040 bytes (35 rows x 144); TR 860720 bytes
   (35 x 24592); OB 65536 bytes.
6. Kill-bar evaluation in main; per-world SUM lines for
   S1-S8 (meas, predB old/new, d old/new, mm old/new,
   nmiss); K-bar lines; verdict line.

## Frozen kill bars

- K1 SUBSTRATE-ANCHOR: row 0 bit-for-bit equals the frozen
  RANK-LAZY row-0 values (same 35 field checks as the parent
  K1). The substrate copy is untouched; any deviation fails.
- K2a SEALED-EXACT-REGIME: with seqmove=1, prospective Sim B
  on S1..S6: simcc==ccT4 EXACTLY and simpay==rkT4 EXACTLY on
  each (d=0 as integers).
- K2b OVERFLOW-EXERCISED (discrimination control): at least
  4 of S1..S6 have measured cdrop>0, and on EACH such world
  the legacy model (seqmove=0) gives mm>0. Rationale: a
  sealed world on which the legacy model is also exact did
  not exercise the fixed overflow path and tests nothing;
  the battery must contain real overflow probes.
- K3 SEALED-LAYOUT-CLEAN: with seqmove=1, tro4 slot
  mismatches == 0 on S1..S6.
- K4 DUPKEY-BREAK (INVERTED adversarial bar): S7 with
  seqmove=1: mm>0 AND d!=0. PASSES iff Sim B breaks as the
  adversary predicts. If S7 is exact (mm==0, d==0), the
  predicted generality boundary is absent: the adversary's
  mechanism model was wrong.
- K5 DUPKEY-VALIDITY: the S7 rk0/rk4 pair: eseq==1, no trace
  overflow on either trace, and the rk0 trace contains at
  least one key with >=2 etype-2 records AND >=1 etype-1
  record. If invalid, S7 is VOID as a break probe (the
  duplicate was never constructed).
- K6 TRACE-PRECONDITIONS: eseq==1 and no trace overflow on
  all S1..S7 rk0/rk4 pairs (14 traces).
- K7 BOUNDARY-GRACEFUL (S8): let ovf = rk0-ovf OR rk4-ovf.
  If ovf==1: PASS iff the S8 prosp run aborted cleanly
  (mm==-1 sentinel and status==0: no prediction emitted).
  If ovf==0: PASS iff d==0 and mm==0 (exactness). Either
  branch documents the boundary honestly.
- K8 DETERMINISM: 3/3 runs byte-identical (external sha256).

## Verdict rule

VERDICT=PASS iff K1..K8 all PASS. A PASS verdict means the
sealed battery executed as designed and mapped Sim B's
generality boundary: exact on the sealed regime worlds
S1-S6, broken at the duplicate-key boundary S7 exactly as
the adversary predicted, S8 handled per K7. It does NOT
mean Sim B is general. Any other combination is
VERDICT=FAIL (n/8): K2a/K3 failing names a regime residual
(the new open thread, with magnitude); K4 failing means the
predicted boundary is absent (adversary model wrong);
K5 failing means the break probe was void. The bars above
are frozen; no weakening, no post-result changes.
