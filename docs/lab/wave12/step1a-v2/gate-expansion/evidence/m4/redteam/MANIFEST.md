# MANIFEST.md — M4 red-team freeze (replacement crew)

Frozen: 2026-09-25. Method: M4 determinism-by-construction subset compiler.
Checker binary: `../m4_subset`, SHA-256
`62b9728a141eb6da1132dd27067e0d6133df5a76246bb5adbd8bddfbbc45be73`
(matches the pinned SHA). Checker self-reports `DIALECT M4-2026-09-25-v1`.
Toolchain for validity proofs: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned znc).

Blindness observed: checker used strictly black-box (`m4_subset <module> <configdir>`);
`M4_VERDICT.md`, `certs/`, `config/` contents, and `m4_subset.zag` (checker source)
were never read. Pinned substrate files (`m4_prelude.zag`, `R33_NATIVE_IO_V1.zag`)
were used only as documented build/import targets (API signatures) — not as
checker internals.

**Freeze verdict (black-box probes by this crew, for the method crew to reproduce):
all 12 plants return `VERDICT CERTIFY` from the frozen checker.** Under the frozen
miss definition (CERTIFY on a valid dirty plant), all 12 are kills.

## Resume note (replacement crew)

Inherited 12 `rt_*.zag` drafts + `bin/` binaries, no manifest. Every draft was
re-validated from scratch: compiled with pinned znc, run ≥2× for variance (or
static proof), and probed against the checker binary.

- **Kept as-is (11):** rt_a1_clock, rt_a2_exec, rt_a3_freelist, rt_b1_malloc_seed,
  rt_b2_fnret, rt_b3_array, rt_c1_readfile, rt_c2_d5alias, rt_d1_newline_as,
  rt_d2_hashorder, rt_d3_argc. Each compiled clean, demonstrated genuine
  nondeterminism (details per plant below), and CERTIFies.
- **Replaced (1):** rt_c3_stdin.zag was broken as drafted — `nio_read_exact` in the
  pinned substrate rejects non-regular fds (`nio_regular(fd)!=1` → -7401), so fd 0
  never yields bytes; both runs printed `-7401` + zeros (no variance, no read).
  Replaced with rt_c3_mkdir.zag (new mechanism, validated below).
- **Probed and discarded (not frozen):** an intermediate variant building the
  banned path at runtime with zero string literals was REFUSEd by the checker
  (`HIT D5-pinned-paths ... non-literal or unparsable path argument`) — D5 is
  fail-closed on non-literal paths, so it is not a kill. Also probed: transitive
  @import closure (D8 catches a dirty file two levels deep — solid), absolute-path
  @import (checker ERRORs — fail-closed, not a miss), and 6 allowlist-path guesses
  (all REFUSEd; the 4 allowlisted paths were not enumerated — not needed).
- `bin/` still holds the previous worker's binaries (stale build artifacts, not
  part of this freeze); `bin/rt_c3_stdin` was removed with its source.

## Plant table

| # | file | category | SHA-256 | targets | validity proof |
|---|------|----------|---------|---------|----------------|
| 1 | rt_a1_clock.zag | (a) token/rule evasion | d2c8bd9934989fc6acd48813810b6e7c36a9570a53f776919ad0e05b681c6859 | D6 | Calls `_zag_clock_monotonic_ms()`. The banned word `clock` is embedded mid-identifier, joined by underscores on both sides; D6's word-boundary match treats `_` as a word char, so it never fires — yet a genuine monotonic ms clock is returned. Runs: `8652165`, `8652169`, `8652175` — varies. |
| 2 | rt_a2_exec.zag | (a) token/rule evasion | 776023479e5f085d60cbf357860707170cf5a405b47045da29f9f3c20b483b7d | D1–D6 (gap) | `_zag_exec_capture("date +%s%N")` — no rule covers process execution (not the D1 raw-syscall token, no D6 word, no path, no _zag_arg/nio_alloc/hash token). Runs print distinct nanosecond timestamps (`...121794934`, `...127485888`, `...152347483`). |
| 3 | rt_a3_freelist.zag | (a) token/rule evasion | 1b577cc171236ef1a53956a511377133f32fa376f1c72a6d625f17111f49e489 | D3, D7 | D3 bans only the token `nio_alloc`; `_zag_malloc`/`_zag_free` are unlisted. D7 seeds taint on `&x`, `_zag_arg(...)`, `z_alloc_init` returns — NOT on `_zag_malloc` — and no cast of a tainted expr occurs: the plant reads BYTES (u8 values) from a malloc/free/malloc-reused chunk, i.e. allocator freed-chunk metadata holding ASLR heap addresses. Runs: `608020884043857920`, `626176987785723904`, `612598767680946176` — varies. |
| 4 | rt_b1_malloc_seed.zag | (b) taint/alias confusion | 926834183a32671b380218df3d134213ecef2e8ed5282792b1b69512b936e83b | D7 | D7's taint-seed set omits `_zag_malloc` returns, so `p` is untainted in the checker's eyes and `p as i64` is not flagged — yet it leaks an ASLR heap address. Runs: `130973502504968`, `132542816247816`, `131453323538440` — varies. |
| 5 | rt_b2_fnret.zag | (b) taint/alias confusion | c62b292f0b2dd8d595e98293d35d8e1a0e0b1b1fda674a6c8f464c6e588abeee | D7 | Taint is intra-procedural: `&x` taints inside `main`, but taint does not follow the pointer through the `leak` function's parameter/return, so `p as i64` inside `leak` is not flagged — yet it leaks an ASLR stack address. Runs: `140730588716592`, `140723212919536`, `140735656273232` — varies. |
| 6 | rt_b3_array.zag | (b) taint/alias confusion | cc8c8826546cb9e15414b917700a0223f6f5e2156bf3976f8d38a88c6b2bb47c | D7 | Taint is tracked through locals/struct fields/pointer arithmetic but NOT through array element stores/loads: stashing tainted `&x` in `arr[0]` launders it; `arr[0] as i64` is not flagged — yet it leaks an ASLR stack address. Runs: `140731736590760`, `140724737469368`, `140731958171432` — varies. |
| 7 | rt_c1_readfile.zag | (c) allowlist/substrate abuse | 51ace4b551df2fce86eb7586d55d0adb0d46aefb42b55a407e30860da3ad8961 | D5 | D5's allowlist is enforced only on `dialect_read`/`nio_open_root`/`nio_open_child`. The native `_zag_read_file` intrinsic is not hooked — any path reads. Plant reads `/proc/sys/kernel/random/uuid`, regenerated by the kernel on every read. Runs print distinct UUIDs (`e03c3c51-…`, `d517ba4b-…`). |
| 8 | rt_c2_d5alias.zag | (c) allowlist/substrate abuse | 936fc4a1b6d6de89beebaf5256827a700a6698ddc0c667de5f544b4b8868077d | D5 | D5's hook matches the call NAME `dialect_read` syntactically and does not resolve `let` aliases (unlike D7's taint analysis, which does). `let dr = dialect_read; dr("/etc/machine-id", out)` bypasses the hook; the pinned prelude's real `dialect_read` then reads the banned path. CONTROLLED PAIR: direct `dialect_read("/etc/machine-id",…)` → `HIT D5-pinned-paths … VERDICT REFUSE`; via alias → `VERDICT CERTIFY`. Static proof: compiling+running prints `/etc/machine-id` (`ca2c3f3a0f2e41438f9f02dbcf3320f1`), a path D5 forbids. |
| 9 | rt_c3_mkdir.zag | (c) allowlist/substrate abuse | 532fa0a747fab6677d105513160a2d5a56501b6567d179b0fb0945989cb5f583 | D5 | D5's hook list omits `nio_mkdir` (pinned substrate, takes an arbitrary path). The module mutates the ambient filesystem outside the 4-path allowlist and CERTIFies. Runs: first prints `0` (created), second prints `-17` (EEXIST) — genuine run-to-run variance from ambient fs state, which the construction model does not capture (rmdir `/tmp/rt_c3_mkdir_probe` to reset). Static proof in addition: source indisputably performs a fs mutation through a path-taking call D5 never inspects. |
| 10 | rt_d1_newline_as.zag | (d) checker-logic attack | 2d247497df08c8d144525a2be61c9baeaa6878ddc33f95bef6aaf8b02dbb2edf | D7 | The D7 cast detector is line-oriented: it matches `EXPR as TYPE` only when `as` sits on the same source line. A newline before `as` (parsed identically by znc) defeats it, leaking an ASLR stack address. CONTROLLED PAIR: `let v:i64 = p as i64;` (same line) → `HIT D7-no-addr-cast … VERDICT REFUSE`; newline-before-`as` → `VERDICT CERTIFY`. Runs: `140724071697072`, `140721350311888`, `140729165036320` — varies. |
| 11 | rt_d2_hashorder.zag | (d) checker-logic attack | 3df782c0cf9f15945efeed5499da63d12b94f359cb92a1533818e36cf050840d | D4 | D4's hash-iteration ban is a token list (bucket/slotmap/hashmap/map_iter/bucket_iter). Innocent names (`slots`, `entries`, `insert_at`, `walk`) are unlisted, so a genuine chained hash table certifies. Bucket assignment comes from kernel-UUID bytes, so printed iteration order is nondeterministic: runs print `5 1 4 6 0 2 7 3`, `7 5 3 0 1 2 4 6`, `5 2 1 7 4 6 0 3`. |
| 12 | rt_d3_argc.zag | (d) checker-logic attack | d288ed690f175a6acccf2ac6bc623e45abd49408c6f53af564df88899a7338f7 | D2 | D2's logic matches the token `_zag_arg` (indices 1–4, bans 0 and env tokens) but not the distinct token `_zag_argc` — the argument COUNT — which leaks external input (how the binary was invoked). Runs: `./rt_d3_argc` → `1`; `./rt_d3_argc x y` → `3`. |

## Notes for the method crew

- All validity binaries were built with pinned znc in `redteam/` as cwd (the two
  @import plants resolve `../m4_prelude.zag` / `../R33_NATIVE_IO_V1.zag` relative
  to cwd — same layout the checker itself resolves, confirmed by its `FILE …
  PINNED` lines).
- rt_c3_mkdir.zag is stateful by design: it creates `/tmp/rt_c3_mkdir_probe`.
  Remove that directory between runs to reproduce the `0` → `-17` variance.
- Category labels are the red team's; every plant is a genuine dirty module
  (proven above) that the frozen checker CERTIFies black-box.
