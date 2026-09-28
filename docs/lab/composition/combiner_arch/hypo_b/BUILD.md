# H-B DELTA — Build Record

## Source identity

- Implementation: `delta.zag` (pure Zag, zero RNG, no per-item hardcodes)
- Frozen D1 source: `docs/lab/composition/battery_amended/items.tsv`
- Source commit: `03ba8919e915224e7b0f393ed10740f8c4547661`
- Commit timestamp: `2026-09-27 15:49:44 -0700`
- D1 rules (6): `reverse`, `dupfirst`, `rotleft`, `droplast`, `upperfirst`, `sortchars`
- Frozen file: 12 TEACH + 8 P0 held-out probes per rule (MAX_EX=16 permits all 12)

## Toolchain

- Pinned compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Compiler version: `znc 2026.07.0-dev (edition 2026)`
- Compiler SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
- Substrate: `R33_NATIVE_IO_V1.zag` (Linux x86-64 port, `@import`ed for `nio_alloc`/`nio_free`)
- Binary SHA-256: `d38ee13f86bbf7ab1a95742cfc1688ff51e09f5f8985052315a8208f9f87c199`
- Binary size: 134,941 bytes (NOT committed to repo; build artifact only)

## Architecture

Pure-Zag implementation of the H-B DELTA specification:

1. **LE arena accessors**: All tables use `[]u8` arenas with explicit little-endian
   `d_p32`/`d_g32`/`d_gi32` accessors. No `as []i32`/`as []u32`/`as []u16` casts
   anywhere (ZNC-2026-09-21-007 avoidance). Verified by grep.
2. **Raw-syscall I/O**: File read/write via `_zag_raw_syscall` (open/read/write/close).
3. **TSV teaching parser**: Splits lines on `\t`, groups by RULEID byte-identity.
   RULEIDs are arbitrary labels; the learner groups by identity but never branches
   on content (zero `_zag_strcmp` calls in the entire program — verified by grep).
4. **Per-slot provenance aligner**: For each output byte, enumerates COPY candidates
   (all input positions with equal byte), then MAP-UPPER, then MAP-LOWER, then EMIT.
   Records stored in a flat arena (9 bytes each: kind u8, pad, arg i32).
5. **Mixed-radix deterministic ambiguity enumeration**: Odometer over ambiguous slots
   (slots with >1 provenance candidate). Candidate order: all COPY (increasing input
   index), then MAPU, then MAPL, then EMIT.
6. **Exact affine fitting**: i64 Cramer's rule for s=a*j+b*L+c with forced-zero
   branches (Jvar&&!Lvar → b=0; !Jvar&&Lvar → a=0; constant-k fast path for
   collinear point sets). Exact integer divisibility required.
7. **Fixed six-condition structural splitter**: Try-order j==0, j==M-1, j==1,
   j==M-2, j==2, j==M-3. Budget 3, max 4 clauses. Discovery order = serialization
   order (first match wins).
8. **Attested-byte EMIT rule**: EMIT clauses only for bytes attested in teaching inputs.
9. **Sort-ascending/descending fallback**: Multiset-match detector for sort rules.
10. **Byte-exact training verification**: Every candidate program must reproduce all
    teaching outputs byte-exactly before acceptance.
11. **Apply-time OOB/no-clause withholding**: Structural codes only (UNDERDET,
    NO_LENGTH_RULE, AMBIGUOUS, NO_PROGRAM, OOB, NO_CLAUSE). No confidence thresholds.
12. **Deterministic serialized-program reporting**: Programs printed to stdout in
    fixed format.

## Capability battery results

| Capability | Required | Achieved |
|---|---|---|
| Frozen D1: reverse | 8/8 held-out | **8/8** |
| Frozen D1: dupfirst | 8/8 held-out | **8/8** |
| Frozen D1: rotleft | 8/8 held-out | **8/8** |
| Frozen D1: droplast | 8/8 held-out | **8/8** |
| Frozen D1: upperfirst | 8/8 held-out | **8/8** |
| Frozen D1: sortchars | 8/8 held-out | **8/8** |
| Swap-first-last (new) | 8/8 | **8/8** |
| Sort-descending (new) | 8/8 | **8/8** |
| Caesar shift | Honest withhold on novel input | **WITHHOLD (NO_PROGRAM)** on 3/3 novel probes |
| Single-length teaching | UNDERDET | **WITHHOLD (UNDERDET)** |

**Total: 64/64 probes correct, 0 confident errors.**

Induced programs (from stdout):
- R1 (reverse): `p=1 q=0 [ELSE,COPY,a=-1,b=1,c=-1]`
- R2 (dupfirst): `p=1 q=1 [j==0,COPY,0,0,0] [ELSE,COPY,1,0,-1]`
- R3 (rotleft): `p=1 q=0 [j==0,COPY,0,0,1] [j==M-1,COPY,0,0,0] [ELSE,COPY,1,0,1]`
- R4 (droplast): `p=1 q=-1 [ELSE,COPY,1,0,0]`
- R5 (upperfirst): `p=1 q=0 [j==0,MAP-UPPER,0,0,0] [ELSE,COPY,1,0,0]`
- R6 (sortchars): `p=1 q=0 [ELSE,SORT-ASC]`
- SWAP: `p=1 q=0 [j==0,COPY,0,1,-1] [j==M-1,COPY,0,0,0] [ELSE,COPY,1,0,0]`
- SORTD: `p=1 q=0 [ELSE,SORT-DESC]`

## Acceptance vectors (spec §A)

| Vector | Expected | Achieved |
|---|---|---|
| Reverse taught on abc→cba, wxyz→zyxw, hello→olleh | `p=1,q=0`, one clause `(ELSE,COPY,a=-1,b=1,c=-1)` | **EXACT MATCH** |
| Dup-first | `p=1,q=1`, `(j==0,COPY,0,0,0)`, `(ELSE,COPY,1,0,-1)` | **EXACT MATCH** |
| Rot-left | `p=1,q=0`, `(j==0,COPY,0,0,1)`, `(j==M-1,COPY,0,0,0)`, `(ELSE,COPY,1,0,1)` | **EXACT MATCH** |
| Caesar+1 | `WITHHOLD (NO_PROGRAM)` | **EXACT MATCH** |
| Single-length teaching | `WITHHOLD (UNDERDET)` | **EXACT MATCH** |

**5/5 acceptance vectors pass exactly.**

## Determinism

- Run 1 output SHA-256: `9a760550a3820d7febd3589302abadd89eb7135b2fc24e079e8a135c7d38fd08`
- Run 2 output SHA-256: `9a760550a3820d7febd3589302abadd89eb7135b2fc24e079e8a135c7d38fd08`
- Run 3 output SHA-256: `9a760550a3820d7febd3589302abadd89eb7135b2fc24e079e8a135c7d38fd08`
- MALLOC_PERTURB_=165 output SHA-256: `9a760550a3820d7febd3589302abadd89eb7135b2fc24e079e8a135c7d38fd08`
- Stdout (program serialization) SHA-256 (all 4 runs): `59ff5c36d1ba883448150ddac9c08956e657818406bf7a84f3981dfa12017278`

**Verdict: byte-identical across 3 runs + allocator perturbation. Deterministic.**

## Static checks

- `as []i32` / `as []u32` / `as []u16`: **zero** in code (one comment mentions them)
- `rand`: **zero** matches
- `time`: **zero** matches (one comment contains "sometimes")
- `_zag_strcmp`: **zero** calls (no rule-name branches anywhere)
- Rule names (`reverse`, `dupfirst`, etc.): **zero** occurrences in learn/apply logic

## Deviations from spec

### DEVIATION 1: Fewest-clauses selection across ambiguity assignments (vs §5.4 "first verifying")

**Spec text (§5.4):** "first verifying assignment in odometer order."

**What was built:** All odometer assignments are enumerated; among those whose
induced program verifies byte-exactly on teaching, the program with the **fewest
clauses** is selected (tie-break: earliest odometer order).

**Why:** The acceptance vectors (§A) require minimal programs:
- reverse must serialize exactly one clause `(ELSE,COPY,a=-1,b=1,c=-1)`
- dupfirst must serialize exactly two clauses
- rotleft must serialize exactly three clauses

With ambiguous provenance (e.g. repeated bytes like 'l' in "hello"), the first
odometer assignment often yields an overfit program with MORE clauses that still
verifies on teaching (it memorizes the specific disambiguation). For example,
reverse's first assignment yielded a 4-clause program; the minimal 1-clause
program was found at a later assignment. Strict "first verifying" would fail
3/5 acceptance vectors. Fewest-clauses is deterministic and satisfies all
acceptance vectors exactly.

### DEVIATION 2: Constant-k fast path in affine fitting (vs §5.6 Cramer's rule only)

**Spec text (§5.6):** "Exact affine fitting with i64 Cramer's rule and forced-zero branches."

**What was built:** Before the jd/ld variance analysis, if all k values in the
span are equal, the fit returns `a=0,b=0,c=k` immediately.

**Why:** Cramer's rule requires 3 non-collinear (j,L) points. For spans like
`(j==M-1)` in rotleft — triples (3,4,0),(2,3,0),(4,5,0) — the (j,L) points are
collinear (they lie on j==M-1), so no independent triple exists, yet the correct
fit is the constant s=0. Without this path, rotleft's required
`(j==M-1,COPY,0,0,0)` clause cannot be induced and the rule withholds (failing
the acceptance vector). The fast path is exact (verifies k equality on all
triples) and deterministic.

### DEVIATION 3: Clause-page capacity enforcement (vs §5.6 "budget 3 (≤4 clauses)")

**Spec text (§5.6):** "budget 3 (≤4 clauses)."

**What was built:** `d_cl_add` returns 0 (failure) when the 4-clause page is full;
`d_one_clause` propagates this as fit failure, causing the splitter to backtrack.

**Why:** The recursive budget (budget-1 per level) permits up to 8 clauses in a
fully-split tree (2 children × 2 children × 2 children), exceeding the 4-clause
page. Without enforcement, a 5th clause write overflows the 80-byte page
("slice index out of bounds" panic, observed 2026-09-28). The capacity check
makes "≤4 clauses" a hard structural invariant; the splitter backtracks and
tries other decompositions. This is a safety hardening, not a semantic change:
no valid ≤4-clause program is rejected.

### Ambiguity recorded (not a deviation): candidate order tension (§1.1 vs §5.4)

**§1.1:** "all COPY candidates, then all MAPU, then all MAPL."
**§5.4:** "scanning each k and taking its first COPY→MAPU→MAPL match"
(i.e. interleaved by k).

**What was built:** §5.4's interleaved order (for each input position k, in
increasing k: COPY(k), then MAPU(k), then MAPL(k)).

**Rationale:** §5.4 is the operational procedure; §1.1 describes the kind
priority which §5.4 refines per-position. The acceptance vectors pass under
this reading. If §1.1's kind-major order was intended, the odometer would
enumerate differently, but fewest-clauses selection (Deviation 1) makes the
outcome robust to this ordering choice for the tested vectors.

### Ambiguity recorded (not a deviation): multi-rule example contiguity

The implementation assumes each rule's teaching examples occupy a contiguous
range in the example table (they are grouped by RULEID at parse time into
per-rule blocks). The shared interface requires grouping arbitrary RULEIDs but
does not explicitly promise grouped line ordering. The parser groups by
scanning: for each distinct RULEID (in first-appearance order), it collects all
lines with that ID. This handles interleaved labels correctly (deterministic
regrouping without branching on label content). No deviation: behavior is
defined for arbitrary input order.

## Files

- `delta.zag`: implementation (pure Zag)
- `R33_NATIVE_IO_V1.zag`: substrate import (copy of pinned toolchain file)
- `fixtures/`: acceptance fixtures + D1 battery fixtures + swap/sortd/caesar fixtures
- `runs/`: run outputs (byte-identical across runs)
- `BUILD.md`: this file

## Test commands

```bash
# Build
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 delta.zag -o delta

# Acceptance vectors
./delta fixtures/acc_reverse_teach.tsv fixtures/acc_probe.tsv runs/acc_reverse.tsv
./delta fixtures/acc_dupfirst_teach.tsv fixtures/acc_probe.tsv runs/acc_dupfirst.tsv
./delta fixtures/acc_rotleft_teach.tsv fixtures/acc_probe.tsv runs/acc_rotleft.tsv
./delta fixtures/acc_caesar_teach.tsv fixtures/acc_probe.tsv runs/acc_caesar.tsv
./delta fixtures/acc_single_teach.tsv fixtures/acc_probe.tsv runs/acc_single.tsv

# Capability battery (96 teach, 64 probe)
./delta fixtures/battery_teach.tsv fixtures/battery_probe.tsv runs/battery_out.tsv

# Determinism
./delta fixtures/battery_teach.tsv fixtures/battery_probe.tsv runs/b1.tsv
./delta fixtures/battery_teach.tsv fixtures/battery_probe.tsv runs/b2.tsv
./delta fixtures/battery_teach.tsv fixtures/battery_probe.tsv runs/b3.tsv
MALLOC_PERTURB_=165 ./delta fixtures/battery_teach.tsv fixtures/battery_probe.tsv runs/bP.tsv
sha256sum runs/b1.tsv runs/b2.tsv runs/b3.tsv runs/bP.tsv  # must match
```
