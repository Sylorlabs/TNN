# B16 REFUTED: the compiler does not miscompile indexed reads

Prior claim (`DEFECT.md` B16, commit `d97d6d0e3`): *"Indexed reads are
miscompiled once `c15_base.zag` is in the unit."* Filed as a blocking
toolchain defect; the whole lifetime experiment was marked VOID on it.

**Verdict: REFUTED. The claim is a probe-authoring error, not a compiler
defect.** Three independent lines of evidence.

## 1. The "correct" probe was never correct

`probe_defect.zag` writes six i32 cells at STRIDE 4 (`set32(C,4,11)`,
`set32(C,8,105)`, ...) and then reads them back at STRIDE 1
(`get32(C,4+j)`). A stride-1 read of a stride-4-written array re-reads three
zero bytes and one live byte, so it is garbage **by construction**.

The committed `probe_defect_out.txt` — the artifact the prior REPORT
describes as "PASSES, all four forms return `11 105 50 11 106 60`" —
actually contains, for its own `A_off_plus_j` form:

```
A_off_plus_j 11
1761607680
6881280
26880
105
838860800
```

Identical to the values the report attributes to the *with-base* build. The
prior worker misread its own committed output.

## 2. Those "wrong" values are exactly correct arithmetic

Decoding each as little-endian against the bytes `set32` actually wrote
(`C[4..8]=11,0,0,0`, `C[8..12]=105,0,0,0`, `C[12..16]=50,0,0,0`, ...):

| j | read offset 4+j | bytes read | value | observed |
|---|---|---|---|---|
| 0 | 4 | 11 00 00 00 | 11 | 11 |
| 1 | 5 | 00 00 00 105 | 1761607680 | 1761607680 |
| 2 | 6 | 00 00 105 00 | 6881280 | 6881280 |
| 3 | 7 | 00 105 00 00 | 26880 | 26880 |
| 4 | 8 | 105 00 00 00 | 105 | 105 |
| 5 | 9 | 00 00 00 50 | 838860800 | 838860800 |

Six for six. `get32(C, 4+j)` executed **correctly**. A raw byte dump of
`C[0..28]` in the same binary reproduces every written byte exactly, which
is a direct end-to-end proof that indexed byte reads and i32 assembly are
intact in this unit.

## 3. The with-base build never ran, and adding the base changes nothing

The committed `probe_defect_with_base_out.txt` is not a program run. It is a
build abort:

```
[znc] arm64: unknown function: z_alloc
[znc] arm64: unknown function: set32   (x7)
[znc] arm68: unknown function: get32   (x9)
[znc] znc: build aborted -- unsupported constructs
[zbuild] COMPILE-FAIL rc=1
```

The committed `probe_defect_with_base.zag` contains only `fn p` and
`fn main`; its `z_alloc`/`get32`/`set32` were supposed to come from the
concatenated frozen base, and the assembly never supplied them. So the
entire B16 comparison rests on a binary that was never produced.

### The controlled re-run (this lane)

Same probe body, three different translation units:

| unit | lines | stdout sha256 |
|---|---|---|
| `b16_probe.zag` (self-contained) | 79 | `22f1784e9e4eb9d6e7d1fffa5510dbe4ae38737e0978346964c8d8606ae6e7b3` |
| `b16_base_only.zag` (+ frozen `c15_base.zag`) | 254 | `22f1784e9e4eb9d6e7d1fffa5510dbe4ae38737e0978346964c8d8606ae6e7b3` |
| `b16_fullprefix.zag` (+ `c15_base` + `c8_learn` 1331 + `hq_module`) | 1880 | `22f1784e9e4eb9d6e7d1fffa5510dbe4ae38737e0978346964c8d8606ae6e7b3` |

**BYTE-IDENTICAL across all three.** Adding the frozen base, and adding the
entire 1880-line frozen prefix that the real learner runs on, changes not one
output byte. 3/3 byte-identical on each. The compiler was never the problem.

## Consequence

The barrier that caused the lifetime experiment to be marked VOID/uncertified
does not exist. Any defect observed in `lt1_full` is a defect in the lane's
own additive code or in the frozen semantics, and is adjudicable. The
mitigation the prior worker applied on the strength of B16 (explicit
multipliers everywhere, a lane-local `lt_chain_add` with inlined byte
stores) was never required by the compiler; it is kept only where it is
independently justified.

Claim ID: **C526** (B16 refuted). **C527** (B16's evidence base was a
compile-abort artifact).
