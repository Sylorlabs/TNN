# PREREG — BUILD-TO-BUILD DETERMINISM (BUILD-STABILITY lane)

Claim IDs: **C530–C539**.
Frozen before the matrix runs. Expectations below are predictions, not results.

## 0. Threat being tested

Brief §4.1 claims the canonical corpus reproduces byte-identically on this host
and CLOSES blocker B13. `lane/corefreeze` (commits 2ceaa1748, 82bfa0ae1)
reports: "plan order differed across rebuilds of logically identical source;
run-to-run is 3/3 byte-identical, BUILD-TO-BUILD is unverified and would qualify
brief §4.1/B13."

If builds from identical source are not byte-stable, §4.1 may be a one-off and
B13 is not closed.

## 1. Hypotheses

* **H-STABLE (prereg prediction).** `znc --target macos-arm64` is a
  self-contained, single-invocation code generator. Its only mutable state is
  `.zag-cache/` (foreground machine cache) and `zagd` snapshots
  (`.zag-cache/zagd/semantic.record`, `profile-plan.record`). Given the same
  source bytes, the same flags and the same target, the emitted Mach-O is
  byte-identical across arbitrarily many builds, under every condition we can
  vary (output path, cwd, PATH, flags, cache state, timestamp, fresh shell).
* **H-UNSTABLE (the corefreeze observation).** Plan order in some program
  varies build-to-build from identical source.

## 2. Kill bars / decision rules (frozen)

* **BUILD-STABLE is established for a source iff** N >= 5 builds from a clean
  state (output binary `rm -f`'d before each build) yield exactly 1 distinct
  binary sha256, **and** each binary's 3/3 runs are byte-identical.
* **Any** single build that yields a different binary sha256, or any run-to-run
  output difference, is a **BUILD-INSTABILITY** finding and qualifies §4.1.
* **Any** condition arm that is UNSTABLE while the baseline arm is STABLE
  attributes the instability to that condition.
* If the baseline arm is STABLE in every arm, the corefreeze observation is
  **not** general build instability and must be attributed to something else
  (source state, flag set, stale artifact, or a source-level defect such as
  B17 `[]u8 as *u8`, or the B16 get32/set32 byte-offset trap).

## 3. Fixtures (frozen shas)

| id | source | bytes | lines | sha256 |
|---|---|---|---|---|
| S1 | `bt_small.zag` (written by this lane) | 1779 | 54 | `2936623db888328103cfe567a8033b9f533808546290872d236d9e44eb93b686` |
| S2 | `cogops_learnosc2/c8_full.zag` + `_zag_print` shim | 75171 | 2468 | `e33420b9debf5c91e6d435e30aa8e2485ca02623fac50664988d699144996a90` |
| S3 | `compression_exec/tnn2_frozen_ref.zag` (already `_zag_print`) | 56508 | 1591 | `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd` |

Reference output: `cogops_learnosc2/c8_run1.txt`,
sha256 `ae0ae3bf0a82c31b6d53d14dba97e6abfb953273259d624f4869c48fb15e4ae7`, 3344 bytes.

S2 is derived from the checked-in `c8_full.zag`
(sha `ce401e34dae6c9abf9406954e8a516e82fb3d2fc5b17d2899a969f0ac4060421`)
by **exactly one** line substitution:

```
-  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0);
+  _zag_print(b[0..c]);
```

## 4. Matrix — 6 arms x 3 sources, N=5 builds each (90 builds total)

Common: `$ZNC --target macos-arm64` plus the arm's flag set. Output binary
`rm -f`'d before every build. Each built binary run 3x under `tnnwatch.sh reg`
(300 s limit).

| arm | description | flags beyond `--target macos-arm64` | cwd | output path | PATH | cache |
|---|---|---|---|---|---|---|
| A0 | baseline, brief/zbuild.sh flags | `--no-zagd --no-analyze --no-foreground-cache` | lane dir | lane dir | pure-zag shim PATH | purged each build |
| A1 | baseline, cache warm (no purge) | same | lane dir | lane dir | pure-zag shim PATH | warm |
| A2 | minimal flags | *(none)* | lane dir | lane dir | pure-zag shim PATH | purged each build |
| A3 | baseline flags | same | `/tmp` | `/tmp/bt_out` | pure-zag shim PATH | purged each build |
| A4 | baseline flags | same | lane dir | lane dir | **host PATH (no shim)** | purged each build |
| A5 | baseline flags + fresh shell per build (`env -i`) | same | lane dir | lane dir | pure-zag shim PATH | purged each build |

Additional non-matrix probes (each N=5 where noted):

* **P1** touch source mtime to a different value, rebuild N=5.
* **P2** zagd: verify `--no-zagd` is genuinely effective (does znc read
  `.zagd.*`? does it spawn a daemon?). Build with and WITHOUT `--no-zagd`, N=5.
* **P3** `--no-analyze` vs analyzer on, N=5 each.
* **P4** `--no-foreground-cache` present vs absent (warm cache), N=5 each.
* **P5** `-o` output name/location varied across 5 *distinct* paths.
* **P6** `znc clean-cache` between builds.
* **P7** rebuild in a different ORDER (S3, S1, S2, ...) to test for
  order-dependence / cross-contamination.

## 5. Excluded / bounded

* Concurrency: builds are run **serially**. The host is shared (load ~7/10) and
  parallel builds would confound wall-clock with determinism. This does NOT
  test concurrent-build determinism — that is explicitly out of scope.
* Only `--target macos-arm64` is tested. Linux x86-64, wasm and GPU targets are
  out of scope.
* The pinned `znc` binary sha is recorded; a *different* znc build is out of
  scope.

## 6. Self-correction note

§4.1 of the brief describes `c8_full.zag` as "340948 bytes of text". The source
file is 75215 bytes / 2468 lines. 340948 is the size `znc` reports for the
emitted Mach-O **__text segment**. This is a wording defect in §4.1 and will be
corrected in the report; it does not affect the reproduction itself.