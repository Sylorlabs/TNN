# Motion3 (M3) build notes — 2026-09-23

## Source
`senses/youtube_ingest/motion3/motion3.zag` — pure Zag, no imports
beyond `R33_NATIVE_IO_V1.zag` (syscall/alloc substrate).

## Toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(pinned). Build: `znc motion3.zag -o build/motion3` (with
`R33_NATIVE_IO_V1.zag` resolvable). The compiled binary lives ONLY in
`motion3/build/` and is NEVER committed.

## Analyzer warnings (4, non-fatal)
- Ignored `nio_close` return (z_read).
- Two small `_zag_i64_to_str` output-path leaks.
- Ignored `nio_write_all` return in failure reporting.
None affect decision logic. Documented here; repairing them would not
change frozen behavior.

## Cost
749,568 ops per standard 8-frame 64×64 clip (frozen target ≤1.5M;
method2 was ~2.8M).

## Zero RNG / zero time
`grep -i "rand|random|time|clock|seed"` over the source: zero matches.
All decisions are pure functions of the input bytes. Determinism:
- 3× single-fixture runs → identical stdout SHA-256
  (`ca2c2a40…ced`).
- Full B1+B2 battery twice → identical SHA-256 digest
  (`8bb05630…53343`).

## Binary anomaly (2026-09-23, documented honestly)
During B3 scoring, ONE direct run of the build binary on
`windows/OQSNhk5ICTI_w153.vid` returned a divergent result
(judgment=S, e_total=146801) while the surrounding runs returned the
correct one (N, e_total=150360). A fresh rebuild from the identical
source is byte-identical (md5 fefb7a46…) to the build binary, and
100+ subsequent runs of the same fixture all return the correct
result. An independent Python replica of the algorithm agrees with
the binary bit-for-bit on every tested input (per-pair n_vote and
e_total exact). Cause of the single divergent run is unknown and did
not reproduce. All verdict numbers below come from re-runs with the
verified binary AFTER the anomaly, plus the Python cross-check.
