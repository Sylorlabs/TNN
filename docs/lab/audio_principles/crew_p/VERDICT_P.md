# VERDICT_P.md — Crew P (Audio Perception Principles)

**Date:** 2026-09-26  
**Prereg:** `~/workspace/audio_principles/PREREG_AUDIO_PRINCIPLES.md` (frozen 2026-09-25)  
**Baseline commit:** `f9748042bfbb`, branch `tnn-native-lab`

## Organ

Pure-Zag input organ (`organ.zag`, 745 lines), zero external tools.
- SHA-256 (source): `eadfc83027b2c469d0f2f8534029ba2ecb3413a78f0908d4a25731aa00d33bfb`
- SHA-256 (binary): `1ed4bfba250336ad1da3fdbc66e865fe09cb6913854894c2faf0b119b53a5128`
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Design frozen in `FROZEN_ORGAN.md`. Key: YIN cumulative-mean F0 (plain
  autocorrelation argmax provably fails 80–112 Hz under the 2048-sample Hann
  window; YIN recovers 80–1200 Hz within ~2–3%).
- Boundary: only question ID + WAV path(s) cross; exact argv logged.

## Procedure compliance

1. **Manifest first:** commit `e0351700f0ad78ed95088fc25e911046470bf0d1`
   (frozen test manifest, 340 questions) landed BEFORE any test WAV existed.
2. **Sealed SHAs:** commit `ed6ef79cd0605a9f7d1bab14a0f8d38eeab66f55`
   (SHA-256 of all 680 test WAVs) landed BEFORE the organ saw any test material.
3. **Scorer sanity:** frozen Python scorer agrees 100% with manifest labels
   on all 340 questions (0 void).
4. **Three runs:** byte-identical answers across run1/run2/run3 (verified).

## Main battery results (3/3 byte-identical)

| Subtest | Score | Chance | p-value | Bar | Verdict |
|---------|-------|--------|---------|-----|---------|
| PITCH-REL | 100/100 | 0.50 | <1e-30 | ≥63 | **PASS** |
| PITCH-ABS | 60/60 | 0.0417 | <1e-83 | ≥8 | **PASS** |
| ENV | 60/60 | 0.333 | <1e-29 | ≥30 | **PASS** |
| RHY | 100/100 | 0.50 | <1e-30 | ≥63 | **PASS** |

All p-values are exact binomial (ceiling).

## Diagnostics

- **P-R1 (+1 dB, 20/subtest):** 20/20 on pitchrel, pitchabs, env, rhy.
  None below chance. No passes voided.
- **P-R2 (donor pools):** pool gaps 0.0pp on all subtests (p0 50/50 vs p1
  50/50, etc.). No POOL-BRITTLE flag.
- **P-R3 (HF, 20 2AFC):** 20/20.
- **P-R4 (40 real clips, 3-bit):** mean bit-agreement 0.783.
  Target was ≥0.90. **Below target.** This is a diagnostic, not a pass/fail
  bar. The organ's measured (frac_static, HNR, prosody) bits agree with the
  frozen analyzer on 78.3% of bits.
- **P-R5 (40 inventory pitch pairs):** 39/40.
- **Dither (x1.001, 20/subtest):** 20/20 stable on all four subtests
  (≥19/20 required). **PASS.**

## Leakage audit

- Organ received only question IDs and WAV paths (verified in runlogs).
- No labels, SHAs, or measured values cross the boundary.
- Test WAVs generated deterministically (LCG noise, no RNG) from the frozen
  manifest after the manifest commit.

## Verdict

**The organ passes all four preregistered perception bars** (PITCH-REL,
PITCH-ABS, ENV, RHY) with ceiling p-values, byte-identical across three runs,
robust to +1 dB perturbation and x1.001 dither, with zero donor-pool gap.

**Caveat:** P-R4 agreement (0.783) is below the 0.90 target. The organ's
real-clip 3-bit descriptors do not yet match the frozen analyzer closely
enough for the ≥90% agreement goal.

## Evidence

- `manifest_p.json` (committed `e0351700`)
- `test_wavs_sha256.json` (committed `ed6ef79c`)
- `evidence/run{1,2,3}/answers_run{N}.json` + `runlog_run{N}.txt`
- `evidence/sanity_report.json`, `pr1_report.json`, `dither_report.json`
- `organ.zag`, `FROZEN_ORGAN.md`, `BUILD_LOG.md`, `scorer_p.py`
