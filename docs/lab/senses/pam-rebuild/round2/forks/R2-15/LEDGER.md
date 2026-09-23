# LEDGER R2-15 — build record

**Fork:** R2-15 (FS-C cross-modal booster). **Prereg:** `../preregs/PREREG_R2-15.md`
(frozen, committed alone as 23a78a47c7b7dcfb68b96409a5c3acab670b122e before any build output).

## Build sequence

1. `fixtures/gen_fsc.py` — frozen generator (numpy; deterministic from (family, idx);
   master seed 20260923, streams 700+family). Every distinct blob verified at generation
   time against the numpy mirror of `front_shapetrans`/`front_pitchdisc`. Output:
   `fixtures/fsc/` — 1,150 trials in 6 batch files + `MANIFEST.fsc.sha256` +
   `GENERATOR_LEDGER_FSC.md`.
2. `src/` — `r2p_front.zag`, `r2p_protos.zag` copied byte-identical from R2-3
   (md5 b3b2ec2e…, 61e4217e…); `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag`
   byte-identical to R2-14's; `fsc.zag` new (booster + battery runner).
   Built with `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
   → 92,610-byte native binary (warnings only, same analyzer classes as R2-3's build).
3. Battery: `work/run_all.sh` — 2 passes × mode {0=booster ON, 1=OFF} × 6 batch files
   = 24 runs → `evidence/report_*_p{1,2}.txt` + `evidence/ledger_*_p{1,2}.txt`.
4. Verification: `cmp` p1≡p2 on all 48 artifacts (clean); `work/verify_fsc_ledger.py`
   re-verified all 24 hash chains (entry counts 200/200/200/200/150 per family per mode);
   `work/xval_fsc.py` Python↔Zag cross-check: 2,300 trials, 0 mismatches
   (`evidence/xval_log.txt`).
5. `VERDICT_R2-15.md` — bar table + ALIVE verdict, written after all measurements.

## Commits (branch tnn-native-lab)

- (1) prereg alone: 23a78a47c7b7dcfb68b96409a5c3acab670b122e
- (2) sources + fixtures + generator: <recorded below>
- (3) evidence + verdict: <recorded below>

No binaries or .zagd caches committed at any step. Python used only for
glue/analysis (generator, ledger verification, cross-validation) — never in the
decision path, which is pure Zag.
