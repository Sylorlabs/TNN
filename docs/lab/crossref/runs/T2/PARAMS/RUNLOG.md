# T2-PARAMS replication — RUNLOG (replacement crew)

## 2026-09-22 21:38 PDT — dispatch
- Spawned as T2-PARAMS (REPLACEMENT); predecessor killed mid-run by daemon restart.
- Predecessor state found: `~/workspace/scratch-crossref/T2/PARAMS/clean/repo/` was an empty `git init` (no commits); `clean/` dir listing otherwise empty; `crew/` did not exist. Integrity check: nothing valid to resume (no VERDICT.md/RUNLOG.md partials anywhere under PARAMS). Recorded as INHERITED: empty dir structure only. Re-cloned from scratch per rule 2 (nothing valid to resume).
- Frozen prereg section (T2-PARAMS) read from local tree copy `~/workspace/tnn-lab/crossref/PREREG_TIER2.md` (pending verification against frozen commit 7b2100d09911c5c10252c5756c7def288e70bd1f once clone lands).
- Evidence pin `ccbb3d3c39d7` API-verified: full SHA ccbb3d3c39d70924c8e2e2463cb5fb7057f19616, message "Parameter scaling: capacity params at fixed 24k facts / 19 configs x reps (59 runs), pure Zag, byte-identical within config. / Finding: architecture is parameter-insensitive above the capacity floor - 16/19 configs produce byte-identical learners (digest 8e6238911bb7cef0); ...".
- Cloning sylorlabs/TNN branch tnn-native-lab (shallow, depth 50) into clean/repo/.

## 2026-09-22 ~22:00 PDT — clean checkout + pins frozen
- Environment: could not git-clone (network too slow: 70M in 20 min, then tarball killed at 756M/unknown-full). Clean checkout assembled as tree at pinned commit instead:
  - `docs/lab/scale/params/` (PARAM_PREREG.md, PARAM_VERDICT.md, driver/{param_learner.zag, run_params.sh, analyze.py}, runs/*.log ×59) fetched per-file from raw.githubusercontent.com at pinned SHA ccbb3d3c39d70924c8e2e2463cb5fb7057f19616.
  - `docs/lab/crossref/PREREG_TIER2.md` fetched at frozen SHA 7b2100d09911c5c10252c5756c7def288e70bd1f → byte-identical to local tree copy (diff clean).
- Frozen pins: crossref prereg 7b2100d09911c5c10252c5756c7def288e70bd1f; params evidence ccbb3d3c39d70924c8e2e2463cb5fb7057f19616. EXPECTED ccbb3d3c39d7 PRESENT ✓ (not UNREPLICABLE-AS-IS).
- Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (sha256 498abcb5…, znc 2026.07.0-dev). Built param_learner from source, no .zagd/binary copies.
- Corpus: ~/workspace/scale/corpus/texts (frozen Gutenberg texts + .tnix + meta.json), read-only; my runs read it, never wrote.
- FIDELITY GATE: base config log BYTE-IDENTICAL to committed runs/base_r0.log (diff clean). Digest 8e6238911bb7cef0, mastery 22841/22841, flaw 96/96, absorption 1159/1159, ops 4.000, 202 B/fact — all match.

## Sweep launched ~22:01 PDT — 19 configs (5 base + 3×18), 2-way parallel

## Sweep complete ~22:14 PDT — 59/59 runs, all det=OK
- Per-config digests: slot025 0a6e548f2dae51dc, base 8e6238911bb7cef0, slot05 9175b7e1f4d24d46, all others 8e6238911bb7cef0 except jsmall = slot05 digest. Matches committed exactly.
- diff of my 59 run logs vs committed runs/*.log: 0/59 differ (byte-identical evidence).
- Summary: mastery/absorption/flaw/ops/B-per-fact all match PARAM_VERDICT.md table cell-for-cell (see runs/summary.tsv).
- Independent grace-bar check: slot025/slot05 deciles show clean prefix cut at exactly the slot cap (5708+292=6000; 11414+586=12000), every stored fact mastered — capacity drops, never corrupts.
- Driver blob SHA da15b9b797b5df715663c738e2adda8d0a6d6662 matches pinned commit blob.
- VERDICT.md written: REPRODUCED.
