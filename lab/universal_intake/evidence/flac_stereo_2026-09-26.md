# FLAC Stereo Decoder — Completion Evidence
**Date:** 2026-09-26  
**Worker:** FLAC STEREO (DECODER COMPLETION fork)  
**Branch:** `tnn-native-lab`  
**Source commit:** `124de3d818ac`  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Verdict
**FLAC stereo decodes byte-identical to `ffmpeg -acodec pcm_s16le` across all channel assignments (1, 8, 9, 10), with byte-identical reruns. Committed mono 16/24-bit fixtures regress clean.**

## Root Cause (White-Box Diagnosis)

Three distinct bugs were found by white-box diagnosis:

### Bug 1: Legal `-1` treated as decode error (PRIMARY)
`fr_takes()` returned a signed sample directly and used `-1` as the error sentinel. Every caller did:
```zag
let v = fr_takes(...);
if (v == -1) { frame_ok = 0; ... }
```
But `-1` is a legal FLAC sample, warmup value, coefficient, shift, escape residual, and side-channel value.

**Proof:** Minimal valid mid-side probe (left=all 0, right=alternating 0/1, side=alternating 0/**-1**):
- Reference (ffmpeg): accepts.
- Original decoder: aborts with `subframe fail`.
- Control (side=0/-2): succeeds.

Failing stage: **subframe signed-value ingestion, before prediction/decorrelation**. First offending value: side-channel sample index 1. No output emitted because failure occurs before decorrelation.

**Fix:** `fr_takes()` and `fr_rice()` now return explicit status (1=ok, 0=error) and store the value in output slice `vp[0]`. All callers updated.

### Bug 2: Independent stereo rejected (assignments 1-7)
Original code skipped assignments 1-7 entirely. FLAC 0-7 are independent channels with `fch = ch_assign + 1`.

**Fix:** `fch = ch_assign + 1` for 0-7, validated against STREAMINFO channel count.

### Bug 3: Escape-coded residuals mishandled (PRE-EXISTING)
Original escape logic had a bogus `param = 31` remap, missed the required `+1` on the 5-bit field (`rawbps = field + 1` per spec), and had dead code paths. This desynced the bitstream on escape-coded partitions.

**Fix:** Per FLAC spec — 4-bit escape (param=15) and 5-bit escape (param=31) both read the 5-bit field and set `rawbps = field + 1`.

## Fixtures
Deterministic stereo 16-bit fixtures (dual tones 440+880Hz left, 660+990Hz right, 3Hz AM, 44100Hz, 1s, 512-sample frames):
- `fx_t_assign1_verbatim.flac`, `fx_t_assign1_fixed2.flac` (independent, assign 1)
- `fx_t_assign8_verbatim.flac`, `fx_t_assign8_fixed3.flac` (left-side, assign 8)
- `fx_t_assign9_verbatim.flac`, `fx_t_assign9_fixed4.flac` (right-side, assign 9)
- `fx_t_assign10_verbatim.flac`, `fx_t_assign10_fixed2.flac` (mid-side, assign 10)
- `fx_t_assign10_wasted.flac` (mid-side, 1 wasted bit)
- `fx_t_assign10_const.flac` (mid-side, constant subframes)

All validated as legal FLAC by ffmpeg 8.1.2.

## Proof Table (held format: TNINAUD1 + u64le nch/sr/nframes + i64le samples)

| Fixture | Reference SHA-256 | Decoder SHA-256 | Diffs |
|---------|-------------------|-----------------|-------|
| fx_t_assign1_verbatim | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | 0/88200 |
| fx_t_assign1_fixed2 | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | 0/88200 |
| fx_t_assign8_verbatim | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | 0/88200 |
| fx_t_assign8_fixed3 | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | 0/88200 |
| fx_t_assign9_verbatim | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | 0/88200 |
| fx_t_assign9_fixed4 | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | 0/88200 |
| fx_t_assign10_verbatim | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | `fbd963a31b2bd64a6f5a14ad97d7d94059464ff695d1127e09a2efe41db94483` | 0/88200 |
| fx_t_assign10_fixed2 | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | `c16a14e635852b60521c7cbc6565ab743f96fbef66391d546288d441284dd456` | 0/88200 |
| fx_t_assign10_wasted | `4ff4b5567df278ac15f159100666b193831cdab1236241decd7a7ecf7b148f25` | `4ff4b5567df278ac15f159100666b193831cdab1236241decd7a7ecf7b148f25` | 0/88200 |
| fx_t_assign10_const | `7e497a45eac2050127c93b74686a72479edf92da5d0e19a2e5396d511d5a3409` | `7e497a45eac2050127c93b74686a72479edf92da5d0e19a2e5396d511d5a3409` | 0/88200 |

Rerun SHAs match decoder SHAs byte-identically for all fixtures (verified via `cmp`).

## Mono Regression
- `fixtures/t.flac` (16-bit mono): `17f57ff51f4e76ab24fba61000466433c8b9bb371ad31cfc1d794ff6d93a53e1` ✅ matches committed baseline
- `fixtures/t24.flac` (24-bit mono): `ece6870f199822d02b777def56b5a20a828b55857df6ec6d407b419002182fc0` ✅ 0/66150 diffs vs ffmpeg

## FFmpeg-Generated Stereo (LPC path)
- `st_ind.flac` (independent): 0/88200 ✅
- `st_ms.flac` (mid-side): 0/88200 ✅
- `st_ms_indep.flac`: 0/88200 ✅

## Notes
- Decoder's Rice `q>64` cap is pragmatic; real encoders use escape for large residuals.
- Fixture generator (`flacenc.py`) is scratch tooling, not committed.
- Sealed fixtures in `../fixtures/fx_t_*.flac` (10 files, 1.4MB total).
