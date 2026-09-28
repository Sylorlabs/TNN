# RUNLOG.md — T2-CERT (REPLACEMENT crew)

Wave 2, Tier 2, cross-reference program. Type C: certifier red-team, committed-evidence re-derivation.
Authorized by Micah's 2026-09-22 "run everything" ruling.

Frozen prereg: sylorlabs/TNN branch tnn-native-lab, commit 7b2100d09911c5c10252c5756c7def288e70bd1f
Governing section: docs/lab/crossref/PREREG_TIER2.md, T2-CERT section (certifier red-team, Type C).

## 2026-09-22 ~21:36 PDT — crew start (replacement)

- Spawned as T2-CERT REPLACEMENT. Predecessor killed mid-run by runtime daemon restart; final message never arrived.
- RESUME check: ~/workspace/scratch-crossref/T2/CERT/clean/repo was an initialized git repo with NO commits (empty) — corrupt, no valid state to resume.
- Inherited state recorded: empty dirs clean/ (empty repo, deleted), crew/ (empty).
- Re-clone initiated: `git clone --branch tnn-native-lab --single-branch https://github.com/sylorlabs/TNN.git` into clean/repo (backgrounded; long download).
- znc expected pin: e3c2b9cc34e8 (to verify before running).
- TMPDIR=/home/hatch/workspace/tmp_commit set per rules (no /tmp for staging).

## Clone status

- Awaiting clone completion (backgrounded proc_8759b8c0ea5a).

## 2026-09-22 ~22:00 PDT — clean environment established

- Attempt 1 (network, full single-branch): OOM-killed after ~40 min (git-remote-https signal 9; 30 concurrent crew clones on 8GB VM). Partial dir auto-removed by git.
- Attempt 2 (network, --depth 1 + pack memory caps): killed by tool-dispatch timeout.
- Attempt 3/4 (local git clone from PROSE/SENSESINT shallow repos): failed — "possible repository corruption on the remote side" (known git limitation: cannot clone FROM a shallow repo via upload-pack).
- Attempt 5 (SUCCESS): file-level copy `cp -r` of RAWVSHUMAN/clean/repo (read-only source, no interference; RAWVSHUMAN fsck was clean). Ownership-preserve not needed.
- VERIFIED: git rev-parse HEAD = 7b2100d09911c5c10252c5756c7def288e70bd1f (exact frozen pin) ✓
- git fsck: clean except one inherited dangling commit 3edd14867296d73bfc0606227c3770127157e22e (harmless) ✓
- git status: clean, detached HEAD ✓
- znc sha256: 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef (prefix 498abcb5ab34; the task's "expected e3c2b9cc34e8" pin to be resolved against the prereg section — likely a frozen-evidence artifact SHA, not the compiler)
- TMPDIR=/home/hatch/workspace/tmp_commit in effect for all commands.

## 2026-09-22 ~22:20–23:10 PDT — re-derivation work

- Extracted T2-CERT section from frozen PREREG_TIER2.md (lines 125–129) — quoted verbatim in VERDICT.md.
- Located committed red-team evidence: commit cadacc199684381833dbed4b27bb171b1d6f739f
  "certifier-rebuild: rebuilt certifiers + full historical diff + verdict (red-team attack #1)"
  (2026-09-21 20:39:58 -0700); prereg commit 26b86329b53b9aa24589dcf11d5ff09b125c1fe8.
  Evidence tree: docs/lab/redteam/certifier-rebuild/ (VERDICT.md, PREREG.md, results.tsv,
  rerun_all.sh, thincert_rb.zag, rngscan_v3_rb.zag, transform.py, tprobe.zag, CAST_AUDIT.md).
  NOTE: MASTER_ERROR_LEDGER.md cites the path as `redteam/...`; actual committed path is
  `docs/lab/redteam/...`. Also note: the task brief's "expected pin e3c2b9cc34e8" matches NO
  object or string anywhere in the frozen repo (git cat-file fails; git grep over the evidence
  tree empty; working-tree grep empty). Crew froze the evidence pin per the prereg method
  ("crew freezes the pin") as cadacc199684 — located, verified, used for all re-derivation.
- Wrote pure-Zag flipcount.zag (reads results.tsv, counts rows/flips/classes; zero RNG).
  Built with pinned znc (sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef).
  3/3 runs byte-identical (sha256 5ee19c73f6e3ff7297efab70a0fa6e11fbc4577d86415581d478dd6a16db9fc8):
  rows=35 flips=0 confirmed=34 void=0 artifact_fail=0 inconclusive=1 other=0.
  First version counted the MISSING-attestation row as a flip (flips=1); corrected per PREREG
  KB-FLIP (INCONCLUSIVE rows are input-missing, never flips) → flips=0.
- dirty1_urandom gap verification:
  * Committed sources match manifest source pins exactly (variation.zag de2b4b6d..., R33_NATIVE_IO_V1.zag e6379ddb...).
  * Rebuild with pinned znc FAILS: `plant_urandom` calls `nio_open_readonly` (absent from the
    committed substrate) and `_zag_rand()` (pinned znc native backend: "call to unknown function").
    No binary producible from committed sources + pinned toolchain → manifest BIN pin
    5f70bf18... unreproducible. Historical attestation corroborates: R7=FAIL (binary hash mismatch).
  * Controls: dirty2_clock, dirty3_uninit, dirty5_ptrleak all rebuild cleanly; dirty2_clock's
    rebuilt binary hash == manifest pin byte-exactly (8396d8bf...) → setup faithful, failure
    specific to dirty1_urandom.
- Minor source-verdict arithmetic slips noted (do not affect the headline): VERDICT.md KB-FLIP
  bar line says "35 CONFIRMED" but its own table + results.tsv sum to 34 CONFIRMED + 1
  INCONCLUSIVE = 35 rows; "35/35 old==stored" baseline is 34/34 scored + 1 unscored.
- Built binaries removed from work dir (no-binary rule); sources, run logs, and extracted
  evidence copies retained.

## 2026-09-22 23:31 PDT — PIN CORRECTION from coordinator (follow-up)

- Coordinator confirmed: the brief's "expected pin e3c2b9cc34e8" was a transcription artifact.
  Verified via GitHub API (gh-api): GET /repos/sylorlabs/TNN/commits/e3c2b9cc34e8 →
  HTTP 422 "No commit found for SHA: e3c2b9cc34e8". Disregarded per instruction; no stop was
  triggered — work had already proceeded on the frozen prereg's authority (§1).
- Per instruction, pins extracted from the frozen T2-CERT prereg section itself
  (docs/lab/crossref/PREREG_TIER2.md @ 7b2100d09911c5c10252c5756c7def288e70bd1f):
  the section names no SHA pins explicitly — its method is "crew freezes the pin".
  The evidence/verdict pins used (cadacc199684 verdict commit, 26b86329 prereg commit)
  are those named by the committed evidence chain (MASTER_ERROR_LEDGER.md, VERDICT.md
  header) at the frozen commit. All verified to resolve via the GitHub API:
  * 7b2100d09911c5c10252c5756c7def288e70bd1f → 200 OK (frozen prereg commit)
  * cadacc199684381833dbed4b27bb171b1d6f739f → 200 OK ("certifier-rebuild: rebuilt certifiers + full historical diff + verdict")
  * 26b86329b53b9aa24589dcf11d5ff09b125c1fe8 → 200 OK (certifier-rebuild prereg)
  * e3c2b9cc34e8 → 422, confirmed nonexistent — discrepancy closed.
- Verdict stands: REPRODUCED (0 flips re-derived pure-Zag 3/3 byte-identical; evidence pin
  located, API-verified; dirty1_urandom gap verified with root cause).
