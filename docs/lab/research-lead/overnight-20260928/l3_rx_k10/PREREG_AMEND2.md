# L3-RX-K10 PREREG AMENDMENT A2 (pre-verdict)

Date: 2026-10-03. Amends PREREG.md (b0b94bfc4) + AMEND1 (df2ce4fec).
Implementation of the battery revealed a flaw in MY W3 world design
(not in the learner): the withhold set left one z-edge in training,
which legitimately determined z's position. This amendment fixes the
world to implement the intended "unseen pairs" condition. The kill bar,
kill condition, and predicted outcome are unchanged.

## Flaw found

W3 (R-B decoy) as frozen withheld {(c1,z,x),(c1,x,z)} for x in
{0,1,3,4,5,6} (12 triples), keeping the {z, idx7} pair in c1 training.
Run 1 showed: the c1 partition then has od[z] = 0 < od[idx7] = 1 (idx7
beats z on the kept edge), so the tournament places z LAST determin-
istically from genuine evidence — the learner scored 6/6 (rk HOLD).
The frozen prediction (0/6 via tie-break artifact) failed because my
world left real evidence in, not because the attack's thesis is wrong.

## Change

W3 withhold set: {(c1,z,x),(c1,x,z)} for ALL x != z (14 triples);
train = 98 (was 100). Heldout unchanged: the same 6 (c1,z,x) triples
(a subset of the 14 withheld).

W6 (p6 recode of W3) inherits the fix automatically (withhold is
defined structurally; p6 maps it).

## Why the amended attack is fair (not tuned to the implementation)

The frozen thesis of RK-B is unchanged: for pairs unseen in training,
where transitive closure cannot apply (no 2-step path exists when
every z-edge is unknown) the induction's ONLY remaining determiner is
the documented deterministic tie-break (PREREG 160f138cc section
5.1(b): "ties -> lowest id"). The amended world is the minimal world
where the tie-break is the sole determiner of the committed content
for the heldout pairs. z = id 7 (smallest id) is LAST in O1C, so the
tie-break (z first) commits the exact opposite of the truth on all 6
heldout triples: predicted COMMIT with heldout 0/6, deterministic.

This does not exploit an undocumented implementation quirk: the
tie-break rule is in the frozen builder prereg, and the builder's own
F1 worlds never tested the expansion path on pairs unseen in training
(their heldout pairs always appeared in training in other
orientations/contexts). Testing the untested composition is the red
team's brief.

## Unchanged

Kill bars RK-A/B/C/D, thresholds (FAIL_K iff COMMIT and heldout < 5/6),
verdict rule, determinism protocol. W3's predicted trace shape is
unchanged (FORM_EXPAND, COMMIT guarded); only the train size (98) and
the predicted heldout (0/6, now on a sound basis) are restated.
