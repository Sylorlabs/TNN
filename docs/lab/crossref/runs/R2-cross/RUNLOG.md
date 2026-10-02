# R2-CROSS RUNLOG — deliberation ceiling (CEILING-CONFIRMED) cross-check

Crew: R2-CROSS (independent cross-check crew, depth 2)
Program: TNN cross-reference / clean-environment replication (Micah 2026-09-22 "run everything")
Frozen program commit: 7b2100d09911c5c10252c5756c7def288e70bd1f (tnn-native-lab)
Family prereg: docs/lab/crossref/PREREG_TIER1.md §R2 (frozen with SCOPE.md)
Method: Type C (independent re-derivation of ceiling table) + independent Type A (fresh re-run of contradiction battery)

## Environment
- VM: lab VM, Linux x86_64
- znc: /home/hatch/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1
- TMPDIR=/home/hatch/workspace/tmp_commit (never /tmp)
- Clone dir: ~/workspace/scratch-crossref/R2/clean-cross/ (fresh clone, checked out at 7b2100d)
- Run dir: ~/workspace/scratch-crossref/R2/cross/ (this dir)
- Zero RNG policy; all verification in pure Zag (Python glue only for API/SHA bookkeeping)

## Pin freeze (BEFORE any runs)
| Pin role | Expected SHA | Resolved | Status |
|---|---|---|---|
| program/frozen prereg | 7b2100d09911c5c10252c5756c7def288e70bd1f | 7b2100d0 (commit) | OK — verified in fresh clone 2026-09-22 |
| prereg (QB) | 39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b | 39d4ccb6 (commit) | OK — "QB prereg: freeze quality-buying design" |
| synthesis (QB) | 3314fc1fdd6fb45ec4d73169817cc9820ce520a1 | 3314fc1f (commit) | OK — "QB synthesis: quality-per-cost curve" |
| mechanisms impl | b447c367677f | b447c367677f (commit) | OK — "new-mechanisms: implementation, 15 runs, verdict" |
| mechanisms driver+logs | a638d4d56a2e | a638d4d56a2e (commit) | OK — "new-mechanisms: add driver source + 15 run logs" |

## Committed claims under test (PREREG_TIER1 §R2)
Ceiling table (coding / epistemic):
- baseline 18/18 + 59/94
- conflict-driven 18/18 + 59/94
- three-round critique 18/18 + 12/94
- hypothesis competition 18/18 + 59/94
- one-brain phases 18/18 + 58/94
- combined 18/18 + 59/94

Contradiction battery (frozen, from b447c367677f + a638d4d56a2e):
- baseline 12/156 vs hypothesis competition 156/156 vs conflict-driven 156/156
- sub-batteries: 2v1 36/36; 1v1 36/36 withheld; both-partially-right 24/24; temporal 24/24; spoofed 24/24
- conflict-driven: identical decisions (same state digest) at exactly baseline cost (2.000 ops) on quiet facts
- Direction: 2x kept, 4x/8x dropped

---

## Timeline

### 2026-09-22 23:0x UTC — clone strategy
- Full `git clone` of sylorlabs/TNN was progressing at ~2.7 MB/min (172 MB after ~10 min) — too slow for the evidence needed.
- Restarted as partial clone: `git clone --branch tnn-native-lab --filter=blob:none --no-checkout https://github.com/sylorlabs/TNN.git repo` into clean-cross/ — completed in 12 s. Blobs fetched on demand from origin with SHA verification against committed trees. This remains a fresh clone; all evidence anchored to pinned commit SHAs.
- NOTE: observed an unrelated concurrent process (R2-PRIMARY crew, presumably) cloning into ~/workspace/scratch-crossref/R2/clean (different dir). Non-interference maintained: I do not read or touch it.

### Pin freeze verification (from the fresh clone, before any runs)
- 7b2100d09911c5c10252c5756c7def288e70bd1f -> commit (program/frozen prereg) OK
- 39d4ccb6b4ea550dd7e12ac8af863aae59bcc08b -> commit (QB prereg) OK
- 3314fc1fdd6fb45ec4d73169817cc9820ce520a1 -> commit (QB synthesis) OK
- b447c367677ff351f240675293eee445bdb97993 -> commit (mechanisms impl) OK
- a638d4d56a2e24baa2fa64084ed096d2183a9bf8 -> commit (mechanisms driver+logs) OK
- No missing pins. Proceeding (no UNREPLICABLE-AS-IS trigger).
- GitHub API cross-check confirmed same SHAs + commit messages match expected roles.

### Evidence extraction
- `git archive` per pinned commit into cross/evidence/ (blobs fetched on demand; slow promisor fetch, running in background proc_720f2cb78811).

### Evidence extraction (completed 2026-09-22)
- `git archive` promisor fetch stalled; switched to `cross/fetch_evidence.py`: fetched all needed files via GitHub API and independently verified each file's Git blob SHA against the fresh clone's pinned trees.
- Result: **148 files fetched and verified, 0 failures**. Evidence root: `cross/evidence/`; log: `cross/evidence/FETCH_LOG.txt`.
- Read: `docs/lab/crossref/SCOPE.md`, `PREREG_TIER1.md`, `docs/lab/coding/speed-intel/quality-buying/PREREG_QB.md`, `RESULTS_QB.md`, `work_epi/RESULTS_QB_EPI.md`, `work_code/RESULTS_QB_CODE.md`, full `docs/lab/new-mechanisms/` subtree (`a638d4d5`), mechanism markdown (`b447c367677f`).
- Coding calibration note (committed): every arm shows 18 pass + X3 halt-genfail + X4 halt-no-patch over 3 runs; raw JSON contains wall-clock timings so raw bytes differ across reps — the committed determinism claim is on the CANONICAL digest (timings stripped), e.g. D0 `dce739cd95143036d8f162e2bdb40b77c26980f2384df50f48426f80f405c6b9`.

### Type C — independent ceiling-table re-derivation (pure Zag)
- Wrote independent verifier `cross/verify_qb.zag` (fresh code, visibly separate from committed scorer scripts). Built with pinned znc 2026-09-22 → `cross/verify_qb`.
- FIRST BUILD BUG (mine, not evidence): verifier summed all 3 reps (D0 epi 177 not 59) and compared raw coding JSON bytes (timings differ by design). Fixed: per-rep cell values (reps byte-identical → rep value used, 3× consistency asserted); epi determinism = raw byte-identity per category; coding determinism = FNV-1a over JSON with the six documented timing-key lines removed (`ms,time_s,cpu_s,compile_ms,test_ms,diag_ms` — the same set the committed `canonical()` strips). Prototype of the strip cross-checked in Python (glue): all 3 reps byte-identical post-strip per mode, 23–29 KB content retained.
- Rebuilt, ran 3× on `evidence/docs/lab/coding/speed-intel/quality-buying`:
  - `vq_r1.txt`, `vq_r2.txt`, `vq_r3.txt` byte-identical, sha256 `72842605c1be1b8e4b3f679c7aff67724310ae6dd93868e6396709d29d1399dd`.
  - Output: `VERDICT: TABLE_REPRODUCED_CELL_FOR_CELL`
  - D0 epi=59/94 preds=846 code 54/54 hg=3 hn=3 | D1 epi=59/94 preds=951 | D2 epi=12/94 preds=1128 | D3 epi=59/94 preds=1128 | D4 epi=58/94 preds=1128 | D5 epi=59/94 preds=1609 — every cell == committed, determinism IDENT everywhere, SUMMARY/COST cross-checks OK.
- Epistemic raw logs independently confirmed byte-identical across reps via shell SHA (e.g. D0 false r1/r2/r3 all `e1baec43d29125f9ad3c6a07666cea42aed2b2edb2777da658c740fa91069c3c`).

### Type A — independent contradiction-battery re-run (pure Zag)
- Source: `evidence/docs/lab/new-mechanisms/mech_learner.zag` (blob-verified `b6da44ead9e914016fd1410cc0421a659b781ee1`), copied to `cross/typea/` (never modified).
- Spec read: `SPEC.md`, `PREREG.md`, `VERDICT.md`. Battery N=264, kinds 0–7; scored contradiction set = kinds 1–6 = 156 facts. CLI: `mech_learner <baseline|hypcomp|confdepth> <rep>`.
- PREREG doc defect noted: PREREG.md battery table lists kind 5 n=24, but the frozen code (`bat_kind`: f<228 → kind 5 = 12 facts), VERDICT.md (12), and KB-M-TEMPORAL ("kind-5 = 1.0 (12/12)") all agree on 12. Code is authoritative; totals reconcile (264). No amendment needed — the frozen formulas were always 12.
- Fresh build with pinned znc → `cross/typea/mech_learner` (63,385 bytes). sha256 of source `1f05abc38bd187fed3b043d6609fd3d7c8895fa7978ea81073dba7e8de45af3d`. Two analyzer warnings (string-buffer leak in print helper; unused local) — benign, properties of the committed source.
- Ran 3 modes × 5 reps = 15 runs → `cross/typea/runs/`. Result: **5/5 byte-identical per mode; all 15 logs byte-identical to the committed `runs/*.log`** (cmp clean).
- Independent Zag verifier `cross/verify_mech.zag` (fresh code) parses the fresh logs and checks every claim; ran 3× byte-identical (sha256 `52dd72cc354bde48683fd57962c65919415d315d78399377bd9f98670ff78f96`):
  - `VERDICT: MECH_REPRODUCED`
  - baseline: resolve 12/156, k1=0 k2=0 k3=0 k4=0 k6=0, withhold 0, digest `60a7095526fdd054`, quiet 2000 (2.000 ops/fact), total ops 1224
  - hypcomp: resolve 156/156, k1=36 k2=36 k3=24 k4=24 k6=24, withhold 36, digest `1f68e26f32a54bac`, quiet 3000, total 1968
  - confdepth: resolve 156/156, identical kind tallies, withhold 36, digest `1f68e26f32a54bac` (= hypcomp, PARITY), quiet 2000 (= baseline, 1.00×), total 2016
  - kind 0: 96/96 all modes; kind 5: 12/12 all modes; kind 7: 12/12 absorbed all modes (honest limit, as committed).

### znc quirk found during this work (for the record)
- `(ptr as []u8)` (pointer→slice cast) yields a ZERO-LENGTH slice in this znc build; indexing the re-sliced result segfaults. Proven minimal reproducer 2026-09-22. The committed `m_alloc` pattern — `let b:[]u8=p[0..n]` (pointer-range indexing) — is correct; `_zag_slice_ptr` is the correct slice→pointer builtin. Both verifiers use only the safe patterns. (Candidate ZNC-2026-09-22-016, unconfirmed beyond the reproducer.)

## Final mechanical verdict
- **Type C: TABLE_REPRODUCED_CELL_FOR_CELL** — all 6 modes, coding 18/18 each, epistemic 59/59/12/59/58/59 per 94, predicate totals 846/951/1128/1128/1128/1609, determinism confirmed.
- **Type A: MECH_REPRODUCED** — fresh build + 15 runs reproduce every committed byte; baseline 12/156, hypcomp 156/156, confdepth 156/156; confdepth parity digest `1f68e26f32a54bac` == hypcomp; confdepth quiet cost 2.000 ops/fact == baseline.
- **R2-CROSS verdict: REPRODUCED.** No scientific divergences. One prereg documentation defect (kind-5 n=24 vs 12) noted; frozen code and verdict self-consistent at 12.
- Deliverables: `cross/VERDICT.md`, `cross/RUNLOG.md` (this file). Binaries (`verify_qb`, `verify_mech`, `typea/mech_learner`) and `.zagd` kept in scratch only, never committed.
