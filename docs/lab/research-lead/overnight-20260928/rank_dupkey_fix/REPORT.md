# REPORT: RANK-DUPKEY-FIX (duplicate-key repair for Sim B)

Date: 2026-10-03. Worker: RANK-DUPKEY-FIX (non-ledger task;
claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_dupkey_fix/.

## Verdict

**PASS (8/8)** under the frozen prereg (as amended by
Amendment A1, committed before the amended implementation
was run; kill bars K1-K8 unchanged).

## What was done

Additive on RANK-SEALED-ADVERSARIAL's
rank_sealed_adversarial.zag; the substrate is
byte-unchanged (K1 anchor passes; all 7 parent SUM lines
reproduce the parent's run1.txt exactly, including the
frozen legacy gaps). Added:

- seqmove=2 variant of `sim_prosp`: the fixed
  entry-attached exile-seq model (identical to seqmove=1)
  plus the duplicate-key repair:
  (a) hit path (et==1): lowest-slot scan of the sim's
  slot->key layout, mirroring the substrate
  `cold_lookup`'s lowest-slot hit semantics;
  (b) promote path (et==3): new key->hit-slot map `kh`
  recording each hit's post-move slot (Amendment A1;
  see "The promote-clobber quirk" below).
  seqmove=0/1 preserved bit-for-bit as controls.
- `run_dupkey_pm1`: the frozen S9 DUPKEY-PROMOTE script
  (same plant as S7, then two pm=1 reads of key 1051;
  the second read fires the promotion on the hit entry).
  Rows 35/36; R 5328, TR 909904.
- `s9_valid(TR,tro)`: key 1051 has >=2 etype-2, >=1
  etype-1, >=1 etype-3 records.
- RES3 prospective suite (17 rows): 14 non-duplicate
  worlds x seqmove=2, S7 x seqmove=2, S9 x seqmove=1/2.
- Frozen K1-K8 evaluation in main; per-world SUM lines.

## Measured table (repaired Sim B, seqmove=2)

| world | meas | predB | d | mm | note |
|-------|------|-------|---|----|------|
| M2C2 | -35 | -35 | 0 | 0 | |
| V1 | -31 | -31 | 0 | 0 | legacy d_old=-22 |
| V2 | (parent) | | 0 | 0 | |
| V3 | (parent) | | 0 | 0 | |
| V4 | (parent) | | 0 | 0 | |
| V5 | -53 | -53 | 0 | 0 | legacy d_old=-22 |
| V6 | (parent) | | 0 | 0 | |
| S1-S6 | | | 0 | 0 | all six |
| S7 DUPKEY | 2 | 2 | 0 | 0 | was mm=1, d=45 |
| S8 | | | 0 | 0 | |
| S9 DUPKEY-PROMOTE | 0 | 0 | 0 | 0 | simcc=18 (2x9) |

(K3 prints d per world: 0 0 0 0 0 0 0 0 0 0 0 0 0 0.)

Discrimination control (K5): the unrepaired seqmove=1
variant still breaks both probes exactly as before:
S7: mm=1, mm_first=66, mm_et=1, d=45 (reproduces the
parent's break bit-for-bit); S9: mm=3, mm_first=58,
mm_et=1, d=90 (two 45-point hit gaps: 54 vs 9).
The repair, not drift, fixed S7/S9.

## The promote-clobber quirk (found via K3's honest failure)

The first implementation used the frozen spec's et==3
lowest-slot scan. K3 FAILED (V1 d=11, V6 d=9, S5 d=31;
mm_et=3, mm_first=90). Trace-verified root cause:

The substrate's `promote_slot`, on the pool-full path,
exiles a pool victim to cold BEFORE freeing the promoted
cold slot. When cold is full, `exile_victim` does
min-exile-seq eviction, which can select the very slot
being promoted (oldest exile-seq). The substrate then
unconditionally frees that slot (`put32(M,co+12,0)`),
DESTROYING the just-installed victim entry. Trace
signature (V1): i=89 et=2 key=3998 slot=2, i=90 et=3
key=1021 slot=2 -- the same slot.

The parent Sim B's `ks` map is stale across this
overwrite (`ks[old]` is not cleared on overflow
install), so it still points at the hit slot at the
etype-3; freeing `sk[cs]` exactly mirrors the
substrate's clobber. The scan found no entry and freed
nothing: divergence. The stale `ks` is LOAD-BEARING for
the parent's exactness on V1/V6/S5 -- not a defect.

Amendment A1 (committed before the kh run): et==3 uses
`kh[key]`, the hit entry's post-move slot recorded at
the et==1. Correct in all three cases: normal
(kh == ks), clobber (kh == ks == hit slot), duplicate
(S9: kh[1051] = 8, the hit slot; ks[1051] = 53 would be
wrong). With kh, K3 passes 14/14 and K4 still passes.

## S7: the break is fixed

S7-r2: mm=0, mm_first=-1, d=0, simcc=210 (was 255;
the 45-point gap closed), simpay=2. The lowest-slot
scan charges 9 for the key-1051 hit, matching the
substrate. K6 confirms the probe is still valid
(dup=1, eseq=1, no overflow).

## S9: the promote half is validated

S9-r2: mm=0, d=0, simcc=18. White-box: both pm=1 reads
hit cold slot 8 (lowest slot holding 1051); the second
read (rc 1->2) promotes, freeing slot 8; the pool
victim exiles to the first free cold slot (no clobber;
occ=55<64). K7 confirms the probe is valid
(s9v=1: >=2 etype-2, >=1 etype-1, >=1 etype-3 for 1051).

## Substrate semantics investigation (for the research director)

Question: is duplicate cold residency intended
substrate semantics (`exile_victim` has no
key-existence check)?

Evidence that it is TOLERATED (defined behavior):
- The cold tier is slot-addressed everywhere: rc table,
  ranked flags, swaps, and promote are all per-slot;
  the key is a payload field, not a map key.
- `cold_lookup`'s scan order defines the duplicate
  semantic: lowest slot with key+owner match wins.
- The hot tier never destroys; the cold tier is an
  exile log, and logs naturally contain duplicates.

Evidence that it is NOT deliberately DESIGNED:
- The hot tier (`mem_write`) maintains key uniqueness
  (conflict detection, owner OR-ing); the cold tier's
  asymmetry is unexplained.
- The S7 duplicate makes a cold read return a STALE
  value (slot 8: val 507, owner 15) shadowing a NEWER
  value (slot 53: val 777051, owner 16) for owner=1.
- The promote-clobber (above) silently DESTROYS a live
  entry (3998's cold entry) with no distinguishing
  counter -- hard to call intended.
- `exile_victim` could check for an existing key the
  way `mem_write` does; the absence looks like
  omission, not choice.

Recommendation (ruling needed, NOT decided here):
the duplicate is currently tolerated rather than
intended. Two candidate rulings: (a) declare
key-unique cold residency an invariant and add a
key-existence check to `exile_victim` (substrate
change; all frozen rows re-freeze; blast radius
includes the clobber quirk); (b) declare the cold
tier a slot-addressed exile log where duplicates are
legal and lowest-slot-wins is the defined semantic
(no substrate change; this lane's Sim B repair is
then the correct predictor). Technical note: (b) is
cheaper and preserves all current exactness results.
The substrate was NOT changed in this lane either
way (K1 anchor).

## What this does NOT test (honest accounting)

- Owner-mismatched duplicates: if the lowest
  key-holding slot has a non-intersecting owner, the
  substrate skips it but the sim's scan picks it.
  S7/S9 do not probe this (owners compatible).
- `sim_predict`/`pw` (dead code in main) still use
  the old ks behavior; untouched deliberately.
- Whether duplicate cold residency SHOULD exist
  (needs the director's ruling above).
- rk not in {0,4} for S9 (S9 ran rk0/rk4 only).

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every
  build/run; `command -v python3` / `command -v python`
  verified empty before the prereg commit; znc
  byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (ZNC-CMP-IDENTICAL). No python invoked; no
  PROCESS-FAIL.
- Two `// znc:allow A0102` (discarded
  mem_read_recov returns in run_dupkey_pm1; carried
  over from run_dupkey). Otherwise no analyzer
  warnings; only the benign zagd-unavailable build
  note.
- grep audit: no `while.*!(` negated conjunctions,
  no _zag_print, no `as *i32` slice construction;
  if-nesting at most 2 in new code; no new `as *u8`
  (the one approved z_alloc cast carried over).
- Prereg committed alone first (19e28b864);
  Amendment A1 committed before the kh implementation
  (2212e9f30); implementation and artifacts committed
  after the verdict. No errata on the bars; the one
  spec correction went through transparent amendment.
- Commits local only, never pushed, explicit
  pathspecs, no reset. Git writes via /usr/bin/git
  (safebin git symlink EPERM workaround, per
  AGENTS.md).

## Artifacts

- `rank_dupkey_fix.zag`: implementation (pure Zag).
- `rank_dupkey_fix_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  (sha256 `a91c529133751e4f4a673e3f0aadd24231631f1a3b90e088933d2b0b3fab3c28`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty;
  `err_build.txt`: benign zagd warning only.
- `PREREG.md` (frozen 2026-10-03, committed alone as
  19e28b864; Amendment A1 committed as 2212e9f30),
  `NAMECHECK.md`, `REPORT.md`.
