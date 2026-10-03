# RUNLOG — T2-LHADV crossref heavy crew (coding LH-ADV-2 replication)
Crew session: 483feff9-1c22-466b-8af7-7bd9b871614c | started 2026-09-23 ~04:00 PDT

## Step 1 — frozen prereg verification (2026-09-23)
- Source: ~/workspace/tnn-lab/crossref/PREREG_TIER2.md, lines 107-111
  ("## T2-LHADV — coding LH-ADV-2: adversarial long-horizon closed (Type A)")
- Section sha256 (lines 107-111, \n-terminated): cb3823ee2bd62bac587e68b7f809e308207898ad4ca00f4525d98b6b14a3b39a
- Full file sha256 (local): 90070c88e43aecb6ba3ee8df6d487f7bf1b1673bb12d3ad8dcd11d597ade4a9f
- tnn-native-lab branch head (API, sylorlabs/TNN, at check time): 9608da1d4bbc18e2292ec445ed5267482039cc64
  (commit "PAM R2-7: amend VERDICT with full-run B2/B3 ...", 2026-09-23T10:59:07Z)
- Section text matches the task's "Section orientation" verbatim: Part A e4d666fc20cc
  (ADV-RET 10/10 PASS, ADV-DET 5/5x5 PASS incl. recovered stages); LH-ADV-2 prereg
  beb00397224ae, result 12487b93756a; 54 stages, 52 accepted + 2 honest halts
  (D9 UNRECOVERABLE, F1 KB-MISS); bars ADV-DS 47/47, ADV-REC 6/6 diag + 5/5 recovered
  <=1 extra cycle + D9 halted + 0 fabrication, ADV-HH 54/54 terminated, ADV-CRIT
  (51/51 cal ACCEPT, 1/1 seeded bug rejected, 0 false rejects), ADV-DIAG
  (D5->UPSTREAM D4, C7->UPSTREAM C6, D8->LOCAL D8; HINT-LEAK audit clean),
  ADV-RET 10/10, ADV-DET 5/5x5. PASS on all claims => proceeding (no STOP).

## Next steps
- Verify committed blob sha of crossref/PREREG_TIER2.md matches local copy (clean-checkout discipline).
- Locate LH-ADV-2 prereg (beb00397224ae) and result (12487b93756a) artifacts in the repo.

## Step 2 — pinned commits resolved (2026-09-23)
- Part A commit e4d666fc20ccb8b0b6b17fe9287794236f6c59ab — "LH-ADV-2026-09-22:
  ADV-RET and ADV-DET dedicated runs (both PASS)" 2026-09-22T21:58:58Z (on
  tnn-native-lab). Verified present via commits API on file path.
- LH-ADV-2 prereg beb00397224ae5ae24df9766ac8f65210d9bab87 — "LH-ADV-2 frozen
  prereg + package (no scored run yet)" 2026-09-22T22:20:24Z. Verified.
- LH-ADV-2 result 12487b93756ac66e9b1ec3d0262d8f00b50ccc3a — "LH-ADV-2 scored
  trial results" 2026-09-22T22:34:26Z. Verified.
- envelope.json is NOT in the prereg commit tree (sealed plaintext never
  committed, as prereg required); local copy sha256
  22f6d1142a18ae5db00ea26025ad4908eb9fcd5c548cae3f459524f3bc9cee26
  matches the committed hash. Used as the sole seeded-failure source.
- Clean-checkout blob check: committed adv2_critic.zag blob content sha256
  == 245d9c325b5b719b... == prereg frozen SHA == local/scratch copy. PASS.
- Reference artifacts preserved in scratch: ref/REF_ledger2.json
  (sha a97df78e...), REF_result2_ret.json (5614ad82...), REF_result2_det.json
  (fe070241...).

## Step 3 — build (2026-09-23)
- Pinned toolchain znc 2026.07.0-dev (edition 2026), sha prefix 498abcb5ab346f8cb246222a1ca63699.
- Scratch tree: ~/workspace/scratch-crossref/T2-heavy/T2-LHADV/work/
  (rsync of committed sources, __pycache__/tmp/build excluded).
- Built adv2_delib / adv2_emit / adv2_critic with --no-analyze --no-zagd; all
  three wrote native binaries without errors.

## Step 4 — rerun 1/3 (started 2026-09-23 ~04:07 PDT)
- python3 adv2_run.py with ADV2_BUILD=work/build, ADV2_TMP=work/tmp_run2;
  log logs/run1.log.

## Step 4a — ADV-CRIT structural audit (rerun-independent, 2026-09-23)
- audit_critic_indep2.py on frozen sources: AUDIT-PASS
  critic_fns=50 emitter_fns=32 delib_fns=64 shared_beyond_main=0
  (matches recorded claim exactly).
- Behavioral ADV-CRIT components (calibration 51/51, 1/1 seeded-bug reject,
  0 false rejects) come out of the scored battery rerun below.

## Step 5 — rerun 1 complete (2026-09-23 ~04:20 PDT)
- 54 stages: 52 accepted, 2 honest halts (D9 UNRECOVERABLE via KB-MISS after
  quarantine; F1 KB-MISS control). ledger2.json sha256:
  a97df78e374dec1bb6a350e2c76ab49b14e2fe4a3341140f025908982a1c16dd
  == REF_ledger2.json (committed result, 12487b93756a) byte-identical.
- audit_adv2.py: ADV-DS PASS 47/47; ADV-REC PASS (6/6 diagnosed, 5/5 recovered,
  unrec halted, fabrication=0); ADV-HH PASS (F1 KB-MISS, 54/54 terminated);
  ADV-DIAG PASS (D5->UPSTREAM D4, C7->UPSTREAM C6, D8->LOCAL D8); HINT-LEAK clean;
  NO-RNG clean; NO-SOLUTION clean. AUDIT-PASS.
- ADV-CRIT behavioral (from ledger): 51 CRITIC-ACCEPT on clean outputs
  (51/51 calibration), 1 CRITIC-REJECT EMITTER-BUG (D8 seeded bug, 1/1),
  0 false rejects.
- Runs 2 and 3 queued (fresh tmp_run2 per run).

## Step 6 — Part A (e4d666fc20cc) handling
- Part A (ADV-RET 10/10, ADV-DET 5/5x5 on LH-ADV-2026-09-22 incl. recovered
  stages) is the LH-ADV-2 RET/DET machinery on the FIRST trial's artifacts;
  LH-ADV-2 ran ADV-RET/ADV-DET natively (dedicated runs, same machinery) and
  those are what the crossref rule's "all bars pass at the same counts"
  covers for THIS crew: ADV-RET 10/10 and ADV-DET 5/5x5 dedicated reruns will
  be executed against my fresh ledger2.json.

## Step 7 — clean-checkout verification complete (2026-09-23)
- All 54 contract files: local git-blob sha1 == prereg-commit blob sha1
  (beb00397224ae5ae24df9766ac8f65210d9bab87). Zero mismatches.
- machinery/adv2_delib.zag + adv2_emit.zag: local sha256 matches frozen
  prereg table (16d66a24aa..., 20edc86f57...); adv2_critic.zag verified
  against committed blob via API (245d9c325b...).
- adv2_run.py (975c3b52dd8...), adv_kb.txt (3b582177c0b...), envelope.json
  (22f6d1142a18...) all match frozen SHAs.
- Verdict on sources: clean — rerun ran from committed sources.

## Step 8 — 3/3 byte-identical battery runs (2026-09-23)
- RUN1 ledger sha256 a97df78e374dec1bb6a350e2c76ab49b14e2fe4a3341140f025908982a1c16dd
- RUN2 ledger sha256 a97df78e... match_run1=YES
- RUN3 ledger sha256 a97df78e... match_run1=YES
- All three == committed REF_ledger2.json byte-identically. 52 accepted / 2
  honest halts (D9 UNRECOVERABLE, F1 KB-MISS) in every run. >=3 byte-identical
  runs: SATISFIED.

## Step 9 — ADV-RET / ADV-DET dedicated reruns (2026-09-23)
- ADV-RET: 10/10 MATCH (spec+output+accept byte-identical, incl. all 5
  injected/recovered stages D6/B7/D5/C7/D8); per-stage cycle counts identical
  to committed REF_result2_ret.json. PASS, exit 0.
- ADV-DET: 5/5 stages x5 byte-identical (spec/source/binary/output;
  incl. recovered stage D6). PASS, exit 0.

## Verdict
- REPRODUCED. Rule check: 52/54 accepted with the same 2 honest halts
  (D9 UNRECOVERABLE, F1 KB-MISS); all bars pass at the same counts
  (ADV-DS 47/47, ADV-REC 6/6 + 5/5 + halted + 0 fabrication, ADV-HH 54/54,
  ADV-CRIT 51/51 + 1/1 + 0 false rejects, ADV-DIAG 2/2 UPSTREAM exact + 1/1 LOCAL,
  ADV-RET 10/10, ADV-DET 5/5x5); 0 fabrication; no seeded failure undiagnosed.
- VERDICT.md written. Caveat carried through unchanged.
