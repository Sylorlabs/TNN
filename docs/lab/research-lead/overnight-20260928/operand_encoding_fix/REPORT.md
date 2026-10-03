# REPORT.md -- Operand-encoding fix implementation (W-IMPL)

Lane: `docs/lab/research-lead/overnight-20260928/operand_encoding_fix/`
Prereg: 447f087af (frozen before this work; strict commit-order self-check:
the prereg commit strictly precedes this implementation commit).
Branch: tnn-native-lab. Local only, never pushed.

## Step 0: Toolchain guard

Executed before any other work:
```
export PATH="$HOME/safebin"
which python3   -> (empty, nothing)
which python    -> (empty, nothing)
guard-check-done
```
Result: PASS. Both `which` commands returned nothing; PATH was
`/home/hatch/safebin` only for every command in this session. All work
pure Zag; shell used only for znc invocation, binary execution, git ops,
file movement. No forbidden-executable invocation occurred.

## Implementation

1. `oe_base.zag`: copied verbatim from
   `../scaling_5000_fixed/s6_base.zag` (1495 lines, identical copy
   confirmed by wc), then applied EXACTLY the 8 frozen changes from
   PREREG.md (t2_sig, tag 102, t_c6 fossil all left as-is per design).
2. `oe_driver.zag`: verbatim copy of `../scaling_5000_fixed/s6_driver.zag`
   (183 lines; audit confirmed it contains no operand code).
3. `oe_full.zag` = oe_base.zag + s6_patch.zag (verbatim, unmodified) +
   oe_driver.zag. Concatenation verified with cmp: byte-exact.

## Diff summary (oe_base.zag vs s6_base.zag)

`diff -u` shows ONLY these hunks; nothing else changed:

- H1 header comment: records the new base revision (sign-tagged operand
  invariant), prereg commit 447f087af, and that SCALING-5000-FIXED FAIL
  remains canonical for the old build.
- H2 `res_op` rewritten (D1): `op<0 -> fr_get(W,f,-1-op)`;
  `op>=65536 -> -999999`; else `ng(W,op,20)`.
- H3 execute tag 101 (D2): `if(d>=0){return -999999;}` then
  `fr_set(W,fr,-1-d,res_op(W,fr,sr));`
- H4 execute tag 103 (D4): `if(s>=0){return -999999;}` then
  `fr_set(W,fr,-1-s,fr_get(W,fr,-1-s)+1);`
- H5 execute tag 104 (D5): same shape with -1.
- H6 stale comment at old line 313 ("1000+slot") rewritten to describe
  the sign encoding (slot s encodes as -1-s).
- H7 encoders: `10000+slot` -> `-1-slot` in t2_guard (field4), t2_set
  (field4), t2_mov (field4 AND field8: `-1-dst`, `-1-src`), t2_inc
  (field4).
- Confirmed ABSENT from diff (as frozen): execute tag 102, t2_sig,
  t_c6 fossil, and every other line of the 1504-line file.

Any unexpected hunk would have been a defect; there were none.

## K1 self-check: PASS

`grep -n '10000' oe_base.zag` returns exactly the two known-unrelated
hits named in the prereg:
- line 264: `let bb:i32=1000000;` (large-number init; old line 257 + 7
  header lines)
- line 1306: `while(r_live_count(W)>cap && guard<10000){` (loop bound;
  old line 1297 + 7 header + 2 comment-rewrite lines)

Zero `op>=10000`, zero `10000+slot`, zero `10000+dst/src` operand
patterns remain anywhere in oe_base.zag.

## Compilation

- Flags matched to s6: `znc oe_full.zag -o oe_bin` using the safebin
  pinned znc (`/home/hatch/safebin/znc`).
- Exit 0. Full log: `oe_compile.log` (untracked, kept on disk).
- Output: `znc: wrote native binary oe_bin (279653 bytes main, 0
  external tools)`. 151 analyzer warnings, all A0102
  ignored-return-value, identical warning class/count to the s6 build
  (s6_compile.txt). No errors.

## Smoke test

`timeout 60 ./oe_bin` -> exit 124 (killed by timeout, as intended; the
full 5000-MAP experiment belongs to W-REG and was NOT run). Output head:
```
S6-START
S6D-START
```
The binary starts, emits its startup lines, and runs without an
immediate crash or panic. Log: `oe_smoke.log` (untracked, kept on disk).

## Files created (lane dir)

- `oe_base.zag` -- new base revision, committed
- `oe_driver.zag` -- verbatim driver copy, committed
- `oe_full.zag` -- concatenated build, committed
- `oe_bin` -- compiled native binary, KEPT ON DISK BUT UNTRACKED
  (repo convention: s6_bin was never committed; binaries stay out of git)
- `oe_compile.log` -- full znc output, kept on disk, untracked
- `oe_smoke.log` -- 60s smoke run output, kept on disk, untracked
- `REPORT.md` -- this file, committed

## Scaling_5000_fixed untouched

No file under `../scaling_5000_fixed/` was modified at any point.
Verified: only reads and `cp` (read) were performed against that dir.

## Ready for W-REG

oe_full.zag/oe_bin are ready for the K2/K3/K4/K5/K6 battery. Boundary
probes (K4) and the old-collision probe (node id 14121) remain to be run
by W-REG; nothing in this lane's scope asserts them.
