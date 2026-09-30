# PREREG_P12: Developmental-language episode inside the continuing learner (FROZEN)

Date: 2026-09-30 UTC. Worker: Learner Developmental-Language Integration.
Status: FROZEN. Committed alone before any implementation exists.

## Design

P12 appends a developmental-language episode to the composed continuing
learner (revert_learn.zag at dc20745db, copied verbatim, plus the P12
episode). One learner, one 32768-byte state W, one main(), no resets.

The OpScope R1R4 battery (frozen: prereg 51c54e262, results c60bfbe7a) is
run as a developmental episode inside the lifetime:

1. The OpScope learner state (8400 bytes, layout per opscope_learner.zag)
   lives in the slice W[2048..10448]. This region is free: the stress
   store occupies W[64..1648], collateral slots W[2000..2048], the DDES
   ledger W[16384..32768]. The slice is zeroed at P12 start.
2. The frozen R1R4 world is generated in-loop (seed 123456789, 120
   episodes, gen_episodes verbatim from opscope_world.zag). Units and
   targets are recovered by the oracle (world side, excluded from the
   learner source audit, exactly as in the frozen battery).
3. Training: episodes 0..99, one-pass online, through the verbatim
   OpScope learner (learn_keep, baseline check, learn_event from t>=20,
   learn_update; proposal_check + retire_check at seen=20,30,...,100).
4. Frozen test: episodes 100..119 with interpret(), no learning.
5. F1/F2/F4/F5 computed as in the frozen harness. F3 is the shell source
   audit (grep for word literals in the learner functions), reported in
   the result doc.
6. The developmental outcome is persisted as learner state, earned 3x
   immediately to importance 31 (the proven P9/P11 discipline):
   (920,2,1) installed trigger unit; (921,2,0) signature DELETION;
   (922,2,20) frozen test accuracy. Then a 20-item pressure wave
   (700..719, rel 99), then delayed probes: P12_DEV 3/3, P12_FOUNDATION
   8/8, P12_CORR 2/2. STATEHASH P12 emitted.

The OpScope learner functions are copied verbatim from
opscope_learner.zag (minus the five utility functions z_alloc, emit,
i32s, get32, set32, which are textually identical to the ones already in
revert_learn.zag). The world functions are copied verbatim from
opscope_world.zag (minus the same five utils). No learner function is
modified. The gate is the R1R4 gate unchanged.

## Frozen predictions

P12-A (installation): proposal_check installs exactly one operator, at
seen=40 only (installed_now=1 at seen=40; 0 at seen=20,30,50,60,70,80,
90,100). Final OPREC: k=0 trig=1 scope=0 sig=0 sup=12 created=40
active=1. (Trig 1 is the "not" unit per the frozen R1R4 lexicon; the
mapping is stated in the result doc, not in the binary.)

P12-B (frozen test): TEST_ACC 20/20. F1=1 (T1 items 109,110,111 3/3 +
white-box OPREC trig=1 sig=0 created>0 sup>=4). F2=1. F4=1
(t1_full=3, t1_abl=0, acc_abl=17/20, negdrop=3). F5=1 (acc>=16, size
3/3).

P12-C (no regression): P1 through P11 output (all lines through
"STATEHASH P11") is byte-identical to RUN1.txt at dc20745db. The only
new output is the P12 region.

P12-D (persistence): after the 20-item wave, P12_DEV 3/3 (queries
(920,2,1)==1, (921,2,0)==0, (922,2,20)==20), P12_FOUNDATION 8/8,
P12_CORR 2/2.

P12-E (determinism): 3/3 byte-identical runs, exit 0, zero stderr.

## Positional scope restriction (explicit)

The "not" in the R1R4 battery always occurs at utterance position 1
("tak not <color>"). Per OPSCOPE-DISPLACEMENT-LOAD-BEARING (prereg
ae9c3f13e, results 54d3e3ca9), the gate's positional assumption is
load-bearing: a position-0 negator can never install (cs==cb exactly),
and the battery's position-1 "not" is a hidden researcher choice. P12
therefore claims ONLY position-contingent operator installation, not
position-general negation learning. Any statement of the P12 result
without this restriction is a misstatement of the verdict.

## Frozen adversary check: Family A confound (out of scope for P12)

The Family A mid-utterance confound ("tak not grn <color>" NEGs, grn
clearing K=2) is a known, sealed boundary of the R1R4 gate:
GATE-STRESS-FAIL (pilot 82262d90c, prereg 37d4212d, sealed ebd62fe5)
proved the confound installs as a DELETION operator (CONFOUND installed,
TEST_ACC 5/20 vs 20/20). P12 integrates the R1R4 gate VERBATIM; it does
not repair the gate. The confound is therefore predicted to install if
the Family A battery were run, and P12 documents this as OUT OF SCOPE:
gate repair is the job of the behavioral-validation redesign
(opscope_behav lane, active), which replaces position-sensitive count
bars with cross-context behavioral validation as the admission
criterion. P12's frozen adversary check is the regression guard: the
R1R4 battery inside the lifetime must install exactly one operator
(trig=1), replicating the frozen white-box result, i.e. no confound
installs in the R1R4 battery itself. The Family A battery is not re-run
in P12: its outcome is already frozen and sealed, and the gate code is
verbatim, so a re-run would add no information.

## Verdict mapping

LEARNER-DEV-PASS iff: K1 holds (this prereg strictly precedes the
implementation; verified by git merge-base --is-ancestor), AND P12-A
through P12-E all match the frozen predictions above 3/3, AND the
verdict states the positional scope restriction.

LEARNER-DEV-FAIL iff: any of P12-A through P12-E misses its frozen
prediction, or P1-P11 regresses, or the scope restriction is dropped.

Honest ceiling: bounded L2. The candidate graphs and the gate remain
researcher-supplied; the "one continuing learner" goal is approached,
not claimed.
