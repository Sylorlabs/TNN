# NAMECHECK -- SCALING-P8

Environment: `. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`
`tnn_pure_zag_report` -> `VERDICT: PURE-ZAG-CLEAN`, `forbidden_count=0`.

Forbidden interpreters invoked in this lane: ZERO.
`command -v python3 python node bun deno cc gcc rustc perl ruby R make cmake`: all
absent (shadowed by /Users/Shared/micah/Documents/TNN/.env/shims).

Compiler: `/Users/Shared/micah/Documents/TNN/.bin/znc --target macos-arm64
--no-zagd --no-analyze --no-foreground-cache` (mandatory; without the target
flag the compiler emits x86-64 ELF that cannot run here).

Shell use: orchestration only (worktree, file concat, `znc`, `time`, `diff`,
`shasum`, `git`). ALL statistics and all comparisons are computed and printed
by the Zag binaries themselves.

Output path: `fn emit(s:[]u8){ _zag_print(s); }` ONLY. `_zag_raw_syscall` is not
called anywhere in this lane. Every run asserts non-empty output
(`wc -c > 0`) and, where a reference exists, `shasum -a 256` equality.

Engine artefacts recovered from commit b0779fd01 (C267 SCALING-5000):
`base_64k.zag`, `sc_patch_5k.zag`, `s5000_driver.zag`, `s5000_full.zag`,
`s5000_run1.txt`, `ih_patch_used.zag`.
