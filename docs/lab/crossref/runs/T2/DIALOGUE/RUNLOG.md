# RUNLOG — T2-DIALOGUE replication crew

Wave 2 (Tier 2) cross-reference program. Authorized by Micah's 2026-09-22 "run everything" ruling.
Crew: T2-DIALOGUE. Replication type: A (rerun dialogue battery from committed sources in clean checkout).

## Timeline

### 2026-09-22 21:05 PDT — crew start
- Checked memory: prior state confirms the claimed result (dialogue rebuild/rerun passed 370/370
  byte-identically, new digest beginning `35aaae8a`; frozen verdict stale, needs re-freeze/amendment).
- Created run dirs: `~/workspace/scratch-crossref/T2/DIALOGUE/clean/` (fresh clone) and
  `~/workspace/scratch-crossref/T2/DIALOGUE/crew/` (run dir, deliverables).
- Set `TMPDIR=/home/hatch/workspace/tmp_commit` (scratch only, never /tmp).

### 21:06–21:20 — clone attempts
- First plain `git clone` hung: interactive credential prompt with no tty.
- Retry with `GIT_TERMINAL_PROMPT=0 </dev/null` exited 0 but left no repo dir (tail captured exit).
- `git ls-remote https://github.com/sylorlabs/TNN.git HEAD` works unauthenticated → repo readable
  without auth; remote HEAD = `dbabd53e9ef0266f56a26bda217ac2acb4fc84bc`.
- Shallow `--depth 50` clone downloaded ~92M then its session died with no refs written.
- Fresh attempt: `git init` + `git fetch --depth 1 origin 7b2100d09911c5c10252c5756c7def288e70bd1f`
  → git-remote-https died of signal 9 (~87M downloaded, early EOF). VM memory pressured
  (8GB, sibling crews cloning concurrently).
- Switched to blob-filtered fetch: `git fetch --filter=blob:none --depth 1 origin
  7b2100d09911c5c10252c5756c7def288e70bd1f` → SUCCESS, 1.2M, commit object present.
- Sparse checkout `docs/lab/dialogue/` + `docs/lab/crossref/` at
  `7b2100d09911c5c10252c5756c7def288e70bd1f`. `git rev-parse HEAD` confirms.
- (Note: a daemon/service restart hit one exec mid-run; workspace state verified intact.)

### 21:20–21:45 — prereg read + pin freeze (from the fresh clone, cross-checked vs GitHub API)
- Read `docs/lab/crossref/SCOPE.md` (blob `dd4d3c67be4132063b2163c033bddbc1786ae14e`)
  and `PREREG_TIER2.md` T2-DIALOGUE section (blob `b1178370036bffbda6eb68ea0989c0e427dc31b7`)
  from the clone; both match the API-at-ref copies byte-for-byte.
- Claim: 370/370 byte-identical, digest `35aaae8a…`. Rule: REPRODUCED iff count=370/370
  AND digest prefix `35aaae8a`; NOT REPRODUCED if either differs.
- Key evidence locations found: `docs/lab/dialogue/` (battery + source + oracle),
  `docs/lab/dialogue/morphology/` (REPRO/FIX/VERDICT + `runs/full_1..5.log`),
  morphology VERDICT addendum digest `35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b`.
- Frozen pins recorded BEFORE running (see VERDICT.md pin table): dialogue.zag blob
  `964b2bc2bd9c186bbd7efab56f9e68a231eb2c8d` (post-fix: `irregular_norm` present),
  battery.txt `bf313e616122b9170ff4588883da7274f8352af9`, kb.txt `68c86046277ecaf0b358bad30f474692d508d381`,
  gaz.txt `f09ec9c61403524bd7fbf6ef2de8305401e29dac`, oracle `c8bfae5f2db69851b79d3d7884df9dd6f657de9f`,
  full_1..5.log blob `e60435c123f6f739ec998a1691e389b107ad0717`,
  SHA256 substrate `src/experiments/R33_NATIVE_SHA256_V2.zag` blob `5dd858fa1097451ee6164c015993fd5a434877db`,
  IO substrate `docs/lab/prose-learning/src/R33_NATIVE_IO_V1.zag` blob `a6b440d256437de5e34faa77a0d73079e2755375`
  (Linux x86-64 port; the `src/experiments` IO copy is the macOS/Darwin build — unusable here;
  Linux port is byte-identical to the substrate in the original build dir and toolchain dir),
  znc `2026.07.0-dev (edition 2026)` sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.

### 21:45–21:55 — build from source
- Build dir `crew/build/` staged with frozen sources (dialogue.zag, kb.txt, gaz.txt,
  battery.txt, both substrate files from pinned commits).
- First build failed: `@import cannot read 'R33_NATIVE_IO_V1.zag'` (the SHA256 substrate
  imports it; per AGENTS.md the substrate files must sit next to the build cwd).
  Resolved with the committed Linux-port copy (see pins).
- `znc dialogue.zag --no-zagd --no-analyze --no-foreground-cache -o dialogue_bin`
  → `znc: wrote native binary dialogue_bin (260655 bytes main, 0 external tools)`, rc=0.
  Binary sha256 `912c809e0d8206f5ceb096d79a54e735337180f5dccc8bded6f1d25a7c023bd5`
  (scratch only, never committed).

### 21:55 — five battery runs
- 5 runs of the frozen `battery.txt` (cwd = build dir), rc=0 each.
- All 5 logs byte-identical: sha256 `33743aead2f6457dce48653df1eff28e91cbf165208839ab86fad0e8c4bbb372` ×5.
- `cmp` clean against committed `docs/lab/dialogue/morphology/runs/full_1.log`.
- `DIGEST 35aaae8ac1bbf764d1f710403a9302ad1f4f9b5327c9b13793cd90299834474b`
  — exact match to the claimed digest.
- SECTION totals: FOLLOWUP 45/45, CORRECTION 45/45, REFERENT 60/60, WEIRD 30/30,
  WEIRD_CLEAN 30/30, TOPIC 60/60, CONTRADICT 72/72, COMPOSE 28/28 = **370/370**.

### 21:56 — independent oracle verification
- Committed `verify_dialogue.py battery.txt run_rep_1.log kb.txt`:
  8/8 sections 100%, 10/10 COMPOSE-NOVEL outputs not verbatim KB facts,
  weird-style gap 0.0pp, **0 errors**, rc=0.

### Verdict: REPRODUCED (2026-09-22/23 PDT)
- 370/370 ✓ · 5/5 byte-identical ✓ · digest `35aaae8a…` exact ✓ ·
  byte-identical to committed logs ✓ · oracle 0 errors ✓.
- Notes: stale `SHA256SUMS` (old dialogue.zag hash + old `f07f26cf…` log digest)
  is consistent with the prereg's recorded staleness, not re-litigated;
  IO-substrate pin must name the Linux-port path explicitly in future pins.
- Deliverables: `VERDICT.md` + this `RUNLOG.md` in
  `~/workspace/scratch-crossref/T2/DIALOGUE/crew/`.
