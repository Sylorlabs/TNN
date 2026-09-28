# R-5 RECOMMENDATION — support-gap floor for B-T4 (Track R0)

Swarm: R-5 debate (RDTDT parameter-setting run) · 2026-09-21 · Micah signs the amendment.
Do NOT commit. Formal verdict: `docs/lab/units/r0/evidence/support_gap/FORMAL_VERDICT_R5.md`
(branch `tnn-native-lab`, HEAD `1f0c057b9dd8bdbb4af1fba87a7ba7e9ebe7d2b0`).

## 1. Recommended floor (R-5)

**B-T4 hard-battery floor, per exposure 1–16, both legs, both sub-batteries:**

- **(a) Clean sub-battery: 8/8 correct decisions at every exposure, both legs.**
  "Correct" is the battery's own judgment (byte-identical across the formal M8
  matrix, N=5 + perturbations, zero RNG):
  - exposures **below the leg's support_min** (leg 0: e<3; leg 1: e<4):
    correct = **abstain** (`recruit_id=-1`, reason `d2=1`, low support).
  - exposures **at/above support_min**: correct = **recruit the byte-exact chunk**
    (`recruit_id=2`, reason 0).
- **(b) Contested sub-battery: zero recruitments at every exposure, both legs**
  (4/4 correct-abstain per leg per exposure; reason `d2=1` below support_min,
  `d2=2` at/above). Any recruitment under contested pressure = fail.
- **No averaging across exposures.** The frozen bar names "no collapse at 1
  exposure"; a mean would let an exposure-1 collapse hide behind e=2..16.

**What "collapse at 1 exposure" means (definitional note for the amendment):**
at e=1 the measured 8/8 is **eight correct abstentions, zero recruitments**
(see §4). The collapse the bar guards against is overeager recruitment of an
under-supported chunk — any recruitment below support_min, or any
wrong/missing recruitment at/above it, fails the floor.

**What Micah signs** (suggested amendment text for §0 I R-5):

> R-5 Support-gap floor: minimum hard-battery score across 1–16 exposures.
> Clean: 8/8 correct per exposure per leg — abstain (d2=1) below the leg's
> support_min, byte-exact recruitment at/above it. Contested: zero recruitments
> at every exposure (4/4 abstain per leg per exposure; d2=1 below support_min,
> d2=2 at/above). Per-exposure, not averaged. Approve.

## 2. Debate 1 — candidates steelmanned

| # | Candidate | What it means |
|---|-----------|---------------|
| A | **Strict 8/8** every exposure, both legs, both sub-batteries | Perfect hard-battery. Under determinism (8 identical reps/exposure) scores quantize to 8/8\|0/8, so this is the honest statement of the bar. |
| B | **Descriptive crew's unsigned proposal**: clean ≥7/8 per exposure both legs + contested abstention "exactly 8/8" | One explicit margin case of tolerance on clean. Note: contested has only 4 cases/exposure/leg, so "8/8" must mean both legs combined — ambiguous as written. |
| C | **Knee/onset-split**: 100% correct-abstain below support_min; 100% correct byte-exact recruit at/above; 0 contested recruitments | Same pass/fail as A (the battery's `correct` column already encodes onset), but stated in the mechanism's own terms: the floor names abstention discipline and recruitment correctness separately. |
| D | **Flat average** ≥ X across exposures | Tolerates one bad exposure. Killed by the frozen bar itself: "no collapse at 1 exposure" forbids hiding e=1 behind e=2..16. |
| E | **Contested-strict + clean-margin** | "Contested is the hard part." Rejected: wrong-chunk recruitment on clean is a memory-integrity failure, not an easy part. |

## 3. Test 1 — sensitivity: candidates × measured data, and the exposure-1 probe

All candidates PASS the measured data (clean 8/8 every exposure both legs;
contested 0 recruitments all 16 exposures both legs; 384-row table
`sg_table.csv`, sha `53b4d12dbbaebbbcc0dcae2b40da9069d4131e0e`).

**Exposure-1 decision-type breakdown** (the probe the debate required):

| Leg | Sub-battery | e=1 score | Composition |
|-----|-------------|-----------|-------------|
| 0 | clean | 8/8 | **8 correct abstentions** (reason 1, rid=-1), 0 recruitments |
| 0 | contested | 4/4 | 4 correct abstentions (reason 1), 0 recruitments |
| 1 | clean | 8/8 | **8 correct abstentions** (reason 1, rid=-1), 0 recruitments |
| 1 | contested | 4/4 | 4 correct abstentions (reason 1), 0 recruitments |

Recruitment onset: leg 0 at e=3, leg 1 at e=4 (reason 0, rid=2, byte-exact) —
exactly on the recovered bars. Pre-onset exposures are pure abstention.
**The e=1 "hard-battery score" measures abstention discipline, not recall.**
A floor stated as a single rate is mechanically sound (the battery's `correct`
judgment already distinguishes abstain-vs-recruit) but conceptually conflates
the two behaviors — see §5 for the Debate 2 correction.

## 4. Debate 2 — position move on the Test 1 evidence

The breakdown forced two moves:

1. **Single-number → behavior-phased floor.** The recommendation keeps the
   battery's per-case `correct` judgment (so pass/fail is unchanged) but the
   signed amendment must state the two phases explicitly (§1), because
   "no collapse at 1 exposure" is an abstention requirement, and a future
   reader will otherwise misread e=1's 8/8 as recall-after-one-exposure.
2. **Margin dropped.** The 8 clean cases per exposure are 8 reps of identical
   stimuli (`rep` 0–7, byte-identical outcomes). Under determinism a 7/8 is
   unreachable — scores quantize to 8/8 or 0/8 — so B's ≥7/8 "margin" is an
   illusion of tolerance that can never be exercised, and it signals that a
   single wrong case is acceptable. In a deterministic system a single wrong
   case is a systematic mechanism bug; the floor should fail it (Test 2, D6).
   If a future 10x battery legitimately needs margin, that is a new amendment,
   not baked-in slack now.

## 5. Test 2 — stress test of the recommendation (synthetic degraded batteries)

Deterministic flips applied to the measured 384-row table; R* = the §1
recommendation. Candidates A (strict) and C (knee-split) behave identically
to R* on every case; B is shown separately where it differs.

| # | Synthetic degradation | rows flipped | A / R* | B (≥7/8) |
|---|-----------------------|--------------|--------|----------|
| D1 | Overeager recruitment at e=1, leg 0 (all 8 reps → rid=2) | 8 | FAIL ✓ | FAIL ✓ |
| D2 | Late onset leg 0 (e=3 abstains instead of recruiting) | 8 | FAIL ✓ | FAIL ✓ |
| D3 | Early onset leg 1 (recruits at e=3 < minsup 4) | 8 | FAIL ✓ | FAIL ✓ |
| D4 | Wrong chunk recruited (rid=3), e=10 leg 0 | 8 | FAIL ✓ | FAIL ✓ |
| D5 | Contested leak: 1 rep recruits, e=16 leg 1 | 1 | FAIL ✓ | FAIL ✓ |
| D6 | Single-rep flake: 1/8 wrong, e=9 leg 0 | 1 | **FAIL ✓** | PASS ✗ |
| D7 | Pre-onset abstain, wrong reason (d2=2 vs 1), e=2 leg 0 | 8 | FAIL ✓ | FAIL ✓ |

✓ = floor behaves as intended (catches real collapse / passes clean data).
D6 is the discriminator: only strict fails a single wrong case; B forgives it.
Under determinism with identical reps, D6 can only be a systematic bug, so
failing it is the honest behavior — this is why the recommendation is strict.

The recommendation catches every named failure mode (overeager recruitment,
onset slip either direction, wrong-chunk recruit, contested leak, wrong
abstain-reason) and passes the measured data. D (flat average) was already
killed in Debate 1; E was rejected on principle.

## 6. Caveats and open items for the parent

- The floor binds the **1x battery** (`units/r0/impl/support_gap/sg_b4.zag`,
  339 lines; reason codes grounded in source: 0=recruit-correct, 1=low-support
  abstain, 2=margin-failed abstain, 4/5=controls). Per R-9 the same bar text
  would apply to a 10x run; support_min values are stated per-leg
  ("the leg's support_min"), not hardcoded, so re-derivation doesn't break
  the amendment.
- Controls (covered → d2=4, archived → d2=5) are not part of the R-5 number;
  they remain hard self-checks (0 fails measured). Flag if Micah wants them
  folded into the signed floor.
- I did not invoke gpt-5.6-sol: the debate positions were fully decidable
  from the table and source; per standing rule, native reasoning was the
  first choice and it sufficed.
- gpt-5.6-sol second-opinion option remains available if Micah wants an
  outside read before signing.
