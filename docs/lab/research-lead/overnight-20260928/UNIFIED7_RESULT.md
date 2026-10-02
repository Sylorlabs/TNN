# H-UNIFIED7: RESULT

**Date:** 2026-09-29
**Verdict: H-UNIFIED7 SURVIVES (22/22).**
**Target repair:** X-U6-2 (digit-magnitude gate bypass), the claim-narrowing
finding from the H-UNIFIED6 red team (`u6_adversary/U6_ADV_RESULT.md`).
**Prereg:** `PREREG_UNIFIED7.md`, committed alone at `5c92d3bdd`
before any implementation edit, build, or run. No amendments.
**Purity:** Pure Zag throughout. No Python at any stage.

## Lineage

- Prereg frozen BEFORE any implementation: `PREREG_UNIFIED7.md`,
  commit `5c92d3bdd` (alone; only the prereg staged).
- Implementation: `unified7_learn.zag` = `unified6_learn.zag`
  (mechanism at `ad82aba60`) copied verbatim (cmp-verified) plus
  exactly the frozen R8 change set; `unified6_learn.zag` untouched.
- Result: this commit. Only H-UNIFIED7-owned paths staged.
- Ancestor check: `git merge-base --is-ancestor 5c92d3bdd HEAD`
  verified at commit time.

## The repair (R8, frozen in prereg)

`parse_ints` gains exact magnitude validation with no wider type:

- A digit run of 11+ digits is rejected unconditionally (value >=
  10^10 > 2147483647, overflow guaranteed).
- A 10-digit run is checked before folding the 10th digit: the
  9-digit prefix v9 <= 999999999 fits i32 exactly, so the test
  `v9 > 214748364 || (v9 == 214748364 && dig > 7)` is exact.
- Runs of 9 or fewer digits always fit i32.

On magnitude overflow the parser emits one loud trace and returns
the new distinct anomaly code -2 (MAGNITUDE_OVERFLOW) immediately;
no value from the field is committed. Trace (frozen verbatim):
`PARSE_MAG: digit run exceeds i32 range; field rejected
(H-UNIFIED7)`. Return-code space is now: >= 0 = skipped-byte count
(0 = clean), -1 = SHAPE_OVERFLOW, -2 = MAGNITUDE_OVERFLOW.

Handlers: `handle_caus_learn` and `handle_caus_revise` widen
`if(plc==-1 || prc==-1)` to `if(plc<0 || prc<0)` with a
magnitude-specific USHAPE trace (`segment skipped (parser
magnitude)`). `handle_caus_query` widens `if(pqc==-1)` to
`if(pqc<0)` and emits `QCAUS USHAPE WITHHOLD: parser magnitude
(H-UNIFIED7)`. No wrapped key ever reaches `cpredict`; no parse, no
commit, no panic.

## Frozen kill-bar evidence

Raw: `UNIFIED7_RAW_OUTPUT.txt` (md5
`1db7ed6ea1b51c8b6cd9c2d8a5422e80`), 3/3 runs byte-identical (cmp),
exit 0, built with `znc 2026.07.0-dev (edition 2026)`.

- **K-U7-1 PASS:** direct `parse_ints` probes: `"2147483648"`
  -> -2; `"99999999999999999999"` -> -2;
  `"123456789012345678901234567890"` -> -2;
  `"2147483647"` -> 0 with exact value 2147483647 (boundary
  accepted); `"2147483646"` -> 0 with exact value. Four
  PARSE_MAG traces, zero silent wraps.
- **K-U7-2 PASS:** red-team F2 fixture through the real handler:
  `handle_caus_learn(W,"2147483648,0,0>1,2")` -> 0 stored with
  PARSE_MAG + USHAPE magnitude traces; `handle_caus_revise` on the
  20-digit operator line -> 0; `handle_caus_query` on
  `"2147483648,0,0"` -> withhold (return 0) with the magnitude
  trace. Causal store has 0 active rules. `s0==-2147483648` appears
  zero times in the raw output (grep-verified): the silent commit
  is closed.
- **K-U7-3 PASS:** 3/3 byte-identical (cmp), same md5 all runs.

Regression (K-U7-2 covers the 20 preserved blocks):

- All 20 preserved main() blocks PASS verbatim: 22/22 total, 0
  FAIL lines in raw.
- The binary output up to the new K-U7-1 banner is byte-identical
  to the rebuilt frozen `unified6_learn.zag` (at `ad82aba60`)
  binary's output (diff-verified): the repair adds output only in
  magnitude-overflow situations, which never occur on the frozen
  fixtures.
- Source diff unified6 -> unified7 is exactly the frozen change
  set: header R8 note, parse_ints digit-run tracking +
  MAGNITUDE_OVERFLOW branch, three handler guard widenings with
  distinguishing traces, K-U7-1/K-U7-2 blocks, verdict strings.

## What the verdict means

The R1 claim is restored to its full literal scope: the
programmatic anomaly flag now covers skipped bytes, field-count
overflow, AND digit-magnitude overflow. A caller that ignores stdout
learns of magnitude overflow from the -2 return code (or the 0
from a handler whose segment was loudly skipped); no wrapped value
is ever committed or used as a query key. The X-U6-2 hazard class
(caller acting on wrapped values with no signal) is closed at the
mechanism level.

## Governance disclosures

- Pure Zag: fixtures, harness, builds, greps, md5, cmp. No Python
  at any stage.
- No binaries committed (builds in /tmp/u7 only).
- No em dashes in loop documentation.
- Staging: only `unified7_learn.zag`, `UNIFIED7_RAW_OUTPUT.txt`,
  `UNIFIED7_RESULT.md` (prereg already committed). Concurrent
  workers' files untouched.
- `unified6_learn.zag` and `unified5_learn.zag` untouched.

## Audit finding (not in repair scope, recorded for the research director)

The same unbounded-accumulator pattern (`v=v*10+digit` with no
width check) was found by reading in `unified_learn.zag:854`
(H-INTENT-UNIFIED5) and `unified_fdcr4.zag:838` (H-FDCR-UNIFIED4),
and in causal/router/learn-family variants across the tree. The
wrap is a toolchain-semantics property, not U6-local. This repair
closes it only in the H-UNIFIED7 line; sibling mechanisms keep
their own lanes and their own preregs.

## Classification

Bounded L2 integration repair (parser hardening). Not L3.

## Files

- Prereg: `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/PREREG_UNIFIED7.md` (commit `5c92d3bdd`)
- Mechanism: `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/unified7_learn.zag`
- Raw: `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/UNIFIED7_RAW_OUTPUT.txt`
- This result: `~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/UNIFIED7_RESULT.md`
