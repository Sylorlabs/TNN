# Fork battery: wave-20261001-1721pdt (GOV lane)

Wave: wave-20261001-1721pdt. Worker: GOV lane (subagent).
Date: 2026-10-01. Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab (tip eb19a4f3c).
Scratch: ~/workspace/fb1001_1721pdt_gov/. Zero Python (safebin guard active, NAMECHECK.md Step 0 in GOV lane dir).
No commits, no checkout, no branch changes: read-only extraction by pinned SHA only.
Did not touch .wave_lock.

## Instrument (frozen, reused unchanged from wave-20261001-1421pdt)

- Driver: ~/workspace/fb1001_1721pdt_gov/run_one.sh (byte-identical copy of ~/workspace/fb1001_0221pdt/run_one.sh, the frozen 2321pdt procedure).
- Harness: ~/workspace/fb0930_2321pdt/build/fork_battery_rebuilt (pure Zag, sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66, pin verified before use).
- Fixtures: copies of ~/workspace/fb1001_0221pdt/fixtures/ (forkbat_hello.zag, neg1.zag, neg2.zag).
- Pins: znc 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef; probe 3b29aa066126b263765986ca6f5b6e8e60113135198d2bea431be53a6518f919; b1_run 5dfe3c161096819c8c0dd6057c4df9944ddd884f57b9a513b47e7655d53c6066; b2_bin 75b85d3cec684f6a156f4c01169551369e4b0e040b56ec1fd24749876eddffa2.

## Enumeration

`git for-each-ref` over refs/heads and refs/remotes: 57 refs total (51 local, 6 remote).
One new ref since the 1421pdt battery: tnn-native-lab-wave-archive-wave-20261001-1421pdt at f52ab3aa1.
One moved tip: tnn-native-lab 02a338dbf -> eb19a4f3c. All other tips byte-identical to the 1421pdt recorded set.

## Method

Per the 1421pdt procedure: each ref's full tip SHA was compared against the recorded SHA set
(02:21 MANIFEST 88 entries plus 1121pdt and 1421pdt fresh results). Matching SHAs recorded
RE-CERT with the recorded verdict (no re-run). The seven task-mandated SHAs plus the new
archive tip were tested FRESH with the frozen instrument via pinned-SHA extraction (no checkout).

## Fresh tests (8, all PASS)

Each entry: znc pin match, probe pin match, harness exit 0, exactly one VERDICT=PASS token,
b1/b2/b3 PASS, b1_cmp PASS, b2_bin_cmp PASS (byte-identical rebuild 75b85d3c...),
neg1 discriminates (E0002, compile and check both fail), neg2 discriminates (compiles,
runs, stdout differs at char 1), probe R32_ZNC_PROBE_OK.

| SHA (entry) | role | verdict |
|---|---|---|
| eb19a4f3ca9debcc1d7ff031c8f6d79694c609c3 | tnn-native-lab tip (protect-how retry) | FRESH PASS |
| f52ab3aa1122ec92b3ad661326804ee0f3ba2e1b | new archive tip wave-20261001-1421pdt | FRESH PASS |
| 1963e994dd549dd6bb32360d3e44ff51ca79a64e | mini-lifetime integration | FRESH PASS |
| 293cf0672c15971f7bc184e6a4dfaf2feee3f9f7 | governance wave 2 (ledger C181-C188) | FRESH PASS |
| 0509fd116c96abcda02d9d34fd8df2610394c29d | rebinding hardening | FRESH PASS |
| ff0d91691fd19c84839264a61aac936e3e429d75 | utility integration | FRESH PASS |
| 105e9ee8b8406f9f2d5690f9fd7797bef57d23c8 | persistent connections | FRESH PASS |
| 02a338dbfcd5bcf196578ac532fa2e1af75fd406 | substrate expansion | FRESH PASS |

Evidence: ~/workspace/fb1001_1721pdt_gov/E/<entry>/RESULT.txt for each entry
(fresh-tnn-native-lab-eb19a4f3c, fresh-arch-1421pdt-f52ab3aa1, fresh-1963e994d,
fresh-293cf0672, fresh-0509fd116, fresh-ff0d91691, fresh-105e9ee8b, fresh-02a338dbf).

Note: 02a338dbf and 105e9ee8b were FRESH PASS in the 1421pdt battery and are
no longer branch tips; they were re-run fresh this wave per the task mandate.
Both PASS again.

## Per-branch table (57 refs)

| branch | tip SHA | result |
|---|---|---|
| tnn-native-lab | eb19a4f3ca9d | FRESH PASS (tested this wave) |
| tnn-native-lab-wave-archive-20260923-2321pdt | 3aa59360d3f4 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-0221pdt | aab82c574098 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-0521pdt | 9f681e2719ea | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-1121pdt | b66c6aeabfff | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-1421pdt | c5f0383e2713 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260924-1721pdt | 088a1914efb3 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260926-2021pdt | 5ba241235482 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260927-0221pdt | 463b115b69e2 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260927-0521pdt | 80c40a7afc02 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260927-1421pdt | 8929cdd93df7 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260928-2021pdt | 345daa6046bf | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-0221pdt | d2fdf1225ec9 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-0521pdt | 2e9326e6caf4 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-0821pdt | 5f86e6cb2eae | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-1121pdt | d18f7f68d379 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-1421pdt | 347260cee11e | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-1721pdt | dff8c200590a | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260929-2321pdt | a4314633ac48 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260930-0221pdt | 697d4f308bb8 | RE-CERT PASS |
| tnn-native-lab-wave-archive-20260930-1121pdt | caf07be92007 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260924-1721pdt | d24bb4b50202 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260924-2321pdt | e33b5ddbdcb6 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-0221pdt | 058ee02a8a31 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-0521pdt | 0ee06268e911 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-0821pdt | 393007563d27 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-1121pdt | 60a0579973fa | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260925-1421pdt | 2e2c65fb294e | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-0521pdt | 4328a8350d98 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-0821pdt | 4bbbca69cecd | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-1121pdt | 746ff60ba16d | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-1421pdt | a222f8f17804 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-1721pdt | a4d4ff7cd4eb | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260926-2321pdt | 004616f65716 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-0821pdt | e9373dad1aca | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-1121pdt | 4805f5363a0d | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-1721pdt | 4042f15bf40b | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-2021pdt | baf48e4744c3 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260927-2321pdt | 43f339e60dad | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-0221pdt | f03aa6fc81b7 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-0829pdt | 81f0cfe12c61 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-1721pdt | 4340126e6c1c | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260928-2321pdt | a014dc1d96d0 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260930-0805pdt | fdadcbe3c7b4 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20260930-0821pdt | bb9b56a34d20 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20261001-0221pdt | 536101b5bcf7 | RE-CERT PASS |
| tnn-native-lab-wave-archive-wave-20261001-1421pdt | f52ab3aa1122 | FRESH PASS (tested this wave) |
| wave-20260927-0221pdt-exp1 | 1010a63c3c1c | RE-CERT PASS |
| wave-20260927-0221pdt-exp2 | a2a36e6571b2 | RE-CERT PASS |
| wave-20260927-0221pdt-sensory | c368b8e1ffec | RE-CERT PASS |
| wave-debate-session-1-backup | 3947dca1a77c | RE-CERT PASS |
| origin/tnn-native-lab | bedf8b4aab01 | RE-CERT PASS |
| rh-main | 27a4271f2082 | RE-CERT PASS |
| rh-pull-1-head | 5802fec8401f | RE-CERT UNTESTABLE |
| rh-pull-2-head | 4b76bb59fd6f | RE-CERT UNTESTABLE |
| rh-pull-3-head | 9914322267e1 | RE-CERT PASS |
| rh-tnn-native-lab-live-tip | b257c02cc68b | RE-CERT PASS |

## Archive immutability

All 46 archive branches (45 from the 1421pdt set plus the new
wave-20261001-1421pdt archive at f52ab3aa1) have tips matching the
recorded set: 46/46 immutable, zero movement. The stale packed-ref
entry for tnn-native-lab (249a1b85e) is superseded by the loose ref
(eb19a4f3c); loose refs take precedence and the live enumeration used
the loose ref.

## Untestable refs

- rh-pull-1-head (5802fec8401f): RE-CERT UNTESTABLE, recorded cause: pinned toolchain path absent in tree.
- rh-pull-2-head (4b76bb59fd6fb): RE-CERT UNTESTABLE, same recorded cause.
Both are reported as UNTESTABLE with reason, not silently skipped. No
new untestable refs.

## Tally

57 refs enumerated. 8 FRESH PASS (7 task-mandated SHAs + 1 new archive
tip; 2 of these are also the current tips of tnn-native-lab and the
new archive branch). 55 RE-CERT with identical SHAs (53 PASS, 2
UNTESTABLE with recorded cause). Zero FAIL. Archive immutability
46/46. Zero Python; nothing committed; branch and working copy
untouched.

## Verdict

FORK-BATTERY-COMPLETE. Hygiene certification only, not content review.
