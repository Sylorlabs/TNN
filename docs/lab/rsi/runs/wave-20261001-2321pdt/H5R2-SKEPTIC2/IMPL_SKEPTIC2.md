# H5R2-SKEPTIC2 Implementation Record

Lane H5R2-SKEPTIC2, wave-20261001-2321pdt. Implements the frozen prereg
PREREG_SKEPTIC2.md (freeze commit 709e1e82e on branch
lane-h5r2-skeptic2, 2026-10-02 ~07:16 UTC; the branch was created from
detached HEAD because concurrent workers held the tnn-native-lab
working tree dirty, see section 5). Pure Zag, safebin toolchain,
`which python3` prints nothing (exit 1) at every check. Zero
forbidden-executable invocations.

## 1. Skeptic arm: NEWEST-LIVE-ON-KEY (bl_newest.zag)

Base: the committed H5R2 source extracted via git show from
9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a
(matches the frozen substrate hash; verified before editing).

Change vs the base (mechanical, per the prereg appendix):
1. Replaced the t2_prov_ok comment block + function (file lines
   508-521) with sk2_newest_on_key + t2_newest_live_ok (exact code as
   frozen in the prereg appendix).
2. The four t2_trial promote sites changed `t2_prov_ok(` to
   `t2_newest_live_ok(` (sed, all four sites).

Verification: `diff` of bl_newest.zag against the verified H5R2 base
shows only the gate block replacement and the four call-site lines
changed (47 diff lines total); one remaining `t2_prov_ok` mention is
inside the new explanatory comment, intentional. No working-tree file
was used as a build input.

SHA-256 of bl_newest.zag:
e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649

Build: pinned znc src/tools/toolchain/znc_linux_x86_64_abed8aa1,
exit 0, zero errors (only pre-existing A0102 warnings, same family as
the baseline lane reported).

## 2. Chained decoy fragment (CHAIN_FRAG.zag)

Written post-prereg to the frozen spec in PREREG_SKEPTIC2.md section 2:
sk2_fact_live_id (single live tag-1 fact on a key), sk2_cdcy (the
CD-check: sup==2, one live MAP with f28==c0, every DEP target live
tag-1 non-superseded, no DEP target is either decoy fact, DEP hits
both the b-level live fact on (b,RF2) and the a-level live fact on
(a,RF1)), sk2_cd_probe (P1, contradict, P2, revert, a-level decoy,
a-level D-ANS, b-level decoy, b-level D-ANS, P3, CD-check),
sealed_main_e1 / sealed_main_e2 with the frozen seeds, key ranges, and
object values (e1 vo=6, e2 vo=0).

SHA-256 of CHAIN_FRAG.zag:
6d3c767600bf06340d7d6eafd6a8b4317114df0feab4a70fed810f832552abd1

## 3. Pre-sealed smoke verification (in /tmp, not committed)

Assembled smoke worlds per the frozen 7.1 rule on world e1 for four
arms and ran once each:
- H5R2: 4/4 "CD ok", 4/4 D-ANS-A ok, 4/4 D-ANS-B ok, DONE-OK. White-box
  trace: live MAP DEP edges to the (a,RF1) fact and the reverted
  (b,RF2) fact; both decoy facts untouched.
- NEWEST-LIVE-ON-KEY: 4/4 "CD ok", DONE-OK. Matches H5R2 exactly.
- REVERT-TO-LATEST: 0/4 "CD ok"; CD-DECOY-FAIL + CD-AKEY-FAIL +
  CD-KEY-FAIL on all 4 probes (decoy-anchored at both chain levels,
  the pre-registered failure signature).
- NO-GATE: 0/4 "CD ok"; CD-DEP-FAIL on all 4 probes (stale original
  anchor, its baseline-lane failure mode).
All D-ANS checks passed on all arms. The sealed evaluation below
re-assembles all worlds from the committed sources; the smoke
assemblies are discarded.

## 4. Other arms (unchanged, extracted read-only)

- H5R2 substrate: 9db334bd4, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a.
- REVERT-TO-LATEST / NO-GATE / RANDOM-ANCHOR: 1203b865d, SHA-256
  d929d50c3b3499b4c1b17bcd9e1319eecf4044f9fb96125e01de35ad1d520220,
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384,
  c03b4575993ecbdb3a851c75972f4281e210340f90d0c7c6622b8160cf1a0ee1.

## 5. Branch note

At lane start the repo was on tnn-native-lab, but concurrent workers
left the working tree dirty (other lanes' uncommitted files) and a
stale index.lock; checkout of tnn-native-lab for the cherry-pick was
blocked to avoid overwriting their files. The prereg freeze commit
709e1e82e was therefore kept on the new branch lane-h5r2-skeptic2
(diverged from tnn-native-lab at 5223efefa). All lane commits are
local-only, under
docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-SKEPTIC2/ only, never
pushed. The parent orchestrator can fast-forward or cherry-pick the
lane branch onto tnn-native-lab when the tree is quiet.

## 6. Deviations from the prereg

None. Ordering: prereg freeze commit 709e1e82e strictly precedes this
implementation commit.
