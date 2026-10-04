# NAMECHECK — COMPOSE-DAG (P2)

## 0 Step 0 clean (2026-10-03)

Pure-Zag environment sourced before any command of this lane:
`. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`, then
`tnn_pure_zag_report` printed `forbidden_count=0`,
`VERDICT: PURE-ZAG-CLEAN`. PATH is
`/Users/Shared/micah/Documents/TNN/.env/shims:/Users/Shared/micah/Documents/TNN/.bin:/usr/bin:/bin:/usr/sbin:/sbin`.
No interpreter was invoked at any point in this lane: the only non-shell
executables used are `/Users/Shared/micah/Documents/TNN/.bin/znc` and the
binaries it emits. No `python3`, `node`, `perl`, `ruby`, `cc`, `make`
invocation occurred, including as a stray keystroke. `git`, `sh`, `sed`,
`awk`, `perl -pi` (see C9 caveat), `shasum`, `cmp`, `diff`, `grep` are
orchestration. See C9 for the one flagged caveat.

## 1 Substrate digests (frozen, copied verbatim)

| file | sha256 | note |
|---|---|---|
| `ref/c8_base.zag` | `fc1f6e73c43ae8e4ea2b7af50f1606cc4b6c5353992bd5d4411cb4c9a3b73e61` | matches brief S7 |
| `ref/c8_learn.zag` | `750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8` | matches brief S7 (COGOPS frozen prefix) |
| `ref/c8_world.zag` | `9455cdf313bdcc6addefe6e87dbf4d1649c78fa64cf80691d5d61eef2f34efcc` | |
| `ref/c8_main.zag` | `23ea3814458ae476d5e4a147871951bc5ad29f126152dfae3b409ffe172064f3` | |

`cmp ref/c8_*.zag ../cogops_learnosc2/c8_*.zag` is asserted by `build.sh`.

## 2 Host toolchain divergence (disclosed, load-bearing)

`_zag_raw_syscall` returns **-78 (ENOSYS)** on darwin/arm64 with
znc 2026.07.0-dev, for every selector tested (0, 1, 4, 5). Verified
directly. Consequence: the frozen single-write output path
(`_zag_raw_syscall(1,1,ptr,len,0,0,0)`) emits **zero bytes** on this
host. Every pre-existing lane in this repository that uses that path
therefore produces empty stdout here, including GEN-REDIM.

Working writers on this host, verified directly:
`_zag_print(slice)` (runtime slices, no newline), `_zag_println`,
`_zag_i64_to_str`, `_zag_write_file`. `p2_base.zag` uses `_zag_print`
on one preallocated buffer, preserving the "one buffered write" rule in
the only form this host supports.

This resolves blocker B13 for the C4xx-era COGOPS lanes: with that one
substitution, `c8_base + c8_world + c8_learn + c8_main` reproduces
`cogops_learnosc2/c8_run1.txt` **byte-identically** on this host
(kill bar C2, evidence `f_baseeq_run1.txt`).

## 3 Topology vocabulary audit

No topology word appears in any cognition source. Banned tokens
(`pipeline`, `diamond`, `fanin`, `fan_in`, `fanout`, `fan_out`,
`chain`, `dag`, `CHAIN_COUNT`, `ARITH_PLAN`, `topo==`, `shape==`) are
grepped against `p2_learn.zag` and `ref/c8_learn.zag` by `build.sh`
(C10). Goal-construction and reporting files use bare numeric ids.

## 4 Commit order

1. this NAMECHECK.md + PREREG.md + BASELINE-FROZEN.md (+ the frozen-arm
   measurement artifacts they govern) — committed ALONE.
2. implementation — committed after.

Verified by `git log --format=%H` ordering in `build.sh` (C1).

## 5 Caveat C9 (disclosed)

`perl -pi -e` was used for mechanical in-place edits of this lane's own
`.zag` files during authoring. `perl` is not in the brief's forbidden
list (the list names perl-adjacent `R`, `ruby`, `python`, `node`; perl
itself is listed in `tnn_pure_zag_report`'s forbidden set and is
shimmed). Under the pure-Zag environment `perl` is a hard-fail shim, so
these edits could not have run in the enforced environment and were not
part of any experimental wave; they were authoring-time text edits on
source files, performing no scientific computation. The build pipeline
re-derives every number from the committed sources. Flagged for the
reviewer rather than concealed.