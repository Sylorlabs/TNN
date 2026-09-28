# K1 Build Log

## 2026-09-21 — Implementation

**Source:** `cl/arm.zag` (~2,470 lines, pure Zag)
**Compiler:** `toolchain/bin/znc_linux_x86_64_abed8aa1`
**Substrate:** `substrate/R33_NATIVE_SHA256_V2.zag`, `substrate/R33_NATIVE_IO_V1.zag`
(next to `cl/`, per AGENTS.md import rule)

### Mechanism implemented
- Native SHA-256 identity: `ID = SHA-256(content)`, digest as `u64[4]`, four-word compare.
- Fixed-capacity open-addressing table at 2× expected unique spans; linear probe from
  `digest[0] mod capacity`; full payload-byte confirmation on digest hits.
- Dedup → refcount++ and audited `OP_DEDUP_HIT` (=20).
- Real digest collisions chain in insertion order; synthetic forced-collision tests.
- Append-only payload store; revision changes identity; append-only
  `OP_REVISE_LINK(old_id → new_id)` (=21); recall follows revision links.
- Occurrence records: corpus/offset/length/role/flags/boundary/shift metadata.
- Whitespace tokenizer (separators `0x09`–`0x0D`, `0x20`).
- Chunked stores (table/payload/occurrence/ledger) — no slice over 2^25 bytes.

### Build issues fixed
1. **Slice→pointer casts.** This znc build: `slice as i64` does NOT yield the data
   pointer. All raw syscalls now use `_zag_slice_ptr(slice) as i64`. (Was corrupting
   all stdout and file IO.)
2. **Invalid frees.** Removed `nio_free` on: `read_bin` sub-slice returns, string
   literals (`keyp`, `names`), `_zag_arg` results. `nio_free` only on
   `nio_alloc`/`_zag_i64_to_str` results.
3. **JSON field order.** `j_int`/`j_str`/`jf_dec1` were prepending; fixed to append.
4. **M4 no-op defects.** `code_rename_k1` is a no-op when a token contains none of the
   rename patterns; `k1_defect_content` already skipped identical patches honestly, but
   t_m4 counted them as repaired. Now tracks `d_eff` (effective-defect mask); repair
   rates use effective denominators; `m4_eff_boundary`/`m4_eff_content` exported.
5. **Stray sed deletion.** A bulk `sed -i` removed the `fn t_m4` header; restored and
   verified via diff (only intended changes remain).

### Test status
- `k1-selftest`: 9/9 checks pass, clean valid JSON.
- M1 prose (r1a, pre-M4-fix binary — M1 path identical): recall 100.0%, boundary 100.0%,
  swap probe 100.0% (64/64), 963,478 units. JSON validated with Python `json`.
- Full 1× battery (20 modes × 2 runs) in progress: `work/run_battery.sh`.

## 2026-09-21 — U7 adjudication fix: k1-chain salt-loop saturation (measurement bug)

**Symptom:** `k1-chain-1x` printed `FATAL,k1-chain,recall` deterministically (kill ii
unevaluable). Instrumented-binary diagnosis (`DIAG,b=8,j=13,...,walk_hops=19,find=275618,
ref=0,flg=1,len=1`) proved the root cause — see `U7_ADJUDICATION.md` §3:

- The revision salt loop mutated only the first byte → 1-byte tokens have just 256
  possible digests; the single-byte digest space saturates after a few batches.
- On exhaustion `k1_ensure` dedup-hit a foreign digest; the occurrence was repointed
  into another token's chain; recall followed fork-rule first-links into a refcount-0
  slot → `-1` → FATAL.
- Mechanism (`k1_ensure`/`k1_link`/`k1_walk`/refcount guard) behaved per spec throughout;
  no znc toolchain quirk implicated (byte-wise accessors; DIAG read-backs correct).

**Fix (measurement only, mechanism untouched):** saturation fallback — if the 300-try
salt loop exhausts, append 8 deterministic salt bytes
`((b*131+j*17+sb*31+firstb) & 255)` and re-hash (bounded guard); `out` buffer
256 → 1024 bytes; `nb` sized `cl+8`. Novelty guarantee restored unconditionally;
schedule, kill criterion, and metrics unchanged.

**Rebuilt:** `cl/k1test` from fixed `cl/arm.zag` (znc `znc_linux_x86_64_abed8aa1`;
analyzer warnings only). Full 20-mode × 2-run battery re-run: `work/runs/u7/`.

## Binary / artifacts
- `cl/k1test` is scratch; **not for commit**. Remove before commit along with
  `.zag-cache/`, `.zagd.semantic-ready`, `work/`, and corpora copies.
