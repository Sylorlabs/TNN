# PREREG ADDENDUM 1 (FROZEN, committed before any implementation file exists)

## Correction to P-B2c: SWITCH prediction 3/6 -> 2/6

The prereg as committed states "SWITCH = 3/6 (SWITCH1 0/3, SWITCH2 2/3)".
0 + 2 = 2, not 3. This is an arithmetic slip in the prediction text, caught
during a hand re-trace before implementation. The frozen prediction is
corrected to SWITCH = 2/6. The mechanism design is unchanged.

Full re-trace (frozen B2 episode lists, v2 mechanism as specified):

SWITCH1 n = [3,6,5], law R2 (tl1 = n, tl2 = n+4). Entering active v1 =
("V", "(A,V,V)") predicting tl2 = 2n.
- ep1 n = 3: predicts (97,3,98,6), true (97,3,98,7). Fail. Dispatch:
  archive minus active is empty, no dispatch. consec = 1.
- ep2 n = 6: predicts (97,6,98,12), true (97,6,98,10). Fail. consec = 2.
- ep3 n = 5: predicts (97,5,98,10), true (97,5,98,9). Fail. consec = 3,
  do_fire runs the search, finds ("V", "(A,V,C4)") exact on the window,
  no archived version matches, constructs v2. The ep3 prediction stands
  as wrong.
SWITCH1 = 0/3. No archived R2 version exists yet, so 0/3 is the ceiling.

SWITCH2 n = [2,3,5], law R1 (tl1 = n, tl2 = 2n). Entering active v2.
- ep1 n = 2: predicts (97,2,98,6), true (97,2,98,4). Fail.
  Single-failure dispatch: v1's programs give (2, 4), exact match on the
  observation, so TRACE-DISPATCH activates v1 with zero construction.
  The ep1 prediction stands as wrong (honest tally).
- ep2 n = 3: v1 predicts (97,3,98,6), correct.
- ep3 n = 5: v1 predicts (97,5,98,10), correct.
SWITCH2 = 2/3. The first post-flip episode is unpredictable without task
labels, so 2/3 is the ceiling.

SWITCH total = 2/6. P-B2c is therefore: HIDDEN-B2 = 3/3, SWITCH = 2/6,
FINAL-B2 = 1/2.

No other prediction changes. P-B2a, P-B2b, P-B2d, all A2 predictions,
all regression predictions, and the verdict rules stand as frozen.
