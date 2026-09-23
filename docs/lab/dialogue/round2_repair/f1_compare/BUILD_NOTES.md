# F1-COMPARE — build notes

Date: 2026-09-23.

## Toolchain (pinned)

`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

## Source

`dialogue/round2_repair/f1_compare/dialogue.zag` (pure Zag, zero RNG)
sha256 `b57ceec0ec5d3d837cf39c38bd11034f4293fcd32e6ca0da7e4a24789c6df902`

Build prerequisites in the same directory (cleanroom fork copies):
`R33_NATIVE_SHA256_V2.zag`, `R33_NATIVE_IO_V1.zag` (the `@import` at the top
of dialogue.zag), `kb.txt`, `gaz.txt`, `battery.txt`.

## Build command (run in `f1_compare/`)

```
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 dialogue.zag -o dialogue_bin
```

Result: `dialogue_bin`, sha256
`4cd89f225aa76b9ab7c4f453345d2a762ce4181639c141dc4fc03532fae6ec10`
(289198 bytes main). Analyzer warnings only (A0102/A0107, same classes as the
unmodified baseline build — no errors).

The binary is a batch runner: it reads `battery.txt` from the working
directory (`DIALOGUE <id> <type>` / `U <turn>` / `E <expected>` lines),
prints `A <response>` per turn and `T <id> <n> PASS/FAIL` per expectation,
then section totals and a sha256 DIGEST of all responses.

## What changed vs the frozen canonical source

Only `dialogue.zag` differs (kb.txt/gaz.txt/R33 files are byte-identical
copies of the frozen originals):

1. **New:** `needs_the`, `word_entity`, `cmp_scan`, `time_marker_idx`,
   `time_val`, `cmp_yesno`, `do_compare` — the general comparison engine
   (see PREREG_F1.md §2).
2. **Replaced:** the two frozen string-prefix branches in `do_compose()`
   (`"was the author of"` → yes/no, `"which is taller"` → "X is taller.")
   with one call to `do_compare()`. The `did…write` → yes/no and
   `birth year` branches are untouched.
3. **Signature:** `do_compose()` takes three new params (`sal`, `pv`, `bout`)
   for pronoun resolution, pair memory, and the resolved-text scratch
   contract; the single call site in `do_turn()` updated.
4. **State:** `pv+32/pv+36` store the last compared entity pair (written only
   by successful comparisons; initialized to −1 at each DIALOGUE reset).
   `pv` was already 64 bytes; slots 32/36 were unused.
5. **Data fix:** `needs_the` listed "montparnasse tower" with length 17, but
   the name is 18 chars, so the `the`-prefix never fired for it (latent —
   no round-1/round-2 probe ever named it a winner). Corrected 17→18; no
   previously-passing output changes.

Binaries are build artifacts and are NOT committed (repo convention);
rebuild with the command above to reproduce byte-identically.
