# VERDICT_R35 — Full-64-bit tag binding repair vs J-35

Prereg: `PREREG_R35.md` (frozen @ `b13b400806021903dddee1db66c14040a75ad609`,
committed alone before code). Target unmodified except the repair; attack
logic byte-identical to RT-JKLM's frozen J-35 class (script-extracted,
diff-verified).

## Repair (auditable diff, `apply_repair.py`)

`hpam3536_r35.zag` = `hpam3536_probe.zag` @ `b20ae9edf87da4aa` + exactly:
1. New `put64i` — 8-byte LE decomposition of `i64` (proven `put32i` style;
   u8 arena, no `[]i32` casts).
2. `tag_half` (HighVal sinks): binds all 8 bytes of `id,conf,meas,label,
   verdict,cap` — 48-byte preimage (was 24). Same dom 7/8, same CAP_NONCE.
3. `vec_tag_half` (IF3 sink): full-64 on `v0..v3,cap` — 40-byte preimage.
4. `premise_keyed` (IF4 sink): full-64 on `k0,k1,cap` — 24-byte preimage.
5. Scratch buffer 32 → 64 bytes (`m35`, driver).

Mode-36 paths untouched. Everything else (fixtures, counts, bar strings)
identical.

## Batteries (3 runs each, SHA-compare)

| Battery | Result (3× identical) | Bar | Verdict |
|---|---|---|---|
| B1 repaired m35 | adv 0/760, H2 0/40, H1 60/60 delay 0; stdout ≡ original (`60cd2abe…`, also matches the frozen probe's recorded SHA) | 0/760, 0/40, ≥57/60 delay 0, byte-identical to original | **PASS** |
| B2 J-35 (repaired tag) | installs **0/120** | ≤ 15/120 | **PASS** |
| B3 J-35 honest control | admits 120/120 (honest-loss 0%) | ≥ 102/120 (loss ≤ 15%) | **PASS** |
| B4 K-35 / L-35 / M-35 | 0/120 each | 0/120 (no regression) | **PASS** |
| B5 mode 36 | stdout ≡ original (`d71bb9be…`) | byte-identical | **PASS** |

No 3× divergence anywhere (battery not void). No honest-loss. No reopened
paths: K/L/M still 0/120, original G1 tag-replay (low-32-different content)
still 0/40 inside B1.

## Interpretation

1. **J-35 is closed by the repair.** The kill mechanism was precise: the
   minted tag bound only low-32 bits, so high-32-modified content recomputed
   the identical tag. With the full-64 preimage, the forged content recomputes
   a different tag at both sinks → 0/120 installs. The J-35 attack logic is
   byte-identical to the one that scored 120/120 on the original — the delta
   is the binding, not the test.
2. **Nothing else moved.** Repaired m35 stdout is byte-identical to the
   original probe's (all counts unchanged: tag values never print, and every
   refuse/admit decision is preserved — guesses still miss, honest mints
   still verify). Mode-36 byte-identical.
3. The verdict-bit authority and type barrier were never in question
   (L-35/K-35/M-35 held before); the repair restores the "tag binds content"
   sub-claim to the strength the hypothesis always stated.

**Outcome per PREREG_R35.md §4: REPAIR SUCCEEDS → H-PAM-35 TESTED-survived
(repaired).**

## Evidence integrity

- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (pinned). Pure Zag, zero RNG. Binaries built fresh, never committed.
- `verify_copies.sh`: `copy35_r35.zag` byte-identical to repaired probe
  functions; `drive35_r35.zag` regeneration-identical; `run_j/run_k/run_l/
  run_m/run_honest` byte-identical to RT-JKLM's frozen class.
- Every battery 3×; all SHAs in `runs/SHA256SUMS`.

## Run SHAs (stdout)

- `r35_m35` / `orig_m35`: `60cd2abe393fcb5eae42a6a86d9f51ea3435f1ae8e5d1bd10c5f61fbba14280b`
- `r35_j35`: `c195f1e288ce52fb0c10855aafab8484c7a00fdff21afe2a1d45d77070c8daa4` (0/120)
- `r35_honest`: `0b20426da60fbcf1d8eda8739b4e43441c0a83043a4a6eabe82caf8f918039c1` (120/120)
- `r35_k35`: `461661082ec14f418fe9663e0207db0f2e6432461714a01a6aca68579ceb2ac3` (0/120)
- `r35_l35`: `e71df6ffdd8170804532fff01ce9cd85c8c0b91171cfa9db0d8690d7dfceba19` (0/120)
- `r35_m35` (M): `bf148b442009799ea34fa0ddf92306f5b292d48f0fba8b9ec80a2f70e36e5558` (0/120)
- `r35_m36` / `orig_m36`: `d71bb9be0751d9004437f51f787fcfc99958b870bc8c4fc4af678330c54d1af3`

## Source SHAs

- `hpam3536_r35.zag`: `da10a482b5ab2ec605e616bd83bf7f6e77f1b5a4dbf57bc99b710f44505f7fd2`
- `copy35_r35.zag`: `4708af904b1bbe96cc07f95a6d5dc4efb6529f14b48492cdd3331c7c0c2b882f`
- `drive35_r35.zag`: `aa8c5a11c7c6dd8c9ae90fd77f8886ee5a9ae71648ee738255938bab1966cf2f`
- `R33_NATIVE_IO_V1.zag`: `e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8` (matches RT-JKLM pin)
- RT-JKLM attack source `rt_jklm/drive35.zag`: `40f9941bcac7d210c7a88258613301fffabd80a419560c51f50d92f05f9f2c69`

## Hash cross-check note

The repaired probe's SHA (`da10a48…`) was initially misread as suspicious;
a from-spec pure-Python SHA-256 (`sha256_pure.py`, FIPS test vectors pass)
agrees byte-for-byte with `hashlib`/OpenSSL/coreutils on all five source
files. Four-way agreement — the native hash stack is sound; pins above are
true.

## Residuals (not patched)

- Zag still cannot make `HighVal` construction private (carried from the
  frozen probe prereg); the tag carries the barrier in the toy.
- `put64i` on negative `i64` uses znc's truncated division/modulo; mint and
  verify share the identical function so binding is self-consistent by
  construction (exercised: IF5 `summarize` produces `id=-1`, still 0/80,
  honest paths unaffected).
