# PREREG ERRATA 2 -- FREEZE-ARENA-1 (FA1)

Claim block **C563-C566**. Committed ALONE, after ERRATA.md (C560-C562) and
**before the FA1 report and before any result is interpreted**.

No prediction (P1-P11) is withdrawn and no kill bar (K1-K12) is weakened,
relaxed or re-scoped. Each entry below records a defect in an INSTRUMENT,
found by reading the instrument's own output against its own source. Where a
bar's literal text is unsatisfiable as written, the literal text is reported as
FAILED and the corrected control is reported *in addition*, never *instead*.

---

## E5. LK5 never executed: the cross-arm snapshot buffer was per-arm, so the comparison read a zeroed arena

`arm_run(frz,b,c)` allocated its own `CS` (110592 B, the 9-checkpoint
cross-arm snapshot buffer) on entry. `main` calls `arm_run(0,...)` then
`arm_run(1,...)`, so each arm got a freshly zeroed `CS`. The LIVE arm stored
its checkpoints into its own `CS`, which was then unreachable; the FROZEN arm
compared its arena against **its own zeroed `CS`**.

Measured symptom in the pre-fix run:

```
LK5 arm cp 1 0 eq=0 live_n=0 frz_n=52 firstdiff=-1
   ... live_n=0 at all 9 checkpoints
ARMSUM FROZEN ... ckeq_bad=9
```

`live_n=0` is the tell: a real comparison cannot report zero stored facts. So
`ckeq_bad=9` was **9 failures against an empty buffer, not 9 measured arm
divergences**, and K8 was untested rather than failed.

**Fix.** `CS` is allocated once in `main` and threaded into `arm_run` as a
parameter. Nothing else changed. Post-fix:

```
LK5 arm cp 1 0 eq=1 live_n=52  frz_n=52  firstdiff=-1
LK5 arm cp 1 1 eq=1 live_n=79  frz_n=79  firstdiff=-1
LK5 arm cp 1 2 eq=1 live_n=107 frz_n=107 firstdiff=-1
LK5 arm cp 1 3 eq=1 live_n=146 frz_n=146 firstdiff=-1
LK5 arm cp 1 4 eq=1 live_n=346 frz_n=346 firstdiff=-1
LK5 arm cp 1 5 eq=1 live_n=360 frz_n=360 firstdiff=-1
LK5 arm cp 1 7 eq=1 live_n=388 frz_n=388 firstdiff=-1
LK5 arm cp 1 8 eq=1 live_n=414 frz_n=414 firstdiff=-1
LK5 arm cp 1 6 eq=1 live_n=416 frz_n=416 firstdiff=-1
```

K8 now **PASSES on its own literal terms**, and it turns out to be the
strongest comparability evidence in the lane: at all 9 stage-exit checkpoints
the two arms' arenas are equal in count AND element-wise (`firstdiff=-1`), so
LIVE and FROZEN differ in the delivery schedule and in nothing else.

## E6. LK2's `nrel` column was identically zero by construction

`frz_hit2` returned `1-sig`. Its two callers in `frz_memcount` passed
`frz_issig(off)` and `0` respectively, so **both** the `raw` accumulator and
the `sg` accumulator were incremented under the identical condition, and
`raw - sg` -- the returned "non-signature count" -- was 0 for every input.
The `LK2 ... nrel` column was therefore vacuous, and `ARMSUM lk2pre=0
lk2post=0` (the K6 evidence) was true by arithmetic, not by measurement.

**Fix.** `frz_hit2` became a pure predicate (1 = admissible stage-`s`
reference, 0 = not). `frz_memcount` applies `frz_issig` itself and returns
`raw-sg` for real. With the fix, LK2 measured **nonzero** counts at two stages
-- see E7, which is the substantive finding.

## E7. LK2's value-equality test is CONFOUNDED in this world, and the confound is demonstrable from the world definition

With E6 fixed, LK2 reports nonzero memory hits at exactly two stages, in both
arms:

```
LK2 arm st tot sig nrel 0 3 4  0 4 0      (stage D)
LK2 arm st tot sig nrel 0 6 26 0 26 0      (stage G)
```

LK2 tests whether a cell's VALUE equals a relation id attributed to stage `s`.
In this world that test cannot distinguish a relation reference from an
ordinary subject or object id, because the id ranges overlap:

* stage D's relation ids are `108..112` (`frz_rbase(3)=108`, `nrel=5`), and
  stage **B's subjects are `110..115`** -- `lt_add(A,110+i,201,120)` for
  `i<6`, plus explicit `lt_add(A,111,205,160)` and `lt_add(A,112,205,160)`.
* stage G's relation ids are `601..604`, and stage **E's objects are
  `600..609`** -- `lt_add(A,900+j,500+k,600+k)` for `k<10`.

A diagnostic probe recording `(offset, value)` of the hits was added and it
confirms the prediction exactly rather than merely asserting it:

```
LK2C arm st n off=val(sig) 0 3 4 5892=111/0 5988=110/0 6180=112/0 6372=112/0
LK2C arm st n off=val(sig) 0 6 8 7432=601/0 7440=601/0 7448=601/0 7456=601/0
                              7464=601/0 7472=601/0 7528=602/0 7536=602/0
```

The stage-D hits are `110,111,112` and not `108,109` -- exactly the subset of
D's relation range that occurs as a stage-B subject. The stage-G hits are
`601,602` -- stage-E objects. Neither is a stage-D or stage-G relation
reference.

**Correction, in addition to (not instead of) the literal bar.** `frz_rmask`
marks a stage-`s` relation inadmissible when its integer value already occurs
as a subject or object of a triple in the arena at the instant of the test
(stages `0..s-1`), on top of the ERRATA E1 first-occurrence rule. LK2 is then
reported twice per stage:

* `LK2` -- **unfiltered** value test. This is K6's literal text. **K6 FAILS**
  on it: `tot=4` at stage D and `tot=26` at stage G.
* `LK2S` / the `nrel` column -- **collision-excluded**. 0 at all 8 stages in
  both arms.

Both numbers are printed in `fa1_run1.txt`. The report states K6 as failed and
then gives the collision-excluded result as the control that speaks to K6's
intent, so a reader can reject my explanation and accept the failure instead.

This is the second time in this lane that an instrument's silence was
confounded rather than clean (E5, E6). Both were found by reading output
against source, not by inspection.

## E8. NOSTRUCT is a hybrid state and is not a clean structure ablation

PREREG §7 defines `ABL-NOSTRUCT` as "clone of LIFETIME with template store and
bind store zeroed" and §11 makes it the discriminator between a data gain and
a structure gain. As built, it zeroes `LT[200..775]` (template store,
`lt_tb(e)=200+e*48`) and `LT[800..1055]` (bind store, `lt_bb(e)=800+e*16`) --
the names are accurate -- while retaining `L`'s three coverage arrays and the
`specialize_*` indexes built by all 416 episodes, and retaining `LT`'s
functional-arity store and snapshot.

The result is a state that is neither fresh nor lifetime: template lookup
(`lt_tmpl_find`, `lt_tb(i)==s`) finds no template and rebuilds one at query
time, while `L` still routes through episode-derived coverage. Measured
`ANSV NOSTRUCT n=1 v=0` -- a 1-element answer vector where the lifetime
produces 22 -- so the ablation does not produce a *wrong answer* but a
truncated/declined one.

Consequence recorded in advance of reading its interpretation: `ablNoStruct=0`
alone does **not** establish that learner-owned structure is causally
load-bearing for the composition, because the same lane also measures
`FRESH_ARENA` = a **zero-state** learner (no templates, no bindings, no
coverage, no episodes) that answers F **correctly**. The report must
adjudicate on the pair, not on NOSTRUCT alone.