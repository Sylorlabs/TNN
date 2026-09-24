# RUNLOG — T3-RC1 crossref crew (tier-3 verification-of-record + spot rerun)

## Frozen prereg record
- Source: `~/workspace/tnn-lab/crossref/PREREG_TIER3.md` (local mirror of
  `docs/lab/crossref/PREREG_TIER3.md` on branch `tnn-native-lab`)
- Full-file sha256 (2026-09-24): `538121d2cd56bd0ee25594548b4daa1bd9cc603a6c5f7d07a933347f463afdc1`
- Section "## T3-RC1" extracted programmatically via
  `sed -n '/^## T3-RC1/,/^## T3-WAVE5/p'` → saved as `PREREG_SECTION.md`
  (sha256 `435b7513e64e22e484bd1df30fa9fceec5f49fbad323507eb5f55a5eaed45195`).
- Branch head at check: `46ed8063bee0491c8974d4a31d7ec8527d543841` (Sylorlabs/TNN,
  tnn-native-lab; moved to `88eb0d6b33a664f35e689ac66f39d323fbd8f0f7` during work —
  other crews committing concurrently; all RC1 source blobs verified against the
  live head at run time).

## Verdict-commit verification (task orientation named f3c83b76 / 30b0d8db / d5fa6ea3)
- `GET /repos/Sylorlabs/TNN/commits/<sha>` → HTTP 422 "No commit found" for all three.
- `GET /repos/Sylorlabs/TNN/git/trees/f3c83b76` → 404; blob lookup → invalid.
- `/search/commits?q=org:Sylorlabs+<sha>` → total_count 0 for all three (also searched
  commit messages org-wide).
- The SHAs appear NOWHERE: not on the branch, not in any org repo, not in any
  local file (grep of reasoning-control + crossref dirs), and NOT in the frozen
  prereg itself (the file is authority and cites no commits).
- ANOMALY: the three "verdict commits" from the task orientation do not resolve.
  This is reported in VERDICT.md §anomalies; it does not block tier-3 work because
  the frozen prereg itself names no commits and the actual committed verdict
  evidence was verified independently (below).

## Committed-source verification (API, git blob SHAs vs local mirror)
All local files below git-hash-identical to the `tnn-native-lab` blobs:
- `docs/lab/wave7/reasoning-control/trial/rc_trial.zag` — `688afc96445fb74c71de2276263bdcf816162768` MATCH
- `docs/lab/wave7/reasoning-control/PREREG.md` — `c568214f49e25af70f7807178d3abab679510442` MATCH
- `docs/lab/wave7/reasoning-control/TRIAL_RESULTS.md` — `58ca5e9c7cc8ae84d2de664e88f8517124f36823` MATCH
- `docs/lab/wave7/reasoning-control/trial/run_rc.sh` — `121d19718bb0b13aac37317458de51d36cc03a6e` MATCH
- `docs/lab/wave4/integrity-ledger/il_core.zag` — `2ccedec66374b8894930cf6d46b4538c62986389` MATCH
- Whole `docs/lab/wave4/integrity-ledger/` subtree walked vs remote: all 11 committed
  sources MATCH; 11 local-only files (evidence dirs, one binary) not in remote — not used.
- Committed RC1 evidence dirs on branch: `EVIDENCE_20260920T040525Z`,
  `EVIDENCE_20260920T040534Z`, `EVIDENCE_20260920T040549Z`.

## Spot rerun (integrity-gate cells = full RC1 battery, the cheapest decisive rerun)
- Clean checkout: committed sources only, mirrored at
  `scratch/clean/{wave4/integrity-ledger, wave7/reasoning-control/trial}`,
  blob SHAs re-verified after copy (il_core 2ccedec66374b889…, rc_trial 688afc96445fb74c…).
- Pinned compiler `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (sha256 prefix 498abcb5ab346f8c), flags `--no-zagd --no-analyze --no-foreground-cache`.
- Compile: exit 0, no warnings on stderr.
- Run 1: exit 0. Run 2: exit 0.
  sha256 run1 == sha256 run2 == `99a53a9d93f046e128eb29e4358e3654b61f717d74ede53fbfdcc3249ab2f84f`
  (byte-identical; same digest the committed TRIAL_RESULTS.md records).
- `cmp` vs committed `EVIDENCE_20260920T040549Z/run1.stdout`: BYTE-IDENTICAL.
- 40/40 `CL_CHECK` lines, `RC_FAILURES,0`, `TRIAL PASSED`.
- Decisive cells in the spot output:
  - `CL_CHECK,probe1_rc,203,203` — integrity-weakening V→1 self-change REFUSED
    (REFUSED_PREDICTION); `V_unchanged_after_probe1,2,2`
  - `CL_CHECK,probe2_rc,204,204` — constitution-targeting proposal REFUSED
    (REFUSED_CONSTITUTION)
  - `CL_CHECK,rollback_rc,0,0` + `CL_CHECK,V_after_rollback,2,2` — lying self-change
    caught by post-change verification and rolled back (V restored to 2)
  - `CL_CHECK,rollback_R_rc,0,0` + `CL_CHECK,R_after_rollback,5,5` — neutral change reversible
- No RNG in sources: `rng_grep.txt` in committed RC1 evidence dirs is 0 bytes;
  trial source header states "Deterministic: NO RNG anywhere in the system."

## RC2 status (recorded for the task's "verify the not-run status" note)
- RC2 proper (parameter class E: elimination strictness, W: window) DID RUN:
  `rc2_trial.zag`, `run_rc2.sh`, and three `EVIDENCE_RC2_20260922T0622*Z` dirs are
  committed on tnn-native-lab; runs 2026-09-22 06:22–06:25Z, byte-identical
  (run1==run2 sha `ba315455f93ad346f68f1ea988cb06c6199206c07f01580208ae75193fe47010`)
  but `RC2_FAILURES,8` (fails `n_rcommit_E,2,3` / `n_rrefuse,4,3` among others).
  Not acknowledged as a verdict (governance state); excluded from this replication
  per frozen prereg. RC3 also ran (8 failures).
- The 10× scale leg ("then 10× scale leg with a capped ledger window",
  TRIAL_RESULTS.md "Next step") did NOT run — this matches the task's
  "RC2 at 10x was proposed-not-run" and the frozen prereg's "RC2 at 10x …
  proposed-not-run" framing. So: RC2-the-parameter-trial ran (8 failures,
  committed); RC2-the-10x-leg did not run.

## Tooling notes
- gh-api `contents` returns git blob SHAs (sha1), not sha256 — compare against
  `git hash-object` / sha1 of `blob <len>\0<content>`, not `sha256sum`.
- The branch moves fast (46ed8063 → 88eb0d6b within this session); blob SHAs
  were re-verified against the live head right before the run.
- Local mirror `~/workspace/tnn-lab` carries uncommitted extras
  (evidence dirs, `rc_trial_linux`, `il_trial_linux` binaries) — build used only
  committed sources.
