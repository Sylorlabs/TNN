# Arm O — Build Log

## Compiler
Frozen toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Source Layout
```
units/arms/O/cl/
  base.zag    — OState, allocator, ledger, IO helpers, JSON output
  proto.zag   — TST-1 encoder/decoder, teacher counting, top-K selection
  learn.zag   — deliberation, word store, tripwire, teach/disconnect, segments
  arm.zag     — mode dispatch (M1–M8, o-disconnect, o-redteam, o-tripwire)
units/arms/O/substrate/
  R33_NATIVE_SHA256_V2.zag, R33_NATIVE_IO_V1.zag (native dependencies)
```

## Key Implementation Decisions

### Struct Passing (Critical Fix)
Zag passes structs BY VALUE to `*Struct` parameters (verified 2026-09-21:
passing `s:OState` to `fn f(s:*OState)` copies; `x` stays 0 after `inc(s)`).
All calls in `arm.zag` were fixed to use `&s` explicitly. Without this fix,
state did not persist across calls and performance collapsed (deep copies).

### Hash Table Sizing
`O_SCTAB` = 262,144 slots (up from 65,536) for teacher/learner token counting.
Probe caps at 4,096 to bound worst-case.

### Byte Index Masking
All `u8 as i32` conversions used as array indices are masked with `& 255`
to guard against sign-extension on high bytes (>127).

### Performance
- `teach_session`: single batch of up to 4096 candidates (teacher_topk with
  binary heap), not 40 batches. Full 5.2MB prose + 9.1MB code teach is slow
  (~5+ min for M1); acceptable for 1x but not 10x without optimization.
- `word_match`: bucketed by first byte (256 buckets). Chain traversal is
  O(n) worst-case; acceptable for vocab ≤4096.

## Build Commands
```bash
cd ~/workspace/o_build
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  ~/workspace/tnn-lab/units/arms/O/cl/arm.zag -o o_bin
```

## Test Results (2026-09-21)

### o-redteam (2 runs, deterministic)
```
REDTEAM adopted=0 rejected=15 kill_iii=0
```
14 attacks, 0 adopted. Kill-(iii) NOT fired. PASS.

### o-disconnect (1 run, 217s)
```
DISCONNECT post_m1=100.0 kill_ii=0
```
Post-scaffold M1 = 100.0% (≥99.5%), rankings identical. Kill-(ii) NOT fired. PASS.

### o-tripwire (secondary trigger)
```
TRIPWIRE proposals=1 fired=1 kill_iv=0
```
Single conf-255 proposal covering 10% of stimulus (>5% threshold) fires
the secondary tripwire immediately. Kill-(iv) NOT fired. PASS.

Note: The primary rolling-200 trigger was not validated with a realistic
scenario (requires 95% adopt rate on 200 distinct tokens, hard to construct
with the cautious learner). The secondary trigger is part of the frozen
spec and is validated.

## Known Issues
- M1/M2 on full corpora are slow (>5 min). The 1x battery may not complete
  in practical time without optimization or subsetting.
- Primary tripwire (rolling 200) untested in integrated scenario.
- Kill-(i) blocked: no emergent-only P scorecard available for comparison.
