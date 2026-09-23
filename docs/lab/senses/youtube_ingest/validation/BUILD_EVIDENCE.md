# validation/BUILD_EVIDENCE.md — sense_t1 fitted-threshold binary

Source: copy of ~/workspace/tnn-lab/senses/rebuild/a_raw/sense.zag (read-only
source; copied 2026-09-22) into code/src/, with the single fitted-rule change
per KB4-VIDEO prereg §3 (rematch T4: STILL iff mag < 1):

    -    if(mag2 >= 9) {
    +    // KB4-VIDEO rematch-T4 fitted rule: STILL iff mag < 1 (was mag < 3).
    +    if(mag2 >= 1) {

Octant rule, confidence rule, and everything else byte-untouched.

Build (pinned toolchain ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1):
    znc sense.zag --no-zagd --no-analyze --no-foreground-cache -o sense_t1
sha256: 1f208c2362000564179fed80a669b1c063ce4a97cb57299b4987f901e1a16385
Rebuild from same source: byte-identical (same sha) — toolchain deterministic.

Behavioral check (validation/probe_mag2.vid: 10x10 white square, 1px/2frames
rightward => measured mag=2, dx=2, dy=0):
  old binary (a_raw/sense, mag<3 STILL): judgment=STILL
  sense_t1 (mag<1 STILL):                judgment=E
Threshold change lands exactly where the fitted rule says. p000.vid
(mag=0) is STILL under both — rule change is the only behavioral delta.
