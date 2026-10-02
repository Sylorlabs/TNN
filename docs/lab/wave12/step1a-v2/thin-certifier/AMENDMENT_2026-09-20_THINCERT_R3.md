# DATED AMENDMENT — THINCERT-2026-09-20-v1 / R3 → R3′ + R1b

**Date:** 2026-09-20. **Status:** DRAFT — pending Micah's re-approval.
**Amends:** `PREREG_THIN_CERTIFIER.md` (frozen commit `d433fc8ba3cd`), §R3 and §R1.
**Author:** phase-2 lead (thin certifier). **Reason:** pre-implementation
validation found the frozen rule unsatisfiable by the frozen representative
build; the replacement is simpler AND sounder. Nothing is bent: the bar is
being changed openly, before any implementation code, with the reason stated.

## 1. The tension (found 2026-09-20, before implementation)

Frozen §R3 requires every `nio_alloc`'d slice to be initialized by a
canonical full-range init loop in the same function, with init loops nested
inside `if`/`while` → FAIL (R3c). The frozen representative build's
`load_file` initializes `dir` conditionally:

```zig
if(cut==0){dir[0]=47;}
else {let k:i32=0; while(k<cut){dir[k]=path[k]; k=k+1;}}
```

Both branches fully initialize `dir`, but the init is nested → the frozen
build FAILS frozen R3c → K1′ could never pass. The build does not fit the
idiom.

## 2. The deeper finding (audited, not assumed)

The pinned substrate's `nio_alloc` (`R33_NATIVE_IO_V1.zag`,
`e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`,
lines 19–23) **zero-fills the entire buffer before returning**:

```zig
let b:[]u8=p[0..n];let i:i32=0;
while(i<n){b[i]=0;i=i+1;}return b;
```

Every `nio_alloc`'d slice is therefore fully initialized at allocation.
Uninitialized-memory reads — the v2 K1 kill class — are IMPOSSIBLE BY
CONSTRUCTION for module code that allocates only via `nio_alloc`. The
dataflow/canonical-loop machinery of frozen §R3 was redundant: it re-proved
a property the allocator already guarantees. The prescriptive rule should be
the allocation idiom, not the dataflow.

## 3. The change

**§R3 is REPLACED by R3′ — allocation-idiom rule:**
- R3′a: the ONLY allocation idiom in module source is `nio_alloc`
  (from the pinned substrate). `_zag_malloc` / `_zag_realloc` tokens in
  module source → FAIL under §R2 (they are not Tier-M). Direct uninit memory
  is therefore unreachable in module code.
- R3′b: since the pinned substrate zero-fills, no read-before-init analysis
  is needed or performed. Canonical init loops (zero-fill or computed fill)
  remain RECOMMENDED defense-in-depth and are already present throughout the
  template — they are simply no longer load-bearing.
- R3′c: module source must not define functions named `nio_*` (new rule R4b
  under §R4): shadowing the substrate's allocation API with a non-zeroing
  impostor → FAIL naming `R4b`.

**§R1 gains R1b — substrate pinning:**
- Tier-S files must hash-match the prereg-pinned known-good substrate
  hashes, not merely be self-consistent with the plant's manifest:
  `R33_NATIVE_IO_V1.zag` =
  `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`.
  A tampered substrate (e.g. `nio_alloc` with the zeroing removed) → FAIL
  naming `R1b`. The substrate is fixed TCB; changing it is a future
  amendment.

## 4. Consequences, stated openly

- The v2 dirty3 class (`nio_alloc` + read-before-write) now PASSES static
  checks — CORRECTLY: it reads deterministic zeros; replay confirms. v2
  flagged it as hygiene; the thin certifier recognizes it as harmless.
- The uninit-read red-team class reduces to: direct `_zag_malloc` in module
  code (→ R2 FAIL) and tampered substrate (→ R1b FAIL). Both are banned-idiom
  plants with named rules.
- K1′/K2′/K3′, the fail-closed meta-rule, and all other rules are UNCHANGED.
- If this amendment is REJECTED: the alternative is amending the frozen
  repbuild (restructure `load_file` to hoist canonical init to top level) and
  keeping frozen §R3 — strictly more churn for a less-sound rule. Not
  recommended.

## 5. Approval

- [ ] Micah approves R3 → R3′ + R1b + R4b as above.
- [ ] Micah rejects → fallback: amend the repbuild instead (re-freeze hashes).

Until approved, all implementation and validation work is marked
`AMENDMENT-PENDING` and no K-bar is claimed as final.
