# BUILD5R — v5 repair build log (2026-09-27)

## Toolchain
- `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- SHA-256: `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`
  (pinned; matches BUILD_LOG.md / AGENTS.md)

## Source provenance
- Base: `onebrain_v4.zag` from commit `bd948b4aa`
  (`docs/lab/onebrain4/impl/onebrain_v4.zag`),
  SHA-256 `bbb1752ec5ee0c8bc3871bb41c4cfe65bc0d8e27f9357883d1712dbb4b006874`
  — verified before editing.
- IO import: `R33_NATIVE_IO_V1.zag` from `bd948b4aa`
  (`docs/lab/onebrain3/impl/R33_NATIVE_IO_V1.zag`),
  SHA-256 `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8`
  — matches BUILD_LOG.md.

## Build-environment verification
Rebuilt v4 from the verified source before touching anything:
`onebrain_v4_check` SHA-256
`630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe`
— EXACTLY the pinned binary SHA from BUILD_LOG.md. Build environment
reproduces the frozen R4/v8 machinery byte-identically.

## The repair (ONLY behavioral delta v4 → v5)
`audit_invalidate`'s annihilation guard: a bid now counts as live only if
it would survive `audit_cleanup` right now — bid row alive AND gating
reading (`bid@32`) alive AND supporting fact (`bid@44`) alive. Previously
row-alive only. Comment documents the repair inline; header documents the
v5 delta. No other behavioral change; all 11 modes' semantics otherwise
identical.

## Build command (cwd = build dir; @import resolves relative to cwd)
```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 onebrain_v5.zag -o onebrain_v5
```
- Exit 0. Same 2 pre-existing analyzer warnings as v4 (E0102, led_init —
  present verbatim in v3/v4 sources; untouched).

## SHAs
| file | SHA-256 |
|------|---------|
| `onebrain_v5.zag` | `d383e385def35f5ef7eefe9c812d81334f3e64e50ff75d5372ed06a0e9529534` |
| `onebrain_v5` (binary) | `2be50614dbf9302971e7ba218ac0ed48d22cb4cfbf992a4e89233ae310ecbec9` |
| `onebrain_v4_check` (rebuild control) | `630586da251f37bd72d60fd426fd7039142b81653a08a3527c892c21a42720fe` |
