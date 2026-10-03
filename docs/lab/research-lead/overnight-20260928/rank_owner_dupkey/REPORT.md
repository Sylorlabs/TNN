# REPORT: RANK-OWNER-DUPKEY (owner-mismatched duplicate probe)

Date: 2026-10-03. Worker: RANK-OWNER-DUPKEY (non-ledger task;
claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_owner_dupkey/.

## Verdict

**PASS (7/7)** under the frozen prereg (committed alone before
implementation; no amendments; kill bars K1-K7 unchanged).

## Question

RANK-DUPKEY-FIX closed with VERDICT=PASS (8/8) and one residual
boundary: "Owner-mismatched duplicates (substrate skips a
non-owner-matching lower slot; the sim's scan would pick it) --
unprobed." This lane probed it.

## Answer

**Yes, Sim B diverges.** The repaired Sim B (seqmove=2,
owner-blind lowest-slot scan) breaks on owner-mismatched
duplicate keys: S10 gives mm=1 (mm_et=1, mm_first=37, the hit
record), d=-33 (simcc=1 vs ccT=34). The residual boundary is
real and is now closed as a confirmed divergence with a
characterized fix.

## What was done

Additive on RANK-DUPKEY-FIX's rank_dupkey_fix.zag; the substrate
is byte-unchanged (K1 anchor passes; all 33 parent SUM/K1 lines
reproduce the parent's run1.txt exactly). Added:

- `run_owner_dupkey` driver: a lean frozen plant (no teach
  phases) producing cold slot 0 = (1051,507,owner 15) and cold
  slot 33 = (1051,777051,owner 16), primary (1051,999051,1),
  pool = 32x (3999,16), 34 cold entries, no overflow.
  - S10 (rows 37-38): probe read of 1051 with owner=16. The
    substrate's `cold_lookup` SKIPS slot 0 ((15&16)==0) and hits
    slot 33 -> etype-1 (1051,33), rv=777051, ccT=34.
  - S10b (rows 39-40): owner-compatible control; probe read with
    owner=2 hits slot 0 ((15&2)!=0) -> etype-1 (1051,0), rv=507,
    ccT=1.
  - Driver-side white-box: layout_ok (exactly two cold 1051
    entries, owners 15/16, non-intersecting, rv matches the read
    owner) and oa_ok (the owner-aware scan formula reproduces
    the substrate's hit slot), recorded in the R row.
- `s10_valid`: trace-shape check (>=2 etype-2, >=1 etype-1 for
  1051).
- RES4 prospective suite (4 rows): S10 x seqmove=2, S10 x
  seqmove=1, S10b x seqmove=2, S10b x seqmove=1.
- Frozen K1-K6 evaluation in main (K7 determinism external).

## Measured results

| world | meas | predB | d | mm | mm_first | note |
|-------|------|-------|---|----|----------|------|
| S10-r2 | 0 | -33 | -33 | 1 | 37 | scan picks 0, substrate hits 33 |
| S10-r1 | 0 | 0 | 0 | 0 | -1 | latest-install accidentally right |
| S10B-r2 | 0 | 0 | 0 | 0 | -1 | control passes |
| S10B-r1 | 0 | 33 | 33 | 1 | 37 | latest-install breaks (mirror) |

Driver lines: S10 e1slot=33, oas=33, rv=777051, layout_ok=1,
oa_ok=1 (rk0 and rk4). S10b e1slot=0, oas=0, rv=507,
layout_ok=1, oa_ok=1 (rk0 and rk4).

K1 SUBSTRATE-ANCHOR -> PASS. K2 OWNER-DUPKEY-DIVERGENCE ->
PASS (mm=1, mm_first=37, d=-33). K3 NO-REGRESSION -> PASS
(14 worlds + S7 + S9 x seqmove=2: all d=0, mm=0). K4
PROBE-VALIDITY -> PASS (e1slot10=33 != e1slot10b=0; eseq=1
both pairs; no overflow). K5 CONTROL-PASS -> PASS (mm=0,
d=0). K6 FIX-FORMULA -> PASS (oa_ok=1 on both reads). K7
DETERMINISM -> 3/3 byte-identical (sha256
ac4bd097d461c991dcb8b4e2a74b7f068b2e6e751e23203134a41ab2e0853fe2).

## The symmetric finding (not preregistered, reported)

Neither owner-blind heuristic is general; they fail as mirror
images:
- S10 (owner-mismatched read): lowest-slot scan (r2) breaks
  (mm=1, d=-33); latest-install (r1) accidentally passes.
- S10b (owner-compatible read): latest-install (r1) breaks
  (mm=1, d=+33); lowest-slot scan (r2) passes.
Only the owner-aware scan (lowest slot with key match AND
owner intersect, K6) is correct on both. This was not a kill
bar (the prereg barred only r2), but it sharpens the fix
characterization: the defect is exactly the missing owner
conjunct in the hit-slot prediction, on both the scan and the
latest-install variants.

## The fix, characterized (for the research director)

The correct hit-slot rule is the substrate's own:
lowest s with used(s) && key(s)==K && (owner(s)&owner_read)!=0.
Sim B seqmove=2 implements this minus the owner conjunct.

Implementing it in Sim B requires two pieces of data the
current trace protocol does NOT carry:
1. Per-slot owners at install time (etype-2 aux is the
   exile-seq, needed for eviction prediction; no room).
2. The read owner at hit time (etype-1 aux is 0, unused --
   this one could be carried without disturbing the layout).
Hence an owner-aware Sim B needs either (i) a trace-protocol
extension (new record/field carrying installed owners; the
read owner fits in the unused etype-1 aux), or (ii) the
substrate ruling already pending from RANK-DUPKEY-FIX:
(a) declare key-unique cold residency an invariant and add a
key-existence check to `exile_victim` (owner-mismatched
duplicates then cannot form; current Sim B stands as-is), or
(b) declare the cold tier a slot-addressed exile log where
duplicates are legal and lowest-owner-matching-slot-wins is
the defined semantic (then fix (i) is required for an exact
predictor). K6 proves the fix LOGIC is exactly right; the
data path is the remaining work. The substrate was NOT
changed in this lane either way (K1 anchor).

Note the stale-value contrast with S7: in S7 the lowest slot
shadowed a newer value for a compatible owner; in S10 the
owner skip means the read returns the NEWER value (777051),
so owner-mismatched duplicates do not cause stale reads --
they cause slot/cost misprediction in an owner-blind
predictor.

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `command -v python3` / `command -v python` verified empty
  before the prereg commit; znc byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (ZNC-CMP-IDENTICAL). No python invoked; no PROCESS-FAIL.
- New code: no `// znc:allow` (all return values used), no
  `while.*!(` negated conjunctions, no _zag_print, no
  `as *i32` slice construction, if-nesting at most 2, no new
  `as *u8` (the one approved z_alloc cast carried over).
- Prereg committed alone first; no amendments; implementation
  and artifacts committed after the verdict.
- Commits local only, never pushed, explicit pathspecs, no
  reset. Git writes via /usr/bin/git (safebin git symlink
  EPERM workaround, per AGENTS.md).

## Artifacts

- `rank_owner_dupkey.zag`: implementation (pure Zag).
- `rank_owner_dupkey_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  (sha256 `ac4bd097d461c991dcb8b4e2a74b7f068b2e6e751e23203134a41ab2e0853fe2`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty;
  `err_build.txt`: benign zagd warning only.
- `PREREG.md` (frozen 2026-10-03, committed alone),
  `NAMECHECK.md`, `REPORT.md`.
