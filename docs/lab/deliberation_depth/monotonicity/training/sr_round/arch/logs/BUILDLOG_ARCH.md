# BUILDLOG — SR ROUND, ARM ARCH (confidence-as-distribution)

## 0. Inherited state (RESUME after daemon restart, 2026-09-24)

Predecessor (killed by daemon restart; final message lost) left
`training/sr_round/arch/` = src/ (10 files: R33_NATIVE_IO_V1.zag,
R33_NATIVE_SHA256_V2.zag, dlb_cfg/dlb_delib/dlb_json/dlb_ledger/dlb_util.zag,
feat.zag, policy_arch.zag, train_arch.zag), logs/ (EMPTY), params/ (EMPTY),
results/ (EMPTY), analysis/ (EMPTY). The trainer source EXISTS — training had
NOT started. No commits landed (branch head was cab05d07 at predecessor's
write; at successor resume the tnn-native-lab branch head is
f58403ff05fcf9123a9b677bf41989c53e12f5de — sister arms (WC, etc.) landed
commits after the restart; nothing from ARCH).

Verified 2026-09-24 by successor (this crew):
- All 7 library files (R33_*, dlb_*.zag) BYTE-IDENTICAL to v2's frozen
  `training/v2/src/` copies (cmp -s, 7/7 SAME).
- feat.zag: same structure as v2's frozen feat extractor (M4 release label,
  f1..f8 index-level §4 features); frozen `training/features/features.tsv`
  (5240 cells) is the input, SHA-256
  `4682190cfd504cb692df122a6b054d8fad65ef860707e6a92abfdf04e65a897d`
  = frozen pin (PREREG_SR §2). No re-extraction needed.
- train_arch.zag verified line-by-line against PREREG_SR §7 (frozen v1):
  head m = clamp((Σuᵢfᵢ)/1000 + c, 0, 1000), init u1=1000 rest 0, c=0;
  head s = clamp((Σvᵢfᵢ)/1000 + d, 0, 1000), init vᵢ=0, d=0;
  released R = clamp(m − s/2, 0, 1000).
  SEPARATE update paths: location on symmetric (m−Y)² + 4·rise² theater
  (own gradient path: uᵢ ← uᵢ − tdiv(2(m−Y)fᵢ + 8·rise·fᵢ, 40000),
  c ← c − tdiv(2(m−Y)·1000 + 8·rise·1000, 40000));
  spread on L_s = (s−|m−Y|)² with STOP-GRAD on m
  (vᵢ ← vᵢ − tdiv(2(s−|m−Y|)fᵢ, 40000), d ← d − tdiv(2(s−|m−Y|)·1000, 40000);
  u/c never touched in the spread path, s's loss never enters location).
  Theater construction (prev released same-id chain, rise on wrong→wrong
  m>mprev under current weights) and G-batch (G on released R per
  family/depth slot, strict rises: c ← c − tdiv(Gdiff,4)) are byte-level
  mirrors of v2's train2.zag (lines 175–196, 245–268, 313) with C→m/R.
  1 pass = 6 epochs (2 per phase, A→B→C); 10× = 10 passes (60 epochs),
  100× = 100 passes (600 epochs). Per-epoch log includes corr(s,|m−Y|) on
  released training cells (the §7 go/no-go telemetry).
- policy_arch.zag verified: M4 release skeleton (release L_t iff L_t==L_1,
  else ABSTAIN), m/s from frozen arch_params_*.zag (au0..au7, ac, av0..av7,
  ad — no collisions with dlb_*.zag symbols, grepped), conf = R,
  cert "trained-conf-arch", per-item TSV columns identical to mech.zag
  plus sidecar <results>.ms with (id, depth, m, s, rel, correct) for the
  §7 dead-spread check corr(m−s/2, m).

## 1. Rebuild (one deviation found and fixed, 2026-09-24)

Predecessor's train_arch.zag set only au_put64(u,0,1000) after nio_alloc —
u[1..7] and v[0..7] were left UNINITIALIZED, inheriting heap garbage.
nio_alloc is NOT reliably zeroed (~/AGENTS.md arena-init lesson; v2's
train2.zag line 207–209 carries the same latent pattern — frozen v2
evidence ran on allocator luck). This violates the §7 literal init
(u1=1000 rest 0, c=0, vᵢ=0, d=0). FIXED: explicit zero loops for u[1..7]
and v[0..7] immediately after allocation. This is a build note enforcing
the frozen init, not a prereg amendment. The repaired source compiles as
the arm's canonical build (below).

## 2. Pins (recorded BEFORE first training run, per §10 operational)

- Prereg: PREREG_SR.md FROZEN v1, SHA-256
  `f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30`
  (sha256sum-verified; every log's first line carries this SHA).
- Kill-bar table (§10): SHA-256 of bytes from the `## §10 Kill-bar table`
  heading line through (exclusive of) the `## §11` heading =
  `2243447e5efacdf36af066712662974aed57f86a844dda5ef6a5365c507b0260`.
  (Footnote: WC's BUILDLOG cites c4f5dfd8… for the same table — their byte
  range is not reproducible from their description; the two conventions
  differ but both pin the same frozen §10 text. This arm's convention is
  stated above; any auditor re-running it gets the same hash.)
- Weight init canonical string
  `ARCH_INIT v1 u1=1000 u2=0 u3=0 u4=0 u5=0 u6=0 u7=0 u8=0 c=0 v1=0 v2=0 v3=0
  v4=0 v5=0 v6=0 v7=0 v8=0 d=0 DIV2=40000` SHA-256
  `8b96321a28e3f950c13285782ea2a60aa2cd423bf68b2214b5f57d550452785d`
- Toolchain (pinned ONLY): ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
  (znc 2026.07.0-dev).

## 3. Design decisions (ARCH arm, PREREG_SR §7)

- Two-head form (m, s) is the intervention: location and spread get
  SEPARATE gradient paths with a hard stop-grad — spread cannot move m,
  location never sees s's loss. The released scalar R = m − s/2 couples
  them only at read time, so "estimate-high + uncertainty-high" is
  representable and the optimizer cannot resolve the tension by crushing
  a single scalar.
- G-batch computes G on the RELEASED confidence R (m−s/2), matching what
  the frozen analyzer will measure on eval legs; it adjusts c ONLY (the
  location bias) — spread weights/d are never touched by the G-batch.
- Theater lives on the location path alone (rise in m), with Cprev
  recomputed under current u/c — the v2 construction with C→m.
- 10× go/no-go (§7): (u,c) ≠ init AND corr(s, |m−Y|) > 0.3 on released
  training cells (log column corr_s, thousandths; 300 = 0.3).
  Else the arm is VOID → stop and diagnose.
- Falsification: corr(m−s/2, m) > 0.99 on eval (dead spread — "explicit"
  claim empty) OR any B1–B3/B4–B8 failure → ARCH KILLED, failing bar named.
- Determinism: pure Zag, zero RNG, fixed file order, fixed inits, integer
  arithmetic; `_zag_arg` reads never gated on argc (ZNC-2026-09-21-007);
  all tables on []u8 arenas with au_get/put32/64 accessors — zero
  `as []i32`/`as []u32`/`as []u16` casts in any source (audited 2026-09-24);
  no slice > 2^25 bytes; no function named zalloc; no bare {...} blocks.
  Builds run with cwd=src/ (imports resolve relative to cwd per
  ~/workspace/AGENTS.md); A/B = two full builds, cmp byte-identical,
  every leg A/B.

## 4. Run record

### 10× (60 epochs), 2026-09-24 ~00:17 PDT
- Binary: train_arch_A (SHA-256 0d85dc910e5a256b570bb25e1da2e9923ed7e4017a90aa527a955a4df70b2072),
  A/B byte-identical builds, RC=0.
- Log: logs/train_10x.tsv (SHA-256 41c3a8b8791c6683ff90271d11e4fb636b7e26a5761360655fd21c654f0a9008);
  first line = PREREG_SHA f55d1dbbe1a609f69301ce8f537282a0372880b51fdec6b51d0f588b9fd96d30.
- GO/NO-GO (§7): (u,c) ≠ init — u1=14053 (≠1000), c=−27134 (≠0) ✓;
  corr(s, |m−Y|) = 385/1000 = 0.385 > 0.3 ✓ (log column corr_s).
  Telemetry: theater fired (v2=5 final epoch), G-batch fired (gviol=23),
  meanConfCorrect=0.705 / meanConfWrong=0.212 on released training cells.
  → ARM NOT VOID, proceed to 100×.
- Params: params/arch_params_10x.zag (SHA-256
  ca701a09edf38edf1ff4e89466b3b8267f8bac9e8a0fd005923d7b708638101d).

### 100× (600 epochs)
(to be appended)
