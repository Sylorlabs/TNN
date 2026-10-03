# PREREG SENSE-BIGLEVER-1121 - frozen preregistration, committed BEFORE any G1 code exists

Wave: wave-20260924-1121pdt. Slot: sensory big-lever scout.
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Run dir: docs/lab/rsi/runs/wave-20260924-1121pdt/
Frozen: 2026-09-24 11:45 PDT. Status: PREREG ONLY. No G1 generator,
verifier, or render exists. Implementation is explicitly deferred until
after this prereg is committed. The prereg commit must strictly precede
the first implementation commit (commit-order self-check); a failure
cannot be adopted this wave.

## Candidate: G1 SUNSHAFTS (crepuscular shafts) [NEW]

The single biggest photo-vs-painting tell left in the r8c sky is that
the light stops at the clouds. The substrate paints 24 thin cirrus dab
streaks (D12) and 50 haze dabs (D13), then the sky is done: no light
ever travels through the air. In real dusk photographs the low sun
throws visible shafts through cloud gaps, and those shafts are one of
the strongest "this is a photograph" signals in the frame.

G1 adds a real atmosphere volume mechanism: a frozen cloud-deck density
field over the sky, through which the frozen D1 sun is raymarched in
screen space. For each sky pixel, the binary marches toward the sun
through the density field and lifts the pixel where the transmittance
is above average. This is not dab placement, not grain, not a relight,
and not a local patch. It is a new world mechanism (volumetric
atmosphere) that changes the sky globally, and no wave has ever tried
it: grep over docs/lab shows crepuscular/god-ray/shaft mechanisms
discussed only in unrelated fork notes (r8b SDF raymarch, r10 costing),
never implemented as a candidate on the adopted r8c substrate.

This honors the standing line directly:
- Big lever, not a micro-lever: the substrate's micro-lever program
  (D15/D17/D18 gas-giant dab patches, D19 focus-plane dabs) is untouched.
  G1 operates on no dab primitive for its effect; it is per-pixel
  screen-space integration.
- Free lunch: perceptual gain at the same cost class (bounded extra
  passes, no new data structures beyond small integer tables).
- E3 honored: the mechanism is explicitly soft (see KB6 anti-grain bar).
  No high-frequency static is added anywhere.
- Data amount is varied and measured: the raymarch sample count N is
  the data knob. The candidate ships the frozen default N=12; evidence
  reports metric bars for N in {6, 12, 24}. The sealed A/B pair uses
  the frozen default only, chosen before any render exists.

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/img/r8c_alien.zag (in-tree,
  unmodified for the baseline build).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- IO substrate: Linux-ported raw-syscall R33_NATIVE_IO_V1.zag vendored
  inside the wave run dir (same arrangement as wave-20260924-0521pdt).
- The baseline must rebuild BEFORE any G1 code is written: a byte copy
  of r8c_alien.zag with only the @import line repointed at the vendored
  substrate must render a BMP with
  sha256 e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
  identical to the committed r8c baseline (S14 record). If the rebuild
  ever fails to reproduce this hash, the wave stops and files a dated
  pre-change addendum; no baseline substitution is permitted.
- Reference render time: about 1 s at 1024x1024 (0521 measurement).

## The lever: G1 sunshafts (frozen mechanism)

Slot: new pass g1_dec15_sunshafts after r8c_pass3 (light logic), before
r8c_pass4 (fixations). Rationale, frozen: shafts are atmosphere lying
over the lit world, and the eye's fixations may respond to them the way
eyes do. Pass 5 (vignette, grain) runs after, unchanged.

All arithmetic is integer, per-mille fixed point. Zero RNG anywhere.
Every constant below is frozen; the implementation may not tune them
against renders.

- Shaft origin S = (82, 532): the frozen D1 sun glow center
  (w*8/100, h*52/100). The sun sits low left, just below the horizon.
- Cloud-deck density D(x,y), sky positions only:
  D = r8c_fbm(x*256/520, y*256/180, 9131, 3). Wind-stretched along x
  like the D12 streaks. D in 0..1024. This field is shaft machinery
  only; it is never rendered as visible cloud.
- For each pixel p with r8c_tier_at(p) == 0 (sky; the planet and moon
  discs are tiers 4 and 5 and are excluded by construction):
  - March N steps from p toward S. Step k (0..N-1): t = k*1024/N,
    qx = px + (82-px)*t/1024 + jx, qy = py + (532-py)*t/1024 + jy,
    where jx = r8c_h01(px, py, 9132+k) / 64 - 8 and
    jy = r8c_h01(py, px, 9133+k) / 64 - 8 (frozen hash jitter, breaks
    marching banding; it is a deterministic function, not RNG).
    Clamp q to the frame.
  - Transmittance T(p) = sum over k of (1024 - D(q_k)) / N, in 0..1024.
  - Lift L(p) = max(0, T(p) - 400) * 90 / 624, in 0..90 luma steps.
    Only above-average transmittance lifts: gaps glow, deck stays.
  - Pixel update, frozen exactly (sun color 255,172,112):
    r1 = r0 + L * 255 / 90, g1 = g0 + L * 172 / 90,
    b1 = b0 + L * 112 / 90, each clamped to 255.
- Terrain is untouched by construction: the loop skips every pixel
  with tier_at != 0, and KB4 audits this.
- The binary prints "G1 shafts: N=<n> sky_px=<m>" and writes its
  decision lines to the elaboration trace like the other decisions.
- Data sweep: N in {6, 12, 24}, three variant binaries differing only
  in this frozen constant. The candidate is N=12. All three are
  measured; only N=12 goes to the sealed pair.

## Frozen point sets (verifier g1_verify.zag, pure Zag, on final BMPs)

Luma L = (299R + 587G + 114B) / 1000. dL = L_variant - L_baseline.

- WEDGE (shaft region): sun S=(82,532). Six rays with direction
  (dx,dy) in {(-3,-4),(-1,-2),(-1,-4),(1,-4),(1,-2),(3,-4)} (upward,
  dy negative, y grows downward). Eight points per ray:
  p = S + t*(dx,dy)*40 for t=1..8. Keep points with 0<=x<1024,
  0<=y<1024 and tier_at==0. Assert kept >= 36 of 48.
- OFFWEDGE (sky control): k=0..47: x = 560 + (k*37 % 440),
  y = 60 + (k*53 % 200). Keep tier_at==0. Assert kept >= 36.
  (The wedge spans x<=442 upward, so this set is clear of it.)
- TERRAIN: k=0..63: x = 40 + (k*61 % 944),
  y = r8c_ridge_y(x) + 40 + (k*37 % 200). Keep tier_at>=1.
  Assert kept >= 56.
- SKY12 (anti-grain): the 12 D19 sky points (80+72k, 60+15*(k%4)),
  k=0..11. Acutance A as in the D19 prereg.
- RADCUT (banding): S + t*(16,-32) for t=1..24. Keep
  y < r8c_ridge_y(x)-10. Assert kept >= 16.

## Frozen kill bars

- KB1-DET: 3 renders of the N=12 variant, sha256 identical across all
  3. Else FAIL.
- KB2-SHAFT: mean L_variant / mean L_baseline over WEDGE >= 1.12.
  The mechanism must fire where the shafts are.
- KB3-STRUCTURE: variance of dL over WEDGE >= 60.0. Distinct shafts,
  not a uniform glow wash. A wash scores near zero and fails.
- KB4-NONREG-TERRAIN: mean |dL| over TERRAIN <= 1.0. Shafts must not
  touch terrain; any terrain change fails the candidate.
- KB5-NONREG-SKY: mean |dL| over OFFWEDGE <= 6.0. The change stays in
  the shafts, not a global sky regrade.
- KB6-ANTIGRAIN (honors the E3 rejection): acutance ratio
  variant/baseline over SKY12 <= 1.10. Shafts are soft; any uniform
  high-frequency lift fails.
- KB7-NOBAND: over RADCUT, max |second difference of dL| <= 25.
  No visible marching banding.
- KB8-COST: g1 shaft pass wall time <= 3.0x baseline total render
  wall time (measured, reported); op count reported. The free lunch
  claim is perceptual gain at the same cost class.
- VKB-EYE: a sealed blind A/B pair (baseline vs N=12 variant) is
  prepared for Micah. Randomized, mapping sealed. He is the judge.
  Nothing is adopted on metrics alone.

## Frozen predictions (directional)

KB2 and KB3 pass with margin (the density field has real structure and
the sun is low, so transmittance varies strongly along rays). KB4
passes by construction (terrain loop is skipped). KB5 passes (the
400/624 gate keeps the deck dark). KB6 passes (no per-pixel hash is
added; jitter is subpixel and absorbed by the 2px acutance step). KB7
is the risk: 12-step marching can band, and the hash jitter is the
mitigation; if KB7 fails, the candidate fails rather than the bar
being tuned. KB8 passes (sky-only loop, ~40% of pixels, bounded N).

## Provenance header (planned, machine-checkable, for JUDGE_BRIEF.md)

RENDER_SHA: <sha256 of the N=12 variant BMP, filled at render time>
FIRST_RENDERED_WAVE: wave-20260924-1121pdt
COMPONENT_LINEAGE: r8c-substrate(S14-record,committed); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S11-AUD:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED
NEW_KNOWLEDGE_CLAIM: Screen-space crepuscular shafts raymarched through a frozen cloud-deck density field add structured dusk light to the r8c sky at the same cost class.
Tag: [NEW]. This is not a re-certification. No pending queue item is
re-surfaced or re-presented here; they are listed only as
QUEUED-UNJUDGED lineage so the judge queue stays honest.

## Levers considered and rejected (why this is not a substrate micro-lever)

- Aerial perspective: already substrate (D13 haze dabs; r8a ghost
  ridge). Proposing it again would be a re-litigation.
- Contact occlusion: R9 is sealed and QUEUED-UNJUDGED. Re-proposing
  would re-surface the pending queue.
- Focus-plane detail: D19, wave-20260924-0521pdt, decided this morning.
- Film grain: E3 was REJECTED by Micah's eyes 2026-09-23 (visible
  staticyness, baseline preferred). KB6 hard-codes that verdict.
- Gas-giant dab patches: D15/D17/D18 territory, micro-levers.
- Water specular glitter: the r8c scene has no water body; adding one
  is a scene change needing new composition, not a mechanism on the
  frozen baseline.
- New scene renderer: out of scope for a single-wave lever; the clean
  A/B needs the frozen r8c baseline.
- Audio: V11 is Micah's audio frontier; this slot stays out of audio.
  His 35 reserved AMBIG video clips are untouched.
- Micah's overnight work (PAMs v2, b_alpha v9 rebuild): not litigated,
  not touched.

## Governance

- Pure Zag, literally: generator, verifier, analysis, and /tmp scratch
  are pure Zag compiled with the frozen toolchain. No Python anywhere.
  Any Python touch of a new wave artifact voids that wave's evidence
  on sight; there is no recovery path this wave.
- No em-dashes in loop documentation (standing style rule).
- Commits stay local on tnn-native-lab. Nothing is pushed.
- Red-team: any dropout, flicker, artifact, or weirdness in the
  renders gets a knowledge-vs-architecture investigation (data gap in
  the density field or substrate flaw), documented before any verdict.

## Verdict: PROCEED

G1 SUNSHAFTS is a genuinely new big-lever mechanism: volumetric
crepuscular shafts, never tried on the adopted substrate, global
rather than dab-local, with frozen realism bars his eyes will judge
and machine bars that discriminate shafts from wash, grain, banding,
and terrain bleed. Draft ends here; implementation begins only after
this prereg is committed.
