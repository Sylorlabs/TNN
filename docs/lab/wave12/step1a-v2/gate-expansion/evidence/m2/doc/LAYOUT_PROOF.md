# M2 §5.2 — Layout-equivalence proof (committed BEFORE battery runs)

**Date:** 2026-09-25. **Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).
**Proof binary:** `evidence/m2/build/proof/layout_proof`
**SHA-256:** `df9aad3bb72e8ace113c1cc4f77986413695262f6042e79579374181a818d2ca`
**Result:** `LAYOUT-PROOF PASS`, 2/2 runs, exit 0.

## Claim

The audit allocator (`src/m2_audit_alloc.zag`) is a TRUE drop-in for the
build's allocation primitive (`nio_alloc`/`nio_free`): same block header,
same alignment semantics, same deallocation path. The ONLY behavioral delta
is the fill value written into a freshly allocated block before hand-out
(production: `0x00`; audit: the active dirt pattern byte).

## Construction (source-level)

`m2_audit_alloc.zag` is the production `nio_alloc`/`nio_free` from
`R33_NATIVE_IO_V1.zag` with exactly one token changed in the fill loop:

```
// production                          // audit (D2 shown)
while(i<n){b[i]=0;i=i+1;}               while(i<n){b[i]=m2_pattern_byte(i as i64);i=i+1;}
```

Same `_zag_malloc(n)` call, same `n` bounds check (`1..33554432`), same
null path, same slice construction (`p[0..n]`), same `nio_free`
(bit-identical: `_zag_free(_zag_slice_ptr(b))`).

`src/m2_substrate.zag` is the production substrate with the `nio_alloc` /
`nio_free` definitions removed and `@import("m2_audit_alloc.zag")` added;
every other substrate function is byte-identical, so ALL allocations in a
target build (module + substrate-internal) resolve to the audit allocator.

## Empirical checks (all in `src/m2_layout_proof.zag`, D2=`0xAA` build)

For each n in {1,7,8,15,16,17,31,32,33,64,100,1000,4096,65536}, a fresh
mixed 4-alloc sequence `prod,audit,audit,prod` with NO frees during
measurement (the runtime recycles freed blocks out of bump order, so
frees would confound placement measurement; all frees happen once, at the
end):

| # | Check | Result |
|---|---|---|
| (a) | `.len == n` for all four blocks | PASS all 14 sizes |
| (b) | stride identity: the three adjacent strides s1,s2,s3 of the mixed sequence are equal (e.g. n=16 → 24,24,24) — placement does not depend on which wrapper called `_zag_malloc` | PASS all 14 sizes |
| (c) | audit fill == `0xAA` on every byte, pre-write | PASS all 14 sizes |
| (d) | production fill == `0x00` on every byte, pre-write | PASS all 14 sizes |
| (e) | post-overwrite identity: after explicit `0x5A` fill, prod and audit blocks compare byte-identical | PASS all 14 sizes |
| (f) | free-interchange: `prod_free(audit_block)` + `nio_free(prod_block)` succeed without fault | PASS (no crash, exit 0) |

Supporting probes (in `src/probe*.zag`, build logs retained):
- `probe10`: 6×`prod_alloc(16)` vs 6×`nio_alloc(16)` → identical stride
  signatures `24 48 48 48 48`, deterministic across runs.
- `probe9`: per-alloc live-byte delta identical (16 B each); allocation
  count identical; the imported `m2_pattern_byte` call itself allocates
  nothing.
- `probe1`: production `_zag_malloc` returns 8-mod-16 aligned blocks; the
  audit wrapper inherits this exactly (same call).

Two false alarms were caught and root-caused during proof development
(documented here, not hidden):
1. An early check compared 1st-of-pair vs 2nd-of-pair alignment and
   "failed" — root cause: the runtime bump allocator emits a per-block
   header, so mod-16 alignment is a function of allocation HISTORY
   (parity), not of the wrapper. Positional/stride checks replaced it.
2. A mid-development run showed non-uniform and negative strides —
   root cause: a probe bug (conditional reassignment allocated a prod
   block AND an audit block per iteration) and, separately, frees inside
   the measurement loop letting the free list recycle blocks out of bump
   order. Both fixed; final proof has neither artifact.

## Sole substrate deviation (2026-09-25, found during r1)

`nio_cstr` in `m2_substrate.zag` carries ONE explicit deviation from
production: `b[s.len]=0;` (explicit NUL terminator).

Root cause: production `nio_cstr` never stores the terminator — it relies
on the allocator's zero-fill. Under dirt D1..D5 the terminator byte is
0xFF/0xAA/..., so every path-based `open(2)` receives an unterminated
string, fails with ENOENT, and deterministic file-IO modules (c04, p10's
state load) spuriously diverge → false FAILs. This is instrument
confounding (substrate machinery breaking), not target nondeterminism.

The fix preserves `nio_cstr`'s documented contract (NUL-terminated C
string) under all dirt patterns. It does not change allocation layout,
header, alignment, or any target-visible behavior beyond restoring the
production-observable contract. All other substrate bytes remain
identical to production. The layout proof above is unaffected (it does
not exercise `nio_cstr`).

## Conclusion

The audit allocator satisfies §5.2: the gate certifies the same build
that ships, modulo the deterministic dirt fill — which is the instrument,
not a layout change. Battery runs may proceed.
