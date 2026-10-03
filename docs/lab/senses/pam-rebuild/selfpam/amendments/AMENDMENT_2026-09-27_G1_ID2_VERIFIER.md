# Prereg amendment B — ledger-verifier low-byte masking for G1 id 2

Date: 2026-09-27 (Crew D, self-PAM production drive)
Applies to: self-PAM prereg v1 (frozen 2026-09-25, commit
`a6ae9d2d28b2b83dc40d50c3d84c0e83a0a7ea5dd`) as extended by amendment A
(2026-09-27-A, commit `e58ee88753818d5b4a2ffb5c200f8b411748eabc`).

## Finding

The Zag ledger writer in `round2/forks/R2-3/src/sense.zag` (unchanged since
R2-3 freeze) folds each pair's two judgment codes into the SHA-256 chain
through their **low bytes only**:

```
hbin[36] = (jf & 255)
hbin[37] = (jg & 255)
```

The Python mirror verifier `round2/forks/R2-3/src/mirror/verify_ledger.py`
(line 19) reconstructed the chain with `bytes([jf, jg, wh])` using the
**printed** judgment values. For gates 0/1 (reference / broken-positive-control)
all printed codes are < 256, so the verifier agreed with the writer. The
self-PAM fact-gate candidate (id 2, amendment A) emits `span_sum/8` judgments
that can exceed 255; on the first id-2 pilot ledger the verifier raises
`ValueError: bytes must be in range(0, 256)` instead of verifying.

This is a **verifier** gap, not a gate-semantics gap: the on-disk chain was
always built from low bytes, for every gate. Id-2 gate semantics are frozen
by amendment A and are not touched by this amendment.

## Amendment

1. The canonical ledger-verification rule for the R2-3 sense battery is:
   verification MUST mask judgment codes with `& 0xFF` exactly as the Zag
   ledger writer does (`hbin[36]=(jf&255)`, `hbin[37]=(jg&255)`).
2. `src/mirror/verify_ledger.py` is patched accordingly (`bytes([jf & 0xFF,
   jg & 0xFF, wh])`). For gates 0/1 this is a provable no-op (their codes are
   0..4), so all previously verified ledgers verify identically before and
   after.
3. The three id-2 pilot runs executed before this amendment are **pilot** runs:
   valid, deterministic, and byte-identical to the runs below, but the runs of
   record for amendment A acceptance are the three runs executed AFTER this
   amendment commits.

## Effect on prior material

- Amendment A unchanged; id-2 gate semantics frozen.
- R2-3 verdict evidence unchanged (masking is a no-op on ids 0/1 ledgers).
- DEMO_ONLY blockers unchanged.
