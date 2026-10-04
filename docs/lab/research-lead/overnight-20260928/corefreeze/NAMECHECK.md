# NAMECHECK / TOOLCHAIN GUARD, corefreeze lane

Recorded BEFORE any implementation file exists.

## Step 0: forbidden-interpreter guard

```
$ . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
$ tnn_pure_zag_report
TNN PURE-ZAG ENVIRONMENT REPORT
  PATH=/Users/Shared/micah/Documents/TNN/.env/shims:/Users/Shared/micah/Documents/TNN/.bin:/usr/bin:/bin:/usr/sbin:/sbin
  ZNC_TARGET=macos-arm64
  ZAG COMPILER: /Users/Shared/micah/Documents/TNN/.bin/znc
  forbidden_count=0
  VERDICT: PURE-ZAG-CLEAN

$ which python3 python node
/Users/Shared/micah/Documents/TNN/.env/shims/python3
/Users/Shared/micah/Documents/TNN/.env/shims/python
/Users/Shared/micah/Documents/TNN/.env/shims/node
```

The three names resolve ONLY to hard-fail shims (exit 127) inside
`.env/shims`, which is the first PATH element. No Python, Node, Bun, Deno,
tsc, cc, gcc, rustc, julia, perl, ruby, R, make, or cmake is reachable.

Pinned compiler digest recorded at prereg time:

```
3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956  /Users/Shared/micah/Documents/TNN/.bin/znc
```

## Isolation

```
$ /Users/Shared/micah/Documents/TNN/TNN/tools/lane.sh new corefreeze
lane.sh: created lane/corefreeze at /Users/Shared/micah/Documents/TNN/.worktrees/corefreeze (base 87a822426)
$ git rev-parse --show-toplevel
/Users/Shared/micah/Documents/TNN/.worktrees/corefreeze
```

The worktree toplevel is the worktree, NOT the main repo. All git and all
file writes happen inside the worktree. No `git checkout`, no branch switch,
no `git commit -a`, no `git add -A`: explicit pathspecs only. Nothing is
pushed.

## Frozen-core digests at prereg time

```
750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8  cogops_learnosc2/c8_learn.zag   (1331 lines)
fc1f6e73c43ae8e4ea2b7af50f1606cc4b6c5353992bd5d4411cb4c9a3b73e61  cogops_rescueaware/c15_base.zag (174 lines)
4200e21fea5fa75d774f8f9785637d2305eccfa3d9b8486f27b7ac287b10b30d  hook_phase1/hq_module.zag        (326 lines)
```

`c8_learn.zag` matches the digest given in the mission brief exactly. The
other two match the brief's `fc1f6e73...` and `4200e21f...` prefixes; full
digests are recorded above and re-verified after the wave.

## Output-path discipline

`_zag_raw_syscall` is INERT on this host (brief section 4.0): it emits
nothing and returns rc=0. Every lane in this wave therefore flushes with

```zag
fn o_flush(b:[]u8,c:i32)void {
  _zag_print(b[0..c]);
  return;
}
```

and every run ASSERTS non-empty output containing at least one `BAR` line
(kill bar 0d). A silently empty log is a FAIL, not a pass. The single
substantive difference between `cf_base.zag` and the frozen `c15_base.zag` is
this one function body; it is diffed and reported, and it is NOT part of the
cognition source under test (`c8_learn.zag` never calls `o_flush`).

## Known-compiler hazards being respected

* `--target macos-arm64` is mandatory (omitting it emits a Linux ELF that
  reports compile success and then fails with `exec format error`).
* Exactly one `fn main(` per translation unit.
* No `for`; `while` only. No `!(A&&B)` inside `while`; De Morgan instead.
* `if` nesting kept at or below 3 by hoisting call results into `let`.
* Return type stated on every `fn`, including `void` functions, with an
  explicit `return;`.
* `[]u8 as *u8` is forbidden; `_zag_slice_ptr` is used where a pointer is
  genuinely needed.
* No claim of a compiler miscompilation will be made anywhere in this lane.
  The brief records a 1928-comparison arena sweep with 0 mismatches, and
  section 4.1 records a 340 KB flat-arena program reproducing byte-exactly on
  this host, so any anomaly found here is treated as MY defect until proven
  otherwise with a memory-free oracle.

## Dash hygiene

Zero em-dash (U+2014) and zero en-dash (U+2013) bytes in any lane file.
Verified by byte grep at the end of the wave (kill bar 0g).
