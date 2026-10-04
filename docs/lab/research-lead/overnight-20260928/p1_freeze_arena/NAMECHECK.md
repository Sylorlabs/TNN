# NAMECHECK.md -- FA1 (FREEZE-ARENA-1)

Committed with PREREG.md, alone, before implementation. Step 0/1 frozen here;
Steps 2+ filled in after implementation and committed with it.

## Step 0 -- toolchain and environment

* `. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh` sourced before every
  build and every run.
* `tnn_pure_zag_report` must print `VERDICT: PURE-ZAG-CLEAN`. Verified in this
  lane: `forbidden_count=0`.
* Forbidden interpreters (python/node/cc/gcc/make/...) are shimmed to exit 127
  and are not invoked anywhere in this lane.
* Compiler invoked ONLY as
  `znc --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`.
  Omitting `--target macos-arm64` silently emits Linux ELF (brief section 1).

## Step 1 -- frozen cores

| file | expected sha256[:12] | verified in this lane |
|---|---|---|
| `cogops_learnosc2/c8_learn.zag` | `750cb01d086f`, 1331 lines | yes (run.sh prints the count) |
| `cogops_rescueaware/c15_base.zag` | `fc1f6e73...` | yes (concat hash) |
| `hook_phase1/hq_module.zag` | `4200e21f...` | yes (concat hash) |
| concatenated frozen prefix | `043b62b427e9...` | **yes**, measured in this lane before the prereg was written |

Concatenation order (fixed, from C500-R1's `run.sh`):

```
cogops_rescueaware/c15_base.zag
cogops_learnosc2/c8_learn.zag
hook_phase1/hq_module.zag
```

Anchor: reassembling `lt1.zag` from that prefix plus C500-R1's
`lt_world.zag`/`lt_life.zag`/`lt_main.zag` gives source sha256
`38484a45ae512a6e2a6c751e2a6cfe5664589f9e0c0f8388e0f58e7e95442831`, byte-identical
to their committed `lt1.zag`; the built binary reproduces their certified
stdout sha256 `09a09548b2675f99e86260da96cb39d9d8f74ffc7ebe3e1b38a896d1e5f15296`
byte-for-byte. Verified in this lane. This is kill bar K11.

## Step 2 -- learner-side namecheck (filled after implementation)

To be completed before the implementation commit.

## Step 3 -- known toolchain traps observed as defences

* Mandatory return type on every `fn`, including `->i32`. `->i32` written as
  `fn f() -> i32` does not parse; the type goes after the parameter list.
* `if`-nesting <= 3. Hoist call results into a `let` before nesting.
* Every computed-offset i32 read uses an explicit multiplier
  (`get32(B, base+k*4)`, `set32(A, 4+n*12+8, v)`). C500-R1 documents a real
  mis-store inside an 8-slice-argument call chain, so this lane avoids
  passing scratch buffers with computed offsets through wide call chains; the
  episode payload travels as three scalar `i32` arguments instead.
* No `for`. No `!(A&&B)` in a `while` condition (De Morgan only).
* `[]u8 as *u8` is forbidden; `_zag_slice_ptr` is the only route.
* `_zag_raw_syscall` is INERT on this host (brief 4.0). All dynamic output is
  formatted into one preallocated buffer and emitted with exactly one
  `_zag_print(b[0..c])` per binary.
* Non-empty output is asserted in `run.sh` by byte count, not in prose
  (kill bar K2).
* No defect may be attributed to the compiler without a memory-free oracle
  (C526/C527 refuted B16 with 1928 comparisons and 0 mismatches).