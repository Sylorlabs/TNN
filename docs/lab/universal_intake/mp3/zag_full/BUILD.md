# Building the pure-Zag MP3 decoder

**Sources** (all in this directory):
- `mp3dec.zag` — the decoder (MPEG-1 Layer III, 44.1 kHz, mono/stereo)
- `mp3tab64.zag` — all constant tables (Huffman, scalefactor bands, IMDCT/synthesis
  coefficients, intensity-stereo pan gains). Includes `load_f64tab` (f32 bit-pattern
  → f64 widening) and `load_f64tab_f64` (exact f64).
- `common.zag` — file IO (`file_read_all`, `file_write_trunc`, `cstr`) and bit/Huffman
  helpers shared with the decoder.

**Toolchain**: pinned znc at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.

**Important**: znc resolves `@import` paths relative to the *current working directory*,
not the source file. Build from this directory:

```sh
cd docs/lab/universal_intake/mp3/zag_full   # (in a checkout of tnn-native-lab)
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 mp3dec.zag -o mp3dec
./mp3dec <in.mp3> <out.pcm>                 # raw PCM16 LE, 44100 Hz
```

**Reproducibility note (2026-09-27)**: `common.zag` and `mp3tab64.zag` were missing
from this directory when `mp3dec.zag` was committed — the committed decoder could not
build from the repo (`@import cannot read 'common.zag'`). They are the exact build
inputs the stereo crew used (verified: fresh build reproduces the committed PCM
SHA-256 for all three fixtures). Always keep all three files together.

**Validation** (vs `../fixtures/`; two runs must be byte-identical):
| Fixture | PCM SHA-256 |
|---|---|
| t_128cbr.mp3 | `f72aca836ff4ddc69e6a084e302302243750e0857a7bc0a36de533a8b10bb467` (committed in `../EVIDENCE.md`) |
| t_vbr.mp3 | `7abcd3cb239f530cbc583ff9427738f2a2276bb47a14ae885551d7be63e4c6d5` (reference build, 2/2 deterministic) |
| t_128js.mp3 | `711f0f067397f1439f62f18275b88e0e25df86875936e11f27be0d65318209b0` (reference build, 2/2 deterministic) |
