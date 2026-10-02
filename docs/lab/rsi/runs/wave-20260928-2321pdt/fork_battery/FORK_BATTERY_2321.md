# FORK_BATTERY_2321.md

Wave: wave-20260928-2321pdt. Verdict: CONFIRM [NEW] as a process confirmation
(toolchain and extraction stability only). Judge: JUDGE_2321.md (M1).

Execution: full fresh run pinned to run-start commit
fab33cb4ca97eaa48aba2e2834287827af913098, driver batch_2321.sh (faithful frozen
driver; pure shell, git, sha256sum; zero Python), run_one.sh byte-identical to the
frozen run_one_2021.sh, harness binary sha256 a2e6284c re-verified byte-identical to
the frozen instrument (re-verified, not rebuilt from source this wave). Scratch:
~/workspace/fb2321pdt/E/ (61 per-entry RESULT.txt files; driver exit 0).

Counts: 61 named entries, 59 PASS, 0 FAIL, 2 UNTESTABLE. 50 unique commits
recomputed from this wave's own verdict table per the standing hygiene rule.
LIVE entries (2): arch-wave-20260928-2021pdt at 345daa604 (newly enumerated archive),
local-tnn-native-lab at fab33cb4c (run-start tip). FIXTURE: 59.
Duplicate groups (8): 1010a63c3 (exp1, wt-exp1); 3947dca1a (wave-debate-session-1-backup,
wt-forktest-debate-backup); 991432226 (rh-reorg-phase-0-1, wt-forktest-reorg,
rh-pull-3-head); a2a36e65 (exp2, wt-exp2); bd3097874 (wt-forktest-tnn-native-lab,
wt-wave3-probe, wt-wave3-senses, wt-wave3-trades); bedf8b4a (origin-tnn-native-lab-rt,
origin-tnn-native-lab-live); c368b8e1 (exp-sensory, wt-exp-sensory); f875b341
(rh-wg-freeze, wt-forktest-wg-freeze).

Uniform evidence on all 59 tested: znc pin 498abcb5 (0 pin divergence); probe sha
3b29aa06; b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS; NEG1 E0002 hit; NEG2 char-1
discrimination; probe_run_stdout R32_ZNC_PROBE_OK.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and rh-pull-2-head at 4b76bb59
(non-TNN research-doc trees, pinned toolchain path absent, git show exit 128,
nineteen waves running).

Recorded gaps: batch_2321.log is empty (0 lines), so no driver execution trace
survives; verdicts rest on the 61 verified per-entry RESULT.txt files.

Remote: origin/tnn-native-lab bedf8b4a unchanged at run start and close (read-only
ls-remote); HEAD ref -> 27a4271f unchanged. Local HEAD fab33cb4c static during the run
(the pin equals a live tip, so the battery certifies the current tips directly with
no pin gap).

The 1721pdt probe-loss FAIL stays closed (repair 37d1d3cab is an ancestor of the pin;
toolchain files intact).

Scope stamp: certifies toolchain and extraction stability only, not the contents of
the tested commits. No future wave may cite this run as evidence that the tip's
contents are good. No transitive claim about the overnight SEM-L3 session's sims or
verdicts may ride this verdict.
