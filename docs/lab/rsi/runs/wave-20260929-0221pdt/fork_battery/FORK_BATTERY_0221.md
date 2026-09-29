# FORK_BATTERY_0221.md

Wave: wave-20260929-0221pdt. Verdict: CONFIRM [NEW] as a process confirmation
(toolchain and extraction stability only). Judge: JUDGE_0221.md (M1).

Execution: full fresh run pinned to run-start commit
a014dc1d96d0935f4e4d53888b3e488e3ce1f459, driver batch_0221.sh (faithful frozen
driver; pure shell, git, sha256sum; zero Python), run_one.sh byte-identical to the
frozen run_one.sh (sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978
on both copies), harness binary sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
re-verified byte-identical to the frozen instrument (re-verified, not rebuilt from
source this wave). Scratch: ~/workspace/fb0221pdt/E/ (63 per-entry RESULT.txt files; driver exit 0).

Counts: 63 named entries, 61 PASS, 0 FAIL, 2 UNTESTABLE. 51 unique commits
recomputed from this wave's own table per the standing hygiene rule.
LIVE entries (2): arch-wave-20260928-2321pdt at a014dc1d9 (newly enumerated archive),
local-tnn-native-lab at a014dc1d9 (run-start tip). FIXTURE: 61, including the
renamed local-2321pdt-tip at fab33cb4c (was LIVE at 2321pdt; rename declared in
ENUMERATION_MANIFEST_0221.md).
Duplicate groups (9): 1010a63c (exp1, wt-exp1); 3947dca1 (wave-debate-session-1-backup,
wt-forktest-debate-backup); 99143222 (rh-reorg-phase-0-1, wt-forktest-reorg,
rh-pull-3-head); a014dc1d (arch-wave-20260928-2321pdt, local-tnn-native-lab);
a2a36e65 (exp2, wt-exp2); bd309787 (wt-forktest-tnn-native-lab,
wt-wave3-probe, wt-wave3-senses, wt-wave3-trades); bedf8b4a (origin-tnn-native-lab-rt,
origin-tnn-native-lab-live); c368b8e1 (exp-sensory, wt-exp-sensory); f875b341
(rh-wg-freeze, wt-forktest-wg-freeze).

Uniform evidence on all 61 tested: znc pin 498abcb5 (0 pin divergence); probe sha
3b29aa06; b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS; NEG1 E0002 hit 61/61;
NEG2 char-1 discrimination 61/61; probe_run_stdout R32_ZNC_PROBE_OK 61/61.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and rh-pull-2-head at 4b76bb59
(non-TNN research-doc trees, pinned toolchain path absent, git show exit 128,
twenty waves running).

Recorded gaps: batch_0221.log is empty (2 lines: only the batch-exit trailer the
coordinator appended), so no driver execution trace survives; verdicts rest on the
63 verified per-entry RESULT.txt files.

Remote: origin/tnn-native-lab bedf8b4a unchanged at run start and close (read-only
ls-remote); HEAD ref -> 27a4271f unchanged. Local HEAD a014dc1d9 static during the run
(the pin equals a live tip, so the battery certifies the current tips directly with
no pin gap).

The 1721pdt probe-loss FAIL stays closed (repair 37d1d3cab is an ancestor of the pin;
toolchain files intact).

Ref-listing anomaly: at run start a ref named tnn-native-lab-wave-archive-20260928-2321pdt
(short name) appeared in ref listings but never resolved and later vanished; see
ENUMERATION_MANIFEST_0221.md. Not evidence; no entry depended on it.

Scope stamp: certifies toolchain and extraction stability only, not the contents of
the tested commits. No future wave may cite this run as evidence that the tip's
contents are good. No transitive claim about the overnight SEM-L3 session's sims or
verdicts may ride this verdict.
