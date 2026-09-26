# M3 VERDICT — Decision-trace equivalence (fixed battery)

**Date:** 2026-09-25. **Method:** frozen `M3_TRACE_EQUIVALENCE.md` under
`PREREG_GATE_EXPANSION.md`. **Status: DONE** — awaiting the blind red-team
manifest (K-RED); no red plants were authored by this crew.

## 1. What was built

- **Tracer** `tracer/m3_tracer.zag` — source-level instrumentation library.
  Modules call `m3_branch` / `m3_r8`+`m3_w8` / `m3_open`+`m3_read`+`m3_close` /
  `m3_write_out` / `m3_getrandom` / `m3_clock_gettime` / `m3_argv_read` /
  `m3_stack_probe`; every call appends a trace event. Byte-cell
  `(init, taint)` metadata is maintained by the instrumented allocator;
  taint propagates on `m3_memcpy`/`m3_fill`/writes and is sourced from
  getrandom, clock, ENV/argv reads, and non-allowlisted fd reads.
- **Checker** `checker/m3_checker.zag` (pure Zag, pinned toolchain) —
  verifies trace integrity (`END <nevents>`), reconciles the static
  instrumentation map against dynamic hits (coverage), applies the static
  volatile-read rule (rule 1), then the trace-equivalence rule (rule 2).
- **Wire format** (superset of the frozen §2 — adds the taint field
  required by frozen §5 hard problem 1):
  - `R <site> <region> <nbytes> <taint>` — read. Regions: 1 INIT-HEAP,
    2 UNINIT-HEAP, 3 STACK, 4 STATIC, 5 ENV, 6 CLOCK, 0 UNTRACKED (= checker
    failure).
  - `B <site> <taken> <taint>` — branch.
  - `X <site> <fd> <nbytes> <path|->` — external IO. fd 3 is the trace
    file itself; paths recorded from an fd→path table.
  - `O <site> <nbytes> <taint>` — output write (lengths only).
  - `C <site> <hits>` + `END <nevents>` — coverage footer and integrity
    footer.
- **Rule 1 (static):** FAIL on region ∈ {2,5,6,0}, on tainted R/B/O, or on
  non-stdio X whose path is not in the frozen allowlist.
- **Rule 2 (equivalence):** exact event count and field-by-field equality
  (X paths compared byte-exact); first divergence cited.

## 2. Pre-test gates (both passed before any battery run)

- **Taint vectors** (`tracer/TAINT_VECTORS.md`, `tracer/m3_taint_test.zag`):
  12/12 PASS — partial-range taint, one-hop and chained memcpy
  propagation, byte isolation, tainted/untainted/untracked reads, clean
  overwrite clearing taint, getrandom and argv taint sources, no
  cross-allocation bleed.
- **Coverage:** every module ships a static map in `maps/`; the checker
  requires every non-`?` site hit ≥1 in BOTH traces and every dynamic
  event mapped to a declared site. `?` marks sites on deterministically
  untaken paths (c02 site 6, p05 site B8, p08 site 3).
- **Data-fd allowlist** (`m3_allowlist.txt`) frozen before battery:
  exactly the two data files under `data/` (SHA-256 recorded below).

## 3. Battery protocol

`run_battery.sh <rundir>`: for each of 18 modules, run A (clean heap,
`clean` mode, `M3_FLAG=7`) and run B (predirtied heap via
`m3_predirty()` + 5000-byte `M3_PAD` environ shift, `dirty` mode,
`M3_FLAG=7`), both under `setarch -R` (ASLR suppressed so only the
heap-layout/environ perturbations differ). p07 additionally needs
`LD_LIBRARY_PATH=runs` for its shim. The checker decides each pair.

## 4. Kill table (per-plant, cited)

| Plant | Expected | Got | Cited kill |
|---|---|---|---|
| P01 getrandom | FAIL r1 | FAIL RULE1_A | ev#0 `R 2 6 16 1` CLOCK tainted |
| P02 clock_gettime | FAIL r1 | FAIL RULE1_A | ev#0 `R 2 6 16 0` CLOCK |
| P03 /dev/urandom | FAIL r1 | FAIL RULE1_A | ev#0 `X 1 4 0 /dev/urandom` non-allowlisted |
| P04 uninit read | FAIL r1 | FAIL RULE1_A | ev#0 `R 2 2 1 0` UNINIT-HEAP |
| P05 env-var | FAIL r1 | FAIL RULE1_A | ev#0 `X 1 4 0 /proc/self/environ` non-allowlisted |
| P06 ASLR leak | FAIL r1/2 | FAIL DIVERGENCE | ev#1 `B 4`: A taken=1 vs B taken=0 |
| P07 rdtsc | FAIL r1 | FAIL RULE1_A | ev#0 `R 1 6 8 1` CLOCK tainted |
| P08 hash order | FAIL r2 | FAIL DIVERGENCE | event-count 54 vs 26 |
| P09 innocent tables | PASS | PASS | — |
| P10 machine-id | FAIL r1 | FAIL RULE1_A | ev#0 `X 1 4 0 /etc/machine-id` non-allowlisted |
| P11 argv[0] | FAIL r1 | FAIL RULE1_A | ev#0 `R 1 5 64 1` ENV tainted |
| P12 invoke-discard | FAIL r1 | FAIL RULE1_A | ev#0 `R 2 6 16 1` CLOCK tainted |

Defense-in-depth spot check: with `/proc/self/environ` temporarily
added to a COPY of the allowlist, P05 still FAILs — `RULE1_A
TAINTED_READ` at ev#2 (`R 3 1 1 1`). The taint bit catches what the
allowlist would miss.

## 5. Kill bars

- **K-CATCH: 12/12** — 11 FAIL + P09 PASS, every kill cited to a trace
  event above. No miss: a miss would have killed M3 under this frozen round.
- **K-CLEAN: 5/5 PASS** — C01, C02, C04, C05, C06 (C03 predeclared
  out-of-scope). Plus the sample variation module: PASS.
- **K-DET: 3/3** — full battery run three times (`runs/battery1..3`);
  all 36 trace pairs byte-identical across runs
  (aggregate SHA-256 `6a645847d50fd80645964dc476453d6c47556047d44020dc98416cd93ba77298`).
- **K-RED:** pending — blind red-team manifest not yet received. This
  crew authored no red plants.

## 6. Build provenance

- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
- `m3_tracer.zag` `a2e9235f0a8f0048e4af52f285dda0cfbb89353f6a10972e101f057e6a92567e`
- `m3_taint_test.zag` `8188b07a546349c94d58da6db39cf70dc468423bde8a9e9cce131df3e87d258e`
- `m3_checker.zag` `9a0465dc92cd58465ad4ae8d66df19084b375a6d7c74d8c887f9eb3b67b321cc`
  → binary `checker/m3_checker`
  `e35ef55f5d38b2062b6c896fea6a881e4de429ff2826e57639e5cff7a614319d`
  (rebuild byte-identical — build is deterministic)
- `m3_allowlist.txt` `8d21392a5d0c3e0a5ee05dd5bda8efc1ab66e5a1a6225d4b9b1098c411e82ad8`
- `run_battery.sh` `adcdba4fb4ef383cedb3df5745fdfc6c93fd37ed6a0d5a0991e47784d731c29c`
- Module sources/binaries: SHAs in §7. Data files:
  `sample_input.bin` `8091197e38b991a5b4ceb3355c2c7c0d9dbf06d3d40ebb68cf15be6924abb74c`,
  `c04_input.bin` `bf525e0bf2dd78540b252a150393e03a51ff90f021cdd32c61c1633e87d22f7a`.
- Per-module checker verdicts: `verdicts/<m>.verdict`. Traces:
  `runs/battery{1,2,3}/<m>_{A,B}.trace`.

## 7. Module source/binary SHA-256

sources: c01 `d5cc4fdf…6e40`, c02 `5658413c…77bc5`, c04 `a9e459ae…56cd1`,
c05 `9c4be4f3…c4e7b`, c06 `efb0b917…26bda`, p01 `6e6d925b…6c18`,
p02 `845ed673…acb3bb`, p03 `ef488fdc…ca1d6`, p04 `245bb754…59c4216b`,
p05 `f08d24e6…7f2591c5`, p06 `ac94dabb…9dde441`, p07 `37f8acf4…9716`,
p08 `02953515…b33f8dda`, p09 `85e40c1f…106caf23`, p10 `1326623b…2701`,
p11 `e7818f90…9239`, p12 `80bf1dd8…3a4279bd`, sample `ef6653b3…dcaad1495d`
(full 64-hex in the battery log `runs/SHASUMS.txt`).
binaries: sample `a123b4ed…30dbad567`, c01 `f0bf3a4b…d292e0a4`,
c02 `ff702d6e…89197222e`, c04 `19735678…138d3f6b`, c05 `079bceaf…8465da5a`,
c06 `c480c6ce…6ebf29d15`, p01 `1b5f850c…3372`, p02 `a7bd37b5…70c4a55b8e`,
p03 `26c0783c…ec8d`, p04 `12ff7c47…46f6ae`, p05 `aa14b5d5…10170987`,
p06 `97b9d75e…5d8c8bfca`, p07 `8d39d503…0739`, p08 `8c91fcef…5e044357`,
p09 `ee44bad7…106caf235e1`, p10 `c1db303a…9484`, p11 `508464f2…a796`,
p12 `95a3fe2f…c7c0565`, shim `librdtsc_m3.so` `9bcc0165…a662a0613d`.

## 8. Limitations and disclosures

1. **P07 rdtsc shim (disclosed deviation from pure Zag):** the pinned znc
   exposes no rdtsc intrinsic (probed 2026-09-25). The timestamp comes
   from a 3-line C shim (`tracer/rdtsc_shim.c` →
   `runs/librdtsc_m3.so`) called via `extern fn` and tagged CLOCK+tainted
   by `m3_rdtsc()`. Confined to this one positive-control fixture;
   every other module is pure Zag. If the bar requires zero C anywhere,
   P07 must be re-cast as an external fixture or dropped — the 11 other
   plants are unaffected.
2. **C03 out of scope** per frozen §3 (seeded-RNG reads are
   region-tagged CLOCK-equivalent; the tracer cannot distinguish seeded
   from unseeded at trace level).
3. **Trace values are not recorded** — only classifications, lengths,
   branch outcomes, taint, and paths. Content equality is replay's job.
4. **P07 K-DET hardening (2026-09-25):** the first p07 build branched on
   `tsc & 1`; three batteries happened to agree but a fourth run flipped the
   branch, proving the trace nondeterministic. The branch was decorative
   (detection is rule 1 on the CLOCK read), so it was removed; the final
   p07 trace is `R 1 6 8 1 / O 3 8 1` and K-DET was re-run 3× fresh.
5. **P06/P08 divergence is allocator-layout-dependent** (verified
   deterministic on this VM across 3 batteries under `setarch -R`; the
   calibration is in `addrprobe.zag`). A different libc could shift the
   exact bit; the method (divergence detection) does not depend on which
   bit differs.
5. **X-event fd numbers** are setup-dependent (trace file = fd 3, so
   data files land on fd 4); the checker resolves identity by path, and
   runs keep opens deterministic.
7. **No red plants authored** — K-RED awaits the blind manifest.

## 9. Verdict

M3 fixed battery: **K-CATCH 12/12, K-CLEAN 5/5, K-DET 3/3.** The
decision-trace method caught every planted volatility channel —
syscalls, clock, device files, environ, uninitialized memory,
heap-layout nondeterminism, and invoke-and-discard — each with a cited
trace event, while passing the innocent table module and all five clean
modules. Taint vectors 12/12, instrumentation coverage reconciled for
all 18 modules, zero RNG in any decision path, byte-identical reruns.
**DONE** — ready for the blind red-team manifest.
