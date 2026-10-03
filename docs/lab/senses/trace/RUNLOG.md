# RUNLOG — SENSE-TRACE v1 trace foundation (worker B, 2026-09-26)

## Brief
White-box trace foundation for all three sense intakes (Micah order
2026-09-26 ~09:56 PDT: "use white box foundation to trace everything").
Model: the pentagon investigation (3a49b9c7031c) — a defect traced to a NAMED
mechanism by parsing the actual trace, not vibes.

## Repo verification (before any commit)
- Live tree: `~/workspace/selfpam_run/tnn-lab` (git repo, branch `tnn-native-lab`).
  `~/workspace/tnn-lab` is a stale mirror (not a git repo) — but the pinned
  toolchain binary there (`toolchain/bin/znc_linux_x86_64_abed8aa1`) is the
  brief's pinned build tool and is used as-is.
- Sibling head-sample repair commit: NOT landed as of 2026-09-26 ~17:30 PDT
  (no commit matching head-sample / samples 0-63 repair in --all log). Built
  on current code; the head stage is documented so the repair's verification
  can use the trace points + golden head checksum.

## What was built (docs/lab/senses/trace/)
| file | role |
|---|---|
| `sense_trace.zag` | pure-Zag trace library (SHA-256 stage hooks, deterministic log writer) |
| `R33_NATIVE_SHA256_V2.zag` | pinned SHA-256 impl (RFC vectors verified: `abc`→ba7816bf…, empty→e3b0c4…) |
| `R33_NATIVE_IO_V1.zag` | pinned nio substrate |
| `audio_intake_trace.zag` | traced WAV intake (crew-P organ idioms verbatim) incl. head_samples_0_63 stage |
| `image_intake_trace.zag` | traced BMP intake (v3/ingest.zag idiom verbatim) |
| `video_intake_trace.zag` | traced PPM intake (read_ppm_gen idiom verbatim) |
| `sense_trace_py.py` | Python emitter, identical grammar (for hear() instrumentation) |
| `trace_verify.py` | verifier: grammar + provenance closure + HELD binding + goldens |
| `TRACELOG_FORMAT.md` | format doc + stage inventory + localization procedure |
| `build.sh` | builds the three drivers with the pinned toolchain |
| `SHA_MANIFEST.txt` | SHAs of committed sources + golden stage checksums |

## Zero-impact proof (tracing on vs off — outputs must be byte-identical)

| sense | input (golden SHA) | out, trace=on | out, trace=off | on==off? | round-trip == input? |
|---|---|---|---|---|---|
| audio | fixture_strike.wav `cca99cda…ad9` | `dd740d0d…d6d7f` | `dd740d0d…d6d7f` | YES | n/a (held = s16 payload) |
| image | original_512.bmp `4ee3414b…b00` | `4ee3414b…b00` | `4ee3414b…b00` | YES | YES, SHA-identical |
| video | circ_test.ppm `1e561e6d…86b6` | `1e561e6d…86b6` | `1e561e6d…86b6` | YES | YES, SHA-identical |

Determinism: trace=on run twice → trace logs byte-identical (audio
`2ea18b2a…4864b35`, image `21a31f6b…220e3415`, video `1305f912…2e24fb`).
No trace log is written when tracing is off (by design).
`trace_verify.py` PASS on all three logs (provenance closure + HELD binding).

## Head-sample stage verification (independent cross-check)
Golden head checksum (samples 0–63 = payload bytes [0..128]) for
fixture_strike.wav: `f183085e661eabe4a09acf919b3c30bca568ea36828cd2ad3895eab45d996271`
— confirmed independently via `python3 hashlib.sha256(open(wav).read()[44:172])`.
nsamp=18856 matches the input verdict. The Python emitter demo:
- repaired hear() (head stored) → `trace_verify.py --goldens` PASS
- buggy hear() (head never stored, the L1 bug) → `FAIL: STAGE 2
  audio.head_samples_0_63: out=- != golden f183085e…` — the defect localizes
  to the exact stage, which is the whole point of this foundation.

## Notes
- Analyzer warnings during build are A0102 (ignored nio_close/nio_sync
  returns) — same pattern as the existing intake code; no behavioral impact.
- `nio_open_child` rejects `/` in names: drivers take bare filenames
  relative to cwd (documented in build.sh usage).
- Outputs overwrite via O_TRUNC (file_write idiom), never O_EXCL — reruns
  don't fail on existing files.
- Pure Zag, zero RNG throughout the intake path and trace library. The
  Python files are tooling (emitter/verifier), not intake machinery.
