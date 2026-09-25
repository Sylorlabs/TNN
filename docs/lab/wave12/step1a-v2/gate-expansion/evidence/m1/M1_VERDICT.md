# M1 VERDICT — Seccomp capability sandboxing (fixed battery)

> Method crew M1, Arm C gate-expansion program. Frozen refs:
> `PREREG_GATE_EXPANSION.md` (umbrella, frozen 2026-09-25),
> `M1_SECCOMP_SANDBOX.md` (mini-prereg, frozen 2026-09-25).
> Battery executed 2026-09-25 ~21:05 UTC. Pure Zag, zero RNG, pinned toolchain
> `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
> NOTHING HERE IS SIGNED OR ADOPTED. No signature on Micah's behalf.

## 1. What was built

**Launcher** `src/m1_sandbox.zag` → `targets/m1_sandbox.bin`:
prctl(PR_SET_NO_NEW_PRIVS) → prctl(PR_SET_TSC, PR_TSC_SIGSEGV) →
seccomp-bpf filter install → personality(query|ADDR_NO_RANDOMIZE) →
execve(target, argv=["target"], envp=[]). This process *becomes* the target;
the outer harness reads exit/signal: 0=PASS, 139 (SIGSEGV)=FAIL,
159 (SIGSYS)=FAIL, else INCONCLUSIVE.

**Filter** `filter.bin` (72 bytes, 9 insns): KILL_PROCESS on nr 318
(getrandom), 228 (clock_gettime), 96 (gettimeofday); ALLOW everything else;
x86-64 arch gate. Decoded and jump-verified (see §6).

**Targets**: 12 plants + 5 clean modules, each a `variation.zag`-style module
with `vary_expr` exercised by a fixed driver main (fixed 96-byte input,
256-byte zero-pattern state, 256-byte out). Corpus plants used verbatim
(main stripped, driver appended); P07 and P12 crew-built per prereg;
C01/C02/C04/C05/C06 crew-written. Generation: `src/gen_battery.py`.

## 2. Build record (SHAs)

- Launcher, 2/2 byte-identical builds:
  `fbc5f338627f63ac26cedae31acca7e003626ae0e146d06fb566b9cc0771ced5`
- Filter bytes: `ea94a7c4fc46640dbb2cfe13c659184160f26ca36055d49921f20dbe3fd3c9b1`
- Target SHAs: `logs/SHAS.txt` (all 17 binaries + launcher source + filter).
- P07 ELF (168 bytes, regenerated deterministically per run):
  `57a1d377127eeec5735cfb80c654a519f55dd3a46e49b37cdf3ebaccade4d46f`
  (bytes verified against design; prints "TSC", exits 0 when run unsandboxed).

## 3. Kill table (r2/r3/r4 — unanimous)

| Plant | Source | Frozen expectation | Observed | Signal | Counting |
|---|---|---|---|---|---|
| P01 | v1 plant01 (getrandom) | FAIL (SIGSYS) | FAIL | SIGSYS rc=159, nr 318 | CAUGHT — kill |
| P02 | v1 plant06 (clock_gettime) | FAIL (SIGSYS) | FAIL | SIGSYS rc=159, nr 228 | CAUGHT — kill |
| P03 | v1 plant03 (/dev/urandom) | FAIL or PASS-NEUTRALIZED (AT-RISK) | PASS rc=0 | — | CAUGHT — neutralized* |
| P04 | v1 plant11 (uninit) | OUT-OF-SCOPE (gap) | PASS rc=0 | — | GAP (excluded) |
| P05 | v1 plant20 (env-var) | PASS-NEUTRALIZED | PASS rc=0 | — | CAUGHT — neutralized |
| P06 | v1 plant19 (ASLR leak) | PASS-NEUTRALIZED | PASS rc=0, out0=247 stable x3 | — | CAUGHT — neutralized |
| P07 | crew-built (rdtsc ELF) | FAIL (SIGSEGV) | FAIL | SIGSEGV rc=139, rdtsc | CAUGHT — kill |
| P08 | v1 plant16 (hash order) | OUT-OF-SCOPE (gap) | PASS rc=0 | — | GAP (excluded) |
| P09 | v3 blind plant17 @7b64c89 (innocent tables) | OUT-OF-SCOPE (gap) | PASS rc=0 | — | GAP (excluded) |
| P10 | k2prime plant19 (machine-id) | OUT-OF-SCOPE (gap) | PASS rc=0 | — | GAP (excluded) |
| P11 | k2prime plant20 (argv) | PASS-NEUTRALIZED | PASS rc=0 | — | CAUGHT — neutralized |
| P12 | crew-built (§10 class 5, invoke-discard) | FAIL (SIGSYS) | FAIL | SIGSYS rc=159, nr 318 | CAUGHT — kill |

\* P03 note: as compiled, v1 plant03's `open(2)` uses a non-NUL-terminated
string literal and fails (fd<0, verified fd=-36 on a probe), so it never
reaches read(2) — PASS-NEUTRALIZED as built. The AT-RISK class is real
anyway: with a proper NUL-terminated path, open("/dev/urandom") SUCCEEDS
under the sandbox (fd=3, rc=0, verified) — read(2) of urandom is allowed by
design (blocking it breaks legitimate file IO). This is mini-prereg §5
option (a) as implemented: the P03 *class* (real urandom reads) is a
documented gap; the P03 *battery plant* is caught-neutralized per the
frozen counting rule.

| Clean | Expect | Observed (r2/r3/r4) |
|---|---|---|
| C01 canonical variation | PASS | PASS rc=0, vary rc=0 |
| C02 state-dependent phrasing | PASS | PASS rc=0, vary rc=0 |
| C04 pinned file IO | PASS | PASS rc=0, vary rc=0 (see §5 note) |
| C05 instruction-count timeout | PASS | PASS rc=0, vary rc=0 |
| C06 fixed-order hash map | PASS | PASS rc=0, vary rc=0 |
| C03 fenced RNG | OUT-OF-SCOPE pre-test | not run (cannot run under sandbox by design) |

## 4. Kill-bar scoring

- **K-CATCH: 8/8 in-scope CAUGHT — PASS.** 4 by kill (P01, P02, P07, P12),
  4 by neutralization (P03, P05, P06, P11). Zero misses.
  > FROZEN-TEXT ERRATUM: mini-prereg §4 says "9 in-scope plants" but
  > enumerates 8 (P01,P02,P05,P06,P07,P11,P12 + P03 at-risk). 12 − 4
  > out-of-scope (P04,P08,P09,P10) = 8. Denominator is 8; all 8 caught.
  > Recorded as erratum, not silently corrected.
- **K-CLEAN: 5/5 PASS — PASS.** No false positives. C03 out-of-scope pre-test
  per frozen §3 (documented limitation, not a false positive).
- **K-DET: 3/3 byte-identical full-battery reruns — PASS.**
  `logs/battery_r2.log`, `r3`, `r4` byte-identical
  (sha256 `c82243a220cc0888541f53425e174e626e2f6ad0edfa432aab7c82a38e609475`
  after the run-id header line) — full stdout included, not just verdicts.
  Launcher binary byte-identical across 2 builds (§2).
- **K-RED:** pending — blind red team not yet dispatched. Frozen launcher
  + filter bytes above are the interface the red team gets.

**Method status: SURVIVES the fixed battery (all four applicable bars pass).**

## 5. Notes and corrections during the round

- r1 was a shakedown run: my C04 module passed a non-NUL-terminated string
  literal to open(2) (fd<0 → vary rc=2, process still exit 0). Fixed C04 to
  use a NUL-terminated copy; r2/r3/r4 use the fixed binary (vary rc=0).
  Harness bug, not a method issue. K-DET triple = r2, r3, r4.
- P06 neutralization confirmed effective: leaked-pointer out0=247 identical
  across all three runs (ADDR_NO_RANDOMIZE working).
- P04's uninit read returned 0 on all three runs (allocator-fresh pages);
  it remains an out-of-scope gap regardless of this run's luck.
- An unattributed file `src/p07.zag` (a P07 draft with different helpers,
  sha256 `91a605d08307db265c5660e2cfbe8baf98dc7e04e99ef763f379adc247d0b4d4`)
  appeared in the evidence dir during the round; I did not write it.
  Quarantined as `src/UNATTRIBUTED_p07_draft.zag`, NOT used in the battery.

## 6. Frozen-text deviations (documented, not silent)

1. **seccomp(2) instead of prctl(PR_SET_SECCOMP).** This VM's runtime
   pre-installs its own seccomp filter (PR_GET_SECCOMP returns 2), and
   prctl(38, 2, prog) returns EINVAL — verified via Python ctypes with
   correct argtypes, even for a trivial 1-instruction ALLOW filter. The
   underlying seccomp(2) syscall (nr 317, SECCOMP_SET_MODE_FILTER) installs
   the IDENTICAL 72 filter bytes with rc=0 (prctl is a thin wrapper over
   the same kernel path). Filters stack: ours evaluates first. Kill
   semantics, filter bytes, and verdict procedure are unchanged.
2. **personality(0xffffffff | ADDR_NO_RANDOMIZE).** 0xffffffff is the QUERY
   constant (verified on this VM: returns the persona without changing it),
   so the launcher queries first, then sets (cur | 0x40000). Intent preserved;
   computed via shift to stay in i64 literal range.
3. Filter decode (from `filter.bin`, little-endian u16 code / u8 jt / u8 jf / u32 k):
   `[LD ABS 4] [JEQ 0xc000003e jt=1] [RET KILL] [LD ABS 0]
    [JEQ 318 jt=2] [JEQ 228 jt=1] [JEQ 96 jt=0 jf=1] [RET KILL] [RET ALLOW]`
   — jump targets land exactly as designed (kill insn / allow insn).

## 7. Method limitations (for the head-to-head and red team)

- L1: The *specific* killed syscall number is not recoverable post-mortem
  from SIGSYS (no siginfo without SECCOMP_RET_TRAP + handler; out of frozen
  scope). Verdict records signal only; the plant→syscall mapping above is
  by construction.
- L2: /dev/urandom (and any file) readable via read(2) — P03-class gap,
  pre-declared AT-RISK, §5 option (a) as implemented.
- L3: Blind by design to P04 (uninit), P08/P09 (table order), P10
  (machine-id/file content) — no kernel boundary crossed. These are the
  red team's expected focus (umbrella §5 categories b/c).
- L4: The launcher is trusted code; it fails closed (any prctl failure
  exits non-zero *before* execve, never runs the target unsandboxed).
- L5: vDSO clock reads BYPASS the filter — PROVEN empirically. A C probe
  installing the identical 72 filter bytes via seccomp(2): glibc
  clock_gettime(CLOCK_REALTIME) SURVIVED (uses __vdso_clock_gettime — no
  syscall issued), direct __vdso_clock_gettime resolved via dlopen SURVIVED,
  while the raw syscall(228) in the same process died SIGSYS (filter proven
  live). Any plant reaching the clock through the vDSO — including ordinary
  libc clock_gettime — is invisible to this method. A Zag plant cannot
  easily reach the vDSO today (no libc linkage), but a red-team plant could
  ship its own vDSO trampoline via the P07 ELF technique. Not exercised in
  the battery; all battery clock plants use the real syscall.

## 8. Coverage map

- Killed at the boundary: P01 (getrandom), P02 (clock_gettime), P07 (rdtsc),
  P12 (getrandom, unconsumed).
- Neutralized (channel removed by launcher): P05 (empty env), P06
  (ASLR off), P11 (fixed argv), P03-as-built (never opens).
- Gaps: P04, P08, P09, P10 (out-of-scope, no syscall boundary);
  P03-class real urandom reads; vDSO clock_gettime (L5).

## 9. Red-team readiness

Frozen launcher: `evidence/m1/targets/m1_sandbox.bin`
(`fbc5f338627f63ac26cedae31acca7e003626ae0e146d06fb566b9cc0771ced5`).
Public interface for the blind red team: *a Zag-compiled target binary is
execve'd with argv=["target"] and empty env, after PR_SET_TSC(SIGSEGV),
seccomp-bpf killing getrandom/clock_gettime/gettimeofday, and
ADDR_NO_RANDOMIZE; verdict = exit 0 PASS / SIGSYS|SIGSEGV FAIL / else
INCONCLUSIVE.* Awaiting the 12-plant red-team manifest path.

## 10. Evidence index

- `src/m1_sandbox.zag` — frozen launcher source
- `src/t_p{01..12}.zag`, `src/t_c{01,02,04,05,06}.zag` — target sources
- `src/gen_battery.py` — battery generator (deterministic)
- `src/p09_plant17.orig.zag` — P09 source as fetched (sylorlabs/TNN@7b64c89)
- `src/R33_NATIVE_IO_V1.zag` — substrate (copy of the plant corpus file)
- `filter.bin` — committed BPF program bytes
- `targets/*.bin` — frozen binaries (SHAs in `logs/SHAS.txt`)
- `logs/battery_r{2,3,4}.log` — per-plant run logs (rc/signal/stdout)
- `run_battery.sh` — battery runner
- `runs/r{1..4}/` — per-run workdirs (c04_data.bin, p07_rdtsc.elf artifacts)
