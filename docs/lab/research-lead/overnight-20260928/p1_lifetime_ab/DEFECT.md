# TOOLCHAIN DEFECTS FOUND BY LIFETIME-AB-1 (new blockers, B15-B17)

Host toolchain per `docs/ops/TOOLCHAIN.md` section 1:
`/Users/Shared/micah/Documents/TNN/.bin/znc`,
sha256 `3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956`,
version string `znc 2026.07.0-dev (edition 2026)`, target `macos-arm64`.
The brief's section 7 recommends running
`/Users/Shared/micah/Documents/TNN/TNN/tools/zbuild.sh X.zag --rep 3`; all
commands below were run through it, so the `--target macos-arm64` flags
were injected and the ELF failure mode of TOOLCHAIN 1.1 did not occur.

These three defects were not on the known-blocker list (B1-B14) and each
blocks the experiment.

---

## B15. `_zag_raw_syscall(1, fd, buf, len)` is inert: the frozen `o_flush` writes nothing

Every existing lane flushes its dynamic output with

```zag
fn o_flush(b:[]u8,c:i32)void {
  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0);
  return;
}
```

Probe (`probe_defect.zag` harness, fd 1 and fd 2 both tested): the call
returns without writing a single byte to either descriptor. `_zag_slice_ptr`
is fine (the pointer value is correct); the syscall itself does nothing on
this target. `_zag_write_file` works. `_zag_print` on a filled slice works
and is what this lane uses instead.

Consequence for the whole program: any lane whose ONLY output path is
`o_flush` produces an empty stdout on this host while exiting rc=0. A lane
that reports "build PASS" and an empty log is indistinguishable from a lane
that ran correctly. The brief asserts `o_flush` was verified working on
this host; that assertion is wrong.

Workaround used here: keep the mandatory single-preallocated-buffer
discipline and the cursor-returning helpers, and emit the finished buffer in
exactly one call via `_zag_print(b[0..c])` (`lt_flush` in `lt_world.zag`).

## B16. Indexed reads are miscompiled once `c15_base.zag` is in the unit

Minimal reproducer, no lane code involved:

* `probe_defect.zag` (self-contained, 78 lines) -- PASSES.
  All four read forms return `11 105 50 11 106 60`.
* `probe_defect_with_base.zag` = the frozen, unmodified
  `cogops_rescueaware/c15_base.zag` (174 lines) concatenated with the same
  40-line probe body -- FAILS.

Same source lines, same bytes written, different reads:

| read form | result |
|---|---|
| `get32(C, 4 + j)` coefficient-1 induction variable | `11 1761607680 6881280 26880 105 838860800` WRONG |
| `get32(C, 4 + j*4)` | `11 105 50 11 106 60` CORRECT |
| `get32(C, 4 + m*12)` | CORRECT |
| `get32(C, 4)` literal | CORRECT |

The wrong values are the correct bytes read at a displaced offset, so this
is silent data corruption, not a crash. Both variants are 3/3
byte-identical across runs, so `--rep 3` determinism does NOT detect it:
the corruption is perfectly deterministic.

This is the same family as the recorded B6 note ("interpreter scratch
overflow at program length 7") and it invalidates every lane on this host
whose learner state is a flat `[]u8` addressed as `base + i`.

Observed consequence in this lane: the learner's own relation-coverage
sets print as garbage, and `get32(L,0)` returns different values in two
different functions of the same binary (`emit_stage` reported
`retcov=5/8/10/14/16`; `emit_cov` reported `0/3/13/16` for the same cells).
Two readers of one cell disagreeing inside one binary makes every derived
statistic uncertifiable.

Mitigation applied in this lane (necessary but NOT sufficient): every
indexed access uses an explicit multiplier (`k*4`, `i*12`, `b+24+i*8`), and
the lane-local chain writer inlines its byte stores instead of calling the
frozen `chain_add`. Even so, `emit_cov` still returned the wrong count for
`get32(L,0)`, so the mitigation does not close the hole.

## B17. Bogus type errors on large translation units

`lt1_full.zag` at 3850 lines produced

```
znc: error[E0202]: unknown type ':' in function __clos_cap_1
znc: error[E0010]: unexpected token at top level: `return`
```

and, in an intermediate state, 130 `E0203` argument-type errors naming
parameters that are correctly typed in the source. Control-flow skeletons
generated for the program (`__clos_cap_*`) are reported as having a type
error, which is a compiler-internal artifact, not a source defect. The
same source compiled once the malformed generated region was removed.

Note this interacts with B13: canonical lanes through C410 were built with a
Linux x86-64 compiler, so there is no evidence on this host that any
multi-thousand-line translation unit has ever been built correctly here.

---

## Also found (not blocking)

* `tools/zbuild.sh X.zag` with a bare filename never runs the binary:
  `BIN="${SRC%.zag}"` is a bare name and the restricted PATH injected by
  `.env/pure-zag.sh` does not contain `.`, so the shell reports
  `fwd: command not found` / rc=127 while the compile succeeded. Passing a
  path containing a slash (`./X.zag`) works. The brief's own invocation
  form has this bug.
* Zag resolves forward references: a `fn` may be called before it is
  defined, so concatenation order is not constrained the way the brief
  states. Verified directly.
* `-> i32` return-type syntax is rejected; use `)i32 {`.