# Addendum 1 to PREREG_L3B_V2_ADV: corrected D-REVISIT prediction

Parent prereg: PREREG_L3B_V2_ADV.md, frozen alone at 42538c6b6.
This addendum is committed ALONE and strictly BEFORE the corrected run.

## The error

Run 1 (verdict L3B-V2-ADV-FAIL, hand-derivation error) observed
`ADV-FAMD done creates=8 dispatches=1 recallok=1/1 revisit=2`
against the frozen prediction `revisit 3/3`.

The prediction was my arithmetic error, not a mechanism deviation.
In the frozen step() source (7a1d3265d, copied verbatim into the attack),
the tally increment lives ONLY in the direct-prediction branch:

    if(ok==1){
      if(tally==1){is(cnt,0,ig(cnt,0)+1);}
      ...
    }else{
      let disp:i32=0;
      ...
      if(disp==1){
        is(consec,0,0);      // dispatch resets the counter but never tallies
      }else{
      ...

A successful try_dispatch sets disp=1, never ok=1, so a dispatch episode
never increments cnt0. Family D revisit is: n=21 dispatch (no tally),
n=22 direct hit (tally 1), n=23 direct hit (tally 2). Correct prediction: 2/3.

Independent corroboration: the builder's own FAM2 run (L3B_V2_RAW.txt)
reports `final=1` from its 2-episode revisit (dispatch + 1 follow-up),
the same no-tally-on-dispatch semantics.

## The correction

D-REVISIT3 is amended from `ig(cnt,0)==3` to `ig(cnt,0)==2`.
Nothing else changes. The mechanism, the sealed families, the other four
primary bars, the dispatch signatures, the eight keys, and the E boundary
probe are untouched. The run-1 FAIL verdict stands as recorded; this
addendum governs run 2 only.

## Why this is a correction, not a moved bar

The corrected value is derived from the frozen source alone (the tally
branch quoted above) and corroborated by the builder's independent run.
It does not weaken any mechanism honesty requirement: creates=8,
dispatches=1, recallok=1/1, the from=8 to=1 on=21 signature, and the
no-9th-version requirement are all unchanged and were all met in run 1.
