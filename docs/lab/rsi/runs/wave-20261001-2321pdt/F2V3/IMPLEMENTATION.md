# IMPLEMENTATION: F2 v4 (depth-9 candidate)

Date: 2026-10-01. Lane: F2V3 (wave-20261001-2321pdt).
Frozen prereg: PREREG_F2V4.md (commit 5e4e56a5f), committed ALONE
before any implementation file existed. Commit-order self-check:
- prereg commit 5e4e56a5f is an ancestor of HEAD (verified via
  git merge-base --is-ancestor);
- the lane dir had zero commits between 5e4e56a5f and the
  implementation commit b5fcf9ae3;
- no implementation file existed at prereg freeze time.
Ordering is verifiable from the commit graph.

## Source change (exact)

`f2v4_learner.zag` is `f2v3_learner.zag` with exactly the v4 prereg
section-3 change. `diff` against the v3 file shows only:

1. `L_D2()` returns 9 instead of 8 (the single mechanism change).
2. Discrimination sequence buffers `dsk`/`dsv`: `z_alloc(8)` -> 10.
3. Discrimination ledger record: `reclen` 48+nhyp -> 50+nhyp; the
   sequence loop `while(i<8)` -> `while(i<9)`; offsets reshifted
   (kinds at base+16..24, vars at base+25..33, predi 34, predj 38,
   actual 42, nkilled 46, killed at base+50).
4. Comment updates only (no logic comments changed).

Diff statistics: 8 hunks, all within the bound/buffer/ledger scope.
No change to L_pairdiff, the restricted alphabet, the
exactly-one-OBSERVE rule, first-hit selection order, the standard
depth-6 scan, candidate generation, the goal planner, the random
control, or any world interface.

Source audit for K4-R2 (construction, not enumeration): the learner
contains no complete experiment, distinguishing sequence, or goal plan
as a literal. The only depth-9-length content in source is buffer
capacity. The SUFFIX protocol is programmatically constructed. The
hand-derived witness sequence from the depth-9 proof (prereg section
2.1) does not appear in source.

## Build

`build.sh` concatenates learner + world and compiles with the pinned
znc (via safebin PATH) in /tmp. Compiler warnings only (pre-existing
in the carried-over code); binaries written. Pure Zag throughout
(Step 0 in NAMECHECK.md).

Binary sha256 (build.sh sealed mode):
- /tmp/f2v4_a: 9c1d44b85eeeae7be26b3b1777e26c09bdca4dc2307180be476fd3991a9cdfe7
- /tmp/f2v4_c2: bdb8f9fc5e6ddad2c2cf9f98ca911debaffe654e70296925d5019ca9b70a7783

Binary sha256 (regression mode, 2021pdt worlds):
- /tmp/f2v4_reg_a: 07d5f78d054186c28302a31e1920e551cb6b829aa7de7c5f0b2a8e6e2937af41
- /tmp/f2v4_reg_c: 6551a304bb18cb8d1327607520bf3cf7642aeb48c7c97c350b4d2147de2e50d6

## Build-verify on regression worlds (2021pdt, retired as test worlds)

### 2021pdt World A (/tmp/f2v4_reg_a): PASS
PROGRAM_ALL_BARS_PASS (mask 63). NHYP 6 >= 2; true hypothesis survives,
nalive=1; GOAL_REAL 1; RANDOM 0/20; OBS_USED 6; K4-R6 PASS. No
regression on the easy world.

### 2021pdt World C-prime (/tmp/f2v4_reg_c): the v3 killing instance
POSITIVE CONTROL. The v3 binary exhausted with SURVIVORS [80,82]
(nalive=2, D2CERT). The v4 binary's discrimination phase discovered:
- round 6, pair (78,79): 9-primitive [SX,SJ,W,CJ,W,W,W,W,OX], killed [78];
- round 7, pair (79,80): 8-primitive [SX,SJ,W,W,W,W,W,OX], killed [79];
- round 8, pair (80,81): 8-primitive [SX,SK,W,W,W,W,W,OX], killed [81,83];
- round 9, pair (80,82): 9-primitive [SX,SJ,W,SK,W,W,W,W,OX],
  pred_i=[1] pred_j=[0] actual=[0], killed [80].
SURVIVORS [82] (the true hypothesis: X rule (Y2,d2,J=1), Y1 (X,3,J=1),
Y2 (X,2,K=1)); w_verify ty1=1 ty2=2; K4-R4 PASS. GOAL_REAL_C2 1
(twelve SUFFIX observations all 1); RANDOM 0/20; K4-R6 PASS;
PROGRAM_ALL_BARS_PASS. The exact crossed-context pair that killed v3
is resolved by learner-discovered evidence at the new bound, and the
found 9-primitive sequence [SX,SJ,W,SK,W,W,W,W,OX] matches the
hand-derived minimal witness form from the depth-9 proof (prereg
section 2.1): cause arrangement at t-5, discriminating context at t-3,
five WAITs, one OBSERVE. The buffer resize was load-bearing: a
9-primitive sequence could not even be recorded at the v3 capacity.

## Architecture accounting (implementation step)

- Cognition source lines added: 0 (the change is one bound constant
  plus buffer-capacity resizes; the diff is 8 hunks in scope).
- New hardcoded semantic cases: 0.
- New modes / bridges / routers: 0.
- New task-specific handlers: 0.
- New learner-state structures: 0 (ledger record capacity only).
- The sealed worlds are authored test substrate, not cognition.
