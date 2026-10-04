# OpScope Tak-Displacement Attack: Preregistration

Committed: 2026-09-30 PDT. Worker: OpScope Tak-Displacement Attacker.
Target: committed learner at c60bfbe7a (OPSCOPE-R1R4-PASS), K=2 prereg 51c54e262,
gate-stress attack at ebd62fe5 (GATE-STRESS-FAIL).

This preregistration is frozen. Sealed family generation and sealed runs
happen only after this commit. The learner is never modified: the sealed
file is copied from ebd62fe5 and only the world (attack instrument) and
harness (driver) regions are edited; the learner functions stay
byte-identical (verified by diff showing changes only in the intended
regions). Everything in pure Zag; zero Python at every step.

## The question

GATE-STRESS-FAIL proved the Position-0 Lemma: a word occurring only at
utterance position 0 is provably immune to DELETION-operator installation
(the zero-parameter gate sees an empty prefix, so in the only episodes
where the word is present the signature prediction is the empty mask,
which never equals T; in episodes where the word is absent the cs and cb
counters move together, so cs > cb is impossible).

This attack turns the lemma on the TRUE negator: every training NEG
episode becomes "not tak <color>" (not at position 0). If "not" can never
install there, the gate's positional assumption is load-bearing and the
battery's "not"-in-position-1 is a hidden researcher choice: negation is
learnable in this setup only via the DELETION operator, and the operator
can only install when the researcher places the negator mid-utterance.

## Sealed family D (displacement)

FAM()=4, SEED()=1004, NEP()=126. The frozen 120-episode battery is shared
with families A-C; only the NEG blocks and the 6 probes vary.

- Phase-1 NEG 24..35: 12x "not tak <color>", colors 0,1 alternating.
  Objects from gen_neg (target avoids the named color); utterance built as
  build_utt(ep,1,0,color_wid(color),0,3). T = {tak} throughout.
- Phase-2 NEG 88..91: 4x "not tak <color>", colors 0,1,0,1. Same form.
- All other episodes (DIRECT/REL/SIZE/train/test) are the frozen battery,
  byte-identical in construction to families A-C.
- Probes 120..122: 3x "not tak red" (the TRAINED surface form), T={tak}.
- Probes 123..125: 3x "not tak grn" (novel color at the trained form;
  grn=wid 4 never appears in any training NEG), T={tak}.

Each family run 3x on seed 1004; byte-identical output across the 3 runs
is required (determinism check, sha256 recorded).

## Static analysis (from committed source, pre-registration)

For "not" (w=1), occurring only at position 0:
- Discovery count bars at seen=30: epc=6 (>=5); recmask={tak}, reclen=1
  (<=1); sup=6 (>=4); mtch: sig_match over suffix {tak,color} vs empty
  prefix gives 6/6 (6*4>=6*3); div: sforms={tak,red,blu}, popcnt=3 (>=2).
  All five count bars clear.
- Zero-parameter gate: in the 6 NEG episodes fi=0, so sp = or_default over
  the empty prefix = 0 != T (T always contains tak). In the other 24
  stored episodes "not" is absent, so sp = p0 and cs/cb move together.
  p0 != T in every training NEG (the DEFAULT mispredicts negation; this
  is the 16/20 pre-operator baseline fact). Hence cs == cb exactly and
  cs > cb is impossible. Gate = 0. "not" can NEVER install. This is a
  source-level proof, not an empirical guess.
- For "tak" (w=0): in NEGs fi=1, sp = recmask(not) = {tak} = T, so cs
  grows by 6 at seen=30; cb counts p0==T over all 30 stored episodes
  (>= the ~24 DIRECT/REL/SIZE episodes). cs < cb at every check. Gate = 0.
- No other word's positional statistics change relative to the baseline
  (only "not" and "tak" swap positions in NEGs), and none installed in
  the baseline. So NO operator installs at any check.

Behavioral consequence: with no operator ever installed and no reground
replay, the DEFAULT records accumulate position-independently and are
identical to the pre-operator baseline's records (the (word,T) multisets
match exactly: same episodes, same targets, only utterance-internal order
differs). interpret() with no operators is or_default, order-independent.
Therefore the test predictions equal the frozen 16/20 pre-operator
baseline item for item.

## Frozen predictions

- P1 (white-box): installed_now=0 at every CHECK line (seen=20..100).
  Final OPREC table: all 8 rows inactive. TRUE_NOT_INSTALLED_WHITEBOX=0
  (no OPREC with trig=1). No operator with any trigger installs.
- P2 (DIAG, mechanism confirmation): at seen=30, w=1 reads
  epc=6 reclen=1 sup=6 mtch=6 div=3, with cs == cb and gate=0; at seen=40,
  w=1 reads epc=12 reclen=1 sup=12 mtch=12 div=3, with cs == cb and
  gate=0. The cs==cb equality is the empirical fingerprint of the proof.
- P3 (behavioral): TEST_ACC=16/20. T1 items (ep 109..111, "tak not grn")
  0/3. Per-item pattern matches the pre-operator baseline.
- P4 (probes): D1 "not tak red" 0/3: the DEFAULT is position-blind (same
  word multiset as the canonical form, same wrong prediction), so the
  trained surface form scores no better than the untrained one.
  D2 "not tak grn" 0/3: no compositional generalization of negation to
  a novel color without an operator.
- P5 (recovery check): F1=0 (t1pass=0, whitebox=0); F4=0 (ablation is a
  no-op: ab_t1 == full_t1, negdrop=0); the VERDICT line reads
  OPSCOPE-R1R4-FAIL (expected: the battery is attacked, as in Family A).

## Honest bars

- LOAD-BEARING: P1-P5 all hold. The gate's positional assumption is
  load-bearing; the battery's position-1 "not" is a hidden researcher
  choice. Negation is learned in this setup only through the DELETION
  operator, which the gate can only install when the researcher puts the
  negator mid-utterance. This bounds OPSCOPE-R1R4-PASS: it is a
  position-contingent L2 result, not position-general learning.
- RECOVERS: any operator installs at any check (especially trig=1), or
  TEST_ACC > 16/20, or T1 > 0. The learner found another route to
  negation; the load-bearing claim is falsified and the recovery
  mechanism becomes the new object of study.
- FAIL (attack execution failure): the 3 runs are not byte-identical,
  the learner region differs from the committed bytes, or the outcome
  matches neither pattern above.

Verdict labels: OPSCOPE-DISPLACEMENT-LOAD-BEARING /
OPSCOPE-DISPLACEMENT-RECOVERS / OPSCOPE-DISPLACEMENT-FAIL.
