# PAR_DIVE RED-TEAM RUNLOG

2026-09-24. All times PDT. Pinned znc:
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

## 06:50–07:50 — baselines and NATIVE attacks

- Rebuilt `rt_hyb_attack.zag` (+true single-bit `sb1`/`sb1mix`), `meter.zag`
  (+sign-correct `g32s`, `postcut`, `zcr`, `peak`, `conv64`), `fault.zag`.
- NATIVE clean reruns byte-identical (rt_clean_r1/r2 = inherited rt_clean).
- A1a (gross XOR): 1292/1292 healed, 0 diffs — DEFENDED.
- A1b (bit13): 0/1292 flagged, 82,688 diffs — ATTACK_WORKS.
- A1c (DC+3277): 0/1292 flagged, 1,323,000 diffs — ATTACK_WORKS.
- A1d (zero 512/block): 2/1292 flagged, 660,266 diffs — ATTACK_WORKS.
- RT-CASCADE (true 1-bit @132300): prediff=0, postdiff=1 — DEFENDED.

## 07:48–08:00 — B determinism break

- First `seqmix` (cas_b_clean) diverged from 10 later runs: 147,014 samples,
  voice path t=2.2 s→, logs byte-identical, no crash. 1/11 silent
  divergence. No RNG/clock syscalls; nio_alloc zeroes. Mechanism unknown.

## 08:00–08:30 — parser fuzz (all targets)

- 14-plan corpus vs NATIVE/A/B/C/D1/D2: all rc=0, zero rejections.
- Fail-open everywhere: rails hit, caps silent, coercions silent.
- C's `seq+mix` wrote WAV (dispatch only honors `seqmix`); re-ran raw.

## 08:30–08:47 — RESPOND corpus

- 11 plans × 6 targets. NATIVE/C: 30 Hz trap (fm=79 → latch 110 Hz) —
  ATTACK_WORKS. B: all defended (range gate). A/D1: nominal-only (deaf).
  D2: plan-referential latch, poly abstain.
- Shipped `render_b` binary deleted from worktree ~08:40; rebuilt from
  untouched source 08:47; fresh binary produces majority (Z) state.

## 08:47–09:10 — A5/A6/A7/A8

- A5: NATIVE postdiff=0; B regions 1–9 zero diffs; C postdiff=0 (raw re-run);
  D2 postdiff=0 — all DEFENDED.
- A6: A 4/4 bit-identical; B rev/stride 0 diffs; D1/D2 WAVs bit-identical
  (after correcting a WAV-vs-raw comparison artifact) — all DEFENDED.
- A7 (t=1→t=28): NATIVE 440/220/440; B 440/220/440; C 425/217/425 Hz;
  D2 440/220/460; A/D1 nominal-only — DEFENDED except A/D1 INCONCLUSIVE.
- A8: NATIVE/D2 zero post-silence diffs — DEFENDED.

## Sustained corruption

- A: 1,322,969 diffs (no recovery by design) — ATTACK_WORKS.
- B: susfaultmix deterministic 2/2; 10 injected bits persist — ATTACK_WORKS
  (confounded by the determinism break on the clean baseline).
- C: 198,529 diffs, all blocks vetoed, output not healed — ATTACK_WORKS
  (output), DEFENDED (servo state).
- D1/D2: 82,688 diffs each, 64/block, peak→rail — ATTACK_WORKS.

## Deliverables

- `sheets/NATIVE_ATTACK_SHEET.md`, `sheets/CONTENDER_{A,B,C,D1,D2}_ATTACK_SHEET.md`
- `REDTEAM_VERDICT.md`, `RUNLOG.md` (this file)
- Sources: `src/rt_hyb_attack.zag`, `src/meter.zag`, `src/fault.zag`
- Plans: `plans/fz_*.txt`, `plans/r_*.txt`, `plans/xr_*.txt`,
  `plans/sil_*.txt`, `plans/lh_cue*.txt`
- Logs: `log/` (per-run stdout)

## Open items / caveats

- B's 1/11 divergence mechanism unidentified; needs a minimal reproducer and
  binary/source provenance audit.
- True single-bit source variants not built for C/D1/D2 (their built-in
  faults inject 64 gross samples); cascade verdicts rest on those.
- C's silent WAV fallback on unrecognized mode strings is a footgun.
- D2's integrity gate covers only the RESPOND cue path.
