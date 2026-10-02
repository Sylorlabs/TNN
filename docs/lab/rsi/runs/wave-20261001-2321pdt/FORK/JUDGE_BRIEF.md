# Judge brief: FORK lane, wave-20261001-2321pdt

RENDER_SHA: 45f3edaa10a0253b3ed892cbcf8171f9a6be8779456b9c2ceebb5b7de61db965
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: fork battery 2021pdt 54 RE-CERT PASS + 2 UNTESTABLE
NEW_KNOWLEDGE_CLAIM: The 2321pdt fork battery enumerates 59 refs (53 local, 6 remote), records FRESH PASS for the two new tip commits 3dceac9cc046f95ea7a6f43ac5f2dbac8bcdbcce and a272a8f6aa102fcab59e663961c06a37aad88831 under the frozen instrument, RE-CERT PASS for the other 55 unchanged refs, and RE-CERT UNTESTABLE for rh-pull-1-head and rh-pull-2-head with the standing toolchain-path cause.

## Summary for judges

The frozen fork battery ran unchanged this wave. All 59 branch and fork refs were enumerated by full tip SHA. Two commits were new since the 2021pdt record: the tnn-native-lab tip (moved to 3dceac9cc046f95ea7a6f43ac5f2dbac8bcdbcce) and the new archive branch tnn-native-lab-wave-archive-wave-20261001-2021pdt (a272a8f6aa102fcab59e663961c06a37aad88831). Both were fresh-tested by pinned-SHA extraction with no checkout and both passed every battery step: znc and probe pins matched, harness exit 0 with exactly one VERDICT=PASS, b1 through b3 plus b1_cmp and b2_bin_cmp all PASS, neg1 and neg2 discriminated as required, driver b3 strict check clean, probe printed R32_ZNC_PROBE_OK.

The remaining 57 refs are byte-identical to the recorded 2021pdt set and were re-certified without re-run: 55 PASS, 2 UNTESTABLE (rh-pull-1-head, rh-pull-2-head; pinned toolchain path absent in tree, same cause as prior waves). Zero FAIL this wave. Archive immutability: 47/47 pre-existing archive tips unchanged; the one new archive ref fresh-tested PASS.

This is a hygiene certification only, not a content review. It establishes that no fork moved or arrived untested this wave, and that every archive tip pins exactly what the record says it pins.
