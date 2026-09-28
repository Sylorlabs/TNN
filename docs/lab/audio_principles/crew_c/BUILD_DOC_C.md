# CREW C — CONTROL PATH BUILD DOC

## What this is
A TNN-native (pure Zag) binary that receives a TARGET DESCRIPTOR (native
string) and renders 2 s of 16-bit PCM mono 44100 Hz WAV hitting it.
Intent path is genuinely parametric: descriptor -> synthesis parameters
-> samples. No lookup tables keyed to targets; no RNG; 3x byte-identical.

## Build order (prereg 5.5 compliance)
1. Sealed held-out target list committed FIRST (5841d4337bf1).
2. Test manifest + frozen C1 derangement committed (048e294085d9).
3. THEN this control path's target handling was written (this file's parser).
   Synthesis primitives only were sketched before step 1; no descriptor
   parsing existed before the seal.

## Descriptor grammar
Parts joined by `+`; each part is `key:value`:
- `pitch:<Hz>`        sine carrier at <Hz> (integer)
- `env:<flat|rise|decay>`  overall amplitude envelope
- `rhy:<even|swing<N>>`    pip train; even = 250 ms IOI; swing<N> = alternate
                           long/short IOI, long=250*(1+N/100) ms,
                           short=250*(1-N/100) ms
- `prosody:<CV%>`     sinusoidal vibrato at 5 Hz; depth set so the CV of
                      instantaneous frequency equals CV% (d = cv*sqrt(2))
- Special descriptor `C0`: intent path severed; the frozen constant
  `pitch:220+env:flat+rhy:even` is substituted before parsing. Same
  machinery renders its default. (C0 arm of the battery.)

## Defaults (frozen design choices)
- No pitch: env/prosody carrier = 220 Hz / 440 Hz; rhy pips = 880 Hz pips
  (or the pitch value if `pitch:` is present alongside `rhy:`).
- No env: flat (0.9 gain + 5 ms raised-cosine edge fades).
- No rhy: continuous tone (no gating).
- No prosody: no vibrato.

## Synthesis (deterministic, closed form)
- SR 44100, 88200 samples, i64 accumulator in a []u8 arena (LE put64).
- Sine via phase accumulator (phase kept wrapped in [0, 2pi)) + Taylor
  cos/sin (technique from bf3.zag).
- Vibrato: f(t) = F*(1 + d*sin(2pi*5*t)), integrated into the phase.
- Rise: gain ramps 0 -> 0.9 linearly. Decay: 0.9 -> 0. Rise/decay hit the
  scorer's 1.5x third-ratio rule with wide margin (5x).
- Rhythm pips: 60 ms sin^2-windowed pips; 8 onsets per 2 s.
- Peak scale 28000 (< 32767 headroom).

## Dev targets (disjoint from held-out; used to validate synth+scorer)
pitch 95/165/275/390/520/700/950/1100; env flat/rise/decay (carrier 330 Hz);
rhy even/swing15/swing30 (pips 660 Hz); prosody 1.0/8.0;
pitch:330+env:rise; rhy:swing30+pitch:520.
No dev render is byte-identical to a held-out render (different carrier
pitches / swing amounts / pitch values).

## Toolchain
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (pinned).
Build: znc control.zag -o control
Constraints honored: no `as []i32/u32/u16` casts (only []u8 arenas with LE
accessors); no slice > 2^25 bytes (largest = 705600 B); argc never read
(_zag_arg read unconditionally, "" treated as absent); _zag_arg results
only read, never freed; no `try` identifier; no `};`; shallow if/else
nesting; no `.*` on non-pointers; O_TRUNC (577) on file_write so reruns
overwrite.
