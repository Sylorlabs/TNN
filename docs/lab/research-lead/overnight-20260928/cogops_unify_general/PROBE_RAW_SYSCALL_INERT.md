# PROBE: `_zag_raw_syscall` is inert on this host (toolchain finding)

**Date:** 2026-10-03. **Claim id:** C501 (infrastructure).

## Finding

On this host the pinned compiler
`/Users/Shared/micah/Documents/TNN/.bin/znc` built with
`--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache`
(the exact invocation `tools/zbuild.sh` uses) accepts
`_zag_raw_syscall(...)` and **returns a negative value while emitting zero
bytes**.

## Minimal reproduction (pure Zag, 12 lines)

```zag
fn main()i32 {
  let B:[]u8=z_alloc(64);
  B[0]=72; B[1]=73; B[3]=10;          // "HI\n"
  let p:i64=_zag_slice_ptr(B) as i64;
  _zag_println("PRE");                // PRE appears
  let r:i64=_zag_raw_syscall(1,1,p,4 as i64,0,0,0);
  _zag_println("POST");               // POST appears
  if(r<0){ _zag_println("NEG"); }     // NEG appears
  return 0;
}
```

Observed:

```
PRE
POST
NEG
```

No `HI` is written. Variants tried and equally inert: `nr=4`,
`(1,1,1,ptr,len,0,0)` 7-argument form, and every buffer size from 128 to
65536. `_zag_println` and `_zag_write_file` both work normally.

## Consequence

The house output idiom of **every** COGOPS lane —

```zag
fn o_flush(b:[]u8,c:i32)void {
  _zag_raw_syscall(1,1,(_zag_slice_ptr(b) as i64),c as i64,0,0,0);
  return;
}
```

— writes nothing here. A binary that "runs rc=0" can be completely silent.
This is a silent-success failure mode: `zbuild.sh` reports success.

## Adaptation used by this lane

`ref/base.zag` (this lane's own copy of `c15_base.zag`) replaces the body of
`o_flush` with a `_zag_write_file` of the same `c` bytes to a fixed path.
This is a **sink substitution only**: no arithmetic, no control flow, no
learner state, no observation. Provenance of the adaptation is checked by the
byte-identity result in `RECON.md` §4: with the substitution, the macOS/arm64
rebuild of the c15 additive reproduces the checked-in Linux-produced
`cogops_rescueaware/c15_run1.txt` **byte for byte** (256 lines, sha match).

## Blast radius / governance note

`docs/ops/ZAG_LANGUAGE_AND_WORKER_BRIEF.md` §4(b) presents the
`_zag_raw_syscall` write as "verified working on this host". **That
verification does not reproduce.** The brief's own §4(a) already records one
builtin claim that turned out to be wrong ("an internal recon pass asserted
this builtin does not exist. That assertion is WRONG"). This is the opposite
error: a builtin that is *accepted and returns a value* while doing nothing.
Recommend the brief be amended and that `zbuild.sh` gain a non-empty-stdout
assertion, since a silent binary currently passes the determinism harness
trivially (all N runs are identically empty).
