# BUILD_CMDS.md — F2 appeal battery instrument builds

All builds run from `kb/autopsy/channels2/build/` (a scratch dir; binaries
and .zagd caches are NEVER committed). The `@import("../../../../toolchain/...")`
in the sources resolves relative to the build cwd:
`build/../../../../toolchain/R33_NATIVE_IO_V1.zag`
= `~/workspace/tnn-lab/toolchain/R33_NATIVE_IO_V1.zag`.

Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

```sh
Z=~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
cd ~/workspace/tnn-lab/kb/autopsy/channels2/build
$Z ../f2appeal/src/r1_noise.zag     --no-zagd --no-analyze --no-foreground-cache -o ../f2appeal/build/r1_noise
$Z ../f2appeal/src/r2_maj.zag       --no-zagd --no-analyze --no-foreground-cache -o ../f2appeal/build/r2_maj
$Z ../f2appeal/src/alt_transform.zag --no-zagd --no-analyze --no-foreground-cache -o ../f2appeal/build/alt_transform
$Z ../f2appeal/src/r4_noise.zag     --no-zagd --no-analyze --no-foreground-cache -o ../f2appeal/build/r4_noise
$Z ../f2appeal/src/channel_c3.zag   --no-zagd --no-analyze --no-foreground-cache -o ../f2appeal/build/channel_c3
$Z ../f2appeal/src/score_tcp.zag    --no-zagd --no-analyze --no-foreground-cache -o ../f2appeal/build/score_tcp
```

Frozen sense binaries (SHAs frozen in the prereg; binaries never committed):
- A: `~/workspace/tnn-lab/senses/rebuild/a_raw/sense`
- B: `~/workspace/kb4-f2/build_b/sense_b_rebuilt` (rebuilt 2026-09-23 from
  frozen `b_percept/*.zag`; byte-identical to the frozen SHA).

Runner scripts (`run_g0.py`, `run_r1.py`, `run_r2.py`, `run_r3.py`,
`run_r4.py`, `score_f2.py`) are Python glue only: file prep, sense-binary
invocation, verdict-line writing, MI arithmetic from Zag-emitted counts.
All verdicts (C=/verdict=) and contingency counts come from the pure-Zag
binaries above. truth.json is opened ONLY by `score_f2.py` at score time.
