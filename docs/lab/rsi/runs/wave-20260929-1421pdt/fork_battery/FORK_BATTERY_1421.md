# FORK_BATTERY_1421.md

Wave: wave-20260929-1421pdt. Verdict: CONFIRM [NEW] as a process confirmation
(toolchain and extraction stability only).

Execution: full fresh run pinned to run-start commit
d18f7f68d3792c58346861b89eab374c2e728ef0, driver batch_1421.sh (faithful
frozen driver derived from batch_0821.sh by mechanical edit; pure shell, git,
sha256sum; zero Python), run_one.sh byte-identical to the frozen run_one.sh
(sha256 4c2fadfc104548fb9c8a13c417e90d96991637030734851dd6ca4471a037e978),
harness binary sha256 a2e6284c5c45cfd65c7e0f974497512f4603f39bdac5bffdcefcdba0f9f4ef66
re-verified byte-identical to the frozen instrument (re-verified, not
rebuilt from source this wave). Scratch: ~/workspace/fb1421pdt/E/ (71
per-entry RESULT.txt files; driver exit 0).

Counts: 71 named entries, 69 PASS, 0 FAIL, 2 UNTESTABLE.
LIVE entries (2): arch-wave-20260929-1121pdt at d18f7f68d (newly enumerated
archive, created this wave to pin the 1121pdt partial-evidence tip),
local-tnn-native-lab at d18f7f68d (run-start tip); both LIVE entries extract
the same commit.
FIXTURE: 69, including the renamed local-1121pdt-tip at 5f86e6cb2 (was LIVE
at 1121pdt; rename declared in ENUMERATION_MANIFEST_1421.md) and the former
LIVE entry arch-wave-20260929-0821pdt at 5f86e6cb2 (moved to fixture, name
kept).

Uniform evidence on all 69 tested: znc pin 498abcb5 (0 pin divergence);
probe sha 3b29aa06 (0 divergence); b1/b2/b3 PASS, b1_cmp/b2_bin_cmp PASS;
NEG1 E0002 hit 69/69; NEG2 char-1 discrimination 69/69;
probe_run_stdout R32_ZNC_PROBE_OK 69/69; harness_verdict_pass_count 1 on
69/69.

UNTESTABLEs (2, expected): rh-pull-1-head at 5802fec8 and rh-pull-2-head at
4b76bb59 (non-TNN research-doc trees, pinned toolchain path absent, git show
exit 128, twenty-four waves running).

Per-entry results: branch name, commit SHA, and verdict are recorded in each
~/workspace/fb1421pdt/E/<entry>/RESULT.txt file; the ref field pins the exact
commit tested. The full per-entry tally (69 PASS / 2 UNTESTABLE) was taken
from those files; zero FAILs, so no "what broke" entries to report.

Duplicate SHA groups (12): bd309787 (wt-forktest-tnn-native-lab,
wt-wave3-probe, wt-wave3-senses, wt-wave3-trades); 99143222
(rh-reorg-phase-0-1, wt-forktest-reorg, rh-pull-3-head); f875b341
(rh-wg-freeze, wt-forktest-wg-freeze); d2fdf122 (arch-wave-20260929-0221pdt,
local-0521pdt-tip); c368b8e1 (exp-sensory, wt-exp-sensory); bedf8b4a
(origin-tnn-native-lab-rt, origin-tnn-native-lab-live); a2a36e65 (exp2,
wt-exp2); a014dc1d (arch-wave-20260928-2321pdt, local-0221pdt-tip);
3947dca1 (wave-debate-session-1-backup, wt-forktest-debate-backup);
1010a63c (exp1, wt-exp1); 5f86e6cb2 (arch-wave-20260929-0821pdt,
local-1121pdt-tip; new duplicate group this wave, both fixture);
d18f7f68d (arch-wave-20260929-1121pdt, local-tnn-native-lab; new duplicate
group this wave, both LIVE).

Remote: origin/tnn-native-lab bedf8b4a unchanged at run start (read-only
ls-remote); HEAD ref -> 27a4271f unchanged. Local HEAD moved during the run
only by this wave's own prereg-freeze commit (pinned-commit discipline:
mid-battery lane commits inert; the battery certifies the run-start tip
directly).

Scope stamp: not evidence that the tip's contents are good; no transitive
claim about the 1121pdt partial evidence or this wave's causal2 re-run rides
this verdict. The 1121pdt battery CONFIRM (67 PASS / 2 UNTESTABLE, debated
this wave as M2 on the intact inherited evidence) is superseded by this
fresh run for process-confirmation purposes.

No em-dashes in wave documentation. No Python anywhere in loop work.
