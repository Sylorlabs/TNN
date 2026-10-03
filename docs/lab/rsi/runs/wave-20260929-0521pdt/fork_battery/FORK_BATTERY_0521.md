# FORK_BATTERY_0521.md

Wave: wave-20260929-0521pdt. Verdict: CONFIRM [NEW] as a process confirmation
(toolchain and extraction stability only). Judge: JUDGE_0521.md (M1).

Execution: full fresh run pinned to run-start commit
d2fdf1225ec973e1e07082af6b067fd1525cb643, driver batch_0521.sh (faithful frozen
driver; pure shell, git, sha256sum; zero Python), run_one.sh byte-identical to the
frozen run_one.sh (sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978
on both copies), harness binary sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
re-verified byte-identical to the frozen instrument (re-verified, not rebuilt from
source this wave). Scratch: ~/workspace/fb0521pdt/E/ (65 per-entry RESULT.txt files; driver exit 0).

Counts: 65 named entries, 63 PASS, 0 FAIL, 2 UNTESTABLE. 52 unique commits
recomputed from this wave's own table per the standing hygiene rule.
LIVE entries (2): arch-wave-20260929-0221pdt at d2fdf1225 (newly enumerated archive),
local-tnn-native-lab at d2fdf1225 (run-start tip). FIXTURE: 63, including the
renamed local-0221pdt-tip at a014dc1d9 (was LIVE at 0221pdt; rename declared in
ENUMERATION_MANIFEST_0521.md) and the former LIVE entry arch-wave-20260928-2321pdt
at a014dc1d9 (moved to fixture, name kept).
Duplicate groups (10): bd309787 (wt-forktest-tnn-native-lab, wt-wave3-probe,
wt-wave3-senses, wt-wave3-trades); 99143222 (rh-reorg-phase-0-1, wt-forktest-reorg,
rh-pull-3-head); f875b341 (rh-wg-freeze, wt-forktest-wg-freeze); d2fdf122
(arch-wave-20260929-0221pdt, local-tnn-native-lab); c368b8e1 (exp-sensory,
wt-exp-sensory); bedf8b4a (origin-tnn-native-lab-rt, origin-tnn-native-lab-live);
a2a36e65 (exp2, wt-exp2); a014dc1d (arch-wave-20260928-2321pdt, local-0221pdt-tip);
3947dca1 (wave-debate-session-1-backup, wt-forktest-debate-backup); 1010a63c
(exp1, wt-exp1).

Uniform evidence on all 63 tested: znc pin 498abcb5 (0 pin divergence); probe sha
3b29aa06; b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS; NEG1 E0002 hit 63/63;
NEG2 char-1 discrimination 63/63; probe_run_stdout R32_ZNC_PROBE_OK 63/63;
harness_verdict_pass_count 1 on 63/63.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and rh-pull-2-head at 4b76bb59
(non-TNN research-doc trees, pinned toolchain path absent, git show exit 128,
twenty-one waves running).

Recorded gaps: batch_0521.log carries only the batch-exit trailer (driver
execution trace is the 65 per-entry RESULT.txt files; verdicts rest on those,
verified by the tally above).

Remote: origin/tnn-native-lab bedf8b4a unchanged at run start and close (read-only
ls-remote plus a git fetch that returned zero new commits); HEAD ref -> 27a4271f
unchanged. Local HEAD d2fdf1225 static during the run (the pin equals the live
tip, so the battery certifies the current tips directly with no pin gap).

The 1721pdt probe-loss FAIL stays closed (repair 37d1d3cab is an ancestor of the pin;
toolchain files intact).

Scope stamp: certifies toolchain and extraction stability only, not the contents of
the tested commits. No future wave may cite this run as evidence that the tip's
contents are good. No transitive claim about the overnight SEM-L3 session's sims or
verdicts may ride this verdict.

No em-dashes used in this document.
