# FROZEN PREREG — IFB-1: image fault battery

**Status:** FROZEN PREREG, signature-pending. PROPOSAL ONLY — not run.
Freezing requires Micah's sign-off (see Signature block below). No battery,
fixture, or probe may be built or run under this prereg before that
signature is recorded. Running without signature violates program law.

**Decision anchor:** Micah APPROVED option B (2026-09-24): the T1–T3
three-gate test as universal law — output feedback earns authority only if
(T1) faults are detectable against plan-derived expectation, (T2) the
correction map is plan-pure (constant in measured output, Lipschitz-0,
idempotent), (T3) the output is epistemically safe to re-ingest. Image
PASSES with a per-path instantiation: plan sole authority; rendered pixels
earn authority only on the exception path as detect-and-reassert with
plan-pure re-render; bit-exact detection (region re-render to scratch +
byte diff) — strictly stronger than audio's band predicate. No continuous
feedback. Piece 3 audited empty for image. Source:
`bytegen/authority_question/DECISION_BRIEF.md` (frozen pin §0).

**Scope guard:** this battery tests the *instantiation*, not the universal
principle. The T1–T3 principle is law by Micah's decision; this battery
settles whether the image rule heals exactly, harms nothing, converges in
one step, and whether the wrong-rule variants (K5 class) fail as predicted.
Nothing in this prereg authorizes changing the principle, the production
emitters, or the rendering plan.

## 0. Frozen pins

| # | Pinned item | Pin |
|---|---|---|
| P1 | Repo + branch | `sylorlabs/TNN`, branch `tnn-native-lab`, HEAD `fce3cf19f3af9ed825df7db1419c24f20b4a67f8` (VERIFIED: branch resolves via GitHub API) |
| P2 | Source draft | `docs/lab/bytegen/authority_question/teams/image/BATTERY_PREREG_DRAFT.md` at P1, blob SHA `904445c35114c00b0564aaa39064ef2c0a7691e5` (VERIFIED) |
| P3 | Image fault analysis | `docs/lab/bytegen/authority_question/teams/image/FAULT_ANALYSIS.md` at P1, blob SHA `596314e6413033b00617598b6bc7ddf5f57b0f06` (VERIFIED) |
| P4 | Image wrong-rule cost | `docs/lab/bytegen/authority_question/teams/image/WRONG_RULE_COST.md` at P1, blob SHA `87b35654df8c6432d72e0ddcb050cba2f4c4732b` (VERIFIED) |
| P5 | Image authority recommendation | `docs/lab/bytegen/authority_question/teams/image/AUTHORITY_RECOMMENDATION.md` at P1, blob SHA `7f9a96ea11bd78a95da323463e885a5b3fc4aee0` (VERIFIED) |
| P6 | Decision brief | `docs/lab/bytegen/authority_question/DECISION_BRIEF.md` at P1, blob SHA `49d7efe186aefd9ae67e24708495bef1392f2f8f` (VERIFIED) |
| P7 | Toolchain | `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` — filename pin as cited in the draft; exact binary SHA-256 recorded in the run log at freeze (build flags `--no-zagd --no-analyze`, disc.zag header convention) |

All pins resolved against true lineage at P1. If any pin fails to resolve,
it is written "UNRESOLVED — needs re-pin" and the battery may not start.

## 1. Claim under test

The image authority rule — plan sole authority; rendered pixels earn
authority only on the exception path as detect-and-reassert with
plan-pure re-render — heals all in-scope faults to 0 differing bytes,
never corrupts clean output, and admits no continuous feedback. The
battery must ALSO run the wrong-rule variants and show they fail, so
the rule is proven against its alternatives, not just against silence.
(Transcribed verbatim from the frozen draft.)

## 2. Subjects (frozen)

- **S-A**: field.zag visual path — scene `f3_gen_g2` (greenhouse, stroke
  log ~20 strokes incl. occlusion), `f3_emit_bmp_g`, 480×480.
  Reference binary: pinned toolchain P7.
- **S-B**: toolkit canvas path — `render.zag render v2 lib` (library
  screen: cards, shadows via d_blend, text), 360×640.
- **S-C**: disc.zag — `alien` scene, 1024×1024, fixed seed (record seed
  in run log).

Clean reference: each subject rendered twice; the two outputs must be
byte-identical (SHA-256 recorded) before any fault leg runs. If not
identical, the battery ABORTS (determinism failure, not a rule failure).

## 3. Fault models (frozen)

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

Fault grounding per FAULT_ANALYSIS.md (P3): F1 region corruption (buffer),
F2 carried-state corruption mid-render, F3 output-derived global gain
(prevention, not cure — the gamma-disease normalizers), F4 seams (authored
seams vs defect seams), F5 grain/dither (plan-pure, not feedback), F6
sub-threshold flips.

## 4. Batteries

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

**B-WRONG (alternative rules must fail — K5 CLASS).** Each wrong-rule
variant runs on FM-1/FM-2/FM-3 and must FAIL at least one kill criterion:
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

*Predicted-failure framing (program law for wrong-rule arms): every W-*
variant is expected to fail ≥1 criterion in {K1, K2}. If any W-* variant
PASSES the {K1, K2} criteria on its assigned faults, the verdict rule's
PARTIAL clause fires (see §7) — the rule is under-differentiated and the
matter is escalated to Micah before any victory is claimed.*

**B-CONTRACT (stability).** Feed the corrector its own output 3× on
FM-3 (sustained): must reach fixed point at step 1 and stay (0 changes
on steps 2–3). Attempt to construct a 2-cycle or rail-pin from plan
text alone (audio Attack 4 method): must be structurally impossible —
correction map takes no input from the damaged bytes.

## 5. Kill criteria (frozen; ALL must pass)

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
  battery sources). Pure Zag (pinned toolchain P7).
- **K7 (cost bound):** B-HEAL total wall time ≤ 3× clean render time
  per subject (exception path must stay an exception, not a second
  renderer).

(All kill criteria transcribed verbatim from the frozen draft.)

## 6. Determinism & provenance requirements

- Pinned toolchain P7 (per AGENTS.md; never claim znc missing before checking this path).
- `--no-zagd --no-analyze` build flags (disc.zag header convention).
- Scratch in `~/workspace` (never /tmp: 512MB shared tmpfs — AGENTS.md).
- Every artifact SHA-256 logged; run log records seeds, regions, masks,
  binary SHAs, znc version string.
- No git commits from the battery (team lead handles commits).

## 7. Out of scope (documented, not tested)

- Piece-3 latch: audited empty for image; no battery leg.
- Perceptual quality judgments (Micah's eyes outrank metrics; the
  battery tests byte-exactness, not beauty).
- The four grandfathered peak normalizers (audio emitters): flagged
  for plan-derivation review, not part of this battery. **Not touched
  by this prereg — their repair is a separate crew's work.**
- Adversarial faults outside the six models (future red-team round).

## 8. Verdict rule

- **PASS** iff K1..K7 all hold.
- **PARTIAL** if K1–K4 hold but a W-* variant unexpectedly passes (rule
  under-differentiated — escalate to Micah before claiming victory).
- **FAIL** otherwise.
- No victory declared on partial batteries: all subjects × all fault
  models, or it didn't happen.

(All verbatim from the frozen draft.)

## 9. Amendments clause

Frozen on Micah's signature. Any change to rules, schedule, subjects,
fault models, batteries, metrics, or kill criteria after signature
requires his re-approval before running. Bent rules during execution are
documented and flagged for revert. The T1–T3 principle itself is not
amendable by this battery — it is law by his 2026-09-24 decision; this
prereg settles only the image instantiation.

## 10. Signature

**Decision (tick one):**

- [ ] **APPROVED** — the battery may be run exactly as written. No amendments.
- [ ] **APPROVED WITH AMENDMENTS** — amendments listed below; prereg re-frozen after edits, re-signed before any run.
- [ ] **REJECTED**

Amendments (if any): ___________________________________________________

_________________________________________________________________________

Signed: ____________________________ (Micah)

Date: ____________________________

**Battery-run authorization:** no battery, fixture, probe, or harness may be
built or run under this prereg before this signature is recorded. Running
without signature violates program law. The four production emitters
(`f3_emit_wav`, `f3_emit_wav_hifi`, `f3_emit_avi`, `f3_emit_avi_g`) are not
touched by this prereg — their repair is a separate crew's work.
