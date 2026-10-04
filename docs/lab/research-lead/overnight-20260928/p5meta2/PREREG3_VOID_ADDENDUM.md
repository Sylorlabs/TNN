# PREREG-3 VOID ADDENDUM (2026-10-04)

F1-F4 implemented (scratch/p5c.zag). After F1-F4 + appended fixes, the run shows:
- IRRELEVANT (fids 34..39) reaches criterion 6/6 at EX=24, PC=6;
- RELATED (fids 16..21) is noise-labelled (fam_build sets FB[3]=1 for fid 16..21),
  so REACH=0, EX=1536; SLOT_REL all zero; STRATT zeros; PC=0 on TRAIN.

Root causes found, in order:
1. gen_ex (scratch p5c.zag:274) computed the label from the family
   DESCRIPTOR slots FB[4+i] (constants per family), not from the example
   features out[...]. Every family therefore emitted a CONSTANT-label stream,
   which is the deep degeneracy behind "constant NOR suffices" (D-B). FIXED:
   s=s+projb(CHKV,dom,gb(CHKV,out,fb(CHKV,FB,4+i))).
2. Condition->fid mapping: RELATED bound to noise families (fids 16..21),
   IRRELEVANT bound to structured families (fids 34..39). Mismatch with the
   frozen semantics of the five conditions (prereg 24c133b42 section 1.x).
   K17's expectation (IRRELEVANT REACH=0) CANNOT be satisfied while bound
   this way.
3. F2 as implemented (zero-mismatch AND both classes observed in-window) is
   UNSATISFIABLE on windows whose labels are momentarily constant -- exactly
   the early rounds of structured families -- so the rule blocks learning
   itself. F2 must be replaced (e.g. non-constant as a function of the
   family's varying bits, or require both classes over the accumulated
   stream) before K17 can be evaluated honestly.

K15=PASS (viol=0, fresh probe consistent: EX=256 RR=0 RA=0 NS=0), F1 works
(AR is now a permutation), F3 splits RA/PC, F4 floors V. But the fixture is
semantically degenerate in ways the prereg did not anticipate: PREREG-3 is
VOID as a test. No meta-learning claim, no bar moved, nothing reinterpreted.
Re-preregister only after a fit-consistency probe demonstrates that (a) the
intended family's true hypothesis is found by search, (b) noise families are
rejected, (c) condition fids match frozen semantics.
