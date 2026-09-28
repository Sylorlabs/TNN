# BATTERY_PREREG_DRAFT — image fault battery (PROPOSAL — do not run)

Team Image, 2026-09-23. Frozen prereg for the battery that would PROVE
the image authority rule (AUTHORITY_RECOMMENDATION.md). Proposal only —
no battery is executed under this draft. Any change to fault models,
batteries, metrics, or kill criteria needs Micah's re-approval before
running.

## 0. Claim under test

The image authority rule — plan sole authority; rendered pixels earn
authority only on the exception path as detect-and-reassert with
plan-pure re-render — heals all in-scope faults to 0 differing bytes,
never corrupts clean output, and admits no continuous feedback. The
battery must ALSO run the wrong-rule variants and show they fail, so
the rule is proven against its alternatives, not just against silence.

## 1. Subjects (frozen)

- **S-A**: field.zag visual path — scene `f3_gen_g2` (greenhouse, stroke
  log ~20 strokes incl. occlusion), `f3_emit_bmp_g`, 480×480.
  Reference binary: pinned `toolchain/bin/znc_linux_x86_64_abed8aa1`.
- **S-B**: toolkit canvas path — `render.zag render v2 lib` (library
  screen: cards, shadows via d_blend, text), 360×640.
- **S-C**: disc.zag — `alien` scene, 1024×1024, fixed seed (record seed
  in run log).

Clean reference: each subject rendered twice; the two outputs must be
byte-identical (SHA-256 recorded) before any fault leg runs. If not
identical, the battery ABORTS (determinism failure, not a rule
failure).

## 2. Fault models (frozen)

| ID | Model | Injection point | Subjects |
|---|---|---|---|
| FM-1 | Bit-flip burst: 64 bytes in a 128×128 region, top-bit flips | pixel buffer post-render | A, B, C |
| FM-2 | Full-region dropout: 128×128 region zeroed | pixel buffer post-render | A, B, C |
| FM-3 | Sustained corruption: every 4th 128×128 tile damaged (bit-flips) | pixel buffer post-render | A, B, C |
| FM-4 | Carried-state corruption: arena cells / canvas bytes corrupted mid-render (after stroke 10 of the log / after layer 5) | field cells (A), canvas (B) | A, B |
| FM-5 | Sub-threshold: 8 low-bit flips in a smooth gradient region | pixel buffer post-render | A, C |
| FM-6 | Seam-targeted: 4-pixel-wide vertical tear at a miter/occlusion line | pixel buffer post-render | A (mullion occlusion), C-arch (miter line) |

Fault injection is deterministic: fixed region coordinates, fixed flip
masks, recorded in the run log. Zero RNG in injector, detector, and
corrector. Pure Zag for all battery code.

## 3. Batteries

**B-DETECT (detection).** For each (subject, fault): run the Piece-2
detector (region re-render to scratch + byte diff; region = 128×128
tiles). Record: detected? (must be YES for FM-1..FM-4, FM-6; FM-5 must
be YES — bit-exact detection has no floor), false positives on the
clean reference (must be 0), detection cost in ms.

**B-HEAL (correction).** For each detected fault: apply plan-pure
region re-render (A: replay stroke log into fresh arena, re-rasterize
tiles; B: replay full op sequence over fresh canvas restricted to
tiles — all layers in order; C: re-evaluate tile pixels). Record:
differing bytes vs clean reference (must be 0), idempotence (second
application changes 0 bytes), convergence steps (must be 1).

**B-NOOP (false-positive safety).** Run detector+corrector on the CLEAN
reference. Record differing bytes vs clean (must be 0) and cost.

**B-WRONG (alternative rules must fail).** Each wrong-rule variant runs
on FM-1/FM-2/FM-3 and must FAIL at least one kill criterion:
- **W-SERVO**: per-tile brightness servo chasing the tile's clean mean
  (frozen target from reference) with ±10% clamp. Expected failure:
  fights authored dark scenes (run on S-A g4 "harbor lights" too —
  must distort clean output), and/or fails to reach 0 differing bytes.
- **W-FORWARD**: brighten clean tiles adjacent to damaged ones to
  "compensate". Expected failure: differing bytes vs clean > 0 after
  "correction" — corruption smeared into clean pixels.
- **W-GLOBAL**: output-derived global gain (normalize tile set peak to
  reference peak). Expected failure: single-tile fault shifts all tiles
  (differing bytes outside the fault region > 0); bit-identity across a
  content edit broken.
- **W-SEAM**: gradient-based seam smoother over FM-6. Expected failure
  on S-C arch: miter over/under shading erased (differing bytes in
  authored seam region vs clean > threshold AND oracle check: cyclic
  over/under unreadable) — proves content destruction.
- **W-NOPLAN (plan-absolute)**: detect-only, no correction. Expected
  "failure": faults persist (differing bytes > 0) — documents the cost
  of refusing Piece 2.

**B-CONTRACT (stability).** Feed the corrector its own output 3× on
FM-3 (sustained): must reach fixed point at step 1 and stay (0 changes
on steps 2–3). Attempt to construct a 2-cycle or rail-pin from plan
text alone (audio Attack 4 method): must be structurally impossible —
correction map takes no input from the damaged bytes.

## 4. Kill criteria (frozen; ALL must pass)

- **K1 (healing exactness):** B-HEAL differing bytes vs clean = 0 for
  every (subject, FM-1..FM-4, FM-6). One nonzero fails the rule.
- **K2 (no harm):** B-NOOP differing bytes = 0; B-DETECT false
  positives = 0.
- **K3 (detection completeness):** B-DETECT detects 100% of FM-1..FM-6
  injections (FM-5 included — no floor).
- **K4 (one-step convergence):** B-CONTRACT fixed point at step 1; no
  2-cycle/rail-pin constructible.
- **K5 (wrong rules fail):** every W-* variant fails ≥1 criterion in
  {K1, K2} on its assigned faults — i.e., the battery demonstrates the
  alternatives are worse, not just that the rule works.
- **K6 (determinism):** every leg byte-identical across 2 reruns;
  SHA-256 recorded per artifact. Zero RNG anywhere (grep-verified in
  battery sources). Pure Zag (pinned toolchain above).
- **K7 (cost bound):** B-HEAL total wall time ≤ 3× clean render time
  per subject (exception path must stay an exception, not a second
  renderer).

## 5. Determinism & provenance requirements

- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (per AGENTS.md; never claim znc missing before checking this path).
- `--no-zagd --no-analyze` build flags (disc.zag header convention).
- Scratch in `~/workspace` (never /tmp: 512MB shared tmpfs — AGENTS.md).
- Every artifact SHA-256 logged; run log records seeds, regions, masks,
  binary SHAs, znc version string.
- No git commits from the battery (team lead handles commits).

## 6. Out of scope (documented, not tested)

- Piece-3 latch: audited empty for image; no battery leg.
- Perceptual quality judgments (Micah's eyes outrank metrics; the
  battery tests byte-exactness, not beauty).
- The four grandfathered peak normalizers (audio emitters): flagged
  for plan-derivation review, not part of this battery.
- Adversarial faults outside the six models (future red-team round).

## 7. Verdict rule

PASS iff K1..K7 all hold. PARTIAL if K1–K4 hold but a W-* variant
unexpectedly passes (rule under-differentiated — escalate to Micah
before claiming victory). FAIL otherwise. No victory declared on
partial batteries: all subjects × all fault models, or it didn't
happen.
