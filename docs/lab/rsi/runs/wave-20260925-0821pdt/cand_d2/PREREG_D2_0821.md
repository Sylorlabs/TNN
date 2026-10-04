# PREREG D2-DF1 - frozen preregistration, committed BEFORE any DF-1 code exists

Wave: wave-20260925-0821pdt. Slot: sensory headspace candidate (image).
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Run dir: docs/lab/rsi/runs/wave-20260925-0821pdt/cand_d2/
Frozen: 2026-09-25 08:55 PDT. Status: PREREG ONLY. No DF-1 generator,
verifier, scratch file, or render exists. Implementation is explicitly
deferred until after this prereg is committed. The prereg commit must
strictly precede the first implementation commit (commit-order
self-check); a failure is UNVERIFIABLE ORDERING and cannot be adopted
this wave.

## Candidate: DF-1 FOREGROUND DEFOCUS [NEW]

The r8c renders are uniformly sharp from the ventifact field at the
viewer's feet to the gas giant in the sky. Uniform sharpness is a
classic computer graphics tell: a real lens focused on the distant
subject renders the near field out of focus. The frozen world
decision D14 already fixes the focus plane ("my eye lands on the lit
shoulder of the great peak, at (430,400)"). The current renderer never
delivers the defocus side of that decision. C-D19 (DISCARDED
2026-09-24) addressed the same axis from the opposite side: it added
sharp detail dabs at the focus plane and failed its efficacy bar.
DF-1 is the complementary, untried mechanism: a final lens pass that
defocuses the near field while the giant, moon, sky, and focus plane
stay bit-identical to the baseline.

DF-1 is not a dab placement, not a tone change, not illumination, and
not grain: it is a frozen-radius separable integer box blur applied
only to the foreground tier (below the plain horizon curve), with a
frozen feather band at the horizon and the arch opening carved out
(the far rim seen through the arch is at infinity focus and stays
sharp). No RNG, no new samples, no clock. Deterministic by
construction.

This honors the standing line directly:
- Big lever, not a micro-lever: depth of field changes the read of
  the whole foreground (stones, arch, dust tails) in one optical
  statement, not one dab or one band.
- Free lunch: one separable blur over about one quarter of the frame
  plus one blend pass; the dry baseline renders in about 0.95 s, and
  the frozen cost bar is KB6.
- E3 honored: the mechanism only removes high frequency content. It
  cannot add grain, static, or micro detail; KB4 freezes that as a
  machine-checked bar.
- Untried: grep over docs/lab and every run dir for bokeh, defocus,
  blur kernel, gaussian blur, circle of confusion, and out of focus
  finds zero prior art. D19's prereg used the words "depth of field"
  as a concept but implemented only sharp detail dabs, and its
  verdict was DISCARD. No candidate has ever blurred anything.

## Survey evidence (why this is genuinely new, not a re-litigation)

Image levers on the r8c substrate, with dispositions:
- S11-IMG sun-conditioned dusk sky gradient: QUEUED-UNJUDGED.
- Moon phase/terminator: already substrate (pass 3 shades the moon
  from the same sun vector).
- Giant terminator plus limb darkening: already substrate (pass 3).
- S14 atmospheric limb scattering on the giant: QUEUED-UNJUDGED.
- Whirlpool surface planform on the giant: QUEUED-UNJUDGED.
- Aerial perspective wash by tier: already substrate (pass 3 L7);
  the 1121pdt survey explicitly rejected re-proposing it.
- D13 haze dabs: substrate micro-lever.
- R9 contact occlusion: QUEUED-UNJUDGED (sealed 2026-09-23; DF-1
  does not stack it, see lineage).
- S13 warm tone: QUEUED-UNJUDGED.
- E3 film grain: REJECTED by Micah's eyes 2026-09-23.
- G1 sunshafts: lane STANDS DOWN until a genuinely new design idea.
- D15/D17/D18 giant dab patches, D19 focus-plane dabs: micro-levers;
  D19 verdict DISCARD (KB2_FOCUS_BP failed), wave-20260924-0521pdt.
Audio levers: S11-AUD mono propagation QUEUED-UNJUDGED; ST-1 stereo
UNVERIFIABLE, pristine re-verification runs this wave in
sensory_st1_reverify/ (a separate lane; DF-1 does not touch it).
b_alpha V11 is Micah's own frontier: untouched. D-VID-1 lane stands
down until a re-aimed prereg with a different mechanism exists.

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/img/r8c_alien.zag, sha256
  395663d473b8f1190181300e307f224d0d256ec002ed435d03603cfb4d3c4452.
- IO substrate: docs/lab/rsi/runs/wave-20260924-0521pdt/freelunch/sub/R33_NATIVE_IO_V1.zag,
  sha256 e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8
  (the in-tree docs/lab/toolchain/ copy is absent from this working
  copy, so the vendored copy keeps the wave self-contained; D19
  precedent).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
  verified with sha256sum before use.
- Dry rebuild gate: a byte copy of r8c_alien.zag with ONLY the
  @import line repointed at the vendored substrate compiles with the
  pinned toolchain and renders a 1024x1024 BMP with sha256
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
  identical to the committed r8c baseline (S14 record). Verified this
  wave, before this prereg was written, in 0.948 s. If the rebuild
  ever fails to reproduce this hash, the wave stops and files a
  dated pre-change addendum; no baseline substitution is permitted.
- The world geometry the mask reads: r8c_plain_y(x) (plain horizon,
  about 760 plus or minus 40), r8c_arch_open (x 288..352, y 800..884,
  the far rim seen through the arch), r8c_arch_body, the 40 stones
  at y 786..986, the giant at (700,250) r 150, the moon at
  (170,120) r 26.

## The lever: DF-1 foreground defocus (frozen mechanism)

Slot: a new final pass, r8c_pass6_defocus, called after pass5 finish
and before the BMP write, in a copy of the vendored baseline source
that is otherwise byte-identical (diff-verified at evidence time:
the implementation may change nothing in passes 1-5 and may add
only the new pass function plus its single call site).

Frozen mask (all from the frozen substrate functions, no new
geometry):
- For pixel (x,y): py = r8c_plain_y(x).
- w = 0 if y <= py (sharp: sky, range, giant, moon, focus plane).
- w = 1 if y >= py + 12 (full defocus: foreground field, stones,
  arch body).
- w = (y - py) / 12 in the 12 px feather band between.
- Carve-out: if r8c_arch_open(x,y) == 1 then w = 0 (the far rim
  through the arch stays sharp).

Frozen blur (integer arithmetic, deterministic):
- Separable box blur, radius R = 7 (15x15 kernel), over a scratch
  buffer: horizontal pass then vertical pass, sums in i64, each
  1D pass divides by 15 with rounding (add 7 before divide).
- Final pixel: out = (sharp * (12 - w12) + blurred * w12 + 6) / 12,
  where w12 = round(w * 12) in 0..12. Every quantity is an integer;
  zero RNG anywhere.

The binary writes DF-1 decision lines (R, feather, blur-zone pixel
count, carve-out pixel count) to the trace. The verifier asserts the
mask geometry against the frozen substrate functions and asserts the
diff touches only the new pass.

## Perceptual metric and cost

- Perceptual metric: Micah's eyes, via sealed blind A/B. The machine
  proxies are KB2 (the subject stays bit-identical), KB3 (the
  defocus is measurable, not a no-op), KB4 (nothing high frequency
  is added), KB7 (no halo at the seam).
- Cost: one separable 15x15 blur over the foreground plus one blend
  pass. Frozen bar KB6.

## Kill bars (frozen before implementation)

- KB1 determinism: 3/3 variant renders byte-identical (sha256 equal).
  FAIL kills.
- KB2 background integrity: every pixel with w == 0 (sky, giant,
  moon, focus plane, arch opening) is bit-identical to the dry
  baseline rebuild. The pure-Zag verifier diffs the full frame; any
  differing pixel outside the mask FAIL kills.
- KB3 defocus efficacy: over the w == 1 zone (arch opening already
  excluded), mean |variant - baseline| luma >= 1.5 levels AND
  high-frequency power ratio (neighbor-difference power)
  variant/baseline <= 0.7. A no-op or near-no-op blur FAIL kills.
- KB4 E3 grain guard: the HF power ratio in KB3 is already <= 0.7
  by construction of a blur; additionally, no pixel may shift by
  more than 24 luma levels (|variant - baseline| <= 24 everywhere),
  bounding any pathological amplification. Any violation FAIL kills.
- KB5 purity: pinned znc (hash above), zero Python contact with any
  wave artifact (shell and sha256sum only), token grep clean for
  rand/srand/random/time/clock. FAIL kills.
- KB6 cost: variant render wall time <= 2.0 s (dry baseline 0.948 s
  this wave). FAIL kills.
- KB7 anti-halo: in the feather band (0 < w < 1), every final pixel
  must lie between its sharp and fully-blurred endpoint values
  (the blend is a convex combination by construction); the verifier
  asserts min <= final <= max per pixel. Any overshoot FAIL kills.

Verdict mapping (frozen): CLEAN PASS requires every bar KB1..KB7
PASS as specified. On a clean pass the deliverable is a sealed blind
A/B pair (baseline BMP vs variant BMP, order assigned by the variant
BMP's sha256 first byte parity, mapping recorded in a sealed file,
images labeled only A and B) QUEUED for Micah's blind verdict; the
candidate is NEVER adopted on metrics. Any bar failed maps to DEAD
with killing evidence. Any bar unevaluable maps to UNVERIFIABLE with
the evidence preserved and no verdict rendered (ST-1 precedent).
No bar may be weakened, narrowed, or re-interpreted to force a pass.

Sealing plan (frozen): the pair is built only from the KB-passing
variant render and the gated dry baseline render. Assignment: if the
first hex digit of sha256(variant BMP) is < 8, variant is A and
baseline is B, else baseline is A and variant is B. The mapping is
written to SEALED_MAPPING_DF1.md and committed without being opened
by the worker afterward. No listening or viewing of the pair by the
worker after sealing.

## Provenance header (planned, machine-checkable, for the evidence)

RENDER_SHA: <sha256 of the variant BMP, filled at render time>
FIRST_RENDERED_WAVE: wave-20260925-0821pdt
COMPONENT_LINEAGE: r8c_alien.zag(committed,395663d4; baseline BMP e4f65557); R9:QUEUED-UNJUDGED (2026-09-23, not stacked, plain baseline used); C1:QUEUED-UNJUDGED (2026-09-23); C2v3:QUEUED-UNJUDGED (2026-09-23); S11-IMG:QUEUED-UNJUDGED (2026-09-23); C12:QUEUED-UNJUDGED (2026-09-23); S11-AUD:QUEUED-UNJUDGED (2026-09-23); S13:QUEUED-UNJUDGED (2026-09-24); S14:QUEUED-UNJUDGED (2026-09-24); whirlpool-planform:QUEUED-UNJUDGED (2026-09-24); D19:DISCARDED (wave-20260924-0521pdt, opposite mechanism, not stacked); ST-1:UNVERIFIABLE (wave-20260925-0521pdt, audio lane, untouched); E3:REJECTED by Micah 2026-09-23; G1:STAND-DOWN; D-VID-1 V3:DEAD (wave-20260925-0221pdt, video lane, stands down)
NEW_KNOWLEDGE_CLAIM: A frozen-radius separable integer box blur applied only to the r8c foreground tier with a 12 px feather at the plain horizon gives the render a lens depth of field (near field defocused, giant and focus plane bit-identical) at negligible cost.
Tag: [NEW]. This is not a re-certification. No pending queue item is
re-surfaced or re-presented here; they are listed only as lineage so
the judge queue stays honest.

## Commit-order statement

This prereg file is committed ALONE, before any DF-1 source,
verifier, scratch, or render exists. The first implementation commit
must strictly follow the prereg commit in the commit graph; the
coordinator verifies the ordering before any verdict. A failure is
UNVERIFIABLE ORDERING and the candidate cannot be adopted this wave.

## Governance

- Pure Zag, literally: generator, verifier, analysis, and scratch
  are pure Zag compiled with the frozen toolchain. Shell coreutils
  plus sha256sum only for orchestration. No Python anywhere: not
  for glue, analysis, verifiers, harnesses, renders, or /tmp
  scratch. Any Python touch of a new wave artifact voids that
  wave's evidence on sight; there is no recovery path this wave.
  Zero-Python attestation: the evidence commit includes the shell
  history of the wave session and a token grep over the run dir.
- No em-dashes in loop documentation (standing style rule); this
  file was checked with grep before writing completed.
- Commits stay local on tnn-native-lab. Nothing is pushed. This
  worker does not commit; only the coordinator commits.
- Never touch Google Drive. Never weaken a frozen kill bar.
- Red-team: any dropout, artifact, or weirdness in the renders gets
  a knowledge-vs-architecture investigation before any verdict. A
  visible seam at the horizon is an architecture flaw in the blend
  (KB7 guards it); a foreground that reads wrong despite a clean
  blend is a knowledge gap in the world's depth story (documented,
  not patched around). Findings are written up before the verdict,
  whatever the bars say.
- This worker cannot spawn a child reviewer (depth 2/2, spawning
  disabled); the red-team pass is performed as a structured
  adversarial self-review and the limitation is disclosed in the
  verdict.

## Verdict: PROCEED (pending coordinator commit of this prereg)
