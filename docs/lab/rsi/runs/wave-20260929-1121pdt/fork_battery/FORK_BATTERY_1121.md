# FORK_BATTERY_1121.md

Wave: wave-20260929-1121pdt. Verdict: CONFIRM [NEW] as a process confirmation
(toolchain and extraction stability only). Judge: JUDGE_1121.md (M2).

Execution: full fresh run pinned to run-start commit
5f86e6cb2eaedb115235e4af52684a44b7c6eb36, driver batch_1121.sh (faithful frozen
driver; pure shell, git, sha256sum; zero Python), run_one.sh byte-identical to the
frozen run_one.sh (sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978
on both copies), harness binary sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
re-verified byte-identical to the frozen instrument (re-verified, not rebuilt from
source this wave). Scratch: ~/workspace/fb1121pdt/E/ (69 per-entry RESULT.txt files; driver exit 0).

Counts: 69 named entries, 67 PASS, 0 FAIL, 2 UNTESTABLE. 55 unique commits
recomputed from this wave's own table per the standing hygiene rule.
LIVE entries (2): arch-wave-20260929-0821pdt at 5f86e6cb2 (newly enumerated archive),
local-tnn-native-lab at 5f86e6cb2 (run-start tip); both LIVE entries extract the same
commit, since the 0821pdt archive was created at the wave-end judge commit. FIXTURE: 67, including the
renamed local-0821pdt-tip at d24eda8b (was LIVE at 0821pdt; rename declared in
ENUMERATION_MANIFEST_1121.md) and the former LIVE entry arch-wave-20260929-0521pdt
at 2e9326e6 (moved to fixture, name kept).
Duplicate groups (11): bd309787 (wt-forktest-tnn-native-lab, wt-wave3-probe,
wt-wave3-senses, wt-wave3-trades); 99143222 (rh-reorg-phase-0-1, wt-forktest-reorg,
rh-pull-3-head); f875b341 (rh-wg-freeze, wt-forktest-wg-freeze); d2fdf122
(arch-wave-20260929-0221pdt, local-0521pdt-tip); c368b8e1 (exp-sensory,
wt-exp-sensory); bedf8b4a (origin-tnn-native-lab-rt, origin-tnn-native-lab-live);
a2a36e65 (exp2, wt-exp2); a014dc1d (arch-wave-20260928-2321pdt, local-0221pdt-tip);
3947dca1 (wave-debate-session-1-backup, wt-forktest-debate-backup); 1010a63c
(exp1, wt-exp1); 5f86e6cb2 (arch-wave-20260929-0821pdt, local-tnn-native-lab;
new duplicate group this wave, both LIVE).

Uniform evidence on all 67 tested: znc pin 498abcb5 (0 pin divergence); probe sha
3b29aa06 (0 divergence); b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS; NEG1 E0002 hit
67/67 (neg1_ok PASS, driver compile exit 1, check exit 1); NEG2 char-1
discrimination 67/67 (neg2_differs_at_char1 PASS); probe_run_stdout R32_ZNC_PROBE_OK
67/67; harness_verdict_pass_count 1 on 67/67.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and rh-pull-2-head at 4b76bb59
(non-TNN research-doc trees, pinned toolchain path absent, git show exit 128,
twenty-three waves running).

Per-entry results: branch name, commit SHA, and verdict are recorded in each
~/workspace/fb1121pdt/E/<entry>/RESULT.txt file; the ref field pins the exact
commit tested. The full per-entry tally (67 PASS / 2 UNTESTABLE, short SHAs)
was taken from those files; zero FAILs, so no "what broke" entries to report.

Recorded gaps: batch_1121.log carries only the driver exit trailer (driver
execution trace is the 69 per-entry RESULT.txt files; verdicts rest on those,
verified by the tally above).

Setup anomaly (documented in ENUMERATION_MANIFEST_1121.md): the copied batch_1121.sh
lacked the executable bit; the first launch failed at exit 126 before any entry ran.
The bit was set and the battery re-run from scratch. No verdict rests on the failed launch.

Remote: origin/tnn-native-lab bedf8b4a unchanged at run start (read-only
ls-remote); HEAD ref -> 27a4271f unchanged. Local HEAD static at the pin during the
run for the battery's purposes (pinned-commit discipline: mid-battery lane commits inert;
the battery certifies the run-start tip directly).

The 1721pdt probe-loss FAIL stays closed (repair 37d1d3cab is an ancestor of the pin;
toolchain files intact).

Scope stamp: certifies toolchain and extraction stability only, not the contents of
the tested commits. No future wave may cite this run as evidence that the tip's
contents are good. No transitive claim about any overnight session's sims or
verdicts rides this verdict.

No em-dashes used in this document.
