# RUNLOG — T2-SENSESINT evidence recovery (2026-09-24 ~08:06–08:30 PDT)

Crew: SENSESINT evidence-recovery crew (parent task; session persistent).
Work dir: `~/workspace/scratch-crossref/T2/SENSESINT/recovery/` (new; `crew/`
untouched). No commits made. /tmp never used. TMPDIR not needed (no git ops).

## 08:06 — Setup + read prior state
- `ls ~/workspace/scratch-crossref/T2/SENSESINT/` → `clean/`, `crew/`.
- Read `../_wave2_tally/VERDICTS.md` §T2-SENSESINT PARTIAL (confirmed).
- Read `crew/VERDICT.md` (replacement crew + crew-of-record §9 addendum) and
  `crew/RUNLOG.md` in full. Missing items (from §5):
  `senses/web-search/v2/src/gk{1,2,3}_trial.zag` (P0, sizes 5285/6329/4235),
  7× `senses/web-search/internet-trial/evidence/phase1/*.jsonl` (P2, sizes
  11986/11992/11990/11994/472/12687/11989).
- Size mismatches: `kb5.py` 2189→2731, `run_all.py` 4302→5801.
- `ls clean/tnn/` → `.git`, `docs`; `git rev-parse HEAD` →
  `7b2100d09911c5c10252c5756c7def288e70bd1f` (frozen pin intact, checkout
  survived — no vanishing incident this session).
- Created `recovery/` dir.

## 08:08 — Found the GK sources in the worker's workdir
- `ls ~/workspace/grok47/senses/gk-scratch/` →
  PREREG_GK{1,2,3}.md + `gk1_trial.zag` (5285B) + `gk2_trial.zag` (6329B) +
  `gk3_trial.zag` (4235B) + run logs (run1.txt, gk2_run1..3.txt, gk3_r1..r3.txt;
  gk3_run1..3.txt are 0 bytes — superseded by gk3_r*.txt).
  Sizes EXACTLY match the manifest.
- `sha256sum`: gk1 `5ba8401c5fe9e28e0fdd844899be2d81a27a132bfa590cb0de78799b42aa22e3`;
  gk2 `a2e5cf050e05322be9fa5b8e9e84d5b71431ecc8c5d36ef1e8996f23d492152a`;
  gk3 `a0cf18c323f11f515eda9cab71c1765592f381ea110a4f628be40689e23c7511`.
- VERDICT_SHEET.md (frozen commit): §3 "All trials: pure Zag,
  znc_linux_x86_64_abed8aa1, N=3 runs byte-identical (sha256): GK1 `488af9ab…`,
  GK2 `7f351a53…`, GK3 `94575a9a…`." — these are RUN-OUTPUT digests.
- `~/workspace/grok47/senses/gk-src/` → ws2_sense.zag + R33 natives + cl/
  (build substrate for the trials).

## 08:10 — Phase-1 jsonl hunt
- `find ~/workspace/grok47/senses -iname '*blind-solo*'` → nothing.
- Full-workspace find (backgrounded, 71s) →
  `~/workspace/tnn-lab/senses/web-search/internet-trial/evidence/phase1/`:
  ALL 7 jsonl files present:
  blind-solo 11986, captured-solo 11992, corrupt-solo 11990,
  gullible-solo 11994, idle-solo 472, oracle-helper 12687, oracle-solo 11989
  — sizes EXACTLY match the manifest. Dated Sep 21 23:18 (worker run window).
- Copied to `recovery/evidence/phase1/`; sha256s recorded in
  `phase1_sha256.txt` (see VERDICT.md). Line counts 84/84/84/84/8/88/84;
  head shows valid JSON trial-arm records (SESSION_START, PRIOR_LOADED).
- GitHub org code search `blind-solo org:sylorlabs` → total_count 0.

## 08:12 — Substrate integrity check
- `sha256sum clean/tnn/docs/lab/senses/web-search/v2/src/ws2_sense.zag` =
  `sha256sum ~/workspace/grok47/senses/gk-src/ws2_sense.zag` =
  `49a370fda4d575f32efd431e652d769bd3d07828d4bd54c9658d7656c0e4ac0d`.
  Worker substrate byte-identical to frozen committed sense.

## 08:13 — Build (pinned znc, zero source edits)
- Copied substrate + 3 trial sources to `recovery/build/`; recorded source
  sha256s in `src_sha256.txt`.
- `znc_linux_x86_64_abed8aa1 gk1_trial.zag -o gk1` etc. → all built;
  only benign L0012 string-leak warnings. Binaries: gk1 104747B, gk2 109294B,
  gk3 104347B.

## 08:14 — Runs (3× each, deterministic)
- First attempt had a shell typo (`for t` but `$r`) → 3 runs overwrote one
  file each (used for first digest check). Rerun properly:
  `./build/gkN > out/gkN_run{t}.txt` for N=1..3, t=1..3.
- sha256s:
  GK1 runs ×3: `488af9ab375eae17cf65015240fb5c8a2f111ed6ca2eee354778b12b74a0db5c`
  GK2 runs ×3: `7f351a53524d67fdb182357dcbf0215af526a6b70d7f6d66ce008d0c301fdf4b`
  GK3 runs ×3: `94575a9a6c9e4aaa916676b6301a57d643c65f28d51d748f36492ac359814d13`
- Prefixes match recorded headlines `488af9ab…` / `7f351a53…` / `94575a9a…`.
- `cmp` vs worker logs: gk1_run1 ≡ gk-scratch/run1.txt; gk2_run1 ≡
  gk-scratch/gk2_run1.txt; gk3_run1 ≡ gk-scratch/gk3_r1.txt (all clean).
- Kill-bar checks: `GK1|total=7|pass=7`, `GK2|total=8|pass=8`,
  `GK3|total=4|pass=4`; tamper=1 appears only on `GK2-15` (positive control);
  result rows match VERDICT_SHEET §3 (GK1-1/6 R8 refuse; GK1-2..5,7 R7 install;
  GK2-8/9 R8 refuse, GK2-10..13 R7 install, GK2-14/15 R8 refuse; GK3-10/14b R8
  refuse, GK3-10b/14 R7 install).

## 08:16 — Size-mismatch investigation
- Committed kb5.py at frozen commit: API contents → sha `a88e20ca…`, size
  2731; local checkout 2731B. Committed run_all.py: 5801B local.
- `git log --follow -- <both files>` → only `7b2100d0` ("crossref: scope +
  frozen preregs") ever touched them: added in FINAL form at the frozen
  commit. The 2189/4302-byte drafts never reached the repo.
- Local `~/workspace/senses-rematch/kb5.py` (Sep 22 07:19) ≡ committed
  (sha256 `c1209b0e…` both); `run_all.py` (Sep 22 05:22) ≡ committed.
  Conclusion: stale manifest measured pre-final drafts. No corruption.

## 08:18 — Prior recovery commits discovered (via API)
- `GET /repos/sylorlabs/TNN/commits?sha=tnn-native-lab&path=…gk1_trial.zag`
  → `16ddf755fee7ab41765d961f01e0d2a3f0f2c875` (2026-09-23T18:22:39Z):
  "T2-SENSESINT evidence recovery: restore GK1/GK2/GK3 trial sources (3 P0)"
  (restored from `~/workspace/grok47/senses/gk-scratch/`, byte-identical,
  manifest sizes exact; verified per RECOVERY_PREREG.md R1, digests
  re-derived with pinned znc, zero source edits).
- Same query for `…/phase1/blind-solo.jsonl` →
  `c9bd2b210f781eb60bc9ebcaa1a280225a758184` (2026-09-23T18:23:45Z):
  "T2-SENSESINT evidence recovery: restore 7 P2 internet-trial phase1 jsonl"
  (byte sizes exact, all lines parse as valid JSONL).
- Both are ancestors of `tnn-native-lab` HEAD `062b21a0…`
  (`compare/tnn-native-lab...16ddf755` → behind, ahead 0; same for c9bd2b21).
- Branches on sylorlabs/TNN: `fs-gr1, main, r2-7, reorg/phase-0-1,
  tnn-native-lab, wg-freeze`. Code search for basenames on other
  branches/history: 0 hits (commits?path= lists only these two recovery
  commits).

## 08:22 — Independent byte-verification of HEAD blobs
- Fetched all 10 files from `ref=tnn-native-lab` via contents API (base64 →
  `recovery/headcheck/`).
- `sha256sum`: all 3 zags identical to gk-scratch originals (5ba8401c… /
  a2e5cf05… / a0cf18c3…); `cmp` of all 7 jsonl vs tnn-lab originals → OK.
- HEAD sizes: 5285/6329/4235 + 11986/11992/11990/11994/472/12687/11989 —
  all manifest-exact.
- (My independent build used byte-identical sources, so the re-derivation
  covers the HEAD bytes too.)
- RECOVERY_PREREG.md referenced in the GK commit message: not findable via
  code search or at `docs/lab/crossref/` at the recovery commit — treated as
  the prior crew's local doc; my verification does not depend on it.

## 08:25 — Wrote deliverables
- `recovery/VERDICT.md`, `recovery/RUNLOG.md` (this file).
- Note: the shell-typo first run batch (`out/gkN_r.txt`) was superseded by
  the correct 3×3 batch; superseded files removed.

## Incidents / anomalies
- None. `clean/tnn/` remained intact at the frozen commit throughout
  (re-verified via `git rev-parse HEAD` before and after the run). No
  vanishing-directory incident in this session.
- Discovered prior recovery (details above) — this crew's work is an
  independent verification + re-derivation, not the first recovery.
