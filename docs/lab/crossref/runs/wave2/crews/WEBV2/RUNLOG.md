# T2-WEBV2 replication — RUNLOG

Crew session: T2-WEBV2 (depth 2/2 subagent), 2026-09-22 ~21:03–21:35 PDT.
Type C replication of "web-search sense v2: live web works" (commit ff97c7a08fcb).

## Environment setup

- 21:03 — task received. Created `~/workspace/scratch-crossref/T2/WEBV2/crew/`
  and `.../clean/`. `TMPDIR=/home/hatch/workspace/tmp_commit` created.
- 21:05 — full `git clone` of sylorlabs/TNN too slow (74 MB in 8 min; parallel
  sibling-crew clones saturating bandwidth). Killed it.
- 21:08 — retried with `--branch tnn-native-lab --single-branch --shallow-since=2026-09-10`;
  the exec dispatch timed out (other crews' full clones still saturating the link).
- 21:12 — switched to partial clone: `--depth 1 --filter=blob:none --no-checkout`
  (14 s). Then `git fetch --deepen 100` loop; pin `ff97c7a08fcb` resolved at ~400
  depth. This is still a fresh clone of the branch; only transfer volume was reduced.
- 21:18 — evidence paths checked out at `ff97c7a08fcb`:
  `docs/lab/senses/web-search/v2/{PREREG.md,VERDICT.md,runs,live,transport,src}`.
  Crossref docs checked out at frozen prereg `7b2100d09911c5c10252c5756c7def288e70bd1f`.
- 21:20 — pins frozen (SHAs in VERDICT.md). `git diff` against both pins:
  every read file byte-matches its pin (0 diff lines for evidence; 0 for crossref docs).

## Evidence review (committed record)

- Read `PREREG.md` (frozen 2026-09-21 + amendment A1), `VERDICT.md`, all 36 run
  logs in `runs/20260922_020800/`, `hash_manifest.txt`, `TRANSPORT_PROBE.md`,
  `probe_results.json`, `reprobe_results.json`, `LIVE_SMOKE.json`, 21 `live/` envelopes.
- Decoded run-log schema: legs A/B/C `L1|K#|G#|D#|A<ans>|H<hash>|T0|M1`,
  leg D `D|G#|G<gate>|E<exp>`, legs M/R `I|M#|R<res>|E<exp>|NI<n>|H...` /
  `O|M12|R#|E#` + `MC|M#|mode#|rule#|P#`, leg S `S|d1..d4|transports=#`.
  Dispositions per committed sense code: 0 NO_SEARCH, 1 PROVISIONAL,
  2 WITHHOLD, 4 HOLD_INSTALLED, 5 catch (C-leg), 6 PROVISIONAL_MAJORITY,
  7 INSTALLED, 8 INSTALL_REFUSED.
- Key finding during review: neither probe JSON contains a lumy.live endpoint —
  the "10/10 probe bar" is asserted in TRANSPORT_PROBE.md's prose table only.
  Machine evidence for lumy working: 21/21 envelopes + smoke, all ≥6 usable results.

## Independent verifier (this crew's code)

- Wrote `crew/verify/verify_webv2.zag` (~560 lines, pure Zag, zero RNG): parses
  every run log line-by-line, re-derives all leg counts and the M/R outcome
  matrices from the line records (not the SUMMARY lines, which are asserted
  separately), byte-compares all 5 replay files per leg, recomputes sha256
  digests vs the manifest, checks mode-1 zero-install, checks the lumy envelopes.
- Uses only the pinned substrate sources (`R33_NATIVE_IO_V1.zag`,
  `R33_NATIVE_SHA256_V2.zag`) copied from the evidence commit — no original-crew
  verifier logic reused.
- Build: pinned `znc_linux_x86_64_abed8aa1`, warnings only, no errors.
- First build had a bug: run filenames built as `A_run1.txt` instead of
  `legA_run1.txt` (caught by the verifier itself: identical5=0, empty sha).
  Fixed, rebuilt.
- Ran 3×: all exit 0, byte-identical stdout
  (sha256 `6e192508db0ffce31c42e28c81f365a7d6f1848b6fe1d5f8aecbeb2663348bba`).

## Results

- All 15 re-derivation checks PASS (see VERDICT.md table).
- Determinism: 5/5 byte-identical per leg for all 7 legs; manifest 7/7 digest match.
- Mode-1 install ops: 0 (12/12 legM mode1 rows NI0/R8; legs A/B/C `installs=0`;
  no D7 anywhere; cross-checked with an independent sequencing pass).
- R-CORR/R-CONTRA separation holds exactly as committed; unanimous-spoof
  residual is exactly M5/M6 under both rules.
- Probe caveat documented in VERDICT.md (prose-only 10/10; operational bar
  corroborated 22/22 by machine evidence).

## Non-interference

Read only committed evidence. No live web requests. No live-workstream files
or processes touched. Scratch confined to `~/workspace/scratch-crossref/T2/WEBV2/`.
No binaries or .zagd committed anywhere (the `verify_webv2` binary and
`probe` binary live only in crew scratch, never in the repo).

## Deliverables

- `crew/VERDICT.md`, `crew/RUNLOG.md` (this file)
- `crew/verify/verify_webv2.zag`, `crew/verify/run{1,2,3}.out`
- Clean checkout retained at `~/workspace/scratch-crossref/T2/WEBV2/clean/`
  (evidence at ff97c7a08fcb, crossref docs at 7b2100d0).
