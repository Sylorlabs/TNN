# AUDIT.md -- Operand Namespace Defect: Complete Site Inventory

Worker: operand-namespace fix workstream. Date: 2026-10-02.
Toolchain: safebin PATH, `which python3` / `which python` return nothing.
Pure Zag. Local only, never pushed.

## 0. Scope and provenance

Frozen base under repair: `docs/lab/research-lead/overnight-20260928/scaling_5000_fixed/s6_base.zag`
(1495 lines). Verified byte-identical to lines 1..1495 of the committed
`docs/lab/research-lead/overnight-20260928/scaling_5000/s5_full.zag`
(`cmp` clean; sha256 `6797e6aeb7e642a5c3ce5875831bff31afb5691e03df96abcc248b9235a4a5bd`).
This is the exact base behind the C299 SCALING-5000-FIXED-FAIL verdict.

The defect (C299 root cause): node ids and frame-slot references share one
integer namespace inside 4-op ISA cell operand fields (field 4 and field 8 of
tag 101/102/103/104 cells). Encoders tag frame refs as `10000+slot`; decoders
treat any `op >= 10000` as a frame-slot reference. Node ids reach 10000 at
roughly 1400 decoys, colliding with the frame-ref tag range.

Companion files checked and cleared: `s6_patch.zag` (FI1-FI5 FACT index; no
ISA operand encode/decode; its `10000`/`100000` literals are bid values and
walk limits) and `s6_driver.zag` (two operand-adjacent sites, listed below).

## 1. Encoder sites (write operands into tag 101..104 cells)

| # | Site | File:line | Writes |
|---|------|-----------|--------|
| E1 | `t2_guard` | s6_base.zag:327-330 | f4 = `10000+slot` (frame ref), f8 = litx (node id) |
| E2 | `t2_set` | s6_base.zag:331-334 | f4 = `10000+slot` (frame ref), f8 = lity (node id) |
| E3 | `t2_mov` | s6_base.zag:335-338 | f4 = `10000+dst` (frame ref), f8 = `10000+src` (frame ref) |
| E4 | `t2_inc` | s6_base.zag:339-342 | f4 = `10000+slot` (frame ref) |
| E5 | `t_c6` self-test | s6_base.zag:871-879 | f4 = `1000` hardcoded, f8 = literal node id. DEAD CODE: `run_all()` is defined but never called anywhere in base/patch/driver (grep for `run_all()` has one hit: the definition). Not on the s6 verification path. |
| E6 | `t2_revise` rollback | s6_base.zag:665 | `ns(W,stale,0,101)` retags the stale cell back to 101; operand fields preserved, not rewritten. Must keep working under the new encoding (it does: fields untouched). |
| E7 | driver `s6_mkbroken` | s6_driver.zag:37 | `ns(W,stcell,0,103)` retags a t2_set cell 101->103 to make a broken decoy; f4 (`10000+slot`) preserved and then decoded by the INC path. The fix must keep SET/INC destination-slot decoding in agreement (it does: one shared decode rule). |

No other constructors of tag 101..104 cells exist. Verified by grep for
`ns(W,*,0,10[1234])` across base/patch/driver: only the sites above plus
`r_mk_guide` (s6_base.zag:1278, guide nodes, see non-sites) and a test-only
retag (s6_base.zag:1423, guides, never executed).

## 2. Decoder sites (read operands from tag 101..104 cells)

| # | Site | File:line | Current rule |
|---|------|-----------|--------------|
| D1 | `res_op` | s6_base.zag:181-185 | `op>=10000` -> frame slot `op-10000`; `op>=0` -> node value `ng(W,op,20)`; else `0`. THE colliding decoder from C299. |
| D2 | `execute` tag 101 (SET) | s6_base.zag:199-202 | `d=f4`; `d<10000` -> fail `-999999`; `fr_set(fr, d-10000, res_op(fr, sr))`; `sr=f8` via `res_op`. |
| D3 | `execute` tag 102 (GUARD) | s6_base.zag:203-205 | `a=res_op(fr,f4)`, `b=res_op(fr,f8)`; branch on `a==b`. |
| D4 | `execute` tag 103 (INC) | s6_base.zag:206-208 | `s=f4`; `s<10000` -> fail; `fr_set(fr, s-10000, fr_get(fr,s-10000)+1)`. |
| D5 | `execute` tag 104 (DEC) | s6_base.zag:209-211 | `s2=f4`; `s2<10000` -> fail; `fr_set(fr, s2-10000, fr_get(fr,s2-10000)-1)`. Decoder exists; no encoder constructs tag-104 cells (see section 4). |
| D6 | `exec_val` | s6_base.zag:218-221 | `res_op(fr, ng(W,root,4))` after successful `execute`. |
| D7 | `t2_exec` | s6_base.zag:393-398 | fresh frame, `execute`, then `res_op(fr, ng(W,root,4))`. Used by `t2_try_verify` (s6_base.zag:437), the s6 query verify path. |
| D8 | `t2_sig` | s6_base.zag:451-468 | reads f8 of 101/102 cells as a node id (`ln>=0 && ln<65536`, then `ng(W,ln,20)`). Only reached from `t_t2_revise`, which is dead test code (not called by the driver). Noted for completeness; behavior on mov cells (f8 = frame ref) changes from garbage-read to 0 under either candidate encoding, strictly cleaner. |
| D9 | driver `s6_chaincheck` | s6_driver.zag:50-78 | reads f8 of 102/101 cells as a node id (`ln>=2 && ln<65536`, then `ng(W,ln,20)`); checks literal sequence. Frame refs never appear in f8 of guard/set cells, so the new encoding does not affect this check. |

## 3. Non-sites (checked, explicitly not operand encode/decode)

- `r_mk_guide` (s6_base.zag:1277-1279) builds tag-102 cells with f4=anchor,
  f8=goal (raw node ids), but these are ACT guide nodes, never passed to
  `execute`/`res_op`/`exec_val`/`t2_exec` (`ev_act` selects via edges and
  reads `ng(W,best,20)`). Different namespace (guide type tag), unaffected.
- `fr_get`/`fr_set` (s6_base.zag:168-179) take raw slot numbers, not encoded
  operands. Unchanged by the fix.
- s6_base.zag:257 `bb=1000000` (bid sentinel) and s6_base.zag:1297
  `guard<10000` (eviction loop counter): unrelated numeric literals.
- `t2_lit` (s6_base.zag:318-321) creates literal nodes; their ids are plain
  node ids, no frame encoding involved.
- `t2_asm_chain` / `t2_asm_count` / `t2_asm_sum` assemble graphs only through
  E1..E4. `t2_chain`, `promote_graph`, `ev_query`, `ev_teach` do not read ISA
  operand fields (verified by field-4/field-8 read grep across base and patch).

## 4. Named-but-absent functions

`t2_dec` and `t2_jnz` do not exist anywhere in the repository. Repo-wide grep
for `fn t2_dec` / `fn t2_jnz` across all `*.zag` returned zero hits. The 4-op
ISA's DEC opcode (tag 104) has a decoder (D5) but no encoder constructor in
this base. The audit site list above is complete for the frozen base; the
prereg will cover D5 anyway so the DEC path follows the same invariant.

## 5. Allocator facts (input to the prereg proof)

- Layout: `NN()=65536` nodes; node `n` at byte offset `64+n*40`; valid
  indices 0..65535 (s6_base.zag:50-57).
- `alloc_node` (s6_base.zag:87): `n=hg(W,20)+2`, clamped `if(n<2){n=2}`,
  scan `while(n<65536)`; returns `n` in [2,65535]; else `evict_node()` result
  or `-1`.
- `evict_node` (s6_base.zag:256): candidates require `n>=2` (from
  `n=cur+i mod 65536`); returns `best` in [2,65535] or `-1`.
- `alloc_raw` (s6_base.zag:105): same bounds, returns `n` in [2,65535] or `-1`.
- Nodes 0 and 1 are reserved header nodes (tags 900/901, s6_base.zag:813-814),
  never returned by the allocators.
- Every t2_* encoder checks its allocation (`if(x<0){return -1;}`) before
  writing operand fields, so the `-1` failure sentinel never lands in an
  operand field.
- Therefore every node id ever stored in an operand field is in [2,65535]:
  strictly positive, and strictly below 65536. Both candidate invariants
  (sign tag, 65536 ceiling) are provable from this code; the prereg selects
  one and states the proof.

## 6. Fix surface

The repair touches exactly E1..E4 (encoders) and D1..D7 (decoders), plus the
documented no-op review of E5..E7, D8, D9. No other source lines encode or
decode the node/frame operand namespace. The revised base will be a copied
tree under `operand_namespace_fix/`; the frozen files above are not modified.
