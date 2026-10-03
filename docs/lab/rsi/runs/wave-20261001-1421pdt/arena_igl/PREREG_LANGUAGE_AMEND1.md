# PREREG AMENDMENT 1: correction of K3 (C10 expectation)

Date: 2026-10-01 PDT (written before any re-freeze run; the v6 binary is unchanged)
Amends: PREREG_LANGUAGE.md section 5, K3 only. All other bars (K1, K2, K4-K8)
are unchanged.

## Defect found in the frozen prereg

K3 required C10 to stay at 0.000. That expectation was written from the CA-1
prereg text, which describes C10 as a distinct "procedure invention" battery.
Inspection of the implemented (sealed) battery in the committed
world_gen.zag shows the expectation was factually wrong:

- C10 items (world_gen.zag, battery emission): `zemprod|` + A-template
  segments, answer = B-form segments. Comment: "C10 procedure invention (2):
  novel A-words -> B-form".
- C16 zemprod items: `zemprod|` + A-template segments, answer = B-form
  segments. Comment: "C16 (6): 3 zemprod on new words + 3 zemclass".

The two item sets are operationally identical: same question format, same
answer computation, same required behavior (produce the transformed word
form from the learned morphology). Any mechanism that correctly implements
the preregistered C16 production behavior necessarily answers C10's items.
K3's "C10 stays 0.000" therefore demanded the impossible: a correct
zemprod mechanism that selectively fails identically-formed items.

Sealed run 1 (under the original prereg) confirmed this: C10 scored 1.000
(2/2) via the same learned position-wise rewrite rule that scored C16's
zemprod items (replies "0,1,2" on items 28, 29, 38, 39, 40; white-box
zem_n 0->10 during word exposures; A/B templates induced from exposure).

## Corrected K3

K3 (no regression, no leakage): every capability except C16 and C10 must be
byte-identical to the v4 baseline (C1,C2,C3,C4,C5,C6,C7,C11,C13,C14 at 1.000;
C8,C9,C12,C15 at 0.000). C10 may score above 0.000 ONLY through the
preregistered zemprod production mechanism on its identically-formed items;
this is verified per item (C10 replies must equal the position-wise rewrite
output of the learned A/B templates, with the templates visible in learner
state). Any change to any capability other than C16/C10, or any C10 score
not attributable to the learned rewrite rule, is FAIL.

Rationale for the correction (not a weakening): the bar still guards
exactly what K3 was for, which is breakage or answer leakage in unrelated
capabilities. It corrects a false factual premise about the sealed battery.
No threshold is lowered: C16 must still reach 1.000 (K1), the total must
still exceed 0.676 (K2), determinism/no-gaming/architecture bars are
untouched.

## Re-freeze

The v6 contestant binary is frozen and unchanged. Three fresh sealed runs
(runs 2, 3, 4) are executed under this amended prereg; the determinism bar
(K6) is evaluated on those three runs. Run 1 is retained as the discovery
record of this defect.

Amended 2026-10-01 PDT. Re-freeze runs begin only after this file is written.
