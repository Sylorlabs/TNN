# FABLE VIDEO ROUND — Deep Technical Advisory

## 1. The K2 Failure: What It Really Tells Us

**My reading: This is a fundamental architectural tension, not a bug.**

The K2 failure exposes a **scale-witness authority paradox** built into any multi-scale motion detector that uses majority-style resolution rules. The coarsest scale (S2) is simultaneously:

- **Blind below its resolution** (0.25 scale-px at 1px/frame is genuinely unresolvable — this is honest aliasing, not malfunction)
- **Granted equal authority** in the resolution rule (its STILL claim can veto finer scales or pass through unchallenged)

**Steelman for fundamental limit (quantization, not bug):**

- S2 at 1px/frame displacement sees 0.25 scale-px of motion. Below Nyquist; the signal is genuinely absent at that scale. Its STILL claim is *correct for its resolution*.
- The 18 `still_dir_conflict` withholds are **correct conservatism**: when scales disagree about basic motion presence, the system withholds rather than hallucinating direction. This is wise.
- The diagonal-concentration in RM1's 6px withholds (NE 9, NW 3, SE 2, SW 2) supports this: diagonal motion aliases worst across scale pyramids because both X and Y components downsample independently. S2 sees decorrelated noise where S0 sees coherent diagonal flow. The incoherence is real at S2's resolution.

**Steelman for mechanism bug (blind-witness authority error):**

- S2's STILL claim at 0.25 scale-px is not "correct" — it's **ungrounded**. A witness that cannot resolve signal should not be allowed to claim signal absence. Silence ≠ stillness.
- The p006 false-STILL is the smoking gun: S0 fell slightly below E\_FLOOR (ebar=57 < 64), withheld its direction claim, and S2's blind STILL claim passed through §4.4 unchallenged. This is not conservatism; it's **blind authority**.
- The 18 moving clips withheld with `still_dir_conflict` are **false negatives under another name**. The ground truth is motion; the system withholds because a blind scale vetoes seeing scales. That's not wisdom — it's letting the deaf judge music.

**Which reading wins? The diagonal evidence tips toward mechanism bug.**

Diagonal concentration in RM1's 6px withholds (where S2 *should* resolve motion — 1.5 scale-px displacement) suggests the incoherence is not just aliasing but **scale-pyramid directional anisotropy**: the downsampling kernel may be crushing diagonal coherence while preserving cardinal coherence. If true, S2's claims are systematically unreliable on diagonals — not because diagonals are fundamentally harder, but because *this pyramid's* S2 sees them wrong.

The repair should target **authority grounding**, not signal processing. S2's claims are honest given its signal, but its signal is ungrounded below \~1 scale-px. The resolution rule should not grant authority to ungrounded claims.

---

## 2. Path (a) vs Path (b): Decision Criteria

**My bet: Path (a), with calibration refinements. K2 should bend to mechanism reality, not the other way around.**

### Path (a): Revise P5 (scale-witness authority grounding)

**Core proposal:** A scale claiming STILL while another scale claims coherent direction at displacement `d ≥ G_MIN_PM` has its STILL claim made **ineligible** when that scale cannot resolve `d` (i.e., `d < scale_resolution_threshold`).

**Consequences:**

- The 18 `still_dir_conflict` withholds at 1px/frame become directional claims (S0/S1's direction, S2's STILL claim rejected as ungrounded).
- The p006 false-STILL remains (it failed because S0 withheld, not because S2 vetoed). Needs separate E\_FLOOR recalibration.
- S2 retains STILL authority when it *can* resolve motion (≥1 scale-px) but sees none.

**Zero-cost kill test for path (a):**
Is there *any* clip in the frozen battery where S2 claims STILL at <1 scale-px displacement and that STILL claim is ground-truth correct while finer scales claim direction incorrectly?

- If **zero such clips exist**, path (a) kills zero true positives. Pure gain.
- If **such clips exist**, path (a) is a tradeoff: fewer withholds, but new false-direction errors. Then you need a **scale-reliability prior** (e.g., trust S0 over S2 when S2 is blind).

### Path (b): Rewrite K2 (declare 1px/frame out of scope)

**Consequences:**

- B2's 26 moving clips become non-battery. K2 passes by definition.
- The mechanism remains unchanged; the slow-motion regime (1px/frame) is permanently ungoverned.
- Any future real-world footage with <1px/frame motion (e.g., slow pan on a distant landscape, glacial cloud drift) will hit the same `still_dir_conflict` withholds, and no battery will ever check them.

**This is cowardice.** Declaring a regime out of scope because the mechanism fails there is only valid if:

1. The regime is physically unreachable in deployment (it's not — slow camera motion is common), or
2. The mechanism's failure is provably unfixable without destroying performance elsewhere (not demonstrated).

Path (b) is acceptable *only if* you prove 1px/frame is fundamentally undetectable with the current scale-pyramid architecture. That's a hard proof — you'd need to show S2's blindness is Nyquist-inevitable and no finer-scale-only fallback exists.

### The discriminating experiments

**Test 1: S2 STILL-claim true-positive rate at <1 scale-px**

- **What it does:** Scan all frozen-battery clips where S2 claimed STILL at displacement <1 scale-px. Check ground truth.
- **Discriminator:** If S2's STILL claim is correct >0% of the time when finer scales claim direction, path (a) has a false-positive risk. If 0%, path (a) is free.
- **Kill:** If S2 STILL-claim true-positive rate >10% at