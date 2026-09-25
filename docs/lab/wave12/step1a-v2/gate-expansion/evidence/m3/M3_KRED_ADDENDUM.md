# M3 K-RED ADDENDUM — blind red-team round (operator report)

**Date:** 2026-09-25. **Operator:** K-RED subagent (depth 2). **Method:**
frozen `M3_TRACE_EQUIVALENCE.md` under `PREREG_GATE_EXPANSION.md`.
**Status: K-RED FIRES — M3 version DEAD (miss rate 10/12 > 0).**

This addendum records the K-RED round mechanically. The M3 method crew's
fixed battery (K-CATCH 12/12, K-CLEAN 5/5, K-DET 3/3) is untouched; the
blind red team froze 12 validity-proven plants in
`evidence/m3/redteam/MANIFEST.md`. Each plant below was rewritten as a
faithful instrumented module through the frozen tracer API (same entropy
source, same output behavior, same evasion shape), built with the pinned
toolchain, run as an A/B trace pair per `run_battery.sh` protocol, and
judged by the frozen checker. Nothing below is signed on anyone's behalf.

## Frozen artifact pins (verified before the round)

| Artifact | SHA-256 (verified) |
|---|---|
| tracer `m3_tracer.zag` | `a2e9235f0a8f0048e4af52f285dda0cfbb89353f6a10972e101f057e6a92567e` |
| checker binary `m3_checker` | `e35ef55f5d38b2062b6c896fea6a881e4de429ff2826e57639e5cff7a614319d` |
| allowlist `m3_allowlist.txt` | `8d21392a5d0c3e0a5ee05dd5bda8efc1ab66e5a1a6225d4b9b1098c411e82ad8` |
| toolchain `znc_linux_x86_64_abed8aa1` | `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |
| red manifest `MANIFEST.md` | read-only; plants validity-proven there, re-verified on the rewrites (§2) |

All frozen files read-only; no modifications made. No commits; working
tree only.

## Per-plant results

Miss rule (frozen): checker outputs `VERDICT PASS` on a valid dirty
plant → MISS. Per frozen §5.2, an instrumentation-coverage gap that
yields PASS is a method bug AND counts as a MISS. All 12 plants are
validity-proven (manifest); all 12 rewrites re-verified valid (§2).

| Plant | Category | Checker verdict | Cited rule/event | Instrumentation notes / gaps | Result |
|---|---|---|---|---|---|
| A1 gettimeofday-heap | (a) region/taint laundering | `VERDICT PASS` | silent — 8× `R 1 1 1 0` (INIT-HEAP, untainted), `O 2 8 0` | Kernel syscall-96 fill wrote under instrumentation; meta stayed (init=1,taint=0) from instrumented zeroing. Reads instrumented and covered — no map gap; the region/taint ontology itself is laundered. | **MISS** |
| A2 extern shim | (a) | `VERDICT PASS` | silent — same shape as A1 | Volatile fill inside extern C `wall8` (manifest shim `a2_shim.c`, entropy read only). No API event exists for arbitrary extern call sites; novel call-site not tagged. | **MISS** |
| A3 table lookup | (a) | `VERDICT PASS` | silent — `R 1 1 1 0`, 16× `R 2 1 1 0`, `O 3 16 0` | Sub-instrumentation fill + volatile byte used as table INDEX (not in the committed copy/fill/write taint rules). Reads instrumented and covered. | **MISS** |
| B1 helper import | (b) trace suppression | `VERDICT PASS` | silent — `O 1 8 0` only | Volatile read lives in the UNINSTRUMENTED `@import`ed helper (`kred_b1_helper.zag`); top-level instrumented per map discipline. **§5.2 coverage gap (method bug)** — and a MISS. | **MISS** |
| B2 extern retval | (b) | `VERDICT PASS` | silent — `O 1 8 0` only | Volatile value arrives as extern `wallret()` register return (manifest shim `b2_shim.c`). No memory read exists → no T-READ site, no taint cell. **§5.2 coverage gap (method bug)** — and a MISS. | **MISS** |
| B3 raw syscalls | (b) | `VERDICT PASS` | silent — `END 0` only | Raw syscalls for fill AND stdout; no Zag-level read, no recognized write wrapper. No API event type exists for raw syscalls — run BEGIN/END only per faithfulness rules. **§5.2 coverage gap (method bug)** — and a MISS. | **MISS** |
| C1 straightline | (c) equivalence gaming | `VERDICT PASS` | silent — 16× `R 1 1 1 0`, `O 2 16 0` | Length-only O by design; no data-dependent branches; reads INIT-HEAP/untainted via sub-instrumentation fill. Trace identical across runs while content varies. | **MISS** |
| C2 fixedloop | (c) | `VERDICT PASS` | silent — 16× `R 1 1 1 0`, `O 2 16 0` | Fixed-trip loop; counter-loop condition uninstrumented per the battery's own discipline (c02/p08 counter loops carry no sites). | **MISS** |
| C3 constbranch | (c) | `VERDICT PASS` | silent — `R 1 1 1 0`, `B 2 1 0`, 8× `R 3 1 1 0`, `O 4 8 0` | Branch on `(v-v)==0` always taken, taint 0; else arm deterministically untaken (map `O 5?`). | **MISS** |
| D1 flood | (d) checker-logic | `VERDICT PASS` | silent — `END 0` only | Counter loop + raw 1-byte writes → ZERO events under the battery discipline; 1,000,000 volatile bytes reach stdout with an empty trace. The red team's ~2M-event flood never materializes — the plant is invisible at any scale, which is worse. | **MISS** |
| D2 nofooter | (d) | **no VERDICT line** — `ERR load`, checker rc=1 | fail-closed empty-trace error | Raw `exit(2)` before the trace buffer flush: 0-byte trace file; checker refuses to load it (fail-closed, per its `exit 1 on internal error` contract). | CAUGHT |
| D3 sites | (d) | `VERDICT FAIL UNMAPPED_SITE A s=256` | coverage/map reconciliation | 5,000 instrumented B sites + map; checker's map parse caps at 256 entries and its hit/site tables are 256 wide → first event at site 256 is unmapped → fail-closed. | CAUGHT |

Full checker outputs: `redteam/checker_out/kred_<p>.check` (12 files).

## Miss rate and verdict

- **Miss rate: 10/12.**
- **K-RED FIRES → M3 version DEAD** (kill bar: miss rate > 0).

Per-miss mechanism, one line each:
- **A1:** kernel writes under instrumentation → tracked buffer reads INIT-HEAP/untainted.
- **A2:** extern C fill is not a recognizable call site → no event, same laundering as A1.
- **A3:** volatile-as-index is outside the copy/fill/write taint rules → laundered.
- **B1:** volatile read in uninstrumented `@import` → no events (§5.2 coverage gap).
- **B2:** volatile arrives as extern register return → no read site exists at all (§5.2 gap).
- **B3:** raw syscalls for fill and output → trace legitimately empty (§5.2 gap).
- **C1:** length-only T-OUT + no data-dependent branches → identical traces, varying content.
- **C2:** fixed-trip loop, counter condition uninstrumented → identical traces, varying content.
- **C3:** always-taken identity branch, taint 0 → identical traces, volatile bytes emitted.
- **D1:** counter loop + raw writes → zero events while 1MB of volatile stdout flows.

The two catches are both fail-closed accidents of checker limits, not
detections of volatility: D2's 0-byte trace is refused (`ERR load`),
D3's 5,000 sites overflow the checker's 256-entry map parse
(`UNMAPPED_SITE`). Neither plant's volatility was observed by any rule.

## Operator notes (judgment calls, recorded)

1. **D1 loop instrumentation:** the battery's own modules (c02, p08)
   never instrument counter-loop `while` conditions — only
   data/state-dependent `if`s get branch sites, and the checker
   reconciles coverage for all 18 modules on that discipline. D1's
   `while(n<1000000)` is a pure counter loop → no site, per the
   established discipline. If the method crew holds that counter loops
   SHOULD be instrumented, that is itself a discipline change to record —
   and it would only convert D1's miss into a truncation FAIL, not a
   principled catch.
2. **Output expression:** plants whose attack is in the acquisition
   (a1–a3, c1–c3, d2, d3, b1, b2) express stdout through `m3_write_out`
   (battery pattern); plants whose attack IS the uninstrumented output
   path (b3, and d1's flood writes) keep raw syscalls per the frozen
   faithfulness rules.
3. **D2's output** uses `m3_write_out`; the O event sits in the never-
   flushed buffer, so the trace file is 0 bytes either way — the footer
   attack is preserved exactly.
4. **A2/B2 shims:** manifest shims `a2_shim.c` / `b2_shim.c` used for the
   entropy read only, rebuilt fresh as `runs/liba2wall_kred.so(.1)` /
   `runs/libb2wall_kred.so(.1)`; everything else pure Zag.
5. **§5.2 gaps:** B1, B2, B3 each record an instrumentation-coverage gap
   (method bug) in their source header and map; all three yielded PASS,
   so each counts as a MISS as well.
6. **Determinism:** zero RNG in operator decision paths; all A/B trace
   pairs for PASS plants are byte-identical across clean/dirty runs
   (checker `EQUIV OK`); build log SHAs in `redteam/KRED_BUILD.log`.

## Artifacts (all under `evidence/m3/redteam/`, plus this addendum)

- Instrumented sources: `kred_a1.zag`, `kred_a2.zag`, `kred_a3.zag`,
  `kred_b1.zag` + `kred_b1_helper.zag` (uninstrumented), `kred_b2.zag`,
  `kred_b3.zag`, `kred_c1.zag`, `kred_c2.zag`, `kred_c3.zag`,
  `kred_d1.zag`, `kred_d2.zag`, `kred_d3.zag` (generated, 5,000 sites)
- Maps: `maps/kred_<p>.map` (12)
- Binaries: `runs/kred_<p>` (12) + `runs/liba2wall_kred.so.1`,
  `runs/libb2wall_kred.so.1`; per-build logs `runs/kred_<p>.build.log`
- Build log with SHAs: `KRED_BUILD.log`; run script: `kred_run.sh`
- A/B traces: `traces/kred_<p>_{A,B}.trace` (24); validity stdout:
  `traces/kred_<p>_v{1,2}.out`
- Checker outputs: `checker_out/kred_<p>.check` (12)

Source SHAs (from `KRED_BUILD.log`):
kred_a1 `551eed3a…`, kred_a2 `3b514665…`, kred_a3 `6ac498d0…`,
kred_b1 `b7b85e09…` (+helper, uninstrumented), kred_b2 `c1388939…`,
kred_b3 `8a867532…`, kred_c1 `f070099a…`, kred_c2 `16b13a420…`,
kred_c3 `0709795a…`, kred_d1 `d6ff3efd…`, kred_d2 `d4893c90…`,
kred_d3 `06a27cc8…`.

## Bottom line

M3's fixed battery caught every plant the method crew could imagine.
The blind red team found ten ways through: the region/taint ontology is
laundered by anything that writes under source instrumentation (kernel,
extern C, register returns, uninstrumented imports, raw syscalls), and
the trace-equivalence rule is blind to content by design (length-only
T-OUT, data-independent branches, uninstrumented counter loops). The
method as frozen cannot certify the decision path it claims to certify.
**K-RED: 10/12 misses — M3 version KILLED.**
