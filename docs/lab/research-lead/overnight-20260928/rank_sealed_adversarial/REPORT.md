# REPORT: RANK-SEALED-ADVERSARIAL (sealed post-freeze adversarial worlds for Sim B)

Date: 2026-10-03. Worker: RANK-SEALED-ADVERSARIAL (non-ledger
task; claim minting paused). Lane:
docs/lab/research-lead/overnight-20260928/rank_sealed_adversarial/.

## Verdict

**FAIL (7/8)** under the frozen prereg. The failed bar is K2b
(OVERFLOW-EXERCISED), a battery control bar, not a Sim B
exactness bar. Every bar governing Sim B itself passed:
K2a (exact on all 6 sealed regime worlds), K3 (0 layout
mismatches), K4 (S7 breaks exactly as the adversary
predicted), K5 (S7 valid), K6, K7, K1, K8 (3/3 byte-identical,
sha256 `c60c55579a6ed6f2afd7a1010b902ec9e32fd0d7d806b821200c61f88b74ac23`).

Plain reading: Sim B did not fail. The battery's own control
assumption failed, and the failure is informative (see
"K2b analysis"). Per governance the bars are not amended
post-result; the verdict stands as FAIL and the corrected
battery is a follow-up re-freeze, not a reinterpretation.

## What was done

Additive on RANK-OVERFLOW-FIX's rank_overflow_fix.zag; the
substrate is byte-unchanged (K1 anchor passes; all 7 parent
SUM lines reproduce the parent's run1.txt exactly, including
the frozen legacy gaps d5o=-22, d6o=-18 and the fixed-model
exactness). Added:

- Sealed rows 19-34 (frozen in PREREG.md before any run):
  S1(0,64,10), S2(1,64,10), S3(2,64,10), S4(3,64,10),
  S5(1,40,40), S6(2,32,48), S7 DUPKEY (custom run_dupkey
  script), S8(1,360,10), each rk0/rk4. Rows 0-18 kept
  identical as anchor + regression control.
- run_dupkey: the frozen S7 access-pattern probe. Plants two
  cold-resident entries for key 1051 (second install with no
  intervening promote, which would have freed the first
  slot), then 20 cold reads (owner=1, pm=0).
- Sealed prospective suite: S1-S7 x 2 seqmove variants, S8
  new only; per-world SUM lines; frozen K1-K8 evaluation.
- Buffers: R 5040, TR 860720, OB 65536 (35 rows).

## Measured table (sealed worlds, Sim B seqmove=1)

| world | regime | meas | predB_new | d_new | mm_new | nmiss | cdrop |
|-------|--------|------|-----------|-------|--------|-------|-------|
| S1 | mode0 w64 sub-overflow | 9 | 9 | 0 | 0 | 0 | 7 |
| S2 | mode1 w64 heavy overflow | 0 | 0 | 0 | 0 | 200 | 70 |
| S3 | mode2 w64 extra-heavy | 0 | 0 | 0 | 0 | 200 | 133 |
| S4 | mode3 w64 X2 heavy | 0 | 0 | 0 | 0 | 200 | 69 |
| S5 | mode1 w40 + c2w40 deep 2nd phase | 2 | 2 | 0 | 0 | 29 | 83 |
| S6 | mode2 w32 + c2w48 deep 2nd phase | 0 | 0 | 0 | 0 | 187 | 113 |
| S7 | DUPKEY (adversarial break) | 2 | 47 | 45 | 1 | 0 | 0 |
| S8 | mode1 w360 capacity probe | 0 | 0 | 0 | 0 | 200 | 319 |

Legacy (seqmove=0) for contrast: S1 d_old=-38 mm=28;
S5 d_old=-62 mm=124; S2/S3/S4/S6 mm=0 (see K2b analysis);
S7 d_old=45 mm=1 (breaks identically: one hit, no swaps
before the break point... nswaps=2 in replay, both after).

## K2b analysis (the failed bar; the informative negative)

Frozen K2b required: >=4 of S1..S6 overflow (cdrop>0), and
the legacy model diverges (mm>0) on EACH such world.
Observed: 6/6 overflow, but legacy mm>0 only on S1 and S5.
K2b FAIL.

Root cause, verified in the traces: S2/S3/S4/S6 are
miss-dominated overflow worlds. At w=64 the cold tier
overflows several times over (cdrop 69-133); the early-exiled
A-keys are min-seq EVICTED before the R rounds, so the
recovery reads almost all MISS (187-200 misses x 64 points =
simcc 12800, exact in both models). With (near-)zero cold
hits, the periodic swap never fires (nswaps=0 on S2/S4/S8),
so the legacy model's per-slot seq array never desyncs from
the entries: installs set it correctly, and nothing moves it.
The slot-attached seq defect is unreachable without swaps.

Mechanism refinement (information gained): the
RANK-OVERFLOW-FIX defect requires the swap x overflow
INTERACTION. Overflow alone does not desync the legacy
model. The frozen K2b coupled "overflow" with "legacy
divergence"; the coupling is false for miss-dominated
regimes. S1 (cdrop=7, 6 swaps, mm_old=28) and S5
(cdrop=83, 8 swaps, mm_old=124) are the genuine probes of
the fixed mechanism in this battery, and the fixed model is
exact on both with 0 mismatches. The bar did its job: it
caught a calibration error in the battery design, not a
predictor defect.

## S7: the predicted break (generality boundary found)

K4 PASS (inverted bar): Sim B breaks exactly as the
adversary predicted. S7-new: mm=1, mm_first=66, mm_et=1,
d=45, eseq=1, dup_valid=1.

White-box confirmation: trace index 66 is the 9th of the 20
planted reads (indices 58-77), i.e. key 1051 (read order
1011,1012,1021,1022,1031,1032,1041,1042,1051). Key 1051 has
two cold-resident entries: slot 8 (507,owner15, first exile)
and slot 53 (777051,owner16, second exile). The substrate's
cold_lookup hits the LOWEST slot (8, charges 9); Sim B's
key->slot map keeps only the LATEST install slot (53,
charges 54). The full S7 divergence is that single hit:
45 = 54-9; simpay=2 matches rkT4=2 (swap COUNT is
nhit-schedule-determined, unaffected). K5 confirms the probe
was valid (no vacuous break).

Generality boundary, stated crisply: **Sim B's key->slot map
assumes at most one cold-resident entry per key. A key
exiled twice without an intervening promote (promote frees
the slot, so the standard script can never produce this)
breaks the slot prediction, the scan-cost prediction, and
cascades into layout divergence.** The substrate permits
duplicate cold residency (exile_victim never checks for an
existing key entry); whether that is intended substrate
semantics is a separate question for the research director.

## S8: boundary probe that did not reach the boundary

K7 PASS via the no-overflow branch (ovf8=0): w=360 produced
only 930/1536 trace records; Sim B exact (d=0, mm=0) on a
200-miss heavy world. The trace-capacity boundary (clean
abort vs silent prediction) remains UNPROBED; reaching it
needs roughly w>=600. Noted as follow-up, not claimed.

## Findings beyond the bars

1. Sim B is exact on 6/6 sealed regime worlds spanning
   sub-overflow heavy churn (S1), extreme overflow
   (S2/S3/S4, cdrop up to 133), deep double-phase overflow
   after recovery (S5/S6), and a 930-record 200-miss world
   (S8). Combined with the parent 7, that is 13/13
   non-adversarial worlds exact, 4 of them sealed.
2. The legacy model's sealed gaps (-38 on S1, -62 on S5)
   confirm the sealed regime worlds are non-trivial where
   swaps fire; the fix closes them to zero.
3. The S7 break is the first observed Sim B inexactness that
   is NOT explained by the seq-attachment defect: it is a
   second, independent modeling assumption (unique cold
   residency per key). Fixing it is a predictor change that
   needs its own prereg (e.g. slot-list or lowest-slot hit
   semantics in the sim).
4. Miss accounting (64 points) holds exactly at 200-miss
   scale (S2/S3/S4/S8: simcc=12800).

## What this does NOT test (honest accounting)

- The corrected K2b battery (re-freeze with swap-active
  heavy worlds and a recalibrated control threshold).
- The actual trace-capacity boundary (S8 did not overflow).
- A duplicate-key fix for Sim B (S7 maps the boundary; the
  repair is future work under a fresh prereg).
- rk not in {0,4}, other policies, pm values (out of scope
  for Sim B, the rk=4 predictor, by design).

## Toolchain and hygiene

- Safebin mandatory: PATH=$HOME/safebin for every build/run;
  `command -v python3` / `command -v python` verified empty
  before the prereg commit; znc byte-identical to
  src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (ZNC-CMP-IDENTICAL). No python invoked; no PROCESS-FAIL.
- One `// znc:allow A0102` (discarded mem_read_recov return
  in run_dupkey; events unaffected). Otherwise no analyzer
  warnings; only the benign zagd-unavailable build note.
- grep audit: no `while.*!(` negated conjunctions, no
  _zag_print, no `as *i32` slice construction; if-nesting at
  most 2 in new code; no new `as *u8` (the one approved
  z_alloc cast carried over).
- Commits local only, never pushed, explicit pathspecs, no
  reset. Prereg+namecheck committed alone first (c99bb4bac);
  implementation and artifacts committed after the verdict.
  No errata on the bars.

## Artifacts

- `rank_sealed_adversarial.zag`: implementation (pure Zag).
- `rank_sealed_adversarial_bin`: built binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical
  (sha256 `c60c55579a6ed6f2afd7a1010b902ec9e32fd0d7d806b821200c61f88b74ac23`).
- `err1.txt`, `err2.txt`, `err3.txt`: empty; `err_build.txt`:
  benign zagd warning only.
- `PREREG.md` (frozen 2026-10-03, committed alone as
  c99bb4bac), `NAMECHECK.md`, `REPORT.md`.

## Recommended follow-ups

1. Re-freeze the battery with corrected K2b: require >=2
   (not >=4) legacy-divergent worlds, and add swap-active
   heavy worlds (moderate w so A-keys survive in cold and
   hits keep firing) to probe the fix under sustained
   swap x overflow interaction.
2. Trace-boundary probe at w~=600-800 to force the
   1536-record overflow and verify the clean-abort branch
   of K7.
3. Duplicate-key repair prereg: give Sim B lowest-slot hit
   semantics (or a per-key slot list) and re-run S7 sealed;
   separately, rule on whether duplicate cold residency is
   intended substrate semantics (exile_victim has no
   key-existence check).
