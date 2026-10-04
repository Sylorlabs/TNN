# PREREG — THINCERT-2026-09-20-v1: thin prescriptive per-build no-RNG certifier

**Status:** FROZEN 2026-09-20. **Decision owner:** Micah.
**Shape:** per-build prescriptive certifier (debate VERDICT_SHEET.md §3 M1, §5).
This prereg was written, frozen, and committed BEFORE any certifier
implementation code existed. Any change to the rules below after this point
is a dated amendment requiring Micah's re-approval.

## 1. Scope — what is certified

THINCERT certifies ONLY an exact frozen trial build: a source tree pinned by
a per-file sha256 manifest plus a binary hash recorded at freeze. It does not
certify arbitrary Zag code (that shape was killed twice; see debate §5).

**Representative build under test** (the Arm C trial build does not exist yet;
its builder stays parked until Micah signs the residual-risk statement — the
production target will be the real Arm C build once unfrozen):
- `repbuild/variation.zag`
  `48b976b674d4b2d83074208db21f3cac0c1656ec3850be9ad36e23e5a2e5aa11`
- `repbuild/R33_NATIVE_IO_V1.zag`
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
- `repbuild/variation.bin` (build artifact, NOT committed)
  `75cf2006ca044081caad740afbf29b239a38dc9bb3214e477830912bd943a83c`
  built with `tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (byte-deterministic: same source → same binary, verified 2026-09-20).
- Manifest: `repbuild/MANIFEST.txt` (TIER PATH SHA256 lines + BIN record).

## 2. Prescriptive rules (frozen)

### Fail-closed meta-rule
Anything not explicitly allowed by this prereg FAILS the build, no matter how
innocent it looks. There are no carve-outs, no `// PINNED` comments, no
name-keyed exemptions (all three were v2 kill vectors).

### R1 — Frozen manifest correspondence
- Every `.zag` file under the build dir must be listed in the manifest with a
  matching sha256; the manifest lists TIER (`M` module / `S` substrate),
  relative path, sha256. The binary's sha256 must match the manifest's BIN
  record.
- No unlisted `.zag` file may exist anywhere under the build dir (certifier
  walks the tree with getdents64; shell `find` cross-check in the runner).
- `@import` targets must resolve inside the build dir to manifest-listed files.
- Any R1 violation → FAIL naming `R1` and the offending path.

### R2 — Intrinsic allowlist (ALLOW-THIN-2026-09-20-v1)
One-time surface audit: `INTRINSIC_AUDIT.md` (98 REAL intrinsics on
`znc_linux_x86_64_abed8aa1`, compiler-probed 2026-09-20).
- **Tier M** (module source): `_zag_arg`, `_zag_argc`, `_zag_print`,
  `_zag_println`, `_zag_i64_to_str`, `_zag_strcmp`. Any other `_zag_*` token
  in module source → FAIL naming `R2` and the token.
- **Tier S** (substrate files only, hash-pinned by R1): Tier M plus
  `_zag_malloc`, `_zag_free`, `_zag_slice_ptr`, `_zag_raw_syscall`.
  `_zag_slice_ptr` or `_zag_raw_syscall` in module source → FAIL.
- `_zag_raw_syscall` (any tier): the first argument must be an integer
  LITERAL in {0 read, 1 write, 2 open, 3 close, 5 fstat, 8 lseek, 23 select,
  72 flock, 74 fsync, 83 mkdir, 160 setrlimit, 257 openat, 265 linkat}.
  Non-literal first argument (computed immediates — v2 red-team class) or an
  unlisted number (228 clock_gettime, 318 getrandom, …) → FAIL naming `R2`.
- Explicit banned tokens (BAN-THIN-2026-09-20-v1, also FAIL by fail-closed):
  `_zag_clock_monotonic_ms` (banned outright per v2 lessons), `_zag_rand`,
  `_zag_getenv`, `_zag_exec_cmd`, `_zag_exec_capture`, `_zag_read_fd`,
  `_zag_read_file`, `_zag_write_file`, `_zag_write_exec`, `_zag_file_exists`,
  `_zag_exit`, all `_zag_x86_cpuid_*`, `_zag_rdmsr`, `_zag_wrmsr`,
  `_zag_inb/_zag_inw/_zag_inl`, `_zag_outb/_zag_outw/_zag_outl`,
  `_zag_cli/_zag_sti/_zag_hlt/_zag_pause/_zag_wbinvd`,
  `_zag_read_cr0/_zag_read_cr2/_zag_read_cr3/_zag_read_cr4`,
  `_zag_write_cr0/_zag_write_cr3/_zag_write_cr4`,
  `_zag_lgdt/_zag_lidt/_zag_ltr/_zag_invlpg`, all `_zag_script_*`,
  all `_zag_process_result_*`, all `_zag_allocation_*/_zag_allocator_*/_zag_fixed_buffer_*`.
  Full table in `INTRINSIC_AUDIT.md`.
- Token matching EXCLUDES `//` comments; string literals are scanned by R6b.

### R3 — Canonical init (INIT-THIN-2026-09-20-v1)
Uninitialized-memory reads are the v2 K1 kill class (zeroed pages hide them
from replay). Prescriptive rule, per function, linear order:
- The ONLY allocation idiom in module source is `let <v>:[]u8=nio_alloc(<n>);`
  (direct `_zag_malloc` in module source → R2 FAIL).
- Every `nio_alloc`'d slice must be initialized by a canonical full-range init
  loop IN THE SAME FUNCTION, textually before any element read of the slice
  and before the slice is passed as a call argument. Canonical skeleton:
  `let <i>:i32=0;` … `while(<i><<v>.len){ <v>[<i>]=<expr>; <i>=<i>+1; }`
  where `<expr>` contains no `<v>[` read and no banned token. (Zero-fill is
  the `<expr> = 0` case; computed fill — e.g. the S-box — is the general case.)
- Between alloc and the init loop only the `if(<v>.len!=<n>){…}` guard idiom
  may appear. Init loops nested inside `if`/`while` → FAIL (R3c).
- Any element read `<v>[…]` or call passing `<v>` while `<v>` is uninit →
  FAIL naming `R3`. Use-after-`nio_free` → FAIL naming `R3`.
- Slice parameters are assumed initialized on entry (documented assumption);
  sub-slices of initialized slices inherit initialized status.
- Rationale for hand-rolled tables (the v2 "couldn't see through it" kill):
  with R2 (no hidden inputs: no clock, no pointers, no env) + R3 (no uninit
  reads), a flat `[]u8` table indexed by any expression is a pure function of
  initialized bytes — deterministic by construction. There is nothing to
  "see through"; iteration order over a flat array is not a nondeterminism
  source. Deterministic data structures are NOT banned.

### R4 — Containers and types (CONT-THIN-2026-09-20-v1)
- Module source may use only: `i32`, `i64`, `u8`, `bool`, `[]u8`, `void`.
  Any other type — including `struct` definitions (v2 EntrySet class),
  `*u8`/`*i64` raw pointers, `[]i32`, enums — in module source → FAIL naming
  `R4`. (Raw pointers would need `_zag_slice_ptr`, already Tier-S-only.)
- Substrate files are hash-pinned by R1; their internals are fixed.

### R5 — Canonical control flow
- Module source: only `while` loops, and every `while` must match the
  canonical bounded-counter form `while(<counter><<bound>)` (the counter
  incremented by exactly 1 in the body). `for`/`loop` tokens, `while(true)`,
  or any other condition shape → FAIL naming `R5`. (Idiom-narrowing: keeps
  the R3 linear scan sound; hangs are additionally caught by replay timeout.)

### R6 — Banned tokens and literals
- R6a: any BANNED-EXPLICIT token (§R2) in module source → FAIL naming `R6a`.
  (Belt-and-suspenders over the R2 fail-closed rule; gives named attestations.)
- R6b: string literals in module source must not contain `urandom`, `/dev/`,
  `/proc/`, `/sys/` (runtime-built device-path class — v2 red-team). Violation
  → FAIL naming `R6b`.

### R7 — Binary correspondence
- sha256 of the presented binary must equal the manifest BIN record.
- The runner rebuilds the binary from the frozen source with the frozen
  toolchain and requires byte-identical output (toolchain verified
  deterministic 2026-09-20). Mismatch → FAIL naming `R7`. (Rebuild lives in
  the shell runner — deterministic glue, not checker logic — because Zag
  cannot spawn processes.)

### R8 — v2 tripwire (informational only)
- The frozen v2 checker (`rngscan_v2`, `ee962e53817c81721996a8086c5e42530da07316250b1a4906ab74a56a3d9e5d`)
  keeps running on the module as a cheap tripwire. Its verdict is recorded in
  the attestation; it carries NO kill bar and cannot flip PASS→FAIL or
  FAIL→PASS.

**Verdict:** PASS iff R1–R7 all pass AND the replay matrix (§5) passes. R8 is
recorded only. The attestation lists every rule's verdict.

## 3. Gates

### K1′ — prereg-frozen allowlist + replay matrix
Passes iff (a) this prereg (+ `INTRINSIC_AUDIT.md`) was committed before any
implementation code, (b) the representative build passes R1–R7, (c) the
replay matrix (§5) passes on the frozen binary. The matrix itself is being
built in parallel by the phase-1 lead; §5 is the interim matrix and the
handoff point.

### K2′ — build-scoped blind red team (20 plants)
- A SEPARATE red-team agent authors 20 plants against a build tree cloned
  from the representative template. Required disguise classes (adapted from
  v2 §8.1): computed syscall immediate; runtime-built `/dev/urandom` path;
  partial-init loop; early-return-before-init; env-family token; clock
  intrinsic; cpuid/rdmsr read; port IO; slice_ptr address leak; uninit read
  via aliased slice; `_zag_rand`-named call (fail-closed check); renamed
  table indexed by uninit; getenv-driven branch; extra unlisted `.zag` file
  smuggled into the tree; modified substrate with own manifest; non-canonical
  while; struct-based hidden state; `_zag_raw_syscall` with unlisted literal
  (e.g. 228); plus novel-class attempts.
- Each plant: red team supplies source tree + manifest; the phase-2 lead
  builds the binary from that source with the frozen toolchain (red team never
  supplies binaries) and runs the FROZEN certifier + replay. No certifier
  changes between plants — any change is a new version, restart from plant 1.
- Scoring per plant: banned-idiom plant (violates R2–R6 or the explicit banned
  list) must FAIL naming a rule, or diverge on replay. **A banned-idiom plant
  that gets PASS = MISS → K2′ FIRES: this version is DEAD, stop the line,
  report honestly. Never patch-and-continue.**
- A plant that passes R1–R8 AND replay but is judged (by the red-team lead,
  with phase-2 concurrence) to contain a genuine entropy source outside the
  preregistered categories is a NOVEL CLASS: it does NOT kill the version and
  is NOT silently patched — it needs a dated prereg amendment with Micah's
  re-approval before the certifier may claim coverage.

### K3′ — hardened replay on the exact frozen binary
- N=8 runs, byte-identical stdout; heap pre-dirtying; allocation-pattern
  variation; deployment-like conditions; per the preregistered matrix (§5).
- Timing: the phase-1 hardened replay harness is being built in parallel.
  Prepare the frozen binary + K3′ protocol now; the final K3′ attestation runs
  against the phase-1 harness when it lands. If phase 1 is late, run K3′ on
  the interim matrix (§5) and explicitly flag hardened-replay re-verification
  as PENDING. **Never claim K3′ final on the interim.**

## 4. Certifier implementation (to be built after this freeze)

- Pure native Zag: `certifier/thincert.zag`, compiled with the frozen znc.
  CLI: `thincert <manifest> <builddir> <binary> <replay-evidence> <attestation>`
  Exit 0 PASS / 1 FAIL (attestation written either way) / 2 usage-IO error.
  Vendored: `R33_NATIVE_IO_V1.zag`, `R33_NATIVE_SHA256_V2.zag` (hashes as in
  the v2 build log). Tree walk via getdents64 (`_zag_raw_syscall(217,…)`) —
  the certifier is the checker, not a trial build; the call is deterministic.
- The no-RNG law applies to the certifier itself: no clock, no randomness,
  deterministic given inputs. No wall-clock in attestations (keeps reruns
  byte-identical).
- Runner `runner/run_thincert.sh`: deterministic shell glue — rebuild-compare
  (R7), replay matrix (§5), v2 tripwire invocation, certifier invocation,
  evidence files. Python only as GitHub commit glue / log analysis.

## 5. Replay matrix

**Interim matrix K3′-interim** (runs against the frozen binary; all runs
`timeout 120`; stdout byte-compared):
1–2. Baseline ×2: identical argv/env → must be byte-identical (core check).
3. `MALLOC_PERTURB_=165` → must equal baseline.
4. `MALLOC_PERTURB_=255` → must equal baseline.
5. Bloated environment (+100 dummy vars) → must equal baseline.
6. Different cwd → must equal baseline.
7. stdin=/dev/null → must equal baseline.
8. Alt-state file → must DIFFER from baseline (varies_with_state sanity).
Exit codes must be 0 on runs 1–7. Any divergence on 1–7, or equality on 8,
fails K3′. (Honest note: fresh-process zero pages blunt MALLOC_PERTURB_
against allocators that mmap directly — the static R3 is the load-bearing
gate for uninit reads; replay is the behavioral gate. Stated, not hidden.)
**Phase-1 handoff:** when the hardened replay harness lands, re-run the full
matrix on it and promote K3′ to final; until then K3′ stays INTERIM-flagged.

## 6. Blind red-team protocol

Adapted from v2 prereg §8 (same blinding discipline):
1. After the certifier binary is built and frozen (sha256 recorded), the
   red-team lead — a separate subagent — receives ONLY: this frozen prereg,
   `INTRINSIC_AUDIT.md`, the clean template (`repbuild/` source + fixtures +
   build/run instructions), and a blank scorecard. NEVER the certifier's
   implementation source, never hints about rule internals beyond this prereg.
2. The phase-2 lead does NOT author plants.
3. The certifier is a FIXED artifact during the round: no per-plant tuning.
4. Each plant: compile with the frozen toolchain (by the phase-2 lead),
   run frozen certifier + replay → expect FAIL (banned-idiom) or scored
   novel-class. A banned-idiom PASS is a MISS; miss rate > 0 fires K2′.
5. Adjudication: red-team lead classifies each plant banned-idiom vs
   novel-class; phase-2 concurs or escalates to the coordinator.

## 7. Purity accounting

- Certifier, runner glue logic, templates: pure Zag / deterministic shell.
  No RNG anywhere (standing law covers the tooling).
- Shell (`run_thincert.sh`): deterministic glue only — rebuild-compare,
  byte-compare replay, evidence files. Not checker logic.
- Python: GitHub commit glue and read-only log analysis only.

## 8. What is NOT certified (residual risks, stated)

1. No general proof of randomness-freedom for arbitrary Zag code — this
   certifier covers only the frozen build (debate §5: the general-detector
   shape was killed twice).
2. Environment-dependent nondeterminism deterministic under all lab replay
   conditions but not in deployment (§5 honest note on zero pages).
3. Hidden channels whose output never reaches measured behavior (cannot
   confound the trial by construction).
4. Toolchain trust: znc itself and the kernel are assumed deterministic;
   the intrinsic audit is pinned to `znc_linux_x86_64_abed8aa1`.
5. K3′ is INTERIM until the phase-1 hardened harness re-verifies.

## 9. Amendment discipline

Any change to §§2–6 after this freeze — rules, allowlist, matrix, bars —
needs a dated amendment with Micah's re-approval, like any rule change.
Novel-class red-team finds go through this path, never a silent patch.
A killed version (K2′ fired) stays dead; its successor restarts at §10.

## 10. Build order (frozen)

1. Capability spike in /tmp ONLY — done 2026-09-20 (intrinsic probe,
   build-determinism check, repbuild smoke test).
2. This prereg + INTRINSIC_AUDIT.md + frozen repbuild/MANIFEST.txt written,
   frozen, committed BEFORE any certifier code exists. ← YOU ARE HERE
3. Build the Zag certifier; dirty-module sanity (v2 dirty1–3,5 must FAIL
   naming rules; dirty4 is deterministic-by-construction, documents §R3
   rationale); clean round on the frozen repbuild must PASS.
4. Freeze certifier (source+binary sha256); commit implementation.
5. Blind red-team round (K2′, §6) via separate agent.
6. K3′ interim now; final on phase-1 harness.
7. Verdict.
