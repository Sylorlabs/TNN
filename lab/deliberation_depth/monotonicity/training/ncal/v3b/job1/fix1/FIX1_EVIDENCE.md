# FIX1 evidence — RT-F repair validation (2026-09-25)

**Fix:** `fix1/src/nec_v2d.zag` — `nec_cmp_id`/`nec_find`/`nec_store`
changed to full-id comparison via (ibuf offset, full length) stored in
slots. No bar/threshold/confidence rule touched. Built with pinned
`znc_linux_x86_64_abed8aa1` (`498abcb5…`), zero RNG.

## Validation 1 — baseline preservation (MUST be byte-identical)

Fixed binary on frozen adopted inputs, variant 20, A/B runs:

| scale | SHA-256 (A and B) | adopted |
|-------|-------------------|---------|
| s1 | `84ffaf89fd76d2a9119b2060f754d5fdaf72bf7288f0d2403be736d084a36b81` | match |
| s10 | `20ff1d1021bba3fcff8d1a4bb303c2f4485fd9a0297b28c2884473265c7c926a` | match |
| s100 | `f6a38269b931153b5b10e1d9df10e72bdfb02ca9806d49eb2c6db993ae680ff1` | match |

All A/B byte-identical. Zero behavior change on ids ≤63.

## Validation 2 — attack fixed

`rtf_collide.tsv` (frozen `34ee8d66…`), A/B byte-identical
(`bd616c7e…`):

- 72-char always-wrong ids: `950,0,0,0,0` (was 950 on all 25 cells).
- 72-char always-correct ids: 950×5 (unchanged).
- Short-id controls: byte-identical to original binary.
- Original-vs-fixed diff: EXACTLY the 20 long-wrong d2/d4/d8/d16
  cells (950→0); all other 80 rows identical.

## Validation 3 — determinism

A/B/C byte-identical on all validation runs (SHA-logged in
`fix1/sha_fix1.txt`).

## Conclusion

FIX1 accepted: principled in-class fix (lookup correctness),
baseline byte-identical, attack repaired. Recommended for adoption.
The 63-byte id cap (an arbitrary hard limit) is removed; ids of any
length are handled.
