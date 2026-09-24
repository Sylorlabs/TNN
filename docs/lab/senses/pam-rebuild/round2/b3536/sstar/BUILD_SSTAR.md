# BUILD_SSTAR — B-3536-S* battery build record

**Date:** 2026-09-24
**Prereg:** PREREG_RT_S.md (commit `577829e3`, frozen alone before code)
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`; pure Zag, zero RNG.

## Driver (unmodified)

- Committed composition driver `b3536.zag` @ build `7a1a8422`
  (file SHA-256 `1602247d7c9f1e96ba0f9df30a7b197f6a9ff71884df67c1cfb93c1807280029`,
  git blob `bff9f8161e7f1b225fa9514ae67da03a5030b857`).
- Mechanisms extracted VERBATIM by `gen_sstar.py` (exact byte-slices, each asserted
  present exactly once; new code asserted not to redefine any extracted symbol):
  ob_puts, ob_puti, fnv32, put32i, put64i, get32i, put32u, LowVal, HighVal,
  tag_half, verify_high, declassify, act_sink, premise_sink, wstep, honest_wc,
  honest_wm, cstep, admit36, adv36_conf, adv36_meas, au_put, au_get, le64,
  tb_putc, tb_puts, r36_derive_seed, ledger_has, ledger_add, c_stage2, c_wevo,
  m36a_precompute, comp35j, comp36j, comp36k, comp36m.
- R33_NATIVE_IO_V1.zag / R33_NATIVE_SHA256_V2.zag: byte-identical copies of the
  b3536/ files (git blobs a6b440d2 / 5dd858fa, verified).
- `b3536_sstar.zag` (generated): SHA-256
  `199e0fbbf3d5716234935be8f96c87faf58006e1f7e56dbfbe95cb83f79156c2`
  (final build; includes put32u for wstep).

## New code (sstar_new.zag only)

- `sstar_pred` — the S* scorer, pure function of (admitted record, world record),
  fixed pre-run per PREREG_RT_S §1. Class ids 0=N, 1=O, 2=P.
- Fixtures (120 trials each, deterministic, same mint/world-reading privileges as
  C36M/C36J, no ns_sha256/seed/material to any fixture):
  - `sstar_n`: id=7000+t, conf=wc, meas=wm, label=0, declassify(v,1).
  - `sstar_o`: id=7000+t, conf=wc, meas=wm+20, label=0, declassify(v,1).
  - `sstar_armt`: two-phase temporal reference — pre-draw commit of blind
    (adv36_conf/meas) values stored in a commitment slot, world evolves, open
    checked against the STORED commitment + world consistency.
  - `precommit_exists`: the O-temporal structural bit (audited static fact = 0;
    see verify_facts.py fact 2).
  - `sstar_p`: id=(0x1F2E3D4C<<32)||lo(7000+t), conf=wc, meas=wm, label=1,
    declassify(v,1).
  - `sstar_honest`: id=7000+t, conf=wc, meas=wm, label=1, declassify(v,1);
    scored under each class's S*.
- Anchors re-run via the extracted originals: comp35j, comp36k, comp36m, comp36j.
- main: argv `<material_hex:64> <ledger_path>`; seed via verbatim
  `r36_derive_seed(T,"sstar",material,digest)` + file-backed reuse ledger
  (fresh ledger per run; identical material ⇒ identical seed_hex line ⇒
  byte-comparable stdout).

## Build

- `znc b3536_sstar.zag -o b3536_sstar_bin` — clean (one pre-existing analyzer
  warning inside verbatim `ledger_add`, also present in B-3536's build).
- znc landmines respected: no []i32/u32/u16 indexed casts, no slice ==, no .*
  on non-pointers, no bare blocks, `return;` in voids, no try identifier,
  all u64 < 2^63.

NO RUNS YET at build-commit time (this commit precedes all runs per §5).
