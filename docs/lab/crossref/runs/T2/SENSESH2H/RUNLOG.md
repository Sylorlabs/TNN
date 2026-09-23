# T2-SENSESH2H — RUNLOG (replacement crew, T2-SENSESH2H)

Crew: T2-SENSESH2H (REPLACEMENT — predecessor killed mid-run by runtime daemon restart, 2026-09-23).
Authorization: Micah's 2026-09-22 "run everything" ruling; TNN cross-reference program, Wave 2 (Tier 2).
Type A: full rerun from committed sources in a clean checkout.

## Inherited state (2026-09-23 ~04:05–04:30 PDT)

- `clean/repo/`: git clone of sylorlabs/TNN (blob:none partial clone) created by predecessor at 04:29, HEAD detached at
  `84df6dc244836848decdf3d76d9796cd60f91269` (matches freeze pin `84df6dc24483`). `git fsck --no-dangling`: CLEAN (no errors).
  `git status`: clean. Remote: https://github.com/sylorlabs/TNN.git.
- Predecessor had set a SPARSE checkout limited to `/docs/lab/crossref/` (working tree had "1% of tracked files").
  Frozen prereg commit `7b2100d09911c5c10252c5756c7def288e70bd1f` verified present as a commit object in the local store.
- No RUNLOG.md / VERDICT.md from predecessor existed in `crew/` (empty dir) — no partial results to resume; full fresh rerun.
- Action taken (2026-09-23, replacement crew): disabled sparse checkout, `git checkout -f 84df6dc...` to materialize the
  full tree for the Type A rerun. Frozen prereg section extracted via `git show 7b2100d...:docs/lab/crossref/PREREG_TIER2.md`
  (not transcribed from memory).

## Pins (frozen BEFORE any run)

- Frozen prereg commit: `7b2100d09911c5c10252c5756c7def288e70bd1f` (branch tnn-native-lab)
- Trial/claim commit (pin): `84df6dc244836848decdf3d76d9796cd60f91269` — detached HEAD, status clean, fsck clean
- znc: `/home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- TMPDIR=/home/hatch/workspace/tmp_commit (never /tmp)

## Run plan

1. Materialize full checkout at 84df6dc (backgrounded).
2. Build A (`a_raw/sense.zag`) and B (`b_percept/sense.zag`) from source with frozen build flags
   `znc <src> --no-zagd --no-analyze --no-foreground-cache -o <bin>` into crew scratch (NOT into the repo tree).
   Boundary proof: `znc check b_percept/percept.zag ...` standalone.
3. Generate fixtures via `harness/gen.py` (master seed 20260921; 170 photos from picsum.photos per FIXTURE_SOURCES.md),
   verify every fixture against committed `harness/fixtures/MANIFEST.sha256`.
4. `run.py --no-wait` with SENSE_A/SENSE_B → results; `score.py` → metrics.json. Compare vs committed metrics.json.
5. ≥3 full pipeline runs byte-identical (raw_results.json SHA-256 match), plus the runner's own KB5 sample (60 fixtures × 3 runs).
6. Write VERDICT.md with the frozen claims checklist quoted verbatim, every figure measured vs claimed, decision rule applied.

## Timeline

- 2026-09-23 (replacement crew start): extracted frozen prereg section; verified clone integrity; began full checkout.
- 2026-09-23 ~05:21: full-tree checkout FAILED — git-remote-https SIGKILLed (signal 9, OOM) during blob fetch
  ("fetch-pack: invalid index-pack output"); the entire clean/repo dir was found DELETED at 05:21 (cause undetermined;
  no crew command deletes it; disk has 68G free). Recorded as an environment incident.
- Recovery: fresh `git clone --no-checkout --filter=blob:none`, sparse checkout limited to `docs/lab/senses/rebuild/`
  (all 22 committed files present), `git checkout 84df6dc244836848decdf3d76d9796cd60f91269` OK; `git status` clean,
  `git fsck --no-dangling` clean. Frozen prereg commit 7b2100d... present as commit object.
- Builds (frozen flags `znc <src> --no-zagd --no-analyze --no-foreground-cache -o <bin>`, cwd=mirror dirs with
  byte-verified source copies — mirrors verified sha256 == committed sources):
  - A: `sense_a`, 88191 bytes main — EXACT size match to BUILD_LOG ("wrote native binary sense (88191 bytes main)")
  - B: `sense_b`, 94129 bytes main, 101807 bytes on disk, md5 e6c98d091bbb0f90f54936b46bf849d8 — EXACT md5 match to
    B BUILD_LOG record. Boundary proof `znc check percept.zag` → "OK — all capability claims proven".
  - Rebuilds of both binaries byte-identical (deterministic compiler confirmed).
  - Note: B's `../../tnn-lab/toolchain/R33_NATIVE_IO_V1.zag` import resolved against a mirror of the committed
    `a_raw/R33_NATIVE_IO_V1.zag`, which is byte-identical to the live toolchain file the original crew used.
- Fixture generation: gen.py running in crew/harness (photos from picsum.photos/seed/tnnsr<i>).
- PHOTO FINDING (recorded, not hidden): gen.py's `fetch_photos` rejects payloads <= 2000 bytes. 6 seeds
  (tnnsr28/81/97/107/148/153) serve small-but-valid JPEGs (1236–1906 bytes) from picsum; the initial run crashed on
  missing ph153.jpg. Downloaded each directly (JPEG-magic validated), and EVERY ONE hashes EXACTLY to the committed
  `fixtures/MANIFEST.sha256` entry (e.g. ph153 = 5f994f5e19d67605f8ad309541d0bfadd69eff8ce5af3888794c93935a77bfb2).
  All 170 photos now match the manifest. The 2000-byte guard is simply over-strict for these 6 seeds; the bytes are
  the original ones. No fixture drift from photo sources.
- Fixture regeneration VERIFIED: all 2020 MANIFEST.sha256 entries OK (925 fixtures + 925 truths + 170 photos
  byte-identical to the original run). End-to-end regeneration — which the original VERDICT noted was "not re-verified
  in this run" — now IS verified.
- Pipeline run 1 launched: run.py --no-wait with SENSE_A/SENSE_B (1850 fixture runs + 360 determinism runs).
- Run 1 COMPLETE: 1849 runs, 1 error (the KNOWN p042.img task_failed — same as original run's honest caveat); determinism
  A 60/60, B 60/60. score.py: A 72.6389% / B 54.0278% / Δ18.6pp / A adv-FIR 58.96% (79/134) / B 54.96% (72/131) /
  ops 1.03B vs 428M — all matching committed metrics.json.
- metrics.json deep-compare vs committed: ZERO mismatches (field-by-field, float-exact).
- Run 2 COMPLETE: byte-identical to run 1 (raw_results.json aa91f3a1... == run 1).
- Run 3 launched (07:12) but the background session was lost by the runtime (no completion notice, empty log,
  no run.py process — second runtime hiccup this task). Relaunched as run 3b.
- Run 3b COMPLETE (RUN3B_EXIT=0): determinism A 60/60, B 60/60. raw_results.json byte-identical to runs 1+2.
- FINAL: 3 full pipeline runs byte-identical — raw_results.json aa91f3a1af0ee42de5229b93a371c5d8efb5ffd5c99bc8b28398bdefd9a2fc0a ×3;
  metrics.json 1cca93a24c71c471e9cfe24e2a6cc1f48c53e96957e17e7629719221026907ab ×3.
  metrics.json deep-identical to the committed metrics.json (0 mismatches). VERDICT: REPRODUCED.
- Clean checkout left pristine (git status clean, HEAD 84df6dc). No binaries/.zagd committed anywhere; all artifacts in crew/.
