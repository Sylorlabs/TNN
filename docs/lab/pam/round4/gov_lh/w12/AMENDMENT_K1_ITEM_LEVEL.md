# Amendment — W12 K1: item-level wrong-admit accounting

**Status:** SIGNED 2026-09-25, decided-autonomously-per-Micah's-order (PAM Round 4 autonomous governance dispatch).
**Supersedes:** the pair-level K1 premise (frozen M1/CC1 pair accounting), for K1 purposes only. W12's no-backdoor property and all other W12 verdicts are unchanged.

## Amended premise (replaces pair-level accounting for K1)

K1's wrong-admit premise is measured at **item level**:

- The frozen bar admitted **2/30 wrongs (6.67%)** on the frozen fixture, exactly stable at 1x, 10x, and 100x under faithful resampling.
- The rate is **family-dependent**: P-family 11.11% at every scale (2/18 = 20/180 = 200/1800); W-family 0% at every scale (structural: mrgF ≤ 2373 < 3588). Adversarial above-threshold wrongs (conf 706–730 × mrgF 3600–7000) admit at **100%** (1040/1040 at 10x, 10400/10400 at 100x).
- **6.67% is a measured property of the fixture's family mix, not a bound on bar behavior.** Any reading of this amendment as "the bar admits ~6.7% wrongs" is falsified by the adversarial leg; the honest reading is "the bar admitted 2/30 wrongs on the frozen fixture, stably."
- Every admitted wrong at every scale sits at the single above-threshold cell (conf=718, mrgF=6600).

## What this corrects

Pair-level accounting (9 CC1 pairs blocked via weakest member conf=704) masked 2 item-level admissions that are really there. Item-level accounting is the honest measure.

## What is unchanged

- W12's no-backdoor property: W12's admit set == the bar's admit set EXACTLY at every scale including under adversarial flood (bar-rejected re-admitted: 0; bar-admitted dropped: 0). The K1 literal trigger is entirely bar-level behavior, frozen and out of W12's scope — nothing in the evidence implicates W12's mechanisms.
- The frozen bar tuple itself (ST=0, AT=0, CT=705, MT=3588) is NOT changed by this amendment; only K1's accounting premise is.

## Evidence

`docs/lab/pam/round4/gov_lh/w12/VERDICT_GOVLH_W12.md` (crew 1; `w12_glh.zag` passed G1 gate byte-identical to frozen evidence; 6 scale streams 2× byte-identical; independent mirror matched every row). Prereg `PREREG_GOVLH_W12.md` committed alone as `1b26ca8a`.

*Signed 2026-09-25 — PAM Round 4 autonomous governance dispatch.*
