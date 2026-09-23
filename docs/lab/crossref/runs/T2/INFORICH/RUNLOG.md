# T2-INFORICH RUNLOG — replacement crew (predecessor killed by 2026-09-23 daemon restart)

Crew: T2-INFORICH (REPLACEMENT), Wave 2 Tier 2, authorized by Micah's 2026-09-22 "run everything" ruling.
Type: C (committed-evidence re-derivation). NO live-web recapture.
Prereg (frozen, authoritative): sylorlabs/TNN branch tnn-native-lab commit
  7b2100d09911c5c10252c5756c7def288e70bd1f, docs/lab/crossref/PREREG_TIER2.md §T2-INFORICH.

## Inherited state
- ~/workspace/scratch-crossref/T2/INFORICH/ contained only: clean/.git (empty, no objects fetched,
  remote=origin https://github.com/sylorlabs/TNN.git) and empty crew/.
- NO predecessor RUNLOG.md or VERDICT.md existed (predecessor was killed mid-clone).
- NOTE: the clean/ dir was later found MISSING entirely (04:15→05:20 UTC); recreated and re-fetched.
  No evidence of predecessor work beyond the empty .git init.
- Action: full fresh clone (filtered, single-commit), no resume of partial state (none was valid).

## Frozen pins (verified via GitHub REST API before any run)
- Frozen prereg commit: 7b2100d09911c5c10252c5756c7def288e70bd1f — EXISTS.
  Commit msg: "crossref: scope + frozen preregs for the cross-reference / clean-environment replication program".
- T2-INFORICH evidence commit (per frozen §T2-INFORICH): 25c2a18b2416e6d1b80d7d11771d3909c9eddee6 — EXISTS.
  Commit msg: "info-source: falsehood detection emerges with information richness" (2026-09-22T02:25:10Z).
- Task instruction named expected pin 23c4fc6ea5a9. VERIFIED MISSING: API returns 422 "No commit found for SHA:
  23c4fc6ea5a9" in sylorlabs/TNN and sylorlabs/zag; no occurrence in any workspace .md or scratch-crossref file.
  DECISION: frozen prereg is AUTHORITATIVE (per task instructions §1). Proceeding on 25c2a18b2416; the
  template-given SHA is recorded as a discrepancy, not a stop condition (the authoritative pin resolves and matches
  the family).
- znc toolchain: /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 — EXISTS (verified on disk).

## Clean-environment setup
- clean/ = fresh git repo, origin=https://github.com/sylorlabs/TNN.git
- `git -c protocol.version=2 fetch --filter=blob:none --depth=1 origin 25c2a18b...` → FETCH_HEAD (fast).
- `git checkout 25c2a18b2416e6d1b80d7d11771d3909c9eddee6 -- docs/lab/info-source` → full info-source tree on disk.
- git fsck: only "dangling commit 25c2a18b..." (expected for a detached single-commit fetch); no corrupt objects.
- TMPDIR=/home/hatch/workspace/tmp_commit (set for all commands). Scratch only; never /tmp.
- Cross-checked: git blob SHAs of PREREG.md/VERDICT.md from checkout match API blob SHAs fetched independently
  (PREREG 9a7fab601867e79076f9ea8e2883ad509b4bd227; VERDICT 3e3dcd6a0f2e6fd78474fd9a7af8990eff13dab0).

## Frozen claims checklist (exact, from frozen PREREG_TIER2.md §T2-INFORICH)
Claims (evidence commit 25c2a18b2416):
  C1. facts-only learner absorbs 12/12 planted falsehoods
  C2. with live web-search sense, read-only installs 0/12, catches 12/12, answers 4/4 unknowns provisionally
  C3. corroboration-gated editable installs 0/12 falsehoods, installs the true value on all 12, answers all 4 unknowns
  C4. corroboration-gated still installs colluding-domain spoofs 2/2 (sensor-deceivable boundary)
  C5. Three axes: parameters→cost, mechanisms→resolve competing claims, information→decides truth.
Method: Type C — re-derive all figures from committed evidence; independent check of the 2/2 colluding-spoof installs.
Rule: REPRODUCED if all figures re-derive; PARTIAL if any axis figure differs (name it).

## Re-derivation work
(see entries below)

## Re-derivation work (2026-09-23 UTC; all times UTC)

- 04:47–05:20 — Pin verification via GitHub REST API: prereg commit 7b2100d0… EXISTS;
  evidence commit 25c2a18b2416e6d1b80d7d11771d3909c9eddee6 EXISTS (msg "info-source:
  falsehood detection emerges with information richness"). Template pin 23c4fc6ea5a9:
  422 "No commit found" in sylorlabs/TNN and sylorlabs/zag; no workspace occurrence.
  Decision: proceed on the authoritative frozen-prereg pin; discrepancy recorded.
- 05:20 — clean/ dir found missing (was present 04:15); recreated: git init, filtered
  single-commit fetch (fast, ~8s), checkout of docs/lab/info-source at 25c2a18b2416.
  git fsck clean. Blob SHAs of PREREG.md/VERDICT.md from checkout match API blob SHAs.
- 05:30 — Read frozen PREREG.md + VERDICT.md + gen_is.py + is_trial.zag + ws2_sense.zag
  (ws_decide/ws_add_result semantics) from the clean checkout.
- 05:40 — Rebuilt is_trial.zag from committed source with pinned znc
  (znc_linux_x86_64_abed8aa1; warnings only: 9× L0012 string-buffer-leak lints).
  Binary: crew/is_trial_rebuild (scratch, never committed).
- 05:42 — Ran rebuilt trial: `all` 3× → sha256 cda86333df6d83b79e6da671227ce64045bd2cacab2fb1b27322bf8f698a0a81,
  byte-identical to committed runs/run_1..5.txt and to the hash in SHA256SUMS/VERDICT.md.
  Per-arm 3× each: R0 af63c7e0…73862, R1 2fe7843e…0c89d2, R2 fc57de6b…0510ca — all match
  committed arm hashes; exit 0 on every run (all per-case assertions passed, incl. R1
  install-refusal rc==8 and R2 stored==V).
- 05:45 — Wrote crew/extract_indep.py (glue: parse is_cases.zag, load case table
  programmatically from committed gen_is.py, re-extract answers from live/*.json,
  verify contested/spoof assemblies, tamper-hash spot check, run-log consistency).
  FOUND + FIXED a glue bug: rel-int regex mis-parsed inside quoted text ("299,792" →
  rel=792), silently dropping V-domain results from the verifier's input. Fixed with a
  positional regex; all glue checks then PASS (140 results, 0 extraction mismatches,
  0 hash mismatches, run-log consistent).
- 05:51 — Wrote crew/indep_is.zag from scratch (own helpers, no shared code with the
  artifact): re-implements the frozen decision rule over the 22 cases/140 results,
  derives all claim figures. Fixed 2 Zag compile errors (u8 vs i64 comparison;
  nio_alloc unavailable → `return ""`). Built with pinned znc → crew/indep_is_bin.
- 05:55 — Ran indep_is_bin 3×: byte-identical (e46ee890…fa4aff), exit 0,
  INDEP_VERDICT|PASS. All 10 FIGURE lines OK: r0_absorbed 12/12, r1_catch 12/12,
  r1_installs 0/0, r1_unknown 4/4, r2_false_installed 0/0, r2_true_installed 12/12,
  r2_unknown_installed 4/4, contested 4/4, spoof R1 provisional-wrong 2/2, spoof R2
  installed 2/2. 20/20 CHECK lines agree with CASE_MANIFEST and run logs; SPOOFDOMS
  confirm exactly {spoof-1.example, spoof-2.example} supporting each fiction.
- Observation (not a claim difference): F08/U02 show 7 pre-cap V-domains in the
  manifest but 6 in the mechanism's view — the documented `if(n<6)` cap in
  ws_add_result drops answers.com / periodictable3d.com. Verifier replicates the
  mechanism exactly; prereg premise (≥2) holds either way.
- Kill bars (frozen info-source PREREG §4) applied mechanically: all 7 PASS.
- 06:0x — Wrote VERDICT.md (this verdict: REPRODUCED) + finalized RUNLOG.md.
- Zero RNG used throughout. No live web access. No commits made by this crew.
  Nothing written outside ~/workspace/scratch-crossref/T2/INFORICH/ (+TMPDIR).
