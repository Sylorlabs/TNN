# K2′ RED-TEAM PLANT INDEX — thin prescriptive certifier (THINCERT-2026-09-20-v1)

**Round:** K2′ blind red team, 20 plants, fixed order. **Authored against:** the
AMENDED rule set (R3′ allocation-idiom rule, R1b substrate pinning, R4b no
`nio_*` impostors — per `AMENDMENT_2026-09-20_THINCERT_R3.md`, which the built
certifier enforces).
**Blinding:** red-team author never read `certifier/thincert.zag`,
`BUILD_RECORD_THINCERT.md`, `K3_PRIME_RECORD.md`, `plants/`, `runner/`, or any
phase-2 lead report. Attack surface was the prereg + amendment + intrinsic
audit + `repbuild/` template only.
**Harness contract:** every plant keeps the template's `main`/`vary_expr`/
`load_file`/`print_hex` and adds one `entropy_mix` helper called from `main`
after `vary_expr`, before `print_hex`. Source only — no binaries.
**Manifests:** per-file sha256 records are real (computed at authoring). The
`BIN` record is intentionally absent: the phase-2 lead MUST append
``BIN variation.bin <sha256>`` after building each plant with the frozen
toolchain (red team never supplies binaries); R7 cannot be evaluated without it.

## Plants 1–20

| # | Disguise class | Genuine entropy mechanism | Targeted rule(s) | Expected scorer outcome |
|---|---|---|---|---|
| 01 | computed syscall immediate | `_zag_raw_syscall(200+28, …)` = clock_gettime(228); kernel wall clock | **R2** (non-literal first arg; token Tier-S-only in module) | FAIL naming R2 (replay would also diverge) |
| 02 | runtime-built device path | path bytes emitted as numeric codes (no banned literal for R6b); open+read of the system randomness device via `_zag_raw_syscall` in module | **R2** (Tier-S-only token in module; R6b correctly finds nothing) | FAIL naming R2 (replay would also diverge) |
| 03 | partial-init loop | `_zag_malloc` block half-initialized; `b[0..2]` carry `_zag_clock_monotonic_ms` | **R2** (`_zag_malloc` not Tier-M), +R4 (`*u8`), +R6a | FAIL naming R2 |
| 04 | early-return-before-init | `_zag_malloc` block; early path reads never-written `b[32]`; clock bytes in `b[0..2]` | **R2**, +R4, +R6a | FAIL naming R2 |
| 05 | env-family token | `_zag_getenv("MALLOC_PERTURB_")`; set on replay runs 3–4, unset on 1–2 | **R2/R6a** (banned-explicit) | FAIL naming R2/R6a; **also diverges on replay** |
| 06 | clock intrinsic | `_zag_clock_monotonic_ms()` XORed into output | **R2/R6a** | FAIL naming R2/R6a; **also diverges on replay** |
| 07 | cpuid read | `_zag_x86_cpuid_eax/ebx(0)`; stable per machine, varies across machines | **R2/R6a** | FAIL naming R2/R6a (replay passes; static must fire) |
| 08 | port IO | `_zag_inb(64)` (keyboard status port) | **R2/R6a** | FAIL naming R2/R6a. Note: `in` faults in userspace — expected to be caught statically, never executed |
| 09 | slice_ptr address leak | `_zag_slice_ptr(out)`; heap address varies per run under ASLR | **R2** (Tier-S-only) | FAIL naming R2; **also diverges on replay** |
| 10 | uninit read via aliased slice | overlapping views `a=p[0..64]`, `b=p[16..48]` of a `_zag_malloc` block; `b[16]` aliases never-written `a[32]`; `a[0]` carries the clock | **R2**, +R4, +R6a | FAIL naming R2 |
| 11 | `_zag_rand`-named call (fail-closed) | own `fn _zag_rand()` wrapping `_zag_arg(0)` (binary path); the NAME is the violation — toolchain has no such intrinsic | **R2** (name banned-explicit; fail-closed) | FAIL naming R2. If PASS → MISS → K2′ fires |
| 12 | renamed table indexed by uninit | `lut` (not `tab`) in a `_zag_malloc` block; index mixes clock byte `lut[0]` with never-written `kb[0]` | **R2**, +R4, +R6a | FAIL naming R2 |
| 13 | getenv-driven branch | `_zag_getenv("HOME")` branch; HOME set on all replay runs | **R2/R6a** | FAIL naming R2/R6a (replay passes; static must fire) |
| 14 | extra unlisted `.zag` file | `evil.zag` imported but NOT in manifest; carries a clock read (not dead code) | **R1** (unlisted `.zag`), +R2/R6a | FAIL naming R1 (and R2) |
| 15 | modified substrate, own manifest | substrate gains `nio_clock()`; manifest self-consistent with the NEW hash | **R1b** (must not match pinned `e6379ddb…`); module itself is clean | FAIL naming R1b |
| 16 | non-canonical while | decrementing `while(i>0)` (not `while(c<bound)` +1) → R5; seed is the wall clock | **R5**, +R2/R6a | FAIL naming R5 (and R2) |
| 17 | struct-based hidden state | `struct Hidden{…}` in module → R4; struct carries the wall clock | **R4**, +R2/R6a | FAIL naming R4 (and R2) |
| 18 | `_zag_raw_syscall` unlisted literal | literal `228` (clock_gettime) not in the 13-allowlist | **R2** (unlisted number; Tier-S-only token) | FAIL naming R2 (replay would also diverge) |
| 19 | **NOVEL:** undeclared-input file read | `load_file("/etc/machine-id")` via substrate API; allowlisted tokens, R6b-clean literal; constant across replay, varies across machines | none as written | **PASS static + PASS replay, genuine deployment entropy → novel class** |
| 20 | **NOVEL:** undeclared argv-string dependence | `_zag_arg(0..2)` raw path-string bytes mixed into output; Tier-M-legal; constant across replay, varies across deployments | none as written | **PASS static + PASS replay → novel class (weaker attempt)** |

## Notes for the scorer (phase-2 lead)

- Plants 05 and 13 assume `_zag_getenv([]u8)[]u8` (empty when unset); plant 07
  assumes `_zag_x86_cpuid_eax(leaf)` integer-in/integer-out (normalized with
  `as i64`); plant 08 assumes `_zag_inb(port)` integer-in/integer-out. These
  signatures were not recoverable from committed sources (the intrinsics are
  only in the audit's REAL list); if any assumption is wrong the plant fails
  to build — report as build failure, not as a certifier verdict.
- Plant 11 defines `fn _zag_rand()`. The intrinsic is UNKNOWN on the frozen
  toolchain (compiler-probed), so no redefinition collision is expected; if
  the toolchain rejects `_zag_`-prefixed user functions, report as build failure.
- Plant 08 will SIGSEGV if executed (`in` is privileged). It is expected to be
  rejected statically; do not treat an execution fault as a certifier PASS.
- The uninit-shape plants (03, 04, 10, 12) read never-written heap tails that
  are zeros in a fresh process; their GENUINE runtime variance comes from the
  wall-clock bytes placed in the same buffer (stated in each plant's header).
  The banned idiom under test is `_zag_malloc` in module source (→ R2), exactly
  the reduction the R3′ amendment prescribes.
- No plant contains an R6b-banned literal substring (`urandom`, `/dev/`,
  `/proc/`, `/sys/`) in module source — verified mechanically at authoring.
  Plant 02's evasion is precisely that the device path never appears as text.
