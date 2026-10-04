# TOOLCHAIN AND ENVIRONMENT (canonical, verified 2026-10-03)

This document records the verified facts required to reproduce any pure-Zag
experiment on this host. It exists because the previous canonical lanes recorded
their environment only in per-lane NAMECHECK.md prose, and because one
undocumented compiler default silently produces unusable binaries.

## 1. Zag compiler

| Property | Value |
|---|---|
| Path (this host) | `/Users/Shared/micah/Documents/TNN/.bin/znc` |
| Origin | `src/tools/toolchain/znc_macos_arm64_7cacbfc0` on `origin/main` |
| sha256 | `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956` |
| file bytes | 7579136 |
| format | Mach-O 64-bit executable arm64 |
| version string | `znc 2026.07.0-dev (edition 2026)` |
| compiler git commit | `7cacbfc04f6cffec02ea9b1d5ff6702fe2e93f3c` |
| target | macos-arm64 |

Provenance verified against
`src/tools/toolchain/R32_E45_ARM64_7CAC_AGGREGATE_ABI_MANIFEST.json`:
the recorded `compiler.sha256` matches the extracted binary exactly, and every
artifact hash in that manifest re-verifies against `origin/main`.

Note the manifest's own self-declared limits, which we adopt as binding:
`qualification_evidence: false`, `promotion_eligible: false`. It is deployment
evidence for an ABI boundary, not a qualification artifact.

### 1.1 MANDATORY COMPILE FLAGS

```
znc --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache FILE.zag
```

**`--target macos-arm64` is mandatory on this host.**

Without it the compiler does not error. It silently emits
`ELF 64-bit LSB executable, x86-64` which cannot run on macOS/arm64:

```
$ znc probe.zag
znc: wrote native binary probe (84 bytes main, 0 external tools)
$ ./probe
zsh: exec format error: ./probe
```

This is a silent-corruption failure mode: the compile step reports success and
exit 0, and the failure only appears at run time. Any worker that omits the flag
will report infrastructure failure while believing the fault is scientific.
The `znc` shell wrapper in `.env/pure-zag.sh` injects the flags so the flag
cannot be forgotten.

## 2. Determinism

Three consecutive builds of an identical source produced byte-identical
binaries (`dbf2720fc91762b5b4b758134dc40852a7ad7eff1ba1de05cc26873d9e009d05`,
3/3). Determinism is currently a property of the toolchain and is preregistered
as a bar (3/3 byte-identical) in canonical experiments.

## 3. Pure-Zag enforcement

Charter section 4 requires that forbidden interpreters be *unavailable*, not
merely unused.

Source `/Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`, then call
`tnn_pure_zag_report`. Expected output ends with:

```
  forbidden_count=0
  VERDICT: PURE-ZAG-CLEAN
```

Enforcement is two layers:

1. Hard-fail shims in `.env/shims/` shadow 33 forbidden names (`python`,
   `python3`, `node`, `bun`, `deno`, `tsc`, `cc`, `gcc`, `g++`, `clang`, `rustc`,
   `cargo`, `julia`, `perl`, `ruby`, `R`, `make`, `cmake`, ...) and are prepended
   to `PATH`. Invoking any of them prints `PROCESS-FAIL` and exits 127.
2. A restricted `PATH` excluding all package-manager prefixes
   (`/opt/homebrew/bin` and friends).

### 3.1 Honest limitation

The shims intercept by NAME. A hard-coded absolute path such as
`/usr/bin/python3` bypasses layer 1, and layer 2 cannot exclude `/usr/bin`
because `git`, `sh`, and core POSIX utilities live there.

This is therefore **enforcement by deterrence plus audit, not a security
sandbox.** It is sufficient to make accidental use impossible, which is what the
charter requires, but it does not constitute adversarial isolation. Isolation
for sealed evaluation must come from role separation (builder never receives
sealed answer keys), not from the shell environment.

### 3.2 Note on this host

`python3`, `node`, `bun`, `perl`, `ruby`, `cc`, `gcc`, `rustc` were all present
on `PATH` before enforcement. Prior canonical lanes recorded having used a
`safebin` PATH to achieve the same effect, which indicates this is a recurring
host-level condition rather than a one-off.

## 4. Host capacity (measured, not assumed)

| Resource | Value |
|---|---|
| CPU | 10 physical / 10 logical |
| RAM | 24 GB |
| Disk free | 326 GB |
| Compiler invocation cost | ~0.07 s |

### 4.1 Measured compile concurrency

Parallel compiles of identical-cost sources:

| Parallel | Wall | Throughput |
|---|---|---|
| 10 | 0.13 s | 76.9 /s |
| 20 | 0.25 s | 80.0 /s |
| **40** | **0.41 s** | **97.5 /s** |
| 60 | 0.63 s | 95.2 /s |
| 80 | 0.88 s | 90.9 /s |

Compile throughput peaks near 40 concurrent and decays beyond it.

### 4.2 Concurrency decision

Compilation is 0.07 s, so compiling is NOT the bottleneck. The bottleneck is
CPU-bound Zag *execution* on 10 physical cores. Therefore:

- **Total worker pool: 40.**
- **Concurrent CPU-heavy execution: 12-16** (semaphore-limited).
- Light lanes (preregistration, world design, red teaming, analysis,
  documentation) are unbounded within the 40 and are scheduled preferentially
  when cores are saturated, per charter section 97.

This is a measured starting point, not a fixed cap. Re-measure when the mix of
experiment runtimes changes, and record the measurement.

## 5. Branch / toolchain mismatch (unresolved, affects reproducibility)

Canonical lanes through C410 were built with
`znc_linux_x86_64_abed8aa1` (a **Linux x86-64** binary) and record
`znc_linux_x86_64_abed8aa1` in their NAMECHECK files. This host is macOS/arm64.
That implies those experiments were executed on a different machine or under
emulation.

Consequences:

- Their recorded hashes cannot be re-verified on this host without the Linux
  binary and a compatible runner.
- `origin/tnn-native-lab` does NOT contain `znc_macos_arm64_7cacbfc0`; that
  binary exists only on `origin/main`. Workers on `tnn-native-lab` must extract
  it from `origin/main`.

This is recorded as an open reproducibility defect, tracked for the
DEFECT-AUDIT lane. It is not silently ignored.
