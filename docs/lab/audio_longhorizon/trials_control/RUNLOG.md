# RUNLOG — Phase B2b (PREREG_LH §2b/§2c), real-target audio control + closed loop

All times UTC, 2026-09-26. Workdir: `~/workspace/audio_longhorizon/trials_control/`.

## Frozen inputs
- Prereg: `~/workspace/audio_longhorizon/PREREG_LH.md`, commit `1278e148dd5bbe6bbbd0516e1f66f730b5a21c2b`.
- Corpus seal (user-supplied): commit `9add0edbc7b4`. (Wiring docs separately cite
  an earlier seal/session commit `e49b2a12`; both preserved, not conflated.)
- Local corpus state 2026-09-26: 359 clips verified SHA-256 clean (0 mismatches);
  field 100/100, speech 76/150 (shortfall + 50% per-source-cap violation),
  child 52 (vowel-class eligibility unconfirmed), prosody 100/100,
  31 low-F0 non-quota clips.
- Frozen scorer base: `~/workspace/audio_principles/crew_p/scorer_p.py`
  (pitchrel/pitchabs/env/rhy/hf bit definitions; defines no prosody CV).
- Frozen organ: `~/workspace/audio_principles/crew_p/organ.zag` + low-F0 guard
  `~/workspace/audio_longhorizon/wiring/src/f0low.zag`.

## Build
- `src/ctrl_main.zag`: pure-Zag control/closed-loop harness (zero RNG).
  Hears references through the embedded frozen organ + low-F0 guard; native
  descriptors (F0, voiced frac, env class, RMS, robust prosody CV) never cross
  the process boundary. Renders 2 s PCM16 mono WAV: continuous F0,
  flat/rise/decay envelope, deterministic 5 Hz vibrato for prosody.
  Persistent 16-entry history ring (matches wiring design).
  Modes: `cal | match | loop | batch | sever`. `batch` supports M (control)
  and L (closed-loop, iters 0-3) targets.
- Assembly: `src/build_ctrl.sh` — organ.zag (main renamed) + f0low.zag
  (byte-identical) + src/ctrl_main.zag → `build/ctrl_full.zag`, compiled with
  pinned `znc_linux_x86_64_abed8aa1`.
- Binary SHA (post robust-CV): `0c01be7471f853176fa7d8ce677a3e5b78ab6dcf60ff927f568ae7b5e78eae09`
  (supersedes `49b4f6e7a7b230a36c8e30c2c3fbadcbc639aaf3575081c2d881a83a2334c515`
  from the raw-CV build).
- `src/scorer_ctrl.py`: frozen offline scorer (SHA
  `dc5a1f1f846ded299d55659b05946681ef31243e014e3ca481d416cbe1e26b`),
  frozen BEFORE scored runs. Defines: robust prosody CV (median-3, f0>0),
  hit criteria, ERR, RC0 permutation test, RC1 frozen derangements
  (pitch/prosody: shift-by-20; env: shift-by-1 on interleaved R/F/D order),
  Wilcoxon signed-rank, instability/sawtooth flags, depth curve.

## Target selection (deterministic, pre-run)
- `src/measure_corpus.py` → `targets/clip_measure.json` (SHA
  `91dfbe4b39b778e60daf59492ecba7f03823fd0b5d9c002ecf64bc7b36e44127`).
- `src/select_targets.py` → `targets/SELECTION.json`:
  pitch40 (F0 126.5–806.3 Hz), env40 (13 rise / 14 flat / 13 decay),
  pros40 (robust CV 0.094–0.487), loop20 (16 general + 4 low-F0 intended;
  one general candidate is also lowf0-class → 5 low-F0-class cases; reported).
- `targets/batch160.txt`: depths 1–40 pitch, 41–80 env (interleaved R/F/D),
  81–120 prosody, 121–140 loop20, 141–160 repeats of first 20 pitch refs.
- `targets/loopfresh20.txt`: same 20 loop refs (fresh-state run).

## Calibration (pure-Zag, pre-run)
- Vibrato depth → native robust CV: 0.02→0.013, 0.05→0.033, 0.10→0.066,
  0.20→0.131. Gain G=660 per-mille per unit depth (raw-CV gain was 690).
- Scorer-vs-native on cal tone (depth 0.10): scorer 0.0655 vs native 0.066.
- Envelope: rise/flat/decay renders classified correctly by organ and scorer.

## Scored runs (all `batch`, gain 660)
- r1/r2/r3: wired, `targets/batch160.txt` → `runs/r1| r2| r3` (3× headline).
- rc0: severed (`sever` flag), same batch → `runs/rc0`. NOTE: first rc0 launch
  used `1` instead of the literal `sever` token and ran wired; killed,
  outputs deleted, relaunched correctly (ANOM-008).
- loopfresh: wired, `targets/loopfresh20.txt` → `runs/loopfresh`.
- All five launched 2026-09-26 ~04:56 UTC in parallel (2-core VM, heavy load).
- **r4**: third COMPLETE 160-target wired run, launched 2026-09-26 ~09:30 UTC
  post-reboot (binary SHA verified unchanged:
  `0c01be7471f853176fa7d8ce677a3e5b78ab6dcf60ff927f568ae7b5e78eae09`),
  → `runs/r4`. r2 died at 159/160 (ANOM-010) and does not satisfy the 3×
  completed-rerun requirement; r4 replaces it.

## Scorer corrections (2026-09-26, before final scoring)
Frozen `src/scorer_ctrl.py` SHA
`7a4c232a1b96aa1a9a2b52a5b843c35a3c604c7c3f246ea2898ab8421e726224`:
(1) restored HITFN; (2) one-based axis bounds pitch [1,41), env [41,81),
pros [81,121); (3) ERR ratio = aggregate sum(ERR3)/sum(ERR0) (the
"mean_err_ratio" field name is a leftover; formula is the aggregate);
(4) RC0 one-sided EXACT Fisher/hypergeometric (zero scorer RNG);
(5) corrected equivalent bounds in `src/analyze.py`. The fresh loopfresh
battery was first scored under the per-case-mean formula (0.951); rescored
2026-09-26 under the corrected scorer: aggregate ratio 0.9649
(`evidence/loopfresh_corrected.json`).

## Byte-identity proof (r1≡r3; evidence/rerun_identity_r1r3.json)
- Raw journal SHAs differ ONLY by embedded run-dir path segments
  (`RENDERED runs/r1/...` vs `runs/r3/...`): r1
  `00a26ce038043fd5c7caff3052c0c754691193dde5184ade71aa679387565d80`,
  r3 `9116cd2c0bb0a115ac62e28f2180ac02b116835722587e49bfa0546fb300eb0e`.
- Canonical journals (run-path normalized): identical, `5f8c19f9fb8de908…`.
- WAV manifests (basename → SHA-256): 220/220 identical, zero mismatches.
- r4 identity vs r1/r3: pending r4 completion.

## Prereg-noted deviations (all frozen before scored runs)
1. MATCH renderer extension: the wired 5-action renderer cannot do continuous
   F0/envelope/prosody matching; added a minimal pure-Zag MATCH extension.
2. Prosody CV definition: scorer_p.py defines none; froze robust median-3 CV
   (f0>0 only) in scorer_ctrl.py after measuring raw frame CV dominated by
   estimator octave-jumps (neutral speech read cv≈1.0).
3. Envelope-axis circularity documented: organ env_class ≡ scorer ans_env
   (same computation); axis measures render fidelity.
4. RC1 derangements chosen for maximal mismatch (documented above).

## Results
- (pending run completion)

## Waveform audit (analyzer-first, 2026-09-26)

`src/waveaudit.py` (new): full analyzer-first battery over every render WAV —
peak/DC/zero-crossing/clipping, spectral centroid, 50/60 Hz fundamental hum,
HNR (cepstral), envelope stationarity (RMS thirds), spectral drift (centroid
thirds), edge-click ratio (first/last 5 ms vs body), and agreement of measured
descriptors with the journal's PLANNED values. Deterministic (numpy only).

Results (`evidence/waveaudit_{r1,r3,r2,rc0,loopfresh}.json`):

| Run | WAVs | Flags | Notes |
|-----|------|-------|-------|
| r1 | 220 | 27 | HUM50 13, HUM60 20, PLAN_F0_MISMATCH 23 |
| r3 | 220 | 27 | identical to r1 (byte-identical renders) |
| r2 | 218 | 27 | partial (159/160 targets) |
| rc0 | 213 | 12 | HUM60 9, PLAN_F0_MISMATCH 3 |
| loopfresh | 80 | 24 | HUM50 13, HUM60 17, PLAN_F0_MISMATCH 21 |

- Zero CLIP / DC / EDGE_CLICK / LOW_HNR / NONSTAT_FLAT flags across all 951
  renders. Max edge-click ratio 1.12 (threshold 12); max |DC| 3.9 (threshold
  100); HNR ≥ 11.4 dB everywhere (mean ~20 dB).
- The 50/60 Hz flags are FM-sideband artifacts of the wide-FM vibrato render
  design, NOT mains: every flagged file has deep vibrato (vib_pm 493939–
  500000, i.e. ±~50% FM deviation), and the renders are pure digital
  synthesis with no mains/ADC path. First implementation used a harmonic-sum
  hum detector which false-flagged 146/220 (sidebands land on 100/120/150/
  180 Hz); corrected to fundamental-only.
- PLAN_F0_MISMATCH: render-measured F0 differs >10% from journal-planned F0
  (native rendering/hearing bias, ANOM-005). Envelope plan agreement 100%
  in all runs.
- Quirk found: in severed (rc0) loop targets, iter0 is severed (440 Hz) but
  iter1+ corrections are wired (e.g. l121_iter1 planned 149578 mHz, vib
  500000) — the sever flag does not propagate into the correction loop.
  Benign for the RC0 guard (control axes only), noted for the record.
