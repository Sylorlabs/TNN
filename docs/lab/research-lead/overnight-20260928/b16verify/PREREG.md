# PREREG — TOOLCHAIN-VERIFY: settle B16 / B17 / brief-section-5 constraints

Lane: `b16verify`. Claims minted: **C501–C509**.
Date: 2026-10-03. Host: darwin/arm64.

## 0. What is being adjudicated

`p1_lifetime_ab/DEFECT.md` asserted three NEW blockers:

* **B15** — `_zag_raw_syscall(1,...)` inert. (Already RESOLVED as B13 by the
  brief section 4.0/4.1. Not re-litigated here; the required shim is used.)
* **B16** — "the pinned compiler silently miscompiles indexed reads of the flat
  learner-state arena once `c15_base.zag` is in the unit".
* **B17** — "bogus type errors on large translation units".

Both B16 and B17 are said to be toolchain barriers that would invalidate
large swaths of the corpus. They must be settled with evidence, not prose.

## 1. Pre-analysis of the reporter's own artifacts (done BEFORE writing probes)

Read-only inspection of `p1_lifetime_ab/{DEFECT.md,probe_defect.zag,
probe_defect_with_base.zag,probe_defect_out.txt,probe_defect_with_base_out.txt}`.

Two facts, both checkable without running anything:

1. **`probe_defect_with_base.zag` is 41 lines and contains NO copy of
   `c15_base.zag`.** Its own header comment claims "the frozen, unmodified
   c15_base.zag (174 lines) followed by the 40-line probe body". It does not.
   Its build log ends `znc: build aborted` with 21 × `unknown function:
   z_alloc|set32|get32` and `[zbuild] COMPILE-FAIL rc=1`.
   **=> The reporter's entire "with the base it FAILS" leg produced no program
   and no output. It is not evidence of anything.**
2. **The reporter's "PASSING" leg is the leg that printed the numbers.**
   `probe_defect.zag` DID run, 3/3 deterministically, and DID print
   `A_off_plus_j 11 1761607680 6881280 26880 105 838860800`.
   So the anomalous values occur in the *control*, not the treatment.

Arithmetic hypothesis H1 (to be verified **inside Zag**, not by hand):
`A` is `get32(C,4+j)` for `j=0..5`, i.e. a **byte**-offset sweep at offsets
4,5,6,7,8,9 — NOT an i32-cell sweep. The reporter's own source comment says
"Expected contents ... 11 105 50 11 106 60" and silently compares a byte-offset
read against an i32-slot expectation. Under H1 each "garbage" value is the
*correct* gather of the *correct stored bytes* at an unaligned offset:
`105<<24`, `105<<16`, `105<<8`, `105`, `50<<24`.
H1 predicts: `1761607680 = 105*2^24`, `6881280 = 105*2^16`,
`26880 = 105*2^8`, `838860800 = 50*2^24`. All four must hold exactly.

If H1 holds, B16 is a defect in the **test**, not in the compiler: a
mis-specified oracle. It predicts the "garbage" is byte-exact and fully
explainable, and predicts a correctly-aligned sweep disagrees 0 times.

## 2. Preregistered probes

All probes: pure Zag, single `fn main(`, built with
`tools/zbuild.sh ./X.zag --rep 3` (determinism bar), all output via
`_zag_print` / `_zag_println` (never `o_flush` — inert, B15/B13).

**P1 (C501) — minimal B16 reproducer, self-contained.**
`z_alloc` per brief section 3.1 *verbatim*:
`let p:*u8=_zag_malloc(n) as *u8; let b:[]u8=p[0..n];` then zero loop.
Stores `11,105,50,11,106,60` at byte offsets 4,8,12,16,20,24.
Emits, for j=0..5: (a) `get32(C,4+j)` [byte sweep], (b) `get32(C,4+j*4)`
[cell sweep], (c) an index-free reference for the byte sweep
`b[4+j]|(b[5+j]<<8)|(b[6+j]<<16)|(b[7+j]<<24)`.
Kill bar: if (a) != (c) for any j, the compiler really does miscompute a
gather. Prediction under H1: (a)==(c) for all 6, and (a) equals the shifted
products above, NOT the cell values.
*No other lane's base file.*

**P2 (C502) — the reporter's exact condition, done correctly.**
`c15_base.zag` (frozen, unmodified, 174 lines, concatenated) + the P1 body.
Must COMPILE and must print byte-identical P1 numbers to the no-base control.
Prediction under H1: the two outputs are IDENTICAL. Any difference would
support B16.

**P3 (C503) — systematic sweep, the core experiment.**
Grid: 4 allocation sizes {64, 512, 4096, 110656} × 8 base offsets
{0,1,2,3,4,7,8,60} × 8 strides {1,2,3,4,5,8,12,40} × 8 indices {0..7}.
For every grid point the compiler-computed `get32(b,off+i*st)` is compared
against a reference assembled by **four separate scalar byte reads with
literal-plus-index addresses and no multiplier** (a distinct expression
shape). Count mismatches over all cells.
Metric: `disagree = mismatches / comparisons`.
Prediction under H1: **disagree == 0 exactly** (both forms index the same
bytes; the reference is not a privileged oracle, it is the same indexing
applied to the same offsets). Kill bar for B16: disagree > 0.
Also reports a content-checksum so a silently-truncated arena would show up.

**P4 (C504) — B17 large-TU probe.**
Generated *inside Zag* (no shell codegen): one `fn` per block, chained by
forward calls, at TU sizes ~1k, ~2k, ~4k, ~8k lines. Each block does
arena work and returns i32. Reports the largest TU that compiles AND runs
AND whose result equals the small-TU result.
Prediction: results identical at every size → B17 is not size-dependent.

**P5 (C505) — brief section 5 constraint audit, one binary.**
Six micro-probes, each in its own `fn`, invoked in order, each printing
PASS/FAIL:
 1. `while` with `&&` in the condition.
 2. `while` with `||` in the condition.
 3. De Morgan form `(!A || !B)` in `while`.
 4. bare `!(A&&B)` in `while`   ← brief says forbidden
 5. bare `!A` in `while`        ← brief says forbidden
 6. `if`-nesting depth 1..5, deepest reached recorded
 7. `for` loop                   ← brief says no `for`
Each in its own fn so one failure cannot poison the others; a compile abort
kills the whole binary, so these are additionally run as SEPARATE binaries.
Prediction: 1,2,3,6(<=3) PASS; 4,5,7 are real restrictions (or cargo cult —
determined by whether the compiler emits a clear diagnostic vs silently
misbehaving).

## 3. Falsification / kill bars (fixed in advance)

* B16 survives ONLY IF P1/P3 find at least one cell where the indexed
  gather disagrees with the scalar-byte reference, OR P2 differs from P1.
* B17 survives ONLY IF P4 finds a size at which a previously-passing TU
  stops compiling, or starts producing a different result.
* Any constraint in section 5 is only "REAL" if the forbidden construct
  produces a compiler diagnostic. A construct that compiles and works is
  CARGO CULT and the brief should be corrected, not obeyed.

## 4. Honesty clauses

* If P3 finds disagreement I cannot explain, I report B16 as REAL and give
  the minimal grid cell that triggers it. I do not explain it away.
* I will not modify `c15_base.zag` or any other lane's file.
* All commits use explicit pathspecs. No `git commit -a`. No git in main repo.