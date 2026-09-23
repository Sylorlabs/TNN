# T2-RSI1 RUNLOG — REPLACEMENT CREW (T2-RSI1)

## 2026-09-22 21:37 PDT — crew start
- Replacement crew dispatched: predecessor was killed by a runtime daemon restart (no live runtime handle).
- Inherited state: ~/workspace/scratch-crossref/T2/RSI1/ contained only empty clean/ and crew/ dirs — no partial VERDICT.md/RUNLOG.md from predecessor. Nothing to resume; starting fresh. (Recorded per resume rule: nothing valid to inherit.)
- House rules noted: ~/AGENTS.md read; TMPDIR=/home/hatch/workspace/tmp_commit set.
- Frozen pins expected: prereg `50e7dd97`, verdict `b5501a3ea2bb`; prereg commit 7b2100d09911c5c10252c5756c7def288e70bd1f on branch tnn-native-lab.
- znc: /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (per task).

## Frozen prereg section extracted
- Fetched docs/lab/crossref/PREREG_TIER2.md at frozen commit via gh-api (API-verified, blob sha b1178370036bffbda6eb68ea0989c0e427dc31b7, 38417 bytes).
- T2-RSI1 section found at line 101 of PREREG_TIER2_FROZEN.md — quoted in VERDICT.md. Decision rule confirmed: REPRODUCED iff all 3 fixes reproduce exactly, all 3 traps refused, negative control recommends the traps, 5/5 byte-identical; NOT REPRODUCED if any trap accepted with the screen on.

## 2026-09-22 ~22:00 PDT — frozen pins verified (all via gh-api)
- prereg pin 50e7dd97 → commit exists; added docs/lab/rsi/PREREG.md ("rsi: frozen prereg — recursive self-improvement trial").
- verdict pin b5501a3ea2bb → commit exists; 12 files: SHA256SUMS, VERDICT.md, rsi.zag, verify_rsi.py, runs/{base_r0..r4,var_dense,var_domain3,var_prin}.log.
- frozen trial commit 7b2100d09911c5c10252c5756c7def288e70bd1f → exists ("crossref: scope + frozen preregs").
- No STOP condition: pins present, none missing.

## Clean-environment note (provenance deviation, recorded)
- git clone/fetch of tnn-native-lab timed out twice (repo ~1GB; git-remote-https died of signal 9 mid-fetch). 
- Fallback: fetched the exact committed blobs via gh-api at ref 7b2100d09911c5c10252c5756c7def288e70bd1f (contents API), then hash-verified against the committed docs/lab/rsi/SHA256SUMS:
  - rsi.zag → sha256 9ec75ae2ec54f7d9704a8e188e9c77a64717762e765eff68ae0669ac6380dca7 ✓ (blob c791bcbe513369fd453d8832fb84a79cb5adb0e7)
  - verify_rsi.py → 8d6816aa6effb1c6360ec50a46c6fe320ad48baeac253e8f38379e1d8661c923 ✓
  - PREREG.md → 8523ef4f67107f2a74f4640d35c712fc58cafc571c02c66c5628302828951faa ✓
- rsi.zag is self-contained (482 lines, zero @imports) — full tree not required for this rerun. This is a provenance note, not a gap: every byte built was hash-matched to the frozen commit.

## Build
- znc /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 present (8,337,204 bytes).
- Build cmd (per source header): `znc_linux_x86_64_abed8aa1 rsi.zag -o rsi --no-analyze` → ok, native binary 55,849 bytes. Rebuilt from source; no .zagd/binaries committed.
- Source scan for RNG: no rand/urandom/srand/seed/_zag_time//dev tokens — zero RNG confirmed by inspection.
- Negative control: `sed 's/let CMASK:i32=31;/let CMASK:i32=0;/' rsi.zag > rsi_nogate.zag` (constitution screen zeroed, per verdict's build note), same znc build.

## Runs (all in ~/workspace/scratch-crossref/T2/RSI1/clean/)
- base: ./rsi base 0..4 → runs/base_r0..r4.log; all 5 sha256 = 9bbcf87dc5d1eedb16dd2654e982bf4c5b36192fc4b8825c790131ff00c6b9d8 — MATCHES frozen SHA256SUMS (5/5 byte-identical to the original crew's committed logs).
- variants: ./rsi dense 0 / prin 0 / domain3 0 → sha256 matches frozen SHA256SUMS exactly:
  - var_dense 3708203e0ddb9053d4981dd3b413b78a9626b758676833e0015c499100b166ce ✓
  - var_domain3 fafdfbdd51985bc42fcf6f87d57c069375eaa76b06765489794d39f6128aeb33 ✓
  - var_prin 747f26d1eea0b42e4aa722732a310e5d0b63c61b74311810f03a36ab3117a7c6 ✓
- extra determinism: 2 additional runs per variant (3/3 identical each); negative control 2/2 identical.
- negative control: ./rsi_nogate base 0 → 3 NEGCONTROL RECs (templates 5,6,7), 0 RSI_REFUSED lines.

## Oracle
- Frozen verify_rsi.py (sha256-verified) run against clean/runs/ → OVERALL: PASS (KB1..KB5 all PASS; diagnosis hit rate 3/3).
- TMPDIR=/home/hatch/workspace/tmp_commit used throughout; all work in ~/workspace/scratch-crossref (never /tmp). No interference with live workstreams.
