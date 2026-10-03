# PREREG AMENDMENT 1: H-INTENT-UNIFIED8 Red Team (IU8-ADV) (FROZEN)

Date: 2026-09-30 UTC. Committed BEFORE any adversary harness
build, compile, or run.

## Correction

The X-IU8-4 fixture string in the base prereg lists 17 pairs
while the frozen text states "18 pairs" and the frozen
precondition requires TRUE npairs = 18. Count of the string as
written: xab, abc, def, ghi, jkl, mno, pqr, stu, vwx, yza, bcd,
efg, hij, klm, nop, abcde, vwxyz = 17.

Corrected X-IU8-4 V3 fixture (18 pairs, `xab` still first so it
falls inside the 16-cap and em=1):

`xab>bax;abc>cba;def>fed;ghi>ihg;jkl>lkj;mno>onm;pqr>rqp;stu>uts;vwx>xwv;yza>azy;bcd>dcb;efg>gfe;hij>jih;klm>mlk;nop>pon;qrs>srq;abcde>edcba;vwxyz>zyxwv`

The appended pair `qrs>srq` is a reversal like all the others,
so the reverse program still fits every pair, the applied
answer on `xab` is still `bax`, em is still 1, and TRUE npairs
is now 18 > 16 (truncated) as the base prereg requires.

## What does not change

- The attack logic (a both-verbatim pair member that is also
  truncated; pair-class exclusivity).
- The frozen expectations: kind=-2, R10-NEW exactly once in the
  decide section, no older guard text.
- The frozen kill/downgrade criteria.
- Every other attack (X-IU8-1, X-IU8-2, X-IU8-3, X-IU8-5).

This is a clerical count correction, disclosed before any
execution. No observation motivated it.
