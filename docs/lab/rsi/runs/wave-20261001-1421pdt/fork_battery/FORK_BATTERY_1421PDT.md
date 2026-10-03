# Fork battery: wave-20261001-1421pdt

Wave: wave-20261001-1421pdt. Worker: fork-battery lane.
Date: 2026-10-01. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Scratch: ~/workspace/fb1001_1421pdt/. Zero Python (safebin guard active, see NAMECHECK.md Step 0).
No commits, no checkout, no branch changes: read-only extraction by pinned SHA only.

## Instrument (frozen)

- Driver: ~/workspace/fb1001_0221pdt/run_one.sh (frozen 2321pdt procedure, byte-identical reuse).
- Harness: ~/workspace/fb0930_2321pdt/build/fork_battery_rebuilt (pure Zag, sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66, matches frozen).
- Fixtures: ~/workspace/fb1001_0221pdt/fixtures/ (forkbat_hello.zag, neg1.zag, neg2.zag).
- Pins: znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef; probe 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919; b1_run 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066; b2_bin 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2.

## Enumeration

`git for-each-ref` over refs/heads and refs/remotes: 56 refs total (50 local, 6 remote).
Ref list snapshot: /tmp/tips_full.txt (56 lines, branch plus full tip SHA).

## Method

For each ref, the full tip SHA was compared against the recorded SHA set:
the wave-20261001-0221pdt full-run table (88 entries: 85 PASS, 1 FAIL, 2 UNTESTABLE;
docs/lab/rsi/runs/wave-20261001-0221pdt/fork_battery/MANIFEST.md) plus the two fresh
1121pdt results (a298709d5c21 PASS, 536101b5bcf7 PASS; evidence at
~/workspace/fb1001_1121pdt/E/). Matching SHAs were recorded RE-CERT with the
recorded verdict (no re-run). Exactly one ref had a new tip and was fresh-tested
with the frozen instrument via pinned-SHA extraction (no checkout).

## Results

Tally: 2 FRESH PASS, 52 RE-CERT PASS (02:21 SHAs), 1 RE-CERT PASS (1121pdt fresh SHA),
2 RE-CERT UNTESTABLE. Zero FAIL. Zero new UNTESTABLE.

Archive-branch immutability: all 45 archive branches (44 from the 02:21 set plus the
1121pdt-fresh 536101b5b) have tip SHAs in the recorded set: 45/45 immutable, zero movement.

### Fresh tests

- tnn-native-lab at 02a338dbfcd5bcf196578ac532fa2e1af75fd406 (tip at battery start): verdict PASS.
  Evidence: ~/workspace/fb1001_1421pdt/E/local-tnn-native-lab/RESULT.txt.
  znc pin match, probe pin match, b1/b2/b3 all PASS, b1_cmp PASS, b2_bin_cmp PASS
  (byte-identical rebuild 75b85d3c...), neg1 discriminates (E0002 hit, compile exit 1,
  check exit 1), neg2 discriminates (compiles, runs, stdout differs at char 1),
  probe R32_ZNC_PROBE_OK. Harness exit 0, exactly one VERDICT=PASS token.

- tnn-native-lab at 105e9ee8b8406f9f2d5690f9fd7797bef57d23c8 (tip at battery end;
  another lane committed on the branch mid-run, reflog 21:30 UTC): verdict PASS.
  Evidence: ~/workspace/fb1001_1421pdt/E/local-tnn-native-lab-tip2/RESULT.txt.
  Same frozen instrument; znc pin match, probe pin match, b1/b2/b3 all PASS,
  b1_cmp PASS, b2_bin_cmp PASS (75b85d3c...), neg1 discriminates, neg2 discriminates,
  probe R32_ZNC_PROBE_OK. Harness exit 0, exactly one VERDICT=PASS token.

### Per-branch table

| branch | tip SHA | result |
| --- | --- | --- |
| origin/tnn-native-lab | bedf8b4aab0110e3c115fb1bca3903551a32577e | RE-CERT PASS |
| rh-main | 27a4271f208247a1e9c24cca35468c298b6cd29d | RE-CERT PASS |
| rh-pull-1-head | 5802fec8401f28b4036b0dd5ebb23905610cab57 | RE-CERT UNTESTABLE |
| rh-pull-2-head | 4b76bb59fd6fb6a50df4e048a3b9d28e97d5bfba | RE-CERT UNTESTABLE |
| rh-pull-3-head | 9914322267e1358e5542a23c72ec51d1a9ae43df | RE-CERT PASS |
| rh-tnn-native-lab-live-tip | b257c02cc68b7a1f079dee28611cccd93b6efc9d | RE-CERT PASS |
| tnn-native-lab | 02a338dbfcd5bcf196578ac532fa2e1af75fd406 | FRESH PASS |
| tnn-native-lab @ 105e9ee8b (tip at battery end; committed mid-run by another lane) | 105e9ee8b8406f9f2d5690f9fd7797bef57d23c8 | FRESH PASS |
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
| tnn-native-lab-wave-archive-wave-20261001-0221pdt | 536101b5bcf76ea5de3d565478e08d0a54d447d2 | RE-CERT PASS (1121pdt fresh) |
| wave-20260927-0221pdt-exp1 | 1010a63c3c1cc3f3724f6cf0ca55decc08207a2d | RE-CERT PASS |
| wave-20260927-0221pdt-exp2 | a2a36e6571b2cf716df151c6ad8b8ffa07c6d3e4 | RE-CERT PASS |
| wave-20260927-0221pdt-sensory | c368b8e1ffecec2f9061011f5d7c0e3e68675e0a | RE-CERT PASS |
| wave-debate-session-1-backup | 3947dca1a77c00818575dbc7476556c8278b8b7b | RE-CERT PASS |

### Notes on dropped 02:21 labels

The 02:21 full run had 88 named entries; the 1121pdt wave carried 86 as RE-CERT plus
2 fresh. Refs that no longer exist in the working copy (wt-* worktrees,
local-*-tip labels, origin-tnn-native-lab-live/rt, rh-fs-gr1, rh-r2-7,
rh-reorg-phase-0-1, rh-wg-freeze, rotated-old-live-23c2c02) are not re-certifiable
as branches; their content SHAs remain recorded in the 02:21 MANIFEST. The 02:21
FAIL entry (rotated-old-live-23c2c02, znc sha mismatch, pin divergence) has no
current branch, so it contributes no live FAIL to this wave. rh-pull-1-head and
rh-pull-2-head remain UNTESTABLE for the identical recorded cause (pinned
toolchain path absent in tree).

## Verdict

FORK-BATTERY-COMPLETE. 56 refs enumerated plus one mid-run superseded tip
(57 named entries); 2 fresh PASS with the frozen instrument; 55 RE-CERT with
identical SHAs; 45/45 archive branches immutable; zero failures; zero Python;
nothing committed.
