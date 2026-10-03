# H-FDCR-UNIFIED8 Red Team: Adversary Result
**Date:** 2026-09-30
**Prereg:** PREREG_FDCR_UNIFIED8_ADV.md (commit 25af0b2c9, FROZEN)
**Builder claim:** SURVIVES 51/51 (result 11918217a)
**Adversary verdict:** SURVIVES (with documentation precision defects noted)

## Method

Pure Zag adversary harness `unified_fdcr8_adv.zag` (mechanism extracted lines 1-2304 from the committed target source, plus frozen attacks X-FU8-1a, 1b, 2, and amended boundary probes 4b/4c). Frozen prereg commit 25af0b2c9 precedes all execution. Three independent runs, byte-identical (md5 437a90d7a926ee69fa8c1d25b2d5b3b6).

Attacks target the new H-FDCR-UNIFIED8 machinery (R8 lifetime distinct-overflow array ovl, R8b current overflow-name table OVN, R8c lifetime restoration, R8d event-to-overflow transfer, R8e OVN-full event path) that closed the FU7 kill findings.

## Frozen results

**X-FU8-1a (main-list excursion + interleaved lifetime restoration): 6/6 PASS.** Main drop list filled (64), subject f1 evicted to OVN with ovl tracking, then main-list subject g1 membered into pet to free a main slot, f2 taught through the freed main slot, and f1 re-dropped. f1 restored via R8c without recounting. Final: total 130, ov 64, ov2 0. The main-list/OVN interleaving does not break the lifetime distinctness invariant.

**X-FU8-1b (lifetime restoration with full OVN): 6/6 PASS.** Full 64/64 OVN, subject e33 membered (frees one OVN slot), re-dropped, and the single OVN slot is immediately re-consumed by the restored e33; a fresh subject h1 then drops and is counted as a NEW distinct overflow subject (ov 64->65). Total 130, ov 65, ov2 0. No double-count of e33, no under-count of h1.

**X-FU8-2 (event-to-named transfer, B-FU7-2 closure): 6/6 PASS.** 56 membered into 7 concepts (a1-a7); 56 single events each for h1 and h2 counted in ov2; h1 membered and merged, h2 membered and merged; h1 re-dropped post-merge. Final: ov 66, ov2 0, total 130. Transfer subtracts recorded event counts from ov2 and adds exactly one distinct subject to ov.

**X-FU8-3 (source lineage, regression, determinism):**
- Builder result file: absent from branch tnn-native-lab as of 2026-09-30 (checked, file not found); RESULT.md claims were compared against source comments and the overnight-20260928 directory listing only.
- Mechanism extracted from committed target source lines 1-2304; extracted mechanism md5 fa33e85b1fb7fb2e47e69a09b5899cac. Prereg recorded builder raw md5 6ae1d1e5716e09d0a07beb3dee420d68 for the claimed builder main; the adversary did not reconstruct the builder main, so raw equality could not be verified here.
- Determinism: 3/3 runs byte-identical (md5 437a90d7a926ee69fa8c1d25b2d5b3b6).
- Regression: mechanism region contains no test-harness overrides of the R8 machinery; the R8 comments are present in the committed source.

**X-FU8-4 (frozen 128-entry boundary): SETUP-INFEASIBLE, not a mechanism finding.** The frozen fixture assumed 8 new clearing concepts were available, but CON_MAX()==8 includes pet, leaving only 7 (56 member slots). 5 of 6 assertions failed on fixture counts (56 subjects cleared instead of 64, ov 120/ov2 8 instead of 128/0). Never retroactively altered.

## Boundary investigation (amended probes, clearly labeled)

X-FU8-4b (7-concept/56-slot corrected design) reached ovl=106 with 22 event-tier subjects; h1 admitted as lifetime entry 107 and correctly NOT recounted on merge (8/9, merge "failure" was the fixture expecting a recount that the correct mechanism does not produce). X-FU8-4c attempted a 128 fill via the OVN-full evl path and exposed the actual architecture: the OVN-full R8e path calls noadd_drop_evl_add (NOT ovl_add), so subjects that overflow while OVN is full never enter the lifetime array. ovl grows only through the OVN-free path and R8d transfers.

**Consequence: with CON_MAX()==8, maximum reachable ovl occupancy is 120 (64 via initial OVN fill + 56 via the 7 memberable concepts), not 128.** The documented 128-entry lifetime boundary is beyond the reachable state space under current capacity constants. The mechanism therefore never encounters the recount window it documents; within the reachable range it never recounts a lifetime-tracked subject. This is a documentation precision defect, not a counting bug.

## Documentation precision defects (no counting impact)

1. RESULT.md "fail loudly by construction" for the lifetime lists is inaccurate: noadd_drop_ovl_add and noadd_drop_evl_add contain zero emits on their silent-full paths (verified by grep: 0 emits). When full they silently return. All other overflows warn loudly; these two do not.
2. The 128-entry lifetime boundary is unreachable (max 120 under CON_MAX=8). The bound as stated cannot be triggered.
3. R8e OVN-full path increments ov2 even when evl_add returns -1 (subject untracked); those events can never transfer via R8d. Per-note honest (counts events), but worth stating plainly.

## Score

27/39 PASS overall. All 18 frozen adversary assertions (X-FU8-1a/1b/2) PASS. Failures are fixture-design issues (X-FU8-4 frozen infeasibility, X-FU8-4b/4c amendment miscounts), not mechanism counting failures. No kill established.

## Evidence

- FDCR_UNIFIED8_ADV_RAW.txt (raw output, 3/3 identical, md5 437a90d7a926ee69fa8c1d25b2d5b3b6)
- unified_fdcr8_adv.zag (harness + extracted mechanism)
- Prereg: commit 25af0b2c9
