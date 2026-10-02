Native source projection for the pinned stable compiler

The unchanged ORIGINAL V68 and V73 roots pass through this native Zag projection and the SAME stable compiler. Direct unchanged V68 still fails 7 checks; direct V73 reports 81. Direct and projected V71 pass with identical stdout. This closes projected-source qualification, not the stable compiler's direct-source defect.

The stable compiler SHA-256 is 3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956. No compiler binary, original source, test checks, wire contract or canonical R27 file was changed. Scientific exposure and learner authority remain zero.

Run from the TNN workspace:

```sh
/Users/Shared/micah/Documents/zag/znc Research/R33_CONTINUING_LIFE_V1/NATIVE_SOURCE_PROJECTION_20260915/project.zag --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o /tmp/r33_finish_recovery_20260915_b/compiler_probe/project
perl Research/R33_CONTINUING_LIFE_V1/NATIVE_SOURCE_PROJECTION_20260915/qualify.pl
```

The first command bootstraps the native projector. The second records compiler/original SHA invariants, exact argv and exits, native hashes checked independently with Perl Digest::SHA, qualification stdout/stderr, fixture commands, and the byte-preservation review in `/tmp/r33_finish_recovery_20260915_b/compiler_probe/qualification.json`. Perl orchestrates and independently reviews; all source projection and production provenance hashing execute in the native Zag binary. No Python is used. `review.pl` can also be run independently against the recorded projections. `qualify.sh` is a simple reproduction of the three direct/projected runs; prefer `qualify.pl` for the complete machine record.

For one root (use fresh output paths):

```sh
/tmp/r33_finish_recovery_20260915_b/compiler_probe/project /Users/Shared/micah/Documents/TNN/TNN/Research/R33_CONTINUING_LIFE_V1/outer_learner_packet_bridge_v68_tests.zag /tmp/r33_finish_recovery_20260915_b/compiler_probe/example.zag /tmp/r33_finish_recovery_20260915_b/compiler_probe/example.tsv
/Users/Shared/micah/Documents/zag/znc /tmp/r33_finish_recovery_20260915_b/compiler_probe/example.zag --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o /tmp/r33_finish_recovery_20260915_b/compiler_probe/example
/tmp/r33_finish_recovery_20260915_b/compiler_probe/example
```

The projector recursively visits actual flat local-file import directives outside strings/character literals/comments, emits each lexically normalized dependency once before its caller, and copies all other source bytes verbatim. It inserts exactly one newline per emitted file to prevent token or end-of-line-comment fusion. Import offsets in TSV are zero-based half-open byte spans in the ORIGINAL input. Native FILE, TOOL_SHA256 and OUTPUT_SHA256 records bind the closure, projector and generated source. No literal substitution or rewriting of const uses occurs. Dependency-before-caller ordering makes the stable parser register the original const declarations before parsing their original uses.

The native parser source explains the failure: `selfhost/parse.zag` registers const names in each Parser's separate `consts` list, desugars const declarations to nullary functions, and auto-calls recognized bare names. An imported caller does not inherit that parser-local list. The newer tree marks `_zag_desugared_const`; this is not evidence that the pinned older binary contains that repair. No direct const/import compile option was identified. Adding another importing wrapper leaves the original caller in its separate parser and does not supply the required recognition.

Scope is the exact qualified six-file local closure for each original root (eight distinct original files across V68/V73/V71). The independently reviewed closure is byte-identical to the pinned 20260915T174458Z frozen sources. V68 retains all 12 checks, including tamper refusal, restored validity, oversize refusal, parent pending, exact learner bytes and world/ingress roundtrips; V68 and V73 produce 245924 bytes. V71 retains all original call-shape checks.

The tool refuses cycles, missing files, malformed or comma-alias imports, `as` aliases, package/colon or escaped import paths, nested imports, `#` resource directives including #embed, top-level non-import annotations including resource declarations, script/module/package/edition directives, unbalanced braces and unterminated quotes/comments. Bounds are 128 files, recursion depth 64, 2 MiB per source and 8 MiB emitted output. Block-comment ignoring is tested at projection level only; the pinned compiler does not parse block comments. No generalized module-namespace, private/export, duplicate declaration, shadowed const, resource/annotation or Script semantic equivalence is claimed. Such inputs require separate qualification.

Inputs and parent directories must be trusted unchanged regular local files with no symlink aliases; path identity is lexical dot/dotdot normalization, not realpath or inode identity. Outputs use Darwin O_CREAT|O_EXCL with mode 0600: existing leaf files and leaf symlinks are never overwritten, including dangling symlinks. Source-path and closure-path output collisions are also refused. Trusted output parent directories are required. This is not an atomic two-file publication protocol: an I/O failure while writing source/provenance can leave a newly created partial artifact; callers must require exit 0 and validate hashes before compiling. Qualification exercises existing-file and output-leaf-symlink refusal on local fixtures.

Review results and commands are in the probe directory; the concise closeout is `/tmp/r33_finish_recovery_20260915_b/compiler_final.txt`.
