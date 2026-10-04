# ERRATA M4c (P1-MECHANISM) -- harness-side declaration fix, committed ALONE

Lane `p1_mech/`, branch `lane/p1mech`. Parents: addendum `a28192a1b`
(C619-C630), implementation v1 `323832ae9` (C610-C618).
No M4 number changes in this file. **No kill bar is moved, and no learner code
is touched.** Two `m4_decl` cases are corrected, both derived from the frozen
executor and cross-checked by the memory-free oracle.

---

## E6. `m4_decl(8)` IS WRONG. The `[1,1]` reading of a kind-2 fan-in is a misreading.

`m4_world.zag` carried this comment at `m4_decl`:

> `apply_kind1` substitutes exactly ONE subject -- the FIRST element of the
> source need's output list (`c8_learn.zag:399-424`, ss=0) -- so the last need
> verifies a single triple and answers `[1,1]`, not the 2-subject list an
> unexamined reading of "fan-in" suggests.

**That misreads the frozen code twice.**

1. `apply_kind1` (`c8_learn.zag:399-410`) handles **kind-1** links, which are
   *scalar copies*. The fan-in substitution for a need reached by a **kind-2**
   link is not in `apply_kind1` at all.
2. The kind-2 fan-in lives in `compose_iter` (`c8_learn.zag:703-722`):
   `let src:i32=fanin_src(G,ni);` ... `let nsub:i32=get32(OUTS,src*160);` then
   `while(k<nsub){ let sub:i32=get32(OUTS,src*160+4+k*4); w_to_chain(W,ni,tmpc,sub);
   ... if(vv2==1){ set32(OUTS,ni*160+4+npass*4,sub); npass=npass+1; } }` and finally
   `set32(OUTS,ni*160,npass);`. It iterates over **every** element of the
   source's output list and appends **every** passing subject. `ss=0` appears
   nowhere on this path.

So a VERIFY need with a kind-2 source answers the **list of passing subjects**,
not `[1,1]`.

**Independent confirmation, already in the certified run.** For goal 8 (the
four-need chain whose last need is a fan-in) the run prints three vectors:

```
ANSV ANS_G3F_AGED n=44 ... 16 subj | 12 subj | 8 subj | 4,100,101,102,103
ANSV OR_G3F       n=44 ... 16 subj | 12 subj | 8 subj | 4,100,101,102,103
ANSV DECL_G3F     n=41 ... 16 subj | 12 subj | 8 subj | 1,1
```

The **learner** and the **memory-free oracle**, which share no code, produce the
identical 44-element vector; the hand-written declaration is the odd one out.
`oracle=1` in the `QG` row was computed as "oracle agrees with the declaration",
so it was reporting agreement with a wrong declaration and therefore certified
the wrong answer -- a defect in the cross-check, not in the oracle.

**Correction.** `m4_decl(8)`'s last group becomes the 4-subject list
`m4_appn(X,4,0)` followed by `m4_appc(X,1)`, i.e. n = 17+13+9+5+2 = **46**...

correction to that arithmetic, from the measured vector: the measured vector is
n=44 = 17+13+9+5, so the final need contributes **5** elements and there is no
`[1,1]` group at all. `m4_decl(8)` becomes
`m4_appn(X,16,0); m4_appn(X,12,0); m4_appn(X,8,0); m4_appn(X,4,0);` -- n=44.

## E7. `m4_decl(6)` IS WRONG FOR THE SAME REASON, and the 5-need oracle was RIGHT.

`m4_decl(6)` declared the fourth group as a 2-subject list. The memory-free
oracle produced a 4-subject list for the same need. Under E6's derivation the
**oracle** is right: the fourth need of the five-need chain has the identical
local structure to the fourth need of `m4_goal4f` (`nf=4`, fields
`[1,0,r3,o3]`, one incoming kind-2 link from need 2), so both must answer the 4
passing subjects `100..103`. `m4_decl(6)` becomes
`m4_appn(X,16,0); m4_appn(X,12,0); m4_appn(X,8,0); m4_appn(X,4,0); m4_appc(X,1);`
-- n=46, which is exactly the oracle's measured vector
(`ORACLE_G2NF n=46 ... 4,100,101,102,103,1,1`).

## E8. WHAT THIS DOES NOT TOUCH

* **The crux is untouched.** The hole goal is `m4_goal(2)`, a four-need chain
  ending in a **COUNT** need. Its declaration and its oracle agree exactly
  (`15` subjects vs the true `16`), which is what K-GEN1/K-GEN4 rest on. Neither
  corrected case involves a COUNT-terminated chain.
* **K-LOC8 is untouched and is now the reason the five-need row cannot be a
  correctness claim.** The frozen plan record is 56 B = `8 + 4*12`
  (`c8_learn.zag:578-601`) and `plan_new` writes `8 + p*12` for `p < nn`, so a
  five-need goal writes 4 bytes **past its own slot** -- measured, the 4 bytes
  after slot 0 go `0 -> 4` across the five-need query and are unchanged by the
  four-need control. A goal the frozen core cannot represent is not evidence
  about age, so **K-I3 stays VOID** even with the declaration corrected.
* Both corrections make the harness **more** self-consistent: the learner, the
  independent oracle and the declaration now coincide on both shapes, where
  before the cross-check was agreeing with a wrong declaration.
* The prior `K4 G3F ok=0` FAIL is expected to clear, and `K3b` is expected to
  fall from 1 row to 0. Both are consequences of E6/E7 and are reported as such
  rather than as passes earned by moving a bar.