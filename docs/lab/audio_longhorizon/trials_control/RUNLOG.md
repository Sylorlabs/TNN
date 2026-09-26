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
