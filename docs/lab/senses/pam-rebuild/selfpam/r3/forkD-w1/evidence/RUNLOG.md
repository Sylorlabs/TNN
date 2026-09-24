# H6-R3 fork D — RUNLOG (2026-09-24)

## What was built
Fork D over a **write-once evidence partition**: provenance depends on
physical partition membership, not EXT/GEN labels. Two structurally
separated binaries from one Zag source tree:

- `forkD` — atomize / prove / verdict / battery / gen / genm7 / verify.
  NEVER imports the partition writer (build-gated, 8 gates).
- `ingest_sensor` — the sensor/ingest path. The ONLY partition writer.
  Never imports the draft generator, deliberation, prover, or atomizer.

Partition format: `EVPART1\n` magic, entries `seq|atom|hexdigest`, atom =
canonical five-field `Q|S|POL|R|O` (no provenance label). Chain:
genesis = 32 zero bytes, `d_i = SHA256(prev || be64(seq) || atom || 0x0A)`.
External `head.txt` anchor. The reader recomputes every entry and compares
the final digest to the anchor; any mismatch → no trusted evidence → the
verdict path withholds (safe failure).

## Build
- Pinned toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`,
  compiled from `src/` (workspace @import convention).
- `build.sh` enforces 8 build-killing gates (KB1 structural separation,
  no PROV label literals, no RNG, no mistyped casts, create-only writer).
- All gates pass. Binaries: `forkD` (475935 B), `ingest_sensor` (122270 B).

## Defect found and fixed during the run
`part_create` initially used `O_WRONLY|O_CREAT|O_TRUNC`: a re-ingest
silently overwrote a sealed partition (observed 17:55, bytes identical due
to deterministic ingest, verify still VALID — the overwrite was caught by
testing re-ingest, not by any failure). Fixed: `part_create` and
`part_seal` now use `O_WRONLY|O_CREAT|O_EXCL` (193); re-ingest fails loudly
("ingest: cannot create partition"), re-seal fails loudly ("ingest: seal
failed"), originals untouched. Gate 8 added: no `,577,` open in
`evpart_write.zag`. The `forkD` binary is byte-identical before/after the
fix (proven by `cmp`), so all battery evidence below stands on the final
binary too — re-verified by reproducing `run1/c6.out` byte-for-byte with
the final binary.

## Corpora (ingest-first workflow)
- `ingest_sensor ingest <kind> corpora` for c1..c6 (72 main-domain EXT
  facts) and m7 (56 forest/water EXT facts) → `partition.dat` + `head.txt`.
- `forkD verify` → all 7 VALID.
- `forkD gen c1..c6` + `forkD genm7` → drafts/delib/manifests.
- Determinism: re-ingest of c1 produced byte-identical `partition.dat`
  (sha256 13b52a3190bf... in two independent runs) and identical heads:
  main `607ab184bfb5d391acaa4624fe1cc31e730c9be93a2518228d6c443bb9776f70`,
  m7 `ff3f5df1a500f05f42ffe757ac6c88bbb43ab41d85efa7afeaa91b1f1beefebe`.

## Batteries (run1 + run2, byte-identical ×2 — all 7 `cmp`-clean)
| battery | score | bar | R2 reference |
|---|---|---|---|
| M1 (c1 confab) | 140/140 withhold | ≥70% | 140/140 |
| M2 (c2 paraphrase) | 135/140 install (96.4%) | ≥90% | 135/140, same 5 misses (M2-108/109/110/113/116) |
| M3 (c3 pairs) | 130/130 install | ≥95% | 130/130 |
| M4 (c4 trace-alibi) | 60/60 withhold | ≥70% | 60/60 |
| M5 (c5 provenance) | 60/60 withhold | ≥70% | 60/60 |
| M6 (c6 clean) | 40/40 install | ≥95% | 40/40 |
| M7a (held-out confab) | 70/70 withhold | ≥70% | NEW |
| M7b (held-out paraphrase) | 70/70 install | ≥90% | NEW |
| M7c (held-out pairs) | 130/130 install | ≥95% | NEW |
| M7d (held-out trace-alibi) | 30/30 withhold | ≥70% | NEW |
| M7e (held-out provenance) | 30/30 withhold | ≥70% | NEW |
| M7f (held-out clean) | 20/20 install | ≥95% | NEW |

Equivalence proof vs R2 D: every c1–c6 case verdict is byte-identical to the
R2 reference `results.txt` (diff-clean excluding the digest line, which
R2's file embeds and R3's binary emits on stderr); c3's digest
`615ff28876cab9d9ac4c507ab8019f1a79bbdb4f4083a3ce11bb8d2a7aaa8814`
reproduces exactly. M7: 350/350, zero mismatches.

## Tamper battery (KB3): 9/9
- t1 entry-field flip (digest kept) → INVALID, battery all-WITHHOLD
- t2 digest hex-char flip → INVALID
- t3 entry swap → INVALID (seq mismatch)
- t4 truncation → INVALID (head ≠ anchor)
- t5 forged suffix: VALIDLY-CHAINED extra entry (independent python
  implementation) vs the STALE anchor → INVALID — detection is via the
  external anchor, not the chain math
- t6 unpartitioned live-state mutation (25 forged GEN entries in
  `live_state.txt`, a file the battery never reads) → verdicts unchanged
- batteries run against t1/t4/t5 partitions → 0 INSTALL (safe failure)

## Write-once proof
- Fresh ingest → ok. Re-ingest same kind → `ingest: cannot create partition`
  + `ingest: unknown kind or failure`; partition bytes untouched, still VALID.
- Partition removed but `head.txt` kept → re-ingest appends then
  `ingest: seal failed`; the original anchor is preserved.

## Notes / limits
- Fixed-size working buffers (reader 65536 B EXT text, 1 MB file reads) are
  corpus-bound implementation buffers, not TNN design limits; the largest
  corpus here (m7 EXT text) is ~5 KB.
- No RNG anywhere (gate 6 greps rand/rng/seed/clock/getrandom/time(); the
  only `time` hits are none — verified). Pure Zag, deterministic.
- `emit_digest` writes the battery digest to stderr (inherited R2 behavior);
  `.out` files hold case lines, `.err` files hold the digest.
