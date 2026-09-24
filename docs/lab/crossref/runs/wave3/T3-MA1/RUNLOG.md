# RUNLOG T3-MA1 (crew)
Started: 2026-09-24 ~00:33 PDT

Local prereg sha256: 538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1
Frozen: 2026-09-22 per file header (line 3)

## Prereg verification
- Local sha256 of crossref/PREREG_TIER3.md: 538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1
- Committed blob on tnn-native-lab (repo path docs/lab/crossref/PREREG_TIER3.md): blob sha 943ab5c984cd16b4a618bbc94329780b2d425a68, sha256 of blob content == local sha256. FROZEN INTACT — no STOP condition.
- T3-MA1 section extracted programmatically (sed -n '7,13p'). Decisive bars: CORE-unkillable attempts (all must fail), kill/pin/promote deliberate ops on a sample, audit replay to exact state on a sample, determinism of the check battery. REPRODUCED rule: 58/58 count re-derives AND every spot-rerun decisive bar passes.

## Verdict-commit pin check (task orientation pins e8f97d28 / 1a24c9b9 / 06bc7da2)
- GitHub API /repos/sylorlabs/TNN/commits/<short-sha>: 422 "No commit found" for all three.
- Fresh blob:none clone of sylorlabs/TNN, all 5 branches fetched (main, r2-7, reorg/phase-0-1, tnn-native-lab, wg-freeze): `git cat-file -t` -> "Not a valid object name" for all three as any object type. PINS DO NOT EXIST anywhere in repo history. ANOMALY (reported; work continues on the true MA1 lineage per prereg re-derive rule).
- True MA1 lineage (all ancestors of tnn-native-lab):
  - a0f0a60513bb3c2e7642b3ddd113b67553369120 (2026-09-19) "lab(wave2): memory agency — survey, ops, safety, MA1 trial 58/58" — matches memory/2026-09-19.md record of the MA1 verdict commit.
  - e4d1c458ea3b1a430e6396a38f1079db0e376788 (2026-09-24 00:20) "REPAIR: MA1 MA_CAP 8->256 regression — trial.zag restored to 8-slot spec (54/58 -> 58/58)". Root cause: after 2026-09-19 run, MA_CAP raised 8->256 for MA2/MA3; as-committed reruns scored 54/58; repair trial.zag only (ma_add_lim cap=8 discipline + bad-slot probe at slot MA_CAP). Re-verified 58/58, 3x byte-identical, byte-identical to 2026-09-19 evidence run per repair note.
  - 23a02a19f49a9a9847170e1f81d8532403094252 (2026-09-19) "lab(wave2): post-table context mechanism — HT1 trial 11/11 PASS" (per memory/2026-09-19.md#L133 record).
- tnn-native-lab branch head: API 77611bee4f0a68f10e1ea00dd689558d1516ee90 at ~00:40; local fetch head 5cd2b9679f914313067d3e29c45c1bf4360cffb5 at ~01:10 (branch active; MA1/posttable files unchanged since the commits above — blob-verified below).

## Clean checkout + blob SHA verification (checked out from origin/tnn-native-lab)
- docs/lab/wave2/memoryagency/trial/trial.zag: MATCH 20551fbd9d1af16f4c8253e10f93de99b0f24418
- docs/lab/wave2/memoryagency/trial/memory_core.zag: MATCH 90c8777b57b24a44c5e27d6fb170d363da054273
- docs/lab/wave2/memoryagency/trial/ma_common.zag: MATCH 58e90e7b392ec04c444e9816f3b1adb514f8bebe
- docs/lab/wave2/posttable/ctx/trial_ht1.zag: MATCH 537021a9bcc48ce7998a6d5cdf0a48859093a53b
- docs/lab/wave2/posttable/ctx/ctx_core.zag: MATCH 1365f0f3c1cd2816c86857698fb22db1179ad4e8
- docs/lab/wave2/posttable/ctx/toy_core.zag: MATCH 9cd8b0b786818307bd715027a25155297633dedb
- Substrate files (R33_NATIVE_IO_V1.zag, R33_NATIVE_SHA256_V2.zag, cl/common.zag) present per commit 23a02a19/e4d1c458 stat.
- Compiler: pinned ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (exists).

## Spot rerun 1: MA1 trial (audit replay to exact state)
- Compiled trial.zag native, exit 0. Ran 3x.
- Run outputs byte-identical x3: sha256 244907dab4283dd7d53b44e6f0686ac571461a2b74b3977104b539af42131d06
- 58 CL_CHECK lines: 58 pass, 0 bad. MA_FAILURES,0, exit 0 x3.
- Decisive bars: kill_core_refused=REFUSED_CORE (CORE unkillable) PASS; pin2_ok/kill0_ok/promote3_ok PASS; ledger_replay (replay all 28 audit entries from genesis == exact live state) PASS; determinism 3x byte-identical PASS.
- My run1.stdout is BYTE-IDENTICAL to committed EVIDENCE_20260924T071512Z/run.stdout (the repair commit's evidence).

## Spot rerun 2: HT1 context-switching curriculum (11/11)
- Compiled trial_ht1.zag native, exit 0. Ran 3x.
- Run outputs byte-identical x3: sha256 11bde0aab928d21a45d10ef87df092b074fe8a345cc64b36a7da3cb0a08cafb0
- 11/11 CL_CHECK pass, HT1_FAILURES,0, exit 0 x3.
- CTX arm: 11 switches for 10 true flips, 0 collapsed blocks, endpoints 16/16 both regimes. Toy arm (R34 v3 negative control): 357 switches, 2 collapsed 0/16 blocks, endpoint R1 0/16 (regime destroyed). Matches committed TRIAL_RESULTS_HT1.md (11/11, HT1_FAILURES,0) number-for-number.
- Curriculum "randomness" is fixed LCG seed literals in source (rng_flip=91001, rng_ctx=92002, rng_toy=93003) — environment-side fixture, not decision-path RNG. CTX decision path deterministic (byte-identical x3 proves it).
- Note: 23a02a19 did not commit an EVIDENCE_* dir for HT1; comparison is against TRIAL_RESULTS_HT1.md record + 3x self-determinism.

## Verdict
SPOT-REPRODUCED. 58/58 count re-derives from committed sources; every prereg-named decisive bar passes on spot rerun (3x byte-identical each); HT1 11/11 reproduces number-for-number. Anomaly: task pins e8f97d28/1a24c9b9/06bc7da2 do not exist in any branch of sylorlabs/TNN; true MA1 lineage (a0f0a605, e4d1c458 repair, 23a02a19) substituted and verified.
