# ZAG TOOLCHAIN DEFECTS — ADJUDICATED
**Lane `tcdefects`. Verified empirically on this host 2026-10-04 with the pinned
compiler `/Users/Shared/micah/Documents/TNN/.bin/znc`, `--target macos-arm64`.**

This is the definitive citable answer to the four SUSPECTED compiler defects
reported by `lane/predopt`, `lane/causal` and `lane/b16verify`. **Do not
re-litigate any of them. Read the verdict, then read §6 before writing Zag.**

Reproducers: `docs/lab/research-lead/overnight-20260928/tcdefects/`
Run them all with `tcdefects/run_all.sh` (25 reproducers, every run behind
`tnnwatch.sh`, 3/3 byte-identical determinism asserted on each).

---

## 0. VERDICT TABLE

| # | Claim | Source | Verdict |
|---|---|---|---|
| 1 | `get32`/`set32` take BYTE offsets, not cell indices | predopt / b16verify | **API TRAP — CONFIRMED** (the one fact every lane must know) |
| 2 | A five-term `&&` in an `if` silently evaluates false | predopt | **UNREPRODUCIBLE** — reporter's oracle bug |
| 3 | An accessor call inside a loop is mis-compiled | causal | **UNREPRODUCIBLE** — reporter's off-by-one |
| 4a | Duplicate `let` bindings compile then segfault | causal | **UNREPRODUCIBLE** — they compile and run |
| 4b | `A[i]=v as u8` is unusable where `set32` works | causal | **UNREPRODUCIBLE** — works correctly |
| 5 | b16verify negative findings (only `for` is real) | b16verify | **CONFIRMED, with one material correction** (§5) |
| 6 | **NEW: `[]u8 as *u8` silently corrupts memory** | found here | **REAL COMPILER DEFECT** (§6) |

**Net result: exactly ONE real compiler defect was found, and it was not on
any lane's list.** Everything else is either an API-semantics trap (claim 1,
which is documentation, not a compiler bug, but is just as dangerous) or a
defect in the reporter's own harness.

---

## 1. CLAIM 1 — `get32`/`set32` TAKE BYTE OFFSETS. **API TRAP, CONFIRMED.**

**This is the single most important toolchain fact in the program.** It is not
a compiler defect. `get32`/`set32` behave exactly as written in brief §3.2 and
do exactly what their parameter name (`off`) says. The trap is that the natural
reading of "cell j" and the actual reading of "byte offset" differ by a factor
of four, and nothing in the language, the compiler diagnostic, or the runtime
tells you.

### Reproducer
`tcdefects/C1_get32_semantics.zag` (minimal core below).

### Memory-free oracle
The construct under test is `get32`/`set32`, so the oracle must not call them.
Three independent oracles are used, and all three agree:

* **O1 — raw byte reads** `b[k]`. No `get32` anywhere.
* **O2 — hand-assembled 4-byte window** written in a *different expression
  form* from `get32`'s body:
  `hand(off) = b[off] + b[off+1]*256 + b[off+2]*65536 + b[off+3]*16777216`
  (multiplicative, versus `get32`'s shift/or). If `get32(off) == hand(off)` for
  every offset, then `get32` is *provably* a byte-window read at `[off,off+3)`
  and nothing else.
* **O3 — pure arithmetic for the write side.** Byte `k` of an i32 `v` is
  `(v / 256^k) mod 256`, computed by repeated division from the literal `v`.
  No memory consulted.

### Results (3/3 byte-identical)

| Test | Result |
|---|---|
| `get32(A,off)` for `off` = 0,4,8,12,16,20 | 11, 22, 33, 44, 55, 66 — **matches literals** |
| Raw bytes after those writes | `11,0,0,0, 22,0,0,0, 33,0,0,0, 44,0,0,0, 55,0,0,0, 66,0,0,0` — **little-endian, exact** |
| **O2: `get32(A,off)` vs `hand(A,off)`, off = 0..24** | **0 mismatches out of 25** |
| **O2 at 9 unaligned offsets** | **0 mismatches out of 9** |
| **O3: 8 write bytes vs arithmetic oracle** | **0 mismatches out of 8** |
| `get32(A,cellindex)` for cell = 0..5 | 11, **369098752**, **1441792**, **5632**, 22, **553648128** |
| `set32(B,cellindex 0..5)` → raw bytes `b[0..10]` | `11,22,33,44,55,66,0,0,0,0` |
| …windows of those 6 "cells" | 740365835, 16951, 0 — **all six unrecoverable** |

The last two rows are exactly the `11, 1761607680, 6881280, 26880, 105, …`
pattern `lane/b16verify` reported. **b16verify's diagnosis was correct**: a BYTE
sweep at offsets 4..9, not an i32-cell sweep.

### Failure mode, quantified

Write `get32(C, 4+j)` for j = 0..5 and read what you actually get, with cells
holding 11,22,33,44,55,66:

| call | naive expectation | actual | why |
|---|---|---|---|
| `get32(C,0)` | 11 | **11** | correct by luck (offset 0 == cell 0) |
| `get32(C,1)` | 22 | **369098752** | reads bytes 1..4 = 0,0,0,22 |
| `get32(C,2)` | 33 | **1441792** | reads bytes 2..5 = 0,0,22,0 |
| `get32(C,3)` | 44 | **5632** | reads bytes 3..6 = 0,22,0,0 |
| `get32(C,4)` | 55 | **22** | correct by luck (offset 4 == cell 1) |
| `get32(C,5)` | 66 | **553648128** | reads bytes 5..8 = 0,0,0,33 |

**Safe call patterns**
* Any offset that is a multiple of 4, derived from the arena base.
* Unaligned offsets are *legal and exact* — they simply straddle cells. There is
  no alignment requirement (0/9 mismatches at unaligned offsets).
* Forward-only sweeps stepping the offset by 4: `o=0; while(o<1024){ ...; o=o+4; }`.

**Silently corrupting patterns**
* `get32(C,j)` / `set32(C,j,v)` where `j` is a **cell index**. Reads return
  large shift-shaped garbage; **writes overlap and destroy every cell they
  touch**. After `set32` at cell indices 0..5 the six intended values are
  unrecoverable — you get a diagonal smear, not six cells.
* `get32(C,0)` and `get32(C,4)` *appear* to work, which is what makes this trap
  survive a smoke test. A sweep that starts at cell 0 and reads only a couple of
  cells looks fine.

**Can a bounds-checked wrapper make misuse impossible?**
**Partly — but the check you need is alignment, not bounds.** Measured:

* There is **no bounds checking at all** on slice indexing. `set32(D,30,…)` on a
  32-byte arena writes bytes 30..33 and **survives with no trap**
  (`C1_get32_semantics.zag` §P7). Reading `b[1000]` on a 64-byte arena returns
  **0 with no trap** (`C5f_oob_read.zag`).
* So a wrapper must carry **both** checks itself. The recommended pair:

```zag
// getc32: CELL-indexed accessor. Alignment and range are enforced here, so a
// caller can never make the byte-offset mistake.
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
  Verified working by `tcdefects/C10_guarded_wrappers.zag` (17 assertions,
  0 failures): 16-cell round-trip against the arithmetic oracle; the trap
  sequence `setc32(B,c,…)` for c=0..5 now yields **6 distinct cells** instead of
  a diagonal smear; write bytes match `(v/256^k) mod 256`; the range check fires
  at cell 16 of a 64-byte arena and at negative cells while leaving in-range
  cells untouched; and the in-range path still sums 256 cells correctly
  (32640) in a 1024-byte arena.
* **Residual risk the wrapper cannot remove:** a wrong `cell` is still a wrong
  `cell`. The wrapper converts a *silent heap corruption* into a *silent wrong
  answer inside your arena*, which is a smaller but not zero blast radius.
  Discipline still matters.

### Blast radius

* **1064** `.zag` files exist under `overnight-20260928/`; **800** call
  `get32`/`set32`. Every one of them is exposed to this trap.
* Triage heuristic that separates safe from suspect call sites:
  * `get32(<arena>, <var>)` where `<var>` is a byte offset: **safe**.
    The dominant idiom — `set32(rb,ro,…)` ×1236, `set32(kb,ko,…)` ×606,
    `get32(kb,ko)` ×606, `set32(G,off,…)` ×304 — ~30 655 call sites.
  * second argument containing `*4` or `+4`: **safe** (~1 746 more).
  * second argument a bare index-like name (`i j k n c e idx cell node slot`):
    **16 call sites** — inspect by hand.
* **All 16 high-risk sites were inspected and all 16 are CORRECT byte-offset
  usage.** Verified examples: `ivwc_veto/src/ivwc_veto.zag:626-636` uses
  `ix = (2*4+p)*4`; `gen_cogops_unify/gu_glue.zag:63` pairs `set32(A,cell,…)`
  with `set32(A,cell+4,…)`, so `cell` is an offset; `p1_lifetime_ab/lt_main.zag:113`
  pairs `get32(LT,e)` with `get32(LT,e+4)`.
* **Conclusion: no existing lane is demonstrably bitten. The risk is
  prospective.** Lanes to re-audit anyway (they are the largest `get32`/`set32`
  users and any future edit is exposed): `p1_lifetime_ab`, `gen_cogops_unify`,
  `ivwc_veto`.

---

## 2. CLAIM 2 — FIVE-TERM `&&` IN AN `if`. **UNREPRODUCIBLE.**

There is **no arity threshold.** Not at 2, not at 3, not at 5. `&&` and `||`
are correct at every arity tested, in `if` conditions and in `while` conditions.

`tcdefects/C2g_boolops_final.zag` — **28 assertions, 0 failures, 3/3 identical.**

| Test | Oracle | Result |
|---|---|---|
| `&&` all-true, arity 1…8 | all taken → `11111111` | **PASS** |
| `\|\|` all-false, arity 1…8 | all not-taken → `99999999` | **PASS** |
| `\|\|` single TRUE at position 1…5 of arity 5 | `11111` | **PASS** |
| `\|\|` single TRUE at position 1, 2, 8 of arity 8 | `111` | **PASS** |
| `&&` single FALSE at position 1…5 of arity 5 | `99999` | **PASS** |
| `&&` full 2-operand truth table (TT TF FT FF) | `1999` | **PASS** |
| `\|\|` full 2-operand truth table (TT TF FT FF) | `1119` | **PASS** |
| `\|\|` inside `while` body, truth in operand 1 and operand 2 | 4 / 4 | **PASS** |
| `\|\|` as the `while` condition itself | 5 iterations | **PASS** |
| `&&` as the `while` condition, false in operand 1 / operand 2 | 0 / 0 | **PASS** |
| `!A`, `!(A&&B)`, `!(A\|\|B)`, De Morgan | truth table | **PASS** |
| `!(A&&B)` as a `while` condition | 10 / 0 | **PASS** |
| `(A&&B)\|\|(C&&D)` mixed precedence, 3 shapes | `199` | **PASS** |
| bare `!A` in `if` and as a `while` condition | truth table | **PASS** |
| De Morgan `(!A \|\| !B)` as a `while` condition | 5 | **PASS** |

### Why the reporter saw a failure — read this before writing your own oracle

This is the most important methodological finding in the document, and it is
the *same* class of error that produced three harness bugs in a previous wave.

I reproduced an apparent defect too. My probe built "the single true operand at
position k" as `k==k` for k = 2..5 — that is, as `1==2`, `1==3`, `1==4`,
`1==5`. **Every one of those is false.** So the chain contained no true operand
anywhere and the compiler's `false` was correct. A second, independent version
of the same error accumulated branch outcomes as `c=c*10+1` / `c=c*10+0`
starting from `c=0`, where **both branches yield 0**, so the test could not
distinguish the branches at all.

The lesson, which is the citable part:

> A reproducer whose oracle is written from the same intuition as the code under
> test proves nothing. Every operand must be checkable **by construction**:
> `k<k+1` is manifestly true, `k>k` is manifestly false, and a comparison result
> is normalised with `(X==1)` before being negated. Any oracle whose expected
> value is "obviously what the expression should say" is a bug waiting to
> happen.

This is why `lane/b16verify`'s probes were weak (§5): its conditions were all
decided by their first operand, so a first-operand-only bug would have been
invisible.

### Action
Brief §5's claim that `&&`/`||` "do exist in `if` conditions" is **correct and
can be strengthened**. The restriction on `!(A&&B)` in `while` conditions is
**cargo cult** and has been removed from the brief. `for` remains the only
control-flow limitation (§5).

---

## 3. CLAIM 3 — ACCESSOR CALL INSIDE A LOOP. **UNREPRODUCIBLE.**

`tcdefects/C3_accessor_in_loop.zag` — 11 sub-tests, **0 failures**, 3/3 identical.

Everything the claim names works:

| Test | Oracle | Result |
|---|---|---|
| `while(n<1000){c++; if(n>=AREV()){break;} n++;}`, `AREV()=500` | 501 | **PASS** |
| accessor in the `while` condition: `while(c<AREV())` | 500 | **PASS** |
| accessor hoisted into a `let` inside the loop | 500 | **PASS** |
| accessor result in arithmetic inside the loop, 500×500 | 250000 | **PASS** |
| accessor called **twice** in one condition | 501 | **PASS** |
| parameterised accessor `LIM(100)` | 101 | **PASS** |
| accessor returning a non-constant `LIM(x)` | 1 | **PASS** |
| **256 `set32` then 256 `get32`, oracle `3*k`** | **0 mismatches** | **PASS** |
| **256 `get32` by `+4` byte-offset sweep** | **0 mismatches** | **PASS** |
| accessor in a loop nested in a loop | 50 | **PASS** |

**Root cause of the report: off-by-one.** The reporter's counter reached 784
because their counter is incremented *before* the cap test, so the visit where
`n` first equals the cap is the `(cap+1)`-th visit. `if(n>=500)` inside a body
that has already done `c=c+1` yields **501**, not 500. `n8>=LIM(n8)` is always
true, so a guard written that way fires on the first visit and yields **1**.

### Action
No lane is blocked. Lanes may use accessor functions inside loops freely. This
was the highest-impact claim of the four ("blocks any lane using accessor
functions in loops") and it is unfounded.

---

## 4. CLAIM 4 — DUPLICATE `let` BINDINGS SEGFAULT; `A[i]=v as u8` UNUSABLE.
**UNREPRODUCIBLE.**

Duplicate bindings **compile and run correctly**, with 3/3 determinism and no
segfault:

| Test | File | Result |
|---|---|---|
| `let x:i32=1; let x:i32=2;` in one scope | `C4a_dup_let_same_scope.zag` | runs, `x=2`, REACHED_END |
| triple redeclaration `z=1; z=2; z=3;` | `C4e_dup_let_redecl.zag` | runs, `z=3` (last binding wins) |
| shadowing in a nested `if` block | `C4b_dup_let_nested.zag` | inner 2, outer 1 after block |
| shadowing an unrelated name in a `while` body | `C4c_dup_let_loop_body.zag` | 4 iters, `n=400` |
| **`A[i]=v as u8` direct byte store** | `C4d_u8_store.zag` | **all PASS** |

`A[i]=v as u8` is fully usable and behaves as integer truncation, checked
against the pure-arithmetic oracle `(v/256^k) mod 256`:

| Store | Oracle | Result |
|---|---|---|
| `B[0]=16909060 as u8` | 4 | **PASS** (truncates, as expected) |
| `B[8]=0 as u8` / `B[9]=255 as u8` | 0 / 255 | **PASS** |
| `B[10]=256 as u8` | 0 | **PASS** (truncates to 0) |
| `B[11]=(0-1) as u8` | 255 | **PASS** |
| indexed store of all 4 bytes of `0x12345678` driven by a loop var | 4 oracle bytes | **PASS**, 0 mismatches |

**Root cause of the report: a caller bug.** The reporter almost certainly wrote
`let A:[]u8=_zag_malloc(n) as *u8;`. `_zag_malloc` returns `*u8`, so that is
`error[E0203]: expected []u8, found *u8`. It needs the two-step form:

```zag
let p:*u8=_zag_malloc(n) as *u8;
let b:[]u8=p[0..n];
```
I hit exactly this error myself while writing `C4d_u8_store.zag`.

### One real caller trap found nearby (not a defect)
Shadowing a **loop variable** inside the loop body makes the loop
**non-terminating**, because a later `i=i+1` in that body updates the inner
binding and the outer loop condition never advances. Demonstrated safely in
`C4c_dup_let_loop_body.zag` (outer variable advanced before the shadow).
Shadowing an unrelated name is harmless. Watchdog-terminated runs are the only
reason this is a note and not a hang report.

### Also tested and clean
Re-declaring one name with two **different** types in the same scope
(`W1_retype_shadow.zag`, `W2_distinct_names.zag`) **compiles and runs**. This
was a hypothesis I formed mid-session and **failed to confirm**; it is recorded
here so nobody re-raises it.

---

## 5. CLAIM 5 — b16verify's NEGATIVE FINDINGS. **CONFIRMED, ONE CORRECTION.**

`lane/b16verify` ran 1928 indexed-read comparisons against a memory-free oracle
with 0 mismatches and concluded most prior "compiler bug" reports were harness
artifacts. **That conclusion is correct**, and this document independently
reproduces it (§1 O2, §3). b16verify's discipline was right; its *probes* were
weak, and it drew one conclusion too far.

| b16verify finding | Verdict | Evidence |
|---|---|---|
| `for` is a real limitation | **CONFIRMED** | `C5b_for_loop.zag` fails to compile |
| `&&` works | **CONFIRMED** | `C2g` — arity 1…8, full truth tables |
| `\|\|` works | **CONFIRMED** | `C2g` — truth in operand 1 and operand 2 |
| De Morgan works | **CONFIRMED** | `C5a` [3] |
| `!(A&&B)` works | **CONFIRMED** | `C2g` [9], `C5a` [4][5] — in `if` **and** `while` |
| bare `!A` works | **CONFIRMED** | `C5a` [1][2] |
| if-nesting to depth 8 | **CONFIRMED and UNDERSTATED** | works to depth **10** |
| `[]u8 as *u8` "compiles — cargo cult" | **CORRECTION: it compiles but is ACTIVELY BROKEN** | see §6 |

**`for` detail.** `for(i=0;i<5;i=i+1){…}` fails to compile with a misleading
diagnostic: `arm64: unknown field: len` / `arm64: unknown identifier: ;` /
`unknown identifier: )` / `unknown identifier: {`, ending in
`znc: build aborted — unsupported constructs (see messages above)`. The parser
is clearly mis-parsing `for` as a field access. **The verdict is unambiguous
(`for` is unsupported) but the error text will mislead you** — do not go
hunting for a `len` field.

### The contradiction I had to adjudicate
`b16verify` said `&&`/`||`/`!` "all compile and give correct results — cargo
cult", i.e. **no defect**. `predopt` said a **five-term `&&` silently evaluates
false**, i.e. **a defect**. These are directly contradictory.

**Resolution: `b16verify` is right and `predopt` is wrong**, but for a reason
worth recording. Both lanes tested *compilation*, and `&&`/`||` compile fine.
The disagreement was only ever about *evaluation*. Once tested with
operands that are true and false **by construction** rather than by intuition,
evaluation is correct at every arity (§2). `predopt`'s failure was in its
oracle, not in `znc`.

Note the direction of the error: `predopt` reported a defect that does not
exist, which is the more expensive kind of mistake — it would have sent lanes
around the `&&` operator for nothing.

### Corrections needed to the brief
1. §5 "if-nesting <= 3" is **false**; depth 10 verified.
2. §5 "NO `!(A&&B)` in while conditions" is **false**; it works.
3. §5 "`&&` and `||` do exist in `if` conditions" is **true** — strengthen to
   "work correctly at arity 1…8, in `if` and in `while`".
4. §5 "`[]u8 as *u8` is forbidden" is **right for the wrong reason** — see §6.

---

## 6. NEW REAL DEFECT — `[]u8 as *u8` SILENTLY CORRUPTS MEMORY

**This is the only genuine compiler defect found in this adjudication, and it
was not on any lane's list.** `lane/b16verify` noticed the construct compiles
and filed it as "cargo cult, fine". It is not fine.

### Verdict: REAL COMPILER DEFECT.

### Minimal reproducers

**M11 — reads return the wrong value** (`M11_slice_as_ptr_read.zag`):
```zag
let p:*u8=_zag_malloc(64) as *u8;
let b:[]u8=p[0..64];
b[0]=7;
let cp:*u8=b as *u8;
let viaCast:[]u8=cp[0..64];
print b[0], viaCast[0];
```
Oracle: this program wrote the **literal 7** into `b[0]` of a 64-byte arena, so
any correct read-back is 7. Observed:

```
direct b[0]        = 7
via (b as *u8)     = 8      <-- WRONG, deterministic 3/3
```

**M12 — control** (`M12_slice_ptr_control.zag`): identical program using
`_zag_slice_ptr(b)` returns **7**. Correct.

**M13 — writes corrupt the original arena** (`M13_slice_as_ptr_write.zag`):
```zag
b[0]=7;
let cp:*u8=b as *u8;
let viaCast:[]u8=cp[0..64];
viaCast[0]=42;
print b[0];
```
Oracle: after writing 42 through an allegedly-derived slice, the original
`b[0]` must be **42** (aliased — the normal expectation) or **7** (disjoint).
**0 is neither**, so no consistent aliasing semantics produces it. Observed:

```
b[0] before          = 7
original b[0] after  = 0      <-- silent corruption, deterministic 3/3
```

**C5g — nondeterminism** (`C5g_slice_as_ptr.zag`): reading the second byte
back through the cast pointer returned **64 on runs 1 and 3 and 192 on run 2**.
This reproducer **fails the 3/3 byte-identical determinism bar** — the only
reproducer in the set that does, and it does so because of this defect.
Two further cast-pointer reads returned 8 and 64 where 7 and 9 were expected.

### Mechanism (as far as the evidence supports)
`b as *u8` is **not** the slice's data pointer. Measured directly:
`_zag_slice_ptr(b) != (b as *u8)`, yet the cast pointer is non-null. The cast
appears to yield the address of the slice *descriptor* rather than of its
bytes: the first byte read back was **8**, which is a plausible descriptor word,
and reads and writes through it land on unrelated memory — which is why the
victim was the *original* arena.

### Blast radius

* **320 of 1064 `.zag` files** under `overnight-20260928/` contain a
  `<identifier> as *u8` cast. That grep deliberately excludes the legitimate
  `_zag_malloc(n) as *u8` form, so **320 files are candidates** and each needs
  its operand checked: the cast is only dangerous when the operand is a `[]u8`
  **slice**, not a `*u8` pointer.
* Highest-count lanes to audit first: `l3_suf_scaling` (19 files),
  `l2_metareuse_compose2` (11), `ns_invariant` (9), `l2_metareuse_adversary`
  (8), `sum_detector_fix` (7), `l3_inr_impl` (7), `formal_compose_rerank` (7),
  `formal_compose_e2e` (7), `l3_rx_k10` (6), `xhier_countmap_fix` (5),
  `l3_rx` (5), `subsumption_p0` (4), `p2_compose_dag` (4), `l3_suf_adversary` (4).
* Triage rule: **`let q:*u8 = <slicevar> as *u8;` is always a bug.** The only
  correct `*u8` sources are `_zag_malloc(n) as *u8` and `_zag_slice_ptr(b)`.
* A quick check that costs nothing: grep for `as \*u8` and confirm every
  operand is one of those two forms.

---

## 7. WHAT I COULD NOT REPRODUCE, AND WHAT I DID NOT TEST

* **Claims 2, 3, 4a, 4b: UNREPRODUCIBLE.** I built minimal, self-contained
  reproducers for each, with memory-free oracles, and swept parameterisations
  well past the reported shapes (arity 1…8 for boolean operators, 28
  assertions; 11 accessor-in-loop shapes; 5 duplicate-binding shapes; 5
  `u8`-store shapes; plus 20 assertions auditing the §5 language questions).
  Each claim's *reported* symptom never appeared. My conclusion is that the
  reporter's harness was at fault in every case, and §2/§3/§4 name the specific
  fault. I cannot prove what the reporter actually ran.
* **Not tested:** integer overflow behaviour beyond the cases in `C5a` §[10]
  (notably that `v>>24` on a negative `v` yields `-1`, and `(0-1)>>24 as u8`
  yields 255 — both verified); division rounding for negative operands
  (verified truncating toward zero: `(-7)/2 == -3`); recursion; `i64`
  arithmetic beyond formatting; multi-file / cross-TU behaviour; anything
  involving `_zag_read_file` / `_zag_write_file`; concurrency (Zag is
  single-threaded here); the `--no-analyze` / `--no-foreground-cache` flag
  combinations other than the mandated one.
* **Not attempted:** disassembling the emitted arm64 to confirm the
  slice-descriptor mechanism in §6. The behavioural evidence is conclusive
  about the *effect*; the mechanism is a hypothesis.

---

## 8. CORRECTED FACTS WRITTEN TO THE BRIEF
Sections 2–5 of `ZAG_LANGUAGE_AND_WORKER_BRIEF.md` were updated from this
document: §3.2 now states in capitals that the argument is a **byte offset**
and gives the `getc32`/`setc32` guarded wrappers; §5's control-flow list is
corrected (no `for`; `&&`/`||` verified to arity 8 in `if` and `while`;
`!(A&&B)` and De Morgan both fine; if-nesting ≥10 not ≤3; `[]u8 as *u8`
actively corrupts memory, use `_zag_slice_ptr`); and a new §5.1 records the
oracle-construction rule that produced three of the four false reports.
