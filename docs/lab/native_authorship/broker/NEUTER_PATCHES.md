# Neuter patches (§6) — exact specifications

All patches apply to the frozen D source `chooser.zag` (commit `ab79f1a5c7d`,
SHA-256 `6f8b1db0…`). `dlib.zag` and `R33_NATIVE_IO_V1.zag` are unmodified in
every neuter. Each neuter rebuilds `drvD_<n>.zag` = driver main + patched
`chooser.zag` + frozen `dlib.zag` + frozen battery `carrier.zag`.

## P-feat — constant-fold all 14 features

Location: `d_intake`, immediately after the `d_features(...)` call that fills
`feat` (the 128-byte feature block). Insert:

```zag
d_neuter_feat(feat);
```

where (appended to `chooser.zag`):

```zag
// P-feat neuter: constant-fold every input feature the chooser reads.
fn d_neuter_feat(feat:[]u8) void {
    f_put(feat,0,5);  f_put(feat,1,2);  f_put(feat,2,3);  f_put(feat,3,20);
    f_put(feat,4,1);  f_put(feat,5,2);  f_put(feat,6,2);  f_put(feat,7,2);
    f_put(feat,8,2);  f_put(feat,9,0);  f_put(feat,10,0); f_put(feat,11,1);
    f_put(feat,12,1); f_put(feat,13,0);
    return;
}
```

(`f_put` is the chooser's existing feature-block writer; indices 0–13 =
kind, shape, nwords, nbytes, nlines, lenclass, ans_unit, count_unit,
addr_depth, edge, last_anchor, needle_hit, relative, anchor_third.)

## P-def — override every choice to candidate 3 post-deliberation

Location: `d_intake`, the deliberation call site (exactly one occurrence):

```zag
    let w:i64=d_deliberate(qid,q,t,out,atp,scr,feat,ebuf,&rule);
```
becomes:
```zag
    let w:i64=d_deliberate(qid,q,t,out,atp,scr,feat,ebuf,&rule);
    w=3; // P-def neuter: override deliberated choice to candidate 3 (WORD>CHAR)
```

Deliberation (features, evidence, eliminations, `# D-CHOICE` trace) runs
unchanged; only the executed candidate is forced.

## P-trace — blank the trace emitter

In `chooser.zag`, insert an early `return;` as the first statement of each of:
`emit_feat`, `emit_ev`, `emit_elim`, and the `# D-CHOICE` emission block, and the
`# D-REFUSE` diagnostic block in `d_intake`. `emit_choice`/`emit_resline` (in
`dlib.zag`, the choice/result record shared with the L arm) are untouched.
Result: zero `# D-` lines; choice execution, answers, and exit codes unchanged
(verified 26/26 behaviorally identical).
