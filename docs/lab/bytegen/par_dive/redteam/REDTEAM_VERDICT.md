# PAR_DIVE RED-TEAM VERDICT

Date: 2026-09-24. Scope frozen per `PREREG_PAR_DIVE.md` §5.
Targets: NATIVE (hybrid v2) + all landed contenders (A, B, C, D1, D2).
Method: pure Zag, pinned compiler
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`, zero RNG,
byte-identical reruns. Attack sheets: `sheets/`.

## Headline: NATIVE breaks in four places

Three inherited detector gaps were independently reproduced:
- **A1b**: single-bit-13 corruption, 64 samples/block × 1292 blocks —
  0/1292 flagged, 82,688 diffs persist.
- **A1c**: +3277 DC on every sample — 0/1292 flagged, all 1,323,000
  samples differ, peak 43337→46506.
- **A1d**: first 512 samples of every block zeroed — 2/1292 flagged,
  660,266 diffs persist across 1290 blocks.

Two NEW failures beyond the inherited ones:
1. **Parser fail-open (A3):** 14 malformed/extreme plans, all rc=0, zero
   rejections. 1e9 amplitude hits the signed rail; 1e18 Hz accepted;
   negative fields accepted; non-numeric tokens coerced; short EVENTs
   dropped silently; 200 EVENTs capped at 64 silently; malformed RESPOND
   overflows the nominal. No rail validation, no fail-closed behavior.
2. **30 Hz harmonic trap (A4):** a 30 Hz cue's harmonics/ZCR produce a false
   in-range 79 Hz sensor estimate; the octave corrector latches nominal
   880 Hz down to 110 Hz instead of 30 Hz. The sensor is confidently wrong.

NATIVE holds on: gross-corruption recovery (1292/1292 healed), RT-CASCADE
(single bit persists, zero propagation), cross-region isolation, the
t=1→t=28 long-horizon latch, and silence-as-memory (no state leaks).

## Contender verdicts

| Target | Breaks | Holds |
|---|---|---|
| A (pure PAR) | fail-open parser | order permutation (4/4 bit-identical); all cue attacks (deaf); cascade |
| B (PAR + region reset) | **1/11 silent clean-output divergence** (147,014 samples, no diagnostic); fail-open parser; no output recovery | region isolation (A5: 0 diffs regions 1–9); all 10 RESPOND attacks incl. 30 Hz (range gate); order (rev/stride 0 diffs); long-horizon |
| C (PAR + veto servo) | fail-open parser; **30 Hz trap (inherits NATIVE sensor)**; no output recovery (198,529 diffs persist) | servo state (vetoes hold); boundary reset (A5); cascade; long-horizon |
| D1 (PAR, nominal-only) | fail-open parser; no recovery (82,688 diffs) | all cue attacks (deaf); order; cascade |
| D2 (PAR, plan-referential) | fail-open parser; no output recovery (82,688 diffs); safety = plan provenance | all sensor attacks (no sensor); cue-tamper integrity gate; long-horizon |

## The determinism finding (B)

B rendered the frozen fixture 12 times with identical inputs: 11 runs
bit-identical, 1 run diverged silently across 147,014 samples (11% of the
file) from t=2.2 s, with byte-identical logs and no crash. No RNG, clock, or
random syscall exists in the source; the allocator zeroes. Mechanism
unidentified — consistent with a layout-dependent znc codegen read. For a
program whose law is byte-identical determinism, one silent divergence in
twelve is the single most serious finding of this campaign. It also
confounds B's sustained-corruption numbers (clean baseline itself is
two-valued).

## The parser finding (all six)

Every target — NATIVE, A, B, C, D1, D2 — accepts all 14 fuzz plans with
rc=0 and zero rejections. The fail-open parser is a family trait, not a
single-target bug. Amplitudes hit the signed rail (2147483648); event counts
are silently capped; malformed fields are coerced or dropped. None of the
six fails closed.

## The 30 Hz finding (NATIVE, C)

Any target with NATIVE's ZCR/harmonic sensor (NATIVE, C) turns an out-of-range
30 Hz cue into a false 79 Hz in-range estimate and latches to the wrong
octave (880→110 Hz). Sensorless targets (A, D1: deaf; B: range gate;
D2: plan-referential) are immune — but only B rejects-while-answering; the
others are immune by not listening.

## Cascade / isolation / memory

- RT-CASCADE (true single-bit @132300): all targets show exactly the fault
  persisting with zero downstream propagation. DEFENDED everywhere
  (NATIVE/A/B measured; C/D1/D2 with 64-sample built-in faults — strict
  single-bit variants flagged as not built).
- Cross-region (A5): NATIVE postdiff=0; B regions 1–9 zero diffs; C
  postdiff=0. DEFENDED everywhere tested.
- Silence-as-memory (A8): NATIVE zero post-silence diffs. DEFENDED.
- Long-horizon (A7): NATIVE/B/C/D2 track the t=1 cue at t=28; A/D1 ignore
  the cue (INCONCLUSIVE as responders).

## Method notes

- C's mode dispatch silently writes WAV (not raw int32) for any unrecognized
  mode string — early C fuzz/lh/xr runs were re-done in raw `seqmix` mode.
- B's output is i64 LE; all B comparisons go through `meter conv64`.
- The shipped `render_b` binary was deleted from the worktree mid-campaign
  (~08:40); rebuilt from untouched source at 08:47; fresh binary produces
  the majority (Z) state.

## Bottom line

NATIVE's detector is blind to in-band corruption (inherited), its parser
fails open (new), and its pitch sensor can be confidently wrong about
out-of-range cues (new). Among contenders, B is the most attack-resistant —
and the only one that breaks the determinism law. C inherits NATIVE's two
new failures through its sensor. A/D1/D2 are immune to cue attacks by not
listening, which is safety by deafness, not by discrimination.
