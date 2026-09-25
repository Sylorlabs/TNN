# BUILD LOG — H5 SR ROUND, ARM SR-S9 (scaffold as input feature)

- **Prereg:** `PREREG_SR.md` FROZEN v1 (commit cab05d072ed255912344d2fbab689f30db3bc20e)
- **PREREG_SHA:** `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`
  (every training log opens with this SHA; verified against the frozen blob at cab05d07)
- **Toolchain (pinned, ONLY):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- **Arm:** SR-S9 — scaffold = oracle INPUT FEATURE s9 (per-depth-slot empirical
  correctness rate from strictly-prior training cells), removed at SIGNAL_DISCONNECT.
- **Frozen inputs:**
  - `training/features/features.tsv` SHA256
    `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d` (verified)
  - Frozen analyzer: `training/analyze.py` (byte-identical copy, not re-frozen here)
  - Mech id for this arm: **15** (0–12 baselines, 13/14 v2, 10/11 v1 — no collision)

## Kill-bar table hash (preregistered BEFORE first training run)

`KILLBARS_SR_S9.txt` (frozen §10 bars for SR-S9: B1–B9, B4b, B10, B11, B12, B13):
- **SHA256:** `e47ba193a663e8a346d15b33a4f027edc9fa649c209d1e1a633b38b2d46f5fba`

## Weight-init SHAs (preregistered BEFORE first training run)

Canonical init block (`INIT_SR_S9.txt`):
```
w1=1000
w2=0
w3=0
w4=0
w5=0
w6=0
w7=0
w8=0
w9=0
b=0
```
- **SHA256:** `958c56bd80ed53cbb6d9c9f437d9ab116e2c05e83725b34efaa6268fb4c888f2`

## Inherited state (daemon-restart resume, 2026-09-24 ~17:10 PDT)

Predecessor was killed by a daemon restart before finishing the build. Verified on resume:
- `src/`: all 7 library files byte-identical to frozen `training/v2/src/` copies
  (R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag, dlb_util/dlb_json/dlb_cfg/dlb_ledger/dlb_delib.zag) — KEPT.
- `params/`, `logs/`, `results/`, `analysis/`: empty — nothing to keep.
- **No train_sr.zag existed — REBUILT from scratch** (this log).
- **No training ran; no commits landed.** Branch head for this arm's work: this build log
  is the first committed artifact.

## Build record

- train_sr.zag: v2 §5 curriculum (A→B→C, DIV2=40000, symmetric loss + theater
  4·rise·(C−Cprev)² + G-batch b ← b − tdiv(Gdiff,4), anti-saturation clamp
  wᵢ∈[−2000000,2000000]) with 9-input head
  C = clamp((Σ_{i=1..9} wᵢfᵢ)/1000 + b, 0, 1000), f9 = s9 scaffold.
- s9: per-depth-slot (7 slots {1,2,4,8,16,32,64}) empirical correctness rate over
  released training cells seen STRICTLY BEFORE the current cell in the fixed
  training order (cumulative across epochs/passes/phases, read from the
  delayed-revelation trainer labels; never advanced during G-batch/telemetry
  re-scans); s9 = 500 when no prior cell in the slot; integer 1000·correct/total.
- policy_sr.zag: released 8-input driver, C = clamp((Σ_{i=1..8} wᵢfᵢ)/1000 + b, 0, 1000)
  from frozen Stage-1 weights w1..w8, b (w9 discarded). No s9 code path anywhere
  (B10 audit target).
- Determinism: A/B byte-identical builds (cmp) and runs; []u8 arenas with LE
  accessors only (ZNC-2026-09-21-007); zero RNG; `_zag_arg` reads ungated on argc.
- **train_sr binary SHA256 (A/B identical):**
  `18c81e8c72d5963dea89c2abaefc44609b87de58db395779a31503c66730cccc`
