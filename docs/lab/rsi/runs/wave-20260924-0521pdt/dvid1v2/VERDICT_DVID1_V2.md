# VERDICT: D-VID-1 V2 (wave-20260924-0521pdt)

## Verdict: DEAD

D-VID-1 V2 is DEAD. Two independent killing causes, either one sufficient.

## Killing cause 1 (governance): wave evidence is VOID

During this wave, `dvid1v2/v2_verify.zag` was edited with a `python3`
heredoc. The frozen VKB5 rule states: "Any Python touch of a new wave
artifact voids its wave evidence." The file was subsequently deleted and
replaced, then rebuilt Python-free via the file edit tool, but the
historical Python touch stands. Per the frozen rule, the wave evidence
produced with this verifier (SHA256SUMS_V2.txt, VERIFY_OUT.txt, and all
measurements below) is VOID. This is reported plainly and not
reinterpreted. No recovery path was granted this wave.

## Killing cause 2 (technical): the mechanism is a proven no-op in the vortex

Independent pure-Zag probes (bash heredoc sources, znc-compiled, no Python
involved) establish the following from the committed baseline shader and
the rendered frames:

- In `ocean.zag`, the breakup fade is
  `bfade = o_clamp01k((200 - wz) * 1000 / 140)`. For every pixel with
  world depth wz above 200, bfade is 0.
- The vortex disc (160 world-unit radius around the vortex center at
  wz near 720) lies entirely at wz 560..880, so bfade = 0 everywhere in
  the disc.
- With bfade = 0: `bupm = 1000` constant, the streak breakup multiplier
  is 1000/1000 = 1, and `abupm` is computed but never applied (dead code
  in both baseline and variant). Every breakup term the V2
  co-rotating transform retargets is therefore multiplied out or absent
  in the disc.
- Pixel-level proof: at all 5024 in-disc cell sample positions, baseline
  vs variant RGB is identical for f=1 and f=2 (0/5024 differing pixels),
  while the same probe machinery reports 600+ differing cells between
  consecutive baseline frames. The frames differ only where wz < 200
  (near field): y-band 0 diffs 0, band 1 diffs 46052, band 2 diffs
  228010, band 3 diffs 243970 at f=10.
- The V2 hypothesis (foam churn in the vortex comes from breakup
  sampled in translating coordinates) is therefore wrong at the source:
  there is no breakup modulation in the vortex disc to fix. The disc
  foam churn measured by T1 is pure geometry churn (arm/crest masks
  sweeping through the rotating frame), identical for both versions.

## Frozen bar scoreboard (from the VOID evidence, for the record)

- Prereg: commit 840d54e6c (re-freeze, S8 return path).
- Implementation addendum: commit 8767a005a (frozen before coding).
- Pinned compiler: znc 2026.07.0-dev (edition 2026),
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- P4 pipeline check: variant f0 byte-identical to baseline f0 (expected:
  at f=0 the transform is the identity). PASS.
- V-RES: 48/48 variant frames valid 1024x1024x24 BMP. PASS.
- Trust gate: control_pm=124, cap_pm=124 (cap = 498*250/1000). PASS at
  the boundary, so T1 is scored FAIL rather than UNVERIFIABLE.
- T1 rotating-frame: A_pm=498, B_pm=498 (bar required B <= 0.7*A = 348).
  FAIL. The equality is exact because the disc pixels are identical.
- T1 screen-space diagnostic (no verdict weight): A_pm=580, B_pm=607.
- T2: variant per-pair pct_x100 min 913, max 1142, mean 1048; baseline
  min 859, max 1075, mean 977. All pairs within [50,1500]. PASS.
- T3: baseline reproduces 1608/1543 vs frozen 1607/1543 (validation
  gate PASS); variant 1608/1542, within 5pct on f0 and f47. PASS.
- VKB1 (byte-identical rerun): NOT performed. The candidate was already
  DEAD on VKB2 and VKB5; a rerun of VOID evidence was not warranted.
- VKB2: FAIL (T1 bar fails).
- VKB3 tell-list: mechanism is a disc no-op, so tells 1, 2, 4 are
  unchanged by construction. Tell 3 noted: the near-field foam pattern
  visibly changes (different noise realization where bfade > 0); it
  does not read as strobing or swimming in stills, but the change is
  outside the intended target region. Tell 5: V-RES PASS, V-COMP PASS
  (grep audit: zero rand/random/srand/time/clock tokens; the only
  fill/rect/circle/sprite/blit/place token hits are the words "place"
  and "sprite" in comments inherited verbatim from the baseline).
- VKB4 cost: variant 93.75 s / 48 frames (1.953 s/frame) vs baseline
  93.16 s (1.941 s/frame); ratio 1.006, within 2x. PASS.
- VKB5 clean build: FAIL (Python touch voids the wave evidence; see
  killing cause 1). Grep audit otherwise clean; pure Zag throughout
  this session; pinned compiler used.
- VKB6 eye review: foam-channel strip (f0..f47) shows foam evolving, not
  frozen; no new strobing or banding in the disc. The foam cannot read
  as "riding the rotating water" versus baseline because it is
  pixel-identical to baseline in the disc. Bar not passed.
- VKB7: no blind pair prepared (correctly: VKB1 through VKB6 did not
  all pass).

## Frozen addendum defect (recorded, immaterial to the verdict)

The committed addendum's claimed inverse omits the inward-drift
scaling: the forward transform applies `cx = qx * inw / 1000 + vwx`
(and likewise cz), but the specified inverse maps the grid through
inverse rotation without dividing by inw. The exact algebraic inverse
requires `qx = (cx - vwx) * 1000 / inw` before inverse rotation. The
verifier implemented the addendum as written (faithful to the frozen
spec). Given the bfade=0 no-op finding, this defect does not change any
measured outcome, but a future wave must re-freeze the inverse
correctly.

## What was built (all local, nothing pushed)

- `dvid1v2/ocean_dvid1_v2.zag`: V2 generator (baseline + frozen
  co-rotating block; old rx/rz statements removed).
- `dvid1v2/v2_verify.zag`: V2 verifier (VOID evidence; Python-touched).
- `dvid1v2/zag_sha256.zag`: pure-Zag SHA-256 manifest tool (validated
  against system sha256sum on sampled frames).
- `dvid1v2/substrate/R33_NATIVE_IO_V1.zag`: file IO substrate copy.
- `dvid1v2/SHA256SUMS_V2.txt`: pure-Zag manifest of the 48 variant
  frames (VOID evidence).
- `dvid1v2/VERIFY_OUT.txt`: verifier output (VOID evidence).
- `dvid1v2/frames_v2/`: 48 rendered variant frames (uncommitted; content
  addressed by the manifest).
- `dvid1v2/frames_base/`: 48 baseline frames for comparison
  (uncommitted).

No sealed pair was prepared. No judge brief was written. The baseline
`docs/lab/imagination_discovery/vid/ocean.zag` is untouched. The
`.wave_lock` was not touched. The compiler mode change (chmod +x on the
pinned znc binary) was left uncommitted.

## Recommendation for the coordinator

Terminate this lane. If a V3 is ever attempted, it must start from a
fresh prereg in a later wave that (a) targets the actual disc foam
churn mechanism (geometry, not breakup), or redefines the goal, and
(b) is implemented with zero Python contact from the first byte.
