# PAMs v2 red-team — verification evidence

2026-09-23. All commands below were run on the lab VM. Digests are sha256.

## A. Sealed generator / fixture verification

Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`

```
znc rt_gen.zag -o /tmp/rt_verify/rt_gen
/tmp/rt_verify/rt_gen /tmp/rt_regen 0 24
```

- Generator manifest digest (printed by rt_gen):
  `c140013e76c520e3e04ca2f3d4283f56a3e8184cbac01d4e5509ff5fb4f56b9d`
  — matches the expected digest exactly.
- Regenerated `MANIFEST.sha256` byte-identical to
  `senses/pam-rebuild/v2/redteam/fixtures/sealed/MANIFEST.sha256`
  (compared with `cmp`).
- Full recursive comparison of `/tmp/rt_regen` against the landed sealed
  tree (every fixture payload + every `.truth` sidecar + manifest):
  **mismatches = 0**.
- Counts: 288 fixture payloads, 288 `.truth` sidecars, 576 manifest rows,
  577 files total including the manifest. Tree size ~14 MiB.

Conclusion: the sealed fixture set is exactly what the sealed generator
produces. The set is sealed: these notes record hashes and counts, not
contents.

## B. Dual-span trial construction

```
znc rt_trials.zag -o /tmp/rt_attack/bin/rt_trials
rt_trials <sealed_dir> <trials_dir>      # twice, into two dirs
diff -r <trials_dir_1> <trials_dir_2>    # no differences
```

- Trials: 288 `rt4_<FAM>_<NNNN>.r24` (magic `0x41343252`, tcode, F bytes,
  G bytes) + 288 `rt4_<FAM>_<NNNN>.g.<ext>` standalone G-span files +
  288 `.r24.truth` sidecars + `TRIALS.sha256` = 865 files.
- TRIALS manifest digest (sha256 of `TRIALS.sha256` bytes, printed on
  stdout): `319f45e3aaf0f5d38569974b9b027770ac6344bcaa618fd835fdd7737dea6cb0`
- Byte-identical across two independent runs (`diff -r` clean).
- Partner selection: deterministic — smallest indices j != i (scanning
  i+1, i+2, ... with wraparound) sharing the family and the truth label.
  pcm families (PTC/TMB) use two partners concatenated under a rebuilt
  header (sr=16000, n=32000) because frozen `gcheck_pitch`/`gcheck_timbre`
  require exactly 32,000 G samples. F and G evidence are distinct spans
  (no duplication of F bytes).
- Smoke test: `vsense pitchdisc rt4_PTC-4_0000.r24` yields `prog=PASS`
  with the internal G selfcheck agreeing (`agree=1, strong=1`);
  G-as-F re-judgment yields `judgment=HIGHER, confidence=990`.
- One bring-up bug was found and fixed before any scoring: trial truth
  sidecars truncated labels by one char (double-stripped newline). All
  trials were regenerated after the fix; the digest above is post-fix.

## C. Sibling autopsy recomputations

- R2-4 RK-3: recomputed from frozen `evidence/clean/sweep.jsonl` and
  `evidence/clean/gate_dispositions.txt` → denominator **1,102**,
  installed **104** — exact match to the autopsy claim. STRONG instrument.
- R2-10 veto 58/76: **NOT RECOMPUTABLE / prose-only** — no persisted
  grid-search output or candidate-level log found in evidence.
- KB4 mech demo: rebuilt pure-Zag `src/mech_demo.zag`, two runs match each
  other and the recorded output exactly; output sha256
  `eccf38999d434878a865691b16ffc06c150d20c3ac4a4877b67d0936e6a429bd`;
  recomputed MI C2 = 0.0000, C3 = 0.0025, C1 = 1.0000 bits.

## D. Fork build status (corrected survey, 2026-09-23 20:40 UTC — supersedes
the earlier "V2-B/V2-C empty" note from 19:09-19:28 UTC)

- **V2-A**: landed `vsense.zag` fails to build (missing `lut.zag`,
  `gcheck.zag` imports); `vgate_a.zag` builds; `deliberate.zag` builds.
  End-to-end = UNTESTABLE as landed (missing imports); gate-only bar-gaming
  valid.
- **V2-B**: populated — `vsense.zag`, `deliberate.zag`, `lut.zag`,
  `gcheck.zag`, IO/SHA sources. `vsense.zag` is byte-identical to V2-A/R2-4
  and builds cleanly. **No gate source landed** — gate UNTESTABLE (nothing
  to attack); sense performance characterized via the diagnostic build.
- **V2-C**: populated — `vknow.zag`, `memgate.zag`, `test_vknow.zag`,
  `lut.zag`, `gcheck.zag`, IO source. `memgate.zag` does NOT build
  (imports missing `R33_NATIVE_SHA256_V2.zag`) — gate UNTESTABLE.
  `test_vknow.zag` builds; detector sweep (src/rt_vknow.zag driver, Zag,
  zero RNG): **0 fires on all 288 sealed fixtures** — K-CCN-1 is
  dimension-gated to 128x128 images, K-CCN-2 / K-PTC-1 / K-TMB-1 are
  unimplemented stubs returning 0, K-SHP-1's occlusion threshold is met by
  none of the sealed shapes. Per-fixture detector-list digest:
  `ae8a506c47f8cff092a3bf97dc1c5af4710919b8fc4c395317eb346558f2711f`.
- **V2-D**: landed `vsense.zag` fails to build (missing `lut.zag`,
  `gcheck.zag` imports); `vgate_d.zag` builds. End-to-end = UNTESTABLE as
  landed; gate-only bar-gaming valid.
- Temporary dependency-vendored sense binary (scratch dir only, does not
  repair the landed forks): built 19:28 UTC, ran all 576 dual-span sense
  runs (0 failures) — diagnostic evidence only for the attack streams.

## E. Attack pipeline digests (all sha256; run twice, byte-identical)

- Records: clean `82b7b98d33061c859e6bc25f587574f33986869678f25fc621f5cb656ab95a4e`,
  withhold `f980085c7f803695fbf0be551a4027f1c851bd35883b6edca6e8d06edd7b2666`,
  install `c26ac9743b8c079e782cdf8511caf2350f653556ac11ac70dfda03720c17c4ad`,
  decoy `96cd6f07ab88506aea8a2b6a839a599913625928fa34285fb84bcf11af1a752b`.
- Gate score digests: a/clean `96ea5325d95348dde8cb9209c436f9c3600630e109abe9447a1677edf05d5453`,
  a/withhold `7d5f9ec0927eda7ce76558a12c46fd5480f31e64337c8a4de6910d2653cb8616`,
  a/install `181f671b8fe817ba9bada7b64edbd9f4c214f9a40b929fb03c99fbc5f632aac7`,
  a/decoy `876e2ca0a88c8b5a861195c4421ab5038424c93f2f5a8c49d26c2a72eaae62c6`,
  d/clean `3acc8a8933c4212ff5f2f3588437b88d7b113faa9723a706add8288010a3614d`,
  d/withhold `1ccf8336cacd3b4a751f0d6d23f26addf9d5788dafaf648b781a97d8d2f246d0`,
  d/install `c674cde41745b7a75d0bb63af34ab0dbbbc7bd66529560dcfa762731ecd74396`,
  d/decoy `2cb9ba5480a9bb9964a1572c8c11d231b5ad7af8f7d9603284c45a6ee83534f5`.
- Ledger verification: all 8 ledgers hash-chain-valid (genesis 32 zero
  bytes; each link sha256(prev_raw32 || canonical)); disposition counts in
  each ledger match its gate stdout exactly. Verifier:
  Python glue `verify_ledger.py` (orchestration only).
- Run 2 (2026-09-23 20:31–20:41 UTC): sense sweep, records, gate runs, and
  scores all byte-identical to run 1 (every digest above matches).
