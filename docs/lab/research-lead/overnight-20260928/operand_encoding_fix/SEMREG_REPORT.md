# SEMREG_REPORT.md -- K6 semantic regression (W-SEMREG)

Lane: `docs/lab/research-lead/overnight-20260928/operand_encoding_fix/`
Branch: tnn-native-lab. Local only, never pushed.
Prereg: 447f087af (K6). Implementation: fd79576d4.
Read before work: PREREG.md, AUDIT.md, NAMECHECK.md, REPORT.md.

## Step 0: Toolchain guard (2026-10-02)

Executed before any other work:
```
export PATH="$HOME/safebin"
which python3   -> (empty; exit 1)
which python    -> (empty; exit 1)
guard-check-done
```
Result: PASS. PATH was `/home/hatch/safebin` only for every command.
All computation pure Zag; shell used only for znc invocation, binary
execution, git ops, file movement. No forbidden-executable invocation
occurred. No PROCESS-FAIL condition triggered.

## Build commands

Minimal main (mine, /tmp/runall_main.zag; calls run_all(), emits rc):
```
fn main()i32 {
  let r:i32=run_all();
  emit("RUNALL-RC ");
  e64(r);
  emit("\n");
  return r;
}
```
OLD: `cat scaling_5000_fixed/s6_base.zag scaling_5000_fixed/s6_patch.zag /tmp/runall_main.zag > /tmp/old_test.zag`
      then `znc /tmp/old_test.zag -o /tmp/old_test_bin` -> exit 0, 145 analyzer warnings
NEW: `cat operand_encoding_fix/oe_base.zag scaling_5000_fixed/s6_patch.zag /tmp/runall_main.zag > /tmp/new_test.zag`
      then `znc /tmp/new_test.zag -o /tmp/new_test_bin` -> exit 0, 145 analyzer warnings
Source diff old_test.zag vs new_test.zag: ONLY the frozen operand-encoding
hunks (res_op, tag 101/103/104, encoders, stale-comment rewrite) plus the
header revision comment. Warning count identical (145/145).

Execution (40 min timeout each):
- OLD: `timeout 2400 /tmp/old_test_bin > old_runall.log` -> immediate panic, rc=1
- NEW: `timeout 2400 /tmp/new_test_bin > new_runall.log` -> immediate panic, rc=1

## Execution result

Both logs are 2 lines, byte-identical except the rc label line I appended:
```
panic: slice index out of bounds
```
Per-test PASS/FAIL lines: 0 on old, 0 on new. TOTAL lines: 0 on old, 0 on new.
stdout of the two binaries is byte-identical.

## Root cause: pre-existing fossil, independent of the operand fix

The battery never reaches any test on EITHER build. Probe (pure Zag,
/tmp/probe_init.zag + /tmp/probe2_init.zag, old base + patch) isolates it:

- Every test allocates `z_alloc(110656)` then calls `tnn2_init(W)`.
- `tnn2_init` zero-fills 593984 bytes, then zero-fills edges via
  `es(W,e,0,-1)` for e in 0..131071, where `eoff(e) = 2621504 + e*16`
  (oe_base.zag line 60; identical in s6_base.zag).
- Even with a full 593984-byte allocation (probe confirmed W.len=593984),
  the edge loop writes at offsets >= 2621504 -> panic. The current layout
  needs >= 2621504 + 131072*16 = 4718656 bytes (the driver allocates
  4722752).
- The 110656-byte per-test allocation is a fossil from an ancient smaller
  layout; the layout grew (edges moved to base 2621504) but the tests were
  never updated. `run_all` was never exercised on this base lineage:
  `scaling_5000_fixed/s6_run1.txt` is driver (s6_world) output with zero
  test PASS/FAIL lines.

The panic is in initialization code untouched by the operand fix
(tnn2_init, es, z_alloc are byte-identical old/new). Both builds panic at
the same instruction before executing any test logic.

## Per-test comparison table

| test | old | new |
|------|-----|-----|
| C1..C15, A1..A6, P1..P7 (+F2,P2b,P3a,P3b,ABL-I,ABL-C), DV, XCAP, R-PACT1..6, T2-CHAIN4, T2-REJECT, T2-INQUIRE, T2-ACTLIVE, T2-REVISE | never executed (panic in tnn2_init) | never executed (panic in tnn2_init) |
| TOTAL | absent | absent |

Differential result: ZERO divergence. Identical (empty) vectors,
byte-identical stdout, identical panic location and rc.

## t_c6 / T2-REVISE specifics

- (a) t_c6: audit predicted FAIL on both. CANNOT BE CONFIRMED EMPIRICALLY:
  t_c6 never executes (panic precedes all tests on both builds). The
  prediction stands as audit-only; the fossil failure mode (field4=1000
  rejected by old `d<10000` and new `d>=0` dest checks) is code-reviewed,
  not observed.
- (b) T2-REVISE (t_t2_revise, oe_base.zag line 1189): DOES NOT PASS on
  the new build -- it never executes (same tnn2_init panic). The K6
  clause "t_t2_revise passes on the new build" is unsatisfiable on the
  frozen sources. No evidence either way about signature-diff detection
  after revision.
- (c) TOTAL counts: absent on both (no battery run completes).

## K6 verdict: FAIL (as frozen)

Per the prereg verdict rule ("BUILD-PASS iff K1..K6 all pass as frozen;
no weakening or reinterpretation of bars after results"):

- The differential clause (identical per-test PASS/FAIL vectors) is
  satisfied: zero divergence old vs new, byte-identical output.
- The absolute clauses fail: T2-REVISE does not pass on the new build,
  t_c6's predicted FAIL cannot be confirmed empirically, no TOTAL line
  exists. The battery cannot emit a single test line on EITHER build.

Root cause is NOT the operand fix: it is the pre-existing fossil
workspace allocation in the frozen base's own test battery (110656-byte
test workspaces vs a ~4.7MB layout; tnn2_init panics in its edge-zeroing
loop at `eoff(e)=2621504+e*16`). This defect predates the fix, is
identical on both builds, and lies outside this prereg's frozen change
set (repairing the test allocations is itself a base change needing its
own prereg).

Recommended follow-up: fresh prereg to repair run_all's test workspace
allocations to the current layout size (matching the driver's 4722752),
then re-run K6 on both builds. The operand fix itself introduced zero
observable semantic divergence in this battery.

## Files

- `old_runall.log` -- OLD build stdout (panic, rc=1)
- `new_runall.log` -- NEW build stdout (panic, rc=1; byte-identical)
- `SEMREG_REPORT.md` -- this file

Bases, patch untouched. Test mains and concatenated sources stayed in
/tmp (ephemeral). Other workers' files in this lane dir (oe_driver_k2_*,
oe_full_k2_*, oe_bound_*) were not touched. Commits local, never pushed.
