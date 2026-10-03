# PREREG H-UNIFIED7: Magnitude Validation in parse_ints (closes X-U6-2)

**Date:** 2026-09-29
**Status:** FROZEN. No implementation exists yet. Any implementation commit must strictly descend from this commit.
**Base:** `unified6_learn.zag` (H-UNIFIED6, at `ad82aba60` for the mechanism; SURVIVES 20/20, DOWNGRADED by red team), copied verbatim then hardened. New file `unified7_learn.zag`; `unified6_learn.zag` untouched.
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.

## Background

H-UNIFIED6 SURVIVES 20/20. Independent red team
(`u6_adversary/U6_ADV_RESULT.md`, prereg `029e2abd7`, result `01a39f8f0`):
X-U6-1, X-U6-3, X-U6-4 FAIL (defenses hold). X-U6-2 SUCCEEDS on the
preregistered BOUNDARY branch: claim-narrowing finding, not a kill.

The downgrade (frozen in U6_ADV_RESULT.md): `field_kind` has no
per-int width limit and `parse_ints` accumulates `v=v*10+digit` with
no width bound. Digit-magnitude overflow wraps silently to a
mod-2^32 residue: `2147483648,0,0>1,2` was committed as
`IF s0==-2147483648` with the parser returning 0 ("clean parse") and
zero traces of any kind; a 20-digit input stored `s0==1661992959`;
a 30-digit input stored `s0==1312754386`; a query with the same huge
digits wraps identically so the corrupted rule fires on the
corrupted query (self-consistent, wrong vs the true input). The
frozen R1 contract ("0 means a clean parse", "the anomaly rides in
the return value") is false for magnitude overflow. The
programmatic anomaly flag narrows to skipped bytes and field-count
overflow. REPAIRED HERE (R8).

## The hazard (confirmed by reading the red-team evidence)

H3: unbounded digit accumulation. Any digit run of any length passes
`field_kind` as one int. `parse_ints` folds digits into an i32 with
no range check. Values beyond [0, 2147483647] wrap per i32
semantics with no signal: return 0, no trace, corrupted value
committed to the causal store and usable as a query key.

## Hardening design (frozen)

### R8: magnitude validation in parse_ints

New contract addition (frozen): the parser tracks the digit-run
length per value. Overflow detection is exact and needs no wider
type:

- A run of 11 or more digits always has value >= 10^10 >
  2147483647, so it is rejected unconditionally.
- A run of exactly 10 digits is valid iff its value <=
  2147483647. The check is done before folding the 10th digit: the
  9-digit prefix v9 satisfies v9 <= 999999999 (fits i32 exactly),
  so the test `v9 > 214748364 || (v9 == 214748364 && digit > 7)`
  is exact.
- Runs of 9 or fewer digits always fit i32.

On magnitude overflow the parser emits one loud trace and returns
a new distinct anomaly code:

- Return code: -2 (MAGNITUDE_OVERFLOW).
- Trace (frozen verbatim): `PARSE_MAG: digit run exceeds i32
  range; field rejected (H-UNIFIED7)`
- No value from the offending field is committed; the parser
  returns immediately (handler discards the segment, see below).
- Return-code space is now: >= 0 = skipped non-digit byte count
  (0 = clean), -1 = SHAPE_OVERFLOW, -2 = MAGNITUDE_OVERFLOW.

### Handler integration (frozen)

- `handle_caus_learn`: the existing `if(plc==-1 || prc==-1)` guard
  becomes `if(plc<0 || prc<0)`; inside, the trace distinguishes:
  -1 keeps the existing "parser capacity" USHAPE text; -2 emits
  `USHAPE: segment skipped (parser magnitude) [...] (H-UNIFIED7)`.
  No parse, no commit, no panic.
- `handle_caus_revise`: identical change.
- `handle_caus_query`: the existing `if(pqc==-1)` guard becomes
  `if(pqc<0)`; -1 keeps the existing text; -2 emits
  `QCAUS USHAPE WITHHOLD: parser magnitude (H-UNIFIED7)` and
  returns 0. No wrapped key ever reaches `cpredict`.

### What does NOT change (frozen)

- All other `parse_ints` behavior: skip counting, PARSE_GUARD,
  SHAPE_OVERFLOW semantics, value recovery on valid inputs.
- All frozen main() test blocks K-U1-* through K-U6-2b: kept
  verbatim; they must all still PASS.
- `unified5_learn.zag`, `unified6_learn.zag` untouched.

## Frozen kill bars

- K-U7-1: the ready red-team regression (F2): `handle_caus_learn`
  on `"2147483648,0,0>1,2"` stores 0, returns 0, emits PARSE_MAG
  (no silent `s0==-2147483648` commit). Parser-level: direct
  `parse_ints` on `"2147483648"` returns -2; on the 20-digit
  `"99999999999999999999"` returns -2; on the 30-digit fixture
  returns -2. Boundary: `"2147483647"` returns 0 with value
  2147483647 (exact max accepted); `"2147483646"` returns 0.
  Query-level: `handle_caus_query` on `"2147483648,0,0"` withholds
  (return 0) with the magnitude trace.
- K-U7-2: all 20 frozen blocks from H-UNIFIED6 still PASS
  (expected total 22/22: 20 preserved + 2 new).
- K-U7-3: 3/3 runs byte-identical (cmp).

Kill criteria: any K-U7-1 assertion fails, any preserved block
fails, or any non-determinism -> H-UNIFIED7 KILLED (not adopted).

## Audit note (not in repair scope)

The same unbounded-accumulator pattern (`v=v*10+digit` with no
width check) was found by reading in `unified_learn.zag:854`
(H-INTENT-UNIFIED5) and `unified_fdcr4.zag:838` (H-FDCR-UNIFIED4),
and in causal/router/learn-family variants across the tree. The
wrap is a toolchain-semantics property, not U6-local. This repair
closes it only in the H-UNIFIED7 line; sibling mechanisms keep
their own lanes and their own preregs. Recorded as a finding for
the research director, not fixed here.
