# Fork battery: wave-20261002-0221pdt (FORK lane)

Wave: wave-20261002-0221pdt. Worker: FORK lane (subagent).
Date: 2026-10-02. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Scratch: ~/workspace/fb1002_0221pdt/. Zero Python (safebin guard active, NAMECHECK.md Step 0 in FORK lane dir).
No checkout, no branch changes: read-only extraction by pinned SHA only.
Did not touch .wave_lock. Nothing written outside docs/lab/rsi/runs/wave-20261002-0221pdt/FORK/.

## Instrument (frozen, reused unchanged)

- Driver: ~/workspace/fb1001_2021pdt/run_one.sh, the frozen 2321pdt procedure; sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978, pin verified before use, matches prior waves.
- Harness: ~/workspace/fb0930_2321pdt/build/fork_battery_rebuilt (pure Zag, sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66, pin verified before use, matches prior waves).
- Fixtures: copies of ~/workspace/fb1001_0221pdt/fixtures/ (forkbat_hello.zag, neg1.zag, neg2.zag).
- Pins: znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef; probe 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919; b1_run 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066; b2_bin 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2.
- Working-copy znc at src/tools/toolchain/znc_linux_x86_64_abed8aa1: sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef, matches the frozen pin and prior waves.

## Enumeration

`git for-each-ref` over refs/heads and refs/remotes: 62 refs total (56 local, 6 remote).
Ref list snapshot: /tmp/fb0221pdt_refs.txt (62 lines, ref plus full tip SHA).

Changes since the 2321pdt battery (59 refs):
- Three new refs: lane-battery-e5 at 8510feee6177ca619f8050581ea6875251dfb62f; lane-h5r2-skeptic2 at 709e1e82e58140379d07690cded1c5e358317880; wave-20261001-2321pdt-backup at c7f6774809d9688f14d158ffacee4b90760e06dd.
- One moved tip: tnn-native-lab 3dceac9cc046f95ea7a6f43ac5f2dbac8bcdbcce -> 8930dcc17d9f332140cf64f0c239172610faced3 (the 2321pdt WAVE-COMPLETE commit).
- All other 58 refs byte-identical to the recorded 2321pdt set. Zero movement elsewhere. No refs removed.

## Method

Per the frozen procedure: each ref's full tip SHA was compared against the recorded SHA set (59 entries from the 2321pdt battery). Matching SHAs recorded RE-CERT with the recorded verdict (no re-run). The three new refs and the one moved tip (4 distinct commits) were fresh-tested with the frozen instrument via pinned-SHA extraction (no checkout).

## Fresh test: lane-battery-e5 @ 8510feee6177ca619f8050581ea6875251dfb62f

Verdict FRESH PASS. Evidence: ~/workspace/fb1002_0221pdt/E/fresh-lane-battery-e5-8510feee/RESULT.txt.
- znc pin match (498abcb5...), probe pin match (3b29aa06...).
- Harness exit 0, exactly one VERDICT=PASS token.
- b1 PASS, b2 PASS, b3 PASS, b1_cmp PASS, b2_bin_cmp PASS (byte-identical rebuild 75b85d3c...).
- b1_run sha 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066 matches pin.
- neg1 discriminates: compile exit 1, check exit 1, E0002 hit (1).
- neg2 discriminates: compiles, runs, stdout "WRONG OUTPUT" differs from expected "FORKBATTERY-OK 42" at char 1 (W vs F).
- Driver b3 strict check exit 0.
- Probe built and ran: R32_ZNC_PROBE_OK.
- Per-entry znc copy deleted per design (no znc.bin survives).

## Fresh test: lane-h5r2-skeptic2 @ 709e1e82e58140379d07690cded1c5e358317880

Verdict FRESH PASS. Evidence: ~/workspace/fb1002_0221pdt/E/fresh-lane-h5r2-skeptic2-709e1e82/RESULT.txt.
Same frozen evidence profile as above: pins match, harness exit 0, one VERDICT=PASS token, b1/b2/b3 PASS, b1_cmp PASS, b2_bin_cmp PASS (75b85d3c...), b1_run 5dfe3c16... matches pin, neg1 discriminates (compile 1, check 1, E0002 hit 1), neg2 discriminates (stdout "WRONG OUTPUT" differs at char 1), b3 strict check exit 0, probe R32_ZNC_PROBE_OK. znc.bin deleted per design.

## Fresh test: wave-20261001-2321pdt-backup @ c7f6774809d9688f14d158ffacee4b90760e06dd

Verdict FRESH PASS. Evidence: ~/workspace/fb1002_0221pdt/E/fresh-backup-2321pdt-c7f67748/RESULT.txt.
Same frozen evidence profile: pins match, harness exit 0, one VERDICT=PASS token, b1/b2/b3 PASS, b1_cmp PASS, b2_bin_cmp PASS (75b85d3c...), b1_run 5dfe3c16... matches pin, neg1 discriminates, neg2 discriminates, b3 strict check exit 0, probe R32_ZNC_PROBE_OK. znc.bin deleted per design.

## Fresh test: tnn-native-lab @ 8930dcc17d9f332140cf64f0c239172610faced3

Verdict FRESH UNTESTABLE, cause: pinned toolchain path absent in tree (git show exit 128).
Evidence: ~/workspace/fb1002_0221pdt/E/fresh-tnn-native-lab-8930dcc1/RESULT.txt.
- At this tip, `git ls-tree` shows no src/tools/ subtree at all; the pinned path src/tools/toolchain/znc_linux_x86_64_abed8aa1 cannot be extracted read-only.
- The driver followed the standing rule: extraction failure -> UNTESTABLE with recorded cause, no further steps attempted.
- This is a STATUS CHANGE: tnn-native-lab was FRESH PASS at 3dceac9cc046f95ea7a6f43ac5f2dbac8bcdbcce in the 2321pdt battery; at the new tip the battery cannot run because the toolchain binary is absent from the tree. The coordinator git-repair (re-adding the pre-incident tracked tree) was in progress this wave; this FORK lane did not interfere with it. If the repair restores the path, the next wave battery will fresh-test the restored tip normally.
- This is hygiene certification only, not content review: UNTESTABLE means the battery could not execute, not that the tree is broken.

## Per-branch table (62 refs)

| branch | tip SHA | result |
| --- | --- | --- |
| lane-battery-e5 | 8510feee6177ca619f8050581ea6875251dfb62f | FRESH PASS (tested this wave, commit 8510feee6177ca619f8050581ea6875251dfb62f) |
| lane-h5r2-skeptic2 | 709e1e82e58140379d07690cded1c5e358317880 | FRESH PASS (tested this wave, commit 709e1e82e58140379d07690cded1c5e358317880) |
| origin/tnn-native-lab | bedf8b4aab0110e3c115fb1bca3903551a32577e | RE-CERT PASS |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | RE-CERT PASS |
| rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | RE-CERT UNTESTABLE (pinned toolchain path absent in tree, standing cause) |
| rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | RE-CERT UNTESTABLE (pinned toolchain path absent in tree, standing cause) |
| rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | RE-CERT PASS |
| rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | RE-CERT PASS |
| tnn-native-lab | 8930dcc17d9f332140cf64f0c239172610faced3 | FRESH UNTESTABLE (pinned toolchain path absent in tree, git show exit 128) |
| tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d3f4849358817fae945aab942882ab92 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574098e8f85d909bfddeac368588f76f72 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | 9f681e2719ea45916da19cad15965717bffa82af | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | b66c6aeabfff03ceca9194386d98b61574ff4601 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-1421pdt | c5f0383e2713aa91166b01a1a15229937cea4b3f | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-1721pdt | 088a1914efb308f8a5d8f168f1f9878cf7a4fca8 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260926-2021pdt | 5ba241235482610f1c8f538d97ca0462164b4014 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260927-0221pdt | 463b115b69e280da0d7f6da15c6ded2f3f610809 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260927-0521pdt | 80c40a7afc0231493e0f1f46540a6dbe60c60c3f | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260927-1421pdt | 8929cdd93df7efeb8b67320d5a7d67e2d6bed467 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260928-2021pdt | 345daa6046bfbac384e33959f2ebc04a4688780d | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-0221pdt | d2fdf1225ec973e1e07082af6b067fd1525cb643 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-0521pdt | 2e9326e6caf4a9462102e8dfc8058e7cec2404d6 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-0821pdt | 5f86e6cb2eaedb115235e4af52684a44b7c6eb36 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-1121pdt | d18f7f68d3792c58346861b89eab374c2e728ef0 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-1421pdt | 347260cee11ef96ad6e1a832bc994d53fbccc4d2 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-1721pdt | dff8c200590a64023b64e9c3a5fbdc4dcf4766b9 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-2321pdt | a4314633ac48591d3217d291c47b68f9e99ef77d | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260930-0221pdt | 697d4f308bb8e2a5b65df3502e6a66b5fecd3f2a | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260930-1121pdt | caf07be920075ccc9027aea075f4ee566a2420a3 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | d24bb4b502022efc675dda80e0e97436acc09278 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260924-2321pdt | e33b5ddbdcb6cf5290c2fb3272d1dd8fb6c86155 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-0221pdt | 058ee02a8a31efc66fb8e92293d399752ce33a6f | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-0521pdt | 0ee06268e9118d1812f7a1e1b85ad384f79a583a | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-0821pdt | 393007563d27b931c8af59ad9d9fedc336fbed1d | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-1121pdt | 60a0579973fa64c80ec2501afc1f5d3080b9b8ba | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-1421pdt | 2e2c65fb294e85348d4329ca1e55caf8f6c258a9 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-0521pdt | 4328a8350d987a65c4e86e4973dbe45c9d5f6cd5 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-0821pdt | 4bbbca69cecd9c47602e125545b137380e8bab1a | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-1121pdt | 746ff60ba16d18c36db2ccd4394cbb9db9d6266d | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-1421pdt | a222f8f178049b9aeee3b053328c59e9b6fd813d | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-1721pdt | a4d4ff7cd4eb3ad7fbed08da7e0fb8282f32844a | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-2321pdt | 004616f657165191c0d0e89d91fc10a99edd2d6e | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-0821pdt | e9373dad1aca4a694cf39d023e7756312e125ba7 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-1121pdt | 4805f5363a0dba762abf2d35e8ab8284abce6731 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-1721pdt | 4042f15bf40b1c73a516ba5eda2a412033db9f6d | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-2021pdt | baf48e4744c3c075e3fc70a383f0a77efec83ad7 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-2321pdt | 43f339e60dad44bf5ceccef83962248b7a434256 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-0221pdt | f03aa6fc81b7ed5dd141e393703425c16f65b794 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-0829pdt | 81f0cfe12c614fef83faab91bef676441e679833 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-1721pdt | 4340126e6c1cd3f03dbc653ee1f585a741fff806 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-2321pdt | a014dc1d96d0935f4e4d53888b3e488e3ce1f459 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260930-0805pdt | fdadcbe3c7b49887e795462a11664122349591c1 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260930-0821pdt | bb9b56a34d2063d41118db1b2aa4a0366790f15d | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20261001-0221pdt | 536101b5bcf76ea5de3d565478e08d0a54d447d2 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20261001-1421pdt | f52ab3aa1122ec92b3ad661326804ee0f3ba2e1b | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20261001-1721pdt | 94767525856b09fa0d93569df941d0c5fd8c5bf3 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20261001-2021pdt | a272a8f6aa102fcab59e663961c06a37aad88831 | RE-CERT PASS |
| wave-20260927-0221pdt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | RE-CERT PASS |
| wave-20260927-0221pdt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | RE-CERT PASS |
| wave-20260927-0221pdt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | RE-CERT PASS |
| wave-20261001-2321pdt-backup | c7f6774809d9688f14d158ffacee4b90760e06dd | FRESH PASS (tested this wave, commit c7f6774809d9688f14d158ffacee4b90760e06dd) |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | RE-CERT PASS |

## Archive immutability

48 archive branches total (same set as the 2321pdt battery). All 48 tips byte-identical to the pinned 2321pdt record: 48/48 immutable, zero movement. No new archive branches this wave. All recorded RE-CERT PASS by SHA match.

## Untestable refs

- tnn-native-lab @ 8930dcc17d9f332140cf64f0c239172610faced3: FRESH UNTESTABLE, new status this wave. Recorded cause: pinned toolchain path absent in tree (git show exit 128; no src/tools/ subtree at this tip). Prior status was FRESH PASS at 3dceac9c. See Fresh test section above. Not a battery failure: the instrument behaved per the standing extraction rule.
- rh-pull-1-head @ 5802fec8401f28b4036b0dd5ebb23905610cab57: RE-CERT UNTESTABLE, recorded cause: pinned toolchain path absent in tree (git show exit 128). Cause re-confirmed this wave.
- rh-pull-2-head @ 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba: RE-CERT UNTESTABLE, same recorded cause, re-confirmed this wave.
All three reported as UNTESTABLE with reason, not silently skipped.

## Tally

- 62 refs enumerated (56 local, 6 remote).
- [NEW]: 4 fresh extraction runs on 4 distinct commits: 3 FRESH PASS (lane-battery-e5, lane-h5r2-skeptic2, wave-20261001-2321pdt-backup), 1 FRESH UNTESTABLE (tnn-native-lab @ 8930dcc1, toolchain path absent).
- [RE-CERT]: 58 refs with identical SHAs: 56 RE-CERT PASS, 2 RE-CERT UNTESTABLE (rh-pull-1-head, rh-pull-2-head, standing cause).
- Zero FAIL. Zero new UNTESTABLE beyond the tnn-native-lab tip status change.
- Archive immutability 48/48.
- Zero Python; no checkout; branch and working copy untouched; per-entry znc copy deleted per design.

## Verdict lines

- FORK-BATTERY-COMPLETE. Hygiene certification only, not content review.
- [NEW] lane-battery-e5 @ 8510feee6177ca619f8050581ea6875251dfb62f: FRESH PASS (full frozen battery, this wave).
- [NEW] lane-h5r2-skeptic2 @ 709e1e82e58140379d07690cded1c5e358317880: FRESH PASS (full frozen battery, this wave).
- [NEW] wave-20261001-2321pdt-backup @ c7f6774809d9688f14d158ffacee4b90760e06dd: FRESH PASS (full frozen battery, this wave).
- [NEW] tnn-native-lab @ 8930dcc17d9f332140cf64f0c239172610faced3: FRESH UNTESTABLE (pinned toolchain path absent in tree; status changed from FRESH PASS at prior tip; see note on the in-progress coordinator git-repair).
- [RE-CERT] 56 refs: PASS by SHA match to prior battery results.
- [RE-CERT] rh-pull-1-head, rh-pull-2-head: UNTESTABLE (pinned toolchain path absent in tree).
- No FAIL entries. No what-broke items to report beyond the tnn-native-lab extraction note above.

## Failure inventory

No battery step failed on any ref. The only non-PASS statuses are the three UNTESTABLE refs whose recorded cause (pinned toolchain path absent in tree) held at measurement time. For tnn-native-lab this cause is new at the current tip and may resolve when the coordinator git-repair completes; the next wave battery will fresh-test whatever tip is then current.
