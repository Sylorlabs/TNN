# A — Build Log

## Toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
(znc native codegen, Linux x86_64).

## Source
`units/arms/A/cl/arm.zag` (single file, ~1,500 lines) +
`units/arms/A/substrate/` (verbatim copies of R33 SHA-256 v2 and IO v1;
MD5s match B-64's copies).

## Build command
```
znc_linux_x86_64_abed8aa1 cl/arm.zag -o work/build/arm --no-analyze
```
The `--no-analyze` flag suppresses the background semantic analyzer
(which emits spurious dead-loop diagnostics on this file); the
foreground compile is clean.

Output: `units/arms/A/work/build/arm` (198,246 bytes, native binary).
Binary and `.zag-cache/` are work artifacts, never committed.

## History

### Prior session (2026-09-21, pre-compaction)
- Read frozen Arm A spec, interface/harness specs, battery scripts, B-64
  implementation, R33 sources, prereg §6.
- Verified all 8 r1 corpus hashes against MANIFEST.json (match).
- Wrote a partial (~10KB) draft with an early struct design
  (`led0..led7`, `ck0..ck7` as separate fields, per-file chunking).

### This session (2026-09-21, post-compaction)
- Completed the implementation to ~56KB / ~1,500 lines, reusing the
  prior session's struct and chunk-accessor functions (`led_get`,
  `ck_get`, `a_led`, `read_chunked`, etc.).
- **Bug 1 (M3 panic)**: `read_chunked` stored each file as its own
  chunk, but `cget(abs)` computed `ci = abs / CHUNK_BYTES` assuming a
  contiguous logical space. Multi-file modes (M3, M5, M6, M8) read CODE
  bytes at abs ≥ 5.4MB via ck0 (5.4MB) → "slice index out of bounds".
  Fixed by rewriting `read_chunked` to append files to a single
  contiguous logical space partitioned into CHUNK_BYTES chunks
  (added `ckfill` field tracking the tail-chunk fill).
- **Bug 2 (M8 artifacts)**: `t_m8` wrote artifacts to `outdir` (argv[3])
  but the smoke invocation passed `--perturb` as argv[3]; artifacts went
  nowhere (writes failed silently). Fixed invocation:
  `arm m8-1x <corpus-root> <outdir> [perturbation]`.
- **Bug 3 (M8 JSON)**: `t_m8` emitted no METRIC_JSON. Added JSON with
  recall, ledger entries/bytes, store/ledger chain hashes, perturbation.
- **Harness bug (scorecard)**: `scorecard_assemble.py` hardcodes
  `"arm": "b64"` (line 34). Fixed in the deliverable JSON (set to "a").
  The script is harness-owned; the fix is documented here, not patched
  upstream.

## Verification
- All 15 non-M8 battery legs pass via `run_metric.sh` (each leg runs
  twice, stdout diffed byte-identical): m1-prose, m1-code, m2-t1-prose,
  m2-t1-code, m2-t2-prose, m2-t2-code, m2-t3, m3, m4-prose, m4-code,
  m5-baseline, m5, m6-p2c, m6-c2p, m7.
- M8 gate: 5 perturbations × 2 reruns via `m8_gate.sh` (in progress at
  time of writing; clean/frag/aslr complete with rc=0).
- Memorizer control legs (memctrl-p2c, memctrl-c2p) via prebuilt
  `harness/memorizer/work/build/memorizer_bin`.

## Reproducibility
- Zero RNG in decision paths. All reruns byte-identical (verified by
  `run_metric.sh` double-run diffing).
- Corpus root: `~/workspace/tnn-lab/units/arms/harness/corpora/r1`.
- Commit: source + docs + evidence text only, via
  `~/workspace/commit_to_branch.py tnn-native-lab`.
