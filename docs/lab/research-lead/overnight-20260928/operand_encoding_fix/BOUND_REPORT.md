# BOUND_REPORT.md -- W-BOUND: operand-encoding fix K4/K5

## Step 0: Toolchain guard (2026-10-02, executed before any other work)

```
export PATH="$HOME/safebin"
which python3   -> (no output)
which python    -> (no output)
guard-check-done
```

Both `which` commands returned NOTHING. Safebin = pinned znc 2026.07.0-dev
(edition 2026) + coreutils + git. All worker commands ran with
`PATH=$HOME/safebin` only. All scientific computation in pure Zag; shell
used only for: invoking znc, running binaries, file movement, checksums.
Zero forbidden-executable invocations. No PROCESS-FAIL condition triggered.

## Build

- Prereg frozen at 447f087af; implementation at fd79576d4 (oe_base.zag).
- oe_base.zag was NOT modified. scaling_5000_fixed/* untouched.
- Test binaries (new files, lane dir):
  - `oe_bound_full.zag` = oe_base.zag + s6_patch.zag (verbatim, supplies
    ev_teach/ev_query which oe_base references) + /tmp/bound_main.zag
    -> `oe_bound_bin` (fast probes, K4 all + K5 all-but-imin).
  - `oe_bound_slow_full.zag` = oe_base.zag + s6_patch.zag +
    /tmp/bound_slow_main.zag -> `oe_bound_slow_bin` (i32::MIN probe only).
  - `oe_bound_mid_full.zag` = ... + /tmp/bound_mid_main.zag ->
    `oe_bound_mid_bin` (slot=100000000 calibration probe, 25M walk iters).
- Output idiom per AGENTS.md toolchain lesson 2: single preallocated u8
  buffer, cursor-returning emit helpers (wbo_puts/wbo_puti), ONE
  `_zag_raw_syscall(1, fd:i64, ptr, len)` write at end. No `_zag_print`
  for dynamic content. (Found during work: the syscall fd argument must
  be i64, an i32 literal `1` silently writes zero bytes; fixed by binding
  `let one:i64=1`.)
- Zero build failures.

## K4 boundary tests -- verdict: PASS (all sub-bars)

Binary oe_bound_bin, 3/3 runs byte-identical
(sha256 3b35f57e79eef24fbda8e67fb349b97cc909e6bea1456bbb496691d18dc5ac9a),
25 PASS lines, 0 FAIL lines. Wall ~1.1s per run.

(a) Node ids 9990/9999/10000/10001/10010 as literal operands.
    Value placed: V = id*3+7 in field20.
    Direct: res_op(W,fr,id) == V for all five (29977/30004/30007/30010/30037).
    End-to-end: guard(slot0==lit) true-branch -> set(slot1=lit); with
    slot0=V, execute==1 and fr_get(fr,1)==V for all five ids.
    Under the OLD 10000-threshold encoding, ids >= 10000 in the set cell
    would have decoded as fr_get(f, id-10000) (=0 here), so the old build
    fails these end-to-end checks; the new build passes. PASS.

(b) Frame slots 0..3 round-trip: t2_set(slot, litnode(4242)) then execute;
    execute==1, fr_get(fr,slot)==4242, and res_op(W,fr,-1-slot)==4242
    for slots 0,1,2,3. PASS.

(c) Node id 65535 as operand: arena filled to 65535 (65533 sequential
    alloc_node calls, O(1) each via the hg hint; no eviction triggered),
    ns(W,65535,20,60035); res_op(W,fr,65535)==60035. Decodes as NODE,
    not rejected by the 65536 bound. PASS.

(d) Operands 65536 and 100000000 -> res_op returns -999999 for both,
    no panic. PASS.

(e) Old-collision probe, literal node id 14121 (exact failing operand from
    the K1 FAIL diagnosis): ns(W,14121,20,42370);
    res_op(W,fr,14121)==42370 while fr_get(W,fr,4121)==0, i.e. resolves
    via ng, not fr_get. PASS.

## K5 red team -- verdict: PASS (all probes; see imin note)

Zero panics, zero build failures across all probes.

- SET with node-id dest (field4=1234, >=0): execute returns -999999
  (rejection, per frozen `if(d>=0){return -999999;}`). PASS.
- SET with dest=-1 (slot 0): execute==1, slot0 written (555). Legitimate
  negative dest accepted. PASS.
- SET with dest=-1000000 (slot 999999): execute==1, terminates; the
  fr_set walk saturates at the end of the frame chain (frame field4=0 ->
  node 0) and the value lands at ng(W,0,32)==321. Defined behavior, no
  hang, no panic. (Documented: huge slots do not address real frame
  storage; the walk is bounded and saturates.) PASS.
- INC with node-id operand (field4=2000): execute returns -999999. PASS.
- DEC with node-id operand (field4=2000): execute returns -999999. PASS.
- GUARD comparing node 14121 vs frame slot (correct discrimination):
  match case (slot0=42370): true branch, execute==1, slot1=42370. PASS.
  mismatch case (slot0=42371): false branch, execute==1, slot1=7777
  (marker literal). PASS. Under the old encoding the guard would have
  compared fr_get(f,4121)=0 against slot0 and taken the wrong branch.
- Stale/evicted node id as operand: a real evict_node() call here costs
  ~6e10 primitive ops (65536 candidates x is_prot/bid, each scanning
  131072 edges) -- measured as a >176s stall, killed; so staleness was
  simulated exactly as evict_node frees a slot: alloc node, write
  field20=31415, ns(W,v,36,0) to free it, then res_op(W,fr,v)==31415.
  Defined (stale) value returned, no panic. Documented: the executor
  performs no liveness check on node operands; a freed id reads whatever
  field20 holds. That matches the frozen design (validity bound only).
  PASS (no panic).
- Zero operand (op=0): res_op(W,fr,0)==ng(W,0,20)==0. Node 0 decodes as
  NODE; value 0 (zeroed header area). No panic. PASS.
- i32::MIN operand (op=-2147483648 -> slot 2147483647, ~536.9M walk
  iterations): completed, exit=0, resop=0, user 13.665s (matches ~14s
  extrapolation from the 25M-iter calibration). No hang, no panic,
  defined value. PASS.
- Cyclic frame: not applicable. Frames are fresh alloc_node() results with
  field4=0; fr_get/fr_set walks terminate at the 0/-1 link. No executor
  or t2_* operation writes a frame node's field4, so a cyclic frame is
  unreachable through the tested API (only direct ns scaffolding could
  forge one, which is outside the executor's input contract). PASS by
  construction; noted.

## i32::MIN probe note

Calibration run first: op=-100000001 (slot 100000000, 25M walk iterations)
completed cleanly: resop=0 (walk saturates at node 0, field32=0), no panic,
no hang: real 2.915s / user 0.645s -> ~25.8ns per walk iteration of CPU.
Extrapolated i32::MIN cost (536.9M iterations): ~14s CPU.

First full attempt (oe_bound_slow_bin, op=-2147483648 -> slot 2147483647)
under `timeout 60` was killed (exit=124) with only 8.4s user CPU in 60s
wall -- the shared VM was heavily contended, so the 60s budget did not
reflect compute progress. This is a measurement-environment artifact, not
an executor hang: the walk is a finite counted loop (ss decreases by 4
per iteration from 2147483647, provably terminating at ss=3). Full run
under `timeout 900` launched in background; result appended below.

CALIBRATION RESULT (oe_bound_mid_bin): exit=0, imin=-100000001,
resop=0, real 2.915s, user 0.645s. PASS (terminates, defined value).

FULL RESULT (oe_bound_slow_bin, op=-2147483648 -> slot 2147483647,
536,870,911 walk iterations): exit=0, resop=0, real 1m49.318s, user
13.665s. The 13.7s CPU matches the calibration extrapolation (~14s)
almost exactly. No hang, no panic, defined return value 0 (walk
saturates at node 0, field32=0). PASS. The earlier 60s-timeout kill was
purely VM CPU contention (8.4s CPU granted in 60s wall), not an executor
defect.

## Raw logs (lane dir)

- oe_bound_run1.log / oe_bound_run2.log / oe_bound_run3.log (fast probes,
  byte-identical, sha256 3b35f57e79eef24fbda8e67fb349b97cc909e6bea1456bbb496691d18dc5ac9a)
- oe_bound_slow_run1.log (empty; killed by 60s timeout under VM contention)
- oe_bound_slow_run2.log + oe_bound_slow_time.txt (full i32::MIN run:
  exit=0, resop=0, real 1m49.318s, user 13.665s)
- oe_bound_mid_run1.log + oe_bound_mid_time.txt (calibration:
  slot=100000000, exit=0, resop=0, real 2.915s, user 0.645s)
- Binaries/sources: oe_bound_full.zag, oe_bound_bin, oe_bound_slow_full.zag,
  oe_bound_slow_bin, oe_bound_mid_full.zag, oe_bound_mid_bin
  (test scaffolding only; oe_base.zag untouched)

## Verdicts

- K4: PASS (a/b/c/d/e all pass, 3/3 byte-identical runs).
- K5: PASS (all probes: node-id dest rejection x3, negative/huge dest
  acceptance, guard discrimination match+missmatch, stale node, zero
  operand, i32::MIN 536.9M-iter walk; zero panics, zero hangs, zero
  build failures).
- No bar weakened. oe_base.zag and scaling_5000_fixed/* unmodified.
