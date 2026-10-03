# PREREG: RANK-OWNER-DUPKEY (owner-mismatched duplicate probe)

Frozen: 2026-10-03. Worker: RANK-OWNER-DUPKEY (non-ledger task).
Lane: docs/lab/research-lead/overnight-20260928/rank_owner_dupkey/

## Question

RANK-DUPKEY-FIX closed with VERDICT=PASS (8/8) and one residual
boundary: "Owner-mismatched duplicates (substrate skips a
non-owner-matching lower slot; the sim's scan would pick it) --
unprobed." This lane probes it: construct a world with
owner-mismatched duplicate cold keys and determine whether the
repaired Sim B (seqmove=2, owner-blind lowest-slot scan) diverges
from the substrate. If it diverges, characterize the fix
(owner-aware scan) and the exact information the trace protocol
lacks to implement it. If it does not diverge, explain why the
case cannot arise.

## Background (from parent REPORT.md)

- Substrate `cold_lookup`: scans cold slots 0..63; hits the first
  slot with used==1, key match, AND (slot_owner & read_owner)!=0.
  A lower slot holding the key with a non-intersecting owner is
  SKIPPED.
- Sim B seqmove=2 (hit half): scans the sim's slot->key layout
  for the LOWEST slot holding the key, with NO owner check.
- The trace protocol records (etype,key,slot,aux): aux=0 for
  etype-1, aux=exile-seq for etype-2. Slot owners and read owners
  are NOT in the trace.

## Sealed worlds (frozen scripts)

S10 (owner-mismatched duplicate probe) and S10b (owner-compatible
control) share one lean plant (no teach phases), built by the new
driver `run_owner_dupkey(M,OB,R,ro,rk,TR,tro,tag,rown)`:

1. mem_zero; pool_size=32; policy=6; consent_mask=16.
2. tr_rec(et=4, phase 1).
3. mem_write(1051,507,15) -> primary install (1051,507,15).
4. mem_write(1051,777051,16) -> conflict; relocate parks
   (1051,507,15) in pool slot 0; primary := (1051,777051,16).
5. tr_rec(et=4, phase 2).
6. 33x mem_write(3999,900001+j,16), j=0..32: j=0 allocates
   primary 3999; j=1..31 fill pool free slots; j=32 evicts
   min-touch pool slot 0 -> (1051,507,15) exiled to cold slot 0
   (etype-2 record).
7. mem_write(1051,999051,1) -> conflict; relocate evicts
   min-touch pool slot 1 (a 3999 entry) to cold slot 1;
   pool[1] := (1051,777051,16); primary := (1051,999051,1).
   (Primary 1051 now has owner 1: invisible to read owner 16.)
8. tr_rec(et=4, phase 3).
9. 32x mem_write(3999,900001+j,16), j=33..64: evicts the 31
   remaining churn pool entries, then pool[1] (1051,777051,16)
   -> cold slot 33 (etype-2 record). Cold holds 34 entries;
   NO overflow (64 slots).
10. Probe: rv = mem_read_recov(1051, rown, pm=0, rk).
    - S10: rown=16. Substrate cold_lookup SKIPS slot 0
      ((15&16)==0), HITS slot 33 ((16&16)!=0); etype-1 (1051,33);
      rv=777051; ccT charges 34.
    - S10b: rown=2. Substrate HITS slot 0 ((15&2)!=0);
      etype-1 (1051,0); rv=507; ccT charges 1.
11. White-box (driver-side, post-probe): scan cold for key 1051
    -> exactly 2 slots (slow < shigh) with owners olow, ohigh;
    e1slot = the trace's etype-1 slot (probe is the last record);
    oas = owner-aware formula result = lowest slot with key
    match AND (slot_owner & rown)!=0.
    R row: ro+92=ccT, ro+128=rankcost, ro+132=layout_ok,
    ro+136=oa_ok, ro+140=e1slot.
    layout_ok = 1 iff exactly-2 1051 cold entries, slow<shigh,
    olow==15, ohigh==16, (olow&ohigh)==0, rv==expv
    (expv=777051 for rown=16, 507 for rown=2).
    oa_ok = 1 iff oas == e1slot (owner-aware formula reproduces
    the substrate's hit slot).

Rows (R = 41*144 = 5904 bytes; TR = 41*24592 = 1008272 bytes):
- Rows 0-36: byte-identical to RANK-DUPKEY-FIX (substrate anchor
  + sealed S1-S9).
- Row 37: S10-RK0  (rk=0, rown=16), ro=5328,  tro=909904.
- Row 38: S10-RK4  (rk=4, rown=16), ro=5472,  tro=934496.
- Row 39: S10B-RK0 (rk=0, rown=2),  ro=5616,  tro=959088.
- Row 40: S10B-RK4 (rk=4, rown=2),  ro=5760,  tro=983680.

Prospective suites:
- RES3 (17 rows x 32, parent-identical): regression control for K3.
- RES4 (4 rows x 32 = 128 bytes), new:
  row 0 S10-r2  (seqmove=2 on S10 rk0/rk4 traces),
  row 1 S10-r1  (seqmove=1 contrast, reported not barred),
  row 2 S10B-r2 (seqmove=2 on S10b traces),
  row 3 S10B-r1 (seqmove=1 contrast, reported not barred).
- meas10  = (ccT[38]-ccT[37]) + rankcost[38].
- meas10b = (ccT[40]-ccT[39]) + rankcost[40].

Expected (predictions, NOT bars): S10-r2: mm=1, mm_first=37
(index of the etype-1 record), d=-33, simcc=1, ccT=34.
S10b-r2: mm=0, d=0. S10-r1: mm=0, d=0 (latest-install heuristic
accidentally matches; reported as contrast).

## Frozen kill bars

- K1 SUBSTRATE-ANCHOR: row 0's 35 field checks, identical to the
  parent K1. PASS iff all hold (substrate byte-unchanged).
- K2 OWNER-DUPKEY-DIVERGENCE: S10 x seqmove=2 (RES4 row 0):
  mm>=1 AND mm_first == (nrec(S10-rk0)-1) [the mismatch is on
  the hit record] AND d != 0, where d = predB - meas10.
  (The repaired Sim B diverges on owner-mismatched duplicates.)
- K3 NO-REGRESSION: RES3 rows 0-12 and 14 (14 non-duplicate
  worlds) + row 13 (S7-r2) + row 16 (S9-r2): each mm==0 AND
  d==0. (The probe disturbs no existing pass.)
- K4 PROBE-VALIDITY: rows 37-40: layout_ok==1 on all four;
  s10_valid==1 on both rk0 traces (key 1051: >=2 etype-2,
  >=1 etype-1); eseq==1 for both pairs (RES4 rows 0,2);
  overflow flag 0 on all four traces; e1slot(S10-rk0) !=
  e1slot(S10b-rk0) (the read owner changes the hit slot);
  rv matches expv per read owner (folded into layout_ok).
- K5 CONTROL-PASS: S10b x seqmove=2 (RES4 row 2): mm==0 AND
  d==0. (With an owner-compatible read the scan is correct;
  the divergence is owner-mismatch-specific, not plant drift.)
- K6 FIX-FORMULA: oa_ok==1 on rows 37 and 39. (The driver-side
  owner-aware scan -- lowest slot with key match and owner
  intersect -- reproduces the substrate's etype-1 hit slot on
  both reads. This validates the fix LOGIC; the trace protocol
  carries no owners, so a Sim B implementation needs either a
  protocol extension or the substrate ruling (a)/(b) from the
  parent report.)
- K7 DETERMINISM (external): 3/3 byte-identical runs (sha256).

VERDICT=PASS iff K1-K6 pass in-binary and K7 passes externally.

## Discrimination (why these bars bite)

- K2 fails if Sim B does NOT diverge (residual absent -> the
  honest answer is "no divergence", verdict FAIL).
- K5 fails if the owner-compatible control also breaks (plant
  drift would then explain K2, not the owner skip).
- K4 fails if the plant is wrong (no owner-mismatched
  duplicates, overflow, eseq break, wrong hit pattern).
- K6 fails if the owner-aware formula does not reproduce the
  substrate (fix characterization wrong).
- K3 fails on any regression; K1 fails on substrate drift.

## Governance

- Prereg committed alone before implementation (this file +
  NAMECHECK.md). No amendments expected; any spec correction
  goes through a committed amendment before the corrected
  implementation runs.
- Pure Zag; safebin mandatory; 3/3 byte-identical.
- Additive on RANK-DUPKEY-FIX: substrate functions
  byte-unchanged; rows 0-36 identical; new driver + 4 rows +
  RES4 + K1-K6. No trace-protocol or substrate redesign in this
  lane (the fix's data requirements are reported, not built).
- Commits local, never pushed, explicit pathspecs, no reset.
  Git writes via /usr/bin/git (safebin git symlink EPERM
  workaround, per AGENTS.md).
