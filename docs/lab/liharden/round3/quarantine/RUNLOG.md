# RUNLOG — quarantine build (Crew C, 2026-09-24)

## Environment
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build dir: `~/workspace/liharden-build/` (binaries + scratch; NOT committed)
- Repo worktree: `~/workspace/liharden-wt/` at origin/tnn-native-lab tip
  (sparse-checkout disabled for the worktree; full tree restored)

## Steps
1. Read `~/workspace/liharden/round3/context_round3.md` and
   `~/workspace/liharden/round3/fable_round3_out.txt` (Q2c design).
2. Studied round-2 evidence on tnn-native-lab under `docs/lab/liharden/`
   (beyond/ probe + fixtures + pins; wallred/ W_S3 flat fixture; tier1/).
   Note: Crew B's `liharden/corrob/` 32-case set is not present in this
   branch tree, so the H1–H12 honest set was newly authored for this battery.
3. Wrote `quarantine.zag` (pure Zag, zero RNG; modes `admit`/`exit`).
   - Verified p32/g32 round-trip of the -1 meta sentinel with a minimal probe
     before relying on it.
   - Compiled clean first try: `quarantine_bin` (119980 bytes main).
4. Smoke-tested all 4 admit paths (INSTALL / QUARANTINED / WITHHOLD-NOQUORUM /
   WITHHOLD-G1_VETO) and all exit paths (PROMOTE / STAY / DROP-MODIFIED /
   DROP-CONTRA older+auth / DROP-DECAYED / STAY-decay) on hand-written bundles.
5. Wrote `gen_fixtures.py` (deterministic, fixed-seed LCG; generation only):
   22 admission fixtures (128-page external corpus each) + 8 exit fixtures.
   Re-ran generator; output diff-clean (byte-identical).
6. Wrote `run_quarantine.py`: every case × every window run twice,
   byte-identity asserted; TSVs + summary.
7. Full battery: determinism OK (440 admit + 16 exit runs, zero diffs);
   admission 22/22 @full window; exit 8/8; window sweep 10 points.
8. Tunability spot-checks: decay_mult 8/16 and div_min 4 via argv — all behave.
9. Wrote DESIGN.md, VERDICT.md, this RUNLOG.md.
10. Assembled `docs/lab/liharden/round3/quarantine/` (sources + fixtures +
    evidence; no binaries, no .zagd caches) and committed race-free.

## Notes / gotchas
- znc `_zag_slice_ptr` (used by the proven read_stdin pattern) is fine; the
  `slice as *u8` cast pitfall from AGENTS.md applies to manual casts, which
  this code avoids (all tables are []u8 arenas + p32/g32).
- `-1` sentinel round-trips through p32/g32 correctly (probed).
- A hand-rolled smoke fixture with a bad splice initially showed votes=5;
  root cause was the test file (duplicated header/pages), not the binary.
