# RESULT: H-CAUSALEXP-CONSTRUCT Transfer/Reuse (cxconstruct_transfer)

Date: 2026-09-30.
Worker verdict: **TRANSFER-PARTIAL**.
Prereg: `PREREG_TRANSFER.md` (frozen at 1a3307b79, before implementation).
Source: `cxtransfer.zag` (pure Zag).
Raw: `CXTRANSFER_RAW.txt` (md5 97054b6023ae0173bb6e78f74940cb2e).

## Kill bar results

### K-TR1 (T1 primitive parameterization): PASS

T1 DEPTH 1 checked=3 found=0
T1 DEPTH 2 checked=27 found=0
T1 DEPTH 3 checked=6 found=1
T1 SELECT seq=[S,W,OX] h0pred=1 h1pred=0
T1 uses_OX=1 total_checked=36

The learner, given 6 primitives, constructed [S,W,OX] using the new
OX primitive. The enumeration base is parameterized by primitive
count (nprim variable); code inspection confirms no `total=total*4`
literal. The base-6 enumeration (9330 sequences depths 1-5) works
correctly.

### K-TR2 (T2 threshold transfer): PASS

T2 DEPTH 1 checked=1 found=0
T2 DEPTH 2 checked=7 found=0
T2 DEPTH 3 checked=3 found=1
T2 SELECT seq=[S,W,OY] h0pred=0 h1pred=1

The learner, given threshold rules (AND vs OR) instead of delay
rules, constructed [S,W,OY]. The enumerate-filter-select loop is
unchanged; only the simulator handles threshold semantics. The
principle transfers to different rule semantics.

### K-TR3 (T3 concept transfer): PASS

T3 obj=(red,round) h0=1 h1=1 agree
T3 obj=(red,square) h0=1 h1=0 DISAGREE
T3 SELECT obj=(red,square) h0pred=1 h1pred=0

The learner selected (red,square), the first object with disagreeing
predictions. This is a static concept learning domain, not sequential
causal experiments. The "enumerate candidates, predict under
hypotheses, select by disagreement" principle transfers to a
non-sequential, non-causal domain.

### K-TR4 (T4 composition): FAIL

T4a DEPTH 1 checked=2 found=0
T4a DEPTH 2 checked=12 found=0
T4a DEPTH 3 checked=56 found=0
T4a DEPTH 4 checked=16 found=1
T4a total_checked=86 flen=4

T4b DEPTH 1 checked=2 found=0
T4b DEPTH 2 checked=16 found=0
T4b DEPTH 3 checked=86 found=1
T4b total_checked=104 flen=3 uses_M=1

T4a (from-scratch): found [S,W,W,OZ] at depth 4, 86 checked.
T4b (with macro M=[S,W]): found [M,W,OZ] at depth 3, 104 checked,
uses_M=1.

The macro enables a shallower solution (depth 3 vs 4) and is used,
but T4b checks MORE sequences (104) than T4a (86). The larger
primitive set (base-5 vs base-4) increases branching at depths 1-2
enough to outweigh the shallower solution depth. Per the frozen
criterion (T4b must check strictly fewer than T4a), K-TR4 FAILS.

This is an honest negative result: providing a macro abstraction
does not reduce search cost in this architecture. The learner cannot
exploit the abstraction to prune the search space; it still
enumerates all combinations including those not using the macro.

### K-TR5 (determinism): PASS

3 runs, byte-identical (cmp), exit 0, zero stderr.
md5 97054b6023ae0173bb6e78f74940cb2e.

### K-TR6 (purity): PASS

Pure Zag (znc build; bash/cmp/md5sum only). Zero Python invocations.
Zero em dash bytes (byte-verified).

## Verdict: TRANSFER-PARTIAL

3 of 4 transfer tests pass (K-TR1, K-TR2, K-TR3). K-TR4 fails.
Per frozen criteria: TRANSFER-PARTIAL (2-3 of K-TR1..K-TR4).

## Interpretation

The disagreement-filter principle shows partial generality:

**What transfers:**
- New primitive vocabularies (T1): The enumeration machinery
  parameterizes correctly. Adding primitives works.
- New rule semantics (T2): Threshold rules instead of delay rules.
  The loop is unchanged; only the simulator differs.
- New domains (T3): Static concept learning. The abstract
  "enumerate, predict, select by disagreement" applies.

**What does not transfer:**
- Compositional reuse (T4): Providing a macro does not help. The
  architecture enumerates from scratch and cannot exploit
  abstractions to prune search. This is a fundamental limitation:
  the learner has no mechanism for hierarchical composition or
  reuse of partial solutions.

**Net:** The filter principle is more general than the specific
delay-rule setup, but the architecture is not compositional. It is
a one-level enumerate-and-filter, not a hierarchical builder. This
is consistent with the A1/A2 finding: researcher owns the
enumeration structure; learner owns only the filter.

## Honest limitations

- T2 and T3 required new simulators. The transfer is of the
  principle, not the implementation.
- T1 tests parameterization, not conceptual leap.
- T4b provided the macro; macro invention was not tested.
- All worlds synthetic and tiny.
- Step 9 of 11. Steps 10 (red team, done) and 11 (governance)
  remain.

## Files

- `PREREG_TRANSFER.md` (frozen 1a3307b79)
- `cxtransfer.zag` (implementation)
- `CXTRANSFER_RAW.txt` (md5 97054b6023ae0173bb6e78f74940cb2e)
- `CXTRANSFER_RESULT.md` (this file)
