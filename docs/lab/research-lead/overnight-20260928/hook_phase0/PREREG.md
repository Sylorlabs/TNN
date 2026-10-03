# PREREG: HOOK-PHASE0 (frozen)

Non-ledger task. Lane
`docs/lab/research-lead/overnight-20260928/hook_phase0/`, file prefix
`hp_`. Branch `tnn-native-lab`, commits local only, never pushed.

## 1. Task

Implement MUTATION-HOOK Phase 0 (A2.6 + A2.1) as pure infrastructure
on the EPOCH-STRONG substrate. No invention claim is made or tested:
the bars verify substrate mechanics only (counter exactness,
allocator stability across calls, registry round-trip, regression
byte-identity). A2.2, A2.3, A2.4, A2.5 are explicitly out of scope;
A2.2 is gated on Micah's pending EXECUTE placement ruling and is
not implemented here.

## 2. Frozen design answers (before implementation)

**Cell layout (frozen, audited free on the EPOCH-STRONG sources).**
S is 16384 bytes (4096 cells). Highest cell touched by any literal
or computed S access in the es_* sources is 3210 (coverage
contracts); zero_counters touches 7, 900-924. The carved region:

- S cell 932: mutation-event counter (A2.6).
- S cell 933: allocator cursor, byte offset into the region (init 0).
- S bytes [3736, 4120): allocation region, cells 934..1029
  (384 bytes). Base byte 3736 = 934*4.
- S cells 1030..1061: registry, 8 entries x 4 cells
  [cell, tag, ev0, ev1] at 1030+e*4.
- S cell 1062: registry entry count.

**Mutation semantics (frozen).** The counter is per-S-arena state,
not global. `fact_add` bumps S cell 932 iff the fact is stored
(inside the existing `if(n<64)` guard): a full store is not a
mutation. `fact_set_obj` bumps on every call (it has no guard; the
existing unchecked write behavior is unchanged). The bump is the
only base behavioral change; nothing reads cell 932 in the
pre-existing battery, so outputs cannot change.

**Allocator semantics (frozen).** `la_alloc(S,n)`: n<0 returns -1;
size rounded up to 4-byte alignment; if cursor+size > 384 returns -1
with the cursor unchanged; else advances the cursor and returns
3736+cursor_old. The cursor persists in S cell 933 across calls
(zeroed arena start). `la_reg(S,cell,tag,ev0,ev1)`: count<0 treated
as 0; count>=8 returns -1; else writes the entry, bumps the count,
returns the entry index. Meaning tags are learner-chosen i32s; in
this lane the probe uses runtime-derived tags only. The registry is
the honest substrate for learner-chosen semantics, not the semantics
itself: no meaning vocabulary is enumerated here.

**Frozen implementation deltas (additive over es_*).**

hp_base.zag = es_base.zag, except:
(a) fact_add gains one line inside the `if(n<64)` block:
    `set32(S,932*4,get32(S,932*4)+1);`
(b) fact_set_obj gains one line after the write:
    `set32(S,932*4,get32(S,932*4)+1);`
(c) appended section (A2.1), exact code:
```
// ---- HOOK-PHASE0 A2.1: learner-allocated persistent state ----
// Bump allocator over carved S region [3736,4120) (cells 934..1029,
// 384 bytes). Cursor in S cell 933. Sizes round up to 4-byte
// alignment. Returns the byte offset, or -1 on exhaustion (cursor
// unchanged) or negative size. Pure lane-base code: get32/set32,
// arithmetic, branch only.
fn la_alloc(S:[]u8,n:i32)i32 {
  if(n<0){ return -1; }
  let a:i32=n;
  let rem:i32=a-(a/4)*4;
  if(rem!=0){ a=a+(4-rem); }
  let cur:i32=get32(S,933*4);
  if(cur<0){ cur=0; }
  if(cur+a>384){ return -1; }
  set32(S,933*4,cur+a);
  return 3736+cur;
}
// Learner-writable registry: 8 entries x [cell, tag, ev0, ev1] at
// S cells 1030+e*4; count at S cell 1062. Returns the entry index,
// or -1 when full.
fn la_reg(S:[]u8,cell:i32,tag:i32,ev0:i32,ev1:i32)i32 {
  let n:i32=get32(S,1062*4);
  if(n<0){ n=0; }
  if(n>=8){ return -1; }
  let b:i32=1030+n*4;
  set32(S,b*4,cell);
  set32(S,(b+1)*4,tag);
  set32(S,(b+2)*4,ev0);
  set32(S,(b+3)*4,ev1);
  set32(S,1062*4,n+1);
  return n;
}
```
hp_world.zag, hp_module.zag, hp_learn.zag = byte copies of the es_
originals (verified with cmp).

hp_main.zag = es_main.zag plus STAGE HP-P0 inserted immediately
before `o_flush(B,c);`, using the ES battery arena S2 (and S for
the isolation check). Exact stage logic:

1. `let s2c:i32=sg(S2,932); let sc:i32=sg(S,932);`
   Print `HP-MUTCNT s2=<s2c> s=<sc>`.
2. Guard probe: `let A3:[]u8=world_new();`
   `let ps0:i32=get32(A,4); let pr0:i32=get32(A,8);`
   `let po0:i32=get32(A,12);` (fact 0 triple, runtime-derived)
   70x `fact_add(S2,A3,ps0,pr0,po0)`.
   `let c1:i32=sg(S2,932);`
   Print `HP-GUARD c0=<s2c> c1=<c1> delta=<c1-s2c>`.
3. Alloc probe:
   `let a1:i32=la_alloc(S2,16);` write `set32(S2,a1+i*4,s2c+i)`
   for i=0..3.
   `let a2:i32=la_alloc(S2,32);` write `set32(S2,a2+i*4,s2c+100+i)`
   for i=0..7.
   Re-read the a1 block; `rd1=1` iff all 4 match.
   `let a3:i32=la_alloc(S2,400);` (exhaustion)
   `let a4:i32=la_alloc(S2,7);` (alignment)
   `let a5:i32=la_alloc(S2,-5);` (negative size)
   Re-read the a2 block; `rd2=1` iff all 8 match.
   Print `HP-ALLOC a1=<a1> a2=<a2> a3=<a3> a4=<a4> a5=<a5>
   rd1=<rd1> rd2=<rd2>`.
4. Registry probe:
   `let e0:i32=la_reg(S2,a1,r601x,a1,s2c);`
   `let e1:i32=la_reg(S2,a2,r601x,a2,s2c);`
   Read back both entries via sg; `r0=1`/`r1=1` iff all 4 fields
   match.
   Register 6 more entries (indices 2..7), then one more;
   `full` = its return.
   Print `HP-REG e0=<e0> e1=<e1> r0=<r0> r1=<r1> full=<full>`.
5. Print `SUMMARY-HOOKPHASE0 mutcnt=<s2c> alloc_ok=<a>
   reg_ok=<r>` where alloc_ok = (a1==3736 && a2==3752 && a3==-1 &&
   a4==3784 && a5==-1 && rd1==1 && rd2==1), reg_ok = (e0==0 &&
   e1==1 && r0==1 && r1==1 && full==-1).

hp_build.sh mirrors es_build.sh with the hp_ prefix and the pinned
znc path. Runs: `./hp_bin > hp_runN.txt 2> hp_runN.err`, N=1..3.

**Frozen expected values.**

- S2 arena: 6 setup_worldA (336) + 3 setup_worldA2 (168) fact_add
  = 504, plus 2 fact_set_obj (ES-C, ES-E) = 506.
- S arena: 2 setup_worldA (112: S1A, demo_cov_revise) +
  2 setup_worldB (80: demo_cov_revise, S5) = 192.
- HP-MUTCNT line: exactly `HP-MUTCNT s2=506 s=192`.
- Guard probe: 70 calls, 64 stored (n=0..63), 6 rejected (n=64..69):
  HP-GUARD line exactly `HP-GUARD c0=506 c1=570 delta=64`.
- HP-ALLOC line exactly
  `HP-ALLOC a1=3736 a2=3752 a3=-1 a4=3784 a5=-1 rd1=1 rd2=1`.
- HP-REG line exactly `HP-REG e0=0 e1=1 r0=1 r1=1 full=-1`.
- SUMMARY-HOOKPHASE0 line exactly
  `SUMMARY-HOOKPHASE0 mutcnt=506 alloc_ok=1 reg_ok=1`.

## 3. Frozen kill bars

- HP-R1 (regression, additive-only): hp_run1.txt lines 1-146
  byte-identical to es_run1.txt lines 1-146 (Acts 1/2/S10/S11/ES).
- HP-A1 (A2.6 exactness): the HP-MUTCNT line is exactly
  `HP-MUTCNT s2=506 s=192`. Fails if the bump is missing from either
  mutation function, fires twice per event, or is global instead of
  per-arena.
- HP-A2 (guard semantics): the HP-GUARD line is exactly
  `HP-GUARD c0=506 c1=570 delta=64`. Fails if the bump sits outside
  the `if(n<64)` guard (delta would be 70) or fact_set_obj does not
  bump (c0 would be 504).
- HP-A3 (A2.1 allocator): the HP-ALLOC line is exactly
  `HP-ALLOC a1=3736 a2=3752 a3=-1 a4=3784 a5=-1 rd1=1 rd2=1`.
  Fails if the cursor is not persistent across calls (a2/a4 wrong),
  alignment is wrong (a4), exhaustion corrupts the cursor, or blocks
  do not survive later allocations (rd1/rd2).
- HP-A4 (A2.1 registry): the HP-REG line is exactly
  `HP-REG e0=0 e1=1 r0=1 r1=1 full=-1`. Fails if entries do not
  round-trip or the full-table sentinel is wrong.
- HP-A5 (protected core untouched, static audit):
  `cmp hp_world.zag es_world.zag`, `cmp hp_module.zag es_module.zag`,
  `cmp hp_learn.zag es_learn.zag` all identical;
  `grep -c "932\|933\|la_alloc\|la_reg" hp_world.zag hp_module.zag
  hp_learn.zag` is 0;
  the diff hp_base.zag vs es_base.zag contains only the two bump
  lines and the la_alloc/la_reg section;
  no file outside the lane is modified; znc is untouched; the new
  code uses only get32/set32, arithmetic, and branch (the frozen
  computational basis, already available at lane level, not a core
  change).
- HP-H1 (toolchain/hygiene): safebin for all build/run/verify
  commands; pure Zag; pinned znc; prereg committed alone before
  implementation; 3/3 byte-identical runs, stderr empty, exit 0;
  zero em/en dash bytes in authored files; no world literals in new
  executable code (probe triple, patterns, and registry tags are all
  runtime-derived).

## 4. What this does NOT claim

- The counter is researcher-placed infrastructure, not a learner
  invention. A learner reading sg(S,932) is observation, not
  stamping.
- The allocator hands out untyped bytes; assigning semantics is the
  learner's future job. The registry stores associations, not
  meanings.
- Phase 0 changes nothing about what the learner can do with
  mutation events (no dispatch, no hook table, no op bodies).
  Behavioral change arrives no earlier than Phase 1/2.
- 56 facts is a toy world; the counter and allocator are O(1)
  machinery, not scaling results.
