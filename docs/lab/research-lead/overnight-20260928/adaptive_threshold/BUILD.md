# BUILD.md: adaptive threshold variant

## Core provenance

- Fixed core: `at_core_fixed.zag` = lines 1-1020 of
  `node2_generalization/gen_base.zag`, byte-verbatim (the same core the
  Node2-v2 generalization tests used).
- Adaptive core: `at_core_adaptive.zag` = the fixed core with exactly one
  line changed (verified by diff):

```
958c958
<   resolve_uncertainty_v2(W,s,r,a_w);
---
>   resolve_uncertainty_adaptive(W,s,r,a_w);
```

- `at_tests.zag`: `at_ev_get` (evidence node), `resolve_uncertainty_adaptive`,
  revelation helper, guide reader, three environment runners.
- `at_drv_adaptive.zag` / `at_drv_fixed.zag`: arm drivers with arm-specific
  state reporting.

## Binaries

- `at_bin_adaptive` = adaptive core + tests + adaptive driver
- `at_bin_fixed` = fixed core + tests + fixed driver

Both compiled with the pinned `znc_linux_x86_64_abed8aa1` under safebin PATH.
Build warnings are the pre-existing A0102 style warnings from the base.

## Runs

- `at_run_adaptive_1/2/3.txt`: SHA-256 identical,
  `ea5d31fcd2cd9a62d5db0d482f3292557b4904499001eebb8ac5213d2ca1ba2b`
- `at_run_fixed_1/2/3.txt`: SHA-256 identical,
  `06b2022d04f933bcf2f8fbc154eb657cbfa102579d6ac2b90395c45aade3d949`

## One-System audit

New code adds: 0 modes, 0 bridges, 0 task-specific handlers, 0 semantic
cases. The evidence node reuses the tag-40 policy-node family with a new
subtype; no new edge types; the write lands in the existing field-20
production path.
