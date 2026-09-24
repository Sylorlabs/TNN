# RUNLOG — T3-WAVE5 (truthfulness wave verification-of-record)

Crew: T3-WAVE5. Frozen prereg: ~/workspace/tnn-lab/crossref/PREREG_TIER3.md
"## T3-WAVE5" section extracted programmatically (sed -n 35,45p).

## Frozen-record verification
- Local PREREG_TIER3.md sha256: 538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1
- Local git blob sha: 943ab5c984cd16b4a618bbc94329780b2d425a68
- Remote blob sha (docs/lab/crossref/PREREG_TIER3.md @ tnn-native-lab): 943ab5c984cd16b4a618bbc94329780b2d425a68 — MATCH.

## Commit verification (task step a)
- Task-named commit `a6cccf1e` ("26 commits verified at a6cccf1e (3f1b0f6...)"):
  NOT FOUND. GitHub API /repos/sylorlabs/tnn/commits/a6cccf1e → 422 "No commit found for SHA".
  Same 422 on sylorlabs/zag. Workspace-wide grep for "a6cccf1e" → zero hits.
  Branch head of tnn-native-lab is actively moving during this run (seen: 16400e32, 46ed8063, 5cd2b967).
  → Verification-of-record proceeds against the live tnn-native-lab head (recorded below);
  the a6cccf1e identifier is treated as stale/mistranscribed, not as a blocker.
- Branch head at evidence time: 5cd2b9679f914313067d3e29c45c1bf4360cffb5 (from git/trees ref resolution).

## Source verification (task step b, blob-level)
docs/lab/wave5/deliberative-refusal/ @ tnn-native-lab vs local mirror (git hash-object):

| file | remote blob sha | local blob sha | match |
|---|---|---|---|
| DESIGN.md | 5814cd98309fc73ad34fbf83219d17cd410f8943 | 5814cd98309fc73ad34fbf83219d17cd410f8943 | yes |
| PREREG.md | a252bb4b247effc8b6f8c40eda545eba48b457aa | a252bb4b247effc8b6f8c40eda545eba48b457aa | yes |
| TRIAL_RESULTS.md | 7a578a7edf3b1507b6d9b85bc69e874c052de31f | 7a578a7edf3b1507b6d9b85bc69e874c052de31f | yes |
| dr.zag | 3f6ea9fb667e0f9746dd987c64426defe0ea04f2 | 3f6ea9fb667e0f9746dd987c64426defe0ea04f2 | yes |
| run_dr.sh | 08d4002336008792a411f7af31b2ee3e918fba6d | 08d4002336008792a411f7af31b2ee3e918fba6d | yes |

- evidence/ is NOT committed (404 on contents API) — committed evidence = TRIAL_RESULTS.md + code.
- Build source for spot rerun: local dr.zag (blob-verified identical to committed) copied to scratch.

## Spot rerun (decisive cell: main legs, 10x + 100x, 2 runs each, byte-identical)
- Toolchain: ~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 (pinned).
- Compile: clean, exit 0, binary 177,464 bytes (not committed).
- 10x: two runs, exit 0/0, cmp clean → BYTE-IDENTICAL.
- 100x: two runs, exit 0/0, cmp clean → BYTE-IDENTICAL.
- 10x result: DR_SUMMARY,blocks,200,entries,5818,min_hold,1000,takes,0,0,0,0,net,15535,strengths,60,150,50,109
  (exact match to committed TRIAL_RESULTS.md). CL_CHECK,offers,255,255. DR_FAILURES,0.
- 100x result: DR_SUMMARY,blocks,2000,entries,58018,min_hold,1000,takes,0,0,0,0,net,147835,strengths,150,150,50,150
  (exact match to committed TRIAL_RESULTS.md). CL_CHECK,offers,2595,2595 → all 2,595 temptations refused.
  DR_FAILURES,0.
- no-RNG static grep on build source: clean.
- Rerun log SHAs: 10x ea2dd12d12fa3ab4dac9b2f4b94a3c173dfe8b39687646a0e57c286b9306cf6e;
  100x b1e48248dd76c8e70185bfe746081561775a2dece12a01310ba761c848c89103.
- Both rerun logs byte-identical to mirror evidence/ logs (dr_10x_a.log, dr_100x_a.log);
  note those evidence logs are NOT committed remotely — fidelity to recorded evidence only.
- Build source: local dr.zag (blob-verified 3f6ea9fb667e0f9746dd987c64426defe0ea04f2, identical to committed).
- .zag-cache/.zagd.semantic-ready artifacts produced by the compiler were left out of the commit.

## Strength-trial rulings 3–5 pending-status record
- wave5/strength-trial-run/BLOCKED_REPORT.md: defects 1–3 (implant indexing/amended closed forms)
  plus clarifications C1 (static-check scope) and C2 (force-pin INVALID vs ledgered refusal, resolved in code)
  require Micah's ruling; "No binary was produced. No trial cell was executed. No git push."
- Pending status VERIFIED-OF-RECORD. Not settled (out of scope for this crew).

## Verdict
SPOT-REPRODUCED. See VERDICT.md.
(to be committed under crossref/runs/wave3/T3-WAVE5/ on tnn-native-lab)
