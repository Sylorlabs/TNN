# VERDICT — PAM GOV-LH CREW 1: W12 K1 premise at long horizon

Evidence: `RUNLOG.md` (this directory). Prereg `PREREG_GOVLH_W12.md`
frozen before any build (committed alone as `1b26ca8a`).
The governance question — amend K1 to item-level accounting or keep
pair-level — is NOT resolved here. What follows is the evidence for
Micah's word.

## What was tested

The frozen M1 bar's ITEM-level wrong-admit rate at 10x/100x scale, and
whether W12's no-backdoor property (admit set == bar admit set exactly)
holds at scale, including under adversarial flood. New instrument
`w12_glh.zag` (mechanism-identical scaled rebuild) passed the G1 gate:
byte-identical stdout to the frozen evidence on both frozen fixtures
before any scale run. All 6 scale streams ran 2× byte-identical; the
independent mirror matched every row on every stream (G3).

## Finding 1 — the 2/30 rate is exactly stable under faithful resampling

| battery | wrongs | bar admits | rate |
|---|---|---|---|
| frozen fixture | 30 | 2 | 6.67% |
| 10x (W-dense 0/120, P-canon 20/180) | 300 | 20 | 6.67% |
| 100x (W-dense 0/1200, P-canon 200/1800) | 3000 | 200 | 6.67% |

The P-family rate is 2/18 = 20/180 = 200/1800 = 11.11% at every scale;
the W-family is 0% at every scale (structural: mrgF ≤ 2373 < 3588).
Every admitted wrong at every scale sits at the single above-threshold
cell (conf=718, mrgF=6600). Prereg predictions held exactly — no
deviations.

## Finding 2 — the rate is family-dependent, not a bound (adversarial leg)

Wrongs engineered just above the thresholds (conf 706–730 × mrgF
3600–7000, strong=agree=1) are admitted by the bar at **100%**:
1040/1040 at 10x, 10400/10400 at 100x. The boundary control (same conf
band, mrgF 358/382) is admitted at 0%: the margin threshold is the
operative gate for near-threshold conf. All 10,600 end-to-end wrong
admissions at 100x have conf ≥ 705 and mrgF ≥ 3588 — the admitted set is
exactly the above-threshold wrongs, nothing else.

## Finding 3 — no-backdoor holds at every scale, including under flood

On all 6 scale streams (honest 10x/100x, attack 10x/100x, adv 10x/100x):
W12's admit set == the bar's admit set EXACTLY; bar-rejected items
re-admitted: 0; bar-admitted items dropped: 0. Under the adversarial
flood, end-to-end wrong admissions (1060 / 10600) equal bar-level wrong
admissions — W12 adds none of its own. The K1 literal trigger remains
entirely bar-level behavior, frozen and out of W12's scope.

## Finding 4 — the implemented bar does not consult strong/agree

Measured on honest_10x: 2760 C rows have strong=0 or agree=0; 2390 pass
on (conf,mrgF) alone and are admitted end-to-end. The frozen bar as
implemented is `conf ≥ 705 ∧ mrgF ≥ 3588` — the (1,1) strong/agree in the
prereg's bar tuple is not enforced by the code. The admitted wrongs'
strong=agree=1 is decorative; a strong=0/agree=0 wrong above (705,3588)
would be admitted identically.

## Secondary: budget scale-invariance

B=24814 produced 0 deferrals and 0 quarantines on the honest streams at
both scales (episodes remain 128-candidate windows over the same
candidate mix). Attack streams: target ADMIT with defer_count 0 at both
scales; the frozen-B2 kill condition never triggered.

## What this means for the governance question

- **For amending to item-level accounting:** the measured "2/30" is
  empirically stable — 6.67% at 1x, 10x, and 100x under faithful
  resampling of the fixture's wrong family. Item-level accounting is the
  honest measure: pair-level accounting (9 CC1 pairs blocked via weakest
  member conf=704) masked 2 item-level admits that are really there.
- **Caveat for the amendment's wording:** "bar admits 2/30 wrongs as
  measured" is a stable measurement OF THIS FAMILY, not a bound on bar
  behavior. The item-level rate ranges from 0% (W-family) to 100%
  (adversarial above-threshold) depending on family mix. If the amended
  premise is read as "the bar admits ~6.7% wrongs," the adversarial leg
  falsifies that reading; if it is read as "the bar admitted 2/30 wrongs
  on the frozen fixture, stably," the evidence supports it.
- **Unchanged by this crew:** W12's no-backdoor property is clean at all
  scales. Nothing in this evidence implicates W12's mechanisms.

## Caveats and open items

- The 100x honest C rows are deterministic repeats of the frozen 1102;
  the wrong families resample the tape's families rather than inventing
  novel wrong archetypes.
- The bar thresholds themselves were not evaluated for optimality — only
  their item-level admit behavior was measured.
- The adversarial flood did not stress the budget (ADV prices are small);
  budget-DoS via above-threshold wrongs was not tested — the junk-flood
  DoS vector was (leg 2, clean).
- Documented deviation: attack-stream trues cycle the 1101 available
  non-target C rows (prereg text assumed 1270/12700 exist); row counts
  and all predictions unaffected. Two scorer bugs were found and fixed
  before any number was recorded; instrument and fixtures untouched.

## Recommendation to parent

The evidence supports amending the K1 premise to item-level accounting
**with the family-dependence caveat above carried into the amendment
text** — the honest amendment states the measured rate AND that it is a
property of the fixture's family mix, not a bound. Keeping pair-level
accounting would preserve a measure that demonstrably masks real
item-level admissions.
