# Crew D Build Provenance

## Toolchain
- Pinned toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- All 5 variant binaries built from identical `src/kbctl.zag` via `src/gen_variant.py`
- Variants differ only in `IG_BLOB_CHUNK` constant:
  - c4096: 4096
  - c8192: 8192
  - c65536: 65536
  - c1m: 1048576
  - c33m: 33488896 (genuine production geometry)

## Fast target source
- Production reference: `~/workspace/kb_control/crewD/ref/ingest.zag`
- Fast target commit: `118251c597d77b41d91927470d007318eef78623`
- Wrapper `src/kbctl.zag` embeds the reference via `@import` and adds CLI commands.

## Build commands
```bash
cd ~/workspace/kb_control/crewD
python3 src/gen_variant.py  # generates build/<variant>/kbctl.zag
for v in c4096 c8192 c65536 c1m c33m; do
  (cd build/$v && ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 kbctl.zag -o kbctl)
done
```

## Wrapper deviations from production
1. **Tail reload**: Reloads final blob tail into `fill_buf`, appends via genuine `igb_append`, reseals. Production cannot reopen partially-filled sealed tail.
2. **Success events**: Adds one success event per fact. Zero-event stores fail reload; native `sc_add` success creates no event.
3. **Init defers store.dat**: Created on first put, not at init.
4. **Offsets**: Persisted offsets are genuine padding-blind fast offsets (the defect under test).
5. **bulkfill**: Uses genuine `igb_append` and `sc_add` (via safe wrapper, see below).
6. **Chain scratch safety**: `kb_compact_and_seal_safe` uses dynamically-sized scratch instead of fixed 49184-byte `chain_scratch`. `kb_seal_final_safe` skips seal when event log exceeds scratch. Both preserve all other semantics; chain/seal not verified on load.
7. **Safe sc_add**: `kb_sc_add` identical to production `sc_add` except uses safe compact.

These deviations do not affect the silent-overwrite defect under test (padding-blind offset reconstruction in `ig_revise`).
