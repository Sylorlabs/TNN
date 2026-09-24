# Crew C-CAVEAT run log — 2026-09-24

## Setup
- Source verified: contender_c/src/render_c.zag SHA-256
  0640f28fe1496d614d45c7480ea0dd211bb76fc24d4549a2433fc07a26c6d3db
  matches the frozen final SHA in contender_c/SPEC.md §6. Proceeding.
- Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
- CHOP instrument: imagination_discovery/aud/b_alpha/chop_v10.py (the only
  CHOP implementation found in the lab; aud_v10/chop.py referenced in the
  dive docs is not present anywhere — not in workspace, not on branch
  tnn-native-lab. Will re-derive CHOP-3 results with the available
  implementation + independent complete event list from plan_v1.txt.)
- Event list: par_dive/work/gen_events.py on fixture plan_v1.txt.

## Experiment record

### Step 1 — rebuild + reproduce (2026-09-24)
- Built `src/render_c.zag` (SHA-256 verified `0640f28f...a26c6d3db` = frozen
  final) with pinned znc. Two `seqmix` renders byte-identical (`cmp` clean).
- Built `src/parsrc/render_par.zag` (fork_par); two renders byte-identical.
- CHOP instrument: `~/workspace/aud_v10/chop.py` (byte-identical to
  `imagination_discovery/aud/b_alpha/chop_v10.py`; the `aud_v10/chop.py`
  path cited in dive docs does not exist in workspace or on branch —
  `~/workspace/aud_v10/chop.py` is the real tool).
- Event list: independent complete list via `par_dive/work/gen_events.py`
  on the frozen fixture (296 timestamps: onsets+offsets+release
  onsets+vibrato extrema+bed edges). The dive's 271-event list was not
  found; the 296-list reproduces BOTH anchor counts exactly, validating it.
- Results on each renderer's own WAV path (`seq` mode):
  - stock C: CHOP-1 0 / CHOP-2 none / **CHOP-3 41 total, 0 unexplained** ✓
  - PAR: CHOP-1 0 / CHOP-2 none / **CHOP-3 29 total, 0 unexplained** ✓
  - 9 V10 gates on stock C WAV: 9/9 PASS (values match RESULTS.md exactly).
- REPRODUCED. Proceeding.

### Step 2 — ablation forks
Three forks by scripted surgery on the verified source (SHAs in work/):
- `render_c_off.zag` (C-servo-off): servo disabled; per-block gain frozen at
  the plan-derived target g*=clamp(65536·T/S, 0.5, 2.0), S = plan-pure block
  RMS measured pre-gain (plan-deterministic, zero servo state). Veto
  dropped (no servo state to protect; vetoes=0 on clean fixture).
- `render_c_unity.zag` (control): g ≡ 65536 — the PAR core with the servo
  deleted. Validates as byte-identical to PAR's own WAV (SHA
  `1823f8fa...e7c5509b` on both) — independent proof the fork = PAR path.
- `render_c_smooth.zag` (C-servo-smooth): full servo dynamics; step gain
  changes replaced by a 512-sample (~11.6 ms) linear ramp
  gg(rel)=(gprev·(511−rel)+g·rel)/511 from previous block's gain to current.
  Region-reset steps kept (deliberate design). Integer arithmetic only.
- All three: byte-identical reruns proven (`cmp` clean).
- CHOP-3 (own WAV path) + 9 gates:
  - off:    53 total, 0 unexplained; GATE FAIL (G-PER 0.362 > 0.350)
  - unity:  29 total, 0 unexplained; GATE PASS 9/9
  - smooth: 36 total, 0 unexplained; GATE PASS 9/9
  - stock:  41 total; par: 29 total (anchors)
- Gain-envelope stats (1295 blocks): stock mean 1.0128 [0.876,1.157],
  137 adapts; smooth mean 1.0116 [0.877,1.212], 146 adapts — dynamics
  preserved. Off: mean 1.0114 [0.794,1.250], 0 adapts (denser stepping).

### Step 3 — smooth fork battery
- 9 V10 gates: PASS 9/9 (G-PER 0.322, G-STA 2.014, G-LURCH 2.513,
  G-DRIFT 478.889, G-FLUXm 245.169, G-SIL1/2 0, G-CLIP 0.849, G-CREST 4.544).
- RT-LONG (plan_long_2oct.txt, cue 440 @1s, RESPOND nominal 1760 @28s):
  stock C and smooth both latch (fm=456, k=-2 → f0=440) and render
  440.00 Hz (+0.0¢ honest); PAR renders 1760 (+2400¢, the lie).
  RT-LONG win preserved.
- DET: byte-identical reruns proven.

### Step 4 — analyzer-driven audibility
(a) Peak flux magnitude vs PAR's spike-magnitude distribution:
    PAR spikes: min 0.0040 / p50 0.0042 / max 0.0047 (n=29).
    The 9 C-only spikes have magnitudes 0.0035–0.0039 — ALL below PAR's
    smallest counted spike. At each C-only spike time, PAR's own flux is
    92–101% of C's flux: the peaks exist in BOTH renders at near-identical
    magnitude. They are vibrato-extremum peaks, not new transients.
(b) Common-threshold test (PAR's adaptive threshold 0.003995 as fixed ref):
    stock 13, off 8, smooth 5, unity 29, PAR 29. Every servo variant has
    FEWER supra-threshold peaks than PAR at a common threshold; stock max
    flux (0.004701) == PAR max flux exactly. The 41-vs-29 count delta is
    fully explained by the per-file adaptive threshold (C thr 0.003533 <
    PAR thr 0.003995 — C's flux floor median 0.000789 < PAR 0.000879).
    Cross-check: PAR's flux at C's threshold → 54 spikes (> C's 41).
(c) Difference signal (C−PAR): rms −34 to −42 dBFS in ±50 ms windows
    around C-only spikes; spectrogram is harmonic (<2 kHz: 80–83%),
    not broadband — the diff is the servo's intended level correction,
    not a transient. No broadband step-transient signature at the
    "extra" spike windows (the two genuine step-driven spikes at
    4.3654/26.3546 are the ones the ramp kills; see below).
(d) Ramp effect: smooth kills 2 of the 9 C-only spikes (4.3654/26.3546,
    the pair nearest the +6.2%/+8.7% adapt steps), adds 0 new spikes;
    smooth maxflux 0.004475 < stock 0.004701 (tallest step transients
    shaved). 41→36: the remaining 7 survivors are threshold artifacts.

### Step 5 — red team (faults AT the adapt boundary, t=4.7864s, dg=-9.5%)
Modes added to `render_c_cav.zag` (test-only): `cavburst` (64-sample XOR at
the boundary sample 211080), `cavdc` (+0.1 FS DC for 2 s from the boundary).
- Burst: veto FIRED (vetoes=1); gain trajectory bit-identical to clean
  (0/1295 blocks diverged). The servo cannot be made to spike by a burst —
  measurement hygiene holds. (CHOP-3 on the burst WAV is meaningless: the
  injected burst dominates peak normalization; documented, not claimed.)
- DC shift: veto did NOT fire (inside the [0.35,2.5] RMS band, by design).
  Servo tracked it: gain dragged down up to 33.6% during the attack
  (bounded by clamp/deadband), re-settled to ±3 Q16 LSBs within 0.8 s
  after the attack ended. CHOP-3: 38 total, 0 unexplained (fewer than
  clean — DC raises the flux floor/threshold).
- Adversary conclusion: can force a temporary bounded level duck, CANNOT
  make the servo generate spikes. The servo is a level follower, not a
  transient generator.

### Step 6 — excerpts banked
`excerpts/`: 4 motif (2.0–5.2 s) WAVs — servo-on stock, servo-off
(frozen target), servo-smooth (ramp512), PAR reference — all labeled
WITHHELD-NOT-FOR-REVIEW. Committed, NEVER presented to Micah.

## Key numbers (anchor table)
| config | CHOP-3 (adaptive) | CHOP-3 @PAR-fixed-thr | max flux | gates | RT-LONG |
|---|---|---|---|---|---|
| PAR | 29 | 29 | 0.004701 | 9/9 | 1760 Hz (lie) |
| C stock (servo-on) | 41 | 13 | 0.004701 | 9/9 | 440.00 Hz |
| C-servo-off (frozen target) | 53 | 8 | 0.004185 | 8/9 (G-PER FAIL) | n/t |
| C-servo-unity | 29 | 29 | 0.004701 | 9/9 | n/t (=PAR) |
| C-servo-smooth (ramp512) | 36 | 5 | 0.004475 | 9/9 | 440.00 Hz |
| C + burst@boundary | — | — | — | — | veto held, 0 diverged |
| C + DC@boundary | 38 | — | — | — | bounded duck, resettles |
