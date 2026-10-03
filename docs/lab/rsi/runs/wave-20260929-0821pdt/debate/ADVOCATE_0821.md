# Debate: wave-20260929-0821pdt -- ADVOCATE

Motion M1: ADOPT H-EXP (discriminating-experiment invention) as a
loop-owned bounded capability.

Provenance probe (answered verbatim): What is the provenance of the
artifacts under judgment, and what exactly is new versus inherited?
The prereg (PREREG_H_EXP.md), the six hypothesis fixture files, the
implementation (exp_learn.zag), the seven execution outputs, the run
script, and the red-team report are all NEW this wave, committed
under docs/lab/rsi/runs/wave-20260929-0821pdt/. Inherited and
untouched: the pinned znc toolchain, Micah's frontier dirs
(surveyed read-only), all prior wave records, and every HELD/banked
item. Nothing in this motion re-certifies prior work.

The advocate argues FOR adoption:

1. The frozen bars all passed with exact numbers: K-E1 SELECT [4,2]
   with DIFFVAR pressure on the P1 pair; K-E2 full trace (names, rule
   counts 12/12, candidates 6/36/216, CHECKED 32, PRED1 0 0 1,
   PRED2 0 1 1); K-E3 exact WITHHOLD on the null pair with zero
   SELECT and exit 0; K-E4 byte-identical reruns on P1 and P3;
   K-E5 SELECT [0,4] on the unseen-structure P3 pair.
2. NQ3 is answered with a mechanism, not a memo: no mechanism had
   attempted discriminating-experiment selection before. The
   selection is data-driven (proven by P3 and the renamed-copy run),
   not hardcoded (zero hypothesis names in code, per red-team grep).
3. The withhold behavior is the honesty signal: on vacuous data the
   module refuses to guess. That is the opposite of benchmark gaming.
4. Zero regressions by construction: no existing file modified. The
   prereg amendment was transparent, pre-execution, and semantic-free.
5. The classification is already deflated: bounded structural
   selection toward Level D, explicitly not L3. Adoption does not
   inflate the claim; it banks a real, tested, narrow capability with
   its boundaries attached.

The advocate asks the judge to ADOPT H-EXP as bounded, with H-EXP2
(true-world execution against a hidden law) queued next.
