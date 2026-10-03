# PREREG H-UNIFIED6: Programmatic Parse-Anomaly Flag + Defense-in-Depth Shape Verification

**Date:** 2026-09-29
**Status:** FROZEN. No implementation exists yet. Any implementation commit must strictly descend from this commit.
**Base:** `unified5_learn.zag` (H-UNIFIED5, committed in the H-UNIFIED5 result; red-team SURVIVES at `cb5da73a6`), copied verbatim then hardened.
**Target:** `unified6_learn.zag` (new file; `unified5_learn.zag` untouched).
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.

## Background

H-UNIFIED5 SURVIVES (17/17). Independent red team
(`unified5_adversary/U5_ADV_RESULT.md`, prereg `916c64de1`, result
`cb5da73a6`): all four attacks FAIL. Clean survival.

The red team left two honest residuals (not kill-worthy, recorded in
U5_ADV_RESULT.md):

1. "Skip-and-continue recovery is flagged by text trace only; there is
   no programmatic anomaly flag on the recovered values. A direct
   white-box caller that ignores stdout could act on split/shifted
   values." ADDRESSED HERE (R1).
2. "The shape overflow is fail-stop (panic) rather than silent, but it
   is still a crash-class hazard if classification is ever bypassed.
   Defense remains single-layer (route_line field_kind)." ADDRESSED
   HERE (R2: the parser itself becomes capacity-safe, and the handlers
   verify shapes as a second layer).

A third residual (K-U5-1 probe-vehicle deviation) is lineage-only and
needs no code change.

## The hazards (confirmed by reading)

H1: `parse_ints` returns void. The only anomaly signal is the
PARSE_GUARD text trace. A caller that does not read stdout cannot
detect that recovery happened.

H2: `parse_ints` writes `set32(out,idx*4,v)` with no capacity check.
A field with more valid numbers than `out` holds writes past the
buffer (the red team proved clobbering through a 16-byte view, and a
fail-stop panic on a 12-byte-exact view). On dispatch paths
`route_line`/`field_kind` classification guarantees exact shapes, but
the handlers (`handle_caus_learn`, `handle_caus_revise`,
`handle_caus_query`) re-parse without re-verifying: single-layer
defense.

## Hardening design (frozen)

### R1: parse_ints returns a programmatic anomaly code

New signature (frozen):

```text
fn parse_ints(b:[]u8, lo:i32, hi:i32, out:[]u8)i32
```

Frozen contract:

- `cap = out.len/4` (integer division). The parser NEVER writes at an
  index with `idx*4+4 > out.len`. When a value completes while
  `idx == cap`, the parser stops immediately and returns -1
  (SHAPE_OVERFLOW). No write past the buffer happens, so no panic is
  possible from the parser, and no silent arena corruption is
  possible through a short view.
- Otherwise the parser returns the count of skipped non-digit bytes
  (>= 0; 0 means a clean parse). The PARSE_GUARD text traces are
  retained verbatim for human audit.
- On the -1 path one PARSE_SHAPE trace line is emitted (distinct text,
  so it cannot be confused with PARSE_GUARD), then -1 is returned.
- Skipped bytes still consume no output slots (unchanged H-UNIFIED5
  behavior). Values already written before a -1 stop are the first
  `cap` values of the field.
- On valid inputs (digits and commas only, fitting the buffer) the
  function returns 0 and writes exactly what H-UNIFIED5 wrote:
  byte-identical behavior on every frozen path.

Callers: every existing call site binds the return
(`let prc:i32=parse_ints(...);`). The two K-U5-1 probe calls bind
with `let _u51a:i32=` / `let _u51b:i32=`; their emit text is
unchanged, so the K-U5-1 block output stays byte-identical.

### R2: handler-layer shape verification (second layer)

`handle_caus_learn` (per segment, on `sline`):

- If `gt<0`, or `field_kind(sline,pos,gt)!=3`, or
  `field_kind(sline,gt+1,end)!=2`: emit
  `USHAPE: segment skipped (expected 3-int>2-int episode) [...]`
  and continue to the next segment. No parse, no commit, no panic.
- Else parse both fields, binding returns. If either return is -1
  (unreachable given the field_kind gate, but the second layer does
  not trust the first): emit `USHAPE: segment skipped (parser
  capacity) [...]` and continue.
- Else the original body runs unchanged.

`handle_caus_revise` (per segment, on `body`): identical gating.

`handle_caus_query`: if `field_kind(line,0,line.len)!=3`: emit
`QCAUS USHAPE WITHHOLD: expected single 3-int tuple` and return 0.
Else parse (bound return), original body unchanged.

New traces fire only on malformed input. Every classified dispatch
path supplies exact shapes, so the 16 frozen blocks emit zero new
lines: their output stays byte-identical to H-UNIFIED5.

### What is NOT changed

- `route_line`, `operator_route`, `clearn`, the coherence gate,
  Repair B accounting, procedure/bridge stores, proc query paths:
  behavior identical to H-UNIFIED5.
- No emit text on any frozen path is altered. The header line changes
  `v5` to `v6` by design (line 1 only).
- No capacity-policy change (refuse-with-warning stands; H-MEM lane
  owns eviction).
- `main()`: all 16 H-UNIFIED5 frozen blocks copied verbatim; the
  K-U5-1 block kept (two call lines gain return bindings, zero output
  change); two new blocks appended for K-U6-1 and K-U6-2 before the
  final tally. The tally becomes 20/20.

## Frozen kill bars

### K-U6-1: programmatic skip flag (new)

Direct white-box probes in main(), assertions in code (no stdout
scraping):

1. `parse_ints("1,0x,0",0,5,p1)` returns 1 and p1 holds [1,0,0].
2. `parse_ints("1,0,0",0,5,p2)` returns 0 and p2 holds [1,0,0].
3. `parse_ints("!!!",0,3,p3)` returns 3 and p3 holds no values
   (get32(p3,0)==0).

PASS iff all three in-code assertions hold. KILL iff any assertion
fails (the flag lies) or the parser hangs.

### K-U6-2: defense-in-depth shape verification (new)

Five in-code subchecks:

a. Parser capacity: 32-byte arena filled with canary 0xAAAAAAAA;
   12-byte view passed as `out`; `parse_ints("1,0,0,5",0,7,view)`
   returns -1; view holds [1,0,0]; `get32(arena,12)` still equals the
   canary (no write past the view). No panic.
b. Learn handler: `handle_caus_learn(W,"1,0,0,5>9,9;1,0,0>9,9")`
   (direct call, bypassing route_line) returns 0 stored, emits USHAPE,
   no panic, no commit.
c. Revise handler: `handle_caus_revise(W,"!1,0,0,5>9,9")` returns 0
   stored, emits USHAPE, no panic, no commit.
d. Query handler: `handle_caus_query(W,"1,0")` returns 0, emits
   USHAPE withhold, no panic.
e. Missing separator: `handle_caus_learn(W,"1,0,0;2,0,0")` returns 0
   stored, emits USHAPE per segment, no panic, no commit.

PASS iff all five hold. KILL iff any subcheck panics, commits a bad
episode, or silently accepts a bad shape.

### K-U6-3: no regression in the 16 frozen checks

All 16 H-UNIFIED5 frozen checks pass. Output lines 2-125 of the new
binary are byte-identical to lines 2-125 of the committed
`UNIFIED5_RAW_OUTPUT.txt` (verified by diff/cmp). The K-U5-1 block
region is additionally verified byte-identical (its two probe calls
gain return bindings with zero output change).

### K-U6-4: determinism

Three full runs of the final binary are byte-identical (cmp). md5
recorded in the result doc.

### K-U6-5: new layers never fire on frozen inputs

`grep -c` over output lines 2-125: PARSE_GUARD == 0 and USHAPE == 0.
(The only PARSE_GUARD/PARSE_SHAPE/USHAPE lines in the full output
are inside the K-U5-1/K-U6-1/K-U6-2 blocks.)

## Honest limitations (frozen)

1. The parser is capacity-safe but not a validator: under-reads (too
   few numbers) are refused at the handler layer via field_kind, not
   inside parse_ints. A direct white-box caller that skips the handler
   layer and reads unwritten slots still sees z_alloc zeros; that
   caller is outside every audited path.
2. `hi > b.len` / `lo < 0` are caller-contract violations, unchanged
   from H-UNIFIED5; all in-tree callers derive bounds from find_ch and
   line lengths.
3. Deployment still needs a genuinely separate authenticated operator
   channel (carried from H-UNIFIED5 limitation 2).
4. Capacity remains refuse-with-warning; principled eviction is H-MEM
   lane future work (carried from H-UNIFIED5 limitation 4).
5. The stale cosmetic string noted by the U5 red team (old version
   naming in a header comment of an ancestor file) is left untouched:
   changing frozen emit text would break K-U6-3 byte-identity for
   zero behavioral gain.

## Commit plan

1. This prereg (frozen, alone).
2. Implementation: `unified6_learn.zag` (R1 + R2 + K-U6-1/K-U6-2 main
   blocks) + `UNIFIED6_RAW_OUTPUT.txt` (3 runs) +
   `UNIFIED6_RESULT.md`.
3. No amendment unless a harness bug is found; any amendment will be
   transparent and will not change kill criteria.

## Classification sought

Bounded L2 integration hardening, not L3. Makes parse anomalies
machine-readable and shape safety two-layered; changes no learned
behavior.
