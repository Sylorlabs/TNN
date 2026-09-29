# PREREG H-UNIFIED5: Parser Hardening + Explicit Capacity Boundary

**Date:** 2026-09-29
**Status:** FROZEN. No implementation exists yet. Any implementation commit must strictly descend from this commit.
**Base:** `unified4_learn.zag` (H-UNIFIED4, implementation `7048fc3e5`, red-team SURVIVES at `453410a11`), copied verbatim then hardened.
**Target:** `unified5_learn.zag` (new file; `unified4_learn.zag` untouched).
**Purity:** Pure Zag. No Python anywhere, including harnesses and analysis.

## Background

H-UNIFIED4 SURVIVES (16/16). Independent red team
(`unified4_adversary/U4_ADV_RESULT.md`, prereg `4440bfded`, result
`453410a11`): all four attacks FAIL. Clean survival. The call-path
separation holds.

The red team left three suggested follow-ups (not executed, out of
red-team scope):

1. Deployment channel separation needs a future integration experiment
   (outside source scope; NOT addressed here).
2. The `parse_ints` non-digit hazard: "a non-digit, non-comma byte in a
   numeric field would loop without advancing" -- unreachable through
   every dispatch path audited (classification guarantees digit-only
   fields wherever `handle_caus_learn`/`handle_caus_revise` run), "but
   a defensive guard would harden it." ADDRESSED HERE.
3. H-MEM eviction remains the principled answer to the
   refuse-with-warning capacity boundary. NOT changed here (would
   supersede frozen K-U3-2); the boundary is DOCUMENTED more explicitly
   here instead.

## The hazard (confirmed by reading)

```text
fn parse_ints(b:[]u8, lo:i32, hi:i32, out:[]u8)void {
  let idx:i32=0;
  let i:i32=lo;
  while(i<hi){
    let v:i32=0;
    while(i<hi){
      if(is_digit(b[i])==0){break;}
      v=v*10+((b[i] as i32)-48);
      i=i+1;
    }
    set32(out,idx*4,v);
    idx=idx+1;
    if(i<hi && b[i]==44){i=i+1;}
  }
  return;
}
```

Trace with `b[i]` a non-digit, non-comma byte (e.g. `!`, a letter, `>`):

- Inner while: `is_digit(b[i])==0` -> break immediately. `v=0`, `i`
  unchanged.
- `set32(out,idx*4,0)`; `idx=idx+1`.
- `b[i]!=44`, so `i` is NOT advanced.
- Outer `while(i<hi)` repeats with identical `i`: INFINITE LOOP.

The parser is not total. It hangs instead of rejecting or skipping.

## Hardening design (frozen)

Minimal change to `parse_ints` only. No other mechanism code changes.
No emit-text changes on any frozen path. No signature change.

```text
fn parse_ints(b:[]u8, lo:i32, hi:i32, out:[]u8)void {
  let idx:i32=0;
  let i:i32=lo;
  while(i<hi){
    // H-UNIFIED5 defensive guard: a non-digit, non-comma byte previously
    // hung the parser (i never advanced). Skip it with an explicit
    // trace. Dispatch classification guarantees digit-only fields, so
    // this is unreachable on valid inputs; the guard is purely
    // defensive. Skipped bytes are not stored and do not consume an
    // output slot, so valid numbers around them still parse.
    if(is_digit(b[i])==0 && b[i]!=44){
      emit("PARSE_GUARD: skipped non-numeric byte ");
      emit(i32s(b[i] as i32));
      emit(" in numeric field (H-UNIFIED5)\n");
      i=i+1;
    } else {
      let v:i32=0;
      while(i<hi){
        if(is_digit(b[i])==0){break;}
        v=v*10+((b[i] as i32)-48);
        i=i+1;
      }
      set32(out,idx*4,v);
      idx=idx+1;
      if(i<hi && b[i]==44){i=i+1;}
    }
  }
  return;
}
```

Properties (frozen):

- On valid inputs (digits and commas only) the guard branch never
  executes: behavior byte-identical to H-UNIFIED4.
- On invalid inputs the parser always advances: no hang possible.
- The guard emits an explicit trace naming the byte value, so the
  anomaly is visible, never silent.
- Skipped bytes do not consume output slots: `"1,0x,0"` parses as
  `[1,0,0]` with one PARSE_GUARD trace.
- The pre-existing shape contract (exactly 3 ints left, 2 ints right,
  enforced by classification upstream) is unchanged; this guard does
  not widen what the parser accepts as valid, it only prevents hangs
  on invalid bytes.

## Capacity boundary documentation (frozen)

No behavior change. K-U3-2 (refuse-with-warning) must pass unchanged.
The result doc will contain an explicit capacity-policy section:

- Policy: refuse-with-warning. `clearn` rc=-1 on full store;
  `handle_caus_learn`/`handle_caus_revise` emit USTOREFULL per dropped
  episode, count drops in W[DCOUNT()], keep verified knowledge intact,
  never silently lose.
- Limits: 16 causal rules, 32 procedure slots (16 direct + bridge),
  128 pair descriptors. First-writer-wins on the unlabeled stream.
- Why not eviction here: eviction changes the frozen K-U3-2 contract
  (refuse -> evict) and is a cross-lane architectural decision owned
  by the H-MEM eviction work. Adopting it inside H-UNIFIED5 without a
  dedicated eviction hypothesis would be scope creep and would force
  a K-U3-2 supersession on non-evidential grounds.
- A code comment block at the capacity policy site will state the
  policy, the counters, and the H-MEM pointer. Comments do not affect
  output bytes.

## What is NOT changed

- `route_line`, `operator_route`, `handle_caus_learn`,
  `handle_caus_revise`, `clearn`, the coherence gate, Repair B
  accounting, procedure/bridge stores, query paths: behavior identical
  to H-UNIFIED4.
- No emit text on any frozen path is altered.
- `main()`: all 16 H-UNIFIED4 blocks copied verbatim; one new block
  appended for K-U5-1 (guard test) before the final tally. The tally
  becomes 17/17.

## Frozen kill bars

### K-U5-1: guard fires correctly on adversarial input (new)

Fresh workspace W7. Direct white-box probe of the hardened parser via
`handle_caus_query` (which calls `parse_ints` on the raw line):

1. `handle_caus_query(W7,"1,0,x")` completes (no hang) and the raw
   output contains `PARSE_GUARD`.
2. The parse recovers: the query is dispatched as `(1,0,0)` (no crash,
   no corrupt state).
3. `handle_caus_query(W7,"1,0,0")` (valid input) emits no PARSE_GUARD.

PASS iff the adversarial call returns, exactly one PARSE_GUARD trace
appears for the bad byte, and the valid call is guard-silent. KILL iff
the parser hangs (timeout) or the guard does not fire.

### K-U5-2: no regression in the 16 frozen checks

All 16 H-UNIFIED4 frozen checks (12 originals + K-U4-1 + K-U4-2 +
K-U4-5 + K-U3-2) pass. Their output sections are byte-identical to
`UNIFIED4_RAW_OUTPUT.txt` (verified by diff on the frozen blocks).

### K-U5-3: determinism

Three full runs of the final binary are byte-identical (cmp). md5
recorded in the result doc.

### K-U5-4: guard never fires on frozen inputs

`grep -c PARSE_GUARD` over the 16 frozen blocks' output is 0. (The only
PARSE_GUARD lines in the full output are the K-U5-1 block's.)

## Honest limitations (frozen)

1. The guard hardens the parser; it does not validate shapes. A line
   like `"1,0,0,5"` (too many valid numbers) still overflows the fixed
   out buffer exactly as in H-UNIFIED4 -- a pre-existing,
   classification-unreachable hazard, unchanged and documented, not
   introduced here.
2. Deployment still needs a genuinely separate authenticated operator
   channel (carried from H-UNIFIED4 limitation 1).
3. Capacity remains refuse-with-warning; principled eviction is H-MEM
   lane future work (carried from H-UNIFIED4 limitation 4).

## Commit plan

1. This prereg (frozen, alone).
2. Implementation: `unified5_learn.zag` (parse_ints guard + capacity
   comment block + K-U5-1 main block) + `UNIFIED5_RAW_OUTPUT.txt`
   (3 runs) + `UNIFIED5_RESULT.md` (with explicit capacity-policy
   section).
3. No amendment unless a harness bug is found; any amendment will be
   transparent and will not change kill criteria.

## Classification sought

Bounded L2 integration hardening, not L3. Makes the unified learner's
parser total and its capacity boundary explicit; changes no learned
behavior.
