# Wiring build log — Phase A2

## Toolchain
- Pinned: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- Build method: concatenate sources (avoids `@import` cwd ambiguity, per AGENTS.md), compile with `znc <full> -o <bin>`.
- Build script: `build.sh` (regenerates all five binaries).

## Sources (local `src/`, committed under `docs/lab/audio_longhorizon/wiring/src/`)
| file | role |
|---|---|
| `organ_lib.zag` | Byte-identical frozen Crew-P organ (main renamed to `organ_standalone_main_unused`); shared helpers. |
| `f0low.zag` | Low-band F0 estimator + range guard (wiring layer, not frozen). 55–125 Hz validated; <55 Hz explicit below-floor/unvoiced. |
| `emit_main.zag` | Ingest diagnostic: WAV → descriptor line; `probe` mode for F0 characterization. |
| `delib_main.zag` | Standalone deliberation from descriptor lines (diagnostic; evidence uses `session_run`). |
| `render_act.zag` | Action → output WAV renderer (pure Zag). |
| `session_main.zag` | Full-loop evidence binary: session.txt + intent + mode → journal. Embeds organ+guard+delib; descriptors internal. |

## Frozen organ rebuild check
`organ_frozen` rebuilt from `~/workspace/audio_principles/crew_p/organ.zag`:
- SHA-256: `1ed4bfba250336ad1da3fdbc66e865fe09cb6913854894c2faf0b119b53a5128`
- Matches frozen `BUILD_LOG.md` SHA byte-identically. The embedded organ in `session_run`/`emit_desc` is this exact code.

## Binary SHAs (build 2026-09-26, after F0 floor fix + sr fix)
| binary | SHA-256 |
|---|---|
| `emit_desc` | `d8efe58c1059d5f82d0cc43409dcf83c2aec33f3d77856a8e1df5da750c61820` |
| `deliberate` | `242c378ef094736905a40dceee1215ffd978c7bdbee45d2a29160335494c7656` |
| `render_act` | `647d76e036b9e627be695afd26d5be6f71050f071e1dd2fb7bc31a65eb1df498` |
| `session_run` | `5513391538104bfb1049835e452b46a00b51427200511b5a0b7f3ae081ec6cad` |
| `organ_frozen` | `1ed4bfba250336ad1da3fdbc66e865fe09cb6913854894c2faf0b119b53a5128` |

Binaries are NOT committed (per repo convention); SHAs + this log are the record.
Rebuild: `bash build.sh` from `docs/lab/audio_longhorizon/wiring/`.

## Zag constraints honored
- No `as []i32/u32/u16`; all tables are `[]u8` arenas with LE accessors.
- No slice > 2^25 bytes (largest: 208000-byte FR arena).
- `.*` only on pointers; no bare `{}` blocks; NUL-terminated syscall paths; `return;` in void fns.
- `_zag_arg(n)` pointers never freed.
