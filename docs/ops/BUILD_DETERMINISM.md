# BUILD-TO-BUILD DETERMINISM — VERDICT AND EVIDENCE

**Lane `buildstab`. Claims C530–C539. Prereg `PREREG.md` (commit 4b225a097),
frozen before any build was run. Nothing in this document was edited after
seeing a result.**

Host: macOS 26.6.2 (Darwin 25.6.0) arm64, 10 cores, shared.
Compiler: `/Users/Shared/micah/Documents/TNN/.bin/znc`
sha256 `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`,
`znc 2026.07.0-dev (edition 2026)`, `--target macos-arm64`.

---

## 0. VERDICT

**BUILD-TO-BUILD IS BYTE-STABLE.** Not "stable in the baseline arm" — stable in
every arm and probe. **162 builds** across **3 sources of different sizes**
(1.8 KB / 56 KB / 75 KB), **6 condition arms**, and **8 condition probes**
produced **exactly one binary sha256 per source**. Not one build differed.
Not one run differed (270+ runs, all 3/3 byte-identical). No empty outputs.

The brief's §4.1 reproduction of the canonical corpus is therefore **not a
one-off**. Blocker **B13 stands**.

The `lane/corefreeze` report of "plan order differed across rebuilds" is
**REFUTED as build nondeterminism**. It is not B17 and not the B16 byte-offset
trap. See §4.

---

## 1. THE HEADLINE NUMBER

Full ledger of the 90 matrix builds (6 arms × 3 sources × 5 builds):

```
total builds:        90
distinct sha256:      3        <- one per SOURCE, zero within a source
  30  3528ec15cd507ddcb50b2681322d39160298f24810b6136c90dba37001af795d   (S3)
  30  797a0a21ecf7bfdb0a22e8509c06e4d20331fd5b0da3343e4578f4e64f522602   (S1)
  30  b2c4382344e79f6e6297b9a849a1f9f5abbcd99bc36217e2cfde729ebe9101a4   (S2)

builds whose binary was 3/3 byte-identical on stdout:  90 / 90
builds with a non-3/3 stdout:                          0
builds that produced EMPTY stdout:                     0
```

Adding the 65 probe builds and the 7 cf-probe builds: **162 builds, 3 distinct
binaries, one per source.**

| id | source | bytes | lines | source sha256 | binary sha256 (all builds) |
|---|---|---|---|---|---|
| S1 | `bt_small.zag` (this lane) | 1 779 | 54 | `2936623db888328103cfe567a8033b9f533808546290872d236d9e44eb93b686` | `797a0a21ecf7bfdb0a22e8509c06e4d20331fd5b0da3343e4578f4e64f522602` |
| S2 | `c8_shim.zag` (c8_full + `_zag_print`) | 75 171 | 2 468 | `e33420b9debf5c91e6d435e30aa8e2485ca02623fac50664988d699144996a90` | `b2c4382344e79f6e6297b9a849a1f9f5abbcd99bc36217e2cfde729ebe9101a4` |
| S3 | `tnn2_frozen_ref.zag` (frozen, untouched) | 56 508 | 1 591 | `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` | `3528ec15cd507ddcb50b2681322d39160298f24810b6136c90dba37001af795d` |

| source | stdout sha256 | stdout bytes |
|---|---|---|
| S1 | `a1f2b9977b018d71f11bf79f7767216bb33815c13e4548526c6cb64fe030cf6c` | 27 |
| S2 | `ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7` | 3 344 |
| S3 | `37c7b552fe56c9b03b93aadb8108dfbd1d8031c056dd0e2cdcb6a1fb88cd3911` | 1 358 |

---

## 2. THE 6-ARM MATRIX (N=5 clean-state builds per cell, 3 runs per build)

Clean state = output binary `rm -f`'d and `.zag-cache` purged before every
build. Every run through `tnnwatch.sh reg <name> 300 <bin>`.

| arm | condition | S1 | S2 | S3 |
|---|---|---|---|---|
| **A0** | baseline: `--no-zagd --no-analyze --no-foreground-cache`, cwd = lane, out = lane, pure-zag shim PATH, cache purged | 5/5 same | 5/5 same | 5/5 same |
| **A1** | baseline flags, cache **warm** (no purge) | 5/5 same | 5/5 same | 5/5 same |
| **A2** | **NO FLAGS AT ALL** beyond `--target macos-arm64` | 5/5 same | 5/5 same | 5/5 same |
| **A3** | cwd = `/tmp`, output into `/tmp/bt_out_…` | 5/5 same | 5/5 same | 5/5 same |
| **A4** | **host PATH** (`/usr/bin:/bin:/usr/sbin:/sbin:.bin`), shim PATH removed | 5/5 same | 5/5 same | 5/5 same |
| **A5** | **fresh shell per build** (`env -i PATH=… HOME=… TMPDIR=…`) | 5/5 same | 5/5 same | 5/5 same |

The binary sha256 is **identical across arms**. Every arm produced exactly the
sha in the §1 table — e.g. S3 is `3528ec15…` whether built in the lane
directory with the pure-Zag shim PATH, or in `/tmp` with the host PATH, or
with a bare empty environment, or with no flags at all.

## 3. THE 8 PROBES (each N=5 unless noted)

| probe | condition varied | result |
|---|---|---|
| **P1** | source mtime forced to 5 distinct values (`touch -t`, epoch 978336000 … 1104912000) | 5/5 identical |
| **P2** | `--no-zagd` present vs **absent** | 5/5 identical both ways |
| **P3** | `--no-analyze` present vs **absent** (analyzer on) | 5/5 identical both ways |
| **P4** | `--no-foreground-cache` present vs **absent** (warm) | 5/5 identical both ways |
| **P5** | five **distinct** `-o` output paths | 5/5 identical |
| **P6** | `znc clean-cache` between every build | 5/5 identical |
| **P7** | **build order**: 5 rounds interleaving S3, S1, S2 | 15/15 identical (5 per source) |
| **P8** | project root containing a `zag.mod` (`znc init`) | 5/5 identical, and **same sha as the no-`zag.mod` build** |

### 3.1 `--no-zagd` IS GENUINELY EFFECTIVE — AND IT IS A NO-OP HERE

This was the mission's specific question, and the answer is stronger than
"verified disabled": **the daemon path is unreachable on this host in both
conditions.**

```
sibling `zagd` executable next to znc : 0        (only znc, znc_probe exist)
`znc status`                          : zagd status: not running (no status record)
build WITHOUT --no-zagd              : "znc: warning: zagd unavailable;
                                        foreground compilation continues without
                                        background planning"
zagd daemons visible on the host      : 2  (roots: .../zag/zag-poc  and
                                        /private/tmp/zagd-product.D5F58H/project)
.zag-cache directories created, wave-wide : 0
```

`znc` reaches its planner through a **sibling `zagd` executable** and through
per-project `./.zagd.lock` / `./.zagd.status` records. There is no sibling
`zagd`, so it can neither start nor attach to a daemon. The two daemons that
are running serve unrelated project roots and are not addressable from any TNN
lane. Building with and without `--no-zagd` gives the same binary sha256 five
times each. **`--no-zagd` cannot be the source of any cross-build variation on
this host.**

### 3.2 `--no-foreground-cache` IS ALSO A NO-OP HERE

`znc` documents a foreground machine cache at `./.zag-cache/foreground/`
(`machine.record`, `machine.code`, `machine.data`). **Across the entire
162-build wave, zero `.zag-cache` directories were ever created** — not in the
lane, not in `/tmp`, not for `--target x86-64`, and not even in a directory
containing a `zag.mod` (P8). The flag has nothing to switch off on this host.
This is *why* the builds are stable: the only mutable state `znc` documents is
absent, so each invocation is a pure function of (source bytes, flags, target).

---

## 4. IS "PLAN ORDER" GENUINELY NONDETERMINISTIC? **NO.**

The corefreeze observation (RESULTS.md §11) was: *"across different builds of
logically identical harness source, the plan order for one goal was observed to
differ (`1,0` vs `0,1`) in an isolated probe."*

I rebuilt the corefreeze harness myself. Concatenation per their PREREG §2:
`cf_base.zag + cf_data.zag + cf_engine.zag + c8_learn.zag + hq_module.zag`
(source sha `6a768e0420fa753d9f3b3cbcc92fb23b9ab2bc7e7614260e74e33b7262a4191c`,
84 385 bytes). `cf_probe.sh`, results in `cfprobe.log`.

### Q1 — N=5 builds from BYTE-IDENTICAL source

```
b1 rc=0 bin_sha=8599500d13aab0c5 out_sha=08969d50f51d78c5 out_bytes=35437  3/3 runs identical
b2 rc=0 bin_sha=8599500d13aab0c5 out_sha=08969d50f51d78c5 out_bytes=35437  3/3 runs identical
b3 rc=0 bin_sha=8599500d13aab0c5 out_sha=08969d50f51d78c5 out_bytes=35437  3/3 runs identical
b4 rc=0 bin_sha=8599500d13aab0c5 out_sha=08969d50f51d78c5 out_bytes=35437  3/3 runs identical
b5 rc=0 bin_sha=8599500d13aab0c5 out_sha=08969d50f51d78c5 out_bytes=35437  3/3 runs identical
```

Identical `porder` multiset every time:
`porder=1:0, 2:0,1, 3:0,2,1, 3:1,0,2, 3:1,2,0` (+ the `porder=0:` and
`porder=na` cases). **Plan order is 5/5 stable across builds.**

Side benefit: my independently assembled harness reproduces their headline
output **exactly** — `08969d50f51d78c5b7748fcc9e9a247964ac585aa4ea5a077bf07b92f8156da3`,
35 437 bytes, from a different worktree and a different concatenation. That is
a second, unplanned independent confirmation that the corefreeze harness is
reproducible on this host.

### Q2 — "LOGICALLY IDENTICAL" BUT BYTE-DIFFERENT source

Same six files, **permuted concatenation order** (source sha
`3b3304f0fa8bd43fff01470628a788882ef6d125946d9a16797090b25ce6efc2`):

```
bin_sha = 66af433754504d890e23f9bd82a01a3ca2b832f5c1c7eaf0a1e85735a837266c   (DIFFERENT binary)
out_sha = 08969d50f51d78c5b7748fcc9e9a247964ac585aa4ea5a077bf07b92f8156da3   (IDENTICAL output)
```

This is the decisive contrast. **The binary is sensitive to source byte order;
the observable output is not.** Two builds of source that is logically but not
byte identical give two different binaries and the *same* answer. So a worker
who re-concatenated a harness between builds — the normal way to build a Zag
program, since `cat` order is what "logically identical" glosses over — sees a
different binary sha and may read that as build nondeterminism.

### Q2b — whitespace-only source difference

Appending one trailing newline (source sha `9520ba7af1b8…`) leaves the binary
**identical** (`8599500d13aab0c5`). Whitespace at end of file is not
significant; file order is.

### Q3 — the B16 byte-offset trap: NOT PRESENT

```
fn get32(b:[]u8,off:i32)i32 {
  return (b[off] as i32)|((b[off+1] as i32)<<8)|((b[off+2] as i32)<<16)|((b[off+3] as i32)<<24);
}
```

Correctly implemented, byte offsets, exactly as brief §3.2. This is not a case
of a cell index passed where a byte offset was meant.

### Q4 — the B17 `[]u8 as *u8` defect: NOT PRESENT

```
grep -n "\[\]u8 as \*u8" cf_full.zag   ->  NONE
grep -o "[A-Za-z_0-9]* as \*u8" | sort | uniq -c
   1  as *u8          (i.e. `_zag_malloc(n) as *u8`, the legitimate form)
```

The only `*u8` source in the entire harness is `_zag_malloc`, which is the one
form `ZAG_TOOLCHAIN_DEFECTS.md` §6 calls correct. **B17 cannot explain the
corefreeze observation.** (B17's own nondeterminism is *run-to-run on a fixed
binary* anyway — a different phenomenon from build-to-build, and it would have
failed the 3/3 bar their probe passed.)

### The mechanism that DOES fit: a stale binary

Demonstrated directly:

```
build v1.zag -> probe                       : probe prints "PROBE_V1 planorder=1,0"
"rebuild" a source that FAILS to compile,
  same -o path, no rm                        : compile rc=1, "arm64: unknown identifier: this"
  binary still present                      : YES, sha unchanged
run probe again                             : still prints "PROBE_V1 planorder=1,0"
```

**A failed `znc` invocation leaves the previous binary in place, byte-identical,
and running it silently reports the old result with no error at the run step.**
The reported signature — run-to-run 3/3 stable, "rebuilds" disagreeing — is
exactly this. A probe that edits its source between builds, rebuilds into an
existing output path, and does not `rm` the binary and does not check the
compile exit code will compare an old binary against a new one and conclude the
compiler is nondeterministic.

`bt_matrix.sh` guards against this: it `rm -f`s the output and asserts
`rc -eq 0 && -f "$BIN"` before every single build, and every one of the 162
builds passed that guard.

### Conclusion on plan order

**Plan order is deterministic. Two candidate benign explanations remain and I
cannot separate them without the probe source, which was never committed:**
(a) the two "logically identical" builds had byte-different source (Q2 shows
this changes the binary while preserving output, and the corefreeze lane's
`cf_data.zag`/`cf_engine.zag` were both edited during the wave — mtimes
23:11 / 02:03 / 02:03), or (b) a stale binary from a failed or skipped rebuild.
Neither is compiler nondeterminism. **The B17 and B16 hypotheses are excluded
by inspection.**

---

## 5. MY OWN c8 REPRODUCTION, FROM SCRATCH

Not taken on trust. Done independently, in this lane, from the checked-in
`c8_full.zag`.

```
base    cogops_learnosc2/c8_full.zag
        sha256 ce401e34dae6c9abf9406954e8a516e82fb3d2fc5b17d2899a969f0ac4060421
        75 215 bytes / 2 468 lines

step 1  cp to lane, then ONE substitution (diff shows exactly one line):
        -  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0);
        +  _zag_print(b[0..c]);

step 2  shim source
        sha256 e33420b9debf5c91e6d435e30aa8e2485ca02623fac50664988d699144996a90
        75 171 bytes

step 3  znc --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache
        -> "wrote signed native binary (340948 bytes text, 697 bytes data,
            0 external build tools)"
        binary sha256 b2c4382344e79f6e6297b9a849a1f9f5abbcd99bc36217e2cfde729ebe9101a4

step 4  run under tnnwatch.sh reg bs_c8run1 300
        rc=0, 3 344 bytes, sha256
        ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7

cmp against checked-in cogops_learnosc2/c8_run1.txt
        (sha256 ae0ae3bf…e4ae7, 3 344 bytes)  ->  BYTE-IDENTICAL
```

**§4.1's claim reproduces. And it reproduces in all 30 builds of S2 across the
matrix, in every arm, with the same binary sha256.**

### A wording defect in §4.1 that should be fixed

§4.1 describes `c8_full.zag` as *"340948 bytes of text"*. The source file is
**75 215 bytes / 2 468 lines**. 340 948 is the size `znc` reports for the
emitted Mach-O **`__text` segment** of the binary. The reproduction is
unaffected; the description of the fixture is wrong and would mislead anyone
trying to find or size the file.

---

## 6. WHAT BRIEF §4.1 AND BLOCKER B13 SHOULD SAY

### 6.1 Replacement text for §4.1

> ### 4.1 PROOF THE `_zag_print` SHIM IS CORRECT (this settles blocker B13)
>
> `cogops_learnosc2/c8_full.zag` (75 215 bytes, 2 468 lines; the emitted
> Mach-O `__text` segment is 340 948 bytes) was rebuilt on this macOS/arm64
> host with the SINGLE substitution
> `_zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0)` →
> `_zag_print(b[0..c])` and run.
>
> ```
> reference c8_run1.txt (Linux x86_64 era): ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7  3344 bytes
> this host, macOS/arm64:                  ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7  3344 bytes
> *** BYTE-IDENTICAL ***
> ```
>
> **This is not a single lucky rebuild.** `znc --target macos-arm64` is
> byte-stable build-to-build: 162 builds of three sources (1.8 KB / 56 KB /
> 75 KB) under six condition arms and eight condition probes produced exactly
> one binary sha256 per source. The c8 binary is `b2c43823…` in all 30 of its
> builds, including with no compiler flags at all, from a different working
> directory, under the host PATH instead of the pure-Zag shim PATH, in a fresh
> `env -i` shell, and after `znc clean-cache`. See
> `docs/ops/BUILD_DETERMINISM.md`.
>
> Three consequences, all important:
>
> 1. **Blocker B13 is RESOLVED.** The canonical corpus is fully reproducible
>    on this host, and reproducibility is now a property of the toolchain
>    rather than a coincidence. Cross-platform determinism holds.
> 2. **The compiler is NOT miscompiling flat-arena indexed reads.** This
>    75 KB flat-arena program executes and produces byte-exact results, now in
>    30 independent builds. B16's "silent miscompilation of indexed reads"
>    remains an API trap (`get32`/`set32` take BYTE offsets — see
>    `ZAG_TOOLCHAIN_DEFECTS.md` §1), not a compiler defect.
> 3. **Any result computed on this host with an unpatched `o_flush` is
>    uncitable.** Re-run with the shim.

### 6.2 Replacement text for blocker B13 (§8)

> * **B13 RESOLVED 2026-10-03, RE-CONFIRMED 2026-10-04.** Canonical lanes
>   reproduce on this host: `c8_full.zag` rebuilt with the `_zag_print` shim
>   gives byte-identical output to the Linux-era `c8_run1.txt`
>   (`ae0ae3bf…`, 3344 B). **Build-to-build byte-stability established
>   separately (C530–C539): 162 builds, one binary sha256 per source.** The
>   contrary report from `lane/corefreeze` (plan order varying across rebuilds)
>   was tested and **refuted as build nondeterminism**; it is a byte-different
>   source state or a stale binary, not B17 (`[]u8 as *u8` is absent from that
>   harness) and not the B16 byte-offset trap. See `BUILD_DETERMINISM.md` §4.

---

## 7. BOUNDARIES — what this does NOT establish

1. **One compiler binary.** Everything here is the single pinned
   `znc 2026.07.0-dev`, sha `3093d12d…`. A different `znc` build is untested
   and need not be stable. Any citation of "reproducible" is relative to this
   compiler image.
2. **One target.** `--target macos-arm64` only. Linux x86-64, wasm and the GPU
   targets are out of scope. This is why "cross-platform determinism" rests on
   the c8 output match, not on the build matrix.
3. **Serial builds only.** Concurrent-build determinism is explicitly NOT
   tested; the host is shared (load ~7/10) and prereg §5 excluded it.
4. **A real cache path is untested.** Because no `.zag-cache` is ever created
   here, I have **not** shown that a warm foreground cache is itself
   deterministic. The determinism is real for this host's configuration; if a
   `zagd` sibling or a project root that engages the cache is ever installed,
   §3.1–§3.2 must be re-run. This is the single most likely way a future
   regression could enter.
5. **The corefreeze isolated probe does not exist.** It was never committed. I
   reproduced the *harness*, not the probe. Q1 rules out compiler
   nondeterminism for that harness at N=5; I cannot rule it out for a probe
   whose source I have never seen, only for a compiler that is provably stable
   on everything I can see.
6. **N=5, not N=infinity.** Five builds per cell detects a low-probability or
   load-dependent divergence poorly. It is strong against *systematic*
   nondeterminism (any hash-table-ordering, path-, time- or env-dependent
   codegen would have shown up) and weak against a rare one.
7. **`env -i` is not a fully empty environment** (PATH/HOME/TMPDIR survive). No
   attempt was made to deny the compiler `/dev/urandom` or a network.

---

## 8. NEXT EXPERIMENT

1. **Install a sibling `zagd` next to `znc` and re-run the matrix.** This is
   the only untested mutable-state path and therefore the only plausible route
   to a real regression. Preregister before: N=5 per arm, kill bar unchanged.
2. **Get the corefreeze probe.** Ask that lane for the isolated probe source,
   or reconstruct `1,0` vs `0,1` from `cf_data.zag` history
   (`git log -p` on `cf_data.zag`, edited twice during the wave). Settle (a)
   byte-different source vs (b) stale binary with a real artifact rather than by
   elimination.
3. **Make `zbuild.sh` fail loudly on a stale binary.** The cheapest structural
   fix for the whole class of false "nondeterminism" reports: `rm -f "$BIN"`
   before compiling, assert `rc -eq 0`, and assert the binary's mtime advanced.
   This one-line guard would have prevented the corefreeze observation.
4. **Extend the matrix to the other two frozen cores** (`l3_suf_intermediate`
   at ~2500 lines) to confirm stability scales with program size, and record the
   `__text` sizes so §4.1's "340948 bytes of text" style claim cannot recur.

---

## 9. REPRODUCERS

```
docs/lab/research-lead/overnight-20260928/buildstab/
  PREREG.md            frozen before any build (commit 4b225a097)
  bt_small.zag         fixture S1
  c8_shim.zag          fixture S2 = c8_full.zag + one substitution
  s3_tnn2.zag          fixture S3 = tnn2_frozen_ref.zag, untouched
  cfprobe/cf_full.zag  the corefreeze 6-file concatenation
  cfprobe/cf_perm.zag  same files, permuted concatenation (Q2)
  cfprobe/cf_nl.zag    same files + one trailing newline (Q2b)
  bt_matrix.sh         one arm x one source x N builds x 3 runs
  bt_run_all.sh        the whole 6-arm matrix + probes P1-P8
  cf_probe.sh          the plan-order probe Q1-Q4
  driver.log           full wave output (162 builds)
  cfprobe.log          plan-order probe output
  SUMMARY.txt          one summary line per (arm, source, probe)
  build_ledger.txt     all 90 matrix builds: arm, source, binary sha256
  builds_sha256.txt    sha256 of all 18 per-cell builds.tsv result tables
  sample_builds.tsv    one cell's per-build table (build, bytes, bin sha, out sha)
```

**One known cosmetic defect in the artifacts, flagged so nobody misreads them.**
`cfprobe.log` line `Q1_RESULT ... distinct_bin_shas=5` is a bug in the
*reporting* line of `cf_probe.sh` at the time it was run (it counted loop
iterations, not distinct hashes). The five per-build `bin_sha=` lines directly
above it are all `8599500d13aab0c5`, and the real distinct count is **1**.
`cf_probe.sh` has been fixed to compute `DISTINCT_BIN_SHA` properly; the fix
changes only that echoed number, no measurement.

Run order: `bt_run_all.sh` (≈20 min, serial), then `cf_probe.sh` (≈2 min).
Both source `.env/pure-zag.sh`, call only `znc`, and put **every** binary
execution through `tnnwatch.sh reg`.