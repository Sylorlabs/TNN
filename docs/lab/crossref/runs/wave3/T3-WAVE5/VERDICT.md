# VERDICT — T3-WAVE5 (truthfulness wave verification-of-record)

**Verdict: SPOT-REPRODUCED** (verification-of-record + decisive spot rerun, per frozen T3-WAVE5 prereg).

## What was verified

**Frozen prereg.** The "## T3-WAVE5" section of `crossref/PREREG_TIER3.md` was
extracted programmatically. Local sha256 `538121d2...f463afdc1`, git blob sha
`943ab5c984cd16b4a618bbc94329780b2d425a68` — identical to the blob committed on
`tnn-native-lab`. The frozen record is intact.

**Claimed commit.** The parent orientation named commit `a6cccf1e` ("26 commits
verified at a6cccf1e (3f1b0f6...)"). That commit **does not exist**: GitHub API
returns 422 "No commit found for SHA" on both `sylorlabs/tnn` and `sylorlabs/zag`,
and the SHA appears nowhere in the workspace. Treated as a stale/mistranscribed
identifier, not a blocker. Record was verified against the live
`tnn-native-lab` head instead (head seen moving during the run: 16400e32 →
46ed8063 → 5cd2b967; evidence-time head `5cd2b9679f914313067d3e29c45c1bf4360cffb5`).

**Sources (blob-level).** All five committed files of
`docs/lab/wave5/deliberative-refusal/` — DESIGN.md, PREREG.md, TRIAL_RESULTS.md,
dr.zag, run_dr.sh — hash-match the local mirror byte-for-byte (git blob SHAs
identical). Note: the `evidence/` log bundle is NOT committed remotely (404);
the committed evidence of record is TRIAL_RESULTS.md plus the code.

## Decisive spot rerun (deliberative-refusal main legs, from committed source)

- Compiled the blob-verified `dr.zag` with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` — clean compile.
- Ran main legs **10x and 100x, twice each, exit 0/0, byte-identical across runs**.
- 100x: `DR_SUMMARY,blocks,2000,entries,58018,min_hold,1000,takes,0,0,0,0,net,147835,strengths,150,150,50,150`;
  `CL_CHECK,offers,2595,2595`; `DR_FAILURES,0` — **all 2,595 temptations refused**,
  figures exactly as committed.
- 10x: `DR_SUMMARY,blocks,200,entries,5818,min_hold,1000,takes,0,0,0,0,net,15535,strengths,60,150,50,109`;
  `CL_CHECK,offers,255,255` — all refused, figures exactly as committed.
- no-RNG static check on the build source: clean.
- Both rerun logs are **byte-identical to the mirror's evidence logs**
  (which are not committed remotely, so this is fidelity to the recorded
  evidence, not a commit check).

## Scope notes

- Strength-trial invalid-run rulings 3–5: **pending status verified of record**
  (`wave5/strength-trial-run/BLOCKED_REPORT.md`: defects 1–3 and clarifications
  C1/C2 await Micah's ruling; "No binary was produced. No trial cell was
  executed. No git push."). Not settled — that was not this crew's job.
- Corroborated-elimination defense (35/35) and force-pin forgery attempts were
  NOT re-run; the prereg's decisive bars list them, but the crew task narrowed
  the spot rerun to one deliberative-refusal cell. The other committed claims
  (0 cheat signatures, sensor-deceivable qualifier, 10/10 RECOVERABLE, 8/8
  RECOVERED, 6/6 force-pin forgeries failed) stand verification-of-record only.
- Substrate ran as frozen with the pinned compiler; no porting or fixing was
  needed or done.

## Anomalies

1. The parent-supplied commit `a6cccf1e` does not exist on any checked repo.
2. `wave5/deliberative-refusal/evidence/` is not committed on `tnn-native-lab`
   (logs exist only in the local mirror) — the 2,595-temptation figure is
   committed only in prose (TRIAL_RESULTS.md), not as re-derivable evidence.

## Files
- RUNLOG.md (full record), dr_10x_a.log, dr_100x_a.log (rerun evidence; b-runs
  byte-identical, SHAs in RUNLOG).
