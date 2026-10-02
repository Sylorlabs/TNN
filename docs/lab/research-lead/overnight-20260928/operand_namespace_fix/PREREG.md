# PREREG.md -- Operand Namespace Fix, Revised Base rev1

Frozen: 2026-10-02. This prereg is committed ALONE before any implementation
(AUDIT.md committed as 0ad4e09d5). Kill bars below govern the verdict. No bar
may be weakened after results are seen. This work is authorized by Micah's
2026-10-02 ruling on the C299 SCALING-5000-FIXED-FAIL (see MEMORY.md); the
ruling's 7 governance items are answered one by one in section 7.

## 1. Question

Does a revised base that replaces the `10000+slot` frame-ref tag with a
structural sign tag (negative = frame ref, nonnegative = node id) restore
correct 5000-MAP scaling (C299's failing K1) while preserving the indexed
scale law and introducing zero semantic regressions on worlds where the old
base was correct?

## 2. Chosen encoding and proof

ENCODING (selected): negative frame-ref tag.
- `FRAME_REF(s) = -(s+1)` for frame slot `s >= 0`. Slot 0 -> -1, slot 1 -> -2.
- Decode rule: `op < 0` -> frame slot `-op-1`; `op >= 0` -> node id, value
  `ng(W,op,20)`.
- The decode rule contains NO magnitude constant. Node and frame operands are
  distinguished structurally by sign.

PROOF (from the frozen allocator, s6_base.zag):
- P1: `alloc_node` (:87) sets `n=hg(W,20)+2`, clamps `if(n<2){n=2}`, scans
  `while(n<65536)`, and returns `n` in [2,65535]; otherwise it returns the
  `evict_node()` result or `-1`.
- P2: `evict_node` (:256) only considers candidates with `n>=2` (from
  `n=cur+i mod 65536`) and returns such a `best` in [2,65535], or `-1`.
- P3: `alloc_raw` (:105) has identical bounds: [2,65535] or `-1`.
- P4: nodes 0 and 1 are reserved header nodes (tags 900/901, :813-814), never
  returned by any allocator.
- P5: every t2_* encoder checks its allocation (`if(x<0){return -1;}`) before
  writing operand fields, so the `-1` failure sentinel never lands in an
  operand field.
- CONCLUSION: every node id ever stored in an ISA operand field is in
  [2,65535]: strictly positive. Every frame ref emitted by the encoders is
  `-(s+1) <= -1`: strictly negative. The two namespaces are disjoint by sign,
  by construction, for any workspace size. The proof does not depend on any
  guessed constant.

WHY NOT the 65536 offset: Micah's ruling permits a >65536 offset only with a
proven ceiling. 65536 is provable (P1-P3 plus `NN()=65536`), but the offset
keeps the *shape* of the old defect: a magnitude threshold inside the decode
rule that a future workspace resize could silently break. The sign tag fixes
the invariant itself ("structurally/tagged distinguishable") with zero
magnitude constants, and it is immune to workspace resizing for as long as
the allocator keeps node ids nonnegative (guaranteed by the `n>=2` clamp).
The 65536 offset is therefore rejected as the weaker invariant, not for lack
of proof.

## 3. Exact source changes (rev1 vs frozen s6_base.zag)

Only these lines change. All other lines of the base are byte-identical.

Encoders:
- t2_guard (:329): `ns(W,g,4,10000+slot)` -> `ns(W,g,4,-1-slot)`
- t2_set (:333): `ns(W,s,4,10000+slot)` -> `ns(W,s,4,-1-slot)`
- t2_mov (:337): `ns(W,c,4,10000+dst); ns(W,c,8,10000+src);` ->
  `ns(W,c,4,-1-dst); ns(W,c,8,-1-src);`
- t2_inc (:341): `ns(W,c,4,10000+slot)` -> `ns(W,c,4,-1-slot)`

Decoders:
- res_op (:181-185) becomes:
  `fn res_op(W:[]u8,f:i32,op:i32)i32 {`
  `  if(op<0){return fr_get(W,f,-op-1);}`
  `  return ng(W,op,20);`
  `}`
  (The old `return 0` default for `op<0` is removed: under the invariant there
  is no third case; negative IS the frame tag.)
- execute tag 101 SET (:200-202):
  `let d:i32=ng(W,cur,4); let sr:i32=ng(W,cur,8);`
  `if(d>=0){return -999999;}`
  `fr_set(W,fr,-d-1,res_op(W,fr,sr)); nx=seq_nx(W,cur);`
- execute tag 103 INC (:206-208):
  `let s:i32=ng(W,cur,4); if(s>=0){return -999999;}`
  `fr_set(W,fr,-s-1,fr_get(W,fr,-s-1)+1); nx=seq_nx(W,cur);`
- execute tag 104 DEC (:209-211):
  `let s2:i32=ng(W,cur,4); if(s2>=0){return -999999;}`
  `fr_set(W,fr,-s2-1,fr_get(W,fr,-s2-1)-1); nx=seq_nx(W,cur);`

Covered without textual change (they delegate to `res_op`):
- execute tag 102 GUARD (:203-205): both operands via `res_op`; no threshold
  literal present, so the sign rule applies automatically.
- exec_val (:218-221) and t2_exec (:393-398): `res_op(fr, ng(W,root,4))`.

Reviewed, no change needed:
- t_c6 (:873, `ns(W,root,4,1000)`): dead code (`run_all()` never called);
  under the new rule 1000 >= 0 in destination position still fails closed,
  so its (unobserved) behavior is preserved.
- t2_revise rollback (:665) and driver s6_mkbroken (s6_driver.zag:37): retag
  only, operand fields preserved; SET/INC destination decoding stays in
  agreement through the single shared rule.
- t2_sig (:460) and driver s6_chaincheck (s6_driver.zag:65): read f8 of
  guard/set cells as node ids; frame refs never appear there; mov-cell f8
  (frame ref) now yields lv=0 instead of a garbage node read, strictly
  cleaner, and both are off the s6 verification path.
- r_mk_guide tag-102 guide nodes (:1278): never executed; separate namespace.

t2_dec and t2_jnz do not exist in the repository (AUDIT.md sec 4); the DEC
decoder (D5) follows the same invariant.

## 4. Revised tree layout (copied, frozen files untouched)

`docs/lab/research-lead/overnight-20260928/operand_namespace_fix/rev1/`:
- `op_base.zag`: s6_base.zag with exactly the section-3 changes.
- `op_patch.zag`: byte-identical copy of s6_patch.zag (sha256 verified).
- `op_driver.zag`: scale-parameterized s6-style driver (decoys = S-5, real = 5,
  3 build orders, 8 queries, modes 0/1/3/5, chain integrity). Scale stamped by
  shell text substitution only (no computation outside Zag).
- `op_small.zag`: 60-decoy differential driver (old-vs-new byte comparison).
- `op_bound.zag`: K1/K4/K5 boundary driver (literal ids at 9995..10005 and
  65530..65535, sign-tag legality assertions).
- `op_redteam.zag`: K6 malformed/cyclic/stale driver.
- `op_clean.zag`: K7b functional driver (t2_asm_chain/count/sum via all four
  encoders, incl. t2_mov epilogue).
- `build/`: assembled `op_full_*.zag`, binaries, compile logs.
- `runs/`: stdout + sha256 per run.

The frozen `scaling_5000_fixed/` tree is never modified; C299 stays canonical.

## 5. Frozen kill bars

K1 NEG-ENCODING LEGALITY (proof bar): the section-2 proof holds by
construction; dynamically, op_bound part 1 allocates past node id 10000,
builds guard/set/inc/mov cells through the real t2_* encoders with literal
operands whose node ids exceed 10000, executes them, and asserts correct
values. PASS iff every assertion holds AND grep finds zero remaining
`10000+slot`, `>=10000`, `<10000`, `-10000` operand patterns in rev1.

K2 SITE COVERAGE: `diff` frozen-vs-rev1 shows changes ONLY at the
section-3 lines (E1-E4, res_op, execute 101/103/104); D3/D6/D7 textually
unchanged (res_op-delegated, documented). PASS iff the diff line inventory
matches section 3 exactly.

K3 REGRESSION at 100/500/1000/5000 MAPs: op_driver at S in {100,500,1000,
5000} (decoys S-5 + 5 real, 3 build orders D/R/I, 8 queries each).
- K3a correctness: ok=1 for every query in every order at every S.
- K3b determinism: 3/3 byte-identical runs per S (sha256 recorded).
- K3c scale law: every mode-1 query scan <= 32 at every S (indexed flat);
  order-D mode-0 scan >= 6*(S-5) at every S (linear scales); at S=5000 the
  order-D ratio >= 1000x.
- K3d robustness: zero panics/hangs, build fails=0.
FAIL on any sub-bar fails K3. The 5000-MAP scaling claim becomes canonical
only if K3a AND K3c both pass (correctness and scan reduction together).

K4 OLD-COLLISION-REGION BOUNDARY: literal node ids
{9995,9998,9999,10000,10001,10002,10005} used as guard/set operands.
- On rev1: 7/7 execute correctly (guard passes, set writes literal value).
- On the frozen base: the 4 ids >= 10000 fail (guard rejects / wrong value),
  proving the test exercises the C299 bug and the boundary is real.
PASS iff rev1 is 7/7 and frozen is exactly 3/7 (the below-threshold three).

K5 MAX-NODE-ID: literal node ids {65530..65535} (top of the legal range)
used as guard/set operands on rev1; `res_op` on op=65535 returns
`ng(W,65535,20)`; encoder sign check (no encoder emits a nonnegative frame
ref). PASS iff all execute correctly with zero panics.

K6 RED-TEAM malformed/cyclic/stale (bounded inputs; the pre-existing
unbounded fr_get walk on astronomic slot magnitudes is out of scope and
identical in kind on both bases):
- malformed: hand-built SET with destination = node id 42 -> fail closed
  -999999 (both bases agree); destination = 10000 (old tag) on rev1 ->
  fail closed -999999, no panic; operands 0, 1, -1 hand-built -> no panic,
  defined behavior; operands within [-100000,200000] -> all terminate.
- cyclic: 2-cell SEQ cycle -> execute terminates via the st<1000 budget and
  returns -999999; self-comparing guard (both operands same frame ref) ->
  takes the true branch with the correct value.
- stale: literal node evicted (live flag cleared), then referenced by a
  guard -> no panic, deterministic across 3/3 runs; node-operand cases
  agree between old and new base (differential).
PASS iff zero panics, zero hangs, all fail-closed assertions hold, and the
differential node-operand cases are byte-identical old-vs-new.

K7 NO-REGRESSION ON PRIOR CLEAN WORLDS:
- K7a: op_small (60 decoys + 5 real, 3 orders, 8 queries; the pilot scale
  that passed on the frozen base) compiled against frozen s6_base+s6_patch
  and against rev1 op_base+op_patch: stdout byte-identical.
- K7b: op_clean functional worlds (chain, count with t2_mov epilogue, sum
  graphs; all four encoders exercised; t2_exec outputs) on frozen vs rev1:
  all outputs byte-identical.
PASS iff both differentials are byte-identical (sha256 match).

## 6. Verdict mapping

- K1..K7 all PASS: OPERAND-NAMESPACE-FIX-COMPLETE. rev1 becomes the candidate
  revised base; the 5000-MAP scaling result may then be claimed canonical
  (correctness K3a + scan law K3c jointly).
- Any K fails: OPERAND-NAMESPACE-FIX-FAIL with the failing bar named; no
  rescue edits inside this wave (fresh prereg required).
- K3b fails: nondeterminism; investigate, no verdict until 3/3 identical.

## 7. Micah's 7 governance items, answered

1. Source-audit EVERY operand decode/encode site: AUDIT.md (commit
   0ad4e09d5), 7 encoders (E1-E7) + 9 decoders (D1-D9) + non-sites +
   t2_dec/t2_jnz proven absent repo-wide.
2. PREREGISTER the new invariant BEFORE implementation: this file, frozen
   alone before any rev1 source exists.
3. Pure Zag implementation: safebin PATH, pinned znc
   (src/tools/toolchain/znc_linux_x86_64_abed8aa1), no Python (Step 0 in
   NAMECHECK.md); all four compiler-defect workarounds apply to new driver
   code (no `as *i32`+slice in functions, no `_zag_print` for dynamic
   content, no `.len` trust on cast slices, if-nesting <= 3 with hoisted
   flags, no `!(... && ...)` in while conditions).
4. Deterministic regression at 100/500/1000/5000 MAPs: K3.
5. Boundary tests around the old collision region and at max legal node id:
   K4 and K5.
6. Red-team malformed/cyclic/stale operands: K6.
7. No semantic regressions on prior clean worlds: K7 (60-decoy pilot config
   + functional chain/count/sum worlds, differential old-vs-new).

C299 SCALING-5000-FIXED-FAIL is preserved as canonical for the old frozen
build: no frozen file is modified, no ledger entry is rewritten, and the
13,107x scan reduction stays exploratory until K3a+K3c jointly pass on rev1.

## 8. Constraints

Unfrozen files only under `operand_namespace_fix/`; frozen tree read-only;
paper untouched; nothing pushed; commits use explicit pathspecs; commit-order
self-check (prereg commit strictly precedes implementation commit); no em
dashes in loop docs (check_no_dash.sh).
