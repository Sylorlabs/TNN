# MINI-PREREG M1 — Seccomp capability sandboxing

> **FROZEN — 2026-09-25** under `PREREG_GATE_EXPANSION.md`.
> Method: enforce no-RNG at the kernel boundary, not by detection.

## 1. Hypothesis

Token-based auditors die to novel idioms because the idiom space is
inexhaustible. The kernel boundary is not: every entropy/clock source a
Linux process can reach (getrandom, clock_gettime, gettimeofday, rdtsc,
/dev/urandom) crosses a syscall or instruction the OS can deny. A gate
that DENIES the capability does not need to recognize the disguise.

## 2. Decision procedure (frozen)

**Launcher** `m1_sandbox.zag` (pure Zag, pinned toolchain):

1. Calls `prctl(PR_SET_TSC, PR_TSC_SIGSEGV)` via `_zag_raw_syscall` —
   rdtsc raises SIGSEGV.
2. Installs a seccomp-bpf filter via
   `prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)`:
   - `SECCOMP_RET_KILL_PROCESS` on syscall numbers
     318 (getrandom), 228 (clock_gettime), 96 (gettimeofday).
   - `SECCOMP_RET_ALLOW` on everything else (the target needs
     read/write/open of data files, mmap, etc.).
3. Calls `personality(0xffffffff | ADDR_NO_RANDOMIZE)` — disables ASLR
   for the target (addresses deterministic across runs).
4. `execve`s the frozen target binary with a **fixed minimal env**
   (empty envp) and fixed `argv[0]="target"`.

**Verdict.**
- Target exits 0 → `PASS`.
- Target dies to SIGSYS (seccomp) or SIGSEGV (rdtsc) → `FAIL`
  with the killing signal + syscall number recorded.
- Any other death → `INCONCLUSIVE` (counts as FAIL for K-CATCH plants,
  as method-bug for K-CLEAN modules; recorded separately).

The filter program bytes are committed; the launcher is rebuilt
deterministically (2/2 byte-identical builds required).

## 3. Battery mapping (pre-declared scope — frozen)

| Plant | Expected | Rationale |
|---|---|---|
| P01 getrandom | FAIL (SIGSYS) | syscall 318 killed |
| P02 clock_gettime | FAIL (SIGSYS) | syscall 228 killed |
| P03 /dev/urandom | FAIL or PASS-NEUTRALIZED | open(2) allowed; but read(2) of urandom returns bytes — hmm, /dev/urandom is read via read(2), NOT getrandom. **Pre-declared AT-RISK** (see §5) |
| P04 uninit | OUT-OF-SCOPE (gap) | no kernel boundary crossed |
| P05 env-var | PASS-NEUTRALIZED | env cleared by launcher; reads return deterministic empty |
| P06 ASLR leak | PASS-NEUTRALIZED | ADDR_NO_RANDOMIZE; leak is deterministic |
| P07 rdtsc | FAIL (SIGSEGV) | PR_SET_TSC |
| P08 hash order | OUT-OF-SCOPE (gap) | no kernel boundary crossed |
| P09 innocent tables | OUT-OF-SCOPE (gap) | deterministic tables; no syscall |
| P10 machine-id | OUT-OF-SCOPE (gap) | file read via allowed read(2); content lab-constant |
| P11 argv[0] bytes | PASS-NEUTRALIZED | argv[0] fixed by launcher |
| P12 invoke-discard | FAIL (SIGSYS) | invocation crosses the boundary even if unconsumed |

**Counting rule (frozen):** FAIL and PASS-NEUTRALIZED both count as
CAUGHT for K-CATCH. OUT-OF-SCOPE plants are excluded from the K-CATCH
denominator (recorded as gaps in the coverage map, not kills).
AT-RISK plants count normally: a miss kills.

**K-CLEAN mapping:** C01, C02, C04, C05, C06 must PASS. C03 (fenced RNG)
declared OUT-OF-SCOPE pre-test: the subset has no RNG by design; a
fenced-RNG build cannot run under this sandbox (documented limitation,
not a false positive).

## 4. Kill-bar instantiation

- K-CATCH: 9 in-scope plants (P01,P02,P05,P06,P07,P11,P12 + P03 at-risk
  + P05/P06/P11 neutralized) — all must be CAUGHT.
- K-CLEAN: C01,C02,C04,C05,C06 — 5/5 PASS required.
- K-RED: 12 novel plants, blind, per umbrella §5. Expected red focus:
  memory/env/file channels (the sandbox's known gaps).
- K-DET: 3/3 byte-identical full-battery reruns (launcher + verdicts).

## 5. Known hard problem (stated pre-test)

P03 (/dev/urandom via read(2)): blocking read(2) entirely breaks
legitimate file IO. Options the crew may implement (frozen choice must
be committed before testing): (a) leave allowed → expected miss,
recorded; (b) Landlock/path-based open restriction — allowed ONLY if
implemented via a second mechanism with its own mini-spec committed
pre-test. No post-hoc fixes.

## 6. Evidence layout

`wave12/step1a-v2/gate-expansion/evidence/m1/`:
`m1_sandbox.zag`, filter bytes, build log + SHAs, per-plant run logs
(exit/signal), `M1_VERDICT.md` with the kill table.
