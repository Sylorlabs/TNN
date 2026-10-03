# AUDIT.md -- Operand encode/decode site audit (frozen base)

Scope: the frozen base used by SCALING-5000-FIXED, i.e.
`docs/lab/research-lead/overnight-20260928/scaling_5000_fixed/s6_base.zag`
(1495 lines, tnn2.zag lineage), plus its build companions `s6_patch.zag`
and `s6_driver.zag`.

Method: grep for `10000`, `res_op`, `fr_get`, `fr_set`, `t2_guard`,
`t2_set`, `t2_mov`, `t2_inc`, `t2_dec`, `t2_jnz`, and all `ns(W,*,0,10[1234])`
executable-cell constructions. Repo-wide grep for the `10000` operand
convention outside `docs/lab/research-lead/overnight-20260928/` found no
other operand-encoding uses (remaining hits are fact-id thresholds and
loop bounds in unrelated experiments).

## Defect

Node ids and frame-slot references share one integer namespace. `res_op`
decodes any `op >= 10000` as frame-slot `op-10000`. Node ids reach 10000
at ~1400 decoys, so valid node operands are misinterpreted as frame
references. This caused SCALING-5000-FIXED K1 FAIL (canonical, preserved).

Historical note: a stale comment in the base (line 313) says "Root field4
is the output operand (1000+slot)", and test t_c6 (line 873-874) writes
`ns(W,root,4,1000)`. Both are fossils of an older 1000+slot convention.
The threshold has already been moved once (1000 -> 10000) when node ids
outgrew it. This is exactly the magic-threshold treadmill Micah's ruling
forbids repeating. The fix must make NODE vs FRAME structurally
distinguishable, not move the constant again.

## Decoders (contain the 10000 threshold)

D1. `res_op` (line 181-184):
```
fn res_op(W:[]u8,f:i32,op:i32)i32 {
  if(op>=10000){return fr_get(W,f,op-10000);}
  if(op>=0){return ng(W,op,20);}
  return 0;
}
```
The single choke point for operand VALUE reads. Callers: execute tag 101
(source operand), execute tag 102 (both operands), exec_val, t2_exec
(output operand = root field4).

D2. `execute` tag 101 = SET/MOV (lines 199-202):
```
let d:i32=ng(W,cur,4); let sr:i32=ng(W,cur,8);
if(d<10000){return -999999;}
fr_set(W,fr,d-10000,res_op(W,fr,sr)); nx=seq_nx(W,cur);
```
Destination must be a frame ref; rejects node-id (and negative) dests.

D3. `execute` tag 102 = BRANCHEQ/guard (lines 204-205):
```
let a:i32=res_op(W,fr,ng(W,cur,4)); let b:i32=res_op(W,fr,ng(W,cur,8));
```
No literal threshold; delegates to res_op.

D4. `execute` tag 103 = INC (lines 207-208):
```
let s:i32=ng(W,cur,4); if(s<10000){return -999999;}
fr_set(W,fr,s-10000,fr_get(W,fr,s-10000)+1); nx=seq_nx(W,cur);
```

D5. `execute` tag 104 = DEC (lines 210-211): same shape as D4 with -1.

## Encoders (write 10000+slot)

E1. `t2_guard` (line 327-330): `ns(W,g,4,10000+slot)` (field4 = frame ref);
    field8 = litx (literal NODE id, unaffected).
E2. `t2_set` (line 331-334): `ns(W,s,4,10000+slot)`; field8 = lity (node id).
E3. `t2_mov` (line 335-338): `ns(W,c,4,10000+dst); ns(W,c,8,10000+src)`
    (both operands frame refs).
E4. `t2_inc` (line 339-342): `ns(W,c,4,10000+slot)`.

No other `10000+` writes exist in the base. (Line 257 `bb=1000000` and
line 1297 `guard<10000` are unrelated: a large-number init and a loop
bound.)

## Operand readers without a threshold (implicated, reviewed)

R1. `t2_sig` (lines 459-462): reads field8 of tag 101/102 cells,
    `if(ln>=0 && ln<65536){lv=ng(W,ln,20);}`. Treats nonneg field8 as a
    node id. Under the old encoding this MISREAD t2_mov field8
    (10000+src) as a node id (latent bug: dereferenced an unrelated
    node). Under the new sign-based encoding a frame ref is negative and
    is correctly skipped by the existing `ln>=0` guard. No code change
    needed; the only frozen caller is t_t2_revise on chain graphs (no MOV
    cells), so no frozen signature changes. Documented as an intended
    correctness improvement, verified by K6.
R2. `exec_val` (line 220) and `t2_exec` (line 398):
    `res_op(W,fr,ng(W,root,4))`. Delegate to res_op; no change needed.

## Confirmed absent

- `t2_dec`, `t2_jnz`: no such functions exist in this base (DEC is inline
  tag 104 in `execute`; the 4-op ISA here is MOVE/BRANCHEQ/INC/DEC with no
  JNZ opcode). Repo-wide search of docs/lab/research-lead/ found no
  `fn t2_dec` / `fn t2_jnz` definitions.
- `s6_patch.zag` (FI1-FI5 FACT index): no operand encode/decode; the two
  `1000000` hits are edge timestamps, the `100000` hits are loop bounds.
- `s6_driver.zag`: no `10000`, `res_op`, `fr_get`/`fr_set` references.

## Tag-102 overload (reviewed, out of scope)

`r_mk_guide` (line 1278) and test code (line 1423) build tag-102 nodes as
learner-state guide nodes for the ACT machinery (field4=anchor,
field8=goal are plain node ids). These never enter `execute`/`res_op`:
both `execute` callers (exec_val, t2_exec) only run roots built by
`t2_asm_*` or promoted MAP graphs, and `t2_sig` only walks MAP roots.
No change needed; no interaction with the operand namespace.

## Fossil test (documented, not fixed)

t_c6 (lines 871-879) writes `ns(W,root,4,1000)` (field4=1000) on a tag-101
cell, a leftover of the older 1000+slot convention. Under the old
10000-encoding the dest check `d<10000` rejects it, so t_c6 already fails
on the old base; under the new sign encoding `d>=0` likewise rejects it.
Identical behavior old vs new. K6 verifies this empirically rather than
assuming it.

## Nonnegativity guarantee (design basis)

`alloc_node` returns node ids in [2, 65536) or -1 on failure; -1 is never
stored as an operand (all encoders check `alloc_node` results for <0).
Frame slots are small nonneg ints. Therefore every legitimately produced
operand is either >= 0 (node id) or will be < 0 (frame ref) under the new
encoding, and the sign bit separates the two kinds with no threshold
constant. NN() = 65536 is the frozen allocation ceiling and is used only
as a node-id validity bound (consistent with the existing `ln<65536`
check in t2_sig), never as a namespace discriminator.
