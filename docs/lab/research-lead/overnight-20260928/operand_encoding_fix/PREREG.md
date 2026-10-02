# PREREG.md -- Operand-encoding fix (new base revision)

Frozen before implementation. This prereg's first commit strictly precedes
any implementation commit. Implements Micah's 2026-10-02 ruling on the
frozen-base operand-encoding defect.

## Background (canonical, preserved)

SCALING-5000-FIXED: FAIL remains the canonical result for the OLD frozen
build (`scaling_5000_fixed/s6_base.zag`). Root cause: node ids and
frame-slot references shared one integer namespace; `res_op` decoded any
`op >= 10000` as frame-slot `op-10000`, colliding with node ids >= 10000.
The 13,107x scan reduction is exploratory evidence that the index idea
scales; the correctness failure is in operand representation, not the
index algorithm. Do not claim 5000-MAP scaling canonical until K3 passes
on the revised build.

## Frozen design: sign-tagged operand encoding

Operands are i32 values in executable-cell fields (field4/field8 of tag
101-104 cells; root field4 output operand). New invariant:

- `op >= 0`              -> NODE operand: node id op.
- `op < 0`               -> FRAME operand: frame slot s = -1 - op,
                           i.e. slot s encodes as op = -1 - s
                           (slot 0 -> -1, slot 1 -> -2, ...).
- `op >= 65536` in a NODE position -> invalid; `res_op` returns the
  -999999 error sentinel (65536 = NN(), the frozen allocation ceiling,
  used ONLY as a validity bound, never as a namespace discriminator;
  consistent with the existing `ln<65536` check in t2_sig).

Unambiguity proof: for any i32 op, exactly one of `op < 0` / `0 <= op`
holds. If `op < 0`, `s = -1 - op >= 0` is the unique slot with
`-1 - s = op`. If `0 <= op < 65536`, op is the unique node id. No
threshold constant participates in the kind decision; the sign bit is the
tag. Node-id nonnegativity is guaranteed by `alloc_node` (returns
[2,65536) or -1; -1 never stored as an operand). This satisfies the ruling:
no moved magic constant, structurally/tagged distinguishable.

## Frozen code changes (complete per AUDIT.md; nothing else changes)

1. `res_op`:
```
fn res_op(W:[]u8,f:i32,op:i32)i32 {
  if(op<0){return fr_get(W,f,-1-op);}
  if(op>=65536){return -999999;}
  return ng(W,op,20);
}
```
2. `execute` tag 101 (SET/MOV): `if(d>=0){return -999999;}`
   then `fr_set(W,fr,-1-d,res_op(W,fr,sr));`
3. `execute` tag 102 (BRANCHEQ): unchanged (delegates to res_op).
4. `execute` tag 103 (INC): `if(s>=0){return -999999;}`
   then `fr_set(W,fr,-1-s,fr_get(W,fr,-1-s)+1);`
5. `execute` tag 104 (DEC): same shape as INC with -1.
6. Encoders: `10000+slot` -> `-1-slot` in `t2_guard` (field4),
   `t2_set` (field4), `t2_mov` (field4, field8), `t2_inc` (field4).
7. `t2_sig`: UNCHANGED. Its existing `ln>=0` guard now correctly skips
   frame refs (previously misread t2_mov's 10000+src as a node id).
8. Stale comment at old line 313 ("1000+slot") rewritten to describe the
   sign encoding. Header comment records the new base revision and this
   prereg hash. `t_c6` fossil left as-is (fails identically old/new).

New file: `operand_encoding_fix/oe_base.zag` (copy of s6_base.zag with
exactly the changes above). Old files untouched. Build: oe_full.zag =
oe_base.zag + s6_patch.zag (verbatim) + oe_driver.zag (verbatim copy of
s6_driver.zag). Pure Zag. Safebin. Pinned znc.

## Frozen kill bars

- K1 audit completeness: every decode/encode site from AUDIT.md changed;
  grep for `10000` in oe_base.zag returns only the two unrelated hits
  (line-257-class large-number init, line-1297-class loop bound); no
  `op>=10000` / `10000+slot` / `<10000` operand patterns remain.
- K2 regression: 100 / 500 / 1000 MAP worlds, chain/count/sum queries,
  3/3 byte-identical runs each, all queries ok=1 with correct answers.
- K3 5000-MAP: the SCALING-5000-FIXED protocol rerun on the revised
  build: build-order invariance (ok=1 for all queries in all 3 orders)
  AND indexed scan reduction >= 1000x (mode-1 scan <= 32, order-D mode-0
  scan >= 25000), 3/3 byte-identical. Both must pass; correctness and
  scan reduction are separate bars.
- K4 boundaries: (a) node ids 9990..10010 used as literal operands decode
  as NODE (correct values, no frame confusion); (b) frame slots 0..3
  round-trip through encode/execute/decode; (c) node id 65535 as operand
  decodes as NODE; (d) operand 65536 and 100000000 -> -999999, no panic;
  (e) old-collision probe: literal node id 14121 (the exact failing
  operand from the K1 FAIL diagnosis) now resolves via ng, not fr_get.
- K5 red team: malformed/cyclic/stale operands (negative dest where node
  expected and vice versa, huge frame slot, stale/evicted node id, zero
  operand, i32::MIN operand) -> executor returns -999999 or defined
  values; zero panics, zero hangs (60s timeout each), zero build fails.
- K6 no semantic regression: the base's own battery (`run_all`: C1..C15,
  A1..A6, P1..P7, DV, XCAP, R-PACT1..6, T2-*) run on old s6_full binary
  vs new oe_full binary produce identical per-test PASS/FAIL vectors;
  t_t2_revise passes on the new build (signature diff still detected).

## Verdict rule

BUILD-PASS iff K1..K6 all pass as frozen. Any bar fails -> BUILD-FAIL,
root-cause, fresh prereg for the next attempt. No weakening or
reinterpretation of bars after results. VOID on any prereg-order
violation or forbidden-interpreter invocation (that wave PROCESS-FAIL).
