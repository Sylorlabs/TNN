# EVAL_SKEPTIC2: sealed evaluation on the chained decoy world family

Lane H5R2-SKEPTIC2, wave-20261001-2321pdt. Evaluator: the lane worker.
Implements the frozen protocol in PREREG_SKEPTIC2.md (freeze commit
709e1e82e, 2026-10-02 ~07:16 UTC; implementation commit f461e812d,
07:19:22 UTC; ordering clean). Pure Zag; safebin PATH; `which python3`
printed nothing at lane startup and at every check (NAMECHECK.md Step
0); zero forbidden-executable invocations.

## Compared arms

- H5R2 (t2_prov_ok provenance gate): substrate extracted via git show
  from 9db334bd4a01d21cce52da3bb2a1c45a10c4c172, SHA-256
  04f8e213bbbb165d101449d0dbcf57e06762c7a8ac56ce4ef8e2bc5cbdaf744a.
- NEWEST-LIVE-ON-KEY (stronger skeptic): built in this lane from the
  H5R2 base per the frozen prereg appendix (diff-verified: only the
  gate block and the four call sites differ), SHA-256
  e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649.
- REVERT-TO-LATEST, NO-GATE, RANDOM-ANCHOR: substrates extracted via
  git show from 1203b865d352ae8ba380f57350218edd4d637b3a, SHA-256
  d929d50c3b3499b4c1b17bcd9e1319eecf4044f9fb96125e01de35ad1d520220,
  d98d08f0746cab4fef88fb062933a314c12492f78ee98b496e8d8912cd7fd384,
  c03b4575993ecbdb3a851c75972f4281e210340f90d0c7c6622b8160cf1a0ee1.
  No working-tree file was used as a build input for the four
  committed sources.

## World files (assembled post-implementation, per prereg 7.1)

Byte-copy of each arm substrate with the single main line changed
(diff-verified: exactly one line differs), plus the frozen
DRIVER_TMPL.zag appended (SHA-256
f2d60568f55aef62d27d260a7ca3966933738b864b645e6c1e5e1cbfa1ea20af,
extracted from 9db334bd4), plus CHAIN_FRAG.zag from the implementation
commit f461e812d (SHA-256
6d3c767600bf06340d7d6eafd6a8b4317114df0feab4a70fed810f832552abd1),
plus the world alias line. Pre-run SHA-256:

- h5r2_e1.zag 522631bebbb12aab29f89c9c31774a515ae10a53bb4786a9db6f9c94950968a8
- h5r2_e2.zag fa1948daa1c0c1099dbdb29934d5100e588a740b3d19b3d73617b486b744cb4a
- bl_newest_e1.zag 13083097a903f241975a5cdde7d1f937b5f4b326369ce3c27327a5888d29a68d
- bl_newest_e2.zag 318134bd3a8843b038b13fcdc6ba0589a9dbbf046c78636bb08154f4ade4a869
- bl_latest_e1.zag 20848e000c923428e7b5fb9b92538fb625c01e3318f2be76314e8fc6441459ad
- bl_latest_e2.zag ae08ec151d47f4e4e4a541aefe2fd4fbdffaa8dfe45815e653d30813a76b81b8
- bl_nogate_e1.zag b148fe9d1a7016f96874b5d8a19c1b33372747f35b36555aca87fa25c092a5cc
- bl_nogate_e2.zag 6273161048a8f451c33801326c19da335e7b9183e14451e285524e514583f3e6
- bl_random_e1.zag 83b919c9a3672779addc7a2e055fcae91a0c959775e8470a3dea1b198dd4218a
- bl_random_e2.zag f324390a4044a2490d477c46d1cdfe8e0735e5274f24596e05b6d9127280a0ea

Each world compiled separately with the pinned znc (exit 0, zero
errors); 3/3 runs; full-stdout SHA-256 (identical across the 3 runs in
every world):

- h5r2_e1 fd022beb77ca71489b0050598e6068bbfdb77bf928aa153fb3d47042d6b130bc
- h5r2_e2 8ce4fddf1516e3fedcc9944c062b3077a0aea1ca1ce308e321e19ac78a81d905
- bl_newest_e1 fd022beb77ca71489b0050598e6068bbfdb77bf928aa153fb3d47042d6b130bc
- bl_newest_e2 8ce4fddf1516e3fedcc9944c062b3077a0aea1ca1ce308e321e19ac78a81d905
- bl_latest_e1 f86387058dc8f68457d9869099d997847c779b8deecbbb8201680491c59d0128
- bl_latest_e2 cc0deea2a87b0a8dda53372a3930e2671ca07079f81db15367a04644861591a4
- bl_nogate_e1 4683537a664d31a86d2b7a9c55ea5c4f45a014d5ad030c6af65d9c905405ae9f
- bl_nogate_e2 a6258110f74fe84d48f3d95ed2ebe9bca5c61d6f9999c318512a4c1d834ec9f4
- bl_random_e1 abf06a323f75cb0082f5612272382108d26bd0bd0a9ab78c8a3155aa9b196996
- bl_random_e2 8128750b3e6f38b82a00a0c8347ed253cf4c917f258635733309ef6a6de56c83

Exit codes: h5r2_* and bl_newest_* exited 1 (all checks passed; the
driver's ok polarity), all old baselines exited 0 (CD-check failures,
see below). Every run completed and dumped. Note: the skeptic's
full-stdout hashes are byte-identical to H5R2's on both worlds.

## SB-4 (determinism): PASS for all arms

3/3 byte-identical full-stdout runs per arm per world (table above).
No nondeterminism anywhere.

## Marker scores (run 1; runs 2-3 byte-identical)

Per world: "CD ok" / "D-ANS-A ok" / "D-ANS-B ok" / CD-DECOY-FAIL /
CD-DEP-FAIL / CD-KEY-FAIL / CD-AKEY-FAIL / other CD-*-FAIL / VAL-FAIL /
DONE-OK:

- h5r2_e1: 4 / 4 / 4 / 0 / 0 / 0 / 0 / 0 / 0 / DONE-OK
- h5r2_e2: 4 / 4 / 4 / 0 / 0 / 0 / 0 / 0 / 0 / DONE-OK
- bl_newest_e1: 4 / 4 / 4 / 0 / 0 / 0 / 0 / 0 / 0 / DONE-OK
- bl_newest_e2: 4 / 4 / 4 / 0 / 0 / 0 / 0 / 0 / 0 / DONE-OK
- bl_latest_e1: 0 / 4 / 4 / 4 / 0 / 4 / 4 / 0 / 0 / DONE-FAIL
- bl_latest_e2: 0 / 4 / 4 / 4 / 0 / 4 / 4 / 0 / 0 / DONE-FAIL
- bl_nogate_e1: 0 / 4 / 4 / 0 / 4 / 4 / 0 / 0 / 0 / DONE-FAIL
- bl_nogate_e2: 0 / 4 / 4 / 0 / 4 / 4 / 0 / 0 / 0 / DONE-FAIL
- bl_random_e1: 0 / 4 / 4 / 1 / 3 / 3 / 1 / 0 / 0 / DONE-FAIL
- bl_random_e2: 0 / 4 / 4 / 1 / 3 / 3 / 1 / 0 / 0 / DONE-FAIL

Bar totals (8 chained probes: 4 per world):

| bar | H5R2 | NEWEST-LIVE-ON-KEY | REVERT-TO-LATEST | NO-GATE | RANDOM-ANCHOR |
|---|---|---|---|---|---|
| CD ok (target 8) | 8/8 | 8/8 | 0/8 | 0/8 | 0/8 |
| D-ANS-A ok (target 8) | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 |
| D-ANS-B ok (target 8) | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 |
| CD-DECOY-FAIL | 0 | 0 | 8 | 0 | 2 |
| CD-DEP-FAIL (stale) | 0 | 0 | 0 | 8 | 6 |
| CD-KEY-FAIL | 0 | 0 | 8 | 8 | 6 |
| CD-AKEY-FAIL | 0 | 0 | 8 | 0 | 2 |
| VAL-FAIL | 0 | 0 | 0 | 0 | 0 |

## What each arm shows (white-box samples, e1 P1)

- H5R2: `CD sup=2 liveid=66 decoy_a=37 decoy_b=38 klive=36 alive=2`,
  `CD dep->2 tag=1 s=89101 r=8901 o=89301 sup=0`,
  `CD dep->36 tag=1 s=89301 r=8902 o=89407 sup=0`: the revert MAP
  anchors to the live (a,RF1) fact and the live reverted fact on
  K=(b,8902); both decoy facts untouched. CD ok on all 8 probes.
- NEWEST-LIVE-ON-KEY: byte-identical stdout to H5R2 on both worlds
  (same full-stdout SHA-256). Its revert MAP anchors to exactly the
  same facts: the newest live fact on each chain-link key coincides
  with the gate's promoted candidate on every chained probe.
- REVERT-TO-LATEST: `CD dep->28 tag=1 s=89101 r=8905 o=89301 sup=0`,
  `CD dep->29 tag=1 s=89301 r=8904 o=89407 sup=0`: the revert MAP
  anchors to the decoy facts at BOTH chain levels (r=8905 a-level,
  r=8904 b-level). CD-DECOY-FAIL + CD-AKEY-FAIL + CD-KEY-FAIL on all 8
  probes: the pre-registered recency failure signature, now at every
  level. Value answers all correct (VAL-FAIL 0): provenance-only
  failure, as in the decoy lane.
- NO-GATE: `CD dep->2 ... sup=0`, `CD dep->3 tag=1 s=89301 r=8902
  o=89407 sup=1`: anchors to the live a-fact and the superseded
  original b-fact. CD-DEP-FAIL on all 8 probes: its baseline-lane
  failure mode, unchanged.
- RANDOM-ANCHOR: 0/8 CD ok; the 8 failures split 2 decoy-anchored and
  6 stale-anchored, chance-level over the 6 verifying candidates
  (expected about 1.3/8; observed 0/8 is within chance).

## Frozen kill bars

- SB-1 (H5R2 8/8 CD ok): PASS. The gate's discrimination holds at
  every chain level: with decoys at both links, every revert MAP still
  anchors to the live chain facts, never either decoy.
- SB-2 (skeptic pre-registered to match): SB-2-MATCH holds with 8/8
  "CD ok", exactly as pre-registered (the gate's promoted candidate
  is the skeptic's first verifying eligible candidate on every
  probe). No failure signature, no UNEXPECTED-SIGNATURE.
- SB-3 (old arms behave as before): PASS. REVERT-TO-LATEST 0/8 with
  CD-DECOY-FAIL on 8/8 (>=5/8); NO-GATE 0/8 via CD-DEP-FAIL on 8/8;
  RANDOM-ANCHOR 0/8 < 8/8.
- SB-4 (3/3 byte-identical): PASS for all 10 worlds.
- SB-5 (D-ANS-A ok and D-ANS-B ok 8/8 on all 5 arms): PASS. Both decoy
  facts are genuine live facts on every arm; no world is
  adversarial-by-brokenness.

## Verdict: SKEPTIC-SURVIVES

All five frozen kill bars hold, with SB-2 landing on the
pre-registered MATCH outcome. The stronger skeptic the decoy lane
recommended survives the chained decoy family: NEWEST-LIVE-ON-KEY
matches H5R2 8/8 with byte-identical full stdout on both worlds. The
t2_prov_ok gate's necessity is therefore still unproven against THIS
skeptic. This is reported honestly: the gate beat recency, no-gate,
and chance, but not the per-key newest-live heuristic.

The next discriminating world family (named per the frozen decision
rule): one where the node-id-first all-live candidate licenses a
live-but-not-newest fact on some chain key while the key-newest live
fact licenses a later-enumerated candidate. In the current substrate
each chain key holds at most one live fact (contradiction supersedes),
so constructing such a world requires an event sequence that leaves
two live facts on one key, e.g. a re-teach path that does not trigger
supersession. Whether that is constructible without breaking the
frozen event semantics is the open question for the next lane.

## Negative controls

NC-S0: no world was VOID; all 10 assemblies verified per the frozen
rule (exactly one line differs from each arm substrate). NC-S1: no
forbidden-executable invocation (PROCESS-FAIL not triggered). NC-S2:
prereg freeze commit 709e1e82e (~07:16 UTC) strictly precedes
implementation commit f461e812d (07:19:22 UTC) strictly precedes this
eval; ordering clean.

## Process incident (git hygiene, disclosed)

The implementation commit f461e812d swept thousands of unrelated
staged deletions into its tree: another worker had staged mass
deletions in the shared index, and a concurrent `git checkout`
moved HEAD from the lane branch to tnn-native-lab mid-commit, so the
commit landed on tnn-native-lab instead of lane-h5r2-skeptic2. Two
lanes (BATTERY-E4, F2V3) restored their files in follow-up commits;
a lane-audit worker is verifying the rest. The lane's own files in
that commit are exactly the three intended (bl_newest.zag,
CHAIN_FRAG.zag, IMPL_SKEPTIC2.md); no lane content was lost. The
wave coordinator's hygiene rule is now in force for this lane:
explicit-path staging only under the lane directory, `git status
--short` verification before every commit, `git reset -- <path>`
(never bare) to unstage anything outside the lane dir. The sealed
evaluation above is unaffected: all sources were hash-verified before
assembly.

## Evidence paths

- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-SKEPTIC2/sealed/
  (10 assembled world files + 10 compiled world binaries)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-SKEPTIC2/CHAIN_FRAG.zag
  (chained decoy probe implementation, SHA-256
  6d3c767600bf06340d7d6eafd6a8b4317114df0feab4a70fed810f832552abd1)
- docs/lab/rsi/runs/wave-20261001-2321pdt/H5R2-SKEPTIC2/bl_newest.zag
  (skeptic substrate, SHA-256
  e5df3ddb28858b60efb01f3d8df524a98ce79686e199532e53713c24f367b649)
- stdout hashes in the table above (run 1 = run 2 = run 3 per world)
