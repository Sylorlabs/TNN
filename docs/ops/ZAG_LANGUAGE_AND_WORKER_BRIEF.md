# ZAG LANGUAGE REFERENCE + WORKER BRIEF
**Verified empirically on this host 2026-10-03; sections 2-5 re-adjudicated
2026-10-04 against the pinned compiler. Read before writing any Zag.**

> **COMPILER-DEFECT DEFERRAL:** if you are about to report a compiler bug, read
> **§5.3** and **`docs/ops/ZAG_TOOLCHAIN_DEFECTS.md`** first. Four lanes have now
> reported "suspected compiler defects"; exactly **one** claim in this program's
> history was a real compiler defect, and it was found by adjudicating those four
> reports, not by any of them. Three were bugs in the reporters' own oracles.

## 0. HARD RULE: PURE ZAG

All scientific computation must be Zag. Shell/git only for orchestration.

```sh
. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
tnn_pure_zag_report     # must print: VERDICT: PURE-ZAG-CLEAN
```

Forbidden: python, node, bun, deno, tsc, cc, gcc, rustc, julia, perl, ruby, R,
make, cmake, ... They are shimmed to hard-fail (exit 127). If one runs during an
experimental wave that is a **PROCESS-FAIL**, even if harmless.

## 1. BUILD AND RUN

```sh
ZNC=/Users/Shared/micah/Documents/TNN/.bin/znc
$ZNC --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache X.zag
./X
```

**`--target macos-arm64` is MANDATORY.** Without it the compiler silently emits
x86-64 Linux ELF; compile reports success, run fails with `exec format error`.

Harness (does this for you, and checks determinism):
```sh
/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh X.zag --rep 3
```
`--rep 3` asserts 3/3 byte-identical stdout. Determinism is a preregistered bar.

Zag files are **concatenated**, not imported. No forward declarations. Order
matters. Exactly one `fn main(` per final translation unit.

## 2. TYPES - THE COMPLETE SET

| Type | Notes |
|---|---|
| `i32` | The only arithmetic type. Everything is i32 fields in a `[]u8`. |
| `i64` | decimal formatting, syscall args |
| `u8` | byte-store element |
| `[]u8` | THE universal container. Strings and byte arrays are both `[]u8`. |
| `*u8` | raw pointer from `_zag_malloc` |
| `void` | |

**There are NO floats** (no f32/f64). Use i32 fixed-point or exact integer
cross-multiplication for rational comparison. Example of exact rational compare:
`if(n1*(u2+2) < n2*(u1+2)){ /* n1/(u1+2) < n2/(u2+2) */ }`

**No arrays, no structs, no enums, no maps/dicts, no generics, no closures, no
`[][]u8`.** Every "record" is a byte-offset convention over a flat arena.

**`i32` arithmetic facts (verified 2026-10-04, `tcdefects/C5a` §10):**
division truncates toward zero (`(0-7)/2 == -3`); `v>>24` on a negative `v`
yields `-1`, so `((0-1)>>24) as u8 == 255` -- exactly what `set32` needs to
store a high byte. `x as u8` truncates: `256 as u8 == 0`, `(0-1) as u8 == 255`.

**`*u8` has exactly two correct sources:** `_zag_malloc(n) as *u8` and
`_zag_slice_ptr(b)`. Any other cast onto `*u8` is either a compile error or the
memory-corrupting defect in **§5.1**. Note `_zag_malloc` returns `*u8`, **not**
`[]u8`, so `let A:[]u8=_zag_malloc(n) as *u8;` is
`error[E0203]: expected []u8, found *u8`. Use §3.1's two-step form. This one
error is the likely root cause of two separate false "compiler defect" reports.

## 3. THE THREE IDIOMS YOU WILL USE CONSTANTLY

### 3.1 Allocation
```zag
fn z_alloc(n:i32)[]u8 {
  if(n<1){ return ""; }
  let p:*u8=_zag_malloc(n) as *u8;
  if(p==null as *u8){ return ""; }
  let b:[]u8=p[0..n];
  let i:i32=0;
  while(i<n){ b[i]=0; i=i+1; }
  return b;
}
```

### 3.2 Little-endian i32 cell access

**`off` IS A BYTE OFFSET. NOT A CELL INDEX. READ THIS TWICE.**

Verified 2026-10-04 by adjudication (`docs/ops/ZAG_TOOLCHAIN_DEFECTS.md` §1,
reproducer `tcdefects/C1_get32_semantics.zag`). `get32(b,4)` reads the i32 at
**byte** 4, which is **cell 1**. Calling `get32(C,4+j)` for j=0..5 is a BYTE
sweep at offsets 4..9, not a cell sweep, and returns shift-shaped garbage
(`11, 1761607680, 6881280, 26880, 105, ...` -- this was long mis-reported as
compiler blocker B16). It is not a compiler bug; it is this API contract.

```zag
fn get32(b:[]u8,off:i32)i32 {
  return (b[off] as i32)|((b[off+1] as i32)<<8)|((b[off+2] as i32)<<16)|((b[off+3] as i32)<<24);
}
fn set32(b:[]u8,off:i32,v:i32)void {
  b[off]=v as u8; b[off+1]=(v>>8) as u8; b[off+2]=(v>>16) as u8; b[off+3]=(v>>24) as u8;
  return;
}
```

Facts established by measurement, not assumption:
* `get32(off)` is **exactly** the 4-byte window `[off,off+3)`: 0 mismatches
  against a hand-assembled window over 25 consecutive offsets and 9 unaligned
  offsets. There is no hidden cell arithmetic anywhere.
* **Unaligned offsets are legal and exact.** They simply straddle cells.
* There is **NO bounds checking**. `set32(D,30,...)` on a 32-byte arena writes
  bytes 30..33 and survives silently; reading `b[1000]` on a 64-byte arena
  returns 0 with no trap. Bounds discipline is entirely on you.

**PREFER THE GUARDED CELL-INDEXED WRAPPERS.** These make the mistake
impossible to express, because the caller supplies a *cell*:

```zag
fn getc32(b:[]u8,cell:i32)i32 {
  if(cell<0){ return 0; }
  let off:i32=cell*4;
  if((off+4)>b.len){ return 0; }
  return (b[off] as i32)|((b[off+1] as i32)<<8)|((b[off+2] as i32)<<16)|((b[off+3] as i32)<<24);
}
fn setc32(b:[]u8,cell:i32,v:i32)void {
  if(cell<0){ return; }
  let off:i32=cell*4;
  if((off+4)>b.len){ return; }
  b[off]=v as u8; b[off+1]=(v>>8) as u8; b[off+2]=(v>>16) as u8; b[off+3]=(v>>24) as u8;
  return;
}
```
Verified: 256 cells written with `set32` at `i*4` and read back two ways
(`k*4` and a `+4` byte sweep) against a memory-free oracle, 0 mismatches both
ways (`tcdefects/C3_accessor_in_loop.zag` §7).

**SAFE / CORRUPTING CALL PATTERNS**
* SAFE: any multiple of 4 derived from the arena base; forward sweeps stepping
  the offset by 4 (`o=0; while(o<1024){ ...; o=o+4; }`).
* SILENTLY CORRUPTING: passing a **cell index**. Writes overlap and destroy
  every cell they touch -- after `set32(B,j,v)` for cell j=0..5 the arena holds
  `11,22,33,44,55,66,0,0,0` and none of the six cells is recoverable.
* `get32(C,0)` and `get32(C,4)` *appear* to work. That is what lets this trap
  survive a smoke test. Always sweep the whole range before trusting it.

Triage for existing code: `get32(<arena>,<var>)` where `<var>` is an offset is
the dominant idiom (~30 600 sites) and is correct. Only 16 call sites use a
bare index-like name; all 16 were inspected and all are correct. See
`ZAG_TOOLCHAIN_DEFECTS.md` §1 for the audit and the lanes to re-check.

### 3.3 Arena layout convention (this IS TNN's memory model)
```zag
fn WSZ()i32 { return 110656; }
fn NN()i32  { return 1024; }             // node capacity
fn NE()i32  { return 4096; }             // edge capacity
fn noff(n:i32)i32 { return 64+n*40; }    // node n record, 40 bytes
fn eoff(e:i32)i32 { return 41024+e*16; }  // edge e record, 16 bytes
fn loff(l:i32)i32 { return 106560+l*32; }
```

## 4. OUTPUT

### 4.0 READ THIS FIRST - `_zag_raw_syscall` IS INERT ON THIS HOST

Every existing canonical lane writes its results with:
```zag
fn o_flush(b:[]u8,c:i32)void {
  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0); return;
}
```
**On this host that call produces NO OUTPUT and returns success (rc=0).** It is
not an error, it is silence. Any lane whose only output path is `o_flush`
therefore emits an EMPTY log and still reports success.

Verified directly:
```zag
let bb:[]u8=z_alloc(64);
bb[0]=79; bb[1]=75; bb[2]=10;           // "OK\n"
_zag_raw_syscall(1,1,(_zag_slice_ptr(bb) as i64),3 as i64,0,0,0);
_zag_println("D_println_OK");
```
prints ONLY `D_println_OK`. The `OK` never appears.

**THE FIX - use `_zag_print` instead. This is the required portable shim:**
```zag
fn o_flush(b:[]u8,c:i32)void {
  _zag_print(b[0..c]);
  return;
}
```

### 4.1 PROOF THIS SHIM IS CORRECT (this settles blocker B13)

The lane `cogops_learnosc2/c8_full.zag` (340948 bytes of text, a large
flat-arena learner) was rebuilt on this macOS/arm64 host with the SINGLE
substitution above and run. Result:

```
reference c8_run1.txt (Linux x86_64 era): ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7  3344 bytes
this host, macOS/arm64:                  ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7  3344 bytes
*** BYTE-IDENTICAL ***
```

Three consequences, all important:

1. **Blocker B13 is RESOLVED and was overstated.** The canonical corpus is
   fully reproducible on this host. Cross-platform determinism holds.
2. **The compiler is NOT miscompiling flat-arena indexed reads.** A separate
   worker reported "silent miscompilation of indexed reads" (barrier B16). That
   claim is DOUBTED and probably an artifact of the broken output path or of
   the reporter's own harness: this 340KB flat-arena program executes and produces
   byte-exact results. Re-verify before building architecture on B16.

   **RESOLVED 2026-10-04 (`docs/ops/ZAG_TOOLCHAIN_DEFECTS.md` §1). B16 was NOT a
   compiler bug. It was the `get32`/`set32` byte-offset API trap of §3.2.** The
   reported symptom -- `get32(C,4+j)` for j=0..5 returning
   `11, 1761607680, 6881280, 26880, 105, ...` -- is exactly what a **byte sweep
   at offsets 4..9** produces over cells holding 11,22,33,44,55,66. Proven: a
   hand-assembled 4-byte window (multiplicative form, no `get32`) agrees with
   `get32(off)` at **0 mismatches over 25 consecutive offsets** and **9 unaligned
   offsets**, i.e. `get32` is exactly the window `[off,off+3)`. **B16 is CLOSED
   as an API-semantics trap. Do not cite it as a compiler defect.**
3. **Any result computed on this host with an unpatched `o_flush` is
   uncitable.** Re-run with the shim.

### 4.2 Both output styles

**(a) Simple, for static lines.** `_zag_println` EXISTS and works:
```zag
fn main()i32 { _zag_println("R32_ZNC_PROBE_OK"); return 0; }
```

**(b) Dynamic content: still use ONE buffer, but flush with `_zag_print`.**
The discipline of formatting into one preallocated buffer and writing once is
correct and worth keeping; only the final call must change.
```zag
fn o_i64(b:[]u8,c:i32,v:i64)i32 {
  let neg:i32=0; let x:i64=v;
  if(x<0){ neg=1; x=0-x; }
  let n:i32=1; let t:i64=x;
  while(t>=10){ t=t/10; n=n+1; }
  let e:i32=c+neg+n; let p:i32=e-1; let y:i64=x;
  if(y==0){ b[p]=48; }
  while(y>0){ b[p]=(48+(y-(y/10)*10)) as u8; y=y/10; p=p-1; }
  if(neg==1){ b[c]=45; }
  return e;
}
fn o_app(b:[]u8,c:i32,s:[]u8)i32 {
  let i:i32=0; while(i<s.len){ b[c+i]=s[i]; i=i+1; } return c+s.len;
}
fn o_nl(b:[]u8,c:i32)i32 { b[c]=10; return c+1; }
fn o_flush(b:[]u8,c:i32)void {
  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0); return;
}
```

Other builtins: `_zag_malloc(n)`, `_zag_slice_ptr(b)`, `_zag_raw_syscall(nr,a1..a6)`,
`_zag_print(s)` (string literals only), `_zag_eprintln(s)`,
`_zag_i64_to_str(v)` -> newline-terminated string,
`_zag_read_file(path)`, `_zag_write_file(path,b)`, `_zag_file_exists(path)`,
`_zag_strlen(s)`, `_zag_arg(i)`, `_zag_argc()`.

## 5. CONTROL FLOW AND CASTS

**Every item below was re-verified 2026-10-04 by the `tcdefects` adjudication.
Full evidence, minimal reproducers and memory-free oracles:
`docs/ops/ZAG_TOOLCHAIN_DEFECTS.md`. Reproducers:
`docs/lab/research-lead/overnight-20260928/tcdefects/` (`./run_all.sh`).**

Most of the old "gotchas" in this section were **cargo cult**. They are kept
below only where they are real, with the evidence stated.

### 5.0 WHAT IS ACTUALLY TRUE

- **NO `for` loop.** This is the ONLY genuine control-flow limitation. Use
  `while(cond){ ... }`. `for(i=0;i<5;i=i+1)` fails to compile with a
  **misleading diagnostic** -- `arm64: unknown field: len` ... `znc: build
  aborted — unsupported constructs`. Do not go hunting for a `len` field; the
  parser is mis-parsing `for` as a field access. (`tcdefects/C5b_for_loop.zag`)
- **`&&` and `||` WORK.** Correct at arity 1..8, in `if` conditions *and* in
  `while` conditions, for all four two-operand combinations, with the true or
  false operand in any position. 28 assertions, 0 failures. The old warning
  about five-term `&&` was a **reporter's oracle bug** (`ZAG_TOOLCHAIN_DEFECTS.md`
  §2). There is no arity threshold.
- **`!(A&&B)` WORKS, including in `while` conditions.** The old prohibition was
  cargo cult. So do `!(A||B)`, bare `!A`, and De Morgan `(!A || !B)`.
- **if-nesting is fine to at least depth 10**, with and without `else` chains,
  and with accessor calls in the innermost body. The old "if-nesting <= 3" limit
  was **false**. (`NEST_2..NEST_10.zag`, `T6_acc_depth8.zag`, `C5a` §6-7.)
- **`break` and `continue` both work**, including at if-nesting depth 4.
- **Accessor functions in loops are fine** -- constants, parameters,
  non-constant returns, two calls in one condition, nested loops, `get32`/`set32`
  sweeps over 256 cells. The "accessor in a loop is mis-compiled" report was an
  **off-by-one in the reporter's harness** (`ZAG_TOOLCHAIN_DEFECTS.md` §3).
- **Duplicate `let` bindings compile and run.** Same scope, triple
  redeclaration, nested-block shadowing: all correct, 3/3 deterministic, no
  segfault. Last binding wins. (`C4a`, `C4b`, `C4c`, `C4e`.) The "duplicate let
  segfaults" report was a **caller bug**: the reporter almost certainly wrote
  `let A:[]u8=_zag_malloc(n) as *u8;`, which is `error[E0203]: expected []u8,
  found *u8`. Use the two-step form in §3.1.
- **`A[i]=v as u8` works** and truncates as integer truncation (256 -> 0,
  -1 -> 255). The "u8 store unusable" report was the same E0203 caller bug.
  (`C4d_u8_store.zag`.)

### 5.1 `[]u8 as *u8` ACTIVELY CORRUPTS MEMORY - REAL COMPILER DEFECT

**This is the only real compiler defect found by the adjudication, and it is
not on any lane's list.** A previous worker noted the construct "compiles" and
filed it as harmless. It compiles. It is also broken.

```zag
let p:*u8=_zag_malloc(64) as *u8;
let b:[]u8=p[0..64];
b[0]=7;
let cp:*u8=b as *u8;          // <-- NOT the slice's data pointer
let viaCast:[]u8=cp[0..64];
print b[0], viaCast[0];       // 7, then 8   (8 is WRONG)
```

* **Reads return the wrong value.** `viaCast[0]` gives **8** where the literal
  7 was written. Deterministic, 3/3.
* **Writes corrupt the ORIGINAL arena.** After `viaCast[0]=42`, the original
  `b[0]` becomes **0** -- neither the old value (7) nor the new value (42), so
  no consistent aliasing semantics can explain it. Deterministic, 3/3.
* **Nondeterministic.** A second byte read back as **64, 192, 64** across three
  runs. This is the only reproducer in the set that fails the 3/3
  byte-identical bar, and it fails because of this.
* `_zag_slice_ptr(b) != (b as *u8)`, yet the cast pointer is non-null. The cast
  appears to yield the address of the slice *descriptor*, not of its bytes.

**RULE: the only correct sources of a `*u8` are `_zag_malloc(n) as *u8` and
`_zag_slice_ptr(b)`. `let q:*u8 = <slicevar> as *u8;` is always a bug.**

Triage: 320 of 1064 `.zag` files contain a `<identifier> as *u8` cast and need
their operand checked. Highest-count lanes: `l3_suf_scaling` (19 files),
`l2_metareuse_compose2` (11), `ns_invariant` (9), `l2_metareuse_adversary` (8),
`sum_detector_fix` (7), `l3_inr_impl` (7), `formal_compose_rerank` (7),
`formal_compose_e2e` (7), `l3_rx_k10` (6), `xhier_countmap_fix` (5), `l3_rx`
(5), `subsumption_p0` (4), `p2_compose_dag` (4), `l3_suf_adversary` (4).

### 5.2 STILL TRUE, STILL REQUIRED

- `return;` written explicitly even in `void` functions.
- Casts: `v as i32`, `p as *u8`, `null as *u8`.
- **No bounds checking on slice indexing** (§3.2). Range-check in your wrappers.
- Recursion works and is used in the frozen core.
- Strings are NOT null-terminated `[]u8`. For syscalls convert with `z_cstr`.
- Exactly one `fn main(` per translation unit.
- **Do not print a pointer's numeric value** (`p as i64`). It is a heap address,
  so macOS ASLR makes it differ every run and it will look like a determinism
  bug. Null-test instead.

### 5.3 ORACLE CONSTRUCTION - WHY 3 OF 4 "DEFECT" REPORTS WERE FALSE

Four lanes reported SUSPECTED compiler defects. **Exactly one claim in this
program's history has ever been a real compiler defect** (`[]u8 as *u8`, above,
found by this adjudication). The other three were bugs in the *reporters'
oracles*. The same failure mode produced three harness bugs in an earlier wave.
**Read this before you file or believe any compiler-defect report.**

> A reproducer whose oracle is written from the same intuition as the code under
> test proves nothing.

The three specific traps, all of which I fell into myself:

1. **"Obviously true" operands that are false.** To build "the single true
   operand at position k of a 5-term `||`", the natural move is `k==k` for
   k=2..5, i.e. `1==2`, `1==3`, `1==4`, `1==5`. **All of those are false.** The
   chain had no true operand anywhere and the compiler's `false` was correct.
   *Use `k<k+1` for true and `k>k` for false -- checkable by construction, not
   by intuition.*
2. **Branch encodings that cannot distinguish the branches.** Accumulating an
   outcome as `c=c*10+1` (then) and `c=c*10+0` (else) starting from `c=0` gives
   **0 either way**. *Use then=+1 / else=+9.*
3. **Counters incremented before the guard.** A cap written
   `c=c+1; if(n>=500){break;}` stops on the **501st** visit, not the 500th. And
   `n>=LIM(n)` is *always true*, so such a guard fires on the first visit.
   *Derive loop-exit counts by hand and print the iteration trace.*

Corollaries that also cost time:
* **"It compiles" is not "it works."** `[]u8 as *u8` compiles.
* **A test whose first operand already decides the answer cannot detect a
  first-operand-only bug.** That is why the earlier `&&`/`||` probes all passed.
* **Never print a heap address** when asserting determinism (see §5.2).

## 6. FILE IO (if you need it)
```zag
fn z_cstr(s:[]u8)[]u8 {           // make null-terminated copy for syscalls
  let b:[]u8=z_alloc(s.len+1);
  let i:i32=0; while(i<s.len){ b[i]=s[i]; i=i+1; }
  b[s.len]=0; return b;
}
fn fopen_r(path:[]u8)i64 { let cp:[]u8=z_cstr(path); return _zag_raw_syscall(2,(_zag_slice_ptr(cp) as i64),0,0,0,0,0); }
fn fclose(fd:i64)void { _zag_raw_syscall(3,fd,0,0,0,0,0); return; }
```
Prefer `_zag_read_file` / `_zag_write_file` when a path suffices.

## 7. FROZEN CORES YOU BUILD ON

| Core | Path | Lines | sha256 (first 12) |
|---|---|---|---|
| COGOPS frozen prefix | `cogops_learnosc2/c8_learn.zag` | 1331 | `750cb01d086f` |
| COGOPS base arena | `cogops_rescueaware/c15_base.zag` | 174 | `fc1f6e73...` |
| Contract module | `hook_phase1/hq_module.zag` | 326 | `4200e21f...` |
| TNN-2 frozen ref | `compression_exec/tnn2_frozen_ref.zag` | 1591 | `a29972ca8183` |
| L3-SUF (CODE-FROZEN) | `l3_suf_intermediate/src/` | ~2500 | see CODEFREEZE.md |

All under `docs/lab/research-lead/overnight-20260928/`.

Key COGOPS functions: `specialize_ret/vfy/cnt`, `ret_spec/vfy_spec/cnt_spec`,
`plan_find/plan_new/plan_drop`, `try_family`, `learn_bindings`, `execute_plan`,
`compose`, `g_tag/g_nneeds/need_f`, `apply_kind1/apply_kind3`, `snap_out/out_eq_snap`.

Key TNN-2 functions: `alloc_node/alloc_raw/link_edge`, `res_op`, `execute/exec_val`,
`t2_trial/t2_try_verify/mp_run`, `promote_graph`, `t2_gather`, `ev_query`,
`ev_observe/ev_teach/ev_act`, `revise_on_contradict/t2_revise_graph`, `evict_node`,
`rec_evict`, `tnn2_init`.

## 8. KNOWN ARCHITECTURAL BLOCKERS (do not rediscover; cite these)

- **B1 node-id / frame-slot namespace collision.** `res_op` reads `op>=10000`
  as a frame slot; trial literals are node ids. Workspace hits node id 10000 at
  ~1400 decoys; at `>=1000` in the smaller E1+D1 engine at ~140 MAPs. Makes
  5k/10k MAP scaling INCORRECT, not merely slow. (C299, C375.)
- **B2 global O(N) scans dominate.** N=28 takes 75-92s vs 0.3s predicted.
  Superlinear: O(N^2) MAP attempts x O(NE) scans. N=100 incomplete after 7min.
- **B3 old GEN arena hard-dimensioned for 4 MAPs.** nm=5..7 silent wrong
  answers, nm=8 panic. Superseded by GEN-REDIM (C429/C434).
- **B6 interpreter scratch overflow at program length 7.** `z_alloc(64)` too
  small; needs 128. One-line fix, genuine source-level stack overflow. (C398/C405.)
- **B7 eviction tie-break cannot hold 6 sequential new facts.** (C75.)
- **B12 frozen TNN-1 has no world-driver interface.** (C141.)
- **B13 RESOLVED 2026-10-03.** Canonical lanes DO reproduce on this host: c8_full.zag
  rebuilt with the `_zag_print` shim gives byte-identical output (see section 4.1).
- **B14 ledger mint pipeline deletes instead of appending.** Guard now installed
  at `mint_guard/mint_guard_v2.sh`. Ledger restored to C410.
- **B16 CLOSED 2026-10-04 — NOT a compiler defect.** The "silent miscompilation
  of indexed reads" was the `get32`/`set32` **byte-offset API trap**. See §3.2
  and §4.1(2). Cite `docs/ops/ZAG_TOOLCHAIN_DEFECTS.md` §1, not B16.
- **B17 (new, 2026-10-04) REAL COMPILER DEFECT: `[]u8 as *u8` corrupts memory.**
  Reads through the cast pointer return wrong values; writes through it corrupt
  the original arena (7 -> 0, neither old nor new value); one read was
  nondeterministic. Use `_zag_slice_ptr`. See §5.1.
- **NOT BLOCKERS — the following were reported as compiler defects and are all
  false.** Do not re-investigate: five-term `&&`/`||`; accessor calls in loops;
  duplicate `let` bindings; `A[i]=v as u8`; `[]u8 as *u8` "just compiles";
  if-nesting beyond 3; `!(A&&B)` in `while`. Each was a bug in the reporter's
  harness, except `[]u8 as *u8` which is B17 above. Adjudication with
  reproducers and memory-free oracles:
  `docs/ops/ZAG_TOOLCHAIN_DEFECTS.md`. **Read §5.3 of this brief before filing
  any new compiler-defect claim.**

## 9. THE CENTRAL NEGATIVE RESULT (context for L3 work)

The canonical ledger records **"L3 achieved anywhere: zero."** Every L3-adjacent
claim contains an explicit researcher-bounding admission:

- C285 killed C284: creation was "MENU SELECTION over 5 ops."
- C459 L3-INR-SEALED: "L3-KILLED," reclassified L2+; "incomplete-disambiguation
  trap."
- C287: "REPEAT schema researcher-enumerated; does not clear C0-B open-form bar."
- C397 GPI-3: "the learner did not invent the WRAP/SEQUENCE strategies (those
  are the frozen templates)."
- C335: "the criterion form (extremum over recency) is researcher-authored."

**Therefore: an L3 claim is only credible if the NOVEL FORM ITSELF is not
enumerable from source.** Selecting among researcher-written operators, filling
templates, or brute-force search over a fixed DSL are all explicitly NOT L3.

## 10. WORKER RULES

### 10.0 ISOLATION IS MANDATORY (wave-1 failure, do not repeat)

Wave 1 had six workers all running `git checkout -b` in the SAME directory.
They corrupted each other's branches: preregs landed on other lanes, branches
moved under active work, two workers rebuilt history. You MUST use a private
worktree:

```sh
WT=$(/Users/Shared/micah/Documents/TNN/TNN/tools/lane.sh new <your-lane-name>)
cd "$WT"          # <-- ALL your git and all your files happen in here
```

Inside that worktree, `git rev-parse --show-toplevel` must be the worktree path,
NOT /Users/Shared/micah/Documents/TNN/TNN. If it is the main repo, stop and fix
your setup before doing any work.

- Never `git checkout` in the main repo. Never switch branches there.
- Never touch another lane's files or worktree.
- Never `git commit -a`. Always explicit pathspecs.
- Your lane directory is `docs/lab/research-lead/overnight-20260928/<your-lane>/`.

### 10.1 Scientific rules

- Your goal is NOT to make the hypothesis pass. Faithfully implement the
  preregistered hypothesis. If it fails, REPORT THE FAILURE. Do not move bars.
- Prereg BEFORE implementing. Freeze fixtures, predictions, kill bars,
  baselines, ablations. Commit the prereg alone.
- New claim IDs: **use the C5xx block or higher.** C377-C466 are contested by
  the pending reconciliation and MUST NOT be minted.
- Report: STATUS, COMMITS, RESULTS, VERDICT, BOUNDARIES, NEXT EXPERIMENT.
  Be concise. Facts over prose. No marketing language.
