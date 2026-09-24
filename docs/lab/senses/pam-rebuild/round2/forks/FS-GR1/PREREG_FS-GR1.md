# FS-GR1 Preregistration — Frozen 2026-09-24

Gate-redesign crew for PAM rebuild round 2. This document freezes the battery,
diagnoses, redesigns, bars, and scoring BEFORE any redesigned mechanism is run.
No mechanism edits after this commit except documented build-defect repair
(requires rerun from scratch).

## 1. Battery pin (frozen, do not redraw)

- Source: `round2/forks/FS-E2b/fixtures_e2b/` (12,000 fixtures + 12,000 truth sidecars)
- Adversarial manifest SHA-256: `f4f85194c4ee0cf157f7b155881a2c0797041beb5e2ee03bfb4ee7b70512e7a2`
- Control manifest SHA-256: `64798b244f90ddeaffe695ed4a43e361dbb397037da5595671c611cb01f6d22d`
- Manifest line counts: 10,000 adversarial, 2,000 control.
- File-level verification 2026-09-24: recomputed all 12,000 SHA-256 entries — **ok: 12000 bad: 0**.
- MASTER=20260926. Draw record: `round2/forks/FS-E2b/evidence/eval/DRAW_RECORD.md`.
- The battery is pinned by the two manifest SHAs above. It must not be redrawn.

## 2. Frozen FS-E2b baselines (carried into prereg)

### Adversarial FI (Wilson 95% UCB)

| Task | FI / n | FI rate | Wilson 95% UCB |
|---|---:|---:|---:|
| colordisc | 0/2330 | 0% | 0.1646% |
| colorconst | 0/1380 | 0% | 0.2776% |
| shapetrans | 0/2345 | 0% | 0.1636% |
| pitchdisc | 0/2330 | 0% | 0.1646% |
| timbredisc | 0/985 | 0% | 0.3885% |
| motiondir | 7/630 | 1.1111% | 2.2756% |
| pooled | 7/10000 | 0.07% | 0.1444% |

### Control recall

| Task | Recall |
|---|---:|
| colordisc | 92.00% |
| colorconst | 98.40% |
| shapetrans | 86.3333% |
| pitchdisc | 93.50% |
| timbredisc | 25.00% |
| motiondir | 85.00% |
| pooled | 85.50% |

### No-regression (other four tasks only)

- FI rate may increase by ≤1 percentage point from FS-E2b.
- Recall may fall by ≤1 percentage point from FS-E2b.
- Floors: colordisc recall ≥91.00%, colorconst ≥97.40%, shapetrans ≥85.3333%, pitchdisc ≥92.50%. FI-rate ceiling 1.00% each (baseline 0%).

## 3. Diagnosis: timbredisc (white-box, complete)

Reference: `round2/forks/R2-16/TIMBREDISC_AUTOPSY.md` (committed as f282eea7).

- FS-E2b controls: formation 200/200 correct. Frozen challenge emits RICH for all 200 → recall exactly 50/200 = 25% (overstrictness, not discrimination).
- Three instrument defects (binding):
  1. **2× sample-rate error**: fixture rate 16000 Hz; frozen coefficients assume 32000 Hz. Supposed 440/880/1320 Hz bins land at ~225/436/658 Hz.
  2. **Coefficient quantization**: scale 1024 cannot place bins at N=32000 (one LSB ≈ 14.5 bins; nearest integer ~7.2 bins off at 440 Hz).
  3. **i64 overflow**: `s1*s2*coeff/1024` multiplies before dividing; wrap quantum 2^54 comparable to signal power.
- Autopsy proof: exact-DFT at true bins with THEORY mapping classifies 8/8 normals and 20/20 distractors; ratios land on templates.
- FS-E2b formation ALREADY carries the corrected front end (`f_tbcoeff2`/`f_tbharm` in fse2b_form.zag): 2^20-scale coefficients (2065924/1973170/1821652 for 440/880/1320 Hz @ sr=16000, N=32000), input downscale /32, overflow-safe power `s1*s1+s2*s2-(s1*s2/1048576)*c`, THEORY mapping. Formation 200/200 on controls proves it.

## 4. Diagnosis: motiondir (white-box, complete)

- Frozen CH-MOT-2: independent 16×16 block-match frame t→t+2, search ±4, lag votes if best SAD <8000, plurality, pure agreement.
- All 7 FS-E2b FIs reproduced with white-box replica. Every FI is opposite-direction confusion where challenge agrees with wrong formation claim.
- Per-FI vote patterns (23 lags): winners 5,11,5,6,8,7,10 votes; margins 1,1,1,0,2,1,3. Fixture 34108 margin 0 (tie misresolved by enumeration).
- Root cause: per-lag argmin SAD is not truth-sufficient when texture is uninformative (aperture problem: 34060 vertical gradient → x unmeasurable; 33802/34145 flat/noisy → argmin ≈ noise). SAD<8000 gate does not abstain (flat landscapes still below gate). Plurality over noise votes installs on razor-thin margins.
- Texture-gradient threshold rejected: FI mean 18.87 vs correct mean 25.37, heavy overlap — empirical patch, forbidden.
- 3×3 blur rejected: repairs 34060 but creates confident wrong votes on 34073/34128/34145 (artifact), FI rises to 8 — empirical patch, forbidden.

## 5. Redesign CH-MOT-3 (frozen)

**Principle**: the challenge votes only on lags carrying genuine alignment signal, and outputs a direction only on decisive agreement; otherwise UNRESOLVED (withhold, never install).

**Algorithm** (on G buffer, 50 frames 32×32 u8):
1. For each lag t in {0,2,4,…,44} (23 lags): take central 16×16 block of frame t; search integer shifts (dx,dy) in [-8,8]² on frame t+2; compute all 289 SADs (sum of absolute u8 differences).
2. Let (bx,by) = argmin SAD (first in row-major order on ties — deterministic). If |bx|=8 or |by|=8: skip lag (boundary latch = wrap-contaminated or censored; the 16-pixel window cycle guarantees wraps latch at the search boundary).
3. Informativeness gate: let med = median of the 289 SADs. If med ≤ 0 or s_best/med ≥ 0.4: skip lag. Else the lag votes for mot_quant(-bx,-by) (negation recovers window direction from content displacement, as in frozen formation).
4. After all lags: let V = total counted votes. If V = 0: output UNRESOLVED (-1).
5. Let w = max votes, win = argmax (lowest index on ties). If w ≤ V/2: output UNRESOLVED (-1) (no strict majority = indecisive evidence). Else output win.

**Derivation of constants** (no battery tuning):
- Search ±8: the 2-frame true content shift is ±4 interior; ±8 contains it with margin while the ±14 wrap jump latches at the boundary and is rejected by rule 2. (Frozen ±4 could not distinguish wrap latches from interior; ±8 makes the boundary a reliable wrap detector.)
- Boundary rejection: from the 16-pixel generator window cycle — a wrap moves the viewport by 14 px, which under a ±8 search latches at the extreme. Interior true shifts (±4) never touch the boundary.
- Gate 0.4: under the null (289 i.i.d. SADs, uninformative texture), order statistics predict s_best/s_med ≈ 0.84. Informative alignments give ratios ≈0.2–0.3. The gate 0.4 sits well below the null prediction (rejects noise) and above the informative range (accepts signal). It is derived from the null model, not tuned to FI counts.
- Strict majority (>50%): the standard decisive-evidence criterion — more than half the informative lags agree. No threshold tuning; it is the weakest supermajority with a principled meaning.
- No blur: rejected (creates artifacts; §4).

**Support rule** (unchanged): INSTALL iff challenge outcome == formation claim and challenge ≠ UNRESOLVED. UNRESOLVED never installs.

## 6. Redesign CH-TBD-3 (frozen)

Port the FS-E2b formation's proven front end into the challenge (applied to G buffer):
- Coefficients (2^20 scale, sr=16000, N=32000): h=1: 2065924 (440 Hz), h=2: 1973170 (880 Hz), h=3: 1821652 (1320 Hz).
- Input downscale: x = i16_sample / 32 (bounds intermediates; mathematically justified common downscale — ratios are scale-invariant).
- Goertzel: s0 = x + c*s1/1048576 - s2; power p = s1*s1 + s2*s2 - (s1*s2/1048576)*c; clamp p<0 → 0 (rounding guard only).
- Ratios r2 = p2*1000/p1, r3 = p3*1000/p1 (p1<1 → 1; clamp r2,r3 ≤ 1000000 for totality).
- Nearest template with THEORY mapping: d0(0,0)→PURE(0), d1(1960,2560)→BRIGHT(1), d2(78,6)→DARK(2), d3(640,384)→RICH(3). Ties → first in PURE,BRIGHT,DARK,RICH order.
- Template values derive from generator TMB_PROFILES squared-amplitude ratios (autopsy §8): DARK (0.28²,0.08²)·1000=(78,6); RICH (0.8²,0.62²)·1000=(640,384); BRIGHT ((0.7/0.5)²,(0.8/0.5)²)·1000=(1960,2560).
- Overflow bound: |x|≤1024 → |s1|,|s2| ≤ ~1.7×10^7 → s1² ≤ 3×10^14 < 2^63; (s1*s2/1048576)*c ≤ ~6×10^14 < 2^63. No i64 overflow. Documented here, not tuned.

## 7. Frozen bars

1. Motiondir adversarial FI Wilson 95% UCB ≤ 1% on frozen 630-item subset. (FI = formation wrong AND challenge agrees with formation's wrong claim.)
2. Timbredisc control recall ≥ 85% on frozen 200-item subset. (Recall = challenge agrees with formation AND formation correct, /200.)
3. Other-four-task no-regression per §2 (FI ≤ +1pp, recall ≥ −1pp).
4. Byte-identical determinism ×2: every output byte-identical across two full runs.
5. Hash-chain verification line-by-line (ledger manifests).
6. No battery redraw; no mechanism edits after this prereg except documented build-defect repair (requires full rerun from scratch).

## 8. Scoring

- Run frozen battery twice with FS-GR1 binaries (formation + supervisor).
- Score per task: FI counts, FI rates, Wilson 95% UCB; control recall per task.
- Write VERDICT_FS-GR1.md with every count/rate/UCB and FINAL ALIVE/DEAD.
- Commit sources, evidence, verdict (no binaries, no .zagd, no cache files).

## 9. Implementation constraints (frozen)

- Pure Zag for mechanisms; Python only for glue/analysis; zero RNG in decision paths.
- Build with pinned znc: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
- Copy FS-E2b sources to `forks/FS-GR1/src/`; replace ONLY motiondir and timbredisc challenge mechanisms; preserve other four tasks exactly.
- Commit via `TMPDIR=~/workspace/tmp_commit python3 ~/workspace/commit_racefree.py` with lab-relative paths `senses/pam-rebuild/round2/forks/FS-GR1/...`.
- If GitHub returns 429/403: stop GitHub work immediately, report partial progress, do not retry-loop.
