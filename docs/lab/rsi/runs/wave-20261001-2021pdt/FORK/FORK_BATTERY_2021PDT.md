# Fork battery: wave-20261001-2021pdt (FORK lane)

Wave: wave-20261001-2021pdt. Worker: FORK lane (subagent).
Date: 2026-10-01. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab (tip 94767525856b09fa0d93569df941d0c5fd8c5bf3 at battery start).
Scratch: ~/workspace/fb1001_2021pdt/. Zero Python (safebin guard active, NAMECHECK.md Step 0 in FORK lane dir).
No commits, no checkout, no branch changes: read-only extraction by pinned SHA only.
Did not touch .wave_lock. Nothing written outside docs/lab/rsi/runs/wave-20261001-2021pdt/FORK/.

## Instrument (frozen, reused unchanged from wave-20261001-1721pdt)

- Driver: ~/workspace/fb1001_2021pdt/run_one.sh (byte-identical copy of ~/workspace/fb1001_0221pdt/run_one.sh, the frozen 2321pdt procedure; sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978 both copies).
- Harness: ~/workspace/fb0930_2321pdt/build/fork_battery_rebuilt (pure Zag, sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66, pin verified before use, matches prior waves).
- Fixtures: copies of ~/workspace/fb1001_0221pdt/fixtures/ (forkbat_hello.zag, neg1.zag, neg2.zag).
- Pins: znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef; probe 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919; b1_run 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066; b2_bin 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2.
- Working-copy znc at src/tools/toolchain/znc_linux_x86_64_abed8aa1: sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef, matches the frozen pin and prior waves.

## Enumeration

`git for-each-ref` over refs/heads and refs/remotes: 58 refs total (52 local, 6 remote).
Ref list snapshot: /tmp/fb2021pdt_refs.txt (58 lines, ref plus full tip SHA); comparison worksheet /tmp/actual_clean.txt.

Changes since the 1721pdt battery (57 refs):
- One new ref: tnn-native-lab-wave-archive-wave-20261001-1721pdt at 94767525856b09fa0d93569df941d0c5fd8c5bf3.
- One moved tip: tnn-native-lab eb19a4f3ca9d -> 94767525856b09fa0d93569df941d0c5fd8c5bf3.
- All other 56 refs byte-identical to the recorded 1721pdt set. Zero movement elsewhere.

## Method

Per the frozen 1721pdt procedure: each ref's full tip SHA was compared against the recorded SHA set (02:21 MANIFEST 88 entries plus 1121pdt, 1421pdt, and 1721pdt fresh results). Matching SHAs recorded RE-CERT with the recorded verdict (no re-run). The one ref with a new tip (tnn-native-lab) and the one new archive ref were fresh-tested with the frozen instrument via pinned-SHA extraction (no checkout). Both point to the identical commit 94767525856b09fa0d93569df941d0c5fd8c5bf3, so a single pinned-SHA extraction run covers both refs; the fresh result applies to the commit and therefore to both refs.

## Fresh test ([NEW])

SHA 94767525856b09fa0d93569df941d0c5fd8c5bf3 (tnn-native-lab tip; also the new archive-wave-20261001-1721pdt tip): verdict FRESH PASS.
Evidence: ~/workspace/fb1001_2021pdt/E/fresh-tnn-native-lab-94767525/RESULT.txt.
- znc pin match (498abcb5...), probe pin match (3b29aa06...).
- Harness exit 0, exactly one VERDICT=PASS token.
- b1 PASS, b2 PASS, b3 PASS, b1_cmp PASS, b2_bin_cmp PASS (byte-identical rebuild 75b85d3c...).
- b1_run sha 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066 matches pin.
- neg1 discriminates: compile exit 1, check exit 1, E0002 hit (1).
- neg2 discriminates: compiles, runs, stdout "WRONG OUTPUT" differs from expected "FORKBATTERY-OK 42" at char 1 (W vs F).
- Driver b3 strict check exit 0.
- Probe built and ran: R32_ZNC_PROBE_OK.
- Per-entry znc copy deleted per design (no znc.bin survives).

## Per-branch table (58 refs)

| branch | tip SHA | result |
| --- | --- | --- |
| tnn-native-lab | 94767525856b09fa0d93569df941d0c5fd8c5bf3 | FRESH PASS (tested this wave, commit 94767525856b09fa0d93569df941d0c5fd8c5bf3) |
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
| tnn-native-lab-wave-archive-wave-20261001-1721pdt | 94767525856b09fa0d93569df941d0c5fd8c5bf3 | FRESH PASS (tested this wave, commit 94767525856b09fa0d93569df941d0c5fd8c5bf3) |
| wave-20260927-0221pdt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | RE-CERT PASS |
| wave-20260927-0221pdt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | RE-CERT PASS |
| wave-20260927-0221pdt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | RE-CERT PASS |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | RE-CERT PASS |
| origin/tnn-native-lab | bedf8b4aab0110e3c115fb1bca3903551a32577e | RE-CERT PASS |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | RE-CERT PASS |
| rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | RE-CERT UNTESTABLE (pinned toolchain path absent in tree) |
| rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | RE-CERT UNTESTABLE (pinned toolchain path absent in tree) |
| rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | RE-CERT PASS |
| rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | RE-CERT PASS |

## Archive immutability

47 archive branches total. The 46 archive branches from the 1721pdt set (45 older archives plus wave-20261001-1421pdt at f52ab3aa1122) have tips matching the recorded set: 46/46 immutable, zero movement. The one new archive branch, tnn-native-lab-wave-archive-wave-20261001-1721pdt, pins 94767525856b09fa0d93569df941d0c5fd8c5bf3, which was fresh-tested this wave ([NEW] PASS above). So 47/47 archive refs accounted, 46 immutable plus 1 new fresh PASS.

## Untestable refs

- rh-pull-1-head (5802fec8401f28b4036b0dd5ebb23905610cab57): RE-CERT UNTESTABLE, recorded cause: pinned toolchain path absent in tree (git show exit nonzero at extraction step).
- rh-pull-2-head (4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba): RE-CERT UNTESTABLE, same recorded cause.
Both reported as UNTESTABLE with reason, not silently skipped. No new untestable refs this wave. Same cause as prior waves.

## Tally

- 58 refs enumerated (52 local, 6 remote).
- [NEW]: 1 fresh PASS extraction run on commit 94767525856b09fa0d93569df941d0c5fd8c5bf3, covering 2 refs (tnn-native-lab tip and the new archive-wave-20261001-1721pdt tip). tnn-native-lab tip passes the full frozen battery.
- [RE-CERT]: 56 refs with identical SHAs: 54 RE-CERT PASS, 2 RE-CERT UNTESTABLE (rh-pull-1-head, rh-pull-2-head, recorded cause).
- Zero FAIL. Zero new UNTESTABLE.
- Archive immutability 46/46 for the pre-existing archive set, plus the new archive fresh PASS: 47/47 accounted.
- Zero Python; nothing committed; branch and working copy untouched; per-entry znc copy deleted per design.

## Verdict lines

- FORK-BATTERY-COMPLETE. Hygiene certification only, not content review.
- [NEW] tnn-native-lab @ 94767525856b09fa0d93569df941d0c5fd8c5bf3: FRESH PASS (full frozen battery, this wave).
- [NEW] tnn-native-lab-wave-archive-wave-20261001-1721pdt @ 94767525856b09fa0d93569df941d0c5fd8c5bf3: FRESH PASS (same commit, same run).
- [RE-CERT] 54 refs: PASS by SHA match to prior battery results.
- [RE-CERT] rh-pull-1-head, rh-pull-2-head: UNTESTABLE (pinned toolchain path absent in tree).
- No FAIL entries. No what-broke items to report.

## Failure inventory

None. No battery step failed on any ref. The only non-PASS statuses are the two standing RE-CERT UNTESTABLE refs whose recorded cause (pinned toolchain path absent in tree) is unchanged from prior waves.
