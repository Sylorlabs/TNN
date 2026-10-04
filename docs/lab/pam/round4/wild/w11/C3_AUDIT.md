# W11 C3 CONSTRUCTION AUDIT — no-bypass (before first fixture use)

**Date:** 2026-09-24. **Auditor:** WILD-B crew. **Gate:** PREREG_W11 §4 C3.
**Status:** PASS — recorded before the W11 build.

## Claim audited

Every fixture chain in `wild/w11/w11_chains.txt` was built through the single
`anchor()` construction path in `wild/w11/gen_chain.py`, and the only
admission path is the `w11_chain.zag` verifier.

## Evidence

1. `gen_chain.py` contains exactly one function that creates an anchor MAC:
   `anchor(cid, calib)` (grep: `def anchor` → 1 hit; `hmac.new`/`M(K,` call
   sites → `anchor()` and `extend()` only). All 8 fixture classes
   (VALID/BROKEN_MAC/UNLISTED/OVERLONG/REPLAY/MID_TRUNCATE/FORGE_NOKEY/
   CALIB_DRIFT) call `anchor()` first; post-anchor mutations (mac flips,
   truncation, replay) are the DELIBERATE attack classes, each labeled.
   No chain literal is hand-written; no second construction path exists.
2. The verifier (`w11_chain.zag`, to be built) is the sole consumer of
   `w11_chains.txt` in this track; the battery admits nothing except through
   its verdict lines. (Re-confirmed at verdict time by source audit.)
3. FORGE_NOKEY chains (the C1 red team) never touch K — their MACs are
   counter-hex, constructed outside `anchor()`'s MAC path by design (the
   attack model), and are labeled as forgeries.

## Result

C3 construction gate: PASS. No bypass path found. The audit is re-verified
mechanically at verdict time (scorer re-checks every chain's provenance
class against its expected verification outcome).
