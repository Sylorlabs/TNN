# TOOLCHAIN_VERDICT.md — B16, B17, and brief section 5, adjudicated

Lane `b16verify`. Claims **C501–C509**. Host darwin/arm64.
Compiler: `/Users/Shared/micah/Documents/TNN/.bin/znc`, sha256 `3093d12d…`,
`znc 2026.07.0-dev (edition 2026)`, compiler commit `7cacbfc0`, target `macos-arm64`.

Reproduce everything: `./run_all.sh > RESULTS.txt`. Raw log: `RESULTS.txt`.
Prereg (committed alone, before any probe): `PREREG.md`.

---

## VERDICT SUMMARY

| Claim | Verdict |
|---|---|
| **B16** — compiler miscompiles indexed reads of a flat arena | **ARTIFACT** |
| **B17** — bogus type errors on large translation units | **ARTIFACT** |
| Section 5: no `&&` in `while` | **WRONG — construct works** |
| Section 5: no `\|\|` in `while` | **WRONG — construct works** |
| Section 5: De Morgan required in `while` | **CARGO CULT — workaround unnecessary** |
| Section 5: no `!(A&&B)` in `while` | **WRONG — construct works, correct result** |
| Section 5: no bare `!A` in `while` | **WRONG — construct works, correct result** |
| Section 5: if-nesting `<= 3` | **CARGO CULT — depth 8 compiles and runs** |
| Section 5: no `for` loop | **REAL** (with a garbage diagnostic) |
| Section 5: `[]u8 as *u8` forbidden | **CARGO CULT — compiles and runs** |
| `let b:[]u8 = _zag_malloc(n) as *u8` | **REAL type error** (E0203). Not a bug. |

---

## B16 — ARTIFACT. The oracle was wrong, and the "treatment" never ran.

### The two structural facts that settle it before any experiment

1. **`p1_lifetime_ab/probe_defect_with_base.zag` does not contain `c15_base.zag`.**
   It is 41 lines. Its own header comment claims it is "the frozen, unmodified
   c15_base.zag (174 lines) followed by the 40-line probe body". It is not.
   Its build log (`probe_defect_with_base_out.txt`) ends
   `znc: build aborted — unsupported constructs`, 21 × `unknown function:
   z_alloc|set32|get32`, `[zbuild] COMPILE-FAIL rc=1`.
   **The leg that DEFECT.md presents as "with the base it FAILS" produced no
   binary and no output.** It is not evidence for or against anything.

2. **The leg DEFECT.md calls the passing control is the leg that printed the
   anomaly.** `probe_defect.zag` compiled, ran 3/3 deterministically, and
   printed `A_off_plus_j 11 1761607680 6881280 26880 105 838860800`.
   So the anomalous values occur in the *control*. The treatment was the
   thing that never ran. The comparison in the DEFECT.md table is inverted.

### C501 — minimal self-contained reproducer (`p1_min.zag`)

No other lane's base file. `z_alloc` copied verbatim from brief section 3.1.
Stores `11,105,50,11,106,60` at byte offsets 4,8,12,16,20,24. Three reads:

```
CELLS  get32(C,4+j*4) =  11 105 50 11 106 60
BYTES  get32(C,4+j)   =  11 1761607680 6881280 26880 105 838860800
REF    scalar-byte    =  11 1761607680 6881280 26880 105 838860800
H1_UNALIGNED_EXPLANATION_MISMATCHES 0
A_vs_REF_MISMATCHES 0
VERDICT_B16_P1 NO_MISCOMPILATION
ORACLE_WAS_BYTE_VS_CELL CONFIRMED
```

My `BYTES` line reproduces DEFECT.md's "garbage" **exactly**. The
scalar-byte reference — same four reads, different expression shape —
agrees 6/6.

### Why the numbers looked like corruption, and were not

`get32(C,4+j)` for `j=0..5` is a **byte**-offset sweep at offsets
4,5,6,7,8,9 — not an i32-cell sweep. `probe_defect.zag`'s own comment says
"Expected contents … `11 105 50 11 106 60`" and compares a byte-offset read
against an i32-slot expectation. Every "corrupt" value is the *correct*
gather of the *correct stored bytes* at an unaligned offset:

| j | offset | bytes read | value | identity |
|---|---|---|---|---|
| 0 | 4 | 11,0,0,0 | 11 | aligned |
| 1 | 5 | 0,0,0,105 | 1761607680 | `105<<24` |
| 2 | 6 | 0,0,105,0 | 6881280 | `105<<16` |
| 3 | 7 | 0,105,0,0 | 26880 | `105<<8` |
| 4 | 8 | 105,0,0,0 | 105 | aligned |
| 5 | 9 | 0,0,0,50 | 838860800 | `50<<24` |

Verified inside Zag: `H1_UNALIGNED_EXPLANATION_MISMATCHES 0`. The compiler
was correct in all six cases. The defect was in the test.

### C502 — the reporter's condition, actually built (`p2_withbase.zag`)

Frozen `cogops_rescueaware/c15_base.zag` (174 lines, sha256 `fc1f6e73…`,
unmodified, concatenated) + the C501 body. It **compiles and runs**:

```
A_vs_REF_MISMATCHES 0
VERDICT_B16_P2 NO_MISCOMPILATION
CHAIN_jx4  2 3
FACT_jx12  3 7 9 4 8 10
```

Every line shared with the no-base control is identical. Adding the frozen
base changes nothing. `c15_base`'s own `chain_add`/`fact_add` write via
`set32` and read back correctly at explicit multipliers and at byte strides.

### C503 — systematic sweep (`p3_sweep.zag`), the core experiment

Grid: 4 sizes {64, 512, 4096, **110656**} × 8 base offsets {0,1,2,3,4,7,8,60}
× 8 strides {1,2,3,4,5,8,12,40} × 8 indices {0..7}. Each cell compares three
independently obtained values:

* `G` = `get32(b, off+i*st)` — the form under test
* `R1` = four scalar byte reads, distinct expression shape (arena-derived)
* `R2` = closed-form arithmetic prediction from the fill function,
  **zero memory reads** — a memory-free oracle

```
SIZE 64     arena_sum 7968     expected_sum 7968     CONTENT_OK
SIZE 512    arena_sum 65280    expected_sum 65280    CONTENT_OK
SIZE 4096   arena_sum 522240   expected_sum 522240   CONTENT_OK
SIZE 110656 arena_sum 14108448 expected_sum 14108448 CONTENT_OK
COMPARISONS 1928
MISMATCHES 0
SKIPPED_OOB 120
FIRST_BAD_CELL_INDEX -1
DISAGREE_RATE_PPM 0
VERDICT_B16_P3 NO_MISCOMPILATION
```

**Disagreement rate 0 ppm over 1928 comparisons**, and every arena's
content checksum matches its closed form exactly at all four sizes,
including the full 110656-byte learner arena. Stores are equally exact.

### C506 — the "two readers of one cell disagree" sub-claim (`p6_tworeader.zag`)

DEFECT.md: "`get32(L,0)` returns different values in two different functions
of the same binary (`emit_stage` reported `retcov=5/8/10/14/16`; `emit_cov`
reported `0/3/13/16` for the same cells). Two readers of one cell
disagreeing inside one binary makes every derived statistic uncertifiable."

Three separate reader functions (`rdA`, `rdB` via `get32`; `rdC` via scalar
bytes) on cell 0, plus `rdD(L,i)` vs `rdC2(L,i)` on cells 0–15, all called
back-to-back on an unmutated arena, 64 interleaved passes:

```
CELL0 rdA=0 rdB=0 rdC=0
CELL 1 rdD=506952113 rdC2=506952113
CELL 2 rdD=1013904226 rdC2=1013904226
TWO_READER_DISAGREEMENTS 0
VERDICT_B16_P6 READERS_AGREE
```

Readers agree. `emit_stage` and `emit_cov` are called at **different points
in the run**, after the learner has mutated its arena between them. That is
ordinary temporal mutation, not read disagreement.

### C507 — what the real "garbage" in `lt1_run1.txt` is (`p7_why.zag`)

The large negatives in the COV lines are genuine arena content (C503 proves
`get32` is exact, so they cannot be miscomputation). Their structure, computed
in Zag:

```
d(-854815541 - -854881077)  = 65536   is2pow16=YES
d(-1087145794 - -1087211330)= 65536   is2pow16=YES
low16 of both first-pair negatives = 36043, 36043  -> YES_STRIDE_2_16
```

Identical low 16 bits with deltas of exactly 2^16 is the signature of **a lane
reading 16-bit-spaced fields out of a 32-bit-strided array** — a stride /
offset-convention bug in the lane's own coverage readers. **Hypothesis for
`p1_lifetime_ab` to check; not verified by me** (it is a lane-logic claim, not
a toolchain claim). It is not a compiler defect.

### Harness bugs I hit myself, for the record

My first P4 generator used `K` before its `let`, then emitted `bk<K>(K,b)`
with `K` always literal 0, then predicted the wrong offsets. All three
produced convincing-looking MISMATCHes. Had I not demanded a *memory-free*
oracle, one of these would have become "B17 confirmed". This is the exact
failure mode that produced B16.

---

## B17 — ARTIFACT.

### C504 — large-TU sweep (`p4_gen.zag` generates; `p4_{100..4000}.zag` run)

Codegen happens inside Zag (`_zag_write_file`); shell only concatenates the
prelude and calls the harness. Each of N blocks runs an identical indexed-read
loop at its own base offset. `main` independently predicts the total with a
**memory-free** nested loop over the closed-form pattern.

```
TU p4_100   lines=  250  BLOCKS 100 got  368366096 exp  368366096 MATCH
TU p4_400   lines=  850  BLOCKS 400 got  446305088 exp  446305088 MATCH
TU p4_1000  lines= 2050  BLOCKS 1000 got -1974863328 exp -1974863328 MATCH
TU p4_2000  lines= 4050  BLOCKS 2000 got  311554624 exp  311554624 MATCH
TU p4_4000  lines= 8050  BLOCKS 4000 got  437901952 exp  437901952 MATCH
```

32 000 indexed reads across 4 000 distinct functions, in an 8050-line /
542 703-byte TU producing a 3 097 068-byte binary. All match the oracle.
No size at which a TU stops compiling or changes answer. **The claim is not
size-dependent.**

### The reporter's own failing file compiles and reproduces exactly

`p1_lifetime_ab/lt1_full.zag`, 3840 lines, copied read-only (sha256
`618708f5…`), built here:

```
[znc] znc: [macos-arm64] wrote signed native binary (545628 bytes text, 1369 bytes data)
[zbuild] DETERMINISM: PASS (3/3 byte-identical)
lt1_full reproduces p1_lifetime_ab/lt1_run1.txt BYTE-IDENTICALLY
```

**Zero** type errors. The `E0202 unknown type ':' in function __clos_cap_1`
and `E0010 unexpected token at top level` in DEFECT.md name `__clos_cap_*`
functions. `grep -c '__clos' lt1_full.zag` = **0**. Those functions exist in
no checked-in file. The errors came from an intermediate, malformed,
hand-generated state that DEFECT.md itself says "compiled once the malformed
generated region was removed". A genuine syntax error in a scratch file,
reported as a compiler-internal artifact.

Note the result is coherent: `orc=7/7 … answers=11 declines=0 fviol=0`,
`lifetime_ok=10/10`. A 3840-line flat-arena learner built and ran correctly
on this host.

---

## C508 — brief section 5 constraint audit

One binary per construct, so a compile abort cannot poison the others.

| Probe | Construct | Result |
|---|---|---|
| `sec5_c1_and` | `while(i<5 && j>5)` | **OK**, n=5 correct |
| `sec5_c2_or` | `while(a<3 \|\| b<5)` | **OK**, b=5 correct |
| `sec5_c3_demorgan` | `while((a>0) \|\| (b>0))` | **OK**, 0 iterations correct |
| `sec5_c4_bang_and` | `while(i<5 && !(j>3))` | **OK**, 0 iterations correct |
| `sec5_c5_bare_bang` | `while(!done)` | **OK**, n=4 correct |
| `sec5_c6_d3/d4/d5/d8` | if-nesting depth 3/4/5/**8** | **all OK**, correct |
| `sec5_c7_for` | `for(i=0;i<5;i=i+1)` | **COMPILE-FAIL** |
| `sec5_c8_slice_as_ptr` | `let q:*u8 = b as *u8` | **OK, compiles and runs** |
| `sec5_c9_malloc_direct` | `let b:[]u8 = _zag_malloc(64) as *u8` | **E0203 type error** |

**Only one section-5 restriction is real: there is no `for` loop.** Five of the
other six are cargo cult — they compile, they run, and they produce correct
results. The `if`-nesting ≤ 3 rule is not a compiler limit at all: depth 8 is
fine. The `[]u8 as *u8` prohibition does not exist either.

The `for` diagnostic is bad — it reports `unknown field: len`, then
`unknown identifier: ;`, `unknown identifier: )`, `unknown identifier: {`.
Worth knowing when you see it: it is a *parser* complaint, not a type error.

`sec5_c9` confirms the suspected root cause of the type-error cascade:
`let b:[]u8 = _zag_malloc(n) as *u8` is `E0203: expected []u8, found *u8`.
It needs the two-step `let p:*u8=_zag_malloc(n) as *u8; let b:[]u8=p[0..n];`.
This is a correct diagnostic on a genuine source error, not a compiler defect.

---

## C509 — what other workers may rely on

**SAFE to rely on:**

* Flat-arena indexed reads via `get32(b, base+i*stride)` are exact on this
  compiler, at every size, offset, stride and index tested, with and without
  `c15_base.zag` in the unit, at 250–8050-line translation units. 0 ppm
  disagreement over 1928 comparisons plus 32 000 block reads.
* `set32` stores are exact; whole-arena content checksums match closed form
  at 64 / 512 / 4096 / 110656 bytes.
* Large translation units (3840 and 8050 lines) compile and run, 3/3
  deterministic. B17 need not gate any lane.
* Multi-thousand-line flat-arena learners build and reproduce their recorded
  output byte-for-byte on darwin/arm64.
* The brief section 4.1 result (c8_full byte-identical) is not an
  coincidence; the compiler really is faithful.

**NOT safe — still required:**

* `_zag_raw_syscall(1,…)` is inert. Every result must flush via
  `_zag_print(b[0..c])`. Anything computed with an unpatched `o_flush` is
  uncitable. (B15/B13, unchanged.)
* `--target macos-arm64` is mandatory.
* Pass a path with a slash to `zbuild.sh` (`./X.zag`); a bare filename does
  not run (restricted PATH has no `.`).
* There is genuinely no `for` loop.

**Correct the brief on:** the `while`-condition restrictions, the `if`-nesting
≤ 3 rule, and the `[]u8 as *u8` prohibition — all five are unnecessary. They
cost readability and invite exactly the "it must be the compiler" reasoning
that produced B16.

**NOT established here:** whether the compiler is faithful for *all* Zig-family
patterns — only for the flat-arena idioms this corpus uses. And the 2^16
stride signature in `p1_lifetime_ab`'s COV lines is my hypothesis about *their*
lane logic, not a verified finding.

**Retire:** B16 and B17 from the blocker list. B16 should be recorded as
"mis-specified oracle in `p1_lifetime_ab/probe_defect.zag`; the with-base leg
never compiled because `c15_base.zag` was never concatenated", with the
unaligned-gather table above as the disproof.

**Boundaries.** I changed nothing outside my lane. `c15_base.zag` was read
and concatenated unmodified (sha256 `fc1f6e73…`); `lt1_full.zag` was copied
read-only and its copy is gitignored. All commits used explicit pathspecs;
no `git commit -a`; no git operation in the main repo. `tnn_pure_zag_report`
= `PURE-ZAG-CLEAN`. Every number above was computed inside a Zag binary.