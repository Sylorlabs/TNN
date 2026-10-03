# PREREG_AMEND1: transparent correction to the Q4a/Q4b hand-derivation

Date: 2026-10-03. Worker: gen-generality.
Status: committed BEFORE the official runs it governs. The three runs
already executed (gg_expl1/2/3.txt) are reclassified as EXPLORATORY:
they exposed this derivation error and are reported, not hidden. No
implementation file changes under this amendment.

## The error

Frozen PREREG.md Section 4 (setup_g4) and Section 5 (Q4a/Q4b predictions)
treat the value 213 as kind 1 (NODE). In setup_g4, 213 appears only as an
object:

  fact_add(A,205,92,213);

No fact has 213 as a subject, so pkind(A,213) = 2 (NUM), not 1. (Contrast
setup_g2, where 211 IS a subject of the 91/92 facts and is correctly kind 1;
and setup_g3, where 212/213 are subjects. The error is specific to the
hand-derivation of setup_g4, where m2's WALK output is a terminal object.)

Consequences, derived mechanically from the frozen GEN rules (PREREG
Section 2):

1. teach(m2,205,213) records m2's contract as in{1} out{2} (not in{1}
   out{1} as Section 4 states).
2. Q4a round 2: the 1-input MAPs have nothing admittable (pool indices 1,2
   are kind 2; m0/m2/m3 require kind 1). The (0,1) 2-input application is
   reached directly: TRIES=4, not 7. The three predicted R2 INTER lines
   (INTER=-2, INTER=-2, INTER=213) do not occur.
3. Q4b: m1's admittable pairs are exactly (0,j) for kind-2 j (slot 1 must
   be kind 1; only pool index 0 qualifies). The predicted (2,j) pairs never
   occur (slot 1 = 213 is kind 2, rejected). Corrected exploration:
   R2: (0,1)=207, (0,2)=418; R3: (0,3)=412, (0,4)=623; R4: (0,5)=617,
   (0,6)=828; R5: (0,7)=822, (0,8)=1033; R6: (0,9)=1027, (0,10)=1238.
   TRIES=13, not 36. No round is quiet, so WIDEN never fires; 999 is never
   produced; ANS stays -2 by round-cap termination.

## Corrected frozen predictions (replace PREREG.md Section 5 Q4a/Q4b blocks)

Q4a:
```
INTER=2
INTER=213
INTER=205
INTER2=207
ARM=GEN PROB=Q4a ANS=207 TRIES=4
```

Q4b:
```
INTER=2
INTER=213
INTER=205
INTER2=207
INTER2=418
INTER2=412
INTER2=623
INTER2=617
INTER2=828
INTER2=822
INTER2=1033
INTER2=1027
INTER2=1238
ARM=GEN PROB=Q4b ANS=-2 TRIES=13
```

Also corrected: setup_g4 contract line in Section 4 reads
"m2 in{1} out{2}" (was "m2 in{1} out{1}").

## What does NOT change

- The world (gg_new.zag setup_g4) is UNCHANGED: it was built exactly as
  frozen in Section 4, and the amendment corrects the prediction to the
  world, never the world to the prediction (post-hoc world edits to force
  a pass are forbidden by the frozen verdict mapping).
- K5's text is unchanged ("prints EXACTLY the Section 5 block"); only the
  Section 5 Q4a/Q4b blocks it references are corrected by this amendment.
- The bar's substance is unchanged: Q4a must succeed via the intended
  partial-applicability path m1(205,2)=207 (ANS=207), and Q4b must decline
  honestly (ANS=-2, no WIDEN=1, no wrong answer). Both hold under the
  corrected derivation, and both are visible in the exploratory runs.
- Q1/Q2/Q3 predictions are unaffected (verified: exploratory output
  matches them byte for byte; their pkind derivations were correct).
- K1/K2/K3/K4/K6/K7 are unaffected.

## Why the substance survives (for the record)

The partial-applicability test asks: m1 needs (NODE, NUM); the upstream
structure m0 supplies only the NUM slot; the NODE slot comes from the
pool-seeded subject. Under the corrected derivation this is EXACTLY what
happens: the single success is (0,1) = m1(205,2) = 207, with slot 1 = the
subject 205 (kind 1) and slot 2 = m0's output 2 (kind 2). The distractor
m2's output kind (NUM, not NODE) only removes three distractor trials from
round 2; it does not touch the m0/m1 partial-satisfaction structure. Q4b's
honest decline is likewise intact: GEN explores the admittable value graph
to the round cap and declines with ANS=-2, never emitting a wrong answer.
